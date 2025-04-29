# audio_utils.py
# Utilidades para generar audios con gTTS
# 🔄 Este módulo es temporal y será reemplazado por Google Cloud TTS en producción

from gtts import gTTS
from io import BytesIO
from django.core.files.base import ContentFile
from .models import VocabularyWord  # Necesario para acceder a source_lang y target_lang dinámicamente

def generate_gtts_audio_for_word(word: VocabularyWord):
    """
    Genera el audio de una palabra utilizando gTTS.
    Usa el idioma definido por source_lang.code del usuario.
    """
    lang_code = word.source_lang.code if word.source_lang else "en"

    tts = gTTS(text=word.word, lang=lang_code)
    audio_buffer = BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)

    filename = f"{word.word}_word.mp3"
    word.audio_word.save(filename, ContentFile(audio_buffer.read()))
    word.save()

    return filename

def generate_gtts_audio_for_sentence(word: VocabularyWord):
    """
    Genera el audio de la frase de ejemplo usando el idioma de origen seleccionado por el usuario.
    """
    lang_code = word.source_lang.code if word.source_lang else "en"

    tts = gTTS(text=word.example_sentence, lang=lang_code)
    audio_buffer = BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)

    filename = f"{word.word}_sentence.mp3"
    word.audio_sentence.save(filename, ContentFile(audio_buffer.read()))
    word.save()

    return filename
