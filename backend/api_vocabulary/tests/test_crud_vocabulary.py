from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from users.models import CustomUser
from api_vocabulary.models import VocabularyWord, Language

class VocabularyWordCRUDTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="cruduser", password="pass", email="crud@example.com")
        self.client.force_authenticate(user=self.user)

        self.english = Language.objects.create(code="en", name="English")
        self.spanish = Language.objects.create(code="es", name="Spanish")

        self.word = VocabularyWord.objects.create(
            word="start",
            user=self.user,
            source_lang=self.english,
            target_lang=self.spanish
        )

    def test_create_vocabulary_word(self):
        """
        Crea una nueva palabra y verifica que se guarde correctamente.
        """
        url = "/api/vocabulary/"
        data = {"word": "develop", "source_lang": self.english.id, "target_lang": self.spanish.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(VocabularyWord.objects.filter(word="develop", user=self.user).exists())

    def test_read_list_vocabulary_words(self):
        """
        Verifica que se puede acceder al listado de palabras del usuario autenticado.
        """
        url = "/api/vocabulary/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(w["word"] == "start" for w in response.json()))

    def test_read_detail_vocabulary_word(self):
        """
        Verifica que se pueda obtener el detalle de una palabra específica.
        """
        url = f"/api/vocabulary/{self.word.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["word"], "start")

    def test_update_vocabulary_word(self):
        """
        Actualiza el campo 'word' y verifica que se guarde correctamente.
        """
        url = f"/api/vocabulary/{self.word.id}/"
        data = {"word": "begin", "source_lang": self.english.id, "target_lang": self.spanish.id}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.word.refresh_from_db()
        self.assertEqual(self.word.word, "begin")

    def test_delete_vocabulary_word(self):
        """
        Elimina una palabra y verifica que ya no exista en la base de datos.
        """
        url = f"/api/vocabulary/{self.word.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(VocabularyWord.objects.filter(id=self.word.id).exists())