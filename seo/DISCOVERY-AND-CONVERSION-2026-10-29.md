# Pusula Lounge — arama görünürlüğü ve müşteri kazanımı

29 Ekim 2026. Başlangıç sürümü: `4a467b1`. Bu çalışma önceki SEO geliştirmelerinin üzerine yapılmıştır; önceki değişiklikler bu çalışmanın yeni kazanımı olarak sayılmamıştır.

## Araştırmanın sonucu

Yeni sayfa sayısını artırmaktan önce mevcut kahvaltı sayfasının ziyaret kararını daha iyi karşılaması önceliklendirildi. Pusula'nın yayınlanmış 08:00–17:00 kahvaltı servisi, geç kahvaltı arayan ziyaretçiye açık bir cevap sunuyor. Tek kişilik tabaklar da serpme porsiyonları dışında bir seçim olanağı sağlıyor. Bu iki ihtiyaç mevcut ticari sayfada yanıtlandı; aynı amaca hizmet eden benzer semt sayfaları oluşturulmadı.

Bu bir arama hacmi veya sıralama ölçümü değildir. Search Console, Google İşletme Profili ve analitik hesabına erişim yoktur. Örnek sonuçlar arama motoru, konum, dil ve zamana göre değişebilir. Trafik, CTR veya müşteri artışı henüz ölçülmemiştir.

## İnceleme ve kaynaklar

Marka, Taksim kahvaltı menü/rezervasyon, Türkçe geç kahvaltı ve İngilizce late breakfast Taksim sorguları araştırıldı. Canlı ana sayfa, kahvaltı, İngilizce kahvaltı, menü, robots ve sitemap HTTP erişimi kontrol edildi; altısı da 200 döndü ve X-Robots-Tag ile engellenmiyordu. Yanıt kanıtı: `live-discovery-audit-2026-10-29.json`. Bu kontrol dizine eklenme kanıtı değildir.

| Kaynak | Gözlem | Pusula için karar |
| --- | --- | --- |
| [Kardeşler Cihangir kahvaltı sayfası](https://www.kardeslercihangir.com/turkish-breakfast-cihangir) | Porsiyon, fiyat ve 09:00–13:00 kahvaltı saati aynı sayfada. | Servis saati ve porsiyon açıklamasını ziyaret kararına bağla. Rakibin fiyatını veya rezervasyonsuz hizmet politikasını kopyalama. |
| [Elite World Taksim](https://www.eliteworldhotels.com.tr/oteller/elite-world-istanbul-taksim/restaurants-bar/elite-restaurant) | Kahvaltıda hafta içi 10:30, hafta sonu 11:00 bitişi belirtiliyor. | Pusula'nın kendi yayınlanmış 17:00 bitişini geç kahvaltı ihtiyacı açısından anlat. Bu örnekler tüm rakiplerin erken kapandığı anlamına gelmez. |
| [Tarihi Van Kahvaltı Evi](https://www.tarihivankahvaltievi.com/) | Menü, ulaşım ve rezervasyon ön planda; karışabilecek adres açıklanıyor. | Pusula girişini Sinek Çıkmazı No:3 olarak açıkça belirt ve yürüyüş tarifine bağla. |
| [Pusula SageNearby kaydı](https://sagenearby.com/tr/detail/pusula-lounge) | Marka, telefon, sokak ve 24 saat açık bilgisi görünüyor; çok sayıda üçüncü taraf hizmet iddiası var. | Mevcut işletme kimliği ile karşılaştır; ödeme, erişilebilirlik, alkol veya evcil hayvan bilgilerini doğrulanmış işletme kaynağı olmadan siteye taşıma. |
| [Pusula Yandex yorumları](https://yandex.com.tr/maps/org/pusula_lounge/172805673915/reviews/) | Farklı dillerde kahvaltı ve porsiyon deneyimlerinden söz ediliyor. | Mevcut dil sayfalarını koru. Yorum fiyatlarını güncel menü fiyatı veya puanları kendi işletme değerlendirme şeması olarak kullanma. |

## SEO ve GEO dayanakları

- [Google AI özellikleri](https://developers.google.com/search/docs/appearance/ai-features): taranabilir sayfalar, görünür metin, doğru iç bağlantılar ve içerikle uyumlu yapılandırılmış veri temel alınır. Ayrı bir AI dosyası veya özel AI şeması görünürlük garantisi sağlamaz. Yeni yanıtlar normal HTML içinde, JavaScript olmadan okunabilir.
- [Google Search Essentials](https://developers.google.com/search/docs/essentials): ziyaretçi ihtiyacını karşılayan içerik ve taranabilir bağlantılar. Aynı anahtar kelime için ayrı, birbirinin benzeri sayfalar üretmek yerine mevcut kahvaltı sayfası geliştirildi.
- [Google yerel işletme verisi](https://developers.google.com/search/docs/appearance/structured-data/local-business): işletme kimliği, adres, saat ve menünün doğru aktarımı. Dört dilde WebPage ile mevcut Menu nesnesi karşılıklı `mainEntity` / `mainEntityOfPage` üzerinden ilişkilendirildi. Bu ilişki özel bir Google zengin sonucu vaadi değildir.
- [OpenAI yayıncı rehberi](https://help.openai.com/en/articles/12627856): ChatGPT arama keşfi için OAI-SearchBot erişimi gerekir. Mevcut robots.txt zaten izin veriyordu; bu çalışmada yeni açılmış gibi raporlanmadı. Bot erişimi alıntılanmayı garanti etmez.
- [Google yerel sıralama rehberi](https://support.google.com/business/answer/7091): alaka, uzaklık ve bilinirlik önemlidir. Kod değişikliği işletme profilinin güncelliğinin ve gerçek müşteri deneyiminin yerini tutmaz.
- [Google başlık rehberi](https://developers.google.com/search/docs/appearance/title-link): açıklayıcı başlıklar gerekir. Başlıklar önceki sürümde yenilenmişti; veri olmadan aynı gün tekrar değiştirilmedi. Bu, sonraki CTR değerlendirmesinde değişken sayısını azaltır.

## Uygulanan değişiklikler

1. `/kahvalti/` ve `/en/breakfast/` içine geç kahvaltı, hafta sonu ve özel gün teyidi yanıtı eklendi. Mekânın 24 saat açık olması ile kahvaltı servis saatinin farklı olduğu açıklandı. Son sipariş saati uydurulmadı; kapanışa yakın gelişler için ekiple görüşme önerildi.
2. Tek ziyaretçi için kahvaltı tabağı ve pişi tabağı fiyatları, Türkçe ana menüden otomatik alındı. Paylaşmalı 2/3/4 kişilik serpme ile bireysel tabakların farkı açıklandı. Metin doğrudan ilgili menü maddesine bağlandı.
3. Giriş adresi ve konum sayfasına bağlantı eklendi. Yürüyüş süresi veya garantili masa uygunluğu iddiası eklenmedi.
4. Türkçe, İngilizce, Rusça ve Arapça menülerde sayfa–menü nesne ilişkisi tamamlandı.
5. Değişen fiyatın iki dildeki yeni metinlere aktarılması, yinelenen üretimin aynı sonucu vermesi ve menü veri ilişkileri testlere alındı.

## Sorgu ve dönüşüm haritası

| İhtiyaç / sorgu hipotezi | Hedef | Bir sonraki anlamlı eylem |
| --- | --- | --- |
| Taksim geç kahvaltı, öğleden sonra kahvaltı | `/kahvalti/#late-breakfast` | Servis saatini öğren → porsiyonu seç → masa iste |
| late breakfast Taksim, Turkish breakfast after noon | `/en/breakfast/#late-breakfast` | İngilizce yanıt → menü → masa iste |
| Taksim tek kişilik kahvaltı, kahvaltı tabağı fiyatı | `/kahvalti/`, `/menu/#kahvalti-tabagi` | Bireysel tabak içeriğini ve fiyatını karşılaştır |
| breakfast for one Taksim | `/en/breakfast/`, `/en/menu/#kahvalti-tabagi` | Tek tabak seçeneğini incele |
| Pusula Lounge giriş / nasıl gidilir | `/konum/`, `/en/location/` | Harita rotası aç veya ara |

Bu ifadeler hacmi doğrulanmış anahtar kelimeler değildir. Sayfalar zaten dizine girebilir URL'lerdir; fragment bağlantıları ayrı sitemap sayfaları değildir.

## Müşteri kazanımı için hesap tarafındaki öncelikler

**İlk hafta:** Google İşletme Profili sahibi gerçek giriş adresi, pin, telefon, ana kategori, kahvaltı saatleri, menü ve masa talebi bağlantılarını kontrol etmeli. Eski araştırmada belirtilen Yandex adres farkı işletme sahibi tarafından teyit edilmeli. Kategoriye kelime eklemek için işletme adı değiştirilmemeli. Gerçek servis ve mekân fotoğrafları eklenmeli. Bu hesaplarda değişiklik yapılmadı.

**Ölçüm:** Search Console'da marka ve marka dışı sorgular ayrı izlenmeli. Başlangıç için 1–28 Ekim ile 30 Ekim–26 Kasım 2026 karşılaştırılabilir; cihaz, ülke ve URL kırılımı korunmalı. Türkiye/Türkçe ile İngilizce ziyaretçi davranışını tek ortalamaya karıştırmayın. 29 Ekim tatili ve turizm mevsimselliği sonuçları etkileyebilir. Önceki SEO sürümleri de aynı dönemde değiştiği için sonuç bu yamaya tek başına atfedilemez.

**Dönüşüm:** Mevcut `pusula:interaction` olayları kalıcı analitik servisine gönderilmiyor. Bir analitik hesabı ve uygun veri tercihleri belirlenmeden gerçek dönüşüm paneli oluşmaz. Menü geçişi, telefon, harita ve WhatsApp açılışı ayrı olaylar olarak raporlanmalı. İsim, telefon, mesaj, masa tarihi veya serbest metin notu analitiğe taşınmamalı. WhatsApp açılışı rezervasyon veya müşteri değildir; işletme onaylanan masa ve gerçekleşen ziyareti ayrıca saymalı.

**İkinci–dördüncü hafta:** Gerçek yakın oteller ve ziyaretçi danışma ekipleri için menü/konum/rezervasyon bağlantılarından oluşan kısa bir bilgi kartı hazırlanabilir. İletişime geçmeden önce işletme tarafından hedefler ve mesaj onaylanmalı. Bu çalışma kapsamında kimseye mesaj gönderilmedi. Gerçek ziyaretçilerden dürüst geri bildirim istenebilir; teşvikli veya sahte yorum kullanılmamalı.

**Karar kuralları:** Gösterim yoksa önce dizine eklenme ve içerik uyumunu; gösterim var ancak tıklama azsa sorgu ve arama önizlemesini; ziyaret var ancak talep azsa fiyat, adres ve rezervasyon akışını inceleyin. Her hafta başlık değiştirmek yerine yeterli veri birikmesini bekleyin. GEO için alıntı gözlemini, referans trafiğini ve gerçek müşteriyi ayrı ölçün.

## Doğrulama sonucu

- 40 sayfa / 182 yapılandırılmış veri nesnesi: teknik SEO denetiminde hata yok.
- Dört dilde 76 menü maddesi ve 84 fiyat teklifi kontrolü geçti.
- Altı dilde rezervasyon, WhatsApp, form ve kişisel veri içermeyen etkileşim testleri geçti.
- 320, 390, 768 ve 1440 piksel genişliklerinde toplam 160 sayfa kontrolü geçti: taşma, kırık görsel, font ve CSP hatası yok.
- Yeni iki bölüm ve ilgili menü maddesine geçiş JavaScript kapalıyken doğrulandı; mobil ekran görüntüsü incelendi.
- Geçici kopyada üç fiyat değiştirildi: serpme ve iki bireysel tabağın iki dilde güncellenmesi doğrulandı.
- Tam yayın yeniden üretildiğinde dosyalar byte düzeyinde aynı kaldı; `git diff --check` temiz.

Bunlar yerel teknik kontrollerdir; gerçek kullanıcı Core Web Vitals veya trafik artışı ölçümü değildir.
