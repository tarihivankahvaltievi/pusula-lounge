"""Check menu-driven landing prices and their update path without changing the release."""
from pathlib import Path
from bs4 import BeautifulSoup
import json, re, shutil, subprocess, sys, tempfile
root=Path(sys.argv[1]).resolve()
def check(base):
    menu=BeautifulSoup((base/'menu/index.html').read_text(),'html.parser')
    expected=[int(re.sub(r'\D','',r.b.get_text())) for r in menu.select('#serpme-van-kahvaltisi .portion-prices > span')]
    for rel in ['kahvalti/index.html','en/breakfast/index.html']:
        s=BeautifulSoup((base/rel).read_text(),'html.parser');section=s.find(id='breakfast-prices').parent
        assert len(s.select('#breakfast-prices'))==1
        actual=[int(re.sub(r'\D','',li.get_text().removeprefix(li.strong.get_text()))) for li in section.select('li')]
        assert actual==expected,(rel,actual,expected)
        assert section.select_one('a[href$="?visit=breakfast"]')
        assert '08:00–17:00' in section.get_text()
        assert s.select_one('meta[property="og:title"]')['content']==s.title.text
        graph=json.loads(s.select_one('script[type="application/ld+json"]').string)['@graph']
        assert next(n for n in graph if n['@type']=='WebPage')['name']==s.title.text
check(root)
with tempfile.TemporaryDirectory(prefix='pusula-prices-') as tmp:
    target=Path(tmp)
    for p in root.rglob('index.html'):
        if '.git' in p.parts:continue
        copy=target/p.relative_to(root);copy.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,copy)
    menu=target/'menu/index.html'
    text=menu.read_text();s=BeautifulSoup(text,'html.parser');old=str(s.select_one('#serpme-van-kahvaltisi .portion-prices b'))
    assert old in text
    menu.write_text(text.replace(old,'<b>9.876 ₺</b>',1))
    subprocess.run([sys.executable,str(Path(__file__).with_name('build_search_growth.py')),tmp],check=True)
    check(target)
    before={p:p.read_bytes() for p in target.rglob('index.html')}
    subprocess.run([sys.executable,str(Path(__file__).with_name('build_search_growth.py')),tmp],check=True)
    assert all(p.read_bytes()==content for p,content in before.items()), 'Builder must be repeatable'
print('PASS: bilingual menu prices, metadata, booking links, changed-price propagation and repeatability.')
