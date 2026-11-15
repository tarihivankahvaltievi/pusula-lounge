# Pusula Lounge SEO, GEO ve rezervasyon araştırması

15 Kasım 2026. Başlangıç sürümü `9fa3b27`.

## Canlı sitenin durumu

- Sitemaptaki 40 URL'nin tamamı doğrudan 200 ve HTML döndürdü. Canonical URL'ler sitemap ile uyumlu ve yanıtlar indekslemeyi engelleyen yönerge içermiyor. HTTP, www'siz alan adı ve sondaki eğik çizgisi eksik rezervasyon yolu örneklerinde 308, uydurma bir rota örneğinde 404 alındı.
- Canlı rezervasyon sayfası Googlebot, Bingbot ve OAI-SearchBot kullanıcı aracısı başlıklarıyla 200 döndürdü. Bu, örnek HTTP testidir. Gerçek botların IP erişimi, tarama kayıtları, dizin ve sıralama verileri için ilgili araçların verileri gerekir.
- Yerel sürüm denetimi 40 sayfayı, 182 yapılandırılmış veri düğümünü, 14 blog rotasını ve 81 sitemap görsel kaydını kapsadı. Birbiriyle eşleşen dil alternatifleri, canonical, görsel metadatası, işletme kimliği, yerel bağlantılar ve yapılandırılmış menü doğrulandı.
- Kamuya açık kaynaklarda Pusula Lounge için Sinek Çıkmazı No:3 ve +90 507 816 29 94, sitedeki kayıtla eşleşiyor. Örneklenen Yandex kaydı Küçük Parmak Kapı Sokak No:4 gösteriyor. Profil sahipliğiyle fiziksel giriş ve pin doğrulandıktan sonra dizin kaydı düzeltilmeli. [SageNearby kaydı](https://sagenearby.com/tr/detail/pusula-lounge) · [Yandex kaydı](https://yandex.com.tr/maps/org/pusula_lounge/172805673915/)
- Kamuya açık arama örneklerinde Tarihi Van Kahvaltı Evi ve Sa Va Anatolian; menü, fiyat, ulaşım ve rezervasyon çağrılarını bir arada gösteriyor. Pusula'nın ayırt edici kaynakları gerçek sofra fotoğrafları, kendi menüsünden üretilen porsiyon karşılaştırması, yayımlanan kahvaltı saatleri ve doğrulanmış harita pinidir. Örnekler arama hacmi veya sabit sıralama ölçümü olarak kullanılmadı. [Tarihi Van](https://www.tarihivankahvaltievi.com/en) · [Sa Va Anatolian](https://www.savaanatolianbreakfasthouse.com/taksim-kahvalti)

## Arama niyeti ve sayfa eşlemesi

| Niyet | Mevcut hedef | Ziyaretçinin sonraki adımı |
| --- | --- | --- |
| Pusula Lounge rezervasyon, Taksim table reservation | Altı dilde rezervasyon sayfası | Doğrudan WhatsApp veya tarih, saat ve kişi sayısı içeren talep |
| Taksim Van kahvaltısı, Turkish breakfast near Taksim | `/kahvalti/` ve `/en/breakfast/` | Menü ve porsiyonları karşılaştırıp kahvaltı için masa isteme |
| Pusula menü, serpme kahvaltı fiyatı | Dört dilde menü ile TR/EN kahvaltı rehberleri | Menüdeki güncel fiyatı görüp kahvaltı için masa isteme |
| Pusula nerede, Taksim walking directions | Dört dilde konum sayfası | İşletme pinine yürüyüş rotası açma |
| Taksim akşam yemeği, waffle ve kahve | TR/EN akşam rehberi ve ana sayfa ziyaret seçenekleri | Akşam için masa isteme veya günün menüsünü sorma |

## Yayına hazırlanan iyileştirmeler

1. Altı rezervasyon sayfasının arama, paylaşım ve WebPage açıklamaları WhatsApp üzerinden masa talebi ile ekip teyidini açıkça tarif ediyor. Aynı bilgi sayfalarda metin olarak mevcut. Google, sonuç açıklamasını sorguya göre sayfadan da seçebilir. [Google snippet rehberi](https://developers.google.com/search/docs/appearance/snippet)
2. Telefon alanı isteğe bağlı. Girilirse doğrulanıyor, boşsa hazır WhatsApp mesajından çıkarılıyor. Doğrudan WhatsApp bağlantısı, formu doldurmadan ve JavaScript kapalıyken de yerel dilde mesaj taslağı açıyor. Özel gün ve masa uygunluğu ekip teyidine bağlı.
3. Kahvaltı saatleri tarih ve saat alanlarının yanında görünüyor. TR/EN menü ve rehberlerdeki kahvaltı rezervasyonu bağlantıları doğru ziyaret türünü seçiyor. Rezervasyon sayfasında dil değiştirirken tanınan ziyaret türü korunuyor. Parametresiz adresler canonical ve sitemap adresi olarak kullanılıyor. [Google canonical rehberi](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls)
4. Doğrudan WhatsApp açılışı mevcut anonim etkileşim olayını tetikliyor. Google Ads etiketi kullanıldığı sayfalarda mevcut izin seçimini uyguluyor. Site, mesajın gönderildiğini veya masanın onaylandığını göremez.
5. GEO kapsamında Google'ın indekslenebilir, görünür ve doğrulanabilir içerik ilkeleriyle OpenAI'nin OAI-SearchBot erişimi esas alındı. Menü, saat, adres, konum ve teyit koşulu HTML'de okunabiliyor. [Google AI görünürlüğü rehberi](https://developers.google.com/search/docs/appearance/ai-features) · [OpenAI arama tarayıcısı](https://developers.openai.com/api/docs/bots)

## Rezervasyon artışını ölçme

İlk 28 günü önceki 28 günle karşılaştırın. Hafta içi ve hafta sonu dağılımını, tatilleri ve reklam bütçesindeki değişiklikleri not edin. Ana metrik ekibin teyit ettiği masa sayısıdır. WhatsApp açılışları yalnızca akışın ara göstergesidir.

| Kaynak | Takip edilecek metrik |
| --- | --- |
| Search Console | Marka ve marka dışı sorgular ayrı olacak şekilde kahvaltı, menü, konum ve rezervasyon sayfalarının gösterim, tıklama ve CTR değerleri |
| Google İşletme Profili | Web sitesi tıklamaları, aramalar ve yol tarifi istekleri |
| Google Ads | İzinli WhatsApp açılışları ve açılış başına maliyet |
| İşletmenin rezervasyon kaydı | Talep, teyit ve gelen masa için ayrı günlük toplamlar. Mümkünse müşterinin beyan ettiği kanal, kahvaltı veya akşam ayrımı |

Güncel Search Console, İşletme Profili ve gerçek rezervasyon kayıtları bu denetime bağlı değildi. Arama hacmi, dizin durumu veya dönüşüm artışı çıkarılmadı.

## Profilde öncelikli kontrol

Profil sahibi kategoriyi, giriş pinini ve normal/özel gün saatlerini kontrol etmeli. Site kahvaltı servisini günlük 08:00–17:00 olarak açıklıyor. Bu servis saatini işletmenin genel çalışma saatinden ayrı değerlendirin. Google, yerel sonuçları alaka, mesafe ve bilinirlikle ilişkilendiriyor. [Google yerel sıralama rehberi](https://support.google.com/business/answer/7091)

Profilde sunuluyorsa WhatsApp seçeneğini iletişim alanından kullanın. Google'ın rezervasyon eylem bağlantıları işlem tamamlamaya yönelik ayrı bir politika izliyor ve doğrudan mesajlaşma bağlantılarını hariç tutuyor. WhatsApp teyidine dayanan mevcut sayfanın rezervasyon bağlantısı olarak uygunluğu profil üzerinden doğrulanmalı. [Profil düzenleme](https://support.google.com/business/answer/3039617) · [İşletme bağlantısı kuralları](https://support.google.com/business/answer/13769188)
