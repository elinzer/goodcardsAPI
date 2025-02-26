from rest_framework import serializers
from cards.models import Card, DeckCard, Deck

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = "__all__"


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