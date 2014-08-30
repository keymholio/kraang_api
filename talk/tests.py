from django.test import TestCase
from talk.views import Translate
import mock
import random
import unittest

@unittest.skip("Don't want to test")
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
        sentence = "mikey went to st. louis."
        s = Translate.capitalize(self.translate, sentence)
        self.assertEqual(s, "Mikey went to st. louis.")


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
