# Reservation search and customer acquisition pass — 27 October 2026

## Findings addressed

The six reservation pages already had canonical URLs, reciprocal hreflang, basic Restaurant/WebPage/FAQPage schema and functional WhatsApp requests. This pass targets remaining discovery and decision gaps:

- Main headings were expressive but did not explicitly state the Taksim booking intent. All six H1s now name both the place and the reservation action in their own language. The Russian title now also names Istanbul.
- Menu and breakfast guides had a reservation link only in navigation or the footer. Four pages now offer a contextual table-request link after the visitor has reviewed food and prices. Existing page typography and layouts are reused.
- HTML site maps did not list all six reservation languages; the Turkish entry still described the older copy-only flow. Both site maps now expose all six native-language links, and the old description is corrected.
- Existing FAQ content did not answer price/portion and exact-address/contact questions. Five concise, localized questions now address confirmation, hours, special requests, prices/portions and location/contact. Price figures are deliberately sourced through the actual menu link rather than duplicated into six translations that can become stale. Structured FAQ answers match visible answers.
- Every page's business entity now points to a real reservation URL and the same reservation phone. The six reservation pages also identify the page's main restaurant, image and translation relationships, with contextual menu/location/guide links. The site's language declaration is consistent with all six published reservation versions.
- Each reservation page preloads only its own heading font. The below-form mobile restaurant photograph is lazy-loaded. Font subsets were refreshed for changed Cyrillic/Arabic/Korean/Chinese heading characters.

## Validation

`check_reservations.py` checks intent-bearing visible H1s, canonical/hreflang/sitemap relationships, visible FAQ/schema agreement, reservation contact entities, translation links, internal URLs/fragments, native labels, SRI/CSP, directory links and site-wide business identity. Isolated DOM tests cover the existing WhatsApp form flow in six languages without sending a message. Build and discovery scripts produce identical output on a second run.

Published HTML is checked against the exact commit before an IndexNow submission is allowed. HTTP 200 means receipt; HTTP 202 means receipt while ownership verification is pending. Neither response proves indexing or rankings. IndexNow is separate from Google Search Console; no Google indexing submission or Search Console performance access is claimed.

No keyword-stuffed location clones, fabricated reviews/ratings, automated backlinks, unverified proximity distances, instant-booking promises or unnecessary AI text files are added. The business facts come from the existing published business and menu content. This work does not edit the Google Business Profile or imply staff support all six languages.

## Maintenance

```sh
# If heading characters change, refresh their Google Fonts subsets first:
python3 scripts/vendor_reservation_fonts.py .
python3 scripts/build_reservations.py .
python3 scripts/strengthen_reservation_discovery.py .
python3 scripts/check_reservations.py .
JSDOM_PATH=/tmp/pusula-reservation-qa/node_modules/jsdom node scripts/test_reservations.cjs .
```

After committing, pushing and verifying the deployment, preview or submit the latest commit's changed public HTML URLs:

```sh
python3 scripts/submit_reservation_indexnow.py . --report /tmp/pusula-indexnow-receipt.json
python3 scripts/submit_reservation_indexnow.py . --submit --report /tmp/pusula-indexnow-receipt.json
```

Record search impressions, actual WhatsApp inquiries and staff-confirmed reservations separately. Existing anonymous browser events mark opening WhatsApp, not message delivery or confirmed bookings. There is no analytics service connected in this repository and no Search Console connector in the current session; query-level performance and confirmed revenue cannot be verified here.

Primary references: [Google AI search guidance](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide), [Local business structured data](https://developers.google.com/search/docs/appearance/structured-data/local-business), [Restaurant reservation property](https://schema.org/Restaurant), [IndexNow protocol](https://www.indexnow.org/documentation).
