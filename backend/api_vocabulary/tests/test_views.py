from rest_framework import status   # Accede a códigos HTTP estándar (como 200, 400...).
from rest_framework.test import APITestCase  # Clase especial de Django REST Framework para simular peticiones a la API
from django.urls import reverse  # Permite construir URLs a partir de nombres de vista
from users.models import CustomUser  # Importa el modelo de usuario personalizado
from api_vocabulary.models import VocabularyWord, Language

class VocabularyWordTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="creator", password="password", email="creator@example.com")
        self.client.force_authenticate(user=self.user)

        self.english = Language.objects.create(code="en", name="English")
        self.spanish = Language.objects.create(code="es", name="Spanish")

    def test_create_vocabulary_word(self):
        data = {
            "word": "testword",
            "source_lang": self.english.id,
            "target_lang": self.spanish.id
        }
        response = self.client.post("/api/vocabulary/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(VocabularyWord.objects.count(), 1)
        self.assertEqual(VocabularyWord.objects.first().word, "testword")