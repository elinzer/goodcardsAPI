from tkinter.constants import CASCADE

from django.db import models
from user.models import User


# Create your models here.
class Card(models.Model):
    name = models.CharField(max_length=120)
    color_identity = models.CharField(max_length=10)
    card_type = models.CharField(max_length=120)
    rarity = models.CharField(max_length=50)
    mtg_set = models.CharField(max_length=3)
    text = models.TextField(max_length=2000)
    image_url = models.URLField(max_length=1000)
    
    def __str__(self):
        return self.name


class Deck(models.Model):
    name = models.CharField(max_length=120)
    user = models.ForeignKey(User, on_delete=CASCADE)

    def __str__(self):
        return self.name


class DeckCard(models.Model):
    deck = models.ForeignKey(Deck, on_delete=CASCADE)
    card = models.ForeignKey(Card, on_delete=CASCADE)