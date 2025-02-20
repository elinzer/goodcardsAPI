from rest_framework import serializers
from cards.models import Card, DeckCard

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = "__all__"


class CardDeckSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeckCard
        fields = ("deck", "card")

    def validate(self, attrs):
        if attrs["deck"] and attrs["card"]:
            return attrs
        else:
            raise serializers.ValidationError({"Error": "Invalid data"})

    def create(self, validated_data):
        DeckCard.objects.create(
            deck=validated_data["deck"],
            card=validated_data["card"]
        )
        return "Successfully added card to deck"