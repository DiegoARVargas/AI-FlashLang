from google.cloud import translate_v2 as translate

client = translate.Client()

def translate_text(text: str, source: str, target: str) -> str:
    """
    Traduce un texto usando Google Cloud Translate.
    source y target son códigos de idioma compatibles con Google (e.g. 'fr', 'es', 'en', 'pt-BR', etc.)
    """
    result = client.translate(text, source_language=source, target_language=target)
    return result["translatedText"]
