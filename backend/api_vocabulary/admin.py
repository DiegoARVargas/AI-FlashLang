from django.contrib import admin
from .models import VocabularyWord

@admin.register(VocabularyWord)
class VocabularyWordAdmin(admin.ModelAdmin):
    list_display = ("word", "part_of_speech", "translation")
    search_fields = ("word", "translation", "part_of_speech")
