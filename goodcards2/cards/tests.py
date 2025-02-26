from django.test import TestCase
from django.urls import reverse
from rest_framework import response
from cards.models import Card
from rest_framework.test import APIClient


class TestCard(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.response = response
        self.test_card = Card.objects.create(
            name="Cool Card",
            color_identity="G",
            card_type="Legendary",
            rarity="Common",
            mtg_set="DSK",
            text="A cool card",
            image_url="www.imagurl.com"
        )

    def test_get_cards_list_when_there_are_cards_in_db(self):
        """
        GIVEN when there are cards in the database
        WHEN a GET request is sent
        THEN it should return a list of cards.
        """
        Card.objects.create(
            name="Cool Card 2",
            color_identity="G",
            card_type="Legendary",
            rarity="Common",
            mtg_set="DSK",
            text="A cool card",
            image_url="www.imagurl.com"
        )
        self.response=self.client.get('/api/cards/card-list')
        self.assertEqual(len(self.response.data), 2)


    def test_get_card_details_when_there_are_cards_in_db(self):
        """
        GIVEN when there are cards in the database
        WHEN a GET request is sent
        THEN it should return a single card's details.
        """
        url = reverse('card-details', kwargs={'pk': self.test_card.pk})
        self.response=self.client.get(url)
        self.assertEqual(self.response.data['name'], "Cool Card")


    def test_get_card_details_when_theres_no_card(self):
        """
        GIVEN the card does not exist
        WHEN a GET request is sent
        THEN it should return a message saying no card found.
        """
        pk = self.test_card.pk
        self.test_card.delete()
        url = reverse('card-details', kwargs={'pk': pk})

        self.response=self.client.get(url)
        self.assertEqual(self.response.status_code, 404)