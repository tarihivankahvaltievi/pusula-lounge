# Pusula Lounge: Derin SEO/GEO ve müşteri kazanımı araştırması

**Tarih:** 29 Ekim 2026

**İncelenen sürüm:** `82b9b85` (`main`)

**Hedef:** Taksim/Beyoğlu aramalarından doğru sayfaya gelen ziyaretçiyi menüyü incelemeye, menü sorusu sormaya veya masa talebi göndermeye taşımak.

## Araştırma kapsamı ve ölçüm sınırı

Canlı sitenin ana sayfası, kahvaltı ve menü yolları, Türkçe/İngilizce akşam rehberleri, fiyat kaynakları, iç bağlantılar ve yayımlı işletme bilgileri incelendi. Kamuya açık arama örnekleri ve rakiplerin kendi sayfaları, kullanıcının ziyaret öncesi hangi bilgileri aradığını anlamak için karşılaştırıldı. Örneklem arama hacmi, Google konumu, sıralama takibi veya Search Console verisi değildir. Bu oturumda Search Console, Google İşletme Profili veya GA4 hesabına bağlı performans verisi bulunmuyordu; mevcut tıklama ve müşteri sayısı doğrulanamıyor.

## Bulgular ve uygulama

### Akşam ziyareti ile fiyatlı menü arasındaki kopukluk

Ana sayfa akşam yemeği için pizza, hamburger ve balığı; mola için waffle, tatlı, kahve ve çayı tanıtıyor. Buna karşılık yayımlı `/menu/` ve `/en/menu/` sayfaları kahvaltı ürünlerini ve fiyatlarını gösteriyor. Akşam yemeği rehberi bu farkı açıklıyordu; ancak “Menü ve fiyatlar / Menu & prices” bağlantısı ziyaretçiyi yine yalnız kahvaltı menüsüne götürüyordu.

Bu turda akşam rehberindeki bağlantılar açıkça **kahvaltı menüsü** olarak etiketlendi. Akşam ürünlerinin güncel seçimi ve fiyatı için, kişinin gözden geçirip WhatsApp’ta kendisinin göndereceği hazır bir soru bağlantısı eklendi. Bu bağlantı masa rezervasyonu değildir; ekip mevcut ürün, fiyat ve masa uygunluğunu teyit eder. WhatsApp tıklaması için ayrı bir anonim olay adı eklendi; bu depoda olayları alan bir analitik hizmeti hâlâ yapılandırılmış değildir.

Akşam menüsü ve fiyatları ilk taraf kaynakta yayımlı olmadığı için yeni ürün/fiyat yazılmadı. Gerçek menü ve fiyat listesi işletme tarafından doğrulanırsa, menü sayfasını tam yiyecek/içecek kataloğuna dönüştürmek en yüksek değerli içerik devam işidir. Rakip fiyatları Pusula içeriğine aktarılmadı.

### Yerel ve AI arama için kaynakların söylediği

- [Google’ın üretken AI arama rehberi](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide) AI Overviews ve AI Mode için temel SEO, erişilebilir/taranabilir sayfalar, özgün yerel bilgi ve kullanıcıya yararlı içerik öneriyor. Ayrı bir “GEO schema” gerektirmiyor. Bu yüzden yapay anahtar kelime blokları veya özel AI işaretlemesi eklemek yerine doğru menü bilgisi, adres, servis saati, yön tarifi ve net sonraki adım esas alındı.
- [Google’ın yerel sıralama açıklaması](https://support.google.com/business/answer/7091?hl=en) alaka, mesafe ve bilinirliği sayıyor. Site içeriği işletmenin aramayla alakasını açıklayabilir; arayan kişinin mesafesini veya işletmenin bilinirliğini tek başına değiştiremez.
- [Google başlık bağlantısı rehberi](https://developers.google.com/search/docs/appearance/title-link) sayfa başlığının kısa, açıklayıcı ve sayfa içeriğiyle uyumlu olmasını öneriyor; başlık arama sonucunda her zaman aynen gösterilmez. Bu nedenle akşam içeriğinin CTA’sı, gittiği kahvaltı sayfası hakkında yanlış beklenti oluşturmuyor.
- [Google yorum alma rehberi](https://support.google.com/business/answer/3474122?hl=en) gerçek müşterilerden yorum istemeye ve yanıtlara izin veriyor; [katkı politikası](https://support.google.com/contributionpolicy/answer/7400114?hl=en) teşvik/indirim karşılığı yorum istemeyi, yalnız olumlu yorumları seçerek istemeyi yasaklıyor. İşletme profili çalışmasında doğal ve tarafsız istek kullanılmalı.
- [Bing AI Performance](https://www.bing.com/webmasters/help/ai-performance-9f8e7d6c), AI yanıtlarındaki atıfları ve grounding query’leri raporlar; atıf tıklama veya satış değildir. AI görünürlüğü ile Search Console tıklamaları ayrı ölçülmeli.

### Rakip örnekleri

[Tarihi Van Kahvaltı Evi’nin menüsü](https://www.tarihivankahvaltievi.com/menu) ürün içeriği, porsiyon ve fiyatı aynı yerde gösteriyor; [Taksim kahve sayfası](https://www.tarihivankahvaltievi.com/en/coffee-taksim) ürün fiyatlarını ziyaret planı ve adres bilgisiyle eşliyor. Bu, Pusula için “fiyat ve içerik aynı akışta” standardını destekliyor. Sitede bulunmayan fiyatlar, servis özellikleri veya işletme iddiaları rakiplerden kopyalanmadı.

## İçerik ve arama niyeti planı

| Arama niyeti | Ana sayfa | Kullanıcının sonraki adımı |
| --- | --- | --- |
| Pusula Lounge, Taksim kafe/restoran | `/` | Kahvaltı, menü, konum veya masa talebi |
| Taksim serpme Van kahvaltısı, porsiyon/fiyat | `/kahvalti/`, `/menu/` | Porsiyon ve fiyatı karşılaştırıp kahvaltı masası istemek |
| Taksim akşam yemeği, waffle, kahve | `/blog/taksimde-aksam-yemegi-waffle-kahve/` | Güncel akşam menüsü/fiyatını WhatsApp’ta sormak veya masa talebi göndermek |
| Taksim yol tarifi, İstiklal ziyareti | `/konum/` ve ilgili rehber | Harita, telefon ve ulaşım bilgisi |

Bu gruplar içerik ve nitel arama örneklerinden çıkarılmıştır; aranma hacmi veya hedef sıralama tahmini değildir. Aynı niyete yönelik benzer semt sayfaları açmak yerine, mevcut sayfaların sunduğu gerçek bilgiyi tamamlamak tercih edildi.

## Yayın sonrası müşteri kazanımı sırası

1. **Tam yiyecek/içecek menüsünü doğrulayın:** Akşam ürünleri, fiyatlar, porsiyonlar, ürün bulunurluğu ve servis saatleri ekip tarafından teyit edilince aynı menü sayfasında kategori, içerik ve güncel fiyatla yayımlayın. Bu veri olmadan ziyaretçi fiyat karşılaştıramaz.
2. **Search Console başlangıç verisini kaydedin:** canonical alan adında hedef URL, sorgu, ülke ve cihaz kırılımında gösterim, tıklama, CTR ve ortalama konumu dışa aktarın; marka ve marka dışı aramaları ayırın. Yüksek gösterim/düşük CTR sayfalarında başlık vaadini sınayın; önce dizin ve sorgu uyumunu kontrol edin.
3. **Google İşletme Profilini eşitleyin:** işletme adı, gerçek kategori, Sinek Çıkmazı No:3 adresi ve harita pini, telefon, 24 saat genel çalışma bilgisi, ayrı 08:00–17:00 kahvaltı servisi, menü ve rezervasyon URL’lerini işletme sahibi panelinde doğrulayın. Profildeki yanlış/kopya adresleri sahip erişimiyle düzeltin.
4. **Gerçek müşteri ve rezervasyon sonucunu ayırın:** “Bizi nereden buldunuz?” yanıtını, WhatsApp’ta gönderilmiş talebi, ekibin onayladığı masayı ve gerçekleşen ziyareti ayrı sayın. Mevcut `pusula:interaction` olayı tıklama açılışını ifade eder; WhatsApp mesajının gönderildiğini veya rezervasyonun kesinleştiğini göstermez.
5. **AI atıflarını ayrı izleyin:** Bing AI Performance erişimi varsa atıf ve grounding query eğilimlerini takip edin; bunları tıklama veya satış olarak raporlamayın.

Artış yüzdesi vaat edilmez. Bu yayının etkisi Search Console ve işletme kayıtlarındaki sonraki dönem verisiyle ölçülmelidir.
