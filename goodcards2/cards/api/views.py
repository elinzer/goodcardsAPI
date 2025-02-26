from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from cards.api.serializers import CardSerializer, CardDeckSerializer
from cards.models import Card, Deck
from user.models import User


class CardListView(APIView):
    #TODO: edit this endpoint to return 404 if no cards
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
    #TODO: serializer for deck creation?
    @api_view(['POST'])
    @authentication_classes([TokenAuthentication])
    @permission_classes([IsAuthenticated])
    def create_deck(request):
        deck = Deck.objects.create(
            name=request.data['name'],
            user=User.objects.get(id=request.user.id)
        )
        return Response(f"Successfully created deck {deck.name}", status=status.HTTP_201_CREATED)


class AddCardToDeck(APIView):
    @api_view(['POST'])
    @authentication_classes([TokenAuthentication])
    @permission_classes([IsAuthenticated])
    def add_card_to_deck(request, pk):
        data = {"deck": pk, "card": request.data['card']}
        serializer = CardDeckSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response("Successfully added card to deck", status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
