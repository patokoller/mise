# 05 — Taxonomy v1

**Status:** Draft v1 — expected to change most of any document here
**Last reviewed:** 2026-07-28

---

## 1. Why this exists

Free-text extraction produces four hundred spellings of "fermented." Counting requires a controlled vocabulary. This file *is* the mechanism that turns a pile of menus into a countable dataset.

**Rules:**
- The extractor selects from this list. It may not invent terms.
- Anything unmapped goes to `taxonomy_unmapped` with an occurrence count.
- Weekly review promotes frequent unmapped values into the vocabulary.
- New terms are retroactively applied to the whole corpus (see `03-data-flow.md` §6).
- Terms are never deleted, only deactivated. Deleting a term destroys the history that used it.

**Design bias:** start narrow. A vocabulary of 150 well-defined terms that get used consistently beats 800 that get applied inconsistently. Terms earn their place by appearing in the unmapped queue repeatedly.

---

## 2. Facets

Eight. Each menu item and venue can carry terms from several.

| Facet | Question it answers | Applies to |
|---|---|---|
| `ingredient` | What is it made of? | menu items |
| `technique` | What was done to it? | menu items |
| `format` | What kind of eating experience is this? | venues |
| `service_model` | How is it delivered and paid for? | venues |
| `cuisine` | What tradition does it reference? | venues, items |
| `beverage` | What's the drink programme? | venues, items |
| `design` | What does the room do? | venues |
| `technology` | What systems does it run on? | venues |
| `sustainability` | What claims are made and evidenced? | venues, items |

---

## 3. `ingredient`

Hierarchical. Tag at the most specific level available; parents are inferred by query.

**Proteins** — beef, pork, lamb, veal, goat, chicken, duck, pigeon, quail, game bird, venison, rabbit, offal, blood, charcuterie, cured fish, white fish, oily fish, shellfish, crustacean, cephalopod, bivalve, roe, seaweed, insect, plant protein, tofu, tempeh, legume, egg, dairy, cheese

**Grains & starches** — wheat, rye, barley, oat, buckwheat, spelt, einkorn, rice, koji rice, corn, millet, sorghum, quinoa, amaranth, potato, sweet potato, cassava, celeriac, jerusalem artichoke

**Produce** — brassica, allium, root vegetable, squash, tomato, aubergine, pepper, mushroom, cultivated mushroom, foraged mushroom, wild herb, cultivated herb, sea vegetable, stone fruit, pome fruit, berry, citrus, tropical fruit, melon

**Fats & seasonings** — olive oil, seed oil, animal fat, butter, cultured butter, vinegar, fish sauce, soy sauce, miso, koji, garum, chilli, pepper, salt, smoked salt, sugar, honey, molasses

**Watchlist terms** — narrower than the above, tracked because they are plausible leading indicators. Reviewed quarterly; graduated or dropped.
buckwheat · koji · garum · kelp · pine · birch sap · verjus · aged citrus · fermented honey · cultured cream · dry-aged fish · beef fat · lacto-fermented berry

---

## 4. `technique`

Raw, cured, brined, pickled, lacto-fermented, koji-fermented, aged, dry-aged, wet-aged, smoked, cold-smoked, hot-smoked, grilled, charcoal-grilled, wood-fired, embers, roasted, braised, confit, poached, steamed, fried, deep-fried, tempura, sous-vide, dehydrated, freeze-dried, powdered, emulsified, whipped, gelled, clarified, reduced, infused, barbecued, spit-roasted, salt-baked, clay-baked, ash-cooked, nixtamalised, sprouted, malted, distilled, hand-cut, house-made, foraged-preparation

---

## 5. `format`

The venue-level experience shape. This facet is where the commercially interesting questions live.

fine-dining · neo-bistro · bistronomy · tasting-menu-only · counter-dining · chef's-table · omakase · izakaya-style · small-plates · sharing-plates · single-product (a venue built around one thing) · grill-house · seafood-focused · vegetable-forward · vegetarian · vegan · bakery-restaurant · wine-bar-kitchen · natural-wine-bar · cocktail-kitchen · listening-bar · hotel-fine-dining · hotel-all-day · residency · pop-up · supper-club · food-hall-stall · takeaway-hybrid · members-club · counter-bakery · coffee-and-food

---

## 6. `service_model`

à-la-carte · fixed-price-menu · multiple-tasting-lengths · no-choice-menu · walk-in-only · reservation-only · ticketed-prepaid · deposit-required · service-charge-included · no-tipping · tipping-expected · single-seating · two-seatings · continuous-service · bar-seating-walk-in · counter-only · communal-table · set-lunch · weekend-only · limited-days (venues open ≤4 days/week — a live labour-cost signal)

---

## 7. `cuisine`

Kept deliberately coarse. Fine-grained national cuisine labels generate endless argument and little analytical value.

nordic · new-nordic · french-classical · french-modern · italian · spanish · catalan · basque · portuguese · greek · levantine · north-african · west-african · east-african · turkish · persian · indian · pakistani · sri-lankan · thai · vietnamese · chinese-regional · cantonese · sichuan · japanese · korean · filipino · indonesian · malaysian · mexican · peruvian · nikkei · brazilian · argentine · caribbean · british-modern · american-regional · jewish-diaspora · fusion-explicit · undeclared-modern

---

## 8. `beverage`

natural-wine · low-intervention-wine · classical-wine-list · biodynamic-focus · local-wine-focus · sake-programme · sherry-programme · vermouth-programme · beer-pairing · cider-programme · cocktail-pairing · non-alcoholic-pairing · zero-proof-programme · fermented-non-alcoholic (kombucha, kvass, water kefir) · juice-pairing · tea-pairing · coffee-programme-specialty · house-fermentation-drinks · wine-by-the-glass-extensive · corkage-permitted

`non-alcoholic-pairing` and `zero-proof-programme` are separate deliberately: one is an add-on, the other is a designed programme. The distinction is exactly the kind of thing worth measuring.

---

## 9. `design`

open-kitchen · closed-kitchen · counter-seating · banquette · communal-table · exposed-concrete · exposed-brick · raw-timber · pale-wood · dark-wood · stone-surfaces · ceramic-tile · terrazzo · steel-surfaces · plaster-walls · textile-acoustic · linen-tablecloth · no-tablecloth · paper-menu · no-printed-menu · qr-menu · pendant-lighting · candlelight · daylight-forward · plant-heavy · minimal-decor · maximalist-decor · vintage-furniture · custom-furniture · visible-fermentation · visible-ageing-cabinet · visible-wine-storage · music-forward · quiet-room

Populated from your own photographs primarily. This facet is thin from web sources and rich from first-hand observation — which makes it one of the more defensible parts of the dataset.

---

## 10. `technology`

The useful insight here: **most restaurant technology is visible on the venue's own website.** The booking widget names the reservation platform. A prepaid checkout names the ticketing system. A QR menu, a delivery integration, a gift-card system — all of it is embedded in the page and mechanically detectable. This makes technology adoption one of the cheapest facets to populate accurately, and one where you can genuinely see the industry shifting before anyone writes about it.

**Reservation and access** — reservation-platform-[name] · in-house-booking · ticketed-prepaid-platform · deposit-capture · waitlist-system · walk-in-only-no-system · membership-platform

**Ordering and payment** — qr-order-at-table · qr-menu-view-only · self-order-kiosk · handheld-payment · pay-at-table-app · split-bill-app · cashless-only · dynamic-pricing · off-peak-pricing

**Kitchen and back of house** — kitchen-display-system · automated-prep · robotics-visible · sous-vide-programme-stated · fermentation-lab-stated · inventory-software-stated · production-kitchen-separate

**Delivery and off-premise** — own-delivery · third-party-delivery-integration · click-and-collect · meal-kit-retail · packaged-product-retail · ghost-kitchen-operation

**Customer-facing AI and data** — ai-concierge-stated · personalisation-stated · loyalty-programme-digital · newsletter-crm-visible · carbon-labelling-tool

**Rules:** record the platform *name* where visible — `reservation-platform-sevenrooms`, `reservation-platform-tock` — because platform migration is itself a signal, and a venue moving from one system to another usually means something changed operationally. Record only what's observable; never infer a POS from a photograph.

---

## 11. `sustainability`

Split into *claim* and *evidence*, because the gap between them is itself a finding.

**Claims:** zero-waste-claim · local-sourcing-claim · seasonal-claim · organic-claim · biodynamic-claim · regenerative-claim · carbon-labelled · plastic-free-claim · fair-pay-claim · four-day-week

**Evidence:** certified-organic · certified-b-corp · michelin-green-star · published-supplier-list · published-carbon-data · own-farm · own-fermentation-programme · whole-animal-butchery · surplus-sourcing

---

## 12. Governance

**Weekly (10 min):** review `taxonomy_unmapped` ordered by occurrence count. Anything appearing 5+ times across 3+ venues is a candidate. Add it, or map it as a synonym of an existing term.

**Quarterly (45 min):** review the whole vocabulary. Which terms have never been used? Which are used inconsistently? Which watchlist terms have graduated to mainstream or died? Deactivate — never delete — dead terms.

**Version the taxonomy.** Tag it in git each quarter. `signals` computed under different taxonomy versions are not directly comparable, and you will forget this if it isn't recorded.

**The synonym discipline:** every term carries a `synonyms` array. "lacto-fermented", "lacto fermented", "lactofermented", "lacto-ferm." all map to one term. This array grows faster than the term list and is where most of the real work is.
