from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from api_vocabulary.models import VocabularyWord
from rest_framework.reverse import reverse
from rest_framework import status

User = get_user_model()

class VocabularyCloningLogicTests(APITestCase):
    def setUp(self):
        # Create two users
        self.user_a = User.objects.create_user(username="userA", email="userA@example.com", password="password123")
        self.user_b = User.objects.create_user(username="userB", email="userB@example.com", password="password123")

        # Get auth tokens
        self.token_a = str(RefreshToken.for_user(self.user_a).access_token)
        self.token_b = str(RefreshToken.for_user(self.user_b).access_token)

        self.url = reverse("vocabularyword-list")

    def test_user_cannot_duplicate_their_own_word(self):
        # El usuario A crea una palabra
        self.client.force_authenticate(user=self.user_a)
        self.client.post("/api/vocabulary/", {"word": "sun"})
        # Luego intentamos crearla de nuevo
        response = self.client.post("/api/vocabulary/", {"word": "sun"})
        # Validamos la respuesta esperada
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("word", response.data)
        self.assertIn("Esta palabra ya fue creada por ti.", response.data["word"])


    def test_user_can_clone_existing_word_from_other_user(self):
        """User B creates 'balance', User A tries to create the same word"""
        VocabularyWord.objects.create(
            word="balance",
            user=self.user_b,
            translation="(n) balance",
            example_sentence="He tries to keep his balance.",
            example_translation="Él trata de mantener su equilibrio."
        )

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token_a}")
        response = self.client.post(self.url, {"word": "balance"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["translation"], "(n) balance")
        self.assertEqual(response.data["user"], self.user_a.id)

    def test_user_can_create_a_completely_new_word(self):
        """User A creates a brand new word"""
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token_a}")
        response = self.client.post(self.url, {"word": "unicornify"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["word"], "unicornify")
