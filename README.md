# Pusula Lounge

Static production site for `https://www.pusulalounge.com`. Published HTML and assets are committed in this repository; changing a content JSON file alone does not update the site.

## Rebuild and verify

Use Python 3 with the dependencies in `scripts/requirements-seo.txt`:

```sh
python3 scripts/build_release.py .
python3 scripts/check_tourism_seo.py .
python3 scripts/check_international_seo.py .
python3 scripts/check_reservations.py .
```

The release builder runs the tourism, reservation, international, font optimization and visitor-quality builders in that order. It refreshes generated pages, menu offers, language links, versioned asset references, SRI/CSP and the sitemap. Run it again after changing content, scripts, CSS or fonts. Commit the generated output with its sources.

For a preview with the release's actual security policy:

```sh
python3 scripts/preview_seo.py . 8875
```

In another terminal, with Playwright and jsdom available:

```sh
PREVIEW_URL=http://127.0.0.1:8875 node scripts/test_international_browser.cjs . /tmp/pusula-browser-qa
PREVIEW_URL=http://127.0.0.1:8875 node scripts/test_visitor_quality.cjs .
node scripts/test_reservations.cjs .
node scripts/test_seo_events.cjs .
```

`PLAYWRIGHT_PATH` and `JSDOM_PATH` can override the test tools' local package paths.

## Content sources

- `scripts/international_copy.json`: Russian/Arabic home, menu and location copy. Prices come from the English menu, checked against the Turkish menu before generation.
- `scripts/arrival_copy.json`: four-language transport and visit-card copy. Recheck official transport links when changing route information.
- `scripts/van_breakfast_article.json`, `scripts/culture_article.json`, `scripts/taksim-evening-article.json` and `scripts/build_tourism_seo.py`: editorial content with real publication dates and sources.
- `scripts/build_reservations.py` and `scripts/reservation_seo_content.json`: six-language WhatsApp table-request pages. The team must confirm a table; the form itself does not book it.
- `assets/fonts/`: original licensed font inputs and optimized derivatives. Do not delete the originals; the font builder checks coverage and advance widths. Adding a published character updates the subset and its cache URL.

Business information must match visible content and the actual business. Do not invent menu prices, ratings, certifications, service availability or travel times. Search Console and business-profile operations are separate account actions.

Research and publication notes are in `seo/`; these documents are excluded from indexing through HTTP response headers.

## Search growth maintenance (29 October 2026)

The release pipeline also runs `build_search_growth.py` and
`finalize_search_metadata.py`. Breakfast landing prices are derived from the
published Turkish menu; edit that menu and rebuild rather than editing landing
prices independently. Final image metadata is derived after the journal design.
The release preserves sitemap dates when final page bytes have not changed.

Additional verification:

```sh
python3 scripts/check_search_growth.py .
python3 scripts/check_search_metadata.py .
```

Research, query-to-page mapping and the measurement plan:
`seo/SEARCH-GROWTH-2026-10-29.md`.
