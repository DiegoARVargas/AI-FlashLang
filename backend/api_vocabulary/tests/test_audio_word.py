from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from users.models import CustomUser
from api_vocabulary.models import VocabularyWord

class GenerateAudioWordTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="audioword", password="password", email="audioword@example.com")
        self.client.force_authenticate(user=self.user)
        self.word = VocabularyWord.objects.create(word="apple", user=self.user)

    def test_generate_audio_word_success(self):
        url = reverse("vocabularyword-generate-audio-word", args=[self.word.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)
        self.assertIn("filename", response.data)