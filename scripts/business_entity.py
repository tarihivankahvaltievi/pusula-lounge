"""Verified business location and Google Maps links shared by the site."""

from urllib.parse import urlencode

# Matches the linked Google Maps business entity for Pusula Lounge, checked
# against its No:3 address on 2026-10-28.
POSTAL_CODE = '34221'
LATITUDE = 41.0352493
LONGITUDE = 28.9825902
ADDRESS = 'Katip Mustafa Çelebi Mahallesi, Küçük Parmak Kapı Sokak, Sinek Çıkmazı No:3, Beyoğlu / İstanbul'
MAPS_PLACE_ID = 'ChIJX5ROthe3yhQRBy7KQJoHBQY'
MAPS_DESTINATION = f'Pusula Lounge, {ADDRESS}'
MAPS_PROFILE = 'https://www.google.com/maps/search/?' + urlencode({
    'api': 1, 'query': MAPS_DESTINATION, 'query_place_id': MAPS_PLACE_ID,
})
WALKING_DIRECTIONS = 'https://www.google.com/maps/dir/?' + urlencode({
    'api': 1, 'destination': MAPS_DESTINATION, 'destination_place_id': MAPS_PLACE_ID,
    'travelmode': 'walking',
})


def apply_restaurant_location(restaurant):
    """Keep the structured address and map pin aligned across every route."""
    restaurant.setdefault('address', {})['postalCode'] = POSTAL_CODE
    restaurant['geo'] = {
        '@type': 'GeoCoordinates',
        'latitude': LATITUDE,
        'longitude': LONGITUDE,
    }
    return restaurant
