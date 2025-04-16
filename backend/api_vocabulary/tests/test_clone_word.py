from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import CustomUser
from api_vocabulary.models import VocabularyWord

class CloneWordTest(APITestCase):
    def setUp(self):
        self.user_a = CustomUser.objects.create_user(username="userA", password="pass123", email="a@example.com")
        self.user_b = CustomUser.objects.create_user(username="userB", password="pass123", email="b@example.com")

        # Autenticación por defecto: usuario B
        self.client.force_authenticate(user=self.user_b)

    def test_user_can_clone_existing_word_from_other_user(self):
        VocabularyWord.objects.create(word="balance", user=self.user_a, translation="(n) equilibrio")

        response = self.client.post("/api/vocabulary/", {"word": "balance"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Validar que el nuevo registro pertenece al usuario B
        self.assertEqual(VocabularyWord.objects.filter(word="balance", user=self.user_b).count(), 1)

    def test_user_cannot_duplicate_their_own_word(self):
        VocabularyWord.objects.create(word="balance", user=self.user_b)

        response = self.client.post("/api/vocabulary/", {"word": "balance"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("word", response.data)

    def test_user_can_create_completely_new_word(self):
        response = self.client.post("/api/vocabulary/", {"word": "harmony"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
