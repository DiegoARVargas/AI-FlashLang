from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from users.models import CustomUser
from api_vocabulary.models import VocabularyWord, Language

class GenerateAudioWordTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="audioword", password="password", email="audioword@example.com")
        self.client.force_authenticate(user=self.user)

        self.english = Language.objects.create(code="en", name="English")
        self.spanish = Language.objects.create(code="es", name="Spanish")

        self.word = VocabularyWord.objects.create(
            word="apple",
            user=self.user,
            source_lang=self.english,
            target_lang=self.spanish
        )

        self.url = reverse("vocabulary-generate-audio-word", args=[self.word.pk])

    def test_generate_audio_word_success(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)
        self.assertIn("filename", response.data)