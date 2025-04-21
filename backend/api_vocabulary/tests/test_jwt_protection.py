from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken

class JWTProtectionTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="secure_user", email="secure@example.com", password="strongpassword")
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.auth_header = {"HTTP_AUTHORIZATION": f"Bearer {self.token}"}
        self.protected_url = reverse("vocabulary-list")  # /api/vocabulary/

    def test_access_denied_without_token(self):
        """Verifica que se rechace el acceso a una vista protegida si no se envía token JWT"""
        response = self.client.get(self.protected_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)

    def test_access_granted_with_valid_token(self):
        """Verifica que un token válido permita el acceso a la vista protegida"""
        response = self.client.get(self.protected_url, **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
