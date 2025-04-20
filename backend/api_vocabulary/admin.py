from django.contrib import admin
from .models import VocabularyWord, Language

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("code", "name")

@admin.register(VocabularyWord)
class VocabularyWordAdmin(admin.ModelAdmin):
    list_display = ("word", "part_of_speech", "translation")
    search_fields = ("word", "translation", "part_of_speech")