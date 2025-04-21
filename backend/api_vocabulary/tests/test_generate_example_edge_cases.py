from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from api_vocabulary.models import VocabularyWord, Language
from users.models import CustomUser
from unittest.mock import patch

class GenerateExampleEdgeCaseTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="user", password="pass", email="user@example.com")
        self.client.login(username="user", password="pass")
        self.client.force_authenticate(user=self.user)

        self.english = Language.objects.create(code="en", name="English")
        self.spanish = Language.objects.create(code="es", name="Spanish")

        self.word = VocabularyWord.objects.create(
            word="testword",
            user=self.user,
            source_lang=self.english,
            target_lang=self.spanish
        )

    # Este test está desactivado temporalmente porque actualmente 
    # no se permite editar palabras una vez creadas.
    # def test_generate_example_fails_if_already_has_example(self):
    #     self.word.example_sentence = "This is already generated."
    #     self.word.save()
    #     url = reverse("vocabulary-generate-example", args=[self.word.id])
    #     response = self.client.post(url)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertIn("error", response.data)

    def test_generate_example_requires_authentication(self):
        """Asegura que no se pueda acceder al endpoint sin un token JWT"""
        client = APIClient()
        url = reverse("vocabulary-generate-example", args=[self.word.id])
        response = client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_generate_example_invalid_id_returns_404(self):
        """Verifica que si se usa un ID inexistente, el servidor responde correctamente"""
        invalid_id = 9999
        url = reverse("vocabulary-generate-example", args=[invalid_id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch("api_vocabulary.views.OpenAI")
    def test_generate_example_handles_openai_failure(self, mock_openai):
        """
        Simula un error de OpenAI y espera una respuesta 500 del endpoint.
        """
        mock_openai.return_value.chat.completions.create.side_effect = Exception("Simulated OpenAI failure")

        url = reverse("vocabulary-generate-example", args=[self.word.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn("error", response.data)