# Pusula blog redesign — 28 October 2026

Rebuilt both journal indexes and all twelve TR/EN articles. Final direction follows the user's correction: no serif typography; use the actual venue, its floral canopy, yellow seating, forest green and checked tables. All text uses the existing self-hosted Source Sans 3. The original homepage sunflower and tablecloth assets connect the index to the restaurant. Each article subject has a distinct real cover image, synchronized with social metadata and the image sitemap.

Content, publication dates, canonical/hreflang pairs, verified Restaurant schema, price tables, sources and breakfast/dinner reservation query parameters are retained. The source processor is scripts/build_blog_design.py, with CSS/JS under scripts/editorial/. The release builder runs it after font optimization and before the final integrity/CSP pass. Pillow is declared in scripts/requirements-seo.txt for actual image dimensions.

Validation:
- All 14 pages at 320, 390, 768 and 1440 CSS pixels: no horizontal overflow, one h1, sans headings and no broken eager images (56 browser checks, in-app browser).
- Topic filters, native mobile menu and contents behavior checked; no console warnings/errors in the inspected browser states.
- Full release built successfully in a separate temporary copy; crawlability/schema/link/asset/SRI checks passed for 40 pages and 182 schema nodes. International menu, prices, dates and sources checks passed.
- All 14 original titles and Restaurant objects match the base commit; original article sections and reservation intent URLs match.
- Design detector returned no mechanical findings; git diff --check passed.
- Existing check_reservations.py fails on the unchanged Russian heading assertion (expects “Бронь”). Reservation pages and that test were not modified by this change. Blog and release validation above passed.

Reduced motion disables spatial animation and reading progress. Without JS, all stories and article content remain visible; filtering is progressively revealed and native details/navigation still work. Continuous animations are avoided.
