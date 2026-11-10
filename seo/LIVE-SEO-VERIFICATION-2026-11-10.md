# Canlı SEO ve GEO doğrulaması — 10 Kasım 2026

GitHub yayın deposu ve canlı site incelendi. Sitenin mevcut kapsamlı araştırması ve önceki uygulamalar için `SEO-GEO-RESEARCH-2026-11-10.md` belgesine bakın.

## Canlı kontroller

- Canlı sitemap'teki 40 URL 200 HTML yanıtı verdi, başka bir URL'ye yönlenmedi, kendisini canonical gösterdi ve robots veya X-Robots-Tag içinde noindex/nosnippet engeli taşımadı. `python3 scripts/check_live_indexability.py` bu kontrolü tekrarlamak için eklendi.
- `robots.txt` sitemap'i bildiriyor ve genel taramaya izin veriyor. Örnek olmayan bir URL 404 döndü; HTTP ve www olmayan alan adı HTTPS www adresine 308 ile yönlendi.
- Depodaki 40 sayfada tek H1, başlık, açıklama ve canonical mevcut; yerel bağlantılar, fragment hedefleri ve görsel alt nitelikleri kontrol edildi.
- Turizm, uluslararası SEO, rezervasyon, arama içeriği, metadata ve menü karşılaştırması doğrulayıcıları geçti. Bu kontroller Google dizini veya gerçek sıralama ölçümü değildir.

## Araştırmanın sonucu ve takip

[Google'ın üretken arama kılavuzu](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide), AI görünürlüğü için özgün ve yararlı içerik, erişilebilir teknik yapı ve normal SEO temellerini önerir; özel AI şeması veya llms.txt gerektirmez. [Yerel sıralama rehberi](https://support.google.com/business/answer/7091?hl=en) alaka, mesafe ve bilinirliği temel faktörler olarak açıklar. Bu nedenle site kodu birinci sıra garantisi veremez.

İşletme sahibi Search Console'da sitemap ve ana sayfaların gerçek dizin durumunu, marka dışı sorguları, tıklama ve gösterimleri; İşletme Profili'nde ise gerçek adres/pin, saat, kategori, menü ve iletişim bilgilerini kontrol etmeli. Saat ve adres gibi işletme gerçekleri hesap veya işletme yetkilisiyle teyit edilmeden değiştirilmedi. Gerçek kullanıcı performansı için Search Console Core Web Vitals raporu kullanılmalı; bu denetim alan verisi ölçmedi. [Google sayfa deneyimi rehberi](https://developers.google.com/search/docs/appearance/page-experience) iyi metriklerin üst sıra garantisi olmadığını belirtir.
