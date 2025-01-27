from django.urls import path
from cards.api.views import CardListView, CardDetailView, CreateDeck, AddCardToDeck

urlpatterns = [
    path('card-list', CardListView.get_cards, name='cards'),
    path('<int:pk>', CardDetailView.get_card_detail, name='card-details'),
    path('deck/create', CreateDeck.create_deck, name='deck-create'),
    path('deck/<int:pk>', AddCardToDeck.add_card_to_deck, name='add-card')
]
