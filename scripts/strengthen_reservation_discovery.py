# -*- coding: utf-8 -*-
"""Keep reservation entry points and shared business entities consistent. Run after build_reservations.py."""
from pathlib import Path
import re,json,sys,html,xml.etree.ElementTree as ET
root=Path(sys.argv[1]);base='https://www.pusulalounge.com'
languages={'tr':('Türkçe','/rezervasyon/'),'en':('English','/en/reservation/'),'ru':('Русский','/ru/reservation/'),'ko':('한국어','/ko/reservation/'),'ar':('العربية','/ar/reservation/'),'zh':('中文','/zh/reservation/')}
changed=set()
def save(p,text):
 if text!=p.read_text():p.write_text(text);changed.add('/'+str(p.relative_to(root).parent).replace('\\','/').strip('./')+'/' if p.relative_to(root).parent!=Path('.') else '/')
for rel in ['menu/index.html','en/menu/index.html','kahvalti-rehberi/index.html','en/breakfast-guide/index.html']:
 p=root/rel;text=p.read_text();en=rel.startswith('en/')
 title='Planning breakfast in Taksim?' if en else 'Taksim’de kahvaltınızı planlayın'
 lead='Choose a date, time and guest count, then send your table request to Pusula Lounge on WhatsApp. Our team will confirm availability.' if en else 'Tarih, saat ve kişi sayısını seçin; Pusula Lounge için masa talebinizi WhatsApp’ta paylaşın. Ekibimiz masa uygunluğunu teyit etsin.'
 label='Request a breakfast table in Taksim' if en else 'Taksim kahvaltı rezervasyonu için talep gönderin'
 route=languages['en' if en else 'tr'][1]
 # Reuse each page's established layout and type styles.
 klass='visit-section' if en or 'rehberi' in rel else 'menu-reading-guide'
 block=f'<!-- RESERVATION-DISCOVERY:START --><section class="{klass}" aria-labelledby="reserve-visit-title"><h2 id="reserve-visit-title">{title}</h2><p>{lead}</p><p><a href="{route}">{label}</a></p></section><!-- RESERVATION-DISCOVERY:END -->'
 text=re.sub(r'<!-- RESERVATION-DISCOVERY:START -->.*?<!-- RESERVATION-DISCOVERY:END -->','',text,flags=re.S)
 marker='<!-- GEO:START -->' if rel=='menu/index.html' else '<!-- GUIDE:START -->' if rel=='en/menu/index.html' else '</main>'
 assert marker in text,rel
 text=text.replace(marker,block+marker,1);save(p,text)
for rel in ['site-haritasi/index.html','en/site-map/index.html']:
 p=root/rel;text=p.read_text();en=rel.startswith('en/')
 # Replace outdated request-copy wording with the actual WhatsApp flow.
 text=text.replace('Rezervasyon Talebi Hazırlayın','Taksim Kahvaltı Rezervasyonu').replace('Pusula Lounge için tarih, saat ve kişi sayısıyla talep metni hazırlayın. Kopyalama işletmeye göndermez; rezervasyon işletme teyidiyle kesinleşir.','Taksim’de kahvaltı için tarih, saat ve kişi sayısını seçin; Pusula Lounge’a WhatsApp üzerinden rezervasyon talebinizi iletin. Rezervasyon ekip onayıyla kesinleşir.')
 title='Reserve a table in your language' if en else 'Kendi dilinizde rezervasyon talebi'
 links=''.join(f'<li><a href="{route}" lang="{lang}" hreflang="{lang}" dir="auto">{name}</a></li>' for lang,(name,route) in languages.items())
 block=f'<!-- RESERVATION-LANGUAGES:START --><section class="visit-section" aria-labelledby="reservation-languages-title"><h2 id="reservation-languages-title">{title}</h2><ul>{links}</ul></section><!-- RESERVATION-LANGUAGES:END -->'
 text=re.sub(r'<!-- RESERVATION-LANGUAGES:START -->.*?<!-- RESERVATION-LANGUAGES:END -->','',text,flags=re.S).replace('</main>',block+'</main>',1);save(p,text)
# Give crawlers the same business identity and reservation URLs on all entry pages.
for p in root.rglob('*.html'):
 if p.name.startswith('__') or '.git' in p.parts:continue
 text=p.read_text();en='lang="en"' in text[:200];route=languages['en' if en else 'tr'][1]
 def update(match):
  payload=json.loads(match.group(1));modified=False
  for node in payload.get('@graph',[]):
   if node.get('@type')=='WebSite' and node.get('inLanguage')!=list(languages):node['inLanguage']=list(languages);modified=True
   if node.get('@type')=='Restaurant' and not node.get('acceptsReservations'):
    node['acceptsReservations']=base+route
    node['contactPoint']={'@type':'ContactPoint','contactType':'reservations','telephone':'+905078162994','url':base+route}
    modified=True
  return '<script type="application/ld+json">'+json.dumps(payload,ensure_ascii=False).replace('<','\\u003c')+'</script>' if modified else match.group(0)
 text=re.sub(r'<script type="application/ld\+json">(.*?)</script>',update,text,flags=re.S);save(p,text)
# All six actual reservation pages changed in this pass, even if links did not.
changed.update(route for _,route in languages.values())
path=root/'sitemap.xml';text=path.read_text()
for route in changed:
 text=re.sub(r'(<loc>'+re.escape(base+route)+r'</loc>\s*<lastmod>)[^<]+',r'\g<1>2026-10-27',text)
path.write_text(text)
print('Updated reservation entry points, six-language directories and shared business entities.')
