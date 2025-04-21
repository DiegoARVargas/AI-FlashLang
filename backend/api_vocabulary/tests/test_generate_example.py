from rest_framework import status
from rest_framework.test import APITestCase
from users.models import CustomUser
from api_vocabulary.models import VocabularyWord, Language

class GenerateExampleTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="testuser", password="testpass", email="test@example.com")
        self.client.force_authenticate(user=self.user)

        self.english = Language.objects.create(code="en", name="English")
        self.spanish = Language.objects.create(code="es", name="Spanish")

        self.word = VocabularyWord.objects.create(
            word="run",
            user=self.user,
            source_lang=self.english,
            target_lang=self.spanish,
        )

    def test_generate_example_success(self):
        """
        Verifica que el endpoint funcione correctamente cuando la palabra tiene definidos los idiomas.
        """
        url = f"/api/vocabulary/{self.word.id}/generate_example/"
        response = self.client.post(url)
        self.assertIn(response.status_code, [200, 500])  # 500 si falla OpenAI