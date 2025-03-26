import time
import requests
from django.core.management.base import BaseCommand
from cards.models import Card, ImportTracker

class Command(BaseCommand):
    help = 'Import new Magic: The Gathering cards'

    def handle(self, *args, **kwargs):
        tracker, created = ImportTracker.objects.get_or_create(id=1)
        page = tracker.last_page
        while True:
            self.stdout.write(f"Fetching page {page}...")
            response = requests.get(f'https://api.magicthegathering.io/v1/cards?page={page}')

            if response.status_code != 200:
                self.stdout.write(f"Error: {response.status_code}")
                break

            cards = response.json().get('cards', [])
            if not cards:
                self.stdout.write("No more cards found.")
                break

            new_cards = []
            for card_data in cards:
                multiverse_id = card_data.get('multiverseid')
                if not Card.objects.filter(multiverse_id=multiverse_id).exists():
                    new_cards.append(Card(
                        name=card_data.get('name'),
                        multiverse_id=multiverse_id,
                        color_identity=card_data.get('colorIdentity'),
                        card_type=card_data.get('type'),
                        rarity=card_data.get('rarity'),
                        mtg_set=card_data.get('set'),
                        image_url=card_data.get('imageUrl'),
                        text=card_data.get('text')
                    ))


            if new_cards:
                Card.objects.bulk_create(new_cards, ignore_conflicts=True)
                self.stdout.write(f"Added {len(new_cards)} new cards.")

            tracker.last_page = page
            tracker.save()

            time.sleep(2)
            page += 1
