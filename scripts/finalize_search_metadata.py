"""Derive search metadata from final rendered content, after design builders."""
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote
import json, re, sys
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

ROOT = Path(sys.argv[1]).resolve()
ORIGIN = 'https://www.pusulalounge.com'
S = 'http://www.sitemaps.org/schemas/sitemap/0.9'
I = 'http://www.google.com/schemas/sitemap-image/1.1'
X = 'http://www.w3.org/1999/xhtml'
for prefix, uri in [('', S), ('image', I), ('xhtml', X)]:
    ET.register_namespace(prefix, uri)
tree = ET.parse(ROOT / 'sitemap.xml')
for entry in tree.getroot():
    url = entry.find(f'{{{S}}}loc').text
    file = ROOT / urlsplit(url).path.lstrip('/') / 'index.html'
    text = file.read_text()
    soup = BeautifulSoup(text, 'html.parser')
    images = []
    for img in soup.select('main img[src][alt]'):
        if not img['alt'].strip() or img.get('aria-hidden') == 'true':
            continue
        src = urljoin(url, img['src']).split('?')[0]
        parts = urlsplit(src)
        if parts.netloc != urlsplit(ORIGIN).netloc or not (ROOT / unquote(parts.path).lstrip('/')).is_file():
            continue
        if src not in [i['url'] for i in images]:
            image = {'@type': 'ImageObject', 'url': src, 'contentUrl': src,
                     'caption': img['alt'], 'inLanguage': soup.html['lang']}
            for key in ['width', 'height']:
                if str(img.get(key, '')).isdigit():
                    image[key] = int(img[key])
            images.append(image)
    def update_schema(match):
        data = json.loads(match.group(2))
        graph = data.get('@graph', [])
        menu = next((n for n in graph if n.get('@type') == 'Menu'), None)
        article = next((n for n in graph if n.get('@type') == 'BlogPosting'), None)
        for node in graph:
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
                if menu:
                    node['mainEntity'] = {'@id': menu['@id']}
                    menu['mainEntityOfPage'] = {'@id': node['@id']}
                if article:
                    node['mainEntity'] = {'@id': article['@id']}
            if node.get('@type') == 'BlogPosting' and images:
                node['image'] = images[0]
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
