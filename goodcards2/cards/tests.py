from django.test import TestCase
from rest_framework import response

from cards.models import Card
from rest_framework.test import APIClient

# Create your tests here.
class TestCard(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_get_cards_list_when_there_are_cards_in_db(self):
        """
        GIVEN when there are cards in the database
        WHEN a get is request is sent
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

        response=self.client.get('/cards/api/card-list')
        self.assertEqual(len(response.data), 2)


    def test_get_cards_list_when_there_are_no_cards_in_db(self):
        pass
