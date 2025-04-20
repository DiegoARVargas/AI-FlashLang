from django.test import TestCase
from api_vocabulary.models import Language

class LanguageModelTests(TestCase):
    def setUp(self):
        self.language = Language.objects.create(code="en", name="English")

    def test_language_creation(self):
        '''Verifica la correcta creación del objeto Language con los valores esperados de código 
           y nombre'''
        self.assertEqual(self.language.code, "en")
        self.assertEqual(self.language.name, "English")

    def test_language_str_representation(self):
        '''Valida la representación en cadena del modelo Language'''
        self.assertEqual(str(self.language), "English (en)")

    def test_language_code_is_unique(self):
        '''Asegura que el campo 'code' del modelo Language es único y lanza una excepción 
           al intentar duplicarlo'''
        with self.assertRaises(Exception):
            Language.objects.create(code="en", name="Duplicate English")

