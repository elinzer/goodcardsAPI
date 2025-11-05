"""
One-time script to fix existing double-sided cards in the database.
Run this script once after running migrations.

Usage:
    python fix_double_sided_cards.py
"""

import os
import django
import requests
import time

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'goodcards2.settings')
django.setup()

from cards.models import Card
from cards.scryfall import process_card_data


def fetch_card_from_scryfall(card_name, set_code):
    """Fetch a specific card from Scryfall by name and set."""
    url = f"https://api.scryfall.com/cards/named"
    params = {
        'fuzzy': card_name,
        'set': set_code
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"  Error fetching {card_name}: {e}")
        return None


def fix_double_sided_cards():
    """Find and fix double-sided cards that are missing back face data."""
    print("Starting double-sided card fix...\n")

    # Get all cards (we'll check each one)
    all_cards = Card.objects.all()
    total_cards = all_cards.count()

    print(f"Checking {total_cards} cards...\n")

    updated_count = 0
    skipped_count = 0
    error_count = 0

    for i, card in enumerate(all_cards, 1):
        print(f"[{i}/{total_cards}] Checking: {card.name} ({card.mtg_set})")

        # Fetch fresh data from Scryfall for all cards
        scryfall_data = fetch_card_from_scryfall(card.name, card.mtg_set)

        if not scryfall_data:
            print(f"  ✗ Could not fetch from Scryfall")
            error_count += 1
            time.sleep(0.1)  # Respect rate limits
            continue

        # Process the data to get correct layout and is_double_sided values
        processed_data = process_card_data(scryfall_data)

        # Check if we need to update this card
        needs_update = (
            card.layout != processed_data['layout'] or
            card.is_double_sided != processed_data['is_double_sided'] or
            (not card.image_url and processed_data['image_url'])
        )

        if needs_update:
            print(f"  → Updating card...")
            print(f"     Old: layout={card.layout}, is_double_sided={card.is_double_sided}")
            print(f"     New: layout={processed_data['layout']}, is_double_sided={processed_data['is_double_sided']}")

            # Update all fields
            card.layout = processed_data['layout']
            card.is_double_sided = processed_data['is_double_sided']
            card.back_name = processed_data['back_name']
            card.back_color_identity = processed_data['back_color_identity']
            card.back_card_type = processed_data['back_card_type']
            card.back_text = processed_data['back_text']
            card.back_image_url = processed_data['back_image_url']

            # Also update front face in case it was missing image
            if not card.image_url and processed_data['image_url']:
                card.image_url = processed_data['image_url']
                print(f"  → Also updated front image")

            card.save()

            print(f"  ✓ Updated: {card.name}")
            updated_count += 1
        else:
            print(f"  - No update needed")
            skipped_count += 1

        # Respect Scryfall's rate limit (100ms between requests)
        time.sleep(0.1)

    print("\n" + "="*60)
    print("Fix complete!")
    print(f"Total cards checked: {total_cards}")
    print(f"Updated: {updated_count}")
    print(f"Skipped: {skipped_count}")
    print(f"Errors: {error_count}")
    print("="*60)


if __name__ == '__main__':
    fix_double_sided_cards()
