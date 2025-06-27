from django.contrib import admin
from .models import Language, SharedVocabularyWord, UserVocabularyWord, CustomWordContent, DownloadHistory

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("code", "name")

@admin.register(SharedVocabularyWord)
class SharedVocabularyWordAdmin(admin.ModelAdmin):
    list_display = ("word", "translation", "source_lang", "target_lang")
    search_fields = ("word", "translation", "example_sentence")

@admin.register(CustomWordContent)
class CustomWordContentAdmin(admin.ModelAdmin):
    list_display = ("word", "context", "translation", "source_lang", "target_lang")
    search_fields = ("word", "translation", "context")

@admin.register(UserVocabularyWord)
class UserVocabularyWordAdmin(admin.ModelAdmin):
    list_display = ("user", "deck", "shared_word", "custom_content", "created_at")
    search_fields = ("user__email", "deck")
    list_filter = ("deck", "shared_word", "custom_content", "created_at")

@admin.register(DownloadHistory)
class DownloadHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'deck_name', 'file_path', 'created_at')
    search_fields = ('user__username', 'deck_name')
    list_filter = ('created_at',)