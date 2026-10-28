"""Regression checks for the complete language journey and actual menu prices."""
from pathlib import Path
import json,re,sys
from bs4 import BeautifulSoup

root=Path(sys.argv[1])
origin='https://www.pusulalounge.com'
groups=[{'tr':'/','en':'/en/','ru':'/ru/','ar':'/ar/'},
        {'tr':'/menu/','en':'/en/menu/','ru':'/ru/menu/','ar':'/ar/menu/'},
        {'tr':'/konum/','en':'/en/location/','ru':'/ru/location/','ar':'/ar/location/'}]
def page(route):return BeautifulSoup((root/route.lstrip('/')/'index.html').read_text(),'html.parser')
def graph(s):return json.loads(s.select_one('script[type="application/ld+json"]').string)['@graph']
def node(s,kind):return next(n for n in graph(s) if n['@type']==kind)
menus={}
for group in groups:
    expected={lang:origin+path for lang,path in group.items()}|{'x-default':origin+group['en']}
    for lang,route in group.items():
        s=page(route)
        assert {a['hreflang']:a['href'] for a in s.select('link[hreflang]')}==expected,route
        assert s.html['lang']==lang
        assert len(s.select('nav.site-languages'))==1
        assert {a['href'] for a in s.select('nav.site-languages a')}==set(group.values())
        assert node(s,'Restaurant')['hasMenu']==[
            {'@type':'Menu','@id':origin+p+'#menu','url':origin+p,'inLanguage':code}
            for code,p in groups[1].items()]
        if lang in ['ru','ar']:
            assert s.select_one(f'a[href="/{lang}/reservation/"]')
            assert s.select_one(f'a[href="/{lang}/menu/"]')
            assert s.html.get('dir')==('rtl' if lang=='ar' else None)
            assert not s.select_one('.eyebrow')
            if lang=='ar':assert any(b.get_text()=='08:00–17:00' for b in s.select('bdi[dir=ltr]'))
for lang,route in groups[1].items():
    s=page(route);menu=node(s,'Menu');prices={}
    for section in menu['hasMenuSection']:
        for item in section['hasMenuItem']:
            item_id=item['@id'].split('#')[-1]
            row=s.find(id=item_id)
            displayed=row.select('.portion-prices b') or row.select('.portion-list strong') or row.select('.price') or row.select('.menu-row-price')
            values=[re.sub(r'[^0-9]','',v.get_text()) for v in displayed]
            assert [offer['price'] for offer in item['offers']]==values,(lang,item_id)
            assert all(offer['priceCurrency']=='TRY' and offer['url']==item['url'] for offer in item['offers'])
            assert all('name' in offer for offer in item['offers']) if len(values)>1 else True
            prices[item_id]=values
    assert len(prices)==19
    menus[lang]=prices
assert all(m==menus['tr'] for m in menus.values()),'Menu prices differ between languages'
for lang in ['ru','ar']:
    s=page(f'/{lang}/reservation/')
    assert s.select_one(f'header a[href="/{lang}/"]')
    assert s.select_one(f'header a[href="/{lang}/menu/"]')
    assert s.select_one(f'a[href="/{lang}/location/"]')
article=json.loads((root/'scripts/van_breakfast_article.json').read_text())
for route in ['/blog/'+article['slug']+'/', '/en/blog/'+article['en']+'/']:
    s=page(route)
    assert node(s,'BlogPosting')['datePublished'].startswith(article['date'])
    assert s.select_one('time')['datetime']==article['date']
    assert s.select_one('a[href="'+article['sources'][0][0]+'"]')
print('PASS: 3 four-language groups, 76 menu items/84 price offers, native RU/AR booking journeys, article dates and sources.')
