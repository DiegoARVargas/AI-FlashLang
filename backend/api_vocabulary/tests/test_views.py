from rest_framework.test import APITestCase # Clase especial de Django REST Framework para simular peticiones a la API
from rest_framework import status   # Accede a códigos HTTP estándar (como 200, 400...).
from api_vocabulary.models import VocabularyWord

class VocabularyWordTests(APITestCase):
    def test_create_vocabulary_word(self):
        data = {"word": "testword"}
        response = self.client.post("/api/vocabulary/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(VocabularyWord.objects.count(), 1)
        self.assertEqual(VocabularyWord.objects.first().word, "testword")
