import os
import tempfile
import genanki
from django.conf import settings
from api_vocabulary.models import UserVocabularyWord
from api_vocabulary.genanki_utils.model import flashlang_model


def generate_apkg_for_user(user):
    # Obtener palabras del usuario
    user_words = UserVocabularyWord.objects.filter(user=user)

    # Crear mazo y lista de archivos multimedia
    deck = genanki.Deck(
        deck_id=genanki.uid(),  # ID único por exportación
        name=f"FlashLang Deck - {user.username}"
    )
    media_files = []

    for word in user_words:
        # Obtener datos desde shared_word o custom_content
        source = word.custom_content or word.shared_word
        if not source:
            continue

        word_text = source.word
        translation = source.translation or ""
        sentence_audio_tag = f"[sound:{source.example_audio_filename}]" if source.example_audio_filename else ""
        example = source.example_sentence or ""
        example_translation = source.example_translation or ""
        word_audio_tag = f"[sound:{source.word_audio_filename}]" if source.word_audio_filename else ""
        image_tag = f"<img src='{source.image_filename}'>" if source.image_filename else ""

        # Crear la nota (tarjeta)
        note = genanki.Note(
            model=flashlang_model,
            fields=[
                word_text,
                translation,
                example,
                example_translation,
                word_audio_tag,
                sentence_audio_tag,
                image_tag
            ]
        )
        deck.add_note(note)

        # Agregar archivos multimedia si existen
        for filename in [source.word_audio_path, source.example_audio_path, source.image_path]:
            if filename and os.path.exists(filename):
                media_files.append(filename)

    # Agregar la imagen de fondo (Flashy)
    flashy_path = os.path.join(settings.MEDIA_ROOT, "anki_assets", "__flashy.png")
    if os.path.exists(flashy_path):
        media_files.append(flashy_path)

    # Guardar .apkg en carpeta temporal del usuario
    user_folder = os.path.join(settings.MEDIA_ROOT, "generated_apkg", f"user_{user.id}")
    os.makedirs(user_folder, exist_ok=True)
    output_path = os.path.join(user_folder, "flashlang_deck.apkg")

    genanki.Package(deck, media_files=media_files).write_to_file(output_path)

    return output_path