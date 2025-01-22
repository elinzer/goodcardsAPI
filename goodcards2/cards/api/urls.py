from django.urls import path
from cards.api.views import CardListView, CardDetailView, CreateDeck

urlpatterns = [
    path('api/card-list', CardListView.get_cards, name='cards'),
    path('api/<int:pk>', CardDetailView.get_card_detail, name='card-details'),
    path('api/deck/create', CreateDeck.create_deck, name='deck-create'),
]
