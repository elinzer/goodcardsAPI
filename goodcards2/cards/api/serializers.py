from rest_framework import serializers
from cards.models import Card, DeckCard, Deck

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = "__all__"


class DeckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deck
        fields = ('user', 'name')

    def validate(self, attrs):
        if attrs["user"] and attrs["name"]:
            return attrs
        else:
            raise serializers.ValidationError({"Error": "Invalid data"})

    def create(self, validated_data):
        Deck.objects.create(
            name=validated_data['name'],
            user=validated_data['user']
        )
        return "Successfully created deck!"


class CardDeckSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeckCard
        fields = ("deck", "card")

    def validate(self, attrs):
        request = self.context.get('request')
        if not attrs['deck']:
            raise serializers.ValidationError({'deck': 'This field is required.'})
        if attrs['deck'].user.id != request.user.id:
            raise serializers.ValidationError({'deck': "You don't have permission to edit this deck."})
        return attrs

    def create(self, validated_data):
        DeckCard.objects.create(
            deck=validated_data["deck"],
            card=validated_data["card"]
        )
        return "Successfully added card to deck"