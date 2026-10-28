# Taksim local discovery and reservation improvements

Research date: 28 October 2026. This is a qualitative review of the published site and official search-platform guidance. No keyword-volume, Search Console, Google Business Profile, analytics, or live rank data was available in this workspace.

## Search intent and current site

The site already has a Turkish breakfast menu with published prices, a Taksim/Beyoğlu location route, breakfast information, a bilingual dinner/waffle/coffee guide, and reservation routes in six languages. The dinner guide accurately asks guests to confirm that day's dinner and dessert availability and prices. There is no reason to publish another near-duplicate page for the same query; this work connects those existing pages to a more useful reservation path.

The three homepage cards for dinner, sweets, and drinks used synthetic representative food images. They now use real photos from Pusula Lounge's gallery and describe the actual scene. The booking links carry a selected visit type into the optional reservation form. On submit, that selection is included in the guest's WhatsApp message; the form still asks the team to confirm table availability.

The reservation builder now uses intent-focused title and description copy on Russian, Korean, Arabic, and Chinese pages. The additional visit selector is translated across all six reservation languages and works without JavaScript as visible form content; URL preselection and WhatsApp message assembly use JavaScript.

`robots.txt` explicitly permits `OAI-SearchBot` to crawl public business and visit information. The general allow rule is retained. GPTBot policy was not changed. This is a crawl-access setting, not a promise of ChatGPT visibility.

## What search guidance supports

- Google describes local ranking as primarily relevance, distance, and prominence/popularity; complete, accurate Business Profile data, reviews, photos and other prominence signals matter. No website edit can guarantee first place.
- Google’s current guidance says foundational SEO remains the basis for AI search features, with no special GEO markup or `llms.txt` requirement. It recommends helpful first-hand content, crawlable pages, internal links, a good mobile experience, and matching structured data to visible content. It does not guarantee crawling, indexing, or inclusion.
- OpenAI documents `OAI-SearchBot` as its search crawler and recommends permitting it for sites that want to be eligible for ChatGPT Search results. `GPTBot` and `OAI-SearchBot` controls are independent.
- Google’s restaurant guidance supports detailed current menus, direct menu/reservation links, authentic food/interior photos, review replies, accurate hours, and tracking profile searches, menu clicks, and bookings.

## Follow-up in the business accounts

These are profile-owner actions; no Google, Yandex, or Search Console account was connected during this work.

1. In Google Business Profile, set the website menu to `https://www.pusulalounge.com/menu/` and the preferred booking link to `https://www.pusulalounge.com/rezervasyon/`. The site now lets each visitor select breakfast, dinner, waffles/dessert, or tea/coffee after opening the form.
2. Publish the complete, current evening menu with accurate prices and sections (for example, dinner, desserts, and drinks) in the profile and on the site when the business confirms the live details. The website's priced menu currently focuses on breakfast; don't infer evening prices from old menu images.
3. Confirm the entrance pin and street number in each business listing against the real storefront. Earlier research found a public No:3/No:4 discrepancy. Keep the address and map pin consistent once the correct door is verified.
4. Add real, current exterior, interior, breakfast, dinner, waffle/dessert, and drink photos to the verified profile. The website's visible dinner/waffle cards now use authentic venue photos rather than synthetic dishes; staff product photos would be needed before showing actual food items there.
5. Keep regular and special hours current, reply to reviews, and invite honest feedback without incentives. Use Business Profile performance and Search Console to measure discovery, menu clicks, table requests, and query changes after publishing.

## Official references

- [Google: Improve your local ranking](https://support.google.com/business/answer/7091?hl=en-11)
- [Google: Start a restaurant Business Profile](https://support.google.com/business/answer/14189260?hl=en)
- [Google: Manage local business links](https://support.google.com/business/answer/6218037?hl=en)
- [Google: Menu editor](https://support.google.com/business/answer/9455840?hl=en)
- [Google: Business Profile photo guidance](https://support.google.com/business/answer/6123536?hl=en)
- [Google Search Central: AI features and your website](https://developers.google.com/search/docs/appearance/ai-features)
- [Google Search Central: Generative AI search guidance](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)
- [OpenAI: Overview of crawlers](https://developers.openai.com/api/docs/bots)
