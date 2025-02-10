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
        try:
            card = Card.objects.get(id=pk)
        except Card.DoesNotExist:
            return Response(data={"message": "No card found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = CardSerializer(card)
            return Response(serializer.data, status=status.HTTP_200_OK)


class CreateDeck(APIView):
    @api_view(['POST'])
    def create_deck(request):
        deck = Deck.objects.create(
            name=request.data['name'],
            user=User.objects.get(id=request.data['user_id'])
        )
        return Response(f"Successfully created deck {deck.name}", status=status.HTTP_201_CREATED)


class AddCardToDeck(APIView):
    @api_view(['POST'])
    def add_card_to_deck(request, pk):
        pass
