from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from .serializers import UserMeSerializer, DownloadHistorySerializer, ChangePasswordSerializer, RegisterUserSerializer
from .models import CustomUser
from api_vocabulary.models import DownloadHistory
from .utils import send_verification_email
from rest_framework_simplejwt.views import TokenObtainPairView
from .token_serializers import CustomTokenObtainPairSerializer
from django.shortcuts import redirect
import os

class UserMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserMeSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserMeSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def patch(self, request):
        serializer = UserMeSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LanguageListView(APIView):
    def get(self, request):
        return Response([
            {"code":code, "label":label}
            for code, label in CustomUser._meta.get_field('preferred_language').choices
        ])
    
class DownloadHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        history = DownloadHistory.objects.filter(user=request.user).order_by("-created_at")
        serializer = DownloadHistorySerializer(history, many=True)
        return Response(serializer.data)
    
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Contraseña actualizada correctamente."})
    
class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        username = user.username
        user.delete()
        return Response({"detail": f"Cuenta '{username}' eliminada correctamente."}, status=status.HTTP_204_NO_CONTENT)

class RegisterUserView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        send_verification_email(request, user)

        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "username": user.username,
                "email": user.email,
                "display_name": user.display_name,
                "preferred_language": user.preferred_language,
            },
            "message": "Te hemos enviado un correo para verificar tu cuenta.",
        }, status=status.HTTP_201_CREATED)
    
class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64).decode())
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            return Response({"error": "Enlace inválido"}, status=status.HTTP_400_BAD_REQUEST)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()

            # ✅ Redirigir al frontend tras verificación
            frontend_url = os.getenv("FRONTEND_VERIFY_SUCCESS_URL", "http://localhost:3000/verified")
            return redirect(frontend_url)

        return Response({"error": "Token inválido o expirado"}, status=status.HTTP_400_BAD_REQUEST)
        
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer