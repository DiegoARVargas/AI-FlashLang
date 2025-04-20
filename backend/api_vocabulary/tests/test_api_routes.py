from rest_framework import status
from rest_framework.test import APITestCase
from users.models import CustomUser
from api_vocabulary.models import VocabularyWord, Language

class APIRouteTests(APITestCase):
    def setUp(self):
        """Crea un usuario y una palabra asociada para verificar las rutas de la API."""
        self.user = CustomUser.objects.create_user(
            username="testuser",
            password="testpass",
            email="test@example.com"
        )
        self.client.force_authenticate(user=self.user)

        self.source_lang = Language.objects.create(code="en", name="English")
        self.target_lang = Language.objects.create(code="es", name="Spanish")

        VocabularyWord.objects.create(
            word="example",
            user=self.user,
            source_lang=self.source_lang,
            target_lang=self.target_lang
        )

    def test_vocabulary_endpoint_accessible(self):
        """Verifica que /api/vocabulary/ esté accesible."""
        response = self.client.get("/api/vocabulary/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_languages_endpoint_accessible(self):
        """Verifica que /api/languages/ esté accesible."""
        response = self.client.get("/api/languages/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
