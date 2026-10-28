"""Add researched arrival help and bring menu actions before long product lists.

Run after build_international_seo.py. Asset refs and CSP are refreshed atomically.
"""
from pathlib import Path
from html import escape
from urllib.parse import urlencode,urlsplit,urljoin
from bs4 import BeautifulSoup
import base64,hashlib,json,re,sys,xml.etree.ElementTree as ET

ROOT=Path(sys.argv[1]).resolve()
ORIGIN='https://www.pusulalounge.com'
DATE='2026-10-28'
ADDRESS='Katip Mustafa Çelebi Mahallesi, Küçük Parmak Kapı Sokak, Sinek Çıkmazı No:3, Beyoğlu / İstanbul'
COPY=json.loads((Path(__file__).parent/'arrival_copy.json').read_text())
LOCATION={'tr':'/konum/','en':'/en/location/','ru':'/ru/location/','ar':'/ar/location/'}
MENU={'tr':'/menu/','en':'/en/menu/','ru':'/ru/menu/','ar':'/ar/menu/'}
RESERVATION={'tr':'/rezervasyon/',**{lang:f'/{lang}/reservation/' for lang in ['en','ru','ar']}}
S='http://www.sitemaps.org/schemas/sitemap/0.9'
before={p:p.read_bytes() for p in ROOT.rglob('index.html') if '.git' not in p.parts}
directions='https://www.google.com/maps/dir/?'+urlencode({'api':1,'destination':'Pusula Lounge, '+ADDRESS,'travelmode':'walking'})

def e(value):return escape(str(value),quote=True)
def file_for(route):return ROOT/route.lstrip('/')/'index.html'
def link(url,text,cls=''):return f'<a href="{e(url)}"'+(f' class="{cls}"' if cls else '')+f'>{e(text)}</a>'
def ref(path,script=False):
    digest=hashlib.sha256((ROOT/path.lstrip('/')).read_bytes())
    url=path+'?v='+digest.hexdigest()[:12]
    sri='sha256-'+base64.b64encode(digest.digest()).decode()
    return f'<script src="{url}" integrity="{sri}" crossorigin="anonymous" defer></script>' if script else f'<link rel="stylesheet" href="{url}" integrity="{sri}" crossorigin="anonymous">'

for lang,c in COPY.items():
    file=file_for(LOCATION[lang])
    text=re.sub(r'<!-- ARRIVAL:START -->.*?<!-- ARRIVAL:END -->','',file.read_text(),flags=re.S)
    body=f'<!-- ARRIVAL:START --><section class="arrival-guide" id="arrival-guide" aria-labelledby="arrival-title" data-copied="{e(c["copied"])}" data-copy-fallback="{e(c["fallback"])}"><h2 id="arrival-title">{e(c["heading"])}</h2><p>{e(c["intro"])}</p><dl class="arrival-routes">'
    for title,description in c['routes']:
        body+='<div><dt>'+e(title)+'</dt><dd>'+e(description)+'</dd></div>'
    body+='</dl><div class="visit-card"><h3>Pusula Lounge</h3><address data-visit-address lang="tr" dir="ltr">'+e(ADDRESS)+'</address><p><bdi dir="ltr">+90 507 816 29 94</bdi></p><p>'+e(c['hours'])+'</p><div class="visit-tool-actions">'+link(directions,c['directions'],'visit-button')+link('tel:+905078162994',c['call'])+f'<button type="button" data-copy-address hidden>{e(c["copy"])}</button><button type="button" data-print-visit hidden>{e(c["print"])}</button></div><p role="status" aria-live="polite"></p></div><p>{e(c["note"])}</p>'
    body+='<div class="transport-sources"><h3>'+e(c['sources'])+'</h3><ul>'
    for line in ['M2','T1','F1']:
        body+='<li>'+link('https://metro.istanbul/Hatlarimiz/HatDetay?hat='+line,'Metro İstanbul · '+line)+'</li>'
    body+='<li>'+link('https://metro.istanbul/', 'Metro İstanbul')+'</li></ul><p>'+e(c['sourcesNote'])+'</p></div>'
    body+='<div class="visit-actions arrival-booking">'+link(RESERVATION[lang],c['reservation'],'visit-button')+link(MENU[lang],c['menu'])+'</div></section><!-- ARRIVAL:END -->'
    if lang=='ar':
        body=body.replace('08:00–17:00','<bdi dir="ltr">08:00–17:00</bdi>')
        for sequence in ['M2 → Taksim','T1 → Kabataş → F1 → Taksim']:
            body=body.replace(sequence,'<bdi dir="ltr">'+sequence+'</bdi>')
    text=text.replace('</main>',body+'</main>')
    for path,is_script in [('/visit-tools.css',False),('/visit-tools.js',True)]:
        pattern=r'<(?:link|script)\b[^>]*(?:href|src)="'+re.escape(path)+r'(?:\?[^\"]*)?"[^>]*>(?:</script>)?'
        text=re.sub(pattern,'',text)
        text=text.replace('</head>',ref(path,is_script)+'</head>')
    file.write_text(text)

# A request/directions link at the top of the visitor menus avoids requiring a
# tourist to read nineteen dishes before discovering how to visit.
for lang in ['en','ru','ar']:
    file=file_for(MENU[lang]);text=re.sub(r'<!-- MENU-ACTIONS:START -->.*?<!-- MENU-ACTIONS:END -->','',file.read_text(),flags=re.S)
    action='<!-- MENU-ACTIONS:START --><div class="menu-intro-actions">'+link(RESERVATION[lang],COPY[lang]['reservation'],'visit-button')+link(LOCATION[lang]+'#arrival-guide',COPY[lang]['directions'])+'</div><!-- MENU-ACTIONS:END -->'
    # The published menu's introduction is a header in EN and a div in RU/AR.
    match=re.search(r'<(?:header|div) class="visit-intro">.*?</(?:header|div)>',text,re.S)
    assert match,lang+' menu introduction missing'
    text=text[:match.end()]+action+text[match.end():]
    text=re.sub(r'<link\b[^>]*href="/visit-tools.css(?:\?[^\"]*)?"[^>]*>','',text)
    file.write_text(text.replace('</head>',ref('/visit-tools.css')+'</head>'))

# No separate promise of unlimited tea exists for the individual plate's text.
# Remove its decorative unlimited-tea badge instead of keeping a second claim.
file=ROOT/'menu/index.html'
text=file.read_text()
text=re.sub(r'<div\b(?=[^>]*class="tea-badge")[^>]*></div>','',text)
file.write_text(text)

# Make the new cultural visit article discoverable from relevant visitor pages.
article=json.loads((Path(__file__).parent/'culture_article.json').read_text())
for lang in ['tr','en']:
    index=int(lang=='en')
    route='/en/blog/'+article['en']+'/' if index else '/blog/'+article['slug']+'/'
    title='Breakfast and a cultural stop in Beyoğlu' if index else 'Kahvaltıdan sonra Beyoğlu’nu keşfedin'
    for path in [LOCATION[lang],'/en/site-map/' if index else '/site-haritasi/']:
        file=file_for(path)
        text=re.sub(r'<!-- CULTURE:START -->.*?<!-- CULTURE:END -->','',file.read_text(),flags=re.S)
        section='<!-- CULTURE:START --><section class="visit-section"><h2>'+title+'</h2><p>'+link(route,article['title'][index])+'</p></section><!-- CULTURE:END -->'
        file.write_text(text.replace('</main>',section+'</main>'))

# Re-version every local stylesheet/script after font or visitor-code changes.
hashes=set()
for file in ROOT.rglob('*.html'):
    if '.git' in file.parts:continue
    text=file.read_text()
    soup=BeautifulSoup(text,'html.parser')
    if soup.select_one('main') is None:continue
    route='/'+file.relative_to(ROOT).as_posix().removesuffix('index.html')
    def update(match):
        tag=BeautifulSoup(match.group(0),'html.parser').find()
        value=tag.get('src',tag.get('href',''))
        absolute=urljoin(ORIGIN+route,value)
        parts=urlsplit(absolute)
        if parts.netloc!=urlsplit(ORIGIN).netloc:return match.group(0)
        target=ROOT/parts.path.lstrip('/')
        if not target.exists():return match.group(0)
        return ref(parts.path,tag.name=='script')
    text=re.sub(r'<link\b[^>]*rel="stylesheet"[^>]*>|<script\b[^>]*src="[^"]+"[^>]*></script>',update,text)
    # Also handle existing link attribute order from the older static pages.
    text=re.sub(r'<link\b(?=[^>]*rel="stylesheet")(?=[^>]*href=")[^>]*>',update,text)
    file.write_text(text)
    for tag in BeautifulSoup(text,'html.parser').select('script[src][integrity]'):hashes.update(tag['integrity'].split())
config=json.loads((ROOT/'vercel.json').read_text())
for group in config['headers']:
    for header in group['headers']:
        if header['key']=='Content-Security-Policy':
            header['value']=re.sub(r'script-src [^;]+;','script-src '+' '.join("'"+h+"'" for h in sorted(hashes))+';',header['value'])
(ROOT/'vercel.json').write_text(json.dumps(config,ensure_ascii=False,indent=2)+'\n')
for prefix,uri in [('',S),('xhtml','http://www.w3.org/1999/xhtml'),('image','http://www.google.com/schemas/sitemap-image/1.1')]:ET.register_namespace(prefix,uri)
tree=ET.parse(ROOT/'sitemap.xml')
for item in tree.getroot():
    route=urlsplit(item.find('{'+S+'}loc').text).path
    file=file_for(route)
    if before.get(file)!=file.read_bytes():item.find('{'+S+'}lastmod').text=DATE
ET.indent(tree,space='  ')
tree.write(ROOT/'sitemap.xml',encoding='unicode',xml_declaration=True)
print('Added four arrival guides, copy/print visit cards, early menu actions and current asset/CSP hashes.')
