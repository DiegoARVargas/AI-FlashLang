from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.reverse import reverse # Nos permite construir URLs a partir del nombre de la vista registrada.
from api_vocabulary.models import VocabularyWord

class GenerateAudioSentenceTest(APITestCase):
    def setUp(self):
        self.word = VocabularyWord.objects.create(
            word="play",
            example_sentence="The kids play in the park every afternoon."
        )
        self.url = reverse("vocabularyword-generate-audio-sentence", args=[self.word.pk])

    def test_generate_audio_sentence_success(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)
        self.assertIn("filename", response.data)

    def test_generate_audio_sentence_fails_without_example(self):
        self.word.example_sentence = ""
        self.word.save()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)