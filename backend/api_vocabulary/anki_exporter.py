import os
import random
import tempfile
import genanki
import hashlib
from django.conf import settings
from api_vocabulary.models import UserVocabularyWord
from api_vocabulary.genanki_utils.model import flashlang_model

def generate_apkg_for_user(user, deck_name=None, ids=None) -> tuple[str, str]:
    """
    Genera un archivo .apkg para el usuario con audios embebidos.

    - Si se pasan IDs, se exportan solo esas palabras.
    - Si se pasa deck_name, se filtra por ese deck.
    - Si no se pasa nada, exporta todas las palabras del usuario.
    """
    # Obtener palabras del usuario
    user_words = UserVocabularyWord.objects.filter(user=user)

    if ids:
        user_words = user_words.filter(id__in=ids)

    elif deck_name:
        # Si se especifica un deck_name, filtrar por ese deck
        user_words = user_words.filter(deck=deck_name)

    if not user_words.exists():
        raise ValueError(f"No words found for user {user.username}")
    
    # Nombre del deck
    deck_name = deck_name or user_words.first().deck or "default"

    # Crear mazo y lista de archivos multimedia
    deck = genanki.Deck(
        deck_id=random.randrange(1 << 30, 1 << 31),  # ID aleatorio único compatible con genanki
        name=f"AIflashLang {deck_name} - {user.username}"
    )
    media_files = []

    for word in user_words:
        # Obtener datos desde shared_word o custom_content
        source = word.custom_content or word.shared_word
        if not source:
            continue

        word_text = source.word
        translation = source.translation or ""
        example = source.example_sentence or ""
        example_translation = source.example_translation or ""
        word_audio_tag = f"[sound:{source.audio_word.name.split('/')[-1]}]" if source.audio_word else ""
        sentence_audio_tag = f"[sound:{source.audio_sentence.name.split('/')[-1]}]" if source.audio_sentence else ""
        image_tag = f"<img src='{source.image_url}'>" if source.image_url else ""

        # Crear la nota (tarjeta)
        unique_key = f"{user.id}-{word_text}-{deck_name}"
        note_guid = hashlib.sha256(unique_key.encode()).hexdigest()[:16]  # 16-char hash
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
            ],
            guid=note_guid
        )
        deck.add_note(note)

        # Agregar archivos multimedia si existen
        for f in [source.audio_word, source.audio_sentence]:
            if f and os.path.exists(f.path):
                media_files.append(f.path)

    # Agregar la imagen de fondo (Flashy)
    flashy_path = os.path.join(settings.MEDIA_ROOT, "anki_assets", "__flashy.png")
    if os.path.exists(flashy_path):
        media_files.append(flashy_path)

    # Guardar .apkg en carpeta temporal del usuario
    user_folder = os.path.join(settings.MEDIA_ROOT, "generated_apkg", f"user_{user.id}")
    os.makedirs(user_folder, exist_ok=True)
    output_filename = f"aiflashlang_{deck_name}.apkg"
    output_path = os.path.join(user_folder, output_filename)

    genanki.Package(deck, media_files=media_files).write_to_file(output_path)

    return output_path, deck_name