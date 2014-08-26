from talk.models import Sentence
from rest_framework import serializers

class SentenceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sentence
        fields = ('input_text',)
