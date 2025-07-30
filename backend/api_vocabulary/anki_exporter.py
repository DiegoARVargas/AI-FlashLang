import os
import random
import hashlib
import tempfile
import shutil
import requests
import genanki
from django.conf import settings
from api_vocabulary.models import UserVocabularyWord, DownloadHistory
from api_vocabulary.genanki_utils.model import get_flashlang_model

def generate_apkg_for_user(user, deck_name=None, ids=None, allow_duplicates=False) -> tuple[str, str]:
    """
    Genera un archivo .apkg para el usuario con las palabras seleccionadas y con audios embebidos.
    Si se proporcionan IDs, se filtra por esas palabras; si no, por deck_name; si tampoco, todas las palabras.
    Si allow_duplicates=False, se reutiliza un archivo si ya existe para el mismo conjunto.
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

    # Nombre base del mazo
    base_deck_name = deck_name or user_words.first().deck or "default"
    final_deck_name = base_deck_name.strip().replace(" ", "_")

    # Ruta de usuario
    user_folder = os.path.join(settings.MEDIA_ROOT, "generated_apkg", f"user_{user.id}")
    os.makedirs(user_folder, exist_ok=True)

    # Comportamiento con duplicados
    if not allow_duplicates:
        word_hash_input = "|".join(sorted([f"{w.custom_content_id or w.shared_word_id}" for w in user_words]))
        deck_hash = hashlib.md5(word_hash_input.encode()).hexdigest()[:8]
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
    else:
        # Si se permiten duplicados, siempre crear nuevo archivo
        temp_suffix = random.randint(1000, 9999)
        output_filename = f"aiflashlang_{final_deck_name}_{temp_suffix}.apkg"
        output_path = os.path.join(user_folder, output_filename)

    # Crear carpeta temporal para audios descargados
    TEMP_DIR = tempfile.mkdtemp()

    def download_to_temp(filefield):
        if not filefield or not filefield.url:
            return None
        try:
            url = filefield.url
            filename = os.path.basename(filefield.name)
            local_path = os.path.join(TEMP_DIR, filename)

            response = requests.get(url)
            if response.status_code == 200:
                with open(local_path, 'wb') as f:
                    f.write(response.content)
                return local_path
        except Exception as e:
            print(f"[ERROR] Fallo al descargar {filefield.name}: {str(e)}")
        return None

    # Crear mazo Anki
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
        word_audio_filename = os.path.basename(source.audio_word.name) if source.audio_word else ""
        sentence_audio_filename = os.path.basename(source.audio_sentence.name) if source.audio_sentence else ""
        word_audio_tag = f"[sound:{word_audio_filename}]" if word_audio_filename else ""
        sentence_audio_tag = f"[sound:{sentence_audio_filename}]" if sentence_audio_filename else ""
        image_tag = f"<img src='{source.image_url}'>" if source.image_url else ""

        note = genanki.Note(
            model=get_flashlang_model(),
            fields=[
                word_text,
                translation,
                example,
                example_translation,
                word_audio_tag,
                sentence_audio_tag,
                image_tag,
            ],
            guid=str(random.randrange(1 << 30, 1 << 31)) if allow_duplicates else None
        )

        deck.add_note(note)

        # Descargar audios desde S3 y agregar como media local
        for f in [source.audio_word, source.audio_sentence]:
            local_path = download_to_temp(f)
            if local_path:
                media_files.append(local_path)

    ''' Comentaremos este fragmento de codigo ya que no es necesario por ahora en produccion
    # Agregar imagen decorativa si existe
    flashy_path = os.path.join(settings.MEDIA_ROOT, "anki_assets", "__flashy.png")
    if os.path.exists(flashy_path):
        media_files.append(flashy_path)
    '''

    # Crear el archivo final
    genanki.Package(deck, media_files=media_files).write_to_file(output_path)

    # Registrar historial de descarga
    DownloadHistory.objects.create(
        user=user,
        deck_name=base_deck_name,
        word_ids=",".join(str(w.id) for w in user_words),
        file_path=output_path,
    )

    # Limpiar carpeta temporal
    shutil.rmtree(TEMP_DIR)

    return output_path, base_deck_name