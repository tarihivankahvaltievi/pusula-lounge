"""Validate crawlability, page graph, links, schema and integrity of the static release."""
from pathlib import Path
from urllib.parse import urlsplit,urljoin,unquote
from urllib.robotparser import RobotFileParser
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import json,sys,hashlib,base64
from datetime import date
R=Path(sys.argv[1]);O='https://www.pusulalounge.com';ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9','x':'http://www.w3.org/1999/xhtml'}
tree=ET.parse(R/'sitemap.xml');entries=tree.findall('s:url',ns);urls=[u.find('s:loc',ns).text for u in entries];assert len(urls)==len(set(urls))
def target(url):
 path=R/unquote(urlsplit(url).path).lstrip('/')
 return path/'index.html' if path.is_dir() else path
pages={url:BeautifulSoup(target(url).read_text(),'html.parser') for url in urls}
robots=RobotFileParser();robots.parse((R/'robots.txt').read_text().splitlines())
v=json.loads((R/'vercel.json').read_text());csp=next(h['value'] for group in v['headers'] for h in group['headers'] if h['key']=='Content-Security-Policy')
errors=[];inbound={url:set() for url in urls};titles=set();descs=set();schemas=0
for entry,url in zip(entries,urls):
 s=pages[url];path=urlsplit(url).path
 def check(ok,msg):
  if not ok:errors.append(path+': '+msg)
 check(len(s.select('h1'))==1,'exactly one h1');check(len(s.select('link[rel=canonical]'))==1 and s.select_one('link[rel=canonical]')['href']==url,'canonical')
 title=s.title.get_text();check(title not in titles,'duplicate title');titles.add(title)
 desc=s.select_one('meta[name=description]')['content'];check(desc not in descs,'duplicate description');descs.add(desc)
 for bot in ['Googlebot','Bingbot','OAI-SearchBot']:check(robots.can_fetch(bot,url),'blocked '+bot)
 check('noindex' not in s.select_one('meta[name=robots]')['content'],'noindex')
 ids=[tag['id'] for tag in s.select('[id]')];check(len(ids)==len(set(ids)),'duplicate IDs')
 for alt in s.select('link[hreflang]'):
  href=alt['href'];check(href in pages,'alternate absent')
  if href in pages:
   other=pages[href];check(any(x.get('hreflang')==s.html['lang'] and x.get('href')==url for x in other.select('link[hreflang]')),'alternate not reciprocal')
 # Check all local asset/link destinations and fragments.
 for tag in s.select('[href],[src]'):
  value=tag.get('src',tag.get('href',''));absolute=urljoin(url,value);parts=urlsplit(absolute)
  if parts.netloc!=urlsplit(O).netloc or parts.scheme not in ['http','https']:continue
  file=target(absolute);check(file.exists(),'missing target '+value)
  if parts.fragment and file.exists() and file.suffix=='.html':
   check(BeautifulSoup(file.read_text(),'html.parser').find(id=unquote(parts.fragment)) is not None,'missing fragment '+value)
  normalized=O+parts.path
  if tag.name=='a' and normalized in inbound and normalized!=url:inbound[normalized].add(url)
  if tag.get('integrity'):
   sri='sha256-'+base64.b64encode(hashlib.sha256(file.read_bytes()).digest()).decode();check(sri==tag['integrity'],'SRI '+value)
   if tag.name=='script':check("'"+sri+"'" in csp,'CSP '+value)
 for script in s.select('script[type="application/ld+json"]'):
  g=json.loads(script.string)['@graph'];schemas+=len(g)
  for node in g:
   if node['@type']=='Restaurant':
    check(node.get('telephone')=='+905078162994','business phone mismatch');check('aggregateRating' not in node,'self-serving ratings')
   if node['@type']=='BlogPosting':
    check(node['headline']==s.h1.get_text(),'article headline mismatch');check(node['mainEntityOfPage']['@id']==url+'#webpage','article main page')
    published=node['datePublished'][:10]
    check(date.fromisoformat(published)<=date.today(),'future publication date')
    check(s.select_one('time[datetime="'+published+'"]') is not None,'visible publication date mismatch')
 if '/blog/' in path:
  check(s.html['lang'] in ['tr','en'],'blog language')
  check(len(s.select('link[hreflang]'))==3,'blog hreflang')
  smap={a.attrib['hreflang']:a.attrib['href'] for a in entry.findall('x:link',ns)}
  check(smap=={a['hreflang']:a['href'] for a in s.select('link[hreflang]')},'sitemap alternates mismatch')
  check(s.select_one('a[href="/en/reservation/"]' if s.html['lang']=='en' else 'a[href="/rezervasyon/"]'),'reservation CTA missing')
  check(s.select_one('nav.seo-breadcrumb [aria-current=page]'),'visible breadcrumb')
for url,sources in inbound.items():
 if url!=O+'/':
  if not sources:errors.append(url+': orphan page')
report={'pages':len(pages),'schemaNodes':schemas,'blogRoutes':sum('/blog/' in u for u in urls),'errors':errors,'blogIncomingLinks':{u:len(v) for u,v in inbound.items() if '/blog/' in u}}
print(json.dumps(report,ensure_ascii=False,indent=2))
if errors:sys.exit(1)
