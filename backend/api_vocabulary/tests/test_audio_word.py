from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.reverse import reverse
from api_vocabulary.models import VocabularyWord

class GenerateAudioWordTest(APITestCase):
    def setUp(self):
        self.word = VocabularyWord.objects.create(word="apple")
        self.url = reverse("vocabularyword-generate-audio-word", args=[self.word.pk])

    def test_generate_audio_word_success(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)
        self.assertIn("filename", response.data)