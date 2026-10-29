# Pusula Lounge: SEO, GEO ve müşteri kazanımı araştırması

29 Ekim 2026 · İncelenen başlangıç: `34104e0` · Hedef: nitelikli arama ziyareti → menü inceleme → masa talebi → işletme tarafından onaylanan ziyaret.

## Araştırmanın kapsamı ve sınırı

Canlı alan adı, 40 canonical sayfa, HTML içerikleri, üretim kaynakları, menü fiyatları, iç bağlantılar, sitemap, dil alternatifleri ve güvenlik başlıkları incelendi. Web araştırmasında “Pusula Lounge”, “Taksim serpme kahvaltı”, “Taksim kahvaltı menü fiyat” sorguları ve resmî arama motoru belgeleri kullanıldı. Sonuçlar bir arama örneklemidir; Google sıralama takibi veya arama hacmi ölçümü değildir. Search Console, Bing Webmaster Tools ve Google İşletme Profili hesaplarına erişilmedi. Mevcut tıklama, CTR, dönüşüm ve müşteri sayısı bilinmiyor; artış yüzdesi vaat edilmez.

## Bulgular ve uygulama kararları

| Bulgu | Müşteri açısından etkisi | Yapılan işlem |
| --- | --- | --- |
| Kahvaltı sayfası porsiyonları anlatıyor, fiyat için başka sayfaya gitmek gerekiyordu. | Bütçe ve seçenek değerlendirmesi uzuyordu. | TR/EN sayfalarda girişin hemen ardından üç porsiyonun menü fiyatı, servis saati, çay kapsamı ve masa talebi. |
| Menü ve kahvaltı başlıkları ağırlıklı Beyoğlu odaklıydı. | Taksim’de arayan kişi sayfanın ihtiyacını karşıladığını daha zor anlayabilir. | Menü, kahvaltı ve konum için altı özgün, niyeti belirgin başlık/açıklama; sosyal ve WebPage verileriyle eşleşme. Bu bir CTR hipotezidir. |
| Bilgi yazılarından ticari kahvaltı sayfasına bağ zayıftı. | Okur içerikten seçenek karşılaştırmasına geçemeyebilir. | On TR/EN yazıda kahvaltı porsiyon/fiyat bölümüne bağlamsal bağlantı. |
| Çalışma klasöründeki son görsel metadata düzeltmeleri yayın deposuna alınmamıştı. | Blog kapağı ile WebPage/görsel sitemap bilgisi ayrışabiliyordu. | Finalizer üretim zincirine alındı: gerçek içerik görselleri, dil ilişkileri ve makale ilişkileri son HTML’den türetiliyor. |
| Eski üreticiler sabit lastmod tarihleri yazıyordu. | Site haritasındaki güncellik sinyali gerçek değişiklikle örtüşmeyebilir. | Son çıktı aynıysa eski lastmod korunur; değişen sayfa İstanbul tarihini alır. |
| Yandex arama örneğinde Küçük Parmak Kapı Sok. 4; sitede Sinek Çıkmazı No:3 görülüyor. | Adres belirsizliği ziyaret ve yerel keşfi zorlaştırabilir. | Site adresi korunuyor; harici kayıt düzeltmesi hesap işi olarak aşağıda ayrıldı. |
| Etkileşim kodu yalnız tarayıcı içi olay yayımlıyor; analitik servise veri göndermiyor. | Mevcut kod tek başına trafik/dönüşüm raporu üretmez. | Ölçüm planı açıkça belgelendi; gerçek analitik entegrasyonu yapılmış gibi raporlanmadı. |

## Rekabet ve arama niyeti

[Kardeşler’in kendi kahvaltı sayfası](https://www.kardeslercihangir.com/turkish-breakfast-cihangir) porsiyon, fiyat, kahvaltı servis saati ve ulaşımı aynı sayfada anlatıyor. Buradan çıkarım: ziyaretçinin sipariş öncesi sorularını tek yerde yanıtlamak yararlı bir karşılaştırma standardı. Rakibin fiyatı veya “rezervasyonsuz” politikası Pusula’ya taşınmadı.

[Tarihi Van Kahvaltı Evi’nin kendi menüsü](https://www.tarihivankahvaltievi.com/menu) ürün içeriği, porsiyon ifadesi ve fiyatı birlikte gösteriyor. Pusula’nın ayrı 2/3/4 kişilik porsiyonları ve serpme içindeki çay bilgisi kendi menü kaynağından görünür hale getirildi. Rakip fiyatlarını kullanarak ucuzluk/üstünlük iddiası yapılmadı.

[Pusula’nın Restaurant Guru kaydı](https://de.restaurantguru.com/pusula-lounge-Istanbul) marka, telefon ve Sinek Çıkmazı No:3 adresini ilişkilendirirken [Yandex kaydı içeren sonuç](https://yandex.com.tr/maps/11508/istanbul/house/kucuk_parmak_kapi_sok_no_2/ZkEYfw9iTUcAQFprfXxydHhnYQ%3D%3D/) farklı kapı numarası gösteriyor. Bunlar üçüncü taraf gözlemleridir; yorumlar, puanlar, dışarıdan bulunan fiyatlar veya hizmet iddiaları siteye kopyalanmadı.

| Sorgu ailesi / niyet | Ana hedef | Beklenen ziyaretçi eylemi |
| --- | --- | --- |
| pusula lounge / pusula taksim | `/` | Menü veya konum |
| taksim serpme kahvaltı / van kahvaltısı beyoğlu | `/kahvalti/` | Porsiyon karşılaştırma, masa talebi |
| taksim kahvaltı menüsü / serpme kahvaltı fiyatları | `/menu/` | Gerçek içerik ve fiyatı inceleme |
| turkish breakfast taksim / van breakfast istanbul | `/en/breakfast/` | İngilizce seçenek karşılaştırma |
| breakfast menu taksim prices | `/en/menu/` | TRY fiyatları ve içerik |
| pusula lounge adres / istiklal yol tarifi | `/konum/`, `/en/location/` | Harita veya telefon |
| serpme nedir / çay dahil mi / kaç kişilik | Mevcut rehberler ve ilgili blog yazıları | Bilgiden kahvaltı sayfasına geçiş |

Bunlar ölçülmüş yüksek hacimli anahtar kelimeler değildir; içerik ve örnek arama sonuçlarından çıkarılan niyet gruplarıdır. Aynı niyete yönelik çok sayıda benzer semt sayfası açılmadı. Ana menü fiyatı ticari kaynak, blog ise açıklayıcı içerik olarak kaldı.

## GEO için dayanaklar

[Google AI özellikleri rehberi](https://developers.google.com/search/docs/appearance/ai-features) normal SEO temellerini, taranabilirliği, metin içeriğini ve görünür içerikle tutarlı yapılandırılmış veriyi esas alır. Özel bir “AI schema” gerekmez. [Google’ın üretken AI rehberi](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide) de kullanıcıya özgün değer sunmaya odaklanır. Bu nedenle bu turda llms.txt veya yapay anahtar kelime blokları eklenmedi.

[Başlık rehberi](https://developers.google.com/search/docs/appearance/title-link) ve [snippet rehberi](https://developers.google.com/search/docs/appearance/snippet) doğrultusunda başlıklar sayfa niyetine göre ayrıldı. Google başlık/açıklamayı yeniden seçebilir; yazılan metnin arama sonucunda aynen görünmesi garanti değildir.

[İç bağlantı rehberine](https://developers.google.com/search/docs/crawling-indexing/links-crawlable) uygun gerçek `a href` bağlantıları kullanıldı. Yeni fiyat ve eylem içeriği JavaScript gerektirmeyen HTML’dir.

[LocalBusiness rehberi](https://developers.google.com/search/docs/appearance/structured-data/local-business) açısından mevcut Restaurant kimliği, telefon ve adres korunuyor. Sitede olmayan hizmet, puan veya sertifika eklenmedi. [Sitemap rehberi](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap) ve [görsel SEO rehberi](https://developers.google.com/search/docs/appearance/google-images) kapsamında gerçek görseller ile son sayfa çıktısı eşleştirildi.

## Hesap erişimiyle yapılacak müşteri kazanımı işleri

Öncelik 1 — [Google İşletme Profili](https://support.google.com/business/answer/7091?hl=en): gerçek işletme adı, en uygun mevcut kategori, telefon, harita pini, giriş adresi, web menüsü ve rezervasyon bağlantısı kontrol edilmeli. Genel açık saat ile kahvaltı servisi karıştırılmamalı. Yandex’teki adres işletme sahibi tarafından teyit edilerek düzeltilmeli. Yerel görünürlük konuma, alaka düzeyine ve bilinirliğe bağlıdır; site kodu tek başına bunların tamamını değiştirmez.

Öncelik 2 — Search Console: canonical `https://www.pusulalounge.com` mülkünde sitemap teslimi, ana hedef URL’lerin dizin durumu ve ülke/cihaz/sorgu kırılımı kontrol edilmeli. Depoda doğrulama dosyasının olması hesap erişimi veya başarılı dizine eklenme kanıtı değildir.

Öncelik 3 — Gerçek ziyaretlerden işletme geri bildirimi: ekip “bizi nereden buldunuz?” yanıtını ve onaylanan masa/gerçekleşen ziyaret sayısını toplu olarak kaydetmeli. Ödüllü/sahte yorum veya yapay backlink çalışması önerilmez.

Öncelik 4 — Analitik: mevcut `pusula:interaction` olayları menü, rezervasyon sayfası, WhatsApp açma, telefon ve harita tıklamasını ayırt ediyor. Bir analitik hesabı ve gerekli veri tercihleriyle entegrasyon kurulmadan bu olaylar kalıcı raporlanmıyor. İsim, telefon, not, WhatsApp mesajı ve rezervasyon tarihi analitiğe gönderilmemeli. WhatsApp açılması, mesajın gönderildiği veya masanın kesinleştiği anlamına gelmez.

## 28 günlük ölçüm planı

Başlangıç dönemi: 1–28 Ekim 2026; yayın sonrası tam dönem: 30 Ekim–26 Kasım 2026. Dönemler aynı sayıda gün içerir. Mevsimsellik, tatiller, kampanyalar ve sıralama değişimi nedeniyle fark tek başına bu sürüme atfedilemez.

1. Search Console’dan hedef URL, sorgu, ülke ve cihaz bazında gösterim, tıklama, CTR ve ortalama konumu dışa aktarın. Marka ve marka dışı sorguları ayrı değerlendirin.
2. Gösterim var, CTR düşükse başlık/sayfa vaadini inceleyin; gösterim yoksa önce dizin ve sorgu uyumunu kontrol edin. Tüm başlıkları her hafta değiştirmeyin.
3. Analitik kurulunca açılış sayfası başına menü ve masa talebi geçişlerini izleyin. Başarıyı yalnız sayfa görüntüleme ile tanımlamayın.
4. Onaylanan rezervasyon ve gerçekleşen müşteri sayısını işletme kayıtlarıyla ayrı ölçün. Tıklama müşteriye eşit değildir.
5. [Bing AI Performance](https://www.bing.com/webmasters/help/ai-performance-9f8e7d6c) hesabında mevcutsa alıntılanan sayfa ve sorgu eğilimlerini kontrol edin. AI alıntısı trafik veya satış sayılmaz. Google AI görünürlüğü için hesapta sunulan Search Console raporlarını kullanın; bir sohbet denemesini sıralama ölçümü saymayın.

## Teknik doğrulama

40 sayfada canonical, hreflang, iç bağlantı/fragment, robots, yapılandırılmış veri, SRI ve CSP kontrolleri; dört dilde 84 fiyat teklifi; altı dilde rezervasyon doğrulaması ve kişisel veri içermeyen olay kontrolleri geçti. Dört ekran genişliğinde 160 sayfa kontrolü ve dört dilde 16 ulaşım akışı kontrolü geçti. Görsel metaveri kontrolü 81 sitemap görsel kaydını doğruladı. Yeniden üretim son HTML ve sitemap çıktısını değiştirmedi. Fiyat değişikliği geçici test kopyasında iki dildeki kahvaltı sayfasına doğru yansıdı.

Eski rezervasyon testleri mevcut siteyle uyumsuzdu: VM’de URLSearchParams yoktu; bazı dillerde eski başlık ve soru adedi bekleniyordu. Test ortamı ve beklentiler mevcut görünür içerikle eşleştirildi; rezervasyon uygulama davranışı değiştirilmedi.

Bu kontroller yerel teknik doğrulamadır; gerçek kullanıcı Core Web Vitals, arama sıralaması veya trafik artışı ölçümü değildir.
