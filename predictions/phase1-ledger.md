# Prediction ledger — Phase 1 (the running ledger, `D-018`)

**Opened:** 2026-09-28. **Author of P1–P5:** Claude, at the operator's request (`D-064`).
**Operator endorsement:** not yet given. An unendorsed prediction stays in the ledger and is scored like any
other; it is never deleted after the fact (the `M1` lesson).

This is the *running* ledger. The three pre-frame hypotheses live separately in `data/predictionledger.xlsx`
and are not touched by this file.

## Rules

- A prediction is written, dated and given a resolution rule **before** the outcome is known, and is never
  edited afterwards. A correction is a new line that says what it corrects.
- Resolution uses a re-collection run under the same spec as the 2026-09-28 capture
  (`D-057`, `D-059`, `D-060`), counted in code, with the denominator stated.
- **Not data-free.** Every prediction below was written after 8 menus were read on 2026-08-12 and
  73 menu rows were collected on 2026-09-28. Each one says what it could have been influenced by.
- A git commit date is not evidence of when a prediction was made (`D-061`). The evidence is this file's
  first published appearance, and issue #1 of The Next Table, which prints them.

---

### P1 · Headline prices rise, and nobody at the top cuts

**Claim:** between the 2026-09-28 capture and a re-collection on or after **2027-03-31**, among Phase 1
venues whose own headline menu price (tasting or set) is captured on both dates in the same currency,
**more will have raised it than cut it**, and **no venue whose tasting menu was ≥ 4,000 DKK, ≥ €300 or
≥ £250 on 2026-09-28 will have cut it**.

**Resolves:** true if both halves hold; false if either fails. Void if fewer than 10 venues have a
comparable price on both dates.
**Confidence:** 0.75.
**Influenced by:** the 2026-09-28 price list (it defines who is "at the top").

### P2 · The most expensive rooms keep selling a price, not a menu

**Claim:** every venue that was `price_only` on 2026-09-28 with a tasting menu at or above 4,000 DKK or
€300 — **Geranium, Kadeau Copenhagen, Alchemist, Noma, Disfrutar, Cocina Hermanos Torres** — will still
publish **no dish list** on its own site or booking page at re-collection on or after 2027-03-31.

**Resolves:** true if none of the six moves to `full`; false if any does. A closed venue is removed from
the six and the denominator says so.
**Confidence:** 0.8.
**Influenced by:** directly — the six were identified from the 2026-09-28 capture.

### P3 · Menus turn over within a quarter

**Claim:** at a re-collection between **2026-12-15 and 2026-12-31**, **at least three in four** of the
venues that were `full` on 2026-09-28 and are still `full` will show **at least one dish added or
removed** against the 2026-09-28 capture.

**Resolves:** comparison of dish lists by venue, done by the operator by eye on any disputed case
(machine text is good enough to detect change, not to quote — `D-059`). Void if fewer than 12 venues
are `full` on both dates.
**Confidence:** 0.7.
**Influenced by:** seasonal cues seen in the capture (autumn menus already live at Geranium and Enigma;
spring produce still listed at Prodigi and Plates, which cuts both ways).

### P4 · English-only stays English-only in Copenhagen

**Claim:** none of the Copenhagen Phase 1 venues that published their menu or price page in English only
on 2026-09-28 — **Kadeau Copenhagen, Alchemist, akmē, Alouette, Noma, Alf** — will publish a Danish
version by re-collection on or after 2027-03-31.

**Resolves:** true if none adds Danish; false if any does. Bears on Q7.
**Confidence:** 0.85.
**Influenced by:** directly — the six were identified from the 2026-09-28 capture.

### P5 · The guides are carrying closed restaurants

**Claim:** when F4 (trading status at frame date 2026-07-28) is run across Copenhagen's 132-venue
Route A frame, **at least 5 of the 132** will be found not trading at frame date — Connection and
Brasserie Barner included — and **most of those removed will be A2-only** (White Guide, not MICHELIN).

**Resolves:** at the F4 pass. Void if F4 has not run by 2027-03-31.
**Confidence:** 0.6.
**Influenced by:** the two closures found on 2026-09-28 — Connection, whose closure was reported by
MigogKBH on 2025-01-21, eighteen months before a frame in which White Guide still listed it; and
Brasserie Barner, whose own site says it has closed, with no date. Both are A2-only.

---

## Still owed

- **The operator's own predictions**, if he wants Q20 to measure his judgement rather than Claude's.
  They go here, marked `author = operator`, and are scored separately (`D-064`).
- **H2-a's six-month lag threshold** in `data/predictionledger.xlsx` is still a Claude placeholder.
  It is a pre-frame hypothesis, so it is **not** replaced by Claude under delegation: replacing it now,
  with data in hand, would falsify the record it exists to keep. It stays flagged as a placeholder.

---

## Added 2026-09-28, later the same day — ingredient predictions (P6–P8)

**Author:** Claude, at the operator's request (`D-064`). **Evidence base:** a panel of the same 17 kitchens
read on 2026-09-28 and, via Internet Archive captures dated 2025-08-09 to 2025-11-11, a year earlier
(`D-068`); 20 published 2026 food-trend forecasts (`data/external/food_trend_forecasts_2026.csv`). Counts from
`analysis/ingredients/tag_ingredients.py`. **Resolution for all three:** a re-collection of the same 17 kitchens
between 2027-09-01 and 2027-09-30 under the same spec, tagged by the same script with the vocabulary frozen as of
this commit. A kitchen that closes or stops publishing dishes is removed and the denominator says so.

### P6 · The forecasters' grocery-aisle favourites stay off serious menus

**Claim:** hojicha, gochujang, beef tallow/beef fat and matcha will **each** be on the menus of no more than 2 of
the 17 panel kitchens in September 2027. (2026-09-28: 0, 0, 0 and 0; September 2025: 0, 0, 0 and 1.)
**Confidence:** 0.75. **Influenced by:** directly — the 2026 and 2025 panel counts.

### P7 · Smoke in, truffle out

**Claim:** in September 2027, truffle will be on the menus of no more than 4 of the 17 panel kitchens, **and**
something smoked on at least 9. (September 2025: truffle 9, smoked 6. 2026-09-28: truffle 3, smoked 9.)
**Confidence:** 0.6. **Influenced by:** directly — the year-apart panel counts.

### P8 · Heat on shellfish reaches Barcelona

**Claim:** by September 2027, at least one Barcelona kitchen among the Phase 1 venues will publish a menu with chilli
heat (chilli, kosho, kimchi, 'nduja, jalapeño or similar, per the frozen vocabulary) on the same dish as shellfish.
(2026-09-28: none of the Barcelona menus we could read; 6 kitchens in Copenhagen and 1 in London.)
**Confidence:** 0.5. **Influenced by:** directly — the 2026 capture. It is a test of the leading-city bet (`D-065`).
