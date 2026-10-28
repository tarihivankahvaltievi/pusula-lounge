# İkinci tur: ziyaret kalitesi, yerel içerik ve yükleme maliyeti

28 Ekim 2026. İlk incelenen sürüm `bb2930e`; eşzamanlı akşam yemeği/waffle yayını `3644f05` korunarak son sürüme dahil edildi. Bu çalışma dört dilde mevcut ulaşım sayfalarını derinleştirir; aynı niyet için çok sayıda semt sayfası üretmez.

## Yeni araştırma ve kararlar

Arama örnekleri: Pusula'nın İngilizce/Almanca işletme kayıtları, Taksim kahvaltı menüleri, resmî metro aktarmaları ve Beyoğlu kültür kurumlarının ziyaret sayfaları. Kamuya açık yorumlarda sipariş dilinin anlaşılması ve konum önem taşıyor; yorumlar kendi sitenize kopyalanmadı. Arama hacmi veya güncel sıralama verisi varmış gibi davranılmadı. Önceki turda bulunan dış adres farkı bu turda da hesap erişimi olmadan düzeltilmiş sayılmıyor.

Kaynaklar ve nasıl kullanıldıkları:

| Birincil kaynak | Kullanım |
| --- | --- |
| [Metro İstanbul M2](https://metro.istanbul/Hatlarimiz/HatDetay?hat=M2), [T1](https://www.metro.istanbul/Hatlarimiz/HatDetay?hat=T1), [F1](https://www.metro.istanbul/en/Hatlarimiz/HatDetay?hat=F1) | Taksim’e metro bağlantısı ve Kabataş aktarması |
| [Metro İstanbul](https://metro.istanbul/) | Ziyaret gününde sefer duyurularına erişim |
| [Google Maps URL belgeleri](https://developers.google.com/maps/documentation/urls/get-started) | Anahtarsız, adresle çalışan yürüyüş yönlendirme bağlantısı |
| [Salt ziyaret sayfası](https://saltonline.org/en/visit), [Pera Müzesi ziyaret sayfası](https://peramuseum.org/Home/Visit), [İstanbul Modern ziyaret sayfası](https://www.istanbulmodern.org/en/visit/museum) | Kültür rehberinin kurum/adres/gün bilgileri ve doğrudan güncel kaynağa geçiş |
| [Google görsel SEO rehberi](https://developers.google.com/search/docs/appearance/google-images) | İlgili bağlam ve doğru dilde görsel açıklamaları |
| [Chrome LCP analizi](https://developer.chrome.com/docs/performance/insights/lcp-breakdown) | Büyük açılış görselinin kaynak ve çizim gecikmesinin ayrılması |
| [web.dev content-visibility](https://web.dev/articles/content-visibility) | Sayfa altındaki dil fontlarının ilk çizime yük bindirmemesi |

Ulaşım için ücret, sabit toplam yolculuk süresi, belirli istasyon çıkışı veya kesintisiz hizmet garantisi verilmedi. Harita bağlantısı gerçek tam işletme adresini kullanır; başlangıç noktası uydurmaz ve site konum izni istemez. Harita uygulaması ziyaretçinin kendi başlangıç noktasını kullanabilir.

Yeni TR/EN kültür yazısı Salt Beyoğlu, Pera ve İstanbul Modern'i üç alternatif durak olarak ele alır. Bilet satışı, kurumlarla ortaklık veya rehberli tur iddiası yok. Geçici sergi ve bilet fiyatları kopyalanmadı; ziyaret günündeki resmî sayfalara bağlantı var. Yazıların yayın tarihi 28 Ekim 2026. Gerçek Pusula görseli kullanıldı; müzede çekilmiş gibi sahte bir görsel üretilmedi.

## Uygulanan ekler ve düzeltmeler

- Türkçe, İngilizce, Rusça ve Arapça konum sayfalarında M2/Taksim, T1/Kabataş/F1 ve son yürüyüş bölümü. Türkçe adresi kopyalama, klavyeyle kullanılabilir kontroller ve sade yazdırma düzeni olan ziyaret kartı.
- JavaScript olmadan tam adres, telefon ve harita bağlantısı kullanılabilir; çalışmayacak kopyala/yazdır düğmeleri gösterilmez. Kopyalama izni yoksa metin seçilerek cihazın kopyalama seçeneği önerilir.
- İngilizce/Rusça/Arapça menülerde masa talebi ve ulaşım bağlantıları 19 ürünün önüne taşındı. Arapçada saat ve aktarma dizilerinin okuma yönü korundu.
- Türkçe tek kişilik kahvaltı tabağındaki sınırsız çay görseli kaldırıldı: metin yalnız “çay” diyordu. Bu görselin ARIA hatası da böylece ortadan kalktı. Serpme kahvaltının metindeki sınırsız çay bilgisi korunuyor.
- Blog üreticisindeki varsayılan fotoğraf açıklaması/altyazısının TR/EN sırası düzeltildi; özel makale görselleri desteklenmeye devam ediyor.
- Tek bir `build_release.py` girişi, font bağımlılıkları ve README. Yalnız eski üç build adımını çalıştırıp yeni ziyaretçi özelliklerini kaybetme riski azaltıldı.

## Ölçüm ve sınırları

İlk mobil Lighthouse laboratuvar ölçümünde ana sayfa 76 performans, 100 erişilebilirlik ve 100 SEO; LCP yaklaşık 7,0 saniyeydi. Menü aynı koşullarda 99/100/100 ve yaklaşık 1,5 saniye LCP verdi. Bunlar yerel önizlemede, simüle mobil koşullarda alınan tekil başlangıç ölçümleridir; gerçek ziyaretçi Core Web Vitals veya Google sıralaması değildir.

13 mevcut font girdisi 714.856 bayttan 176.680 bayta indi: dosya toplamında yaklaşık %75 azalma. Orijinal fontlar ve OFL lisansları tutuldu. Türetilen fontlar Pusula iç adlarını kullanıyor; yayımlanan karakter kapsamı ve her karakterin advance width değeri üretimde kontrol ediliyor. Harf çizimleri ve ölçüleri değiştirilmedi. Yeni bir karakter eklendiğinde ilgili fontun cache URL'sinin de yenilendiği ayrı fixture ile doğrulandı.

Sonraki yerel ölçümlerde ana sayfanın toplam ilk yük aktarımı yaklaşık 1.221 KiB'den 972 KiB'ye geriledi. Tekil performans puanları 79–84, LCP 4,5–5,6 saniye aralığında değişti. Bu değişken ölçümler bir saha performans garantisi değildir; başlangıç yükünün azalması daha sağlam bulgudur. LCP'nin 2,5 saniyelik iyi eşik altında olduğu iddia edilmiyor. Canlı CrUX/Search Console verisiyle ayrıca değerlendirilmelidir.

Otomatik WCAG kontrolleri manuel erişilebilirlik denetiminin yerine geçmez. İlk masaüstü taramasında tek kişilik tabağın dekoratif çay etiketinde geçersiz ARIA görüldü; görsel ve çelişkili iddia birlikte kaldırıldı. Yeni butonlar ve durum mesajları ayrıca klavye, kopyalama geri dönüşü ve JavaScript kapalı durumda denendi.

## Yayın öncesi doğrulama

Tam üretim tekrarlandığında çıktı değişmedi. 40 canonical sayfada SEO, sitemap, iç bağlantı, JSON-LD, dil eşleşmesi, SRI ve CSP kontrolleri geçti; dört dilde 84 fiyat kaydı ve altı dilde rezervasyon akışı korunuyor. Dört ekran genişliğinde tüm sayfalar kontrol ediliyor. Ziyaret kartları ayrıca dört dil × dört genişlikte 16 kombinasyonda kopyalama, geri dönüş, yazdırma, harita hedefi ve kişisel veri taşımayan olaylar açısından test edildi.

Kanıtlar çalışma klasörünün `audit-seo-round2-2026-10-28/` dizininde. Kaynak araştırmasının sonucunu trafik veya müşteri artışı olarak raporlamayın; bunlar analitik ve işletme teyidi gerektirir. Önceki rapordaki Search Console/işletme profili işleri hesap erişimi gerektirmeye devam eder.

## Bakım

Kök README'deki `python3 scripts/build_release.py .` komutunu kullanın. Fiyat ve işletme saati değişikliklerini gerçek kaynaktan doğrulayın. Kültür/ulaşım bilgilerinin kontrol tarihini ancak yeniden kontrol ettiğinizde güncelleyin; eski makalelerin yayın tarihini yenilemeyin. Yayınlandıktan sonra site çıktısı ve yönlendirmeler ayrıca HTTP üzerinden doğrulanmalı.
