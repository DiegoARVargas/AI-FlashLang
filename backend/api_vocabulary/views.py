from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import UserVocabularyWord, SharedVocabularyWord, CustomWordContent, Language
from .serializers import UserVocabularyWordSerializer, LanguageSerializer
from django.db import IntegrityError
from openai import OpenAI
import os
import re
from deep_translator import GoogleTranslator
from .audio_utils import generate_gtts_audio_for_word, generate_gtts_audio_for_sentence


class LanguageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer

class UserVocabularyWordViewSet(viewsets.ModelViewSet):
    queryset = UserVocabularyWord.objects.none()
    serializer_class = UserVocabularyWordSerializer
    permission_classes = [IsAuthenticated]

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

    def generate_content_for_shared(self, shared):
        prompt = (
            f"For the word '{shared.word}' in language '{shared.source_lang.code}', generate the following ONLY in English:\n"
            f"1. An example sentence using the word (start with 'Example sentence:')\n"
            f"2. A translation to '{shared.target_lang.code}' in the format: (v.) translate "
            f"(start with 'Translation:')\n"
            f"Always respond in English only."
        )

        client = self.get_openai_client()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un asistente que ayuda a aprender vocabulario con frases y traducciones."},
                {"role": "user", "content": prompt}
            ]
        )

        content = response.choices[0].message.content.strip()
        example_sentence, translation = self.extract_response_data(content)

        if not example_sentence or not translation:
            raise Exception(f"No se pudo extraer contenido de OpenAI. Respuesta: {content}")

        translated_sentence = GoogleTranslator(
            source=shared.source_lang.code,
            target=shared.target_lang.code
        ).translate(example_sentence)

        shared.translation = translation
        shared.example_sentence = example_sentence
        shared.example_translation = translated_sentence

        # Generar audios
        generate_gtts_audio_for_word(shared)
        generate_gtts_audio_for_sentence(shared)
        shared.save()

    def generate_content_for_custom(self, custom):
        prompt = (
            f"Para la palabra '{custom.word}' en el idioma '{custom.source_lang.code}', con el contexto '{custom.context}', "
            f"genera una respuesta en **inglés** que contenga:\n"
            f"1. Example sentence: Una oración de ejemplo que use la palabra en contexto.\n"
            f"2. Translation: Su traducción en '{custom.target_lang.code}' incluyendo el tipo gramatical "
            f"en formato (abreviación) traducción. Por ejemplo: (n) préstamo"
        )

        client = self.get_openai_client()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un asistente de vocabulario."},
                {"role": "user", "content": prompt}
            ]
        )
        content = response.choices[0].message.content.strip()
        example_sentence, translation = self.extract_response_data(content)
        translated_sentence = GoogleTranslator(source=custom.source_lang.code, target=custom.target_lang.code).translate(example_sentence)

        custom.translation = translation
        custom.example_sentence = example_sentence
        custom.example_translation = translated_sentence
        generate_gtts_audio_for_word(custom)
        generate_gtts_audio_for_sentence(custom)
        custom.save()

    def extract_response_data(self, content):
        """
        Extrae la oración de ejemplo y la traducción desde el contenido entregado por OpenAI.
        Limpia símbolos innecesarios y duplicados como '**' o duplicaciones como 'word (v) word'.
        """
        lines = content.strip().split("\n")
        example_sentence = ""
        translation = ""

        for line in lines:
            # Detectar oración de ejemplo
            if re.search(r"example sentence", line, re.IGNORECASE) or line.strip().startswith("1."):
                example_sentence = line.split(":", 1)[-1].strip()
            elif re.search(r"translation", line, re.IGNORECASE) or line.strip().startswith("2."):
                translation = line.split(":", 1)[-1].strip()

        # Limpieza de símbolos '**'
        example_sentence = example_sentence.lstrip("* ").strip()
        translation = translation.lstrip("* ").strip()

        # Limpieza de duplicación como 'ganar (v) ganar'
        match = re.match(r"^(.+?)\s+\((.*?)\)\s+\1$", translation)
        if match:
            root, abbr = match.groups()
            translation = f"({abbr}) {root}"

        return example_sentence, translation
    
class GenerateAudioView(APIView):
    permission_classes = [IsAuthenticated]

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