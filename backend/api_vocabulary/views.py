from django.core.files.base import ContentFile  # Módulo para manejar archivos en Django
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import VocabularyWord
from .serializers import VocabularyWordSerializer
from openai import OpenAI
import os
import re  # Módulo para expresiones regulares para buscar patrones en cadenas de texto ?
from deep_translator import GoogleTranslator  # Módulo para traducir texto
from io import BytesIO # Módulo para manejar flujos de bytes ?
from gtts import gTTS  # Módulo para convertir texto a voz

class VocabularyWordViewSet(viewsets.ModelViewSet):
    queryset = VocabularyWord.objects.all()
    serializer_class = VocabularyWordSerializer

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

        # Recibir idiomas del frontend o usar inglés/español por defecto
        source_lang = request.data.get("source_lang", "en")
        target_lang = request.data.get("target_lang", "es")

        # Instrucción mejorada para OpenAI
        prompt = (
            f"Dime qué tipo de palabra es '{word.word}' en inglés (por ejemplo: noun, verb, adjective, etc.) "
            f"y tradúcela al {target_lang} usando el formato: (abreviación) traducción.\n"
            f"Luego, genera una frase de ejemplo corta en inglés usando esa palabra en contexto.\n"
            f"Devuelve la respuesta separada por línea así:\n"
            f"Traducción: (n) tabla\n"
            f"Ejemplo: I waxed my surfboard before hitting the waves."
        )

        try:
            client = self.get_openai_client()
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Eres un asistente para estudiantes que genera vocabulario y frases con contexto."},
                    {"role": "user", "content": prompt}
                ]
            )

            # Procesar respuesta de OpenAI
            content = response.choices[0].message.content.strip()
            lines = content.splitlines()

            translation_line = next((line for line in lines if line.lower().startswith("traducción:")), "")
            example_line = next((line for line in lines if line.lower().startswith("ejemplo:")), "")

            translation = translation_line.replace("Traducción:", "").strip()
            example_sentence = example_line.replace("Ejemplo:", "").strip()

            # Traducir frase con contexto
            example_translation = GoogleTranslator(source=source_lang, target=target_lang).translate(text=example_sentence)

            # Guardar en la base de datos
            word.translation = translation
            word.example_sentence = example_sentence
            word.example_translation = example_translation
            word.save()

            return Response({
                "translation": translation,
                "example_sentence": example_sentence,
                "example_translation": example_translation,
                "message": "Frase y traducción generadas correctamente."
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Error en la generación de la frase: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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
    
    @action(detail=True, methods=["post"])
    def generate_audio_sentence(self, request, pk=None):
        word = self.get_object()

        try:
            # Verificar que haya una frase de ejemplo
            if not word.example_sentence:
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