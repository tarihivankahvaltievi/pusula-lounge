# Pusula Lounge — SEO/GEO, fiyat kararları ve yerel müşteri kazanımı

29 Ekim 2026 · Başlangıç: `ade9726` · Kaynak/yayın deposu: `tarihivankahvaltievi/pusula-lounge`.

## Yönetici değerlendirmesi

Sitede teknik SEO, çok dilli içerik, fiyatlı kahvaltı menüsü, ulaşım rehberleri ve masa talebi akışları zaten mevcut. Yeni turda dört dilde menüye, porsiyon toplamını kişi başına hesaplanan tutardan ayıran erişilebilir bir karşılaştırma eklendi. Bu, fiyatı yanlış yorumlayarak ayrılma ihtimaline yönelik bir dönüşüm hipotezidir; müşteri veya CTR artışı ölçülmüş değildir.

Büyüme için sonraki yüksek değerli işler: işletme kayıtlarında adres tutarlılığını doğrulamak, gerçek arama performansını edinmek ve kahvaltı dışındaki doğrulanmış menüyü tamamlamak. Daha fazla benzer blog açmak bu eksiklerin yerine geçmez.

## Yöntem ve sınırlar

- Mevcut kaynak/üretim zinciri, menü fiyatları, dört dilde ziyaret akışı ve önceki araştırmalar incelendi. Eski `pusula lounge 2/site/` kopyası kullanılmadı.
- Site haritasındaki 40 URL canlı HTTP isteğiyle tarandı: tamamı 200 döndü, canonical kendi URL'siydi ve HTTP başlığında noindex görülmedi. Ham kayıt: `menu-budget-live-audit-2026-10-29.json`. Bu kontrol yayın öncesi teknik erişilebilirlik kanıtıdır; Google dizinine girdiğini kanıtlamaz ve gerçek Googlebot/CDN erişim testi değildir.
- Nitel sorgu örnekleri: `Pusula Lounge Taksim`, `Pusula Lounge breakfast`, `Pusula Lounge Sinek`, `Taksim Van kahvaltısı restoran menü`, `Turkish breakfast Taksim restaurant menu`. Sonuçlar kişiselleştirilmiş Google sırası, arama hacmi veya pazar payı ölçümü değildir.
- Search Console, işletme profili ve kalıcı analitik verisine erişim yok. Mevcut tarayıcı olayları bir analitik sunucusuna gönderilmiyor; geçmiş tıklama, dönüşüm veya gelir uydurulmadı.

## Araştırma bulguları ve kararlar

### 1. SEO ile GEO aynı doğrulanmış bilgiye dayanmalı

[Google'ın üretken AI rehberi](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide), yararlı ve işletmeye özgü içerik ile temel SEO'yu öneriyor. Özel AI dosyaları ve yapay anahtar kelime çoğaltımı Google görünürlüğüne ayrı bir avantaj sağlamıyor. [AI özellikleri rehberi](https://developers.google.com/search/docs/appearance/ai-features), arama sonuçlarında snippet göstermeye uygun ve dizine eklenmiş içerik gerektiğini açıklıyor.

Karar: ziyaretçinin fiyat sorusunu, görünür HTML'de gerçek menü verisiyle yanıtlamak. Gizli AI metni, gereksiz yeni URL, yapay yorum veya özel GEO şeması eklenmedi. Yeni bölüm native `details` içinde; metin ilk HTML yanıtında var, kullanıcı klavye veya dokunmayla açabiliyor. Google'ın bu bölümü göstereceği/alıntılayacağı garanti edilmiyor.

### 2. Fiyat anlamı müşteri kararını etkiliyor

Mevcut [Türkçe menü](https://www.pusulalounge.com/menu/) iki kişilik 1.200 TL, üç kişilik 1.800 TL, dört kişilik 2.500 TL listeliyor. Bölme işlemiyle kişi başına 600 / 600 / 625 TL elde ediliyor. Dört kişilik fiyatı iki kişiliğin iki katı varsaymak yanlış olur.

Dört menüye aynı kaynak veriden üretilen tablo eklendi. Açıklama hesaplanan değerin ayrı sipariş verilebilen bir menü olmadığını, ilavelerin dahil olmadığını ve sınırsız çayın serpme kahvaltıda listelendiğini söylüyor. Kullanıcı hem serpme içeriğine hem tek kişilik tabağa doğrudan geçebiliyor. Masa talebi ve yol tarifi önce kalıyor; kıyaslama başlangıçta kapalı olduğu için ürün listesini gereksiz yere aşağı itmez.

[Karşılaştırmalı yerel örnek](https://www.tarihivankahvaltievi.com/van-kahvaltisi) kişi başı ücret ve minimum servis koşulunu ürünle birlikte açıklıyor. İşletme ilişkisi bu araştırmada belirlenmedi; bu sayfa bağımsız rakip olarak varsayılmadı. Örnek, Pusula'nın kendi porsiyon modelini açık anlatma gereğini destekliyor; oradaki fiyat ve koşullar Pusula'ya aktarılmadı.

### 3. Adres/kategori tutarlılığı dış keşifte öncelikli

[Yandex Beyoğlu barlar listesinde](https://yandex.com.tr/maps/115695/beyoglu/category/bar_pub/184106384/) Pusula Lounge için Küçük Parmak Kapı Sokak 4 yazıyor. [SageNearby kaydı](https://sagenearby.com/tr/detail/pusula-lounge), sitedeki Sinek Çıkmazı No:3 ve +90 507 816 29 94 ile örtüşen bilgiler gösteriyor. [Restaurant Guru kaydı](https://de.restaurantguru.com/pusula-lounge-Istanbul) da Sinek Çıkmazı 3 ve aynı telefonu gösteriyor.

Bu, olası bir kayıt tutarsızlığıdır; Yandex profil detayına bu araçla erişilemediğinden aynı fiziksel işletme/pin eşleşmesi kesinleştirilmedi. İşletme sahibi önce telefon, konum pini ve giriş fotoğrafını karşılaştırmalı; aynı kayıtsa adres düzeltmesi yapmalı. Dış platform verisi esas alınarak sitenin doğrulanmış adresi değiştirilmedi.

[Google yerel sıralama rehberi](https://support.google.com/business/answer/7091?hl=en), eksiksiz işletme bilgisi ile alaka, mesafe ve bilinirliği vurguluyor. İşletme profillerindeki gerçek kategori, kahvaltı menüsü, çalışma/servis saatleri ve giriş adresi kullanıcı beklentisiyle eşleşmeli. Dizinlerde görülen puan, fiyat aralığı veya erişilebilirlik iddiaları doğrulanmadan siteye taşınmamalı.

### 4. Teknik temel büyük ölçüde hazır

40 sayfanın yerel taramasında canonical, karşılıklı hreflang, iç bağlantılar/fragmentler, dosyalar, tekil başlıklar, taranabilirlik, CSP/SRI ve 182 yapılandırılmış veri nesnesi kontrol edildi. Dört dilde menü 76 ürün ve 84 fiyat teklifi içeriyor. Altı rezervasyon dili korunuyor.

[Çok dilli sayfa rehberi](https://developers.google.com/search/docs/specialty/international/localized-versions) karşılıklı dil ilişkilerini; [LocalBusiness rehberi](https://developers.google.com/search/docs/appearance/structured-data/local-business) görünür işletme bilgilerinin doğru işaretlenmesini destekliyor. Hesaplanan kişi başı rakamlar yeni Offer olarak yazılmadı: gerçekte ayrı satılan ürünler değiller. [FAQ zengin sonuç kısıtları](https://developers.google.com/search/blog/2023/08/howto-faq-changes) nedeniyle bu restorana FAQ schema ekleyerek Google'da geniş sonuç vaat edilmedi.

[Görsel arama rehberi](https://developers.google.com/search/docs/appearance/google-images) gerçek ve ilgili görselleri öneriyor. Mevcut görsel site haritası/primaryImageOfPage ilişkileri korundu; sırf SEO için yeni illüstrasyon eklenmedi.

### 5. Akşam menüsü ve ölçüm hâlâ büyüme fırsatı

Ana sayfada akşam yemekleri, tatlı ve kahve anlatılıyor; yayımlı fiyatlı menü esasen kahvaltı. Gerçek akşam/içecek ürünleri ve fiyatları doğrulanınca mevcut menünün genişletilmesi, benzer içerikli yeni sayfalardan daha doğrudan müşteri sorusunu çözer. Şimdiki akşam rehberi ekipten güncel menü sorulmasına yönlendiriyor.

[Google'ın Search Console/Analytics ölçüm rehberi](https://developers.google.com/search/docs/monitor-debug/google-analytics-search-console), aramada gösterim/tıklama ile site içi davranışın farklı ölçümler olduğunu açıklıyor. `reservation_page_click` veya WhatsApp açılışı gerçekleşmiş rezervasyon değildir.

## Sorgu → sayfa → müşteri adımı

| Niyet / örnek sorgu | Öncelikli sayfa | Kullanıcının kararı |
| --- | --- | --- |
| Pusula Lounge menü, Pusula kahvaltı fiyatı | `/menu/` | Toplam/kişi başı ayrımı → ürün içeriği → masa talebi |
| Taksim serpme kahvaltı, Van kahvaltısı | `/kahvalti/` | Sofra/porsiyon seçimi → menü → kahvaltı talebi |
| Turkish breakfast Taksim price per person | `/en/menu/`, `/en/breakfast/` | TRY toplamı ve hesaplanan maliyet → İngilizce talep |
| Турецкий завтрак Таксим цена | `/ru/menu/` | Rusça içerik/fiyat → aynı dilde talep |
| فطور تركي تقسيم السعر | `/ar/menu/` | Arapça içerik/fiyat → aynı dilde talep |
| Pusula Lounge adres / directions | `/konum/` ve dil eşleri | Doğru giriş → yürüyüş rotası |
| Taksim akşam yemeği, waffle/kahve | Mevcut TR/EN akşam rehberi | Güncel ürün/fiyatı işletmeden öğrenme |

Bu bir içerik eşlemesidir; hacim veya sıralama tahmini değildir.

## Yayın sonrası uygulama ve ölçüm planı

1. **İlk hafta:** sahibi erişimiyle Google/Yandex kayıtlarında ad, telefon, giriş adresi, pin, kategori ve menü bağlantısını kontrol edin. Öncelik olası No:4 / No:3 farkı. Gerçek giriş ve sofra fotoğrafları kullanın. Hesap erişimi olmadan bu değişiklikler yapılmadı.
2. **İlk hafta:** Search Console'da dört menü URL'sinin dizin/canonical durumunu inceleyin; gerekiyorsa güncellenen URL'leri inceleme aracıyla bildirin. Yeni sitemap zaten aynı canonical URL'leri koruyor.
3. **28 günlük takip:** 30 Ekim–26 Kasım dönemini 2–29 Ekim ile karşılaştırın. Marka/marka dışı, ülke, dil, cihaz ve landing page kırılımı kullanın. Önceki dönemde de çok sayıda yayın yapıldığı için değişimi yalnız bu tabloya bağlamayın; resmi tatil, sezon, sorgu bileşimi ve ortalama konum değişimini not edin.
4. **Gerçek sonuç zinciri:** arama gösterimi → tıklama/CTR → menü ziyaretleri → gönderilmiş masa talebi → işletmenin onayladığı masa → gerçekleşen ziyaret. Son üç aşama ekip kayıtlarıyla ayrı doğrulanmalı. Kişisel mesaj/telefon/form alanlarını analitik olaylara taşımayın.
5. **Önceliklendirme:** gösterim yüksek, CTR düşük ve konum benzerse başlık/açıklama uyumunu test edin. Trafik var ama talepler azsa fiyat/ürün/rezervasyon anlaşılabilirliğini inceleyin. Dizin sorunu varsa yeni içerikten önce teknik nedeni giderin.
6. **Gerçek menü:** kahvaltı dışı fiyat ve içerik sağlandığında TR/EN/RU/AR katalogları tek kaynaktan genişletin; günlük bulunurluk ve servis saatlerini ayrıca doğrulayın.

## Doğrulama ve bakım

- `check_menu_budget.py`: dört dilde aritmetik, kaynak fiyat değişikliğinin aktarılması, tekrar üretim ve sahte Offer eklenmemesi.
- `test_menu_budget.cjs`: 32 kombinasyonda 320/390/768/1440 px, JavaScript açık/kapalı, klavye açılışı, RTL, taşma, ürün bağlantıları, CTA sırası ve tarayıcı/CSP hataları geçti.
- Mevcut müşteri akışı testleri: 24 kontrol geçti; ürün arama/sıfırlama, kahvaltı talebi önseçimi ve anonim olaylar korundu.
- Mobil TR/EN/RU/AR ekran görüntüleri gözle incelendi. Mekanik tasarım tarayıcısı yeni bölüm dışında mevcut arama alanı, doku ve tipografi için uyarı verdi; SEO/fiyat kapsamı dışında mevcut tasarım değiştirilmedi.
- Tam yayının tekrar üretiminde değişmeyen dosyaların hash'leri ayrıca kontrol edilir. Tarihler sadece son çıktı değiştiğinde güncellenir.
- Kaynak: `scripts/build_menu_budget.py`; görünüm: `menu-budget.css`. Fiyatı Türkçe menüde güncelleyip tam build çalıştırın; çeviri tablolarına bağımsız fiyat yazmayın.
