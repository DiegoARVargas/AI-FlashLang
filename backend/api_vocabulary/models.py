from django.db import models
from django.conf import settings

class Language(models.Model):
    code = models.CharField(max_length=10, unique=True)  # ej: "en", "es", "fr"
    name = models.CharField(max_length=100)  # ej: "English", "Español", "Français"

    def __str__(self):
        return f"{self.name} ({self.code})"

class VocabularyWord(models.Model):
    word = models.CharField(max_length=100, unique=False)   # Palabra en el idioma base
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="vocabulary_words",
    )
    source_lang = models.ForeignKey(Language, on_delete=models.CASCADE, related_name="words_as_source")
    target_lang = models.ForeignKey(Language, on_delete=models.CASCADE, related_name="words_as_target")
    part_of_speech = models.CharField(max_length=50, blank=True, null=True)  # Ej: noun, verb, adjective
    translation = models.CharField(max_length=255, blank=True, null=True)  # Traducción en español
    example_sentence = models.TextField(blank=True, null=True)  # Frase generada por GPT-4
    example_translation = models.TextField(blank=True, null=True)  # Traducción de la frase
    audio_word = models.FileField(upload_to="audio/", blank=True, null=True)
    audio_sentence = models.FileField(upload_to="audio/", blank=True, null=True)
    image_url = models.CharField(max_length=500, blank=True, null=True)  # Imagen opcional

    def __str__(self):
        return self.word


