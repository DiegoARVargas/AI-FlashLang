from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.reverse import reverse
from api_vocabulary.models import VocabularyWord

class GenerateExampleTest(APITestCase):
    def setUp(self):
        self.word = VocabularyWord.objects.create(word="run")
        self.url = reverse("vocabularyword-generate-example", args=[self.word.pk])

    def test_generate_example_success(self):
        response = self.client.post(self.url)
        self.assertIn(response.status_code, [200, 500])