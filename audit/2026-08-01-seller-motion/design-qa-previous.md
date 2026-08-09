# OBER — Design QA

**Source visual truth**

- Product rules: `D:\SUNIYAGENT\ober\OBER-DIZAYN-BRIF.md` and `D:\SUNIYAGENT\ober\memory\state.md`.
- Pre-fix banner capture: `D:\SUNIYAGENT\ober\audit\2026-07-31-perfection\02-banner-xato-natija.png`.
- Pre-fix seller onboarding: `D:\SUNIYAGENT\ober\audit\2026-07-31-perfection\03-sotuvchi-onboarding.png`.

**Rendered implementation**

- URL: `http://127.0.0.1:8800/`.
- Banner empty/live-request state: `D:\SUNIYAGENT\ober\audit\2026-07-31-perfection\04-banner-togri-jonli-sorov.png`.
- Seller onboarding: `D:\SUNIYAGENT\ober\audit\2026-07-31-perfection\03-sotuvchi-onboarding-yakuniy.png`.
- Seller request and response: `05-banner-sotuvchiga-yetdi.png`, `06-sotuvchi-javobi.png`.
- Buyer request and response: `07-xaridor-sorov-yubordi.png`, `08-xaridor-taklifni-kordi.png`.

**Viewport and normalization**

- Primary CSS viewport: 390 × 844; screenshot content width is 375 px because of the visible scrollbar.
- Desktop reflow: 1280 × 800.
- Captures use 1 CSS pixel per output pixel. Old and new states were normalized to 375 × 844 for comparison.
- State: public buyer → banner live request → registered banner seller → `BOR + narx` → buyer receives offer.

**Full-view comparison evidence**

- Banner old/new in one image: `D:\SUNIYAGENT\ober\audit\2026-07-31-perfection\qa-banner-old-vs-new.png`.
- Seller onboarding old/new in one image: `D:\SUNIYAGENT\ober\audit\2026-07-31-perfection\qa-seller-old-vs-new.png`.

**Focused-region evidence**

- `05-banner-sotuvchiga-yetdi.png`: routing, budget chip and answer controls.
- `06-sotuvchi-javobi.png`: success state.
- `07-xaridor-sorov-yubordi.png`: request confirmation.
- `08-xaridor-taklifni-kordi.png`: received price and privacy-safe seller metadata.

**Findings**

- No actionable P0, P1, or P2 finding remains in the audited flow.
- Fonts and typography: existing Segoe UI Variable stack keeps clear heading/body/meta hierarchy; long seller labels now reflow without a squeezed side note.
- Spacing and layout: 390 and 1280 px states have no horizontal overflow; cards, fields, chips, and 44 px+ controls preserve rhythm.
- Colors and tokens: navy primary, green confirmation, amber budget and restrained borders remain semantically consistent.
- Image quality: supplied OBER logo/icon assets are used; no placeholder or new generated asset was introduced in these states.
- Copy and content: banner direction, privacy, distribution and success states now describe what the prototype actually does.
- Interaction states: loading, empty, validation, selected `BOR`, success and polling response were exercised.
- Accessibility: semantic form labels, focus handling, `aria-invalid`, `aria-live`, reduced motion and practical tap targets are present. Full assistive-technology compliance was not claimed.

**Comparison history**

- Pass 1 findings: P0 banner returned unrelated auto prices; P0 contact data leaked through APIs; P1 seller name missing; P1 first reply hid the request from other sellers; P1 `BOR` allowed an empty price; P2 long mobile labels cramped.
- Fixes: universal banner direction parser and safe fallback; direction-based routing; API contact redaction; mandatory seller name/location; multi-offer request visibility; client/server price validation; mobile label reflow.
- Pass 2 evidence: combined old/new comparisons plus the four focused flow captures above. No P0/P1/P2 issue remains.

**Primary interactions tested**

- Banner search produces zero auto cards and a recognized live-request direction.
- Unknown intent does not route to sellers.
- Banner request reaches only banner sellers.
- Buyer phone is absent from seller payload/UI.
- `BOR` without price is rejected; priced response succeeds.
- Other matching sellers can still see the request after the first response.
- Seller phone is absent from buyer payload/UI.
- Buyer receives the price via polling.
- Browser console warnings/errors: none.
- Automated checks: 21/21 dictionary and 26/26 full-loop assertions.

**Follow-up polish**

- P3/out of current visual scope: design and build the offer-selection → internal conversation flow, then add web-push notification permission/onboarding.

final result: passed
