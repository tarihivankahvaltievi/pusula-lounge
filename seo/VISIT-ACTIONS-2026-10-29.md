# Ulaşım ve masa talebi: ikinci iyileştirme turu

29 Ekim 2026 · Başlangıç commit'i: `4f98194`.

## Tespit

Dört dildeki konum sayfaları doğru adres ve ulaşım bilgilerini içeriyordu, ancak yürüyüş rotası, adres kopyalama ve ziyaret kartı araçları uzun içeriklerin arkasındaydı. İngilizce ana sayfa masa talebinden söz ediyor, fakat ilk içerik bölümünde doğrudan bir talep bağlantısı sunmuyordu. Türkçe ana sayfadaki “Yol tarifi” bağlantısı ise bir yürüyüş rotası yerine Google işletme kaydını açıyordu.

Bu tur yeni sayfa, fiyat veya hizmet iddiası eklemez. Arama başlıkları ve önceki CTR denemesi korunur. Mevcut ziyaret bilgisi ve eylemler daha erken sunulur.

## Değişiklikler

1. Türkçe, İngilizce, Rusça ve Arapça konum sayfalarında ulaşım kartı girişin hemen arkasına taşındı. Adresin ardından rota ve telefon eylemleri geliyor. Kopyalama, yazdırma, resmî ulaşım kaynakları ve özel erişim ihtiyaçlarına ilişkin bilgi korundu.
2. İngilizce ana sayfanın girişine kahvaltı masa talebi, menü/fiyat ve yürüyüş bilgisi bağlantıları eklendi. Talep bağlantısı kahvaltı seçimini rezervasyon formuna geçiriyor; masayı işletme onayı kesinleştiriyor.
3. Türkçe ana sayfanın mevcut “Yol tarifi” bağlantısı artık tam işletme adresine Google yürüyüş rotası açıyor. Başlangıç noktası veya cihaz konumu site tarafından alınmıyor.
4. Yorum, yürüyüş rotası ve işletme profili tıklamaları ayrı anonim tarayıcı olayları oldu. Yorum bağlantıları açıkça işaretlendi; sorgu içeriği, rota başlangıcı veya form verisi olaylara taşınmıyor.

## Ölçülen yerleşim farkı

Yerel Chrome önizlemesi, 390 × 844 CSS piksel, fontlar yüklendikten sonra bağlantının belgenin üstünden uzaklığı. Bunlar tek bir ekran boyutundaki yerleşim ölçümleridir; yüklenme hızı, tıklama veya dönüşüm artışı değildir.

| Sayfa / eylem | Önce | Sonra |
| --- | ---: | ---: |
| Türkçe konum: yürüyüş rotası | 2.817 px | 743 px |
| İngilizce konum: yürüyüş rotası | 2.769 px | 743 px |
| Rusça konum: yürüyüş rotası | 2.655 px | 797 px |
| Arapça konum: yürüyüş rotası | 2.632 px | 773 px |
| İngilizce ana sayfa: ilk içerik masa talebi | 1.783 px | 637 px |

İngilizce ana sayfanın üst gezinmesinde zaten bir rezervasyon bağlantısı vardı. Tablodaki karşılaştırma ana içerikteki ilk masa talebi içindir. Diğer ekran genişliklerinde yazı satırları ve konumlar değişir. Ham değerler `visit-actions-layout-2026-10-29.json` dosyasındadır.

## Olay sözleşmesi

| Olay | Anlamı |
| --- | --- |
| `reviews_click` | İşaretlenmiş gerçek Google yorum bağlantısı açıldı. |
| `directions_click` | Google Maps yürüyüş rotası bağlantısı açıldı. |
| `map_profile_click` | İşletme harita/profil bağlantısı açıldı. |
| `reservation_page_click` | Masa talebi sayfasına geçildi; rezervasyon gerçekleştiği anlamına gelmez. |

Mevcut menü, telefon ve WhatsApp olayları korunur. Yeni ayrım nedeniyle eski toplam profil tıklamaları yeni dönemle doğrudan karşılaştırılmamalı: daha önce rota tıklamaları da profil olayına dahil olabiliyordu. İleride bir analitik hesabı bağlanırsa geçiş tarihi rapora not düşülmeli.

Kalıcı analitik sistemi bu görevde kurulmadı. Olaylar yalnızca `{name, path, language}` içerir ve tarayıcı içinde yayınlanır. Gerçek onaylanan masa ve ziyaret ayrıca ölçülmelidir. Henüz trafik veya müşteri artışı iddiası yoktur.

## Doğrulama

- 40 sayfa, 182 yapılandırılmış veri nesnesi; canonical, iç bağlantılar, dil ilişkileri, dosyalar ve CSP/SRI kontrolleri geçti.
- Dört dilde menü ve altı dilde rezervasyonun statik kontrolleri geçti.
- Ulaşım kartlarında dört ekran genişliği/dört dil için kopyalama, yedek kopyalama, yazdırma, rota ve içerik sırası doğrulandı. JavaScript kapalıyken de adres ve rota erişilebilir.
- İngilizce ana sayfanın yeni bağlantıları JavaScript kapalıyken de bulunuyor.
- Altı dilde olay testleri yorum/rota/profil ayrımını ve kişisel veri içermeyen olay alanlarını doğruluyor. Benzer yazılmış farklı alan adları Google bağlantısı olarak sayılmıyor.
- Tam yayın ikinci kez üretildiğinde çıktı dosyaları aynı kaldı. Mobil görünüm Türkçe, İngilizce, Rusça ve Arapçada incelendi. Mevcut tipografi ve alt bölümlere ilişkin tasarım tarayıcısı önerileri bu dar değişikliğin dışında bırakıldı.
