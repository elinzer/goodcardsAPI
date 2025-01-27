from django.test import TestCase
from rest_framework import response
from cards.models import Card
from rest_framework.test import APIClient


class TestCard(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.response = response

    def test_get_cards_list_when_there_are_cards_in_db(self):
        """
        GIVEN when there are cards in the database
        WHEN a GET request is sent
        THEN it should return a list of cards.
        """
        card1 = Card.objects.create(
            name="Cool Card",
            color_identity="G",
            card_type="Legendary",
            rarity="Common",
            mtg_set="DSK",
            text="A cool card",
            image_url="www.imagurl.com"
        )
        card2 = Card.objects.create(
            name="Another Cool Card",
            color_identity="G",
            card_type="Legendary",
            rarity="Uncommon",
            mtg_set="DSK",
            text="Another cool card",
            image_url="www.imagurl.com"
        )

        self.response=self.client.get('/cards/api/card-list')
        self.assertEqual(len(self.response.data), 2)


    def test_get_card_details_when_there_are_cards_in_db(self):
        """
        GIVEN when there are cards in the database
        WHEN a GET request is sent
        THEN it should return a single card's details.
        """
        card1 = Card.objects.create(
            name="Cool Card",
            color_identity="G",
            card_type="Legendary",
            rarity="Common",
            mtg_set="DSK",
            text="A cool card",
            image_url="www.imagurl.com"
        )

        #TODO: can i test this with {pk} instead of "1"?
        self.response=self.client.get('/cards/api/1')
        self.assertEqual(self.response.data['name'], "Cool Card")


    def test_get_card_details_when_theres_no_card(self):
        """
        GIVEN the card does not exist
        WHEN a GET request is sent
        THEN it should return a message saying no card found.
        """
        self.response=self.client.get('/cards/api/1')
        self.assertEqual(self.response.data['message'], "No card found")