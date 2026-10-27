# Reservation pages — 27 October 2026

Six static pages: `/rezervasyon/`, `/{en,ru,ko,ar,zh}/reservation/`.

- One shared form, stylesheet and validation script. A compact mobile form leads the page; a real restaurant photograph and visitor information support the booking decision. The existing yellow/cream/green/red Pusula palette and self-hosted Kalam/Source Sans identity are retained. Cyrillic, Arabic, Korean and Chinese headings use self-hosted, licensed Noto subsets.
- Localized titles, descriptions, Open Graph/Twitter previews, reciprocal hreflang, self-canonicals, breadcrumbs and Restaurant/WebSite/WebPage/FAQPage entities. The visible FAQ matches schema text. Address, phone and breakfast service hours come from the existing published business information; no new ratings, proximity distances or availability claims were invented.
- WhatsApp uses same-tab `https://wa.me/905078162994?text=…` navigation within the submit gesture, avoiding popup blockers. This opens a draft: the guest must press Send in WhatsApp, and staff must confirm the reservation. No delivery or completed booking is asserted or measured. Copy, edit, SMS and phone fallbacks remain on the page. There is no backend, storage or logging of guest details.
- Istanbul date/time validation applies regardless of guest timezone. Phone input handles Arabic/Persian numerals. Message encoding preserves Unicode, ampersands, plus signs, newlines and special characters. Anonymous events contain only name, route and language.
- Versioned assets, SRI and the existing hash-based script CSP are updated together. Existing script permissions are preserved. Localized `index.html` paths redirect to canonical directory routes.

## Maintenance

The deployment checkout is `/Users/baran/Desktop/pusula-lounge-github`; Vercel serves this repository root. Generate updated HTML after changing translations, CSS or JS:

```sh
python3 scripts/build_reservations.py .
python3 scripts/strengthen_reservation_discovery.py .
python3 scripts/check_reservations.py .
```

Only rerun `vendor_reservation_fonts.py .` when heading/caption characters change. It downloads matching Google Fonts subsets and adjacent SIL licenses. Existing reservation font declarations are replaced when rerun.

For isolated DOM interaction tests, install jsdom outside the deployment directory and supply its path:

```sh
npm install --prefix /tmp/pusula-reservation-qa jsdom --no-audit --no-fund
JSDOM_PATH=/tmp/pusula-reservation-qa/node_modules/jsdom node scripts/test_reservations.cjs .
```

Validation: six-language static SEO/asset/CSP checks and DOM interaction tests pass. Browser inspection covered a 1280px desktop composition, 390px mobile pages in all languages, 320px English/Russian/Arabic, and the mobile submit/contact section. The design detector reported only the cream palette, intentionally preserved from the existing Pusula brand. No WhatsApp messages were sent during testing; actual delivery requires the guest’s action in WhatsApp.

Search visibility and customer conversion must be measured after indexing; these changes do not guarantee rankings or reservations. Google guidance: https://developers.google.com/search/docs/specialty/international/localized-versions and https://developers.google.com/search/docs/appearance/structured-data/local-business.
