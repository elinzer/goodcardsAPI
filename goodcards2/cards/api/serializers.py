from rest_framework import serializers
from cards.models import Card

class CardSerializer(serializers.Serializer):
    name = serializers.CharField()
    color_identity = serializers.CharField()
    card_type = serializers.CharField()
    rarity = serializers.CharField()
    mtg_set = serializers.CharField()
    text = serializers.CharField()
    image_url = serializers.URLField()
    