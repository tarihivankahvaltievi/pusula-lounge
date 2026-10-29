"""Static SEO, localization, asset integrity and CSP checks; no third-party requests."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib,base64,json,re,sys,xml.etree.ElementTree as ET
from urllib.parse import urlsplit
root=Path(sys.argv[1]); base='https://www.pusulalounge.com'
routes={'tr':'/rezervasyon/','en':'/en/reservation/','ru':'/ru/reservation/','ko':'/ko/reservation/','ar':'/ar/reservation/','zh':'/zh/reservation/'}
class Page(HTMLParser):
 def __init__(self,text):
  super().__init__();self.tags=[];self.h1=[];self.in_h1=False;self.feed(text)
 def handle_starttag(self,tag,attrs):
  self.tags.append((tag,dict(attrs)))
  if tag=='h1':self.in_h1=True
 def handle_endtag(self,tag):
  if tag=='h1':self.in_h1=False
 def handle_data(self,data):
  if self.in_h1:self.h1.append(data)
 def all(self,tag):return [a for t,a in self.tags if t==tag]
config=json.loads((root/'vercel.json').read_text());csp=next(h['value'] for group in config['headers'] for h in group['headers'] if h['key']=='Content-Security-Policy')
sitemap=ET.fromstring((root/'sitemap.xml').read_text());ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9','x':'http://www.w3.org/1999/xhtml'}
for lang,route in routes.items():
 p=root/route.lstrip('/')/'index.html';text=p.read_text();page=Page(text)
 assert page.all('html')[0]['lang']==lang
 assert page.all('html')[0].get('dir')==('rtl' if lang=='ar' else None)
 assert len(page.all('h1'))==1
 canonical=[a for a in page.all('link') if a.get('rel')=='canonical'];assert len(canonical)==1 and canonical[0]['href']==base+route
 links={a['hreflang']:a['href'] for a in page.all('link') if a.get('rel')=='alternate'}
 assert links=={**{l:base+r for l,r in routes.items()},'x-default':base+'/en/reservation/'}
 metas={a.get('property',a.get('name')):a.get('content') for a in page.all('meta')}
 for key in ['description','og:title','og:description','og:locale','og:url','og:image','og:image:alt','twitter:title','twitter:description','twitter:image:alt']:assert metas.get(key), (lang,key)
 ids=[a['id'] for _,a in page.tags if 'id' in a];assert len(ids)==len(set(ids))
 for tag,attrs in page.tags:
  for key in ['href','src']:
   value=attrs.get(key,'')
   if value.startswith('/') and not value.startswith('//'):
    parts=urlsplit(value);target=root/parts.path.lstrip('/')
    assert target.exists(),(lang,value)
    if parts.fragment:
     target_page=target/'index.html' if target.is_dir() else target
     assert any(a.get('id')==parts.fragment for _,a in Page(target_page.read_text()).tags),(lang,value,'fragment')
  if 'integrity' in attrs:
   url=attrs.get('src',attrs.get('href'));data=(root/url.split('?')[0].lstrip('/')).read_bytes()
   sri='sha256-'+base64.b64encode(hashlib.sha256(data).digest()).decode();assert attrs['integrity']==sri
   assert hashlib.sha256(data).hexdigest()[:12] in url
   if tag=='script':assert "'"+sri+"'" in csp
  if 'aria-describedby' in attrs:
   for id in attrs['aria-describedby'].split():assert id in ids
 for label in page.all('label'):assert label['for'] in ids
 schemas=re.findall(r'<script type="application/ld\+json">(.*?)</script>',text,re.S);assert len(schemas)==1
 graph=json.loads(schemas[0])['@graph']; restaurant=next(x for x in graph if x['@type']=='Restaurant');assert restaurant['telephone']=='+905078162994'
 assert restaurant['address']['addressLocality']=='Beyoğlu'
 assert restaurant['acceptsReservations']==base+route
 assert restaurant['contactPoint']['telephone']==restaurant['telephone']
 webpage=next(x for x in graph if x['@type']=='WebPage')
 assert webpage['mainEntity']['@id']==restaurant['@id']
 assert len(webpage['relatedLink'])==3
 assert len(webpage.get('workTranslation',[]))==5 if lang=='tr' else webpage['translationOfWork']['@id']==base+'/rezervasyon/#webpage'
 heading=''.join(page.h1)
 assert {'ru':'Таксиме','ar':'تقسيم','ko':'탁심','zh':'塔克西姆'}.get(lang,'Taksim') in heading
 assert {'tr':'rezervasyon','en':'table','ru':'столик','ko':'예약','ar':'طاولة','zh':'预约'}[lang] in heading
 faq=next(x for x in graph if x['@type']=='FAQPage');assert len(faq['mainEntity'])==len(page.all('details'))==(5 if lang in ['tr','en'] else 6)
 for question in faq['mainEntity']:
  from html import escape
  assert escape(question['name'],quote=True) in text and escape(question['acceptedAnswer']['text'],quote=True) in text
 entries=[u for u in sitemap.findall('s:url',ns) if u.find('s:loc',ns).text==base+route];assert len(entries)==1
 assert {l.attrib['hreflang']:l.attrib['href'] for l in entries[0].findall('x:link',ns)}==links
 assert 'window.open' not in (root/'rezervasyon/reservation.js').read_text()
 print('PASS',lang,'canonical, reciprocal hreflang/sitemap, metadata, schema/visible FAQ, labels, assets, SRI and CSP')
# Preserve the entire site’s hash-only script policy, including unrelated pages.
for p in root.rglob('*.html'):
 if p.name.startswith('__'):continue
 for attrs in Page(p.read_text()).all('script'):
  if 'src' not in attrs:continue
  source=attrs['src'].split('?')[0]
  target=root/source.lstrip('/') if source.startswith('/') else p.parent/source
  assert target.exists(),(p,source)
  sri='sha256-'+base64.b64encode(hashlib.sha256(target.read_bytes()).digest()).decode()
  assert attrs.get('integrity')==sri,(str(p),'SRI')
  assert "'"+sri+"'" in csp,(str(p),'CSP')
print('PASS site-wide external script integrity and CSP allowlist')

for rel in ['site-haritasi/index.html','en/site-map/index.html']:
 page=Page((root/rel).read_text())
 for route in routes.values():assert any(a.get('href')==route for a in page.all('a'))
for rel in ['menu/index.html','en/menu/index.html','kahvalti-rehberi/index.html','en/breakfast-guide/index.html']:
 assert 'RESERVATION-DISCOVERY:START' in (root/rel).read_text()
print('PASS contextual reservation links and six-language HTML site maps')

for p in root.rglob('*.html'):
 if p.name.startswith('__'):continue
 for payload in re.findall(r'<script type="application/ld\+json">(.*?)</script>',p.read_text(),re.S):
  for node in json.loads(payload).get('@graph',[]):
   if node.get('@type')=='Restaurant':
    assert node['acceptsReservations'] in [base+r for r in routes.values()]
    assert node['contactPoint']['telephone']==node['telephone']=='+905078162994'
   if node.get('@type')=='WebSite':assert node['inLanguage']==list(routes)
print('PASS site-wide business reservation identity and language consistency')
