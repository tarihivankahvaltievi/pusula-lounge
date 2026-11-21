"""Verify source-price propagation and prevent computed costs becoming offers."""
from pathlib import Path
from bs4 import BeautifulSoup
from decimal import Decimal
import json, re, shutil, subprocess, sys, tempfile
root=Path(sys.argv[1]).resolve()
paths=['menu/index.html','en/menu/index.html','ru/menu/index.html','ar/menu/index.html']
def verify(base, totals, solo):
 for path in paths:
  soup=BeautifulSoup((base/path).read_text(),'html.parser')
  assert len(soup.select('#shared-breakfast-budget'))==1,path
  rows=soup.select('#shared-breakfast-budget tbody tr')
  def number(cell):
   text=cell.get_text().replace(' TL','').strip()
   if path=='menu/index.html':text=text.replace('.','').replace(',','.')
   else:text=text.replace(',','')
   return Decimal(text)
  assert len(rows)==3,path
  intro = soup.select_one('.menu-visit p' if path == paths[0] else '.visit-intro .lead')
  assert number(intro.select_one('a[href="#serpme-van-kahvaltisi"]')) == totals[0], path
  assert number(intro.select_one('a[href="#kahvalti-tabagi"]')) == solo, path
  assert '08:00' in intro.get_text() and '17:00' in intro.get_text(), path
  for row,(people,total) in zip(rows,zip([2,3,4],totals)):
   cells=row.select('th,td')
   assert number(cells[0])==people and number(cells[1])==total,path
   assert number(cells[2])==(Decimal(total)/people).quantize(Decimal('.01')),path
  graph=json.loads(soup.select_one('script[type="application/ld+json"]').string)
  assert 'shared-breakfast-budget' not in json.dumps(graph), 'Computed cost must not become a separate Offer'
source=BeautifulSoup((root/paths[0]).read_text(),'html.parser')
totals=[int(re.sub(r'\D','',r.b.get_text())) for r in source.select('#serpme-van-kahvaltisi .portion-prices > span')]
solo_tag=source.select_one('#kahvalti-tabagi .price')
solo=int(re.sub(r'\D','',solo_tag.get_text()))
verify(root,totals,solo)
with tempfile.TemporaryDirectory() as temp:
 dest=Path(temp)
 for path in paths:
  (dest/path).parent.mkdir(parents=True,exist_ok=True)
  shutil.copy2(root/path,dest/path)
 menu=dest/paths[0];text=menu.read_text();old=str(source.select_one('#serpme-van-kahvaltisi .portion-prices b'))
 assert old in text
 old_solo=str(solo_tag)
 assert old_solo in text
 text=text.replace(old,'<b>1.202 <small>₺</small></b>',1)
 solo_start=text.index('id="kahvalti-tabagi"')
 menu.write_text(text[:solo_start]+text[solo_start:].replace(old_solo,'<p class="price">519 ₺</p>',1))
 subprocess.run([sys.executable,str(root/'scripts/build_menu_budget.py'),str(dest)],check=True)
 verify(dest,[1202,*totals[1:]],519)
 before={path:(dest/path).read_bytes() for path in paths}
 subprocess.run([sys.executable,str(root/'scripts/build_menu_budget.py'),str(dest)],check=True)
 assert all((dest/path).read_bytes()==before[path] for path in paths),'Standalone repeatability'
print('PASS: four-language price math, source-price mutation propagation, repeatability and no invented structured offers.')
