import requests
import time
from celery import shared_task
from cards.models import Card


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

    # Build the API URL
    if set_code:
        # Fetch cards from a specific set
        url = f"https://api.scryfall.com/cards/search?q=set:{set_code}&unique=prints"
    else:
        # Fetch random cards (for testing)
        url = "https://api.scryfall.com/cards/search?q=type:creature&order=random"

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
                    # Extract card fields
                    # Scryfall uses different field names than our model
                    name = card_data.get('name')

                    # Color identity is a list, join it into a string
                    color_identity = ''.join(card_data.get('color_identity', []))
                    if not color_identity:
                        color_identity = 'C'  # Colorless

                    # Type line contains the card type
                    card_type = card_data.get('type_line', 'Unknown')

                    # Rarity
                    rarity = card_data.get('rarity', 'common').capitalize()

                    # Set code
                    mtg_set = card_data.get('set', '').upper()

                    # Oracle text (rules text)
                    text = card_data.get('oracle_text', '')

                    # Image URL
                    image_uris = card_data.get('image_uris', {})
                    image_url = image_uris.get('normal', image_uris.get('large', ''))

                    # Check if card already exists (by name)
                    # You might want to use Scryfall ID instead for uniqueness
                    if Card.objects.filter(name=name).exists():
                        print(f"Skipping duplicate card: {name}")
                        cards_skipped += 1
                        continue

                    # Create and save the card
                    Card.objects.create(
                        name=name,
                        color_identity=color_identity[:10],  # Limit to field max_length
                        card_type=card_type[:120],  # Limit to field max_length
                        rarity=rarity[:50],  # Limit to field max_length
                        mtg_set=mtg_set[:3],  # Limit to field max_length
                        text=text[:2000] if text else None,  # Limit to field max_length
                        image_url=image_url[:1000] if image_url else None  # Limit to field max_length
                    )

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
