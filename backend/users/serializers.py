from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import CustomUser
from api_vocabulary.models import DownloadHistory

class UserMeSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False)
    class Meta:
        model = CustomUser
        fields = ("username", "email", "is_premium", "preferred_language", "display_name", "avatar","created_at")
        read_only_fields = ("username", "email", "is_premium", "created_at")

class DownloadHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DownloadHistory
        fields = ("id", "deck_name", "word_ids", "file_path", "created_at")

class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_current_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("La contraseña actual es incorrecta.")
        return value

    def validate_new_password(self, value):
        validate_password(value)  # Usa las validaciones de Django (longitud, etc.)
        return value

    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user