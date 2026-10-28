"""Complete RU/AR visitor journeys and align public SEO data with the visible menu.

Run after the existing tourism/reservation builders. Never translates prices or
changes business facts. Existing canonical URLs and reservation behavior survive.
"""
from pathlib import Path
from html import escape
from urllib.parse import urlsplit
import base64
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

ROOT = Path(sys.argv[1]).resolve()
ORIGIN = 'https://www.pusulalounge.com'
DATE = '2026-10-28'
MAP = 'https://share.google/l1BSBLDwv6suQkW7Y'
ADDRESS = 'Katip Mustafa Çelebi Mahallesi, Küçük Parmak Kapı Sokak, Sinek Çıkmazı No:3, Beyoğlu / İstanbul'
COPY = json.loads((Path(__file__).parent / 'international_copy.json').read_text())
GROUPS = [
    {'tr': '/', 'en': '/en/', 'ru': '/ru/', 'ar': '/ar/'},
    {'tr': '/menu/', 'en': '/en/menu/', 'ru': '/ru/menu/', 'ar': '/ar/menu/'},
    {'tr': '/konum/', 'en': '/en/location/', 'ru': '/ru/location/', 'ar': '/ar/location/'}
]
LABELS = {'tr': 'Türkçe', 'en': 'English', 'ru': 'Русский', 'ar': 'العربية'}
S = 'http://www.sitemaps.org/schemas/sitemap/0.9'
X = 'http://www.w3.org/1999/xhtml'
I = 'http://www.google.com/schemas/sitemap-image/1.1'
before = {p: p.read_bytes() for p in ROOT.rglob('index.html') if '.git' not in p.parts}


def e(value):
    return escape(str(value), quote=True)


def dump(value):
    return json.dumps(value, ensure_ascii=False).replace('<', '\\u003c')


def file_for(route):
    return ROOT / route.lstrip('/') / 'index.html'


def ref(path, script=False):
    data = (ROOT / path.lstrip('/')).read_bytes()
    digest = hashlib.sha256(data)
    href = path + '?v=' + digest.hexdigest()[:12]
    sri = 'sha256-' + base64.b64encode(digest.digest()).decode()
    if script:
        return f'<script src="{href}" integrity="{sri}" crossorigin="anonymous" defer></script>'
    return f'<link rel="stylesheet" href="{href}" integrity="{sri}" crossorigin="anonymous">'


def a(path, label, cls=''):
    return f'<a href="{e(path)}"' + (f' class="{cls}"' if cls else '') + f'>{e(label)}</a>'


def section(title, text):
    return f'<section class="visit-section"><h2>{e(title)}</h2><p>{e(text)}</p></section>'


source = BeautifulSoup((ROOT / 'en/menu/index.html').read_text(), 'html.parser')
identity = [n for n in json.loads(source.select_one('script[type="application/ld+json"]').string)['@graph']
            if n['@type'] in ['Restaurant', 'WebSite']]
source_sections = source.select('main > section[id]')
assert [s['id'] for s in source_sections] == ['kahvalti', 'gozlemeler', 'menemenler', 'omletler']
source_ids = [row['id'] for s in source_sections for row in s.select('.menu-row')]
turkish_menu = BeautifulSoup((ROOT/'menu/index.html').read_text(), 'html.parser')
for item_id in source_ids:
    tr_row, en_row = turkish_menu.find(id=item_id), source.find(id=item_id)
    assert tr_row, f'Turkish menu item missing: {item_id}'
    tr_prices = tr_row.select('.portion-prices b') or tr_row.select('.price')
    en_prices = en_row.select('.portion-list strong') or en_row.select('.menu-row-price')
    digits = lambda values:[re.sub(r'[^0-9]','',v.get_text()) for v in values]
    assert digits(tr_prices) == digits(en_prices), f'TR/EN menu price mismatch: {item_id}'
new_routes = []

# Keep the visitor-facing HTML site maps useful as the site grows.
article_copy = json.loads((Path(__file__).parent/'van_breakfast_article.json').read_text())
for lang,routes in [('tr',['/kahvalti/','/kahvalti-rehberi/']),('en',['/en/breakfast/','/en/breakfast-guide/'])]:
    for path in routes:
        file = file_for(path)
        text = re.sub(r'<!-- VAN-ARTICLE:START -->.*?<!-- VAN-ARTICLE:END -->','',file.read_text(),flags=re.S)
        article_route = '/en/blog/'+article_copy['en']+'/' if lang=='en' else '/blog/'+article_copy['slug']+'/'
        label = 'From the Van tradition to your table' if lang=='en' else 'Van geleneğinden masanıza'
        link = '<!-- VAN-ARTICLE:START --><section class="visit-section"><h2>'+label+'</h2><p>'+a(article_route,article_copy['title'][int(lang=='en')])+'</p></section><!-- VAN-ARTICLE:END -->'
        file.write_text(text.replace('</main>',link+'</main>'))
for lang,path in [('tr','/site-haritasi/'),('en','/en/site-map/')]:
    file = file_for(path)
    text = re.sub(r'<!-- INTERNATIONAL-MAP:START -->.*?<!-- INTERNATIONAL-MAP:END -->','',file.read_text(),flags=re.S)
    links = '<!-- INTERNATIONAL-MAP:START --><section class="visit-section"><h2>' + ('Breakfast reading and other languages' if lang == 'en' else 'Kahvaltı yazıları ve diğer diller') + '</h2><ul>'
    for code in ['ru','ar']:
        for index,route in enumerate([f'/{code}/',f'/{code}/menu/',f'/{code}/location/']):
            label = COPY[code][['heading','menu','location'][index]]
            links += f'<li><a href="{route}" lang="{code}" dir="auto">{e(label)}</a></li>'
    for en in [False,True]:
        route = '/en/blog/'+article_copy['en']+'/' if en else '/blog/'+article_copy['slug']+'/'
        links += '<li>'+a(route,article_copy['title'][int(en)])+'</li>'
    links += '</ul></section><!-- INTERNATIONAL-MAP:END -->'
    file.write_text(text.replace('</main>',links+'</main>'))

for lang, c in COPY.items():
    assert set(source_ids) == set(c['items']), f'{lang}: translation missing or menu structure changed'
    home, menu, location = f'/{lang}/', f'/{lang}/menu/', f'/{lang}/location/'
    reservation = f'/{lang}/reservation/'
    header = f'<header class="visit-header">{a(home, "Pusula Lounge", "visit-brand")}<nav aria-label="{e(c["navigation"])}">' + ''.join(a(p, c[k]) for p, k in [(home, 'home'), (menu, 'menu'), (location, 'location'), (reservation, 'reservation')]) + '</nav></header>'
    footer = f'<footer class="visit-footer"><p><strong>Pusula Lounge</strong><br>Beyoğlu · İstanbul</p><address class="address-latin" lang="tr">{e(ADDRESS)}</address><p>{a("tel:+905078162994", c["call"])} <bdi dir="ltr">+90 507 816 29 94</bdi></p><p>{e(c["hours"])}</p><p>{a(MAP, c["map"])}</p><p class="business-source">{e(c["sourceNote"])}</p></footer>'
    actions = '<div class="visit-actions">' + a(reservation, c['reservation'], 'visit-button') + a(menu, c['menu']) + a(location, c['location']) + '</div>'
    photo = f'<figure><img src="/assets/gallery/pusula-sofrasi-600.webp" srcset="/assets/gallery/pusula-sofrasi-600.webp 600w, /assets/gallery/pusula-sofrasi-1200.webp 1200w" sizes="(max-width:700px) calc(100vw - 40px), 500px" alt="{e(c["photoAlt"])}" width="1200" height="800" decoding="async" fetchpriority="high"><figcaption>{e(c["photoCaption"])}</figcaption></figure>'

    for kind in ['home', 'menu', 'location']:
        route = {'home': home, 'menu': menu, 'location': location}[kind]
        url = ORIGIN + route
        title = c['title'] if kind == 'home' else c[kind + 'Title']
        desc = c['description'] if kind == 'home' else c[kind + 'Description']
        heading = c['heading'] if kind == 'home' else c[kind + 'Heading']
        lead = c['lead'] if kind == 'home' else c[kind + 'Lead']
        graph = json.loads(json.dumps(identity))
        restaurant = graph[0]
        restaurant['acceptsReservations'] = ORIGIN + reservation
        restaurant['contactPoint']['url'] = ORIGIN + reservation
        web = {'@type': 'WebPage', '@id': url + '#webpage', 'url': url, 'name': title,
               'description': desc, 'inLanguage': lang, 'isPartOf': {'@id': ORIGIN + '/#website'},
               'about': {'@id': ORIGIN + '/#restaurant'}, 'translationOfWork': {'@id': ORIGIN + GROUPS[['home', 'menu', 'location'].index(kind)]['tr'] + '#webpage'}}
        graph.append(web)
        crumb = ''
        if kind != 'home':
            graph.append({'@type': 'BreadcrumbList', '@id': url + '#breadcrumb', 'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': c['home'], 'item': ORIGIN + home},
                {'@type': 'ListItem', 'position': 2, 'name': heading, 'item': url}]})
            web['breadcrumb'] = {'@id': url + '#breadcrumb'}
            crumb = f'<nav class="seo-breadcrumb" aria-label="{e(c["breadcrumb"])}"><ol><li>{a(home,c["home"])}</li><li><span aria-current="page">{e(heading)}</span></li></ol></nav>'
        body = crumb + f'<div class="visit-intro"><h1>{e(heading)}</h1><p class="lead">{e(lead)}</p></div>'
        if kind == 'home':
            web['mainEntity'] = {'@id': ORIGIN + '/#restaurant'}
            web['primaryImageOfPage'] = {'@type': 'ImageObject', 'url': ORIGIN + '/assets/gallery/pusula-sofrasi-1200.webp', 'width': 1200, 'height': 800, 'caption': c['photoAlt']}
            body += actions + f'<div class="visit-spread"><div><h2>{e(c["spreadTitle"])}</h2><p>{e(c["spreadText"])}</p>{a(menu,c["menu"])}</div>{photo}</div>'
            body += section(c['hotTitle'], c['hotText']) + section(c['hoursTitle'], c['hoursText']) + section(c['bookingTitle'], c['bookingText']) + actions
        elif kind == 'menu':
            body += f'<p>{e(c["hours"])}</p><nav class="menu-jump" aria-label="{e(c["menu"])}">' + ''.join(a('#' + s['id'], label) for s, label in zip(source_sections, c['categories'])) + '</nav>'
            menu_node = {'@type': 'Menu', '@id': url + '#menu', 'url': url, 'name': heading, 'inLanguage': lang, 'hasMenuSection': []}
            for s, label in zip(source_sections, c['categories']):
                ms = {'@type': 'MenuSection', '@id': url + '#' + s['id'], 'name': label, 'hasMenuItem': []}
                body += f'<section class="visit-section" id="{s["id"]}"><h2>{e(label)}</h2>'
                for row in s.select('.menu-row'):
                    item_id = row['id']
                    name, description = c['items'][item_id]
                    body += f'<article class="menu-row" id="{item_id}"><h3>{e(name)}</h3><p>{e(description)}</p>'
                    if row.select('.portion-list li'):
                        body += '<ul class="portion-list">'
                        for index, price in enumerate(row.select('.portion-list strong'), start=2):
                            people = c['people'].format(n=index)
                            if lang == 'ar' and index == 2:
                                people = 'لشخصين'
                            body += f'<li>{e(people)} <strong dir="ltr">{e(price.get_text())}</strong></li>'
                        body += '</ul>'
                    else:
                        body += f'<p class="menu-row-price"><bdi dir="ltr">{e(row.select_one(".menu-row-price").get_text())}</bdi></p>'
                    body += '</article>'
                    ms['hasMenuItem'].append({'@type': 'MenuItem', '@id': url + '#' + item_id, 'url': url + '#' + item_id, 'name': name, 'description': description})
                menu_node['hasMenuSection'].append(ms)
                body += '</section>'
            graph.append(menu_node)
            web['mainEntity'] = {'@id': url + '#menu'}
            body += f'<p>{e(c["priceNote"])}</p><p class="note">{e(c["dietary"])}</p>' + section(c['bookingTitle'],c['bookingText']) + actions
        else:
            body += f'<section class="visit-section"><h2>{e(c["addressLabel"])}</h2><address class="address-latin" lang="tr">{e(ADDRESS)}</address><p>{e(c["locationText"])}</p><div class="visit-actions">{a(MAP,c["map"],"visit-button")}{a("tel:+905078162994",c["call"])} <bdi dir="ltr">+90 507 816 29 94</bdi></div></section>'
            body += section(c['hoursTitle'],c['hoursText']) + f'<p>{e(c["accessText"])}</p>' + section(c['bookingTitle'],c['bookingText']) + actions
        meta = f'<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{url}"><meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">'
        for k, val in {'type':'website','site_name':'Pusula Lounge','title':title,'description':desc,'url':url,'locale':c['locale'],'image':ORIGIN+'/assets/gallery/pusula-sofrasi-share.jpg','image:width':1200,'image:height':800,'image:alt':c['photoAlt']}.items():
            meta += f'<meta property="og:{k}" content="{e(val)}">'
        for k, val in {'card':'summary_large_image','title':title,'description':desc,'image':ORIGIN+'/assets/gallery/pusula-sofrasi-share.jpg','image:alt':c['photoAlt']}.items():
            meta += f'<meta name="twitter:{k}" content="{e(val)}">'
        if lang == 'ar':
            # A numeric time range must keep its LTR order inside Arabic text.
            protect = lambda value:re.sub(r'\b\d{2}:\d{2}[–-]\d{2}:\d{2}\b',lambda m:'<bdi dir="ltr">'+m.group(0)+'</bdi>',value)
            body = protect(body)
            page_footer = protect(footer)
        else:
            page_footer = footer
        css = ''.join(ref(p) for p in ['/assets/menu/fonts.css','/visit.css','/seo-common.css','/international.css'])
        page = f'<!doctype html><html lang="{lang}"' + (' dir="rtl"' if lang == 'ar' else '') + f'><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">{meta}<link rel="icon" href="/assets/pusula-amblem.png">{css}<script type="application/ld+json">{dump({"@context":"https://schema.org","@graph":graph})}</script>{ref("/seo-events.js",True)}</head><body class="visit-page localized-page"><a class="skip" href="#content">{e(c["skip"])}</a>{header}<main id="content">{body}</main>{page_footer}</body></html>'
        file = file_for(route)
        file.parent.mkdir(parents=True,exist_ok=True)
        file.write_text(page)
        new_routes.append(route)

# Head alternates only join equivalent, fully localized pages.
for group in GROUPS:
    tags = ''.join(f'<link rel="alternate" hreflang="{lang}" href="{ORIGIN+path}">' for lang,path in group.items()) + f'<link rel="alternate" hreflang="x-default" href="{ORIGIN+group["en"]}">'
    for path in group.values():
        file = file_for(path)
        text = re.sub(r'<link\b[^>]*hreflang="[^"]+"[^>]*>', '', file.read_text())
        file.write_text(text.replace('</head>',tags+'</head>'))

# Human language links exist on every page, including the otherwise isolated
# reservation languages. When a translation is absent, link to its real home.
for file in ROOT.rglob('index.html'):
    if '.git' in file.parts:
        continue
    text = file.read_text()
    s = BeautifulSoup(text,'html.parser')
    if s.html is None or s.select_one('main') is None or s.footer is None:
        continue
    lang = s.html.get('lang','tr')
    canonical = s.select_one('link[rel=canonical]')
    path = urlsplit(canonical['href']).path
    group = next((g for g in GROUPS if path in g.values()), GROUPS[0])
    nav = '<!-- LANGUAGES:START --><nav class="site-languages" aria-label="' + e(COPY.get(lang,{}).get('languages', 'Diller' if lang == 'tr' else 'Languages')) + '">'
    for code,label in LABELS.items():
        nav += f'<a href="{group[code]}" lang="{code}" hreflang="{code}" dir="auto"' + (' aria-current="page"' if group[code] == path else '') + f'>{label}</a>'
    nav += '</nav><!-- LANGUAGES:END -->'
    text = re.sub(r'<!-- LANGUAGES:START -->.*?<!-- LANGUAGES:END -->','',text,flags=re.S)
    text = text.replace('</footer>',nav+'</footer>')
    if not s.select_one('link[href^="/international.css"]'):
        text = text.replace('</head>',ref('/international.css')+'</head>')
    # Price offers match the visible values, including the shared portion basis.
    if path in GROUPS[1].values():
        soup = BeautifulSoup(text, 'html.parser')
        tag = soup.select_one('script[type="application/ld+json"]')
        data = json.loads(tag.string)
        node = next(n for n in data['@graph'] if n['@type'] == 'Menu')
        for ms in node['hasMenuSection']:
            for item in ms['hasMenuItem']:
                row = soup.find(id=item['@id'].split('#')[-1])
                offers = []
                portions = row.select('.portion-list li') or row.select('.portion-prices > span')
                if portions:
                    for portion in portions:
                        price = portion.select_one('strong') or portion.select_one('b')
                        name = portion.get_text(' ',strip=True).replace(price.get_text(), '').strip()
                        offers.append({'@type':'Offer','name':name,'price':re.sub(r'[^0-9]','',price.get_text()),'priceCurrency':'TRY','url':item['url']})
                else:
                    price = row.select_one('.menu-row-price') or row.select_one('.price')
                    assert price, f'Price missing for {item["@id"]}'
                    offers.append({'@type':'Offer','price':re.sub(r'[^0-9]','',price.get_text()),'priceCurrency':'TRY','url':item['url']})
                item['offers'] = offers
        text = text.replace(str(tag), f'<script type="application/ld+json">{dump(data)}</script>') if str(tag) in text else re.sub(r'<script type="application/ld\+json">.*?</script>',lambda _:f'<script type="application/ld+json">{dump(data)}</script>',text,count=1,flags=re.S)
    # A single, discoverable set of menus attached to the same restaurant entity.
    def normalize_schema(match):
        data = json.loads(match.group(1))
        for node in data.get('@graph',[]):
            if node.get('@type') == 'Restaurant':
                node['hasMenu'] = [{'@type':'Menu','@id':ORIGIN+p+'#menu','url':ORIGIN+p,'inLanguage':code} for code,p in GROUPS[1].items()]
        return '<script type="application/ld+json">' + dump(data) + '</script>'
    text = re.sub(r'<script type="application/ld\+json">(.*?)</script>', normalize_schema, text, flags=re.S)
    # Refresh only references to assets we changed, preserving all other markup.
    for asset_path in ['/international.css','/seo-events.js']:
        pattern = r'<(?:link|script)\b[^>]*(?:href|src)="' + re.escape(asset_path) + r'(?:\?[^\"]*)?"[^>]*>(?:</script>)?'
        text = re.sub(pattern, lambda _, p=asset_path:ref(p,p.endswith('.js')),text)
    file.write_text(text)

for prefix,uri in [('',S),('xhtml',X),('image',I)]:
    ET.register_namespace(prefix,uri)
tree = ET.parse(ROOT/'sitemap.xml')
root = tree.getroot()
entries = {u.find('{'+S+'}loc').text:u for u in root}
for file in ROOT.rglob('index.html'):
    if '.git' in file.parts:
        continue
    soup = BeautifulSoup(file.read_text(),'html.parser')
    canonical = soup.select_one('link[rel=canonical]')
    if not canonical:
        continue
    url = canonical['href']
    entry = entries.get(url)
    if entry is None:
        entry = ET.SubElement(root,'{'+S+'}url')
        ET.SubElement(entry,'{'+S+'}loc').text = url
    lastmod = entry.find('{'+S+'}lastmod')
    if lastmod is None:
        lastmod = ET.SubElement(entry,'{'+S+'}lastmod')
    if before.get(file) != file.read_bytes() or not lastmod.text:
        lastmod.text = DATE
    for link in list(entry):
        if link.tag == '{'+X+'}link':
            entry.remove(link)
    for link in soup.select('link[hreflang]'):
        ET.SubElement(entry,'{'+X+'}link',{'rel':'alternate','hreflang':link['hreflang'],'href':link['href']})
    if urlsplit(url).path in [f'/{lang}/' for lang in COPY] and entry.find('{'+I+'}image') is None:
        image = ET.SubElement(entry,'{'+I+'}image')
        ET.SubElement(image,'{'+I+'}loc').text = ORIGIN+'/assets/gallery/pusula-sofrasi-1200.webp'
ET.indent(tree,space='  ')
tree.write(ROOT/'sitemap.xml',encoding='unicode',xml_declaration=True)

config = json.loads((ROOT/'vercel.json').read_text())
sources = {r['source'] for r in config['redirects']}
for path in new_routes:
    if path+'index.html' not in sources:
        config['redirects'].insert(0,{'source':path+'index.html','destination':path,'permanent':True})
# Reports and build tools are not visitor landing pages. Leave public ownership
# verification files crawlable; do not block crawlers from seeing noindex.
for path in ['/seo/:path*','/scripts/:path*']:
    if not any(group['source'] == path for group in config['headers']):
        config['headers'].append({'source':path,'headers':[{'key':'X-Robots-Tag','value':'noindex'}]})
hashes = set()
for file in ROOT.rglob('*.html'):
    if '.git' in file.parts:
        continue
    for script in BeautifulSoup(file.read_text(),'html.parser').select('script[src][integrity]'):
        hashes.update(script['integrity'].split())
for group in config['headers']:
    for header in group['headers']:
        if header['key'] == 'Content-Security-Policy':
            header['value'] = re.sub(r'script-src [^;]+;', 'script-src '+' '.join("'"+h+"'" for h in sorted(hashes))+';', header['value'])
(ROOT/'vercel.json').write_text(json.dumps(config,ensure_ascii=False,indent=2)+'\n')
print('Built six RU/AR pages; synchronized four-language menus, prices, hreflang, discovery and sitemap.')
