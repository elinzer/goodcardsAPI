from django.contrib import admin
from cards.models import Card, Deck, DeckCard

# Register your models here.
admin.site.register(Card)
admin.site.register(Deck)
admin.site.register(DeckCard)