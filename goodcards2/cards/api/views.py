from rest_framework import status
from rest_framework.decorators import api_view
from cards.models import Card, Deck
from cards.api.serializers import CardSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from user.models import User


class CardListView(APIView):
    @api_view(['GET'])
    def get_cards(request):
        cards = Card.objects.all()
        serializer = CardSerializer(cards, many=True)
        return Response(serializer.data)
        

class CardDetailView(APIView):
    @api_view(['GET'])
    def get_card_detail(request, pk):
        card = Card.objects.get(id=pk)
        serializer = CardSerializer(card)
        return Response(serializer.data)        


class CreateDeck(APIView):
    @api_view(['POST'])
    def create_deck(request):
        deck = Deck(name=request.data['name'], user=User.objects.get(id=1))
        deck.save()
        return Response(f"Successfully created deck {deck.name}", status=status.HTTP_201_CREATED)


class AddCardToDeck(APIView):
    @api_view(['POST'])
    def post(self, request):
        pass
