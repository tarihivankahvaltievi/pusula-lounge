# Pusula Lounge — kapsamlı SEO/GEO denetimi

**Tarih:** 17 Kasım 2026

**İncelenen sürüm:** `7a76033` (`main`)

**Site:** [pusulalounge.com](https://www.pusulalounge.com/)

## Sonuç

Yayınlanan site, teknik taranabilirlik ve yerel işletme sinyalleri açısından güçlü durumda. Googlebot’u engelleyen bir kural, sitemap’teki URL’lerde canonical/robots hatası, dil eşleşmesi kopukluğu, yetim sayfa veya bozuk canlı site içi varlık bulmadım. Bu nedenle bu çalışmada adres, fiyat, saat, içerik ve görünür meta etiketlerini gelişigüzel değiştirmedim. Bu bilgiler zaten işletme kaynağıyla üretiliyor ve birbirleriyle tutarlı.

Bu turdaki kalıcı teknik değişiklik, canlı SEO denetiminin yalnızca HTML sayfalarını değil, sayfa varlıklarını da kontrol etmesidir. Yeni Google Search generative AI kontrolü ve topluluk araştırmasının sonucu ayrı bir güncel rapor olarak kaydedildi. Search Console veya Google İşletme Profili hesabı gerektiren ayarlar depodan doğrulanamadı.

## İnceleme yöntemi

- Güncel GitHub `main` deposu ve statik yayın üreticileri incelendi.
- Depodaki SEO denetimleri çalıştırıldı: crawl graph, title/description/canonical, `hreflang`, XML sitemap, yerel bağlantılar, JSON-LD, menü/fiyat ilişkileri, rezervasyon yolları, CSP ve SRI.
- Canlı sitemap’teki tüm HTML URL’leri; `robots.txt`, sitemap XML’i, her sayfanın aynı kaynaklı görsel/CSS/JS varlıkları ve sitemap görselleri HTTP üzerinden kontrol edildi.
- Google Search Central’ın güncel SEO, AI arama, sitemap, yerel işletme ve uluslararası sayfa yönergeleri okundu.
- Reddit’te Taksim/İstiklal çevresi için kahvaltı arayan ziyaretçi konuşmaları ve 2026 tarihli seyahat rehberleri, ziyaretçi sorularını anlamak için incelendi. Bu küçük ve kendi kendini seçen örneklem arama hacmi, sıralama veya tüm ziyaretçilerin tercihi değildir.

## Canlı teknik bulgular

| Kontrol | Sonuç |
| --- | --- |
| Sitemap sayfaları | 46 URL; hepsi 200 HTML yanıtı, yönlendirme yok, kendine canonical ve kısıtlayıcı `noindex` yok |
| Site keşfi | Sitemap’te yinelenen URL yok; sayfalar iç bağlantı grafiğine bağlı, yetim sayfa yok |
| Tarama kuralları | `robots.txt` 200 `text/plain`; genel `User-agent: *` kuralı izin veriyor, sitemap’i doğru canonical alan adıyla bildiriyor; `OAI-SearchBot` ayrıca izinli |
| Sitemap görselleri | 111 `<image:loc>` girdisi; HTML taramasındaki 89 benzersiz aynı kaynaklı varlıkla birlikte tüm kontrol edilen kaynaklar 200 |
| Diller | 3 dört dilli sayfa grubu, altı dilde rezervasyon sayfası; HTML ve sitemap alternatifleri karşılıklı |
| Blog | 20 sitemap rotası (TR/EN blog dizinleri ve içerikleri); her içerikte breadcrumb, rezervasyon yolu ve iç bağlantı mevcut |
| Yapılandırılmış veri | 46 sayfada 212 JSON-LD düğümü; Restaurant, menü, sayfa, makale ve breadcrumb ilişkileri mevcut |
| Menü | 76 menü maddesi ve 84 fiyat teklifi; kaynak menüden türetme ve fiyat tutarlılığı kontrolleri geçti |
| Alan adı | HTTP ve `pusulalounge.com` ana sayfası 308 ile `https://www.pusulalounge.com/` adresine gidiyor |

`check_live_indexability.py` artık `robots.txt`/sitemap HTTP yanıtı ve MIME türünü; canonical host’taki sayfa URL’lerini; sitemap görsellerini ve taranan sayfalarda kullanılan aynı kaynaklı `img`, `srcset`, stylesheet, preload, script ve ikonları denetliyor. Yayınlı kontrolde 46 sayfa ve 89 varlıkta hata çıkmadı. XML sitemap içinde 111 görsel girdisi var; tekrar eden görseller HTTP isteği için tekilleştiriliyor.

Site kaynağındaki diğer kontroller de geçti: uluslararası SEO, altı dilde rezervasyon, arama içeriği, yerel harita/varlık ilişkileri ve menü bütçe karşılaştırmaları. Bu yerel kontroller gerçek Google dizin durumunu, zengin sonuç uygunluğunu veya sıralamayı ölçmez.

## Google yönergelerinden çıkan kararlar

Google’ın [SEO başlangıç rehberi](https://developers.google.com/search/docs/fundamentals/seo-starter-guide) ve [sitemap açıklaması](https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview) sitemap’i URL keşfi için yararlı bir sinyal olarak tanımlar; listedeki her URL’nin taranacağını veya indeksleneceğini garanti etmez. Site sitemap’te 46 URL içeriyor; bu ölçekte “crawl budget” müdahalesi veya tüm URL’ler için elle yeniden tarama isteği gerekmez. Önemli URL’ler zaten menüler ve içerik bağlantılarıyla bulunabiliyor.

[Çok dilli sayfa yönergesine](https://developers.google.com/search/docs/specialty/international/localized-versions) göre varyantlar kendilerini ve birbirlerini göstermeli; doğru dil kodu, tam URL ve karşılıklı bağlantı önemlidir. Mevcut dil grupları bu kuralları denetleyen kontrolü geçiyor. Her içeriği yapay olarak altı dile genişletmek yerine, yalnızca gerçekten çevrilmiş ve o ziyaretçiye yararlı olan sayfalar eşlenmiş durumda.

İşletme varlığı sayfalarda `Restaurant` türüyle; adres, telefon, koordinat, saat, menü, harita profili ve sosyal profil ilişkileriyle tanımlanmış. Google’ın [LocalBusiness belgeleri](https://developers.google.com/search/docs/appearance/structured-data/local-business) en özgül işletme tipini ve sayfada görünen bilgilerle uyumu öneriyor. Site kendi yorumlarını `aggregateRating` olarak işaretlemiyor. İşletme sahibinin kontrolündeki yorumlar için sahte yıldız verisi eklemek doğru olmaz.

Google’ın 10 Temmuz 2026 tarihli [üretken AI arama rehberi](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide) people-first, özgün ve faydalı içeriği; teknik taranabilirliği; görünür metinle aynı yapılandırılmış veriyi; Search Console ölçümünü vurguluyor. Google, `llms.txt`, AI’ye özel schema, yapay içerik parçalama, her sorgu varyasyonu için ayrı sayfa veya sahte çevrimiçi mention çalışmalarının Google Search’te özel görünürlük sağlamadığını açıkça söylüyor. Bu yüzden bu taktikler eklenmedi.

### Yeni hesap düzeyindeki GEO kontrolü

Google’ın [Search generative AI kontrolü](https://support.google.com/webmasters/answer/16908024) 31 Ağustos 2026 itibarıyla tüm sitelere açıldı. AI Overviews/AI Mode’a kaynak ve bağlantı olarak dahil edilmek için doğrulanmış Search Console mülkünün bu özelliklere dahil olması gerekiyor. Google’ın yardımına göre varsayılan tüm mülkler dahil; ancak mülk sahibi kendi ayarını değiştirmiş veya bir üst mülkten hariç tutulan ayarı devralmış olabilir. Bu seçim HTML, `robots.txt` veya GitHub deposundan okunamıyor.

Search Console sahibi `Settings → Search generative AI` bölümünde `Include my site's links and content` seçimini veya üst mülkten gelen devralma durumunu kontrol etmeli. Site zaten dahil görünüyorsa kod tarafında ekstra bir dosya/etiket gerekmez. Google’ın [Generative AI performance report](https://support.google.com/webmasters/answer/16984139) raporu 31 Ağustos 2026’dan beri küresel kullanıma açık; az gösterimi olan mülklerde rapor görünmeyebilir. Gerçek gösterim, sayfa, ülke ve cihaz performansı yalnızca mülk hesabından incelenebilir.

Google’ın genel [AI özellikleri açıklaması](https://developers.google.com/search/docs/appearance/ai-features) de indekslenebilirliği, metin olarak erişilebilen içeriği, iç bağlantıları, sayfa deneyimini, görünür içerikle uyumlu schema’yı ve güncel Business Profile bilgisini vurguluyor. Teknik uygunluk yayınlanma veya gösterilme garantisi değildir.

## Topluluk ve ziyaretçi niyeti araştırması

- [r/AskTurkey: İstiklal yakınında, yaklaşık 15 dakika yürüme mesafesinde uygun fiyatlı kahvaltı arayışı](https://www.reddit.com/r/AskTurkey/comments/1izpsej/good_place_to_eat_breakfast_next_to_istiklal/) bir kullanıcının aynı anda bütçe ve yürünebilir mesafeyi sorduğu eski bir örnek. Bu, fiyatı ve doğrulanmış adres/yol bilgisini ayrı ayrı bulmayı kolaylaştırmanın önemini gösteriyor; belirli bir işletme için güncel fiyat veya süre kanıtı değildir.
- [r/istanbul: Beyoğlu/Taksim’de kahvaltı, brunch ve öğle yemeği seçenekleri](https://www.reddit.com/r/istanbul/comments/1khs9ui/breakfastbrunchlunch_spots_beyoglotaksim/) önerileri öğün türü, bütçe ve çevre semt ayrımına göre veriyor. Bu, genel “en iyi restoran” metni yerine ziyaretçinin ne yiyeceğini ve hangi deneyimi istediğini açıklamanın yararlı olduğuna işaret ediyor.
- [r/istanbul: İstanbul’da sabah 07:00–10:00 arasında ne yapılabileceği](https://www.reddit.com/r/istanbul/comments/1vu5nyl/what_can_i_realistically_do_in_istanbul_between_7/) gibi yeni seyahat soruları saat planlamasını öne çıkarıyor. Sitedeki genel açık olma saati ile kahvaltı servis saatinin ayrı açıklanması bu niyet için önemlidir.
- [2026 Taksim kahvaltı rehberi](https://taketravelinfo.com/best-breakfast-in-taksim-for-tourists/) ziyaretçinin serpme sofra, menemen, hızlı simit/börek, konum ve değişebilen fiyat/saatler arasında seçim yaptığını anlatıyor. Rakip veya üçüncü taraf rehberindeki bilgiler Pusula’nın menü verisi olarak kullanılmadı.

Bu örnekler anekdottur; Reddit kullanıcılarını SEO mention’ı veya bağlantı almak için hedeflemek anlamına gelmez. Google’ın AI rehberi inauthentic mention arayışına karşı uyarıyor. Gerçek ziyaretçi soruları, menüde yayımlanan içerik ve fiyat, servis saati, adres, yön tarifi ve masa talebi sayfalarıyla yanıtlanmalı; bulunmayan mesafe, alerjen, ödeme veya ürün bilgisi uydurulmamalı.

## Takip edilmesi gereken işler

1. **Search Console:** Doğrulanmış mülkte generative AI kontrolünün dahil olduğuna bakın. Sitemap raporu, URL Inspection ve Page Indexing raporuyla ana sayfa, `/menu/`, `/kahvalti/` ve `/konum/` sayfalarını kontrol edin. İndeks ve gösterim verisi bu çalışma ortamında yok.
2. **AI ve organik performans:** Yeterli veri biriktiğinde Search Console AI performans raporunda sayfa/ülke/cihaz kırılımını; normal Web performans raporunda marka dışı sorgu ve CTR’yi inceleyin. Günlük snippet veya tek arama örneğini sıralama ölçüsü saymayın.
3. **Google İşletme Profili:** Sahip, gerçek pin/giriş, işletme adı ve kategorisi, telefon, saatler, menü ve masa talebi URL’sini web sitesiyle karşılaştırmalı. Google’ın yerel sıralama açıklaması alaka, mesafe ve bilinirliği ayırır; site kodu arayan kişinin mesafesini veya dışarıdaki bilinirliği değiştiremez. [Google yerel sıralama açıklaması](https://support.google.com/business/answer/7091?hl=en).
4. **Performans:** Bu turda PageSpeed/CrUX alan verisi alınmadı. Güncel mobil LCP/INP/CLS için Search Console Core Web Vitals ve PageSpeed Insights kullanın; kaynak kod denetimi gerçek kullanıcı metriği değildir.
5. **İçerik:** Fiyat, saat, rota veya kurum çalışma takvimi değiştiğinde birincil işletme/kurum kaynağını kontrol edin ve yalnızca gerçek değişiklikte sayfa, schema ve sitemap `lastmod` alanını birlikte güncelleyin. Daha fazla benzer bölge sayfası yayınlamadan önce Search Console’da sorgu ve talep olduğunu doğrulayın.

## Doğrulamanın sınırları

Bu çalışma Google Search Console, Google Business Profile, GA4 veya Bing Webmaster hesabına bağlı değildi. Dolayısıyla indekslenme, AI kontrolünün gerçek seçimi, arama sorguları, tıklamalar, yerel sıralama, Business Profile tutarlılığı, rezervasyon dönüşümü ve güncel CrUX Core Web Vitals hakkında iddia yoktur. Reddit ve seyahat rehberi örnekleri nitel ziyaretçi araştırmasıdır; hacim veya sıralama verisi değildir.

## Başvurulan kaynaklar

- [Google Search SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide)
- [Google AI Search optimization guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)
- [Google AI features and your website](https://developers.google.com/search/docs/appearance/ai-features)
- [Search generative AI control — Search Console Help](https://support.google.com/webmasters/answer/16908024)
- [Generative AI performance report — Search Console Help](https://support.google.com/webmasters/answer/16984139)
- [Google sitemap overview](https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview)
- [Google localized versions and hreflang](https://developers.google.com/search/docs/specialty/international/localized-versions)
- [Google LocalBusiness structured data](https://developers.google.com/search/docs/appearance/structured-data/local-business)
- [Google Business Profile local ranking](https://support.google.com/business/answer/7091?hl=en)
- [r/AskTurkey breakfast near İstiklal](https://www.reddit.com/r/AskTurkey/comments/1izpsej/good-place-to-eat-breakfast-next-to-istiklal/)
- [r/istanbul breakfast/brunch recommendations](https://www.reddit.com/r/istanbul/comments/1khs9ui/breakfastbrunchlunch_spots_beyoglotaksim/)
- [r/istanbul early-morning itinerary question](https://www.reddit.com/r/istanbul/comments/1vu5nyl/what_can_i_realistically_do_in_istanbul_between_7/)
- [Taksim breakfast travel guide (2026)](https://taketravelinfo.com/best-breakfast-in-taksim-for-tourists/)
