"""Verified location fields shared by the site's Restaurant JSON-LD builders."""

# Matches the linked Google Maps business entity for Pusula Lounge, checked
# against its No:3 address on 2026-10-28.
POSTAL_CODE = '34221'
LATITUDE = 41.0352493
LONGITUDE = 28.9825902


def apply_restaurant_location(restaurant):
    """Keep the structured address and map pin aligned across every route."""
    restaurant.setdefault('address', {})['postalCode'] = POSTAL_CODE
    restaurant['geo'] = {
        '@type': 'GeoCoordinates',
        'latitude': LATITUDE,
        'longitude': LONGITUDE,
    }
    return restaurant
