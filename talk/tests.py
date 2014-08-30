from django.test import TestCase
from talk.views import Translate

class TestCapitalization(TestCase):
    def setUp(self):
        self.translate = Translate()

    def test_cap_simple_sentence(self):
        sentence = "booyakasha!"
        s = Translate.capitalize(self.translate, sentence)
        self.assertEqual(s, "Booyakasha!")

    def test_proper_noun_sentence(self):
        sentence = "let's skateboard in the Dojo with Mikey."
        s = Translate.capitalize(self.translate, sentence)
        self.assertEqual(s, "Let's skateboard in the Dojo with Mikey.")
