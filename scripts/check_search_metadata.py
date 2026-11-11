"""Regression checks for metadata derived from the final rendered pages."""
from pathlib import Path
from urllib.parse import parse_qs, urlsplit, urljoin
from bs4 import BeautifulSoup
import json, sys, xml.etree.ElementTree as ET
root = Path(sys.argv[1])
ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9', 'i': 'http://www.google.com/schemas/sitemap-image/1.1'}
count = 0
for entry in ET.parse(root/'sitemap.xml').getroot():
    url = entry.find('s:loc', ns).text
    soup = BeautifulSoup((root/urlsplit(url).path.lstrip('/')/'index.html').read_text(), 'html.parser')
    graph = json.loads(soup.select_one('script[type="application/ld+json"]').string)['@graph']
    page = next(n for n in graph if n.get('@id') == url+'#webpage')
    restaurant = next(n for n in graph if n.get('@type') == 'Restaurant')
    place_id = 'ChIJX5ROthe3yhQRBy7KQJoHBQY'
    map_profile = urlsplit(restaurant['hasMap'])
    assert (map_profile.hostname, map_profile.path) == ('www.google.com', '/maps/search/'), url
    assert parse_qs(map_profile.query)['query_place_id'] == [place_id], url
    route = urlsplit(url).path
    if route in {'/konum/', '/en/location/', '/ru/location/', '/ar/location/'}:
        assert page['mainEntity']['@id'] == restaurant['@id'], url
    if route in {'/kahvalti/', '/en/breakfast/'}:
        assert soup.select_one('.visit-section a[href*="destination_place_id="]'), url
    if route == '/rezervasyon/' or route.endswith('/reservation/'):
        assert len(soup.select('a[href*="destination_place_id="]')) == 2, url
    for link in soup.select('a[href^="https://www.google.com/maps/dir/"]'):
        params = parse_qs(urlsplit(link['href']).query)
        assert params['destination_place_id'] == [place_id], (url, link['href'])
        assert params['travelmode'] == ['walking'], (url, link['href'])
    choices = {urljoin(url, a['href']) for a in soup.select('a[data-menu-choice]')}
    if choices:
        assert {n['@id'] for n in page['mentions']} == choices, (url, 'visible menu references')
    visible = [urljoin(url, i['src']).split('?')[0] for i in soup.select('main img[src][alt]')
               if i['alt'].strip() and i.get('aria-hidden') != 'true']
    listed = [i.find('i:loc', ns).text for i in entry.findall('i:image', ns)]
    assert listed == list(dict.fromkeys(visible)), (url, 'image discovery')
    if visible:
        assert page['primaryImageOfPage']['url'] == visible[0], (url, 'stale primary image')
    expected = {a['href']+'#webpage' for a in soup.select('link[hreflang]') if a['hreflang'] != 'x-default' and a['href'] != url}
    actual = page.get('workTranslation', [])
    if isinstance(actual, dict): actual = [actual]
    assert {a['@id'] for a in actual} == expected, (url, 'translations')
    for article in [n for n in graph if n.get('@type') == 'BlogPosting']:
        assert page['mainEntity']['@id'] == article['@id']
        assert article['image']['url'] == visible[0], (url, 'article image')
    for menu in [n for n in graph if n.get('@type') == 'Menu']:
        assert page['mainEntity']['@id'] == menu['@id']
        assert menu['mainEntityOfPage']['@id'] == page['@id']
    count += len(listed)
print(f'PASS: verified Maps destinations, image metadata, translations and entity relationships; {count} sitemap image entries.')
