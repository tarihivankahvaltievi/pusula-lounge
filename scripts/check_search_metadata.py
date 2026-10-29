"""Regression checks for metadata derived from the final rendered pages."""
from pathlib import Path
from urllib.parse import urlsplit, urljoin
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
print(f'PASS: final image metadata, translations and article relationships; {count} sitemap image entries.')
