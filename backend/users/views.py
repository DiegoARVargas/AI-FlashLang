from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from .serializers import UserMeSerializer, DownloadHistorySerializer, ChangePasswordSerializer, RegisterUserSerializer
from .models import CustomUser
from api_vocabulary.models import DownloadHistory

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

        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "username": user.username,
                "email": user.email,
                "display_name": user.display_name,
                "preferred_language": user.preferred_language,
            }
        }, status=status.HTTP_201_CREATED)