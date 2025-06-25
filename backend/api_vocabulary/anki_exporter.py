import os
import random
import hashlib
import tempfile
import genanki
from django.conf import settings
from api_vocabulary.models import UserVocabularyWord, DownloadHistory
from api_vocabulary.genanki_utils.model import flashlang_model

def generate_apkg_for_user(user, deck_name=None, ids=None) -> tuple[str, str]:
    """
    Genera un archivo .apkg para el usuario con las palabras seleccionadas y con audios embebidos.
    Si se proporcionan IDs, se filtra por esas palabras; si no, por deck_name; si tampoco, todas las palabras.
    Se reutiliza un archivo si ya existe para el mismo conjunto de palabras y nombre de mazo.
    También registra la descarga en el historial.
    """

    # Obtener palabras filtradas
    user_words = UserVocabularyWord.objects.filter(user=user)
    if ids:
        user_words = user_words.filter(id__in=ids)
    elif deck_name:
        user_words = user_words.filter(deck=deck_name)

    if not user_words.exists():
        raise ValueError("No se encontraron palabras para exportar.")

    # Definir nombre base del mazo
    base_deck_name = deck_name or user_words.first().deck or "default"
    final_deck_name = base_deck_name.strip().replace(" ", "_")

    # Crear un hash único del conjunto de palabras exportadas
    word_hash_input = "|".join(sorted([f"{w.custom_content_id or w.shared_word_id}" for w in user_words]))
    deck_hash = hashlib.md5(word_hash_input.encode()).hexdigest()[:8]  # corto para nombre de archivo

    # Ruta de salida y nombre de archivo reutilizable
    user_folder = os.path.join(settings.MEDIA_ROOT, "generated_apkg", f"user_{user.id}")
    os.makedirs(user_folder, exist_ok=True)
    output_filename = f"aiflashlang_{final_deck_name}_{deck_hash}.apkg"
    output_path = os.path.join(user_folder, output_filename)

    if os.path.exists(output_path):
        # Registrar historial incluso si se reutiliza
        DownloadHistory.objects.create(
            user=user,
            deck_name=base_deck_name,
            word_ids=",".join(str(w.id) for w in user_words),
            file_path=output_path,
        )
        return output_path, base_deck_name

    # Crear mazo Anki y medios
    deck = genanki.Deck(
        deck_id=random.randrange(1 << 30, 1 << 31),
        name=f"AIflashLang {base_deck_name} - {user.username}"
    )
    media_files = []

    for word in user_words:
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

        for f in [source.audio_word, source.audio_sentence]:
            if f and os.path.exists(f.path):
                media_files.append(f.path)

    # Agregar imagen de fondo Flashy si existe
    flashy_path = os.path.join(settings.MEDIA_ROOT, "anki_assets", "__flashy.png")
    if os.path.exists(flashy_path):
        media_files.append(flashy_path)

    # Escribir archivo final solo si no existe
    genanki.Package(deck, media_files=media_files).write_to_file(output_path)

    # Registrar historial de descarga
    DownloadHistory.objects.create(
        user=user,
        deck_name=base_deck_name,
        word_ids=",".join(str(w.id) for w in user_words),
        file_path=output_path,
    )


    return output_path, base_deck_name