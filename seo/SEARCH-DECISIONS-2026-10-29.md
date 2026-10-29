# Pusula Lounge: aramadan masa talebine

29 Ekim 2026 · Başlangıç: `b9111e5` · Kapsam: SEO, üretken arama görünürlüğü (GEO), yerel keşif ve ziyaret kararı.

## Araştırmanın sonucu

Sitede zaten 40 URL, dört dilde kahvaltı menüsü, altı dilde masa talep akışı, iki dilde kahvaltı rehberleri ve yazılar var. Yeni benzer sayfalar açmak yerine mevcut ticari sayfaların daha fazla soruyu yanıtlaması ve ziyaretçiyi doğru sonraki adıma götürmesi önceliklendirildi.

Bu turda üç yayın sayfası geliştirildi: Türkçe menü, Türkçe kahvaltı ve İngilizce kahvaltı. Önceki sürümlerdeki başlık, yorum bağlantısı, ulaşım rehberi, dil sayfaları ve bot izinleri bu çalışmanın yeni kazanımı olarak sayılmadı. Önceki CTR denemelerinin başlıkları korunarak ölçümdeki değişken sayısı sınırlı tutuldu.

## Yöntem ve kanıt sınırı

- Güncel GitHub `main`, üretim zinciri, sitemapteki sayfalar, görünür içerik ve JSON-LD incelendi. Eski çalışma klasöründeki `site/` yerine yayın deposu kullanıldı.
- Marka, menü ve Taksim kahvaltı arama örnekleri; Kardeşler Cihangir, Sa Va Anatolian ve Tarihi Van Kahvaltı Evi'nin kendi sayfaları karşılaştırıldı. Arama örnekleri tam bir sıralama araştırması veya anahtar kelime hacmi ölçümü değildir; sonuçlar konum ve zamana göre değişir.
- Google Search Central ve Google İşletme Profili'nin birincil rehberleri incelendi. Öneriler üçüncü taraf GEO puanlarına veya görünürlük garantilerine dayanmıyor.
- Canlı alan adı, menü, İngilizce ana sayfa, sitemap, robots, yönlendirme ve 404 yanıtları HTTP üzerinden kontrol edildi. Web metin aracının iki site URL'sini açamaması tek başına tarama engeli sayılmadı; HTTP kontrolleri erişimi doğruladı. Makbuz: `search-decisions-live-audit-2026-10-29.json`.
- Aynı gün çalışma klasörüne kaydedilmiş önceki hesap araştırması bağlam olarak okundu. Bu turda Search Console, İşletme Profili veya reklam hesabından yeni veri çekilmedi; hesaba özel performans bilgileri bu açık rapora taşınmadı. Yeni trafik, müşteri veya rezervasyon artışı ölçülmüş değildir.

## Bulgular ve kararlar

| Bulgu | Müşteri üzerindeki etkisi | Bu turdaki karar |
| --- | --- | --- |
| Türkçe menünün H1'i yalnızca ekran okuyuculara görünüyordu; masa talebi ürünlerden sonra geliyordu. | Aramadan gelen ziyaretçi sayfanın yerini ve ziyaret için sonraki adımı geç görüyordu. | Görünür, açıklayıcı H1; ürünlerden önce masa talebi ve yol tarifi. |
| Kahvaltı sayfalarında serpme porsiyonları karşılaştırılıyordu; sıcak ürünlerin tek tek fiyatı için menüye geçmek gerekiyordu. | Serpme istemeyen ziyaretçi seçenekleri karşılaştırmak için birden fazla bölüm açıyordu. | Beş gerçek ürünün fiyatını ve menüde listelenen çay kapsamını TR/EN tabloda bir araya getir. |
| İngilizce, Rusça ve Arapça menülerde erken ziyaret eylemleri zaten vardı. | Türkçe ziyaretçinin akışı diğer dillerin gerisindeydi. | Yeni bir genel şablon yerine Türkçe akıştaki eksikliği tamamla. |
| Canlı canonical, robots, sitemap ve URL yönlendirmelerinde incelenen örnekler çalışıyordu. | Öncelik tarama iznini yeniden yazmak değil, mevcut görünürlüğü nitelikli ziyarete çevirmek. | Teknik yapıyı koru, bağlantı ve fiyat doğrulamasını genişlet. |

### Rakiplerin kendi sayfaları ne gösteriyor?

[Kardeşler Cihangir](https://www.kardeslercihangir.com/turkish-breakfast-cihangir) kahvaltı saatlerini, serpme porsiyonunu, sıcak ürün fiyatlarını ve yol tarifini birlikte sunuyor. [Sa Va Anatolian](https://www.savaanatolianbreakfasthouse.com/en/breakfast-near-me) İngilizce ziyaretçiye konum, servis, paylaşmalı sofra ve rezervasyon yollarını aynı akışta anlatıyor. [Tarihi Van Kahvaltı Evi](https://www.tarihivankahvaltievi.com/en) menü, adres ve masa talebini doğrudan bağlıyor. Ortak ders, ziyaret kararına gereken bilgileri birlikte sunmak. Rakiplerin fiyatları, beslenme uygunluğu, tarihçesi ve yürüyüş süreleri Pusula'ya aktarılmadı. Bunlar pazarın tamamını temsil eden örnekler değildir.

### SEO ve GEO için dayanak

[Google AI rehberi](https://developers.google.com/search/docs/appearance/ai-features), normal arama temellerini, metin halinde erişilebilir bilgiyi, iç bağlantıları ve görünür içerikle tutarlı yapılandırılmış veriyi öneriyor. Özel bir AI dosyası veya özel şema gerekmiyor. Bu yüzden yeni karşılaştırma JavaScript olmadan HTML'de okunabiliyor; sayfa verisi yalnızca tablodaki gerçek menü maddelerine `mentions` ile işaret ediyor. Bu ilişki bir AI alıntısı veya zengin sonuç garantisi değildir.

[Yerel işletme verisi rehberi](https://developers.google.com/search/docs/appearance/structured-data/local-business) işletmenin doğru tanımlanmasına yardımcı oluyor. Mevcut Restaurant kimliği, adres, telefon, menü ve saatler korundu. Çay listelenmeyen ürünlere “çay dahil” veya “çay kesinlikle yok” iddiası eklenmedi. Menü açıklamasında bulunmayan bilgi ayrıca teyit edilmeli.

[Google snippet rehberi](https://developers.google.com/search/docs/appearance/snippet) arama açıklamasının sayfa içeriğinden de üretilebildiğini anlatıyor. Görünür menü başlığı ve ürün tablosu daha anlaşılır kaynak metin sağlıyor. Menüdeki sonuç bulunamadı durumu `data-nosnippet` ile işaretlendi; ürünler ve ziyaret bilgisi snippet'e açık. Google'ın seçtiği snippet'i site zorlayamaz.

[Spam politikaları](https://developers.google.com/search/docs/essentials/spam-policies#doorway-abuse) benzer sorgular için aynı sonuca yönlendiren zayıf ara sayfaları sorun olarak tanımlıyor. Bu çalışma “Taksim menemen”, “Beyoğlu menemen” gibi birbirine benzeyen sayfalar üretmiyor; gerçek ürünleri mevcut kahvaltı ve menü sayfalarında buluşturuyor.

## Sorgudan müşteri eylemine harita

Aşağıdakiler hacmi doğrulanmış anahtar kelimeler değil, ziyaretçi ihtiyacını test etmek için sorgu kümeleridir. Fragmentler yeni sayfalar değildir.

| İhtiyaç / örnek sorgular | Asıl sayfa | İstenen sonraki eylem |
| --- | --- | --- |
| Pusula Lounge menü, Taksim kahvaltı fiyatları | `/menu/` | Fiyatı incele → masa talebi veya yol tarifi |
| Taksim tek kişilik kahvaltı, serpme dışında kahvaltı | `/kahvalti/#late-breakfast` | Beş seçeneği karşılaştır → ürün içeriğini aç |
| Taksim menemen, gözleme fiyatı | `/menu/#sade-menemen`, `/menu/#peynirli-gozleme` | Gerçek ürün ve fiyat → ziyaret kararı |
| breakfast for one Taksim, menemen Taksim | `/en/breakfast/#late-breakfast` | İngilizce fiyat/çay karşılaştırması → İngilizce menü |
| Pusula yol tarifi, entrance, directions | `/konum/`, `/en/location/` | Gerçek giriş adresi → kişiye göre harita rotası |
| Pusula Lounge reviews | `/en/` | Önceki sürümün gerçek Google yorum bağlantısını kullan |

## Öncelikli müşteri kazanım planı

| Öncelik | İş | Neden / başarı ölçüsü |
| --- | --- | --- |
| 1 | İşletmenin tek güncel fiyat kaynağını belirle; web menüsü ile harici dijital menü ve işletme profilini eşitle. | Önceki araştırmada iki menü arasında fiyat farkı kaydedilmişti. Bu tur harici menünün okunabilir güncel fiyatını doğrulayamadı; mevcut web fiyatı değiştirilmedi. Karar işletme tarafından teyit edilmiş fiyat listesine dayanmalı. |
| 1 | Google İşletme Profili'nde gerçek kategori, pin, telefon, menü bağlantısı, kahvaltı ve özel gün saatlerini kontrol et. | [Yerel sıralama rehberi](https://support.google.com/business/answer/7091?hl=en), alaka, uzaklık ve bilinirliği temel alıyor. Yakınlık site koduyla değişmez; doğru bilgi ve gerçek deneyim gerekir. |
| 1 | Pusula'ya ait ölçüm hesabı ve ziyaretçi veri tercihi belirlendiğinde anonim eylemleri raporla. | Menü, telefon, rota ve masa talebi farklı niyetlerdir. Başka işletmeye ait Analytics akışına veri bağlama. |
| 2 | Doğru adres ve menüyle gerçek işletme fotoğraflarını düzenli güncelle; gerçek müşterilerden dürüst geri bildirim iste. | İşletme profiliyle web sitesinin aynı deneyimi anlatmasını sağla. Sahte veya teşvikli yorum kullanma. |
| 2 | Search Console'da marka / marka dışı, TR / EN ve mobil / masaüstü kırılımlarını incele. | Toplam trafik artışı hangi sayfanın doğru ziyaretçiyi getirdiğini açıklamaz. |
| 3 | Gerçek yakın oteller ve ziyaretçi danışma noktaları için kısa menü/konum bilgi kartı hazırla. | Somut yerel keşif ve yönlendirme olanağı; dış iletişim ayrıca yetkilendirilmeli. Bu görevde kimseye mesaj gönderilmedi. |

## Ölçüm tasarımı

Yayın sonrasındaki ilk tam 28 günü, önceki 28 günle ve mümkünse geçmişte aynı dönemle karşılaştırın. 30 Ekim–26 Kasım 2026 bir ilk değerlendirme penceresidir; çok düşük gösterimde daha uzun veri birikmesi gerekir. 29 Ekim tatili, mevsimsellik, reklamlar ve aynı günün önceki site değişiklikleri nedensel çıkarımı sınırlar.

Her hedef URL için gösterim, tıklama, CTR ve ortalama konumu sorgu ve cihaz kırılımıyla izleyin. Gösterim yoksa önce indeksleme ve sorgu eşleşmesini; gösterim var tıklama azsa arama önizlemesini; ziyaret var talep azsa fiyat ve ziyaret akışını araştırın. Bu sürüm başlıkları yeniden değiştirmediği için önceki başlık deneyi korunur, ancak tüm site değişiklikleri yine ortak etki yaratabilir.

Sitedeki `pusula:interaction` olayları yalnızca olay adı, yol ve dil taşır. Kalıcı analitik sistemine bağlı değillerdir. Yeni masa talebi düğmesi mevcut `reservation_page_click` olayını kullanır; sorgu parametresi, isim, telefon, mesaj, tarih veya not göndermez. WhatsApp açılışı, gönderilmiş talep, onaylanmış masa ve gerçekleşen ziyaret ayrı aşamalardır. Gerçek müşteri kazanımı ancak işletmenin onay/ziyaret kaydıyla değerlendirilebilir. AI kaynaklı yönlendirme veya manuel alıntı gözlemi de gerçek müşteriden ayrı raporlanmalıdır.

## Uygulama ve bakım

- `scripts/build_search_growth.py`: görünür Türkçe menü girişi, erken eylemler, iki dilde karşılaştırma ve ilgili CSS üretimi.
- `scripts/finalize_search_metadata.py`: görünen beş ürün bağlantısının WebPage verisindeki referansları.
- Fiyat kaynağı mevcut Türkçe menüdür; ürün adları ilgili dilin menüsünden alınır. Fiyat/ürün değişikliğinden sonra tam yayın üretimi çalıştırılır.
- Yeni sayfa veya harici izleyici eklenmedi. Mevcut güvenlik politikası ve dosya bütünlük değerleri üretim zincirinden geçer.
- `python3 scripts/build_release.py .` sonrasında README'deki kontrolleri ve yeni `node scripts/test_search_decisions.cjs /tmp/pusula-search-decisions` kontrolünü çalıştırın.

## Doğrulama

40 sayfa ve 182 yapılandırılmış veri nesnesinde canonical, iç bağlantı, dil ilişkisi, yerel dosya, SRI/CSP ve tarama kontrolleri hatasız. Dört dilde 76 ürün / 84 fiyat teklifi ve altı dilde rezervasyon kontrolleri geçti. Beş ürünün fiyatı geçici kopyada değiştirilerek iki dilde aktarımı ve üretimin tekrar çalışabilirliği doğrulandı.

320, 390, 768 ve 1440 pikselde, JavaScript açık ve kapalı toplam 24 yeni akış kontrolü geçti: yatay taşma yok; tablo ve ürün bağlantıları okunuyor; menü arama/sıfırlama çalışıyor; erken masa talebi kahvaltı seçimiyle rezervasyon sayfasını açıyor; kişisel veri içermeyen olay yapısı korunuyor. Mobil ve masaüstü görüntüler ayrıca incelendi. Tasarım tarayıcısının mevcut menü dokusu, yazı tipi ve eski giriş etiketleri hakkındaki önerileri kapsam dışı mevcut stillere aittir; yeni alanlarda taşma veya işlev hatası saptanmadı.

Teknik doğrulama, gerçek kullanıcı Core Web Vitals, arama sıralaması veya müşteri artışı ölçümü değildir.

Tam yayın ikinci kez üretildiğinde HTML, CSS, JavaScript, JSON, XML ve WOFF2 dosyaları byte düzeyinde aynı kaldı. Genel tarayıcı denetimindeki 160 sayfa/ekran genişliği kontrolü de CSP, görseller, fontlar, klavye geçişi ve RU/AR menü–rezervasyon akışları için geçti.
