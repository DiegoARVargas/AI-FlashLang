import os
from io import BytesIO
from gtts import gTTS
from django.core.files.base import ContentFile

# 📁 Ruta donde se guardarán los audios en desarrollo y pruebas
# Django usará MEDIA_ROOT/audio/
AUDIO_DIR = "audio/"

def generate_audio_for_word(word_obj):
    """
    Genera un archivo de audio MP3 para la palabra (`word_obj.word`) usando gTTS.
    El archivo se guarda en word_obj.audio_word.
    """
    try:
        tts = gTTS(text=word_obj.word, lang="en")
        buffer = BytesIO()
        tts.write_to_fp(buffer)
        buffer.seek(0)

        filename = f"{word_obj.word}_word.mp3"
        word_obj.audio_word.save(filename, ContentFile(buffer.read()))
        word_obj.save()

    except Exception as e:
        raise Exception(f"Error al generar el audio de la palabra: {str(e)}")

def generate_audio_for_example(word_obj):
    """
    Genera un archivo de audio MP3 para la frase de ejemplo (`word_obj.example_sentence`) usando gTTS.
    El archivo se guarda en word_obj.audio_sentence.
    """
    try:
        tts = gTTS(text=word_obj.example_sentence, lang="en")
        buffer = BytesIO()
        tts.write_to_fp(buffer)
        buffer.seek(0)

        filename = f"{word_obj.word}_sentence.mp3"
        word_obj.audio_sentence.save(filename, ContentFile(buffer.read()))
        word_obj.save()

    except Exception as e:
        raise Exception(f"Error al generar el audio del ejemplo: {str(e)}")

# ⚠️ Este script es temporal. Será eliminado al migrar a almacenamiento externo (AWS S3).