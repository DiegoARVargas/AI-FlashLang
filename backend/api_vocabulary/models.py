from django.db import models
from django.conf import settings

class Language(models.Model):
    code = models.CharField(max_length=10, unique=True)  # ej: "en", "es", "fr"
    name = models.CharField(max_length=100)  # ej: "English", "Español", "Français"

    def __str__(self):
        return f"{self.name} ({self.code})"

class SharedVocabularyWord(models.Model):
    word = models.CharField(max_length=100)
    source_lang = models.ForeignKey(Language, on_delete=models.CASCADE, related_name="shared_words_as_source")
    target_lang = models.ForeignKey(Language, on_delete=models.CASCADE, related_name="shared_words_as_target")
    translation = models.CharField(max_length=255)
    example_sentence = models.TextField()
    example_translation = models.TextField()
    audio_word = models.FileField(upload_to="audio/", blank=True, null=True)
    audio_sentence = models.FileField(upload_to="audio/", blank=True, null=True)
    image_url = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        unique_together = ("word", "source_lang", "target_lang")

    def __str__(self):
        return f"{self.word} ({self.source_lang} → {self.target_lang})"
    
    @property
    def word_audio_filename(self):
        return self.audio_word.name.split("/")[-1] if self.audio_word else ""

    @property
    def example_audio_filename(self):
        return self.audio_sentence.name.split("/")[-1] if self.audio_sentence else ""

    @property
    def word_audio_path(self):
        from django.conf import settings
        return str(settings.MEDIA_ROOT / self.audio_word.name) if self.audio_word else None

    @property
    def example_audio_path(self):
        from django.conf import settings
        return str(settings.MEDIA_ROOT / self.audio_sentence.name) if self.audio_sentence else None

    @property
    def image_filename(self):
        return self.image_url.split("/")[-1] if self.image_url else ""

    @property
    def image_path(self):
        from django.conf import settings
        return str(settings.MEDIA_ROOT / self.image_url) if self.image_url else None

class UserVocabularyWord(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="vocabulary_words"
    )
    shared_word = models.ForeignKey(
        SharedVocabularyWord,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="user_words"
    )
    custom_content = models.OneToOneField(
        'CustomWordContent',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    deck = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "shared_word", "custom_content")

    def __str__(self):
        return f"{self.user.email} - {self.deck} - {self.shared_word or self.custom_content}"
    
class CustomWordContent(models.Model):
    word = models.CharField(max_length=100)
    source_lang = models.ForeignKey(
        Language, on_delete=models.CASCADE, related_name="custom_source_words"
    )
    target_lang = models.ForeignKey(
        Language, on_delete=models.CASCADE, related_name="custom_target_words"
    )
    context = models.TextField()
    translation = models.CharField(max_length=255, blank=True, null=True)
    example_sentence = models.TextField(blank=True, null=True)
    example_translation = models.TextField(blank=True, null=True)
    audio_word = models.FileField(upload_to="audio/", blank=True, null=True)
    audio_sentence = models.FileField(upload_to="audio/", blank=True, null=True)
    image_url = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        unique_together = ("word", "source_lang", "target_lang", "context")

    def __str__(self):
        return f"{self.word} - custom with context"
    
    @property
    def word_audio_filename(self):
        return self.audio_word.name.split("/")[-1] if self.audio_word else ""

    @property
    def example_audio_filename(self):
        return self.audio_sentence.name.split("/")[-1] if self.audio_sentence else ""

    @property
    def word_audio_path(self):
        from django.conf import settings
        return str(settings.MEDIA_ROOT / self.audio_word.name) if self.audio_word else None

    @property
    def example_audio_path(self):
        from django.conf import settings
        return str(settings.MEDIA_ROOT / self.audio_sentence.name) if self.audio_sentence else None

    @property
    def image_filename(self):
        return self.image_url.split("/")[-1] if self.image_url else ""

    @property
    def image_path(self):
        from django.conf import settings
        return str(settings.MEDIA_ROOT / self.image_url) if self.image_url else None
    
class DownloadHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    deck_name = models.CharField(max_length=255)
    word_ids = models.TextField(help_text="Lista separada por comas de los IDs de palabras exportadas")
    file_path = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.deck_name} ({self.created_at})"