# Pusula Lounge: local discovery and evening visits — 28 October 2026

## Research and decisions

The current site already had a detailed Van breakfast menu and local breakfast pages, but its homepage mentioned pizza, burgers, fish, salads, coffee and desserts without linking those services to a useful visitor page. Its public menu only listed breakfast dishes. The new work connects the existing food and drink categories to a bilingual visit guide and a table request.

Search examples reviewed included `Taksim akşam yemeği`, `Beyoğlu waffle`, `Taksim kahve tatlı`, `dinner Taksim`, and `waffles coffee Taksim`. These were qualitative query checks, not Search Console data, keyword-volume estimates or ranking measurements. Exact waffle varieties, current evening dishes and their prices were not reliably documented on the first-party website, so the guide does not invent them; it tells visitors to confirm the current selection and price with the team.

Google's local ranking documentation describes relevance, distance and prominence. Site changes can improve the information available for relevant searches, but cannot change the searcher's distance or guarantee a map position. Google's AI-search guide says existing SEO practices still apply and emphasizes crawlable, useful, original information; it does not require a special GEO schema or keyword-stuffed text.

## Applied

- Added `/blog/taksimde-aksam-yemegi-waffle-kahve/` and `/en/blog/dinner-waffle-coffee-taksim/` with original visit planning, a real Pusula Lounge interior photograph, accessible editorial styling, menu and location links, and a WhatsApp reservation CTA.
- Added a sourced breakfast-to-culture guide for Salt Beyoğlu, Pera Museum and Istanbul Modern, with official visitor pages, addresses and schedule caveats rather than a templated list of nearby attractions.
- Renamed the Turkish/English journal as a food and visit guide and updated its discovery copy so breakfast and evening visits live in one coherent editorial section.
- Made the homepage's dinner and coffee/dessert cards navigable; explicitly names waffle, tea and coffee and links visitors to the guide.
- Broadened Turkish and English reservation title, description, heading, copy and FAQ from breakfast-only to table requests for breakfast, dinner and waffle visits. The WhatsApp request still requires staff confirmation.
- Added localized, mobile-friendly arrival guidance on the location pages, with verified Metro İstanbul route links, one-tap directions/call, copyable address and a printable visit card. Put directions and reservation actions before long menu lists in the visitor menus.
- Subsetted existing licensed home fonts using the site's published text while preserving glyph metrics and keeping original font files; no new display-font trend was introduced.
- Preserved the breakfast service window as 08:00–17:00 and instructed visitors to confirm evening availability, current dishes and prices directly. General hours were not used as a promise that every menu item is served at every hour.
- Kept the current custom type and editorial system; no new typeface, third-party embed or generated hero image was introduced for the guide.

## Measurement and limitations

No Google Search Console, Google Business Profile or reservation-confirmation data was available in this session. No search-volume, indexing, top-ranking or booking-growth result is claimed. After publication, compare non-brand evening/dessert/coffee queries and landing pages in Search Console, and count WhatsApp table requests separately from staff-confirmed reservations.

Google Business Profile should carry the same live menu, reservation URL, category, hours, entrance pin, phone and genuine recent food/interior photos as the site. Check the entrance pin against the exact Sinek Çıkmazı No:3 address before changing any directory listing. Encourage real customers to leave honest reviews without incentives.

## Sources

- [Google Business Profile: improve your local ranking](https://support.google.com/business/answer/7091?hl=en)
- [Google Search Central: AI features and your website](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)
- [Google Search Central: helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)
- [Salt Beyoğlu — official visitor information](https://saltonline.org/en/visit)
- [Pera Museum — official visitor information](https://peramuseum.org/Home/Visit)
- [Istanbul Modern — official visitor information](https://www.istanbulmodern.org/en/visit/museum)

## Rebuild

From the release root, run:

```sh
python3 scripts/build_tourism_seo.py .
python3 scripts/build_reservations.py .
python3 scripts/optimize_home_fonts.py .
python3 scripts/build_international_seo.py .
python3 scripts/build_visitor_quality.py .
```
