"""
Scryfall API integration helpers.
"""


def build_scryfall_url(set_code=None):
    """
    Build the Scryfall API URL based on the set code.

    Args:
        set_code: Optional MTG set code (e.g., 'DSK', 'MKM'). If None, returns URL for random cards.

    Returns:
        str: Scryfall API URL
    """
    if set_code:
        return f"https://api.scryfall.com/cards/search?q=set:{set_code}&unique=prints"
    else:
        return "https://api.scryfall.com/cards/search?q=type:creature&order=random"


def process_card_data(card_data):
    """
    Transform Scryfall card data into our Card model format.
    Handles single-sided, double-sided, split, and other card layouts.
    """
    layout = card_data.get('layout', 'normal')

    card_faces = card_data.get('card_faces', [])
    has_multiple_faces = len(card_faces) > 1

    # Only these layouts actually have a separate back face:
    # - transform: Transform cards (e.g., werewolves)
    # - modal_dfc: Modal double-faced cards
    # - reversible_card: Reversible cards
    # Other layouts like 'split', 'flip', 'adventure' have both faces on one side
    is_double_sided = has_multiple_faces and layout in ['transform', 'modal_dfc', 'reversible_card']

    if is_double_sided:
        front_face = card_faces[0]
        back_face = card_faces[1]

        name = front_face.get('name')
        card_type = front_face.get('type_line', 'Unknown')
        text = front_face.get('oracle_text', '')

        front_image_uris = front_face.get('image_uris', {})
        image_url = front_image_uris.get('normal', front_image_uris.get('large', ''))

        back_name = back_face.get('name')
        back_card_type = back_face.get('type_line', '')
        back_text = back_face.get('oracle_text', '')

        back_image_uris = back_face.get('image_uris', {})
        back_image_url = back_image_uris.get('normal', back_image_uris.get('large', ''))

        # Color identity is at the card level for double-faced cards
        color_identity = ''.join(card_data.get('color_identity', []))
        if not color_identity:
            color_identity = 'C'  # Colorless

        back_color_identity = color_identity

    else:
        name = card_data.get('name')
        card_type = card_data.get('type_line', 'Unknown')
        text = card_data.get('oracle_text', '')

        color_identity = ''.join(card_data.get('color_identity', []))
        if not color_identity:
            color_identity = 'C'  # Colorless

        image_uris = card_data.get('image_uris', {})
        image_url = image_uris.get('normal', image_uris.get('large', ''))

        back_name = None
        back_color_identity = None
        back_card_type = None
        back_text = None
        back_image_url = None

    rarity = card_data.get('rarity', 'common').capitalize()
    mtg_set = card_data.get('set', '').upper()

    return {
        'name': name,
        'color_identity': color_identity[:10],
        'card_type': card_type[:120],
        'rarity': rarity[:50],
        'mtg_set': mtg_set[:3],
        'text': text[:2000] if text else None,
        'image_url': image_url[:1000] if image_url else None,
        # Double-sided card fields
        'layout': layout[:50],
        'is_double_sided': is_double_sided,
        'back_name': back_name[:120] if back_name else None,
        'back_color_identity': back_color_identity[:10] if back_color_identity else None,
        'back_card_type': back_card_type[:120] if back_card_type else None,
        'back_text': back_text[:2000] if back_text else None,
        'back_image_url': back_image_url[:1000] if back_image_url else None,
    }
