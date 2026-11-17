# Pusula Lounge — kapsamlı SEO, yerel SEO ve GEO denetimi

**Tarih:** 17 Kasım 2026  
**Kaynak:** `tarihivankahvaltievi/pusula-lounge`, `main`  
**Canlı alan adı:** https://www.pusulalounge.com/  
**Hedef:** Taksim ve Beyoğlu'nda kahvaltı, menü, yol tarifi ve ziyaret bilgisi arayan kişileri doğru sayfaya ve doğru ziyaret adımına ulaştırmak.

## Yönetici özeti

Sitenin Google tarafından taranmasını engelleyen bir teknik hata bulmadım. Canlı sitemap'teki 46 URL'nin tamamı doğrudan `200` yanıtı veriyor; canonical ve robots metadatasında engel yok. Yerel kaynak dosyalarında 46 sayfanın tamamına ana sayfadan normal HTML bağlantılarıyla ulaşılabiliyor. Sayfalar statik HTML olarak sunuluyor; ana içerik JavaScript çalışmasına bağlı değil.

Uyguladığım somut düzeltme, tüm sayfalardaki `Restaurant` yapılandırılmış verisinde bulunan yanlış `34221` posta kodunu, Katip Mustafa Çelebi Mahallesi için kullanılan `34433` koduyla değiştirmek oldu. Kaynak `scripts/business_entity.py`; yayın çıktıları üretim aracıyla yeniden oluşturuldu. Güncel yerel çıktıda 46 Restaurant nesnesinin tamamı `34433` kullanıyor.

Yerel keşif açısından koddan daha önemli iki dış veri konusu var: Yandex kaydı Pusula Lounge'ı aynı sokakta **No:4**, site ve bağlı Google harita kimliği ise **No:3** olarak gösteriyor; site içindeki işletme saatleri için son Google kayıt kontrol tarihi **9 Ekim 2026**. Fiziksel giriş ve güncel saatler işletme sahibi tarafından doğrulanmadan bu bilgileri tahmin ederek değiştirmedim.

Google'ın güncel GEO rehberi, özel AI dosyaları veya “GEO şeması” yerine taranabilir sayfaları, erişilebilir metni, iç bağlantıları, iyi sayfa deneyimini ve özgün, güvenilir içeriği vurguluyor. Bu sitede `llms.txt` veya AI'ye özel şema eklemek için desteklenen bir gerekçe yok.

## Kapsam ve yöntem

- Güncel kaynak deposu ve `python3 scripts/build_release.py .` üretim akışı incelendi. Eski çalışma klasöründeki `site/`, `dist/` ve `seo-blog-release/` kopyaları kaynak olarak kullanılmadı.
- Canlı `robots.txt`, sitemap'teki sayfalar ve örnek bir bulunmayan URL HTTP üzerinden kontrol edildi.
- Sitemap URL'leriyle yerel dosyalar; başlık, açıklama, H1, canonical, robots, JSON-LD ve iç bağlantı grafiği karşılaştırıldı.
- Google Search Central, Google Business Profile, OpenAI tarayıcı yönergeleri, ilgili Reddit teknik SEO/yerel SEO tartışmaları ve Pusula'nın herkese açık harita/listing sonuçları incelendi.
- Bu incelemede Search Console, Google İşletme Profili sahibi paneli, GA4 veya reklam hesabından veri alınmadı. Sıralama, gerçek kullanıcı Core Web Vitals, trafik, rezervasyon ya da müşteri artışı hakkında yeni bir sonuç ileri sürülmüyor.

## Teknik tarama ve dizine eklenebilirlik

| Kontrol | Bulgular |
| --- | --- |
| Canlı sitemap | 46 benzersiz URL; tamamı kendi canonical adresinde doğrudan `200` ve HTML dönüyor; 0 yönlendirme veya kısıtlayıcı robots yönergesi |
| `robots.txt` | `200`; genel bot grubuna izin veriyor, sitemap adresini bildiriyor ve `OAI-SearchBot` için de açık izin içeriyor |
| İç bağlantılar | Yerel statik crawl'da 46/46 sitemap sayfasına ana sayfadan erişiliyor; ulaşılamayan sayfa yok |
| Meta başlık/açıklama | Yerel yayında 46/46 benzersiz; tek canonical, tek açıklama ve bir H1 mevcut |
| Yapılandırılmış veri | 46 JSON-LD bloğu geçerli JSON olarak çözümleniyor; 46 Restaurant, 46 WebSite, 46 WebPage, 42 BreadcrumbList, 18 BlogPosting, 8 FAQPage, 4 Menu ve 2 Blog nesnesi |
| Görseller | Statik HTML taramasında `alt` niteliği olmayan görsel bulunmadı |
| Bulunmayan sayfa | Canlı rastgele olmayan kontrol URL'si `404` döndü; 404 sayfası ana sayfaya yanlış `200` yönlendirmiyor |

Sitemap ve robots dosyaları taramayı destekler, ancak Google'a her URL'yi dizine alma veya sıralama garantisi vermez. Bu küçük site için “crawl budget” artırma, her botu ayrı ayrı listeleme veya ek bir sitemap katmanı kurma gereksiz. Google'ın taranabilir HTML bağlantılarını kullanması ve sitemap'i bir keşif ipucu olarak ele alması mevcut yapıyla uyumlu.

Çok dilli sayfalar dil varyantlarını HTML'de ve sitemap'te sunuyor. İleride dil eklenirse yalnızca gerçekten çevrilmiş ve o dildeki ziyaretçiye yarar sağlayan içerik yayınlanmalı; arama terimi değiştirerek aynı sayfanın kopyalarını üretmekten kaçınılmalı.

## Uygulanan adres verisi düzeltmesi

`Restaurant.address.postalCode` değeri önceki kaynakta `34221` idi. Bu değer Beyoğlu posta kodu aralığıyla uyuşmuyordu. PTT'nin posta kodu sorgu kaynağı ve aynı mahalledeki resmî Taksim Eğitim ve Araştırma Hastanesi adresi `34433` değerini destekliyor. Ortak restoran varlığındaki kod `34433` olarak düzeltildi; üretim akışı tüm 46 sayfanın JSON-LD'sini ve sitemap `lastmod` alanlarını güncelledi.

- [PTT Posta Kodu Sorgulama](https://www.ptt.gov.tr/posta-kodu)
- [Taksim Eğitim ve Araştırma Hastanesi — adres ve telefon](https://taksimeah.saglik.gov.tr/TR-968800/hizmet-binamiz.html)
- [Beyoğlu mahalleleri ve posta kodları — PTT kaynaklı mahalle tablosu](https://telefon.org.tr/il/istanbul/beyoglu/posta-kodlari)

## Yerel SEO / GEO bulguları

Google, yerel sonuçları başlıca alaka, arayan kişiye uzaklık ve bilinirlik üzerinden açıklar. Site doğru adres, telefon, saat, menü, harita ve yapılandırılmış işletme verisini sağlayabilir; arayan kişinin konumuna olan fiziksel mesafeyi kodla değiştiremez. İşletme Profili'nin doğru kategorisi, adres pini ve saatleri; gerçek yorumlar ve yerel sitelerdeki tutarlı kayıtlar site kodu dışındaki önemli işlerdir. [Google'ın yerel sıralama rehberi](https://support.google.com/business/answer/7091)

### Adres ve harita kaydı

- Site, `Katip Mustafa Çelebi Mahallesi, Küçük Parmak Kapı Sokak, Sinek Çıkmazı No:3` adresini ve Google harita Place ID'sini kullanıyor.
- [Yandex Maps'teki Pusula Lounge kaydı](https://yandex.com.tr/maps/11508/istanbul/house/ZkEYfw9iTE0HQFprfXxydH5rbA%3D%3D/) aynı sokak için No:4 gösteriyor. Yandex'in işaretlediği koordinat ile sitedeki işletme koordinatı yaklaşık 4–5 metre farkla aynı konuma düşüyor; bu, kapı numarası farkını çözmüyor.
- Harita verisini kimin güncelleyeceğine karar vermeden önce giriş tabelası, resmî işletme adresi ve gerçek Google/Yandex pinleri birlikte kontrol edilmeli. No:3 veya No:4 bilgisi tahminle siteye uygulanmamalı.
- Farklı dizinlerde mahalle adı ve posta kodu da tutarsız görünebiliyor. Nihai kaynak, işletmenin resmî adresi ve doğrulanmış işletme profili olmalı; kopya/otomatik dizin kayıtları tek tek düzeltme adayı olarak ele alınmalı.

### Saat ve hizmet bilgisi

Site, genel çalışma saatini 24 saat; kahvaltı servisini 08:00–17:00 olarak ayırıyor. Bu ayrım faydalı: genel olarak açık olmak, kahvaltının gece boyunca servis edildiği anlamına gelmiyor. Ancak bazı sayfalardaki işletme kaynağı notu Google kaydının son kontrol tarihini **2026-10-09** olarak gösteriyor. İşletme sahibi güncel genel ve özel gün saatlerini Google İşletme Profili'yle karşılaştırmalı; doğrulamadan yeni bir “son kontrol” tarihi yazılmamalı.

### Yorumlar, atıflar ve dış kaynaklar

Site Google misafir yorumlarına doğrudan bağlantı veriyor; işletmenin kendisinin seçtiği yorumlardan `aggregateRating` üretmiyor. Bu doğru yaklaşım: Google, işletmenin kendi kontrol ettiği LocalBusiness/Organization yorumlarını organik review snippet olarak göstermiyor. Dizinlerdeki yorum sayıları ve puanlar hızla değişebildiği için sitede elle sabitlenmemeli.

Yerel bilinirlikte güvenilir yerel yayın, kültür/ziyaret kaynağı, otel veya gerçek bir topluluk iş birliğinden gelen editoryal atıf; düşük kaliteli dizinlere toplu kayıt ve ücretli bağlantıdan daha sağlıklı bir hedef. Müşteri yorumları gerçek ziyaretlerden, teşviksiz ve tüm müşterilere eşit biçimde istenmeli.

## GEO ve üretken arama araştırması

Google'ın [üretken AI arama rehberi](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide) şu temelleri öne çıkarıyor: indekslenebilir SEO altyapısı, kullanıcı için yararlı ve özgün içerik, önemli bilgilerin HTML metninde bulunması, iç bağlantılar, görünür içerikle tutarlı yapılandırılmış veri, iyi görsel/video deneyimi. Google, `llms.txt`, özel AI şeması, yapay içerik parçalama veya yalnızca AI sistemleri için yeniden yazım gerektirmediğini açıkça söylüyor. Bu nedenle yeni bir AI dosyası, gizli metin veya özel “GEO hack” eklemedim.

`OAI-SearchBot` `robots.txt` içinde açıkça serbest; OpenAI bu tarayıcıyı ChatGPT arama sonuçlarında site keşfi için kullanıyor. OpenAI dokümanında `GPTBot`'un eğitim amaçlı ayrı bir tercih olduğu belirtiliyor. Mevcut genel `User-agent: * / Allow: /` kuralı, özel bir engel eklenmedikçe diğer tarayıcıları da dışlamıyor. [OpenAI tarayıcı açıklamaları](https://developers.openai.com/api/docs/bots)

### Reddit ve SEO topluluğu araştırması

- [r/TechSEO: “Technical Matters”](https://www.reddit.com/r/TechSEO/comments/1qjlz4c/technical_matters/) tartışmasında kullanıcılar robots/sitemap, iç bağlantı ve mimari, render, kırık bağlantılar ve gerçek Search Console dizine eklenme örüntülerini başlangıç kontrolü olarak sayıyor; bir diğer yorum otomatik denetim araçlarının bağlam dışı uyarılarını kovalamamayı öneriyor.
- [r/localseo: yerel SEO için altı denetim](https://www.reddit.com/r/localseo/comments/1sgs43w/i_run_6_audits_before_i-touch-anything-on-a-local/) profil kategorisi ve saatleri, web sitesi NAP uyumu, dizin kayıtları, yorumlar, rakipler ve teknik taramayı birlikte ele alıyor.
- [r/TechSEO: XML sitemap gerçekten yardımcı oluyor mu?](https://www.reddit.com/r/TechSEO/comments/1q5kcrs/is_your_xml_sitemap_actually_helping_your_seo/) sitemap'in keşfe katkısı ve dizine ekleme garantisi olmadığı konusunda farklı deneyimler içeriyor. Bu küçük sitede karar Reddit oylarına değil Google'ın birincil dokümanlarına ve canlı URL denetimine dayandırıldı.
- [r/TechSEO: Google'ın GEO rehberi üzerine tartışma](https://www.reddit.com/r/TechSEO/comments/1te4xtn/google_releases_the_official_ai_seogeo_guide/) özel AI dosyaları ve “GEO hack” söylemlerine karşı Google rehberinin altını çiziyor.
- [r/istanbul: Beyoğlu/Taksim kahvaltı önerileri](https://www.reddit.com/r/istanbul/comments/1khs9ui/breakfastbrunchlunch_spots_beyoglotaksim/) ve [İstiklal yakınında kahvaltı arayan ziyaretçi](https://www.reddit.com/r/AskTurkey/comments/1izpsej) gerçek ziyaretçilerin “yakın/kolay ulaşım”, kahvaltı tipi ve fiyat tercihiyle soru sorduğunu gösteren örnekler. Bunlar anahtar kelime hacmi, temsilî örneklem veya sıralama verisi değildir.

Reddit yorumları kullanıcı deneyimi ve SEO meslektaşlarının hipotezleri olarak değerlendirildi; kontrollü çalışma veya Google sıralama açıklaması yerine kullanılmadı. Pratik çıkarım, mevcut sayfaların ziyaretçinin gerçek sorusunu yanıtlaması ve yerel kaydın hatasız olmasıdır. Marka hakkında sahte Reddit gönderisi, yorum satın alma veya yapay atıf oluşturma önerilmiyor.

## Önceliklendirilmiş sonraki adımlar

| Öncelik | İş | Kimin verisi/işlemi gerekir? |
| --- | --- | --- |
| 1 | No:3 / No:4 fiziksel girişi, işletmenin resmî adresini, harita pinini ve 34433 posta kodunu doğrula; doğru değeri Google, Yandex ve gerçek dizinlere eşle | İşletme sahibi / adres belgesi |
| 1 | Google İşletme Profili'nde birincil kategori, telefon, genel saat, kahvaltı servisi, pin, menü bağlantısı ve masa talebi URL'sini güncel bilgiyle doğrula | Profil sahibi |
| 1 | Search Console'da güncel 46 URL sitemap'ini, indeks durumu ve Google'ın seçtiği canonical'ları incele; son üç yeni yazının keşif/dizin durumunu kontrol et | Search Console erişimi |
| 2 | Marka/marka dışı, Türkçe/İngilizce, ülke ve cihaz kırılımında gösterim, tıklama ve CTR'yi 28 günlük pencerelerle takip et; yayın/değişiklik tarihlerini not et | Search Console verisi |
| 2 | Google Business Profile ve Search Console'da gerçek kullanıcı Core Web Vitals/performans sinyali varsa mobil URL örneklerini incele; laboratuvar skorunu tek başına sıralama hedefi yapma | Search Console / CrUX |
| 2 | Menü fiyatları, servis saati ve ulaşım bilgisini kaynağında değiştiğinde site ve dış profilleri aynı anda güncelle | Güncel menü ve işletme sahibi teyidi |
| 3 | Beyoğlu/Taksim bağlamında gerçek otel, ziyaretçi danışma noktası, kültür kurumu ve yerel yayınlarla ziyaretçiye yararlı içerik/iş birliği üzerinden atıf kazan | İşletme / yerel ortaklar |

Yeni ilçe sayfaları, birbirine benzeyen ürün-şehir sayfaları, yapay anahtar kelime tekrarı veya her sayfada daha fazla şema eklemek önerilmiyor. Sitede zaten Türkçe/İngilizce ticari sayfalar, Arapça/Rusça bilgilendirme sayfaları, altı dilde rezervasyon akışı ve 18 BlogPosting bulunuyor; yeni içerik yalnızca gerçek ziyaretçi sorusunu yeni ve doğrulanabilir bilgiyle yanıtlarsa açılmalı.

## Üretim ve doğrulama

- Ortak adres kaynağı `scripts/business_entity.py` içindeki posta kodu `34433` olarak düzeltildi.
- `python3 scripts/build_release.py .` başarılı tamamlandı. 46 indexlenebilir sayfanın Restaurant JSON-LD'si güncellendi; sitemap `lastmod` değerleri üretici tarafından yenilendi. Üretim aracı font alt kümeleri ve bunların varlık bütünlük/hash kayıtlarını da tazeledi.
- Aynı üretimde altı rezervasyon sayfası mevcut dil bağlantılarıyla eşitlendi; ziyaretçiler ve tarayıcılar rezervasyon akışından diğer dil sürümlerine de geçebiliyor.
- Yerel statik incelemede: 46 benzersiz başlık, 46 benzersiz açıklama, 46 kendi canonical'ı, 46 H1, 46 çözümlenen JSON-LD bloğu, 46/46 iç bağlantıyla erişim ve 46 Restaurant nesnesinde `34433`.
- Canlı 46 URL denetimi yerel düzeltmeden önce yapıldı: `Checked 46 live sitemap URLs; 0 failed.` Kod değişikliği henüz canlıya yayımlanmadı; canlı site kontrol sonucu yeni postal code değerinin canlıda bulunduğu anlamına gelmez.
- Bu turda browser, Lighthouse/PSI, Search Console, gerçek kullanıcı CrUX veya Google İşletme Profili sahibi paneli denetimi yapılmadı. Trafik ve dönüşüm artışı ölçülmedi.

## Kaynaklar

- [Google SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide)
- [Google robots.txt rehberi](https://developers.google.com/search/docs/crawling-indexing/robots/intro)
- [Google sitemap yönergeleri](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap)
- [Google canonical yönergeleri](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls)
- [Google çok dilli sayfalar / hreflang](https://developers.google.com/search/docs/specialty/international/localized-versions)
- [Google LocalBusiness yapılandırılmış verisi](https://developers.google.com/search/docs/appearance/structured-data/local-business)
- [Google FAQ rich result değişikliği](https://developers.google.com/search/blog/2023/08/howto-faq-changes)
- [Google review snippet kuralları](https://developers.google.com/search/docs/appearance/structured-data/review-snippet)
- [Google spam politikaları](https://developers.google.com/search/docs/essentials/spam-policies)
- [Google'ın yerel sıralama açıklaması](https://support.google.com/business/answer/7091)
- [OpenAI web crawler yönergeleri](https://developers.openai.com/api/docs/bots)
