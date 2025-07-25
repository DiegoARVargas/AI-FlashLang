from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from django.http import FileResponse, Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from .permissions import IsAuthenticatedAndVerified
from rest_framework.parsers import MultiPartParser
from django.db.models import Q
from .models import UserVocabularyWord, SharedVocabularyWord, CustomWordContent, Language
from .serializers import UserVocabularyWordSerializer, LanguageSerializer
from django.db import IntegrityError, transaction
from openai import OpenAI
import os, io, csv, sys
import re
from google.cloud import translate_v2 as gcloud_translate
#from deep_translator import GoogleTranslator
from .audio_utils import generate_gtts_audio_for_word, generate_gtts_audio_for_sentence
from .anki_exporter import generate_apkg_for_user


class LanguageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = [IsAuthenticatedAndVerified]

class UserVocabularyWordViewSet(viewsets.ModelViewSet):
    queryset = UserVocabularyWord.objects.none()
    serializer_class = UserVocabularyWordSerializer
    permission_classes = [IsAuthenticatedAndVerified]

    def get_queryset(self):
        user = self.request.user
        queryset = UserVocabularyWord.objects.filter(user=user)

        deck = self.request.query_params.get('deck')
        word = self.request.query_params.get('word')

        if deck:
            queryset = queryset.filter(deck__iexact=deck)

        if word:
            queryset = queryset.filter(
                Q(shared_word__word__icontains=word) |
                Q(custom_content__word__icontains=word)
            )

        return queryset

    def perform_create(self, serializer):
        print("[LOG] perform_create ejecutado", file=sys.stderr)    # Debugging line
        validated = serializer.validated_data
        user = self.request.user

        word = validated.get("word")
        source_lang = validated.get("source_lang")
        target_lang = validated.get("target_lang")
        context = validated.get("context", None)

        if context and not self.request.user.is_premium:
            raise serializers.ValidationError({
                "context": "Este campo solo está disponible para usuarios premium."
            })

        if not word or not source_lang or not target_lang:
            raise serializers.ValidationError({"error": "Faltan campos obligatorios: 'word', 'source_lang' o 'target_lang'."})

        word = word.strip().lower()

        # 🧠 Premium: con contexto → flujo Custom
        if context:
            # Verifica si ya existe este custom exacto
            if CustomWordContent.objects.filter(
                word=word,
                source_lang=source_lang,
                target_lang=target_lang,
                context=context.strip()
            ).exists():
                raise serializers.ValidationError({
                    "word": "Ya existe una palabra personalizada con ese contexto."
                })

            # Crear y generar contenido
            custom = CustomWordContent.objects.create(
                word=word,
                source_lang=source_lang,
                target_lang=target_lang,
                context=context.strip()
            )
            self.generate_content_for_custom(custom)
            serializer.save(user=user, custom_content=custom)

        else:
            # 🔄 Reutilizable: flujo compartido (Shared)
            shared = SharedVocabularyWord.objects.filter(
                word=word,
                source_lang=source_lang,
                target_lang=target_lang
            ).first()

            if not shared:
                shared = SharedVocabularyWord.objects.create(
                    word=word,
                    source_lang=source_lang,
                    target_lang=target_lang
                )
                self.generate_content_for_shared(shared)

            # Verifica si el usuario ya la tiene
            if UserVocabularyWord.objects.filter(user=user, shared_word=shared).exists():
                raise serializers.ValidationError({
                    "word": "Ya tienes esta palabra en tu lista."
                })

            serializer.save(user=user, shared_word=shared)

    def get_openai_client(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise Exception("La API Key de OpenAI no está definida en las variables de entorno.")
        return OpenAI(api_key=api_key)
    
    def translate_with_google_cloud(self, text, source_lang, target_lang):
        client = gcloud_translate.Client()
        result = client.translate(text, source_language=source_lang, target_language=target_lang)
        return result['translatedText']

    def generate_content_for_shared(self, shared):
        print(f"[LOG] Generando contenido para palabra compartida: {shared.word}", file=sys.stderr) # Debugging line
        prompt = (
            f"You are an AI assistant helping users learn vocabulary through example sentences and direct translations.\n\n"
            f"Your task is to generate the following for the word **'{shared.word}'** in the source language **'{shared.source_lang.name}'**:\n\n"
            f"### FORMAT STRICTLY:\n"
            f"Example sentence:\n"
            f"<example_sentence_here>\n\n"
            f"Translation:\n"
            f"<only the translation of the word '{shared.word}' in '{shared.target_lang.name}', with the grammatical type abbreviated like (v.), (n), (adj.), etc.>\n\n"
            f"### RULES:\n"
            f"- The example sentence must be written in **{shared.source_lang.name}**.\n"
            f"- The translation must be in **{shared.target_lang.name}** and ONLY include the meaning of the word '{shared.word}' in this format: (v.) traducción, (n) traducción, etc.\n"
            f"- DO NOT include full sentence translations.\n"
            f"- DO NOT explain anything or ask any questions.\n"
            f"- DO NOT add any introductory or closing sentences.\n"
            f"- Just follow the FORMAT strictly and output the two blocks only.\n"
        )

        client = self.get_openai_client()
        print("[LOG] Llamando a OpenAI...", file=sys.stderr) # Debugging line
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un asistente que ayuda a aprender vocabulario con frases y traducciones."},
                {"role": "user", "content": prompt}
            ]
        )
        print("[LOG] Respuesta de OpenAI recibida", file=sys.stderr) # Debugging line

        content = response.choices[0].message.content.strip()
        print(f"[LOG] Contenido generado por OpenAI: {content}", file=sys.stderr) # Debugging line

        example_sentence, translation = self.extract_response_data(content)
        print(f"[LOG] Frase extraída: {example_sentence}", file=sys.stderr)  # Debugging line
        print(f"[LOG] Traducción extraída: {translation}", file=sys.stderr)  # Debugging line

        if not example_sentence or not translation:
            raise Exception(f"No se pudo extraer contenido de OpenAI. Respuesta: {content}")

        print("[LOG] Traduciendo frase con Google Translate...", file=sys.stderr)    # Debugging line      
        translated_sentence = self.translate_with_google_cloud(
            example_sentence, shared.source_lang.code, shared.target_lang.code
        )
        print(f"[LOG] Traducción generada: {translated_sentence}", file=sys.stderr)  # Debugging line

        shared.translation = translation
        shared.example_sentence = example_sentence
        shared.example_translation = translated_sentence

        # Generar audios
        print("[LOG] Generando audio de palabra y frase...", file=sys.stderr)    # Debugging line
        generate_gtts_audio_for_word(shared)
        generate_gtts_audio_for_sentence(shared)
        shared.save()
        print(f"[LOG] Proceso finalizado para: {shared.word}",file=sys.stderr)  # Debugging line

    def generate_content_for_custom(self, custom):
        print(f"[LOG] Generando contenido para palabra personalizada: {custom.word} con contexto: {custom.context}", file=sys.stderr)    # Debugging line
        prompt = (
            f"You are an AI assistant helping users learn vocabulary through example sentences and direct translations.\n\n"
            f"Your task is to generate the following for the word **'{custom.word}'** in the source language **'{custom.source_lang.name}'**, "
            f"with the usage context **'{custom.context}'**:\n\n"
            f"### FORMAT STRICTLY:\n"
            f"Example sentence:\n"
            f"<example_sentence_here>\n\n"
            f"Translation:\n"
            f"<only the translation of the word '{custom.word}' in '{custom.target_lang.name}', with the grammatical type abbreviated like (v.), (n), (adj.), etc.>\n\n"
            f"### RULES:\n"
            f"- The example sentence must be written in **{custom.source_lang.name}** and reflect the context: '{custom.context}'.\n"
            f"- The translation must be in **{custom.target_lang.name}** and ONLY include the meaning of the word '{custom.word}' in this format: (v.) traducción, (n) traducción, etc.\n"
            f"- DO NOT include full sentence translations.\n"
            f"- DO NOT explain anything or ask any questions.\n"
            f"- DO NOT add any introductory or closing sentences.\n"
            f"- Just follow the FORMAT strictly and output the two blocks only.\n"
        )

        client = self.get_openai_client()
        print("[LOG] Llamando a OpenAI...", file=sys.stderr) # Debugging line
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un asistente de vocabulario."},
                {"role": "user", "content": prompt}
            ]
        )
        print("[LOG] Respuesta de OpenAI recibida", file=sys.stderr) # Debugging line

        content = response.choices[0].message.content.strip()
        print(f"[LOG] Contenido generado por OpenAI: {content}", file=sys.stderr) # Debugging line
        
        example_sentence, translation = self.extract_response_data(content)
        print(f"[LOG] Frase extraída: {example_sentence}", file=sys.stderr)  # Debugging line
        print(f"[LOG] Traducción extraída: {translation}", file=sys.stderr)  # Debugging line

        print("[LOG] Traduciendo frase con Google Translate...", file=sys.stderr)    # Debugging line
        translated_sentence = self.translate_with_google_cloud(
            example_sentence, custom.source_lang.code, custom.target_lang.code
        )
        print(f"[LOG] Traducción generada: {translated_sentence}", file=sys.stderr)  # Debugging line

        custom.translation = translation
        custom.example_sentence = example_sentence
        custom.example_translation = translated_sentence

        print("[LOG] Generando audio de palabra y frase...", file=sys.stderr)    # Debugging line
        generate_gtts_audio_for_word(custom)
        generate_gtts_audio_for_sentence(custom)

        custom.save()
        print(f"[LOG] Proceso finalizado para: {custom.word}", file=sys.stderr)  # Debugging line

    def extract_response_data(self, content):
        """
        Extrae la oración de ejemplo y la traducción desde el contenido entregado por OpenAI.
        Se asegura de que la traducción sea corta y con formato (v.) palabra, y no una oración.
        """
        lines = content.strip().split("\n")
        example_sentence = ""
        translation = ""

        for i, line in enumerate(lines):
            lower = line.strip().lower()

            if "example sentence:" in lower:
                example_sentence = line.split(":", 1)[-1].strip()
                if not example_sentence and i + 1 < len(lines):
                    example_sentence = lines[i + 1].strip()

            elif "translation:" in lower:
                translation = line.split(":", 1)[-1].strip()
                if not translation and i + 1 < len(lines):
                    translation = lines[i + 1].strip()

        # Limpieza de símbolos
        example_sentence = example_sentence.strip("* ").strip()
        translation = translation.strip("* ").strip()

        # ⚠️ Validación: evitar que la traducción sea una oración completa
        # Si contiene más de 6 palabras o termina en punto, algo anda mal
        if len(translation.split()) > 6 or translation.endswith("."):
            print(f"[ERROR] Traducción inválida: '{translation}'", file=sys.stderr)  # Debugging line
            raise Exception(f"La traducción parece ser una oración completa: '{translation}'")

        # Corrección de formato duplicado: "piña (v.) piña"
        match = re.match(r"^(.+?)\s+\((.*?)\)\s+\1$", translation)
        if match:
            root, abbr = match.groups()
            translation = f"({abbr}) {root}"

        return example_sentence, translation
    
    @action(detail=False, methods=['get', 'post'], url_path='download-apkg', permission_classes=[IsAuthenticatedAndVerified])
    def download_apkg(self, request):
        user = request.user
        deck_name = request.query_params.get("deck_name", "").strip() or request.data.get("deck_name", "").strip()  # capturar desde la URL
        ids = request.data.get("ids")
        allow_duplicates = request.data.get("allow_duplicates", False)
        
        if ids and not isinstance(ids, list):
            return Response({"error": "El campo 'ids' debe ser una lista de enteros."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            apkg_path, final_deck_name = generate_apkg_for_user(
                user, 
                deck_name=deck_name, 
                ids=ids,
                allow_duplicates=bool(allow_duplicates)
            )
            filename = f"aiflashlang_{final_deck_name}.apkg"
            return FileResponse(open(apkg_path, 'rb'), as_attachment=True, filename=filename)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GenerateAudioView(APIView):
    permission_classes = [IsAuthenticatedAndVerified]

    def post(self, request, *args, **kwargs):
        word_id = request.data.get("word_id")
        if not word_id:
            return Response({"error": "Se requiere 'word_id'."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_word = UserVocabularyWord.objects.get(id=word_id, user=request.user)
        except UserVocabularyWord.DoesNotExist:
            return Response({"error": "Palabra no encontrada o no pertenece al usuario."}, status=status.HTTP_404_NOT_FOUND)

        content = user_word.custom_content if user_word.custom_content else user_word.shared_word

        try:
            generate_gtts_audio_for_word(content)
            generate_gtts_audio_for_sentence(content)
            content.save()
            return Response({"message": "Audios generados correctamente."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Error al generar audios: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class BulkUploadView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticatedAndVerified]

    def post(self, request):
        uploaded_file = request.FILES.get('file')
        if not uploaded_file or not uploaded_file.name.endswith('.csv'):
            return Response({'error': 'Debes subir un archivo .csv válido.'}, status=400)

        decoded_file = uploaded_file.read().decode('utf-8')
        csv_reader = csv.DictReader(io.StringIO(decoded_file))

        # ✅ Limpieza segura de encabezados
        cleaned_headers = [h.strip().replace('\ufeff', '').lower() for h in csv_reader.fieldnames]
        csv_reader.fieldnames = cleaned_headers

        expected_fields = {"word", "source_lang_code", "target_lang_code"}
        missing_fields = expected_fields - set(cleaned_headers)

        if missing_fields:
            return Response(
                {
                    "error": f"El archivo CSV debe tener los siguientes encabezados: {', '.join(expected_fields)}. "
                             f"Faltan: {', '.join(missing_fields)}"
                },
                status=400
            )

        rows = list(csv_reader)
        if len(rows) > 50:
            return Response({'error': 'No puedes subir más de 50 palabras por archivo.'}, status=400)

        creator = UserVocabularyWordViewSet()
        creator.request = request

        results = []
        for idx, row in enumerate(rows, start=2):  # empieza en 2 por encabezado

            word = row.get("word", "").strip().lower()
            source_lang_code = row.get("source_lang_code", "").strip().replace("\ufeff", "")
            target_lang_code = row.get("target_lang_code", "").strip().replace("\ufeff", "")
            deck = row.get("deck", "").strip() or "MyDeck"

            if not word or not source_lang_code or not target_lang_code:
                results.append({'line': idx, 'word': word, 'status': 'error', 'reason': 'Campos requeridos vacíos'})
                continue

            try:
                source_lang = Language.objects.get(code=source_lang_code)
                target_lang = Language.objects.get(code=target_lang_code)
            except Language.DoesNotExist:
                results.append({'line': idx, 'word': word, 'status': 'error', 'reason': 'Código de idioma inválido'})
                continue

            try:
                with transaction.atomic():
                    shared = SharedVocabularyWord.objects.filter(
                        word=word,
                        source_lang=source_lang,
                        target_lang=target_lang
                    ).first()

                    if not shared:
                        shared = SharedVocabularyWord.objects.create(
                            word=word,
                            source_lang=source_lang,
                            target_lang=target_lang
                        )
                        creator.generate_content_for_shared(shared)

                    UserVocabularyWord.objects.get_or_create(
                        user=request.user,
                        shared_word=shared,
                        deck=deck
                    )
                    results.append({'line': idx, 'word': word, 'status': 'ok'})

            except Exception as e:
                results.append({'line': idx, 'word': word, 'status': 'error', 'reason': str(e)})

        success = sum(1 for r in results if r['status'] == 'ok')
        errors = [r for r in results if r['status'] == 'error']

        return Response({
            'message': 'Carga masiva completada.',
            'total': len(rows),
            'success': success,
            'errors': errors
        }, status=status.HTTP_207_MULTI_STATUS)
    
class BulkUploadTemplateView(APIView):
    permission_classes = [IsAuthenticatedAndVerified]

    def get(self, request):
        # Encabezados esperados por el sistema
        headers = ['word', 'source_lang_code', 'target_lang_code', 'deck']
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="bulk_upload_template.csv"'

        writer = csv.writer(response)
        writer.writerow(headers)  # Solo la fila de encabezados

        return response