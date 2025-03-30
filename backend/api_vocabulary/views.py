from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import VocabularyWord
from .serializers import VocabularyWordSerializer
from openai import OpenAI
import os
import re  # Módulo para expresiones regulares para buscar patrones en cadenas de texto
from deep_translator import GoogleTranslator  # Módulo para traducir texto

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

        # Recibimos los idiomas del request enviado desde el FRONTEND o se usa valores por defecto
        source_lang = request.data.get("source_lang", "en")
        target_lang = request.data.get("target_lang", "es")

        prompt = (
            f"Crea una frase de ejemplo en inglés para la palabra '{word.word}' "
            f"(tipo de palabra: {word.part_of_speech}) que significa '{word.translation}'."
        )

        try:
            client = self.get_openai_client()
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Eres un generador de frases de ejemplo para estudiantes de idiomas."},
                    {"role": "user", "content": prompt}
                ]
            )
            generated_sentence = response.choices[0].message.content.strip()

            # Traducir la frase generada automaticamente
            translated_sentence = GoogleTranslator(source=source_lang, target=target_lang).translate(generated_sentence)

            # Traducir la palabra
            translated_word = GoogleTranslator(source=source_lang, target=target_lang).translate(word.word)
            
            # Combinar con el part_of_speech para generar la traducción completa
            translation_full = f"{word.part_of_speech} {translated_word}"

            # Se guardan los resultados en la base de datos
            word.example_sentence = generated_sentence
            word.example_translation = translated_sentence
            word.translation = translation_full
            word.save()

            return Response({
                "example_sentence": generated_sentence,
                "example_translation": translated_sentence,
                "translation": translation_full,
                "message": "Frase y traducción generadas correctamente."
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Error al generar la frase: {str(e)}"},
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