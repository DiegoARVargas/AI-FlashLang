from django.db import models

class VocabularyWord(models.Model):
    word = models.CharField(max_length=100, unique=True)
    part_of_speech = models.CharField(max_length=50, blank=True, null=True)  # Ej: noun, verb, adjective
    translation = models.CharField(max_length=255, blank=True, null=True)  # Traducción en español
    example_sentence = models.TextField(blank=True, null=True)  # Frase generada por GPT-4
    example_translation = models.TextField(blank=True, null=True)  # Traducción de la frase
    audio_word = models.FileField(upload_to="audio/", blank=True, null=True)
    audio_sentence = models.FileField(upload_to="audio/", blank=True, null=True)
    image_url = models.CharField(max_length=500, blank=True, null=True)  # Imagen opcional

    def __str__(self):
        return self.word