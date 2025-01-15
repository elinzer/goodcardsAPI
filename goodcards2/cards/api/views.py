from cards.models import Card
from cards.api.serializers import CardSerializer
from rest_framework.response import Response
from rest_framework.views import APIView


class CardListView(APIView):
    
    def get(self, request):
        cards = Card.objects.all()
        serializer = CardSerializer(cards, many=True)
        return Response(serializer.data)
        

class CardDetailView(APIView):
    
    def get(self, request, pk):
        card = Card.objects.get(id=pk)
        serializer = CardSerializer(card)
        return Response(serializer.data)        

    
    
    