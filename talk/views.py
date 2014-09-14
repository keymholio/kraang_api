import random
import re
import nltk
from rest_framework import status
from talk.models import Sentence
from talk.serializers import SentenceSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from textblob import TextBlob
from textblob_aptagger import PerceptronTagger

# set the path to the natural language tokenizer
nltk.data.path.append('./talk/nltk/')

@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'translate': reverse('translate', request=request, format=format)
    })


class Translate(generics.CreateAPIView):
    """
    API endpoint that creates translated kraang sentences
    """
    permission_classes = (AllowAny,)
    serializer_class = SentenceSerializer

    def post(self, request, format=None):
        data = request.DATA.copy()
        sentence = data.get('input_text')
        if (sentence):
            result = self.kraang(sentence)
            data['output_text'] = result
            s = Sentence(input_text=sentence, output_text=result)
            s.save()
            json_dict = {'kraang': result}
            return Response(json_dict, status.HTTP_201_CREATED)
        else:
            content = {'error': 'that is which is known as a bad request'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

    def kraang(self, sentence):
        """ Modify the sentence into 'kraang' speech
        """
        nouns = ['the thing known as ',
                 'the thing which is known as ',
                 'that which is called ']

        plurals = ['the things. the things known as ',
                   'that which are known as ',
                   'the things which are named ']

        propers = ['that which is called ',
                   'the thing which is known as ',
                   'the thing named ']

        prop_plurals = ['those who are called ',
                        'the things who are known as ',
                        'the things named ']

        result = ""
        blob = TextBlob(sentence, pos_tagger=PerceptronTagger())
        tags = dict((x.lower(), y) for x, y in blob.tags)
        for index, word in enumerate(blob.tokens):
            key = word.lower()

            # get previous tag
            prev_tag = tags.get(blob.tokens[index-1].lower())
            if index+1 == len(blob.tokens):
                next_tag = None
            else:
                next_tag = tags.get(blob.tokens[index+1].lower())

            # lookahead to furthest noun
            curr_index = index
            while (next_tag and "NN" in next_tag and "NN" in tags[key]):
                if curr_index+1 == len(blob.tokens):
                    next_tag = None
                else:
                    next_tag = tags.get(blob.tokens[curr_index+1].lower())
                    key = blob.tokens[curr_index].lower()
                    curr_index += 1

            if key in tags:
                if index == 0 or \
                   (prev_tag and
                    "NN" not in prev_tag and
                    "POS" not in prev_tag and
                    "JJ" not in prev_tag):

                    if tags[key] == "NNPS":
                        result += random.choice(prop_plurals)
                    elif tags[key] == "NNS":
                        result += random.choice(plurals)
                    elif tags[key] == "NNP":
                        result += random.choice(propers)
                    elif tags[key] == "NN":
                        result += random.choice(nouns)
                    elif tags[key] == "TO" and "VB" not in next_tag:
                        result += "to that place. "
            result += word + " "

        # remove extra space before "n't"
        result = re.sub(""".(?=n\'t)""", '', result)
        # remove spacing near punctuation
        result = re.sub("""\s(?=(\.|\!|\?|\,|:|'|"))""", '', result)
        # remove double "the"s
        result = re.sub(""".(the|that)(?<=[Tt]he.the)""", '', result)
        # remove "the","an", "a" before "that" or "the"
        result = re.sub("""([Tt]he\s|[Aa]n\s|[Aa]\s)(?=(that|the))""", '',
                        result)
        # Change 'I am' to 'Kraang is'
        result = re.sub("""(I\sam|[Ww]e\sare)""", 'Kraang is', result)
        # Change 'I, we, us, our' to 'Kraang'
        result = re.sub("""(I\s|[Ww]e\s|[Uu]s\s|[Oo]ur\s)""", 'Kraang ', result)
        # Change 'my' to 'Kraang's'
        result = re.sub("""[Mm]y""", 'Kraang\'s', result)

        result = self.capitalize(result)

        return result

    def capitalize(self, sentence):
        """ Capitalize the first letter of each sentence
        """
        # trim whitespace
        sentence = sentence.strip()
        sents = re.split('([.!?] *)', sentence)
        cap_sent = ''

        for s in sents:
            if (len(s)):
                cap_sent = cap_sent + s[0].capitalize() + s[1:]

        return cap_sent
