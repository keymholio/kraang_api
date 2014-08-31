import random
import re
from rest_framework import status
from talk.serializers import SentenceSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from textblob import TextBlob
from textblob_aptagger import PerceptronTagger


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
        input_text = request.DATA.get('input_text')
        if (input_text):
            sentence = input_text
            result = self.kraang(sentence)
            data = { 'kraang': result }
            json = JSONRenderer().render(data)
            return Response(json, status.HTTP_201_CREATED)
        else:
            content = {'error': 'that is which is known as a bad request'}
            json = JSONRenderer().render(content)
            return Response(json, status=status.HTTP_400_BAD_REQUEST)

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
        result = re.sub("""([Tt]he\s|[Aa]n\s|[Aa]\s)(?=(that|the))""", '', result)

        result = self.capitalize(result)

        return result


    def capitalize(self, sentence):
        """ Capitalize the first letter of each sentence
        """
        blob = TextBlob(sentence, pos_tagger=PerceptronTagger())
        s = ""
        for sent in blob.sentences:
            curr_sent = sent.string.strip()
            s += curr_sent[0].upper() + curr_sent[1:] + " "

        return s.strip()
