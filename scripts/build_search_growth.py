"""Decision-ready TR/EN landing pages; prices always come from the published menu.
Run after editorial design and before font subsetting and asset integrity sealing.
"""
from pathlib import Path
from html import escape
import json, re, sys
from bs4 import BeautifulSoup

ROOT = Path(sys.argv[1]).resolve()
ORIGIN = 'https://www.pusulalounge.com'
menu = BeautifulSoup((ROOT/'menu/index.html').read_text(), 'html.parser')
portions = [(int(row.small.get_text().split()[0]), int(re.sub(r'[^0-9]', '', row.b.get_text())))
            for row in menu.select('#serpme-van-kahvaltisi .portion-prices > span')]
assert [n for n, _ in portions] == [2, 3, 4], 'Review changed menu portions'

def money(value, en):
    return (f'TRY {value:,}' if en else f'{value:,}'.replace(',', '.')+' TL')

def patch_metadata(text, title, description):
    text = re.sub(r'<title>.*?</title>', '<title>'+escape(title)+'</title>', text, flags=re.S)
    def replace(match):
        tag = BeautifulSoup(match.group(0), 'html.parser').meta
        key = tag.get('name', tag.get('property'))
        if key in ['description','og:description','twitter:description']: tag['content'] = description
        elif key in ['og:title','twitter:title']: tag['content'] = title
        return str(tag)
    return re.sub(r'<meta\b[^>]*>', replace, text)

def visit_answers(en):
    """Useful late-breakfast and solo-visitor answers, with menu-derived prices."""
    prefix = '/en/' if en else '/'
    plate = int(re.sub(r'[^0-9]', '', menu.select_one('#kahvalti-tabagi .price').get_text()))
    pisi = int(re.sub(r'[^0-9]', '', menu.select_one('#pisi-tabagi .price').get_text()))
    if en:
        heading = 'Late breakfast in Taksim: plan your visit'
        hours = 'Looking for Turkish breakfast after noon? Pusula Lounge serves breakfast every day from 08:00 to 17:00 near İstiklal Avenue in Beyoğlu. These breakfast hours also apply on weekends; check special-day hours and availability with our team.'
        timing = 'The venue is open 24 hours, but breakfast is served only during the breakfast hours above. If you are arriving close to 17:00, ask the team about the last breakfast order before setting off.'
        solo_title = 'Visiting on your own?'
        solo = f'The individual breakfast plate is {money(plate, True)} and the pişi plate is {money(pisi, True)} in our web menu. The shared Van breakfast has portions for 2, 3 or 4 people. Choose an individual plate if you are not looking for a shared spread.'
        menu_label = 'Compare individual breakfast plates'
        location_label = 'Find the entrance and walking directions'
        address = 'Find us at Sinek Çıkmazı No:3, off Küçük Parmak Kapı Sokak in Katip Mustafa Çelebi, Beyoğlu. Use the location page to open a route from your starting point.'
        location = '/en/location/'
    else:
        heading = 'Taksim’de geç kahvaltı: ziyaretinizi planlayın'
        hours = 'Öğleden sonra kahvaltı yapmak istiyorsanız Pusula Lounge, Beyoğlu’nda İstiklal yakınında her gün 08:00–17:00 arasında kahvaltı servis eder. Hafta sonu kahvaltı saatleri de aynıdır; özel gün saatlerini ve uygunluğu ekibimizle teyit edin.'
        timing = 'Mekân 24 saat açıktır; kahvaltı servisi ise yukarıdaki saatlerle sınırlıdır. Saat 17:00’ye yakın gelecekseniz yola çıkmadan önce son kahvaltı siparişi için ekibimize danışın.'
        solo_title = 'Tek kişi için kahvaltı seçenekleri'
        solo = f'Web menümüzde kahvaltı tabağı {money(plate, False)}, pişi tabağı {money(pisi, False)} olarak listelenir. Serpme Van kahvaltısının 2, 3 ve 4 kişilik porsiyonları vardır. Paylaşmalı bir sofra istemiyorsanız tek tabak seçeneklerini değerlendirebilirsiniz.'
        menu_label = 'Tek tabak kahvaltı seçeneklerini karşılaştırın'
        location_label = 'Giriş adresini ve yürüyüş tarifini görün'
        address = 'Adresimiz Katip Mustafa Çelebi Mahallesi, Küçük Parmak Kapı Sokak, Sinek Çıkmazı No:3, Beyoğlu. Bulunduğunuz noktadan yürüyüş rotası açmak için konum sayfasını kullanın.'
        location = '/konum/'
    return ('<!-- VISIT-ANSWERS:START --><section class="visit-section" aria-labelledby="late-breakfast">'
            '<h2 id="late-breakfast">'+heading+'</h2><p>'+hours+'</p><p>'+timing+'</p>'
            '<h3>'+solo_title+'</h3><p>'+solo+'</p><p><a href="'+prefix+'menu/#kahvalti-tabagi">'+menu_label+'</a></p>'
            '<p>'+address+' <a href="'+location+'">'+location_label+'</a></p>'
            '</section><!-- VISIT-ANSWERS:END -->')

metadata = {
 'menu/index.html': ('Taksim Kahvaltı Menüsü ve Fiyatları | Pusula Lounge', 'Pusula Lounge Taksim kahvaltı menüsü: 2, 3 ve 4 kişilik serpme Van kahvaltısı, kahvaltı tabağı, pişi, menemen ve gözleme fiyatlarını karşılaştırın.'),
 'en/menu/index.html': ('Taksim Breakfast Menu & Prices in TRY | Pusula Lounge', 'Read Pusula Lounge’s English breakfast menu in Taksim: shared Van breakfast for 2, 3 or 4, individual plates, menemen and gözleme. Prices in Turkish lira.'),
 'kahvalti/index.html': ('Taksim Serpme Van Kahvaltısı ve Fiyatları | Pusula Lounge', 'Taksim’de serpme Van kahvaltısı: 2, 3 ve 4 kişilik porsiyon fiyatları, sınırsız çay ve tek tabak seçenekleri. Kahvaltı 08:00–17:00; WhatsApp ile masa talebi.'),
 'en/breakfast/index.html': ('Van Breakfast in Taksim: Portions & Prices | Pusula Lounge', 'Compare shared Van breakfast for 2, 3 or 4 in Taksim, Istanbul. Menu prices, unlimited tea and individual plates. Breakfast 08:00–17:00; request a table.'),
 'konum/index.html': ('Pusula Lounge Nerede? Taksim Yol Tarifi ve İletişim', 'Pusula Lounge adresi: Sinek Çıkmazı No:3, Beyoğlu. Taksim ve İstiklal’den ulaşım, harita, telefon ve kahvaltı saatleriyle ziyaretinizi planlayın.'),
 'en/location/index.html': ('Find Pusula Lounge in Taksim | Directions & Contact', 'Visit Pusula Lounge near İstiklal Avenue: Sinek Çıkmazı No:3, Beyoğlu, Istanbul. Taksim directions, map, phone and breakfast hours in one place.'),
}
for rel, (title, description) in metadata.items():
    file = ROOT/rel
    text = patch_metadata(file.read_text(), title, description)
    en = rel.startswith('en/')
    if rel in ['kahvalti/index.html','en/breakfast/index.html']:
        prefix = '/en/' if en else '/'
        reserve = '/en/reservation/?visit=breakfast' if en else '/rezervasyon/?visit=breakfast'
        heading = 'Van breakfast in Taksim, Beyoğlu' if en else 'Taksim’de serpme Van kahvaltısı'
        text = re.sub(r'<h1>.*?</h1>', '<h1>'+heading+'</h1>', text, count=1, flags=re.S)
        text = re.sub(r'<!-- SEARCH-DECISION:START -->.*?<!-- SEARCH-DECISION:END -->', '', text, flags=re.S)
        rows = ''.join('<li><strong>'+ (f'{n} people' if en else f'{n} kişilik')+'</strong>'+money(price,en)+'</li>' for n,price in portions)
        block = '<!-- SEARCH-DECISION:START --><section class="visit-section" aria-labelledby="breakfast-prices"><h2 id="breakfast-prices">'+('Shared breakfast: portion prices' if en else 'Serpme kahvaltı porsiyon fiyatları')+'</h2><p>'+('Breakfast is served daily 08:00–17:00. The shared Van breakfast lists unlimited tea, menemen and pan-fried eggs alongside cheeses and accompaniments.' if en else 'Kahvaltı her gün 08:00–17:00 arasında servis edilir. Serpme Van kahvaltısında peynir ve eşlikçilerin yanında menemen, sahanda yumurta ve sınırsız çay listelenir.')+'</p><ul class="portion-list">'+rows+'</ul><p class="note">'+('Prices shown are the total for each portion in our web menu, not per person. Extras are separate; confirm current prices and availability before ordering.' if en else 'Fiyatlar web menümüzdeki porsiyon toplamıdır; kişi başı değildir. İlave siparişler ayrıdır; güncel fiyat ve uygunluğu sipariş öncesinde teyit edin.')+'</p><div class="visit-actions"><a class="visit-button" href="'+reserve+'">'+('Request a breakfast table' if en else 'Kahvaltı için masa isteyin')+'</a><a href="'+prefix+'menu/#serpme-van-kahvaltisi">'+('See the full breakfast menu' if en else 'Kahvaltı menüsünü inceleyin')+'</a><a href="'+('/en/location/' if en else '/konum/')+'">'+('Directions from Taksim' if en else 'Taksim’den yol tarifi')+'</a></div><p>'+('Send the request in WhatsApp and wait for our team to confirm your table.' if en else 'Talebinizi WhatsApp’ta gönderin; masanız ekibimizin onayıyla kesinleşir.')+'</p></section><!-- SEARCH-DECISION:END -->'
        text = re.sub(r'<!-- VISIT-ANSWERS:START -->.*?<!-- VISIT-ANSWERS:END -->', '', text, flags=re.S)
        block += visit_answers(en)
        # Keep the introduction, then answer price/service/booking questions before the long content.
        text, count = re.subn(r'(<div class="visit-intro">.*?</div>)', lambda m:m.group(1)+block, text, count=1, flags=re.S)
        assert count == 1, rel
    def schema(match):
        data = json.loads(match.group(2))
        for node in data.get('@graph',[]):
            if node.get('@type') == 'WebPage':
                node['name'] = title; node['description'] = description
        return match.group(1)+json.dumps(data,ensure_ascii=False).replace('<','\\u003c')+match.group(3)
    text = re.sub(r'(<script\b[^>]*type="application/ld\+json"[^>]*>)(.*?)(</script>)',schema,text,flags=re.S)
    file.write_text(text)

# Link informational articles back to the appropriate commercial breakfast page.
# Existing evening article actions already address dinner; leave that journey intact.
for en in [False,True]:
    slugs = ['turkish-breakfast-taksim','shared-breakfast-portions-prices','what-is-van-breakfast','istiklal-breakfast-walk-directions','beyoglu-breakfast-museums'] if en else ['taksimde-kahvalti-plani','serpme-kahvalti-porsiyon-fiyat-rehberi','van-kahvaltisi-nedir-pusula-sofrasi','istiklal-kahvalti-ulasim-gezi','kahvaltidan-sonra-beyoglu-sanat-muze']
    for slug in slugs:
        file=ROOT/('en/blog' if en else 'blog')/slug/'index.html'
        text=re.sub(r'<!-- BREAKFAST-NEXT:START -->.*?<!-- BREAKFAST-NEXT:END -->','',file.read_text(),flags=re.S)
        link='<p><!-- BREAKFAST-NEXT:START -->'+('Planning your meal? <a href="/en/breakfast/#breakfast-prices">Compare Pusula’s breakfast portions and prices</a> before requesting a table.' if en else 'Sofranızı seçerken <a href="/kahvalti/#breakfast-prices">Pusula’nın kahvaltı porsiyonlarını ve fiyatlarını karşılaştırın</a>; ardından masa talebinizi iletin.')+'<!-- BREAKFAST-NEXT:END --></p>'
        # Marker includes the enclosing paragraph for stable direct reruns.
        link=link.replace('<p><!-- BREAKFAST-NEXT:START -->','<!-- BREAKFAST-NEXT:START --><p>').replace('<!-- BREAKFAST-NEXT:END --></p>','</p><!-- BREAKFAST-NEXT:END -->')
        text,count=re.subn(r'(<div class="sidebar-visit">.*?)(</div>)',lambda m:m.group(1)+link+m.group(2),text,count=1,flags=re.S)
        assert count==1,file
        file.write_text(text)
print('Updated six search previews, two breakfast decision sections and ten article-to-breakfast links.')
