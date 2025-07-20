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
    
class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = CustomUser
        fields = ("email", "username", "password", "confirm_password", "display_name", "preferred_language")

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Ya existe un usuario con este correo electrónico.")
        return value

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Las contraseñas no coinciden.")
        validate_password(data["password"])
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        return CustomUser.objects.create_user(
            email=validated_data["email"],
            username=validated_data.get("username", ""),
            display_name=validated_data.get("display_name", ""),
            preferred_language=validated_data.get("preferred_language", "es"),
            password=validated_data["password"]
        )