from rest_framework import serializers
from .models import VocabularyWord, Language

class VocabularyWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = VocabularyWord
        fields = '__all__'
        read_only_fields = ['user']

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ["id", "code", "name"]