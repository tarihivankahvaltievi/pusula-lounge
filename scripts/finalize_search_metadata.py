"""Derive search metadata from final rendered content, after design builders."""
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote
import hashlib, json, mimetypes, re, sys
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from PIL import Image
from business_entity import MAPS_PROFILE

ROOT = Path(sys.argv[1]).resolve()
ORIGIN = 'https://www.pusulalounge.com'
GOOGLE_SEARCH_SHARE = 'https://share.google/l1BSBLDwv6suQkW7Y'
INSTAGRAM_PROFILE = 'https://www.instagram.com/pusulalounge/'
S = 'http://www.sitemaps.org/schemas/sitemap/0.9'
I = 'http://www.google.com/schemas/sitemap-image/1.1'
X = 'http://www.w3.org/1999/xhtml'
HOME_PATHS = {'/', '/en/', '/ru/', '/ar/'}
LOCATION_PATHS = {'/konum/', '/en/location/', '/ru/location/', '/ar/location/'}
for prefix, uri in [('', S), ('image', I), ('xhtml', X)]:
    ET.register_namespace(prefix, uri)
BREAKFAST_PATHS = {'/kahvalti/', '/en/breakfast/'}
BREAKFAST_IMAGE = '/assets/gallery/pusula-sofrasi'
BREAKFAST_VARIANTS = {}
for extension in ('avif', 'webp'):
    path = f'{BREAKFAST_IMAGE}-screen-800.{extension}'
    version = hashlib.sha256((ROOT / path.lstrip('/')).read_bytes()).hexdigest()[:12]
    BREAKFAST_VARIANTS[extension] = f'{path}?v={version} 800w'


def improve_breakfast_image(text):
    def update_picture(match):
        picture = match.group(0)
        for extension, candidate in BREAKFAST_VARIANTS.items():
            picture = re.sub(
                rf'({BREAKFAST_IMAGE}-screen-600\.{extension}(?:\?v=[0-9a-f]+)? 600w), '
                rf'(?:{BREAKFAST_IMAGE}-screen-800\.{extension}(?:\?v=[0-9a-f]+)? 800w, )?',
                lambda size: f'{size[1]}, {candidate}, ',
                picture,
            )
        if 'fetchpriority=' not in picture:
            picture = picture.replace('<img ', '<img fetchpriority="high" ', 1)
        return picture

    return re.sub(
        rf'<picture>[^<]*(?:(?!</picture>).)*{BREAKFAST_IMAGE}-1200\.webp(?:(?!</picture>).)*</picture>',
        update_picture, text, count=1, flags=re.S,
    )


tree = ET.parse(ROOT / 'sitemap.xml')
for entry in tree.getroot():
    url = entry.find(f'{{{S}}}loc').text
    file = ROOT / urlsplit(url).path.lstrip('/') / 'index.html'
    text = file.read_text()
    # The old share link opens Google Search. Map links should open the
    # verified place in Maps, while links labelled reviews keep their purpose.
    def map_link(match):
        tag = BeautifulSoup(match.group(0), 'html.parser').a
        if tag.get('href') != GOOGLE_SEARCH_SHARE or tag.get('data-interaction') == 'reviews':
            return match.group(0)
        tag['href'] = MAPS_PROFILE
        return str(tag).removesuffix('</a>')
    text = re.sub(r'<a\b[^>]*>', map_link, text)
    route = urlsplit(url).path
    if route in BREAKFAST_PATHS or route == '/en/':
        text = improve_breakfast_image(text)
    soup = BeautifulSoup(text, 'html.parser')
    social = soup.select_one('meta[property="og:image"]')
    if social and social.get('content'):
        media_type, _ = mimetypes.guess_type(urlsplit(social['content']).path)
        if media_type and media_type.startswith('image/'):
            text = re.sub(r'(<meta\b[^>]*property="og:image:type"[^>]*content=")[^"]+(")',
                          lambda match: match[1] + media_type + match[2], text)
            text = re.sub(r'(<meta\b[^>]*content=")[^"]+("[^>]*property="og:image:type"[^>]*>)',
                          lambda match: match[1] + media_type + match[2], text)
    images = []
    for img in soup.select('main img[src][alt]'):
        if not img['alt'].strip() or img.get('aria-hidden') == 'true':
            continue
        src = urljoin(url, img['src']).split('?')[0]
        parts = urlsplit(src)
        asset = ROOT / unquote(parts.path).lstrip('/')
        if parts.netloc != urlsplit(ORIGIN).netloc or not asset.is_file():
            continue
        if src not in [i['url'] for i in images]:
            image = {'@type': 'ImageObject', 'url': src, 'contentUrl': src,
                     'caption': img['alt'], 'inLanguage': soup.html['lang']}
            with Image.open(asset) as photo:
                image['width'], image['height'] = photo.size
            images.append(image)
    def update_schema(match):
        data = json.loads(match.group(2))
        graph = data.get('@graph', [])
        restaurant = next((n for n in graph if n.get('@type') == 'Restaurant'), None)
        menu = next((n for n in graph if n.get('@type') == 'Menu'), None)
        article = next((n for n in graph if n.get('@type') == 'BlogPosting'), None)
        for node in graph:
            if node.get('@type') == 'Restaurant':
                node['hasMap'] = MAPS_PROFILE
                # Connect the site’s verified social profile to its canonical
                # business entity for search and knowledge graph consumers.
                profiles = node.get('sameAs', [])
                if isinstance(profiles, str):
                    profiles = [profiles]
                node['sameAs'] = list(dict.fromkeys([*profiles, INSTAGRAM_PROFILE]))
            if node.get('@id') == url + '#webpage':
                # Reference the same real dishes that visitors can compare and
                # open in the local-language menu. No separate AI-only facts.
                choices = list(dict.fromkeys(urljoin(url, a['href']) for a in soup.select('a[data-menu-choice][href]')))
                if choices:
                    node['mentions'] = [{'@id': choice} for choice in choices]
                if images:
                    node['primaryImageOfPage'] = images[0]
                translations = [{'@id': a['href'] + '#webpage'} for a in soup.select('link[hreflang]')
                                if a['hreflang'] != 'x-default' and a['href'] != url]
                if translations:
                    node['workTranslation'] = translations
                if restaurant and (route in HOME_PATHS or route in LOCATION_PATHS):
                    node['mainEntity'] = {'@id': restaurant['@id']}
                if menu:
                    node['mainEntity'] = {'@id': menu['@id']}
                    menu['mainEntityOfPage'] = {'@id': node['@id']}
                if article:
                    node['mainEntity'] = {'@id': article['@id']}
            if node.get('@type') == 'BlogPosting':
                if images:
                    node['image'] = images[0]
                if restaurant:
                    node.setdefault('about', {'@id': restaurant['@id']})
        return match.group(1) + json.dumps(data, ensure_ascii=False).replace('<', '\\u003c') + match.group(3)
    text = re.sub(r'(<script\b[^>]*type="application/ld\+json"[^>]*>)(.*?)(</script>)', update_schema, text, flags=re.S)
    file.write_text(text)
    # Publish only actual content images; exclude decorative logos and textures.
    for old in list(entry.findall(f'{{{I}}}image')):
        entry.remove(old)
    for img in images:
        node = ET.SubElement(entry, f'{{{I}}}image')
        ET.SubElement(node, f'{{{I}}}loc').text = img['url']
ET.indent(tree, space='  ')
tree.write(ROOT / 'sitemap.xml', encoding='unicode', xml_declaration=True)
print('Final search metadata aligned with visible images and language alternatives.')
