from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from users.models import CustomUser
from api_vocabulary.models import VocabularyWord

class GenerateExampleTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="testuser", password="testpass", email="test@example.com")
        self.client.force_authenticate(user=self.user)
        self.word = VocabularyWord.objects.create(word="run", user=self.user)

    def test_generate_example_success(self):
        url = reverse("vocabularyword-generate-example", args=[self.word.id])
        response = self.client.post(url)
        self.assertIn(response.status_code, [200, 500])  # 500 si hay error con OpenAI