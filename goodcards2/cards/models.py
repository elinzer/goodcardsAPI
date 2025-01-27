from django.db import models
from django.db.models import CASCADE
from user.models import User


# Create your models here.
class Card(models.Model):

    class Meta:
        db_table = 'card'

    name=models.CharField(max_length=120, null=False)
    color_identity=models.CharField(max_length=10, null=False)
    card_type=models.CharField(max_length=120, null=False)
    rarity=models.CharField(max_length=50, null=False)
    mtg_set=models.CharField(max_length=3, null=False)
    text=models.TextField(max_length=2000, null=True)
    image_url=models.URLField(max_length=1000, null=True)
    
    def __str__(self):
        return self.name


class Deck(models.Model):
    name=models.CharField(max_length=120)
    user=models.ForeignKey(User, on_delete=CASCADE)

    def __str__(self):
        return self.name


class DeckCard(models.Model):

    class Meta:
        db_table = 'deck_card'

    deck=models.ForeignKey(Deck, on_delete=CASCADE, related_name='cards')
    card=models.ForeignKey(Card, on_delete=CASCADE)
