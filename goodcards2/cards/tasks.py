import requests
import time
from celery import shared_task
from cards.models import Card
from cards.scryfall import build_scryfall_url, process_card_data


@shared_task
def fetch_cards_from_scryfall(set_code=None, limit=100):
    """
    Fetch MTG cards from Scryfall API and save to database.

    Args:
        set_code: Optional MTG set code (e.g., 'DSK', 'MKM'). If None, fetches random cards.
        limit: Maximum number of cards to fetch (default: 100)

    Returns:
        dict: Summary of cards fetched and saved
    """
    print(f"Starting Scryfall fetch task - Set: {set_code}, Limit: {limit}")

    url = build_scryfall_url(set_code)
    cards_saved = 0
    cards_skipped = 0
    errors = []

    try:
        # Scryfall returns paginated results
        while url and cards_saved < limit:
            print(f"Fetching from: {url}")

            # Make request to Scryfall API
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            # Process each card in the response
            for card_data in data.get('data', []):
                if cards_saved >= limit:
                    break

                try:
                    # Process the card data
                    processed_data = process_card_data(card_data)
                    name = processed_data['name']

                    # Check if card already exists (by name)
                    # You might want to use Scryfall ID instead for uniqueness
                    if Card.objects.filter(name=name).exists():
                        print(f"Skipping duplicate card: {name}")
                        cards_skipped += 1
                        continue

                    # Create and save the card
                    Card.objects.create(**processed_data)

                    cards_saved += 1
                    print(f"Saved card {cards_saved}/{limit}: {name}")

                except Exception as e:
                    error_msg = f"Error saving card {card_data.get('name', 'Unknown')}: {str(e)}"
                    print(error_msg)
                    errors.append(error_msg)

            # Get next page URL if available
            url = data.get('next_page')

            # Scryfall asks for a 100ms delay between requests
            if url:
                time.sleep(0.1)

        result = {
            'status': 'completed',
            'cards_saved': cards_saved,
            'cards_skipped': cards_skipped,
            'errors': errors
        }
        print(f"Task completed: {result}")
        return result

    except Exception as e:
        error_msg = f"Fatal error during fetch: {str(e)}"
        print(error_msg)
        return {
            'status': 'failed',
            'cards_saved': cards_saved,
            'cards_skipped': cards_skipped,
            'error': error_msg,
            'errors': errors
        }
