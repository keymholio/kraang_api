from rest_framework import status
from talk.serializers import SentenceSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'translate': reverse('translate', request=request, format=format)
    })

class Translate(generics.CreateAPIView):
    """
    API endpoint that creates kraang translated sentences
    """
    permission_classes = (AllowAny,)
    serializer_class = SentenceSerializer

    def post(self, request, format=None):
        if (request.DATA['input_text']):
            data = { 'output_text': u'sup!' }
            return Response(data)
        else:
            content = {'error': 'that is which is known as a bad request'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
