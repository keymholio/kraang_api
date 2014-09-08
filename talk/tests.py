from django.test import TestCase
from talk.views import Translate
import mock
import random
import unittest
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestAPI(APITestCase):
    def test_post(self):
        """
        Ensure we can create a kraang translated sentence as a service
        """
        url = reverse('translate')
        data = {'input_text': 'Donny likes April'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_bad_req(self):
        """
        Test a bad request
        """
        url = reverse('translate')
        data = {'some_other_data': 'Bad data'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'that is which is known as a bad request'})


class TestCapitalization(TestCase):
    def setUp(self):
        self.translate = Translate()

    def test_sentences(self):
        sentence = "booyakasha!"
        s = Translate.capitalize(self.translate, sentence)
        self.assertEqual(s, "Booyakasha!")

    def test_proper_noun_sentence(self):
        sentence = "let's skateboard in the Dojo with Mikey."
        s = Translate.capitalize(self.translate, sentence)
        self.assertEqual(s, "Let's skateboard in the Dojo with Mikey.")

    def test_multiple_proper_noun_sentences(self):
        sentence = ("let's skateboard in the Dojo with Mikey. we'll flip out "
                    "Donny!")
        s = Translate.capitalize(self.translate, sentence)
        self.assertEqual(s, ("Let's skateboard in the Dojo with Mikey. We'll "
                             "flip out Donny!"))

    def test_truncate_extra_spaces(self):
        sentence = "    let's skateboard in the Dojo with Mikey.     "
        s = Translate.capitalize(self.translate, sentence)
        self.assertEqual(s, "Let's skateboard in the Dojo with Mikey.")

    def test_tricky_period_sentence(self):
        sentence = "mikey went to St. Louis."
        s = Translate.capitalize(self.translate, sentence)
        self.assertEqual(s, "Mikey went to St. Louis.")

    def test_lots_of_punctuation(self):
        sentence = "this is the test string! will it work? let's find out. it should work! or should it? oh yes. indeed."
        s = Translate.capitalize(self.translate, sentence)
        self.assertEqual(s, "This is the test string! Will it work? Let's find out. It should work! Or should it? Oh yes. Indeed.")


class TestKraangSpeech(TestCase):

    def setUp(self):
        self.translate = Translate()

    @mock.patch('random.choice')
    def test_adding_the(self, random_call):
        sentence = "Donny likes April."
        random_call.return_value = "<kraang> "
        s = Translate.kraang(self.translate, sentence)
        self.assertEqual(s, u"<kraang> Donny likes <kraang> April.")

    @mock.patch('random.choice')
    def test_starting_with_the(self, random_call):
        sentence = "The pizza was stolen by Mikey."
        random_call.return_value = "<kraang> "
        s = Translate.kraang(self.translate, sentence)
        self.assertEqual(s, u"The <kraang> pizza was stolen by <kraang> "
                         "Mikey.")

    @mock.patch('random.choice')
    def test_to_place(self, random_call):
        sentence = "The Turtles went to the Dojo."
        random_call.return_value = "<kraang> "
        s = Translate.kraang(self.translate, sentence)
        self.assertEqual(s, u"The <kraang> Turtles went to that place. "
                         "To the <kraang> Dojo.")

    @mock.patch('random.choice')
    def test_to_followed_by_verb(self, random_call):
        sentence = "The Turtles went to play above ground."
        random_call.return_value = "<kraang> "
        s = Translate.kraang(self.translate, sentence)
        self.assertEqual(s, u"The <kraang> Turtles went to play above "
                         "<kraang> ground.")

    @mock.patch('random.choice')
    def test_double_plural_nouns(self, random_call):
        sentence = "Splinter saw Snoop Dogg."
        random_call.return_value = "<kraang> "
        s = Translate.kraang(self.translate, sentence)
        self.assertEqual(s, u"<kraang> Splinter saw <kraang> Snoop Dogg.")

    @mock.patch('random.choice')
    def test_double_nouns(self, random_call):
        sentence = "Splinter saw a space mutant."
        random_call.return_value = "<kraang> "
        s = Translate.kraang(self.translate, sentence)
        self.assertEqual(s, u"<kraang> Splinter saw a <kraang> space mutant.")

    @mock.patch('random.choice')
    def test_apostrophes(self, random_call):
        sentence = "Splinter isn't going to take a nap."
        random_call.return_value = "<kraang> "
        s = Translate.kraang(self.translate, sentence)
        self.assertEqual(s, u"<kraang> Splinter isn't going to take a "
                         "<kraang> nap.")

    @mock.patch('random.choice')
    def test_single_quote(self, random_call):
        sentence = "The Turtle's pizza was getting cold."
        random_call.return_value = "<kraang> "
        s = Translate.kraang(self.translate, sentence)
        self.assertEqual(s, u"The <kraang> Turtle's pizza was getting cold.")

    @mock.patch('random.choice')
    def test_double_thes(self, random_call):
        sentence = "The Turtles fight Shredder's clan."
        random_call.return_value = "the things known as "
        s = Translate.kraang(self.translate, sentence)
        self.assertEqual(s, u"The things known as Turtles fight the things "
                         "known as Shredder's clan.")

    @mock.patch('random.choice')
    def test_that_replace_the(self, random_call):
        sentence = "Mikey yells at Shredder."
        random_call.return_value = "that which is known as "
        s = Translate.kraang(self.translate, sentence)
        self.assertEqual(s, u"That which is known as Mikey yells at that "
                         "which is known as Shredder.")

    @mock.patch('random.choice')
    def test_replace_an(self, random_call):
        sentence = "An attacker approached Leo."
        random_call.return_value = "the thing known as "
        s = Translate.kraang(self.translate, sentence)
        self.assertEqual(s, u"The thing known as attacker approached "
                         "the thing known as Leo.")

    @mock.patch('random.choice')
    def test_replace_an2(self, random_call):
        sentence = "Russian soldiers approached the Turtles."
        random_call.return_value = "the things known as "
        s = Translate.kraang(self.translate, sentence)
        self.assertEqual(s, u"Russian soldiers approached "
                         "the things known as Turtles.")

    @mock.patch('random.choice')
    def test_replace_a(self, random_call):
        sentence = "A Foot Clan soldier approached Raphael."
        random_call.return_value = "the thing known as "
        s = Translate.kraang(self.translate, sentence)
        self.assertEqual(s, u"The thing known as Foot Clan soldier approached "
                         "the thing known as Raphael.")

    @mock.patch('random.choice')
    def test_no_period(self, random_call):
        sentence = "Donnie creates Metalhead"
        random_call.return_value = "<kraang> "
        s = Translate.kraang(self.translate, sentence)
        self.assertEqual(s, u"<kraang> Donnie creates <kraang> Metalhead")

    def test_plural(self):
        random.seed(0)
        sentence = "Turtles fight the Foot Clan soldiers."
        s = Translate.kraang(self.translate, sentence)
        self.assertEqual(s, u"The things which are named Turtles fight "
                         "the things which are named Foot Clan soldiers.")
