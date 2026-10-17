# Pusula Lounge: SEO, GEO, yerel görünürlük ve performans değerlendirmesi

**Tarih:** 17 Ekim 2026

**İncelenen GitHub sürümü:** `main` / `19eaa08` (`Update breakfast menu prices`)
**Canlı alan adı:** `https://www.pusulalounge.com/`

## Bu değişiklikte yapılan iş

Son menü commit'i serpme kahvaltı fiyatlarını Türkçe ve İngilizce menüde güncelliyor. Her iki URL'nin sitemap `lastmod` değeri 15 Ekim'de kalmıştı. Google, `lastmod` değerini yalnızca sayfanın önemli içeriği gerçekten değiştiğinde kullanmayı öneriyor; fiyat değişikliği bu koşulu karşılıyor. `/menu/` ve `/en/menu/` değerleri 17 Ekim 2026 olarak düzeltildi. Diğer URL'lerin tarihleri değiştirilmedi.

## Mevcut teknik SEO temeli

- `robots.txt` tüm taranabilir içeriğe izin veriyor ve kök sitemap'i işaret ediyor.
- `sitemap.xml` 15 canonical Türkçe/İngilizce sayfa içeriyor; dil alternatiflerini ve sayfa görsellerini tanımlıyor. Menü sayfalarının güncelleme tarihi bu commit'te eşitlendi.
- Sayfalarda canonical, ayrı başlık/açıklamalar, tek H1 ve karşılıklı `hreflang` bağlantıları bulunuyor. Türkçe/İngilizce içerik çiftleri tarandı; yerel bağlantı ve fragment hedeflerinde bozuk hedef çıkmadı.
- Ana sayfadaki JSON-LD `Restaurant`, `WebSite` ve `WebPage` varlıklarını birbirine bağlıyor. Menü, konum, kahvaltı ve diğer içerik sayfalarında menü/breadcrumb varlıkları, telefon, adres, harita, mutfak ve 24 saatlik işletme bilgisi yer alıyor. Sayfada görünen kahvaltı servis saatleri ayrıca 08:00–17:00 olarak belirtiliyor.
- Ziyaretçinin görebildiği içerik; adres, ulaşım, telefon, porsiyon/fiyat, alerjen uyarısı ve sık sorular gibi yerel/işlemsel niyetleri cevaplıyor. İçerik hem Türkçe hem İngilizce sunuluyor.

Google'ın resmi üretken arama rehberi özel bir “GEO işareti” şartı tanımlamıyor. AI Overviews ve AI Mode için de sayfanın Google Search'te dizine eklenebilir olması ve temel SEO/tarama koşullarını karşılaması gerekiyor. Rehber; Google Search için gerekli olmayan `llms.txt`, yapay içerik parçalama ve sahte/inauthentic mention taktiklerine zaman ayırmamayı açıkça öneriyor. Bu yüzden projeye doğrulanmamış AI dosyaları, yapay yorum şeması veya tekrar eden anahtar kelime blokları eklenmedi.

## Yerel işletme ve backlink çalışması

### Sitede hazır olanlar

- İşletme adı, tekil adres, telefon, Google işletme profili bağlantısı, çalışma ve kahvaltı saatleri site metninde bulunuyor.
- `Restaurant` şeması ile ziyaretçinin gördüğü bilgiler uyumlu tutuluyor. Google yorumlarını kopyalayıp siteye `Review` / `AggregateRating` şemasıyla eklemeyin; işletmenin kendi sitesi üzerindeki yorumlar Google'ın yerel işletmeler için review-snippet politikasına uygun bir kestirme yol değildir.
- Beyoğlu/Taksim ve İstiklal çevresine yönelik sayfalar, site içinden menü, ziyaret ve konum sayfalarına bağlanıyor.

### Hesap erişimi ve editoryal yayın gerektiren işler

Backlink, üçüncü taraf bir yayıncının kendi sitesinde vereceği bağlantıdır; Git commit'i ile üretilemez. Hesap girişi veya başka işletmeler adına yayın yapma olmadan bu değişiklik kapsamında gerçek dış bağlantı satın alınmadı, kataloglara otomatik kayıt yapılmadı ve kimseye mesaj gönderilmedi.

Önerilen sıra:

1. **Google Business Profile:** İşletme sahipliği onaylıysa ana kategori, telefon, web sitesi, doğru adres, 24 saat açık olma ve 08:00–17:00 kahvaltı servisi bilgilerini işletme panelinde teyit edin. Özel gün saatlerini gerektiğinde ayrıca güncelleyin. Sitedeki ve profildeki NAP (ad, adres, telefon) ile menü URL'si aynı olmalı.
2. **Mevcut kayıtları düzeltin:** Google, Yandex, Apple Maps, Bing Places, TripAdvisor ve RestaurantGuru gibi müşterilerin gerçekten kullandığı platformlarda tekil kayıtların adres/telefon/saatlerini karşılaştırın. Yinelenen veya yanlış kaydı düzeltin; toplu düşük kaliteli dizin kaydı açmayın. Bir dizin kaydı kendi başına editoryal backlink sayılmaz.
3. **İlgili yerel kaynaklara başvurun:** Visit Istanbul Directory'deki restoran kategorisini, yayıncının niteliği ve kayıt şartları uygunsa inceleyin; ayrıca Beyoğlu Belediyesi'nin işletme/kalite programlarının koşullarını kontrol edin. Bu kaynaklarda kayıt veya link garantisi yoktur; yalnızca işletmenin gerçek bilgileriyle başvuru yapın.
4. **Editoryal tanıtım:** İstiklal çevresindeki otel/hostel ziyaretçi rehberlerine, İstanbul gastronomi ve seyahat yayıncılarına yalnızca gerçek ziyaret veya faydalı yerel kaynak temelinde ulaşın. Önce birinci elden deneyim içeren kahvaltı rehberi/menü sayfasını önerin; bağlantı zorunlu kılmayın. Sponsorlu veya ücretli yayınlarda yayıncıdan `rel="sponsored"` (veya `nofollow`) kullanmasını isteyin.
5. **Sonuçları ölçün:** Her edinilmiş bağlantı için kaynak URL, hedef sayfa, bağlantı durumu, NAP doğruluğu, iletişim tarihi ve yönlendirme trafiğini kaydedin. Search Console bağlantı raporu ve organik performans raporunu; işletme profilindeki arama ve yol tarifi etkileşimlerini ayrı takip edin. Bağlantı adedini tek başarı ölçütü yapmayın.

**Örnek, gönderilmeye hazır olmayan kısa tanıtım metni:**

> Merhaba, Beyoğlu'nda İstiklal çevresinde hizmet veren Pusula Lounge için adres, kahvaltı saatleri ve güncel menü/fiyatları içeren ziyaretçi sayfamızı paylaşıyorum. İstanbul'da kahvaltı veya mahalle rehberi hazırlıyorsanız, okurlarınıza yararlı olacaksa bu kaynağı değerlendirmeniz için göndermek istedim. Yayın kararınız ve bağlantı biçimi tamamen editoryal tercihinizdir.

Google, sıralama amacıyla bağlantı satın almayı/satmayı, otomatik link oluşturmayı, aşırı karşılıklı bağlantıyı, düşük kaliteli dizinleri ve anchor-text'i zorlayan advertorial/guest-post kampanyalarını link spam örnekleri arasında sayıyor. Ücretli tanıtım yapılacaksa bağlantı uygun `sponsored`/`nofollow` niteliği taşımalı.

## Performans bulguları ve ölçüm

Kaynakta zaten güçlü performans önlemleri var: ilk hero görseli responsive AVIF/WebP kaynakları ve preload/fetch priority kullanıyor; aşağıdaki görseller lazy-load ediliyor; içerik `srcset` ile farklı ekran genişliklerine göre sunuluyor; fontlar yerelden WOFF2 yükleniyor; sürümlü statik dosyalar bir yıl immutable cache alıyor. Canlı yanıt örneklerinde ana sayfa Brotli, CSS Brotli ve mobil hero AVIF (yaklaşık 157 KB) döndü. Versiyonlu CSS/AVIF dosyaları 200 ve `max-age=31536000, immutable` ile yanıt verdi.

Google PageSpeed Insights API'sinden 17 Ekim'de mobil/masaüstü raporu alınmaya çalışıldı; API her iki isteğe de **HTTP 429** döndürdü. Bu nedenle bu raporda Lighthouse puanı, LCP/INP/CLS ölçümü veya “Core Web Vitals iyi” iddiası yoktur. Kod deposu tek başına gerçek kullanıcı verisini (CrUX) ya da Google Search Console raporlarını içermez.

Saha hedefleri, Core Web Vitals p75 eşiklerine göre takip edilmeli: **LCP ≤ 2,5 sn, INP ≤ 200 ms, CLS ≤ 0,1**. Search Console/PSI erişimi olduğunda önce mobil ana sayfa, `/menu/`, `/konum/` ve `/kahvalti/` raporlarını karşılaştırın. LCP sorunu varsa önce LCP alt parçasını (TTFB, kaynak bulma gecikmesi, indirme süresi, çizim gecikmesi) teşhis edin; yalnızca görseli yeniden sıkıştırmak her zaman çözüm değildir. INP/CLS sorunları varsa düşük uçlu telefon ve yavaş ağ koşullarında menü etkileşimleri, yazı tipi geçişleri ve carousel davranışını gözlemleyin.

## Yayın sonrası izleme sırası

- Search Console'da kök sitemap'in işlendiğini ve güncellenen iki menü URL'sinin canonical/dizine eklenme durumunu kontrol edin. Sitemap gönderimi bir tarama ipucudur; hemen dizine eklenme garantisi vermez.
- Rich Results Test ve URL Inspection ile ana sayfa, menü ve konum sayfasını inceleyin; işletme bilgisinin görünmesi garanti değildir.
- 2–4 hafta sonra Search Console'da marka + Beyoğlu/Taksim + Van kahvaltısı/menü sorgularının gösterim, tıklama ve CTR değişimini kaydedin; landing page'i sorgu niyetine göre iyileştirin.
- Gerçek işletme bilgileri değiştiğinde sayfadaki bilgi, JSON-LD, çeviriler ve sitemap `lastmod` aynı sürümde güncellensin.

## Kaynaklar

- [Google: Generative AI features and your website](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)
- [Google: LocalBusiness structured data](https://developers.google.com/search/docs/appearance/structured-data/local-business)
- [Google: Review snippets and self-serving business reviews](https://developers.google.com/search/docs/appearance/structured-data/review-snippet)
- [Google: Build and submit a sitemap](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap)
- [Google: Spam policies — link spam](https://developers.google.com/search/docs/essentials/spam-policies#link-spam)
- [Google: Establish your business details](https://developers.google.com/search/docs/appearance/establish-business-details)
- [web.dev: Core Web Vitals thresholds](https://web.dev/articles/defining-core-web-vitals-thresholds)
- [Visit Istanbul Directory](https://directory.visitistanbul.com/) (yayıncı/uygunluk başvurudan önce kontrol edilmeli)
- [Beyoğlu Belediyesi — Beyaz Zambak programı](https://beyoglu.bel.tr/beyaz-zambak-projesi/sertifika-sahibi-is-yerleri/)
