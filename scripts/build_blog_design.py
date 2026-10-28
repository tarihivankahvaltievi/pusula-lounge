"""Apply Pusula's bilingual journal design after content generation.

Content, route pairs, sources and structured data stay with the SEO generator.
Run before build_visitor_quality.py, which seals asset hashes and CSP.
"""
from pathlib import Path
from html import escape as e
import base64, hashlib, json, re, shutil, sys
from bs4 import BeautifulSoup
from PIL import Image
R=Path(sys.argv[1]).resolve()
HERE=Path(__file__).parent
ORIGIN='https://www.pusulalounge.com'
SUBJECTS=[
 ('taksimde-kahvalti-plani','turkish-breakfast-taksim','breakfast','paylasilan-kahvalti',('İlk kahvaltı, güzel bir başlangıç.','Your first breakfast at Pusula.'),('Pusula’da paylaşılan bir kahvaltı sofrası.','A shared breakfast table at Pusula.')),
 ('serpme-kahvalti-porsiyon-fiyat-rehberi','shared-breakfast-portions-prices','breakfast','kahvalti-sofrasi',('Sofrayı birlikte seçelim.','Find the right spread for your table.'),('Kareli örtü üzerinde serpme kahvaltı; porsiyonları menüden karşılaştırın.','A shared breakfast spread; compare portions in the menu.')),
 ('istiklal-kahvalti-ulasim-gezi','istiklal-breakfast-walk-directions','city','tram',('Bir sabah, İstiklal’de.','A morning on İstiklal.'),('İstiklal Caddesi’nin nostaljik tramvayı.','The nostalgic tram on İstiklal Avenue.')),
 ('van-kahvaltisi-nedir-pusula-sofrasi','what-is-van-breakfast','breakfast','kahvalti-detay',('Van’dan gelen sofra kültürü.','A breakfast tradition from Van.'),('Pusula kahvaltısından peynirler, sıcaklar ve sofradaki diğer lezzetler.','Cheese, hot dishes and other flavours from a Pusula breakfast.')),
 ('taksimde-aksam-yemegi-waffle-kahve','dinner-waffle-coffee-taksim','evening','birlikte-mola',('Akşama da yer var.','Stay a little longer.'),('Pusula’da masada paylaşılan bir içecek molası.','Sharing a drink around a table at Pusula.')),
 ('kahvaltidan-sonra-beyoglu-sanat-muze','beyoglu-breakfast-museums','city','yesil-kose',('Sofradan sonra, Beyoğlu.','After breakfast, Beyoğlu awaits.'),('Beyoğlu gezisine başlamadan önce Pusula’nın yeşil köşesi.','Pusula’s green corner before exploring Beyoğlu.')),
]
CATEGORIES={'breakfast':('Sofra & kahvaltı','Breakfast & the table'),'city':('Beyoğlu & şehir','Beyoğlu & the city'),'evening':('Akşam & mola','Evenings & coffee')}
def fragment(text):return BeautifulSoup(text,'html.parser')
def asset(path,script=False):
 digest=hashlib.sha256((R/path.lstrip('/')).read_bytes()).digest();version=digest.hex()[:12];sri='sha256-'+base64.b64encode(digest).decode()
 return f'<script src="{path}?v={version}" integrity="{sri}" crossorigin="anonymous" defer></script>' if script else f'<link rel="stylesheet" href="{path}?v={version}" integrity="{sri}" crossorigin="anonymous">'
def route(s,en):return ('/en/blog/'+s[1] if en else '/blog/'+s[0])+'/'
def photo(s):return '/assets/istiklal-tram-calm-screen-1280.webp' if s[3]=='tram' else '/assets/gallery/'+s[3]+'-1200.webp'
def image(s,i,lazy=True):
 path=photo(s);w,h=Image.open(R/path.lstrip('/')).size
 smaller='/assets/istiklal-tram-calm-screen-480.webp' if s[3]=='tram' else '/assets/gallery/'+s[3]+'-600.webp'
 sw=Image.open(R/smaller.lstrip('/')).width
 return f'<img src="{path}" srcset="{smaller} {sw}w, {path} {w}w" sizes="(max-width:700px) calc(100vw - 40px), (max-width:1320px) 48vw, 600px" width="{w}" height="{h}" alt="{e(s[5][i])}" decoding="async" '+('loading="lazy"' if lazy else 'fetchpriority="high"')+'>'
def nav(en):
 prefix='/en/' if en else '/';r='/en/reservation/' if en else '/rezervasyon/';loc='/en/location/' if en else '/konum/'
 return f'<a href="{prefix}">'+('Home' if en else 'Ana sayfa')+f'</a><a href="{prefix}menu/">'+('Menu' if en else 'Menü')+f'</a><a href="{loc}">'+('Find us' if en else 'Konum')+f'</a><a href="{prefix}blog/" aria-current="page">'+('Journal' if en else 'Günlük')+f'</a><a class="journal-book" href="{r}">'+('Request a table' if en else 'Rezervasyon')+'</a>'
def header(en,pair):
 n=nav(en)+f'<a href="{pair}" lang="'+('tr' if en else 'en')+'">'+('Türkçe' if en else 'English')+'</a>'
 return '<header class="journal-header"><a class="journal-brand" href="'+('/en/' if en else '/')+'" aria-label="Pusula Lounge '+('home' if en else 'ana sayfa')+'"><img src="/assets/pusula-lounges-logo-fast-320.webp" width="78" height="78" alt=""><span><strong>Pusula Lounge</strong>Beyoğlu · İstanbul</span></a><nav class="journal-nav" aria-label="'+('Main navigation' if en else 'Ana menü')+'">'+n+'</nav><details class="journal-mobile"><summary>'+('Menu' if en else 'Menü')+'</summary><nav aria-label="'+('Mobile navigation' if en else 'Mobil menü')+'">'+n+'</nav></details></header>'
# Copy source assets rather than editing generated output only.
for filename in ['blog.css','blog.js']:shutil.copyfile(HERE/'editorial'/filename,R/filename)

for en in [False,True]:
 i=int(en);prefix='/en/' if en else '/';index=prefix+'blog/';reservation='/en/reservation/' if en else '/rezervasyon/'
 docs={s[0]:BeautifulSoup((R/route(s,en).lstrip('/')/'index.html').read_text(),'html.parser') for s in SUBJECTS}
 def entry(s,lead=False,related=False):
  doc=docs[s[0]];title=doc.h1.get_text();desc=doc.find('meta',attrs={'name':'description'})['content'];href=route(s,en)
  return '<'+('div' if related else 'li')+' class="journal-entry'+(' journal-entry--lead' if lead else '')+'" data-category="'+s[2]+'"><a class="entry-image" tabindex="-1" aria-hidden="true" href="'+href+'">'+image(s,i,not lead)+'</a><div class="entry-copy"><p class="entry-category">'+CATEGORIES[s[2]][i]+'</p><'+('h3' if related else 'h2')+'><a href="'+href+'">'+e(title)+'</a></'+('h3' if related else 'h2')+'>'+('' if related else '<p class="entry-description">'+e(desc)+'</p><a class="entry-read" href="'+href+'">'+('Read the story' if en else 'Yazıyı okuyun')+'</a>')+'</div></'+('div' if related else 'li')+'>'
 for s in SUBJECTS:
  doc=docs[s[0]];a=doc.article
  old_header=a.select_one('.visit-intro');old_header['class']=['article-heading']
  old_header.insert(0,fragment('<p class="journal-kicker">'+CATEGORIES[s[2]][i]+'</p>'))
  old_meta=a.select_one('.article-meta');old_actions=a.select_one('.article-actions');old_photo=a.select_one('.article-photo');toc=a.select_one('.article-toc')
  words=len(a.get_text(' ',strip=True).split());minutes=max(3,round(words/190))
  old_meta.append(' · '+str(minutes)+(' min read' if en else ' dk okuma'))
  old_header.append(old_meta.extract());old_header.append(old_actions.extract())
  # Rebuild the photo with real dimensions and a matching responsive pair.
  w,h=Image.open(R/photo(s).lstrip('/')).size
  cover=fragment('<figure class="article-cover'+(' article-cover--portrait' if h>w else '')+'">'+image(s,i,False)+'<figcaption>'+e(s[5][i])+'</figcaption></figure>').figure
  old_photo.decompose();old_header.extract()
  contents='<details open><summary>'+('In this story' if en else 'Bu yazıda')+'</summary>'+str(toc.ul)+'</details>'
  toc.decompose()
  sections=list(a.select(':scope > .visit-section'))
  related=None
  for section in sections:
   heading=section.h2.get_text() if section.h2 else ''
   if heading in ['Diğer yazılar','Keep reading']:
    section.decompose();continue
   if section.select_one('.article-actions'):section['class']=['visit-section','journal-booking']
  # Existing table and its explanatory note remain before the prose.
  body=doc.new_tag('div',attrs={'class':'article-body'})
  for child in list(a.contents):body.append(child.extract())
  aside='<aside class="article-sidebar" aria-label="'+('Story navigation' if en else 'Yazı navigasyonu')+'">'+contents+'<div class="sidebar-visit"><p><strong>Pusula Lounge</strong><br>Beyoğlu · İstanbul</p><p>'+('Breakfast · 08:00–17:00' if en else 'Kahvaltı · 08:00–17:00')+'</p><a href="'+('/en/location/' if en else '/konum/')+'">'+('Plan your visit' if en else 'Ziyaretinizi planlayın')+'</a></div></aside>'
  opening=doc.new_tag('div',attrs={'class':'article-opening'});opening.append(old_header);opening.append(cover);a.append(opening)
  layout=doc.new_tag('div',attrs={'class':'article-layout'});layout.append(fragment(aside));layout.append(body);a.append(layout);a['class']=['journal-article']
  others=[x for x in SUBJECTS if x!=s];others.sort(key=lambda x:x[2]!=s[2])
  related='<section class="journal-related" aria-labelledby="related-title"><div class="related-heading"><h2 id="related-title">'+('A little more to explore' if en else 'Biraz daha keşfedin')+'</h2><a href="'+index+'">'+('All stories' if en else 'Tüm yazılar')+'</a></div><div class="related-grid">'+''.join(entry(x,related=True) for x in others[:3])+'</div></section>'
  doc.main.append(fragment(related));doc.body.insert(0,fragment('<div class="reading-progress" aria-hidden="true"></div>'))
  # Make cover, social metadata, BlogPosting and sitemap agree.
  for m in doc.select('meta[property="og:image"],meta[name="twitter:image"]'):m['content']=ORIGIN+photo(s)
  for m in doc.select('meta[property="og:image:width"]'):m['content']=str(w)
  for m in doc.select('meta[property="og:image:height"]'):m['content']=str(h)
  for m in doc.select('meta[property="og:image:alt"],meta[name="twitter:image:alt"]'):m['content']=s[5][i]
  for script in doc.select('script[type="application/ld+json"]'):
   graph=json.loads(script.string)
   for node in graph.get('@graph',[]):
    if node.get('@type')=='BlogPosting':node['image']=ORIGIN+photo(s)
   script.string=json.dumps(graph,ensure_ascii=False)
  docs[s[0]]=doc
 # Index uses the same source titles, summaries and routes.
 indexfile=R/index.lstrip('/')/'index.html';doc=BeautifulSoup(indexfile.read_text(),'html.parser')
 masthead='<header class="journal-masthead"><div class="masthead-copy"><p class="journal-kicker">'+('Food, people & Beyoğlu' if en else 'Sofra, sohbet, Beyoğlu')+'</p><h1>'+('Stories from<br><span>Pusula.</span>' if en else 'Pusula’dan<br><span>hikâyeler.</span>')+'</h1><p class="journal-description">'+('A table to share. A coffee that turns into a conversation. A few notes from our colourful corner of Beyoğlu.' if en else 'Birlikte kurulan sofralar, kahveyle uzayan sohbetler. Beyoğlu’ndaki rengârenk köşemizden notlar.')+'</p><a class="masthead-link" href="#stories">'+('Pull up a chair. Explore the stories.' if en else 'Bir sandalye çekin. Hikâyelere göz atın.')+'</a></div><figure class="masthead-photo"><img src="/assets/hero-mekan-screen-1066.webp" srcset="/assets/hero-mekan-screen-480.webp 480w, /assets/hero-mekan-screen-1066.webp 1066w" sizes="(max-width:700px) 100vw, 60vw" width="1066" height="1600" alt="'+('Yellow chairs and a flower-filled ceiling at Pusula Lounge' if en else 'Pusula Lounge’un çiçekli tavanı, yeşil duvarları ve sarı sandalyeleri')+'" fetchpriority="high"></figure></header><div class="journal-floral" aria-hidden="true"></div>'

 filters='<div class="journal-filters" role="group" aria-label="'+('Filter stories' if en else 'Yazıları konuya göre süz')+'" hidden>'+''.join('<button type="button" data-journal-filter="'+key+'" aria-pressed="'+str(key=='all').lower()+'">'+label+'</button>' for key,label in [('all','All stories' if en else 'Tüm yazılar'),('breakfast','Breakfast' if en else 'Sofra'),('city','Beyoğlu'),('evening','Evenings' if en else 'Akşam & mola')])+'<span class="filter-caption" data-filter-count role="status" aria-live="polite">6 '+('stories' if en else 'yazı')+'</span></div>'
 endnote='<section class="journal-endnote"><h2>'+('Let’s meet around a table.' if en else 'Bir sonraki hikâye, sizin sofranızda.')+'</h2><div class="article-actions"><a href="'+prefix+'menu/">'+('Explore the menu' if en else 'Menüyü inceleyin')+'</a><a class="visit-button" href="'+reservation+'">'+('Request a table' if en else 'Masa talebi gönder')+'</a></div></section>'
 doc.select_one('.blog-index').replace_with(fragment('<div class="blog-index">'+masthead+'<section class="journal-archive" id="stories" aria-label="'+('All stories' if en else 'Tüm yazılar')+'">'+filters+'<ol class="blog-entries">'+''.join(entry(s,lead=k==0) for k,s in enumerate(SUBJECTS))+'</ol></section>'+endnote+'</div>'))
 docs['index']=doc
 for key,doc in docs.items():
  s=next((x for x in SUBJECTS if x[0]==key),None);pair=route(s,not en) if s else ('/blog/' if en else '/en/blog/')
  doc.select_one('.visit-header').replace_with(fragment(header(en,pair)))
  # Redundant language link moves into the shared header; retain breadcrumb.
  for p in list(doc.main.find_all('p',recursive=False)):
   if p.a and p.a.get('href')==pair:p.decompose()
  for link in list(doc.head.select('link[rel="stylesheet"]')):
   if link.get('href','').split('?')[0] in ['/blog.css','/assets/fonts/site-fonts.css']:link.decompose()
  doc.head.append(fragment(asset('/blog.css')))
  for script in list(doc.select('script[src]')):
   if script['src'].split('?')[0]=='/blog.js':script.decompose()
  doc.head.append(fragment(asset('/blog.js',True)))
  target=R/(route(s,en) if s else index).lstrip('/')/'index.html';target.write_text(str(doc))
# Update image sitemap entries for each article in both languages.
import xml.etree.ElementTree as ET
S='http://www.sitemaps.org/schemas/sitemap/0.9';I='http://www.google.com/schemas/sitemap-image/1.1'
for prefix,uri in [('',S),('xhtml','http://www.w3.org/1999/xhtml'),('image',I)]:ET.register_namespace(prefix,uri)
tree=ET.parse(R/'sitemap.xml')
for url in tree.getroot():
 loc=url.find('{'+S+'}loc').text
 for en in [False,True]:
  for s in SUBJECTS:
   if loc==ORIGIN+route(s,en):
    im=url.find('{'+I+'}image')
    if im is not None:
     im.find('{'+I+'}loc').text=ORIGIN+photo(s)
     caption=im.find('{'+I+'}caption')
     if caption is not None:caption.text=s[5][int(en)]
tree.write(R/'sitemap.xml',encoding='unicode',xml_declaration=True)
print('Designed 14 journal pages with six distinct subject covers.')

# Seal this new script into the existing hash-only policy without widening sources.
config=json.loads((R/'vercel.json').read_text())
script_hash="'sha256-"+base64.b64encode(hashlib.sha256((R/'blog.js').read_bytes()).digest()).decode()+"'"
for group in config['headers']:
 for header in group['headers']:
  if header['key']=='Content-Security-Policy' and script_hash not in header['value']:
   header['value']=header['value'].replace('script-src ','script-src '+script_hash+' ',1)
(R/'vercel.json').write_text(json.dumps(config,ensure_ascii=False,indent=2)+'\n')
