from django.http import FileResponse    # Módulo para manejar respuestas de archivos (sera temporal)
from django.core.files.base import ContentFile  # Módulo para manejar archivos en Django
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly  # Permiso para verificar autenticación
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import VocabularyWord, Language
from rest_framework import serializers
from .serializers import VocabularyWordSerializer, LanguageSerializer
from openai import OpenAI
import os
import re  # Módulo para expresiones regulares para buscar patrones en cadenas de texto ?
from deep_translator import GoogleTranslator  # Módulo para traducir texto
from io import BytesIO # Módulo para manejar flujos de bytes ?
from gtts import gTTS  # Módulo para convertir texto a voz
from .audio_utils import generate_audio_for_word, generate_audio_for_example

class VocabularyWordViewSet(viewsets.ModelViewSet):
    queryset = VocabularyWord.objects.none()    # seteado como .none() porque estamos personalizando dinámicamente con get_queryset()
    serializer_class = VocabularyWordSerializer
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden acceder a esta vista

    def get_queryset(self):
        return VocabularyWord.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        word_text = serializer.validated_data["word"].strip().lower()

        # Verificar si ya la tiene el usuario actual
        if VocabularyWord.objects.filter(user=self.request.user, word__iexact=word_text).exists():
            raise serializers.ValidationError({
                "word": "Esta palabra ya fue creada por ti."
            })

        # Buscar si existe una palabra completa de otro usuario
        existing = VocabularyWord.objects.filter(
            word__iexact=word_text,
            translation__isnull=False,
            example_sentence__isnull=False,
            example_translation__isnull=False,
            audio_word__isnull=False,
            audio_sentence__isnull=False,
        ).exclude(user=self.request.user).first()

        if existing:
            serializer.save(
                user=self.request.user,
                translation=existing.translation,
                example_sentence=existing.example_sentence,
                example_translation=existing.example_translation,
                audio_word=existing.audio_word,
                audio_sentence=existing.audio_sentence,
                image_url=existing.image_url,
            )
        else:
            serializer.save(user=self.request.user)


    # Diccionario de abreviaciones gramaticales
    POS_ABBREVIATIONS = {
        "noun": "(n)",
        "verb": "(v.)",
        "adjective": "(adj.)",
        "adverb": "(adv.)",
        "pronoun": "(pron.)",
        "preposition": "(prep.)",
        "conjunction": "(conj.)",
        "interjection": "(interj.)"
    }

    def get_openai_client(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise Exception("La API Key de OpenAI no está definida en las variables de entorno.")
        return OpenAI(api_key=api_key)

    @action(detail=True, methods=["post"])
    def generate_example(self, request, pk=None):
        word = self.get_object()
        
        # Verifica que los idiomas esten definidos
        if not word.source_lang or not word.target_lang:
            return Response(
                {"error": "Faltan los idiomas 'source_lang' o 'target_lang' para esta palabra."},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Usamos directamente los codigos de idioma del modelo (base de datos)
        source_lang = word.source_lang.code
        target_lang = word.target_lang.code

        prompt = (
            f"Para la palabra en '{source_lang}' '{word.word}', genera:\n"
            f"1. Una oración de ejemplo (Example sentence).\n"
            f"2. Una traducción directa en '{target_lang}' con tipo gramatical (Translation), en el formato (abreviatura) traducción.\n"
            f"Ejemplo:\n"
            f"Example sentence: I borrowed a book from the library.\n"
            f"Translation: (v.) prestar"
        )

        try:
            client = self.get_openai_client()
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Eres un asistente que ayuda a aprender vocabulario con frases y traducciones."},
                    {"role": "user", "content": prompt}
                ]
            )

            content = response.choices[0].message.content.strip()
            lines = content.split('\n')

            example_sentence = ""
            translation = ""

            for line in lines:
                if "example sentence" in line.lower():
                    example_sentence = line.split(":", 1)[-1].strip()
                elif "translation" in line.lower():
                    translation = line.split(":", 1)[-1].strip()

            if not example_sentence or not translation:
                return Response({
                    "error": "No se pudo extraer la oración de ejemplo o la traducción de la respuesta de OpenAI.",
                    "respuesta_raw": content
                }, status=status.HTTP_400_BAD_REQUEST)

            # Traducir la oración de ejemplo
            translated_sentence = GoogleTranslator(source=source_lang, target=target_lang).translate(example_sentence)

            # Guardar resultados en el modelo
            word.example_sentence = example_sentence
            word.example_translation = translated_sentence
            word.translation = translation
            word.save()

            return Response({
                "translation": translation,
                "example_sentence": example_sentence,
                "example_translation": translated_sentence,
                "message": "Frase y traducción generadas correctamente."
            })

        except Exception as e:
            return Response({
                "error": f"Error al generar la frase: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=["post"])
    def generate_part_of_speech(self, request, pk=None):
        word = self.get_object()

        prompt = (
            f"¿Qué tipo de palabra (por ejemplo, noun, verb, adjective, adverb, etc.) "
            f"es '{word.word}' en inglés? Responde solo con una palabra en inglés."
        )

        try:
            client = self.get_openai_client()
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Eres un asistente lingüístico que identifica tipos gramaticales."},
                    {"role": "user", "content": prompt}
                ]
            )

            raw_result = response.choices[0].message.content.strip().lower()
            match = re.search(
                r"\b(noun|verb|adjective|adverb|pronoun|preposition|conjunction|interjection)\b", raw_result
            )
            result = match.group(1) if match else None
            abbreviation = self.POS_ABBREVIATIONS.get(result, "(?)")

            word.part_of_speech = abbreviation
            word.save()

            return Response({
                "part_of_speech": abbreviation,
                "original": result or raw_result,
                "message": "Tipo de palabra generado correctamente."
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Error al generar el tipo de palabra: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    '''    
    @action(detail=True, methods=["post"])
    def generate_audio_word(self, request, pk=None):
        word = self.get_object()

        try:
            if not word.word:
                return Response({
                    "error": "La palabra está vacía. No se puede generar el audio."
                }, status=status.HTTP_400_BAD_REQUEST)

            # Usamos gTTS (requiere conexión a internet)
            # 🔄 Este método es temporal y será reemplazado por Google Cloud TTS en producción
            tts = gTTS(text=word.word, lang="en")
            audio_buffer = BytesIO()
            tts.write_to_fp(audio_buffer)

            audio_buffer.seek(0)

            filename = f"{word.word}_word.mp3"
            word.audio_word.save(filename, ContentFile(audio_buffer.read()))
            word.save()

            return Response({
                "message": "Audio de la palabra generado correctamente con gTTS.",
                "filename": filename
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "error": f"Error al generar el audio de la palabra con gTTS: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    '''
    @action(detail=True, methods=["post"])
    def generate_audio_word(self, request, pk=None):
        word = self.get_object()

        if not word.word:
            return Response({
                "error": "La palabra está vacía. No se puede generar el audio."
            }, status=status.HTTP_400_BAD_REQUEST)

        # ✏️ TEMPORAL PARA PRUEBAS: Genera automáticamente el audio MP3 de la palabra en /media/audio/
        # Este bloque será reemplazado por Google Cloud TTS en producción real.
        generate_audio_for_word(word)

        return Response({
            "message": "Audio de la palabra generado correctamente con gTTS."
        })
    
    '''
    @action(detail=True, methods=["post"])
    def generate_audio_sentence(self, request, pk=None):
        word = self.get_object()

        try:
            # Verificar que haya una frase de ejemplo
            if not word.example_sentence or word.example_sentence.strip() == "":
                return Response({
                    "error": "La frase de ejemplo (example_sentence) está vacía. Debes generarla primero."
                }, status=status.HTTP_400_BAD_REQUEST)

            # Usamos gTTS (requiere conexión a internet)
            # 🔄 Esta implementación es temporal para desarrollo local y pruebas.
            # 🚀 Más adelante será reemplazada por Google Cloud TTS en producción.
            tts = gTTS(text=word.example_sentence, lang="en")
            audio_buffer = BytesIO()
            tts.write_to_fp(audio_buffer)

            # Volver al inicio del buffer para leer el contenido
            audio_buffer.seek(0)

            filename = f"{word.word}_sentence.mp3"
            word.audio_sentence.save(filename, ContentFile(audio_buffer.read()))
            word.save()

            return Response({
                "message": "Audio de la frase generado correctamente con gTTS.",
                "filename": filename
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "error": f"Error al generar el audio con gTTS: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    '''
    @action(detail=True, methods=["post"])
    def generate_audio_sentence(self, request, pk=None):
        word = self.get_object()

        if not word.example_sentence:
            return Response({
                "error": "La frase de ejemplo está vacía. No se puede generar el audio."
            }, status=status.HTTP_400_BAD_REQUEST)

        # ✏️ TEMPORAL PARA PRUEBAS: Genera automáticamente el audio MP3 del ejemplo en /media/audio/
        # Este bloque será reemplazado por Google Cloud TTS en producción real.
        generate_audio_for_example(word)

        return Response({
            "message": "Audio de la frase generado correctamente con gTTS."
        })
    
    # Endpoint temporal para descargar el audio de la palabra
    @action(detail=True, methods=["get"])
    def download_audio_word(self, request, pk=None):
        word = self.get_object()
        if not word.audio_word:
            return Response({"error": "Este vocabulario no tiene audio generado aún."}, status=404)

        # ⛔️ TEMPORAL – eliminar en producción real cuando se use AWS S3
        return FileResponse(word.audio_word.open(), content_type='audio/mpeg')


    # Endpoint temporal para descargar el audio de la oración
    @action(detail=True, methods=["get"])
    def download_audio_sentence(self, request, pk=None):
        word = self.get_object()
        if not word.audio_sentence:
            return Response({"error": "Este vocabulario no tiene audio de oración aún."}, status=404)

        # ⛔️ TEMPORAL – eliminar en producción real cuando se use AWS S3
        return FileResponse(word.audio_sentence.open(), content_type='audio/mpeg')
    
class LanguageViewSet(viewsets.ReadOnlyModelViewSet):  # 🔒 Solo lectura por ahora
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]