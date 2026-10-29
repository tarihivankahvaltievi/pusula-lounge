"""Add researched TR/EN visitor articles to an existing static release; repeatable, no dependencies beyond bs4."""
from pathlib import Path
from html import escape as e
import json,re,hashlib,base64,sys,xml.etree.ElementTree as ET
from urllib.parse import quote
from bs4 import BeautifulSoup
R=Path(sys.argv[1]); O='https://www.pusulalounge.com'; DATE='2026-10-27'
MAP='https://share.google/l1BSBLDwv6suQkW7Y'
# Prices are read from the delivered menu, never invented or converted to other currencies.
menu=BeautifulSoup((R/'menu/index.html').read_text(),'html.parser')
portions=[(int(row.small.get_text().split()[0]),int(re.sub(r'[^0-9]','',row.b.get_text()))) for row in menu.select('#serpme-van-kahvaltisi .portion-prices > span')]
assert [n for n,_ in portions]==[2,3,4], 'Review menu portions before publishing'
ARTICLES=[
 dict(slug='taksimde-kahvalti-plani', en='turkish-breakfast-taksim',
 title=('Taksim’de Kahvaltı: İlk Ziyaretinizi Planlayın','Turkish Breakfast in Taksim: Plan Your First Visit'),
 desc=('Taksim’de kahvaltı planı: Pusula Lounge’da serpme Van kahvaltısı, tek kişilik seçenekler, çay, servis saatleri ve WhatsApp ile masa talebi.', 'Plan Turkish breakfast in Taksim at Pusula Lounge: shared Van breakfast, individual dishes, tea, breakfast hours and requesting a table on WhatsApp.'),
 lead=('Taksim’de kahvaltı için Pusula Lounge’a gelirken önce sofrayı, sonra ziyaret saatinizi seçebilirsiniz. İstiklal çevresindeki mekânımızda serpme Van kahvaltısı ve ayrı kahvaltı tabakları bulunur. Bu yazı, ilk siparişinizden masa talebine kadar ziyaretinizi planlamanız için hazırlandı.', 'Planning your first Turkish breakfast in Taksim? Pusula Lounge serves shared Van breakfast and individual breakfast dishes in the İstiklal area of Beyoğlu, Istanbul. Start with your group size, compare the menu and choose a breakfast time before requesting a table.'),
 sections=[
 ('Serpme mi, tek tabak mı?','A shared spread or an individual plate?',
 'Serpme kahvaltı, ortaya gelen tabakları birlikte paylaşmak isteyenler için bir seçenektir. Pusula menüsünde iki, üç ve dört kişilik porsiyonlar ayrı listelenir. Kahvaltı tabağı ise kendi içeriği ve fiyatı olan farklı bir üründür. Bir kişinin daha hafif, diğerinin daha geniş bir kahvaltı istemesi durumunda herkesin aynı ürünü seçmesi gerektiğini varsaymayın; siparişi masadaki tercihlere göre ekiple konuşun.',
 'Serpme kahvaltı means a spread of dishes served for sharing. Our menu lists separate portions for two, three and four people. An individual breakfast plate is a different dish with its own contents and price. If one guest wants a full spread and another wants something smaller, discuss your order with the team rather than assuming every guest needs the same breakfast.'),
 ('Sofrada hangi lezzetler var?','What is on the breakfast table?',
 'Serpme Van kahvaltısında otlu Van peyniri ve diğer peynirler, bal-kaymak, zeytin, tahin pekmez, reçel, domates, salatalık, menemen, sahanda yumurta ve sınırsız çay listelenir. Sıcak ürünleri ayrıca sipariş etmek isterseniz menemen, gözleme ve omlet seçeneklerini inceleyin. Pişi tabağı ayrı bir üründür; serpmenin içinde olduğunu varsaymak yerine menü içeriğine bakın.',
 'The shared Van breakfast lists cheeses including Van herb cheese, honey and kaymak (clotted cream), olives, tahini with grape molasses, jam, tomatoes, cucumber, menemen, pan-fried eggs and unlimited tea. Separately listed dishes include gözleme, omelette and menemen variations. Pişi, fried dough, has its own plate; check the listed contents before assuming it is included in the spread.'),
 ('Çay ve ilaveleri nasıl seçmeli?','How do tea and extras work?',
 'Serpme kahvaltının açıklamasında sınırsız çay, kahvaltı tabağının açıklamasında çay bulunur. Pişi tabağında çay listelenmez. Ayrı bir sıcak ürün, içecek veya ilave istediğinizde bunun seçtiğiniz kahvaltı fiyatına dahil olup olmadığını sipariş öncesinde sorun. Böylece sofranın içeriğini de ödeyeceğiniz toplamı da birlikte netleştirebilirsiniz.',
 'Unlimited tea is listed with the shared breakfast; tea is listed with the individual breakfast plate. The pişi plate does not list tea. When adding a hot dish or another drink, ask whether it is included in your chosen breakfast or charged separately. Check both the portion and its contents before comparing prices.'),
 ('Kahvaltı saati ile genel çalışma saatini ayırın','Choose a breakfast time',
 'Sitedeki işletme bilgilerine göre kahvaltı her gün 08:00–17:00 arasında servis edilir. İşletmenin genel çalışma saatinin 24 saat olması, gece serpme kahvaltı sunulduğu anlamına gelmez. Özellikle erken, geç veya özel bir günde gelecekseniz saatinizi ekiple teyit edin. Kalabalık bir grup için tarih ve kişi sayısını önceden paylaşmak masa planlamasını kolaylaştırır.',
 'The breakfast service shown on our website is daily 08:00–17:00. The business’s general opening hours are listed as 24 hours; that does not mean the breakfast spread is available all night. Confirm the service time if arriving early, late or on a holiday. Give the team your date and group size when asking about a table.'),
 ('Masanızı nasıl talep edebilirsiniz?','How to request your table',
 'Rezervasyon formunda tarih, saat ve kişi sayısını girin. Formun hazırladığı talebi WhatsApp’ta gönderin ve ekipten onay bekleyin. Formu doldurmak tek başına masayı ayırmaz. Son dakika soruları için +90 507 816 29 94 numarasını arayabilirsiniz. Adresimiz Katip Mustafa Çelebi Mahallesi, Küçük Parmak Kapı Sokak, Sinek Çıkmazı No:3, Beyoğlu / İstanbul.',
 'Choose a date, time and guest count in the reservation form, send the prepared request in WhatsApp and wait for the team’s confirmation. Filling out the form alone does not reserve a table. For a last-minute question, call +90 507 816 29 94. Our address is Katip Mustafa Çelebi Mahallesi, Küçük Parmak Kapı Sokak, Sinek Çıkmazı No:3, Beyoğlu, Istanbul.'),
 ('Özel beslenme ihtiyaçlarını siparişten önce konuşun','Discuss dietary requirements before ordering',
 'Ürün açıklamaları tüm alerjenleri ve hazırlama koşullarını kapsamaz. Bir gözlemenin veya tabağın içeriğini değiştirmenin mümkün olup olmadığını ekibe sorun. Çocuk sandalyesi, grup düzeni veya başka bir ihtiyaç varsa rezervasyon notuna ekleyin; karşılanabildiğini ekiple netleştirin.',
 'Menu descriptions do not cover every allergen or preparation detail. Ask the team whether changes to a dish are possible. Add a high-chair request, group arrangement or other need to the reservation note and confirm it with the team. Do not infer dietary suitability from a dish name alone.')]),
 dict(slug='serpme-kahvalti-porsiyon-fiyat-rehberi',en='shared-breakfast-portions-prices',
 title=('Serpme Kahvaltı Fiyatı: Porsiyon ve Bütçe Rehberi','Shared Breakfast Prices: Portions and Budget Guide'),
 desc=('Pusula Lounge menüsündeki 2, 3 ve 4 kişilik serpme Van kahvaltısını, tek tabak seçeneklerini ve kişi başı hesaplamayı karşılaştırın.', 'Compare Pusula Lounge’s shared Van breakfast portions for two, three and four guests, individual plates and what menu prices mean for your budget.'),
 lead=('Serpme kahvaltı fiyatını karşılaştırırken önce kaç kişilik porsiyon aldığınıza bakın. Pusula Lounge’da iki, üç ve dört kişilik serpme Van kahvaltısı ayrı fiyatlarla listelenir. Aşağıdaki karşılaştırma mevcut web menüsündeki rakamları açıklar; siparişinizin güncel tutarını ekiple teyit edin.', 'When comparing Turkish breakfast prices, check how many people the listed portion serves. At Pusula Lounge, shared Van breakfast has separate prices for two, three and four guests. This comparison explains our current website menu; confirm the latest total with the team before ordering.'),
 sections=[
 ('Kişi başı karşılaştırmayı doğru yapın','Read portion prices correctly',
 'İki kişilik bir serpmenin menü fiyatı, o porsiyonun toplamıdır. Kişi başı karşılaştırma yapmak için toplamı belirtilen kişi sayısına bölün. Bu hesap siparişte ayrı bir kişi başı fiyat uygulandığı anlamına gelmez. Dört kişilik seçeneğin kişi başı hesabının diğer porsiyonlarla aynı çıkacağını varsaymayın; her porsiyonu kendi menü fiyatıyla değerlendirin.',
 'A two-person spread is listed with a total price for that portion. Divide that total by the stated guest count if you want a per-person comparison. This calculation is not a separate per-person offer. Do not assume a four-person portion has the same calculated price per guest as the smaller portions; compare each listed total.'),
 ('Tek kişi veya farklı iştahlar için','For solo visitors and different appetites',
 'Kahvaltı tabağı ve pişi tabağı, serpmeden ayrı ürünlerdir. Kahvaltı tabağında peynir, bal-kaymak, zeytin, haşlanmış yumurta ve çay gibi ürünler listelenirken pişi tabağında üç adet pişi, tulum peyniri, reçel ve zeytin bulunur. Bu nedenle yalnız fiyatı karşılaştırmak yerine sıcak ürünleri, içecekleri ve porsiyon açıklamasını birlikte okuyun.',
 'The breakfast plate and pişi plate are separate from the spread. The breakfast plate lists cheeses, honey and kaymak, olives, a boiled egg and tea among its contents. The pişi plate lists three pieces of fried dough, tulum cheese, jam and olives. Compare what is included, including drinks and hot dishes, rather than comparing the price alone.'),
 ('İlave siparişleri toplamdan ayrı değerlendirin','Allow for separately ordered extras',
 'Serpmenin açıklamasında menemen, sahanda yumurta ve sınırsız çay yer alır. Ancak menüde ayrı satırda bulunan her menemen çeşidinin veya içeceğin dahil olduğunu varsaymayın. Örneğin gözleme ya da farklı bir içecek ekleyecekseniz ilave ücretini sorun. Masadaki herkesin tercihi farklıysa siparişin hangi porsiyonlardan oluştuğunu ve toplam tutarı baştan konuşun.',
 'Menemen, pan-fried eggs and unlimited tea appear in the shared breakfast description. That does not mean every separately listed menemen variation or drink is included. If adding gözleme or a different drink, ask about the additional charge. When guests want different dishes, agree on the portions and the order total before the food is prepared.'),
 ('Fiyatlar hangi para biriminde?','Which currency are the menu prices in?',
 'Menü fiyatları Türk lirası, yani ₺ / TRY cinsindedir. Bu yazıda kur dönüşümü yapılmaz; döviz karşılığı ödeme anındaki kura göre farklılaşabilir. Ödeme yöntemleri veya ek ücretlerle ilgili kesin bir bilgiye ihtiyacınız varsa sipariş öncesinde işletmeye sorun. Web menüsü bütçe planlamak için başlangıç noktasıdır; güncel fiyat, ürün uygunluğu ve servis koşullarını ekip teyit eder.',
 'Prices are in Turkish lira, shown as ₺ / TRY. This article does not convert them into another currency; exchange rates change. Ask the business directly about payment methods or any additional charges before ordering. The website menu is a starting point for budgeting, while the team confirms current prices, availability and service terms.'),
 ('Grup için masa talebi','Requesting a table for your group',
 'Kişi sayınız menüdeki porsiyonlardan farklıysa kendi kombinasyonunuzu varsaymak yerine ekibe sorun. WhatsApp talebinde tarih, saat ve toplam kişi sayısını belirtin. Porsiyon seçimi ile masa rezervasyonunun farklı adımlar olduğunu unutmayın: masa uygunluğu işletmenin onayıyla kesinleşir; sipariş içeriği ve fiyatını da ekip ile konuşabilirsiniz.',
 'If your group size does not match a listed portion, ask the team how to combine orders rather than assuming a particular arrangement. Include the date, time and full guest count in your WhatsApp request. Choosing a breakfast portion and reserving a table are separate steps: a table is confirmed by the team, and the order contents and price can be discussed with them.')]),
 dict(slug='istiklal-kahvalti-ulasim-gezi',en='istiklal-breakfast-walk-directions',
 title=('İstiklal’de Kahvaltı ve Gezi: Taksim’den Bir Sabah Planı','Breakfast and a Walk on İstiklal: A Taksim Morning'),
 desc=('İstiklal’de kahvaltıyı Beyoğlu gezisiyle birleştirin. Taksim’e M2 ve F1 bağlantıları, Pusula Lounge adresi ve esnek bir sabah planı.', 'Combine breakfast near İstiklal with a Beyoğlu walk. Find Taksim’s M2 and F1 connections, Pusula Lounge’s address and a flexible morning plan.'),
 lead=('Beyoğlu’nda kahvaltı ve geziyi aynı güne koymak isterseniz, önce geliş noktanızı ve kahvaltı saatinizi belirleyin. Bu plan Taksim, Pusula Lounge ve İstiklal çevresini birleştiren esnek bir öneridir. Sabit yürüyüş süresi veya rehberli tur içermez; rotayı hava durumuna ve ilginize göre değiştirebilirsiniz.', 'A Beyoğlu morning can begin with breakfast and continue with a walk around İstiklal. This suggested plan connects Taksim, Pusula Lounge and the surrounding area. It is a flexible self-guided idea, with no fixed walking time or guided tour included; adapt it to the weather and your interests.'),
 sections=[
 ('Taksim’e raylı sistemle gelmek','Arriving at Taksim by rail',
 'Taksim, M2 metro hattı üzerinde yer alır. Kabataş’tan F1 füniküleriyle Taksim’e ulaşılabilir. Metro İstanbul’un resmi hat bilgilerini ve güncel duyurularını yolculuk öncesinde kontrol edin. Otelinizin konumuna göre uygun aktarma değişeceği için tüm ziyaretçiler için tek bir güzergâh önermiyoruz.',
 'Taksim is on the M2 metro line, and the F1 funicular connects Kabataş with Taksim. Check Metro İstanbul’s official line information and service notices before travelling. The right connection depends on where you are staying, so choose the route from your actual starting point.'),
 ('Son yürüyüş için işletme konumunu açın','Use the business map for the final approach',
 'Pusula Lounge, Katip Mustafa Çelebi Mahallesi, Küçük Parmak Kapı Sokak, Sinek Çıkmazı No:3 adresindedir. Taksim’e geldikten sonra işletmenin harita kaydını açarak bulunduğunuz noktadan yürüyüş yolunu kontrol edin. Ara sokaktaki giriş için yön bulmakta zorlanırsanız ekibi arayın. Yalnızca cadde adını takip etmek yerine kapı numarasını da kontrol edin.',
 'Pusula Lounge is at Katip Mustafa Çelebi Mahallesi, Küçük Parmak Kapı Sokak, Sinek Çıkmazı No:3. After reaching Taksim, open the business map listing and check the walking route from your position. Look for the door number as well as the street name. If you have trouble finding the entrance, call the team.'),
 ('Kahvaltıyı günün ilk sabit noktası yapın','Make breakfast your first planned stop',
 'Kahvaltı servis aralığı sitede her gün 08:00–17:00 olarak belirtilir. Sonrasında biletli bir etkinliğe yetişecekseniz kahvaltı için ayıracağınız zamanı kendiniz planlayın; burada servis veya yürüyüş süresi sözü verilmez. Masa talebinde geliş saatinizi paylaşın ve işletme onayı alın. Çocuklarla veya kalabalık grupla gelecekseniz ihtiyaçlarınızı önceden yazın.',
 'Breakfast is listed on our website as daily 08:00–17:00. If you have a ticketed activity afterwards, leave enough time for your meal and journey; this suggested plan does not promise a service or walking duration. Share your arrival time in the table request and wait for confirmation. Mention children or group needs in advance.'),
 ('Kahvaltıdan sonra kendi İstiklal rotanızı seçin','Choose your İstiklal walk after breakfast',
 'Yemeğin ardından İstiklal çevresinde yürüyüşe çıkabilir, ilginizi çeken sokaklarda mola verebilirsiniz. Galata yönünü de düşünüyorsanız günün kalan kısmını kendi temponuza göre ayırın. Bu yazı bir müze bileti, ücretsiz giriş veya işletmeler arası ortaklık sunmaz. Ziyaret etmek istediğiniz müze ve etkinliklerin resmi sayfalarından saat ve bilet bilgilerini ayrıca kontrol edin.',
 'After your meal, explore the İstiklal area at your own pace and stop in the streets that interest you. If continuing towards Galata, allow time according to your walking pace. This article does not include attraction tickets or an arrangement with other businesses. Check each museum or event’s official website for its own opening hours and tickets.'),
 ('Hava, hareketlilik ve dönüş planı','Weather, mobility and the return journey',
 'Yağışlı bir günde daha kısa bir yürüyüş seçebilir, kahvaltıdan sonra programı yeniden düzenleyebilirsiniz. Basamaksız giriş veya çocuk arabasıyla erişim gibi bir ihtiyacınız varsa işletmeye ve ulaşım işletmecisine doğrudan sorun; bu rota erişilebilirlik garantisi değildir. Dönüşte de istasyon duyurularını kontrol edin. Böylece kahvaltı, günlük planınızın baskı oluşturmayan bir parçası olur.',
 'On a wet day, shorten the walk or adjust your plans after breakfast. If you need step-free access or are using a pushchair, ask the restaurant and transport operator directly; this suggested route does not guarantee accessibility. Check station notices again for the return trip. Keep the rest of the morning flexible rather than trying to follow a minute-by-minute itinerary.')])]
def digest(path):
 b=(R/path.lstrip('/')).read_bytes();return hashlib.sha256(b).hexdigest()[:12],'sha256-'+base64.b64encode(hashlib.sha256(b).digest()).decode()
def asset(path):
 v,s=digest(path);return f'<link rel="stylesheet" href="{path}?v={v}" integrity="{s}" crossorigin="anonymous">'
def j(data):return json.dumps(data,ensure_ascii=False).replace('<','\\u003c')
def route(a,en):return ('/en/blog/'+a['en'] if en else '/blog/'+a['slug'])+'/'
def link(path,label):return '<a href="'+path+'">'+e(label)+'</a>'
def menu_inquiry_link(article,en):
 i=int(en)
 message=article['menuInquiryMessage'][i]
 href='https://wa.me/905078162994?text='+quote(message,safe='')
 return '<a href="'+href+'" data-interaction="menu-inquiry">'+e(article['menuInquiryLabel'][i])+'</a>'
# This researched article has its own real publication date.
ARTICLES.append(json.loads((Path(__file__).parent/'van_breakfast_article.json').read_text()))
ARTICLES.append(json.loads((Path(__file__).parent/'taksim-evening-article.json').read_text()))
ARTICLES.append(json.loads((Path(__file__).parent/'culture_article.json').read_text()))
# Inherit existing fonts, colors, header/footer and identity graph.
base={}
for en in [False,True]:
 t=(R/('en/breakfast-guide/index.html' if en else 'kahvalti-rehberi/index.html')).read_text();s=BeautifulSoup(t,'html.parser')
 g=json.loads(s.select_one('script[type="application/ld+json"]').string)['@graph']
 base[en]=(str(s.select_one('header')),str(s.select_one('footer')), [x for x in g if x['@type'] in ['Restaurant','WebSite']])
css='''/* Editorial extension of the existing visitor pages. */
.blog-page article,.blog-page .blog-index{max-width:74ch;margin-inline:auto}.blog-page .visit-intro{padding-bottom:28px}.blog-page .article-meta{font-size:16px;color:var(--green);margin-bottom:28px}.blog-page .article-photo{margin-bottom:36px}.blog-page .article-photo img{aspect-ratio:3/2;object-fit:cover}.blog-page .article-photo--portrait img{aspect-ratio:2/3;max-height:min(84vh,960px);object-position:center 68%}.blog-page .article-toc{border-block:1px solid var(--line);padding:22px 0;margin:30px 0}.blog-page .article-toc ul{padding-inline-start:24px;margin:12px 0 0}.blog-page li{margin-bottom:10px}.blog-page .visit-section{padding-block:34px}.blog-page .visit-section h2{margin-bottom:18px}.blog-page .visit-section p:last-child{margin-bottom:0}.blog-page .blog-entries{list-style:none;margin:0;padding:0}.blog-page .blog-entries li{padding:30px 0;border-top:1px solid var(--line)}.blog-page .blog-entries h2{margin-bottom:14px}.blog-page .table-scroll{overflow-x:auto;max-width:100%;margin:28px 0}.blog-page table{width:100%;border-collapse:collapse;font-size:17px;font-variant-numeric:tabular-nums}.blog-page caption{text-align:start;font-weight:700;margin-bottom:14px}.blog-page th,.blog-page td{text-align:start;padding:14px 10px;border-bottom:1px solid var(--line)}.blog-page thead{background:var(--sun)}.blog-page .article-actions{display:flex;flex-wrap:wrap;gap:12px 24px;align-items:center}.blog-page ::selection{background:var(--sun);color:var(--ink)}.blog-page h1{max-width:18ch}.blog-page a:hover{text-decoration-thickness:2px}.blog-page a:focus-visible{outline:3px solid var(--green);outline-offset:4px}.blog-page .sources{font-size:16px}.blog-page .visit-intro .lead{font-size:21px}@media(max-width:480px){.blog-page th,.blog-page td{padding:12px 6px;font-size:15px}.blog-page .article-toc a{display:inline-block;padding-block:5px}.blog-page .visit-intro{padding-top:32px}}
'''
(R/'blog.css').write_text(css)
def render(path,title,desc,en,pair,body,article=None):
 publication=article.get('date',DATE) if article else DATE
 lang='en' if en else 'tr';home='/en/' if en else '/';index='/en/blog/' if en else '/blog/';label='Food & visit journal' if en else 'Sofra ve ziyaret günlüğü';header,footer,identity=base[en];url=O+path
 old_pair='/kahvalti-rehberi/' if en else '/en/breakfast-guide/'
 header=header.replace('href="'+old_pair+'"','href="'+pair+'"');footer=footer.replace('href="'+old_pair+'"','href="'+pair+'"')
 crumbs=[('Home' if en else 'Ana sayfa',home)]+([(label,index)] if article else [])+[(title,path)]
 breadcrumb={'@type':'BreadcrumbList','@id':url+'#breadcrumb','itemListElement':[{'@type':'ListItem','position':i+1,'name':n,'item':O+p} for i,(n,p) in enumerate(crumbs)]}
 web={'@type':'WebPage','@id':url+'#webpage','url':url,'name':title,'description':desc,'inLanguage':lang,'isPartOf':{'@id':O+'/#website'},'about':{'@id':O+'/#restaurant'},'breadcrumb':{'@id':url+'#breadcrumb'}}
 graph=identity+[web,breadcrumb]
 if article:
  image_path=article.get('image','/assets/gallery/pusula-sofrasi-1200.webp')
  image_width,image_height=article.get('imageDimensions',[1200,800])
  image_caption=article.get('imageCaption',['Pusula Lounge’da paylaşılan kahvaltı sofrası','A shared breakfast table at Pusula Lounge'])[int(en)]
  web['primaryImageOfPage']={'@type':'ImageObject','url':O+image_path,'contentUrl':O+image_path,'width':image_width,'height':image_height,'inLanguage':lang,'caption':image_caption}
  modified=article.get('dateModified',publication)
  graph.append({'@type':'BlogPosting','@id':url+'#article','headline':title,'description':desc,'url':url,'inLanguage':lang,'datePublished':publication+'T00:00:00+03:00','dateModified':modified+'T00:00:00+03:00','author':{'@id':O+'/#restaurant'},'publisher':{'@id':O+'/#restaurant'},'mainEntityOfPage':{'@id':url+'#webpage'},'image':O+image_path,'isPartOf':{'@id':O+index+'#blog'}})
 else:
  graph.append({'@type':'Blog','@id':url+'#blog','name':title,'url':url,'inLanguage':lang,'publisher':{'@id':O+'/#restaurant'},'blogPost':[{'@id':O+route(a,en)+'#article'} for a in ARTICLES]})
 alt=article.get('imageAlt',['Pusula Lounge’da paylaşılan kahvaltı sofrası','A shared breakfast table at Pusula Lounge'])[int(en)] if article else ('Breakfast at Pusula Lounge in Taksim' if en else 'Taksim Pusula Lounge’da kahvaltı sofrası')
 social_image=O+article.get('image','/assets/gallery/pusula-sofrasi-share.jpg') if article else O+'/assets/gallery/pusula-sofrasi-share.jpg'
 social_width,social_height=article.get('imageDimensions',[1200,800]) if article else (1200,800)
 social_type='image/webp' if social_image.endswith('.webp') else 'image/jpeg'
 metadata=f'<title>{e(title)} · Pusula Lounge</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{url}"><meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">'
 for l,p in [(lang,path),('tr' if en else 'en',pair),('x-default',path if en else pair)]:metadata+=f'<link rel="alternate" hreflang="{l}" href="{O+p}">'
 for key,val in {'type':'article' if article else 'website','site_name':'Pusula Lounge','title':title,'description':desc,'url':url,'locale':'en_GB' if en else 'tr_TR','image':social_image,'image:width':str(social_width),'image:height':str(social_height),'image:type':social_type,'image:alt':alt}.items():metadata+=f'<meta property="og:{key}" content="{e(val)}">'
 for key,val in {'card':'summary_large_image','title':title,'description':desc,'image':social_image,'image:alt':alt}.items():metadata+=f'<meta name="twitter:{key}" content="{e(val)}">'
 if article:metadata+=f'<meta property="article:published_time" content="{publication}T00:00:00+03:00"><meta property="article:modified_time" content="{publication}T00:00:00+03:00">'
 breadcrumb_html='<nav class="seo-breadcrumb" aria-label="'+('Breadcrumb' if en else 'Sayfa yolu')+'"><ol>'+''.join('<li>'+ (link(p,n) if i<len(crumbs)-1 else '<span aria-current="page">'+e(n)+'</span>')+'</li>' for i,(n,p) in enumerate(crumbs))+'</ol></nav>'
 language='<p>'+link(pair,'Türkçe' if en else 'Read in English')+'</p>'
 header=header.replace(' aria-current="page"','').replace('>Talep hazırla</a>','>Rezervasyon</a>')
 journal_link=link(index,'Journal' if en else 'Blog')
 if not article:journal_link=journal_link.replace('<a ','<a aria-current="page" ')
 header=header.replace('</nav>',journal_link+'</nav>')
 footer=footer.replace('</footer>','<nav aria-label="'+('Food & visit journal' if en else 'Sofra ve ziyaret günlüğü')+'">'+link(index,label)+'</nav></footer>')
 scriptpath='/seo-events.js';v,sri=digest(scriptpath)
 output=f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">{metadata}<link rel="icon" href="/assets/pusula-amblem.png" type="image/png">'+''.join(asset(p) for p in ['/assets/menu/fonts.css','/visit.css','/seo-common.css','/blog.css'])+f'<script type="application/ld+json">{j({"@context":"https://schema.org","@graph":graph})}</script><script src="{scriptpath}?v={v}" integrity="{sri}" crossorigin="anonymous" defer></script></head><body class="visit-page blog-page"><a class="skip" href="#content">'+('Skip to content' if en else 'İçeriğe geç')+f'</a>{header}<main id="content">{breadcrumb_html}{language}{body}</main>{footer}</body></html>'
 p=R/path.lstrip('/')/'index.html';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(output)
 return path
new=[]
for en in [False,True]:
 i=int(en);prefix='/en/' if en else '/';index=prefix+'blog/';reservation='/en/reservation/' if en else '/rezervasyon/'
 for a in ARTICLES:
  publication=a.get('date',DATE); date_label=a.get('dateLabel',['27 Ekim 2026','27 October 2026'])[i]
  intent='dinner' if a['en']=='dinner-waffle-coffee-taksim' else 'breakfast'
  intent_reservation=reservation+'?visit='+intent
  toc='<nav class="article-toc" aria-label="'+('On this page' if en else 'Bu yazıda')+'"><strong>'+('On this page' if en else 'Bu yazıda')+'</strong><ul>'+''.join('<li>'+link('#section-'+str(k+1),s[i])+'</li>' for k,s in enumerate(a['sections']))+'</ul></nav>'
  body='<article><header class="visit-intro"><h1>'+e(a['title'][i])+'</h1><p class="lead">'+e(a['lead'][i])+'</p></header><p class="article-meta">Pusula Lounge · <time datetime="'+publication+'">'+e(date_label)+'</time>'
  if a.get('dateModified') and a['dateModified']!=publication:body+=' · '+('Updated ' if en else 'Güncellendi: ')+e(a['dateModifiedLabel'][i])
  body+='</p>'
  evening=a['en']=='dinner-waffle-coffee-taksim'
  menu_label='Breakfast menu & prices' if en else 'Kahvaltı menüsü ve fiyatları'
  body+='<div class="article-actions"><a class="visit-button" href="'+intent_reservation+'">'+('Request a table' if en else 'Masa talebi gönder')+'</a>'
  if evening:body+=menu_inquiry_link(a,en)
  body+=link('/en/menu/' if en else '/menu/',menu_label)+'</div>'
  photo=a.get('image','/assets/gallery/pusula-sofrasi-1200.webp');photo_alt=a.get('imageAlt',['Pusula Lounge’da paylaşılan kahvaltı sofrası','A shared breakfast table at Pusula Lounge'])[i];photo_caption=a.get('imageCaption',['Sipariş öncesinde menüden porsiyonları ve içerikleri karşılaştırın.','Compare portions and contents in the menu before ordering.'])[i];photo_width,photo_height=a.get('imageDimensions',[1200,800])
  photo_stem=photo.rsplit('-',1)[0]
  photo_class='article-photo article-photo--portrait' if photo_height>photo_width else 'article-photo'
  photo_tag='<figure class="'+photo_class+'"><img src="'+photo+'" srcset="'+photo_stem+'-600.webp 600w, '+photo+' '+str(photo_width)+'w" sizes="(max-width: 800px) calc(100vw - 40px), 740px" width="'+str(photo_width)+'" height="'+str(photo_height)+'" alt="'+e(photo_alt)+'" decoding="async" fetchpriority="high"><figcaption>'+e(photo_caption)+'</figcaption></figure>'
  body+=photo_tag+toc
  if a['en']=='shared-breakfast-portions-prices':
   body+='<div class="table-scroll" role="region" aria-label="'+('Menu price comparison' if en else 'Menü fiyat karşılaştırması')+'" tabindex="0"><table><caption>'+('Website menu comparison, 27 October 2026 (TRY)' if en else 'Web menüsü karşılaştırması, 27 Ekim 2026 (TL)')+'</caption><thead><tr>'+''.join('<th scope="col">'+v+'</th>' for v in (['Shared portion','Portion total','Calculated per guest'] if en else ['Serpme porsiyonu','Porsiyon toplamı','Hesaplanan kişi başı']))+'</tr></thead><tbody>'+''.join('<tr><th scope="row">'+str(n)+(' guests' if en else ' kişilik')+'</th><td>'+str(total)+' ₺</td><td>'+format(total/n,'.2f').rstrip('0').rstrip('.')+' ₺</td></tr>' for n,total in portions)+'</tbody></table></div><p>'+('These are the prices displayed on the website menu, not a new quote. Calculated per-guest figures are only comparisons; confirm your order total before ordering.' if en else 'Bunlar web menüsünde gösterilen fiyatlardır; yeni bir fiyat teklifi değildir. Kişi başı değerler yalnızca karşılaştırma hesabıdır. Sipariş toplamınızı ekiple teyit edin.')+'</p>'
   # Fail closed if existing menu no longer contains the source figures.
   assert len(portions)==3
  for k,s in enumerate(a['sections']):body+='<section class="visit-section" id="section-'+str(k+1)+'"><h2>'+e(s[i])+'</h2><p>'+e(s[2+i])+'</p></section>'
  visit_title=('Plan your evening at Pusula' if en else 'Pusula’da akşam ziyaretinizi planlayın') if evening else ('Plan your breakfast at Pusula' if en else 'Pusula’da kahvaltınızı planlayın')
  body+='<section class="visit-section"><h2>'+visit_title+'</h2><div class="article-actions"><a class="visit-button" href="'+intent_reservation+'">'+('Request a table' if en else 'Masa talebi gönder')+'</a>'
  if evening:body+=menu_inquiry_link(a,en)
  body+=link(prefix+'menu/' if en else '/menu/',menu_label)+link(MAP,'Open business map' if en else 'Haritada konumu aç')+'</div>'
  if evening:body+='<p>'+e(a['menuInquiryNote'][i])+'</p>'
  body+='<p><a href="tel:+905078162994">+90 507 816 29 94</a></p></section>'
  body+='<section class="visit-section"><h2>'+('Keep reading' if en else 'Diğer yazılar')+'</h2><ul>'+''.join('<li>'+link(route(other,en),other['title'][i])+'</li>' for other in ARTICLES if other!=a)+'</ul></section>'
  body+='<section class="visit-section sources"><h2>'+('Sources and updates' if en else 'Kaynaklar ve güncellemeler')+'</h2><p>'+('This article uses Pusula Lounge’s published breakfast menu and visit information. Evening items, availability and prices should be confirmed with the team. Business hours were last checked against the business listing on 9 October 2026; reconfirm special-day hours and availability. Content was prepared with AI assistance and checked against those sources.' if en and evening else 'This article uses Pusula Lounge’s published menu and visit information. Business hours were last checked against the business listing on 9 October 2026; reconfirm special-day hours and availability. Content was prepared with AI assistance and checked against those sources.' if en else 'Bu yazı Pusula Lounge’un yayınlanan kahvaltı menüsüne ve ziyaret bilgilerine dayanır. Akşam ürünlerini, uygunluğu ve fiyatları ekiple teyit edin. İşletme saatlerinin harita kaydındaki son kontrol tarihi 9 Ekim 2026’dır; özel gün saatlerini ve uygunluğu yeniden teyit edin. İçerik yapay zekâ desteğiyle hazırlanmış, bu kaynaklarla karşılaştırılmıştır.' if evening else 'Bu yazı Pusula Lounge’un yayınlanan menüsüne ve ziyaret bilgilerine dayanır. İşletme saatlerinin harita kaydındaki son kontrol tarihi 9 Ekim 2026’dır; özel gün saatlerini ve uygunluğu yeniden teyit edin. İçerik yapay zekâ desteğiyle hazırlanmış, bu kaynaklarla karşılaştırılmıştır.')+'</p><ul><li>'+link(prefix+'menu/' if en else '/menu/','Pusula Lounge breakfast menu' if en else 'Pusula Lounge kahvaltı menüsü')+'</li><li>'+link('/en/location/' if en else '/konum/','Business address and hours' if en else 'İşletme adresi ve saatleri')+'</li>'
  if a['en']=='istiklal-breakfast-walk-directions':body+='<li>'+link('https://metro.istanbul/Hatlarimiz/HatDetay?hat=F1','Metro İstanbul — F1 Taksim–Kabataş')+'</li><li>'+link('https://metro.istanbul/','Metro İstanbul — '+('lines and service notices' if en else 'hatlar ve sefer duyuruları'))+'</li>'
  for source in a.get('sources',[]):body+='<li>'+link(source[0],source[2 if en else 1])+'</li>'
  body+='</ul></section></article>'
  new.append(render(route(a,en),a['title'][i],a['desc'][i],en,route(a,not en),body,a))
 title='Taksim Food & Visit Journal' if en else 'Taksim’de Sofra ve Ziyaret Rehberi'
 desc='Pusula Lounge’da kahvaltı, akşam yemeği, tatlı ve içecek seçenekleri; menü ve ziyaret planı için yerel rehber.' if not en else 'A local guide to breakfast, dinner, dessert and drinks at Pusula Lounge, with menu and visit planning.'
 body='<div class="blog-index"><header class="visit-intro"><h1>'+e(title)+'</h1><p class="lead">'+e(desc)+'</p></header><ol class="blog-entries">'+''.join('<li><h2>'+link(route(a,en),a['title'][i])+'</h2><p>'+e(a['desc'][i])+'</p>'+link(route(a,en),'Read article' if en else 'Yazıyı oku')+'</li>' for a in ARTICLES)+'</ol><section class="visit-section"><h2>'+('Ready to choose your breakfast?' if en else 'Sofranızı seçmeye hazır mısınız?')+'</h2><div class="article-actions">'+link('/en/menu/' if en else '/menu/',menu_label)+'<a class="visit-button" href="'+reservation+'">'+('Request a table' if en else 'Masa talebi gönder')+'</a></div></section></div>'
 new.append(render(index,title,desc,en,'/blog/' if en else '/en/blog/',body))
# Link from existing indexable pages, preserving reservation work owned by the other task.
changed=[]
for p in R.rglob('*.html'):
 rel=p.relative_to(R).as_posix()
 if rel.startswith(('.git/','blog/','en/blog/','seo/')) or 'reservation/' in rel or 'rezervasyon/' in rel or p.name=='404.html' or p.name.startswith(('google','__')):continue
 t=re.sub(r'<!-- JOURNAL:START -->.*?<!-- JOURNAL:END -->','',p.read_text(),flags=re.S)
 if '<main' not in t or BeautifulSoup(t,'html.parser').html.get('lang') not in ['tr','en']:continue
 en=BeautifulSoup(t,'html.parser').html.get('lang')=='en';target='/en/blog/' if en else '/blog/'
 if '<!-- JOURNAL:START -->' not in t:
  section='<section class="visit-section"><h2>'+('Plan food and a visit in Taksim' if en else 'Taksim’de sofra ve ziyaret planı')+'</h2><p>'+link(target,'Breakfast, dinner, dessert, drinks and an İstiklal visit guide.' if en else 'Kahvaltı, akşam yemeği, tatlı, içecek ve İstiklal ziyareti için rehberimizi okuyun.')+'</p></section>'
  # Home uses a different visual system: add a compact footer link there.
  if rel=='index.html':t=t.replace('</footer>','<!-- JOURNAL:START --><p class="business-source">'+link(target,'Taksim kahvaltı blogu ve ziyaret planları')+'</p><!-- JOURNAL:END --></footer>')
  else:t=t.replace('</main>','<!-- JOURNAL:START -->'+section+'<!-- JOURNAL:END --></main>')
  p.write_text(t);changed.append('/'+rel.removesuffix('index.html'))
# Clarify the primary tourist landing page and its existing schema/social metadata consistently.
p=R/'en/index.html';t=p.read_text();old='Turkish Breakfast in Beyoğlu · Pusula Lounge';newtitle='Turkish Breakfast in Taksim, Istanbul · Pusula Lounge'
t=t.replace(old,newtitle).replace('<h1>Turkish breakfast in Beyoğlu</h1>','<h1>Turkish breakfast in Taksim, Istanbul</h1>').replace('Welcome to Pusula Lounge, in Istanbul’s İstiklal area. Explore our breakfast options and plan a visit.','Pusula Lounge serves Van breakfast near İstiklal in Taksim, Beyoğlu. Explore shared breakfast for two, three or four guests, read the menu in Turkish lira and request a table on WhatsApp.')
t=t.replace('Explore Van breakfast at Pusula Lounge in the İstiklal area of Beyoğlu, Istanbul. Find breakfast options, menu prices and information for your visit.','Turkish breakfast in Taksim, Istanbul: explore Pusula Lounge’s shared Van breakfast, menu prices in Turkish lira, directions and WhatsApp table requests.')
p.write_text(t)
p=R/'index.html';t=p.read_text().replace('class="hero-title" aria-label="Pusula Lounge"','class="hero-title" aria-label="Pusula Lounge — Taksim, Beyoğlu’nda Van kahvaltısı"');p.write_text(t)
# Only change lastmod for pages actually changed; keep pre-existing image and hreflang metadata.
S='http://www.sitemaps.org/schemas/sitemap/0.9';X='http://www.w3.org/1999/xhtml';I='http://www.google.com/schemas/sitemap-image/1.1'
for pre,uri in [('',S),('xhtml',X),('image',I)]:ET.register_namespace(pre,uri)
tree=ET.parse(R/'sitemap.xml');root=tree.getroot();existing={u.find('{'+S+'}loc').text:u for u in root}
for path in new+changed:
 url=O+path;u=existing.get(url)
 if u is None:u=ET.SubElement(root,'{'+S+'}url');ET.SubElement(u,'{'+S+'}loc').text=url
 lm=u.find('{'+S+'}lastmod')
 if lm is None:lm=ET.SubElement(u,'{'+S+'}lastmod')
 lm.text=DATE
 if path in new:
  for child in list(u):
   if child.tag=='{'+X+'}link':u.remove(child)
  soup=BeautifulSoup((R/path.lstrip('/')/'index.html').read_text(),'html.parser')
  for a in soup.select('link[hreflang]'):ET.SubElement(u,'{'+X+'}link',{'rel':'alternate','hreflang':a['hreflang'],'href':a['href']})
  if soup.select_one('article img') and u.find('{'+I+'}image') is None:
   im=ET.SubElement(u,'{'+I+'}image');ET.SubElement(im,'{'+I+'}loc').text=O+'/assets/gallery/pusula-sofrasi-1200.webp'
ET.indent(tree,space='  ');tree.write(R/'sitemap.xml',encoding='unicode',xml_declaration=True)
# Add canonical index.html redirects for new routes; avoid broad route rewrites.
v=json.loads((R/'vercel.json').read_text());sources={x['source'] for x in v['redirects']}
for path in new:
 if path+'index.html' not in sources:v['redirects'].insert(0,{'source':path+'index.html','destination':path,'permanent':True})
(R/'vercel.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
print('Built',len(new),'TR/EN routes; linked from',len(changed),'existing pages.')
