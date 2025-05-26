from rest_framework import serializers
from .models import SharedVocabularyWord, CustomWordContent, UserVocabularyWord, Language

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'code', 'name']


class SharedVocabularyWordSerializer(serializers.ModelSerializer):
    source_lang = LanguageSerializer(read_only=True)
    target_lang = LanguageSerializer(read_only=True)

    class Meta:
        model = SharedVocabularyWord
        fields = [
            'id', 'word', 'source_lang', 'target_lang', 'translation',
            'example_sentence', 'example_translation',
            'audio_word', 'audio_sentence', 'image_url'
        ]


class CustomWordContentSerializer(serializers.ModelSerializer):
    source_lang = LanguageSerializer(read_only=True)
    target_lang = LanguageSerializer(read_only=True)

    class Meta:
        model = CustomWordContent
        fields = [
            'id', 'word', 'source_lang', 'target_lang', 'context',
            'translation', 'example_sentence', 'example_translation',
            'audio_word', 'audio_sentence', 'image_url'
        ]


class UserVocabularyWordSerializer(serializers.ModelSerializer):
    # Entrada: campos auxiliares para crear palabras nuevas
    word = serializers.CharField(write_only=True, required=False)
    source_lang = serializers.PrimaryKeyRelatedField(queryset=Language.objects.all(), write_only=True, required=False)
    target_lang = serializers.PrimaryKeyRelatedField(queryset=Language.objects.all(), write_only=True, required=False)
    context = serializers.CharField(write_only=True, required=False, allow_blank=True)

    # Entrada: IDs explícitos si ya existen
    shared_word_id = serializers.PrimaryKeyRelatedField(
        queryset=SharedVocabularyWord.objects.all(), source="shared_word",
        write_only=True, required=False, allow_null=True
    )
    custom_content_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomWordContent.objects.all(), source="custom_content",
        write_only=True, required=False, allow_null=True
    )

    # Salida: contenido anidado
    shared_word = SharedVocabularyWordSerializer(read_only=True)
    custom_content = CustomWordContentSerializer(read_only=True)

    class Meta:
        model = UserVocabularyWord
        fields = [
            "id", "user", "deck", "created_at",
            "shared_word_id", "custom_content_id",
            "shared_word", "custom_content",
            "word", "source_lang", "target_lang", "context"
        ]
        read_only_fields = ["user", "created_at", "shared_word", "custom_content"]

    def validate(self, attrs):
        word = attrs.get("word")
        source_lang = attrs.get("source_lang")
        target_lang = attrs.get("target_lang")
        context = attrs.get("context")

        if not word or not source_lang or not target_lang:
            raise serializers.ValidationError({
                "error": "Faltan campos obligatorios: 'word', 'source_lang' o 'target_lang'."
            })

        word = word.strip().lower()

        if context:
            attrs["custom_content"] = CustomWordContent(
                word=word,
                source_lang=source_lang,
                target_lang=target_lang,
                context=context.strip()
            )
        else:
            attrs["shared_word"] = SharedVocabularyWord(
                word=word,
                source_lang=source_lang,
                target_lang=target_lang
            )

        return attrs

    def create(self, validated_data):
        # Eliminar campos auxiliares antes de guardar
        validated_data.pop("word", None)
        validated_data.pop("source_lang", None)
        validated_data.pop("target_lang", None)
        validated_data.pop("context", None)
        return super().create(validated_data)