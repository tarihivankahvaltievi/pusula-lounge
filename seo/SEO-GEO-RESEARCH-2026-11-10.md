# Pusula Lounge — SEO ve GEO araştırması

**Tarih:** 10 Kasım 2026

**İncelenen başlangıç sürümü:** `5135976` (`main`)

**Hedef:** Taksim/Beyoğlu’nda kahvaltı veya ziyaret bilgisi arayan kişiyi doğru dildeki sayfaya, güncel menüye, konuma ve onaylı masa talebine ulaştırmak.

## Yönetici özeti

Site, temel teknik SEO ve çok dilli keşfedilebilirlik açısından sağlam bir tabana sahip. Bu incelemede 40 sitemap URL’si, 14 blog rotası, 182 JSON-LD nesnesi ve örnek canlı sayfalar denetlendi. Canonical, indexlenebilirlik, karşılıklı dil alternatifleri, menü fiyatlarının sayfalar arası üretimi ve iç bağlantılar için çalışan kontroller hata vermedi.

Yeni bulunan somut sorun, güncel menü fiyatlarını kaynaktan alan serpme kahvaltı karşılaştırma yazısının tablo başlığında ve güncellenme meta bilgisinde 27 Ekim tarihinin kalmış olmasıydı. Menü ve yazıdaki fiyatlar aynı olsa da ziyaretçiye gösterilen tarih doğru değildi. Türkçe ve İngilizce yazılar artık tarihi olmayan, menünün kendisini kaynak gösteren tablo başlığı kullanıyor; görünür güncellenme tarihi, `dateModified`, `article:modified_time` ve sitemap `lastmod` aynı değişiklikle eşleşiyor. Akşam yemeği yazısındaki `article:modified_time` tutarsızlığı da düzeltildi.

“Google’da en üst sıra” veya belirli bir AI yanıtında görünme teknik bir değişiklikle garanti edilemez. Google’ın yerel sonuçları alaka, arayanla mesafe ve bilinirlik; organik sonuçları da sayfa düzeyinde pek çok sinyal üzerinden belirlenir. Mesafeyi site koduyla değiştiremeyiz; profil kalitesi, gerçek yerel bilinirlik, özgün ve doğru içerik, ölçüm ve kullanıcı deneyimi üzerinde çalışabiliriz.

## Araştırma yöntemi ve kapsam

- GitHub yayın deposundaki sürüm ve üretim zinciri incelendi: statik HTML, Python üreticileri ve `python3 scripts/build_release.py .`.
- Sitemap’teki 40 sayfanın HTML metadatası kontrol edildi: başlık, açıklama, canonical ve indexlenebilir robots kuralı.
- Mevcut SEO doğrulayıcıları çalıştırıldı: hreflang/sitemap eşleşmeleri, yerel bağlantılar, içerik ve menü ilişkileri, 6 dilde rezervasyon sayfaları, JSON-LD görünür metin uyumu, SRI/CSP ve fiyat üretimi.
- Canlı ana sayfa, Türkçe/İngilizce menüler, fiyat rehberi, sitemap ve `robots.txt` HTTP ile açıldı; örneklenen URL’ler `200` döndürdü.
- Kamuya açık işletme profilleri ve `@pusulalounge` Instagram profili karşılaştırıldı. Bu örnekler alan adı dışı sıralama ölçümü sayılmadı.
- Google Search Central ve Google Business Profile’ın resmi yönergeleri okundu. Güncel Search Console, GA4 veya işletme sahibi paneli bu incelemede bağlı değildi; bu nedenle yeni trafik, sorgu, indekslenme, yerel sıralama veya gerçek rezervasyon ölçüsü raporlanmıyor.
- PageSpeed Insights API bu incelemede kota nedeniyle `429` döndürdü; güncel PSI/CrUX ölçümü alınamadı.

## Bulgular

### 1. Teknik taban iyi; dizine girmek yine de garanti değil

40 sitemap URL’si için her sayfada tekil başlık, açıklama, kendine canonical ve indexlenebilir robots yönergesi mevcut. `check_tourism_seo.py` 40 sayfayı ve 182 yapılandırılmış veri nesnesini taradı; canonical, hreflang karşılıklılığı, yerel bağlantı/fragment, yetim sayfa, JSON-LD, SRI ve CSP hatası bulmadı. Altı yerel rezervasyon yolu da kendi kontrollerinden geçti.

Bu sonuç Google’ın sayfaları gerçekten dizine aldığı veya belirli bir sorguda göstereceği anlamına gelmez. URL Inspection ve dizin raporu yalnızca Search Console’daki mülkten doğrulanabilir. Google, teknik şartları karşılamanın taranma, dizine eklenme veya gösterilme garantisi olmadığını açıkça belirtiyor.

### 2. Güncel fiyatın eski tarih etiketi güveni zedeliyordu

Serpme kahvaltı yazısındaki fiyat tablosu yayınlanan Türkçe menüden üretiliyor; kişi başı rakam ayrıca satılan bir teklif olarak sunulmuyor. Canlı menü ve yazı fiyatları eşleşiyordu. Fakat yazıdaki tablo başlığı “27 Ekim 2026” diyordu ve bazı Open Graph `article:modified_time` alanları, görünür/JSON-LD güncelleme tarihinden farklıydı. Bu, okuyucuya hangi fiyatın güncel olduğu konusunda gereksiz belirsizlik veriyordu.

Artık tablo menünün kendisini kaynak gösteriyor; karşılaştırma yazısı son gerçek içerik kontrolünü 10 Kasım 2026 olarak gösteriyor. Üretici yazının görünür güncelleme metnini, JSON-LD `dateModified` ve `article:modified_time` değerlerini birlikte üretiyor. Bu tarihi her içerik değişikliğinde elle doğru tutmak gerekir; sırf arama motoruna güncel görünmek için tarihi değiştirmeyin.

### 3. Çok dilli mimari doğrulanıyor

40 sitemap kaydı içinde HTML alternatifleri ve sitemap `hreflang` bağlantıları birbiriyle eşleşiyor; karşılıklılık kontrolü başarılı. Türkçe/İngilizce içeriklerin yanında Rusça/Arapça ana, menü ve konum sayfaları ile altı dilde rezervasyon sayfaları korunuyor. Google, alternatiflerin her varyantta kendisini ve diğer dil varyantlarını listelemesini öneriyor; mevcut kontrol bu kuralı doğruluyor.

Yeni dil veya benzer lokasyon sayfası yalnızca gerçek, çevrilmiş ve o kullanıcıya özgü fayda varsa eklenmeli. Aynı içeriği farklı arama ifadeleriyle çoğaltmak hem kullanıcıya değer sağlamaz hem de Google’ın ölçekli içerik kötüye kullanımı politikasına yaklaşabilir.

### 4. GEO için ayrı bir “AI schema” gerekmiyor

Google’ın AI Overviews / AI Mode yönergeleri standart SEO temellerini vurguluyor: taranabilir sayfalar, iç bağlantı, önemli bilgilerin metin olarak bulunması, iyi sayfa deneyimi, yüksek kaliteli görsel ve görünür içerikle eşleşen yapılandırılmış veri. Google, özel AI dosyalarının, `llms.txt`’nin, yapay “chunking” yaklaşımının veya özel GEO şemasının Google Search görünürlüğünü artırdığını söylemiyor.

Mevcut sayfalar menü, porsiyon, fiyat, adres, saat, yön tarifi ve masa talebini metin olarak veriyor; Restaurant, Menu, WebPage, BlogPosting ve Breadcrumb verileri sayfalarla ilişkilendirilmiş. İşletmenin kendi yorumları için `aggregateRating` eklenmemesi doğru: Google, işletmenin kontrol ettiği kendi LocalBusiness yorumları için yıldızlı review snippet göstermiyor.

Bu turda kamuya açık Instagram profili `@pusulalounge` doğrulandı. Profil adı Pusula Lounge/Taksim kahvaltısı olarak geçiyor; profili aynı işletmenin web sitesi, telefonu ve No:3 adresiyle eşleştiren işletme listelemesi de bulundu. Restaurant varlığına profil için `sameAs` eklendi; bu Google’a işletme kimliği için ek bir kaynak sunar, tek başına sıralama yükseltme vaadi değildir. Kamuya açık Yandex kaydında kapı numarası `4`, sitede `3` görünüyor. Giriş numarası ve harita pini işletme sahibi tarafından doğrulanana kadar sitedeki adres değiştirilmedi.

### 5. Yerel sıralamanın önemli kısmı site dışındadır

Google, yerel sonuçlarda alaka, mesafe ve bilinirliği temel faktörler olarak açıklıyor. Sitedeki açık adres, telefon, saat, menü ve konum bu bilgilerin anlaşılmasına yardım eder; arayan kişinin konumuna olan mesafeyi veya internetteki bağımsız bilinirliği değiştirmez.

İşletme sahibi Google İşletme Profili’nde pin/giriş, gerçek işletme adı ve kategorisi, telefon, genel çalışma saati, ayrı kahvaltı servisi, menü ve masa talebi bağlantılarını kontrol etmeli. Web sitesindeki son kaynak kontrol notu 9 Ekim 2026 tarihli; bu çalışma Google işletme sahibi panelinde saatleri yeniden doğrulamadı. Profil düzeltmeleri bu nedenle kod değişikliği olarak taklit edilmedi.

Yerel bilinirlik için öncelik, gerçek müşteri geri bildirimi, tutarlı işletme bilgileri ve Beyoğlu/Taksim bağlamında gerçek editoryal/kurumsal atıflardır. Yorum isteği tüm müşterilere tarafsız ve teşviksiz yapılmalı; yalnızca memnun müşterilerden yorum seçmek veya ödül vermek Google politikasına aykırıdır.

## Yapılan değişiklikler

- Türkçe ve İngilizce serpme kahvaltı fiyat karşılaştırmasının eski tarihli tablo başlığı kaldırıldı; tablo fiyatların yayınlanan Pusula menüsünden geldiğini belirtiyor.
- Aynı iki yazıda 10 Kasım 2026 gerçek güncelleme tarihi görünür ve yapılandırılmış `dateModified` olarak gösteriliyor.
- Blog üreticisi `article:modified_time` değerini artık yazının gerçek `dateModified` alanından alıyor. Akşam yazısının önceden var olan tarih farklılığı da böylece giderildi.
- Değişen sayfaların sitemap `lastmod` değerleri içerik değişikliğiyle güncellendi. Fiyat tablosu menü kaynağından üretildiği için menü rakamları değişirse bu karşılaştırma da yeniden üretimde güncellenir.
- Son metadata üreticisi, doğrulanan `@pusulalounge` profilini 40 sayfadaki `Restaurant.sameAs` listesine ekliyor. İşletme varlığı bütün yerel sayfalarda aynı dış profille ilişkilendiriliyor.

## Sonraki 30 gün için öncelikler

1. **Google İşletme Profili:** Sahip erişimiyle gerçek kategori, adres/pin, telefon, saatler, kahvaltı servisi, menü ve masa talebi URL’sini doğrulayın. Çalışma saatini profil ile site arasında aynı gerçek hizmeti anlatacak biçimde tutun.
2. **Search Console:** Sitemap ve ana ticari URL’lerin URL Inspection/dizin durumunu gözden geçirin. Sorguları marka / marka dışı; sayfaları kahvaltı, menü, konum ve rezervasyon gruplarında; ülke, dil ve cihaz kırılımında izleyin. Gösterim, tıklama ve CTR’yi birlikte değerlendirin; ortalama konumu tek başına hedef olarak kullanmayın.
3. **Ölçüm:** Pusula’ya ait, yetkili bir GA4 mülkü seçilirse menü, telefon, harita ve WhatsApp tıklamalarını ayrı ve kişisel alanları göndermeden ölçün. Tıklama, gönderilmiş WhatsApp talebi, işletmenin onayladığı masa ve gerçekleşmiş ziyaret farklı sonuçlardır.
4. **Yerel otorite:** Yakındaki oteller/ziyaretçi kaynakları, kültür kurumları ve gerçek yerel yayınlarla yalnızca ziyaretçiye faydalı bilgi veya iş birliği üzerinden ilişki kurun. Sahte işletme dizinleri, ücret karşılığı düşük kaliteli bağlantılar ve yorum teşvikinden kaçının.
5. **Sayfa deneyimi:** Search Console’daki gerçek kullanıcı Core Web Vitals raporunu takip edin. Bu kod denetimi mobil tarama veya gerçek kullanıcı LCP/INP/CLS ölçümü değildir; laboratuvar skoru da tek başına üst sıra garantisi vermez.
6. **İçerik bakımı:** Fiyat, servis saati, ulaşım ve kurum programı gibi değişebilen bilgileri ilgili birincil kaynaktan tekrar doğrulayın. Yazının gerçek değerini artıran değişiklik yaptığınızda görünür güncelleme ve yapılandırılmış tarihi birlikte güncelleyin.

## Doğrulama sonucu

- Üretim: `python3 scripts/build_release.py .` başarılı.
- `check_tourism_seo.py`: 40 sayfa, 182 schema nesnesi, 14 blog rotası; hata yok.
- 40 `Restaurant` şema varlığının tamamında Instagram `sameAs` bağlantısı bir kez bulunuyor; mevcut Google Knowledge Graph bağlantısı da korunuyor.
- `check_international_seo.py`: 6 dilin tamamında canonical, hreflang, metadata, görünür SSS, menü ve varlık kontrolleri geçti.
- `check_reservations.py`, `check_search_growth.py`, `check_search_metadata.py`, `check_menu_budget.py`: tamamı geçti.
- Sitemap URL’lerinin tümünde title, description, canonical ve indexlenebilir robots metadatası doğrulandı.
- Örnek canlı ana sayfa, menüler, serpme fiyat rehberi, sitemap ve `robots.txt`: HTTP 200.
- Bu kontroller gerçek Search Console dizin durumunu, alan verisi Core Web Vitals’ı, organik tıklama artışını veya rezervasyon dönüşümünü ölçmez.

## Resmi kaynaklar

- [Google Search Essentials](https://developers.google.com/search/docs/essentials)
- [Google: AI features and your website](https://developers.google.com/search/docs/appearance/ai-features)
- [Google: Generative AI search için resmi optimizasyon rehberi](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)
- [Google: Helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)
- [Google: Local ranking faktörleri](https://support.google.com/business/answer/7091?hl=en)
- [Google: LocalBusiness yapılandırılmış veri](https://developers.google.com/search/docs/appearance/structured-data/local-business)
- [Google: Organization yapılandırılmış verisi ve `sameAs`](https://developers.google.com/search/docs/appearance/structured-data/organization)
- [Pusula Lounge Instagram profili](https://www.instagram.com/pusulalounge/)
- [Restaurant Guru’daki Pusula Lounge kaydı](https://de.restaurantguru.com/pusula-lounge-Istanbul)
- [Yandex’teki Pusula Lounge kaydı](https://yandex.com.tr/maps/org/pusula_lounge/172805673915/reviews/)
- [Google: İşletmenin kendi yorumları ve review snippet politikası](https://developers.google.com/search/docs/appearance/structured-data/review-snippet)
- [Google: Güncel title link oluşturma ilkeleri](https://developers.google.com/search/docs/appearance/title-link)
- [Google: Çok dilli sayfalar ve hreflang](https://developers.google.com/search/docs/specialty/international/localized-versions)
- [Google: Sitemap oluşturma ve gönderme](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap)
- [Google: Search Console performans ve indeks raporları](https://developers.google.com/search/docs/monitor-debug/search-console-start)
- [Google: Page experience ve Core Web Vitals sınırları](https://developers.google.com/search/docs/appearance/page-experience)
- [Google Business Profile: Doğal ve teşviksiz yorum alma](https://support.google.com/business/answer/3474122?hl=en)
