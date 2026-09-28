# 21 — Venue Inclusion Criteria

**Status:** v1 — Phase 0 deliverable
**Last reviewed:** 2026-07-29
**Frame date:** 2026-07-28 (frozen — see §2)
**Decisions:** `D-023`, `D-024`, `D-025`, `D-026`

---

## 1. What this file is for

Venue selection determines what is discoverable. Q9 can only ever find originators inside the cohort, so whatever this rule excludes is permanently invisible — not missing, *invisible*, because nothing in the data will indicate it was ever there.

This document is therefore written to one standard: **a stranger, given this file and an internet connection, should produce the same frame and the same cohort.** Not a similar one. The same one.

**What this rule is not.** It is not an attempt to reproduce the operator's intuition. If it did, every trend later "discovered" would have been embedded in the selection. The operator's intuition is a hypothesis generator; this rule is a measurement device; the two must never be the same object. Substantial overlap with intuition is expected. Complete overlap is a failure signal.

**Two objects, kept distinct throughout:**

| Object | What it is | Used for |
|---|---|---|
| **The frame** | Every venue in a city that satisfies §3 and §4, enumerated in full, including those excluded and why | Denominators, coverage claims, Q15, Q18 |
| **The cohort** | The venues actually collected from — drawn from the frame by §6 | Menu collection, Group A questions, weekly events |

Most of the honesty in this project comes from the frame existing. Most of the work comes from the cohort.

---

## 2. The frame date

**2026-07-28.** Every test in §3 and §4 is evaluated as of that date, using guide editions and press archives current on that date.

This exists because denominators drift silently. A rule applied continuously is not a rule, it's a habit, and it will absorb the operator's changing interests without anyone noticing. Freezing the date makes the frame reproducible and makes drift visible as a dated event rather than a mood.

The frame is refreshed on a schedule, not continuously. See §7.

---

## 3. Hard filters

All six must hold at the frame date. A venue failing any of these is recorded in the frame with its reason code (§5), not deleted.

| ID | Filter | The bright line |
|---|---|---|
| **F1** | Inside the city boundary | Named administrative unit only — see below. Not "central", not "greater area", not judgement |
| **F2** | Publishes menu information, retrievable | Three states — see §3.2. `full` or `price_only` passes; `none` fails |
| **F3** | *(withdrawn as a filter — see §3.1)* | — |
| **F4** | Trading at the frame date | Not announced-not-yet-open, not closed, not on indefinite hiatus |
| **F5** | Publicly accessible | No membership, invitation, or residency requirement to book |
| **F6** | Hotel F&B qualifies on its own terms | Holds a qualifying route in its own right, listed as a restaurant under its own name — see §3.3 |

**F0 — resolve the entity first.** No filter can be applied to a name. Before F1, every candidate is resolved to a street address and, where one exists, a `google_place_id`; if it cannot be resolved to exactly one venue, it is recorded as `unresolved` and no verdict is issued. Added after calibration, where a supplied venue name matched four different Barcelona restaurants and could not be adjudicated (`D-029`).

**F0 is an identity test only — amended 2026-08-01 (`D-040`).** The original wording required resolution to "exactly one **trading** venue," which made F0 do two jobs and gave the trading question to the wrong filter. A venue that is closed but unambiguously identified now **passes F0**, takes an F1 verdict on its resolved address, and fails **F4** as `not_trading`. The distinction is not cosmetic: `unresolved` means *we could not tell what this is*, `not_trading` means *this closed*, and Q13 rests on being able to count the second. Kiin Kiin Tok Tok was filed as `unresolved` under the old wording when it was in fact a confirmed closure at the guide's own stated address.

**Places does not return permanently closed venues — a systematic blind spot, not an incident.** A candidate that shut before enumeration does not present as a closure. It presents as a **wrong-venue match**: the query returns the nearest still-trading business, which is then correctly rejected, and the row lands in `unresolved`. Re-tested 2026-08-01 on both Copenhagen cases; both returned the same wrong venues as at enumeration. **This finding stands unchanged.**

**What `unresolved` actually contained, once all 14 Copenhagen rows were checked — amended 2026-08-01 (`D-044`).** An earlier version of this section, written on a sample of 2 of 2, read `unresolved` as principally *unrecognised closure*. On the full 14 it was **12 unrecognised geography and 2 closure**. Four consequences, and they apply in all three cities:

1. **`unresolved` is a mixture**, not a category. It contains genuine ambiguity, unrecognised closure, *and* — dominantly, in Copenhagen — **venues outside the boundary that the resolver could not place**. Cause is unknown until each row is checked by hand against a source that displays closed listings.
2. **The commonest cause is a truncated address, not a closure.** White Guide's strings for these rows carried street and number with no locality — *"Annebergparken 50,"* — so F1 could not be applied to the guide's own text and the row fell through to Places resolution, **which was scoped to the target city**. A venue in Agger, Sønderborg or Tórshavn had no way to resolve. **Resolve on the guide's full address text where it exists, and treat a truncated address as its own state rather than letting it fall through to `unresolved`.**
3. **No coverage claim may present `unresolved` as a measure of ambiguity.** State it as what it is — unresolved, cause unknown — until the rows are adjudicated. Copenhagen's bucket is now empty; London's and Barcelona's have not been enumerated.
4. **A closed venue may carry no `google_place_id`.** An exclusion row does not require one; the A2 boundary exclusions already have none. Only frame membership requires a place_id, and a closed venue never reaches the frame.

**Do not generalise from a small sample here.** The 2-of-2 reading was wrong in direction and would have been carried into two more cities. `M1`, a prediction that rested on it, was deleted unendorsed (`D-042` reversed).

**This will be harder to see in London and Barcelona.** Both cities' registered guides cover far more territory than the target city, and a wrong match in Greater London or greater Catalonia looks plausible in a way that a wrong match for a Faroese venue does not.

**A guide's territory is not the territory you assume.** White Guide Denmark includes the **Faroe Islands** — 5 of its 199 entries. Establish each guide's stated territory *before* reconciling counts against it (`D-037`).

**F1 boundaries, stated once:**

| City | Boundary | Neighbourhood grain (for Q15) |
|---|---|---|
| Copenhagen | Københavns Kommune + Frederiksberg Kommune | Official *bydele* |
| Barcelona | Barcelona municipality | The 10 *districtes* |
| London | Greater London (32 boroughs + City of London) | Borough |

These are administrative, published, and stable. They are also arbitrary at the edges — a venue 200m outside Barcelona municipality in L'Hospitalet is excluded. Arbitrary and stated beats fuzzy and defensible.

### 3.2 F2 — three states, not two (`D-027`)

F2 originally required "a priced food menu." Calibration broke that: **Alchemist**, two Michelin stars and top-five in the world, publishes a price and no dish list — it sells prepaid tickets through Tock. Under the original wording, the highest-profile venue in the census city was excluded. Meanwhile Enigma, structurally the same proposition, publishes a dated menu PDF *and* a price and passed.

A price and a dish list are different artefacts and F2 now records them separately as `menu_publication_mode`:

| State | What is published | What the venue can answer |
|---|---|---|
| `full` | Dish list **and** prices | All of Group A — Q1–Q7 |
| `price_only` | A venue-set price, no dish list | **Q4 and Q5 only** |
| `none` | Neither | Nothing — fails F2 |

`full` and `price_only` pass. `none` fails.

**Who has to publish it.** Published **by the venue or on its behalf, not compiled about it.**

- Counts: the venue's own site; its Tock, SevenRooms or Resy page, where the venue sets the price and the description
- Does not count: TheFork's "average price around €120", scraped aggregator listings, review-site menus

Checkable in seconds, and it is what keeps Bar Brutal out — aggregators carry its dishes, the venue does not.

**The cost, stated because it is not free.** Every Group A count now needs a second denominator. Not "17 of 60 tracked" but "17 of the 44 tracked venues that publish dish lists." More bookkeeping and one more place to get it wrong. Carried into `09-editorial-and-predictions.md` §2.

**One thing calibration corrected.** Enigma and Alchemist are the same format — tasting-only, surprise-led, secrecy as part of the proposition. One publishes, one does not. **Menu publication is a venue-level choice, not a function of format.** The excluded set is therefore messier than "the fast-rotating venues," which is mildly good news for Q6: the bias is real but it is not a clean category that can be characterised and set aside.

**One thing it did not correct.** Prepaid ticketed dining is itself a format shift — datable, venue-specific, squarely in Q15 and Q17 territory — and it correlates with menu non-publication. The rule is therefore partially blind at a point where something is changing. `menu_publication_mode` is recorded as a **tracked attribute**, not merely an exclusion flag, so that a venue moving from `full` to `price_only` is a dated event rather than a silent one.

### 3.3 F6 — hotel F&B (`D-028`)

The original F6 required a name distinct from the hotel's and a menu page at its own URL. Calibration showed both clauses were inert. **Alain Ducasse at The Dorchester** passes "a name distinct from the hotel's" while containing the hotel's name in full. **Moments** passes on a sub-page of the hotel's own site, and nearly every hotel gives each outlet one.

Requiring a separate domain would have been worse — it would exclude Moments, a Michelin-starred destination restaurant, on a web-hosting decision.

**F6 therefore collapses into the routes.** A hotel F&B outlet is in scope if it holds a qualifying route **in its own right, listed as a restaurant under its own name** in the guide's restaurant selection — not the hotel selection. Third-party listing is the independent-identity test, and it is the same test everything else faces.

This is the second replacement for the judgement question in the old `06-source-registry.md` §5 ("would someone not staying at the hotel go there specifically to eat?"). That question was good and not mechanical. The route test does its work without asking anyone to imagine a diner.

`venue_type = 'hotel_restaurant'` and the hotel group as parent are recorded either way.

### 3.1 Why there is no ownership-size filter

Earlier drafts excluded groups operating more than ~10 venues. That is withdrawn (`D-024`).

**Q18 asks how ownership concentration is changing per city.** Concentration cannot be measured on a frame that excludes the concentrators — the question is not merely weakened, it is arithmetically unanswerable. The exclusion also cost nothing analytically, because Routes A and B already exclude QSR and the mass market: a chain outlet is not guide-listed and is not covered as a press subject.

Ownership scale is therefore **recorded, not filtered**:

- `independent` — single venue, no group parent
- `small_group` — parent group operating 2–10 venues globally at the frame date
- `large_group` — parent group operating more than 10

Counted from the group's own website. Where the group does not publish a venue list, count what a company register (Class F) shows and record which source was used.

**What counts as one of the group's venues.** Only venues the group **operates**. Investment stakes, licensing deals and partnership concepts do not count, and are recorded in `notes` rather than the tally. Calibration surfaced this: JKS Restaurants' own boilerplate puts its portfolio at 30 restaurants "including concepts created by the Sethis as well as those they partner and invest in." At the >10 threshold the distinction rarely changes the tag; at 8 versus 12 it decides it. Record the count, the source, and the date it was read.

**The consequence to hold:** press over-covers group openings relative to their share of the world, so Route B will pull large-group venues into the frame at an inflated rate. **Do not correct this with a quota.** Ownership mix is part of Q18's answer; quota-ing it fixes the answer in advance. Measure what the frame contains and report it.

---

## 4. Qualifying routes

A venue must satisfy at least one. Every route flag is recorded separately, per venue, because the combination is data.

### Route A1 — Michelin (all three cities)

Listed at **any** level in the Michelin Guide edition current at the frame date for that city: Three, Two or One Star, Bib Gourmand, or the Selected / Main Selection tier.

A1 is the **comparability spine.** It is the only qualifying route with one publisher, one stated method, and one inspection regime across all three cities. Any Q8 three-city comparison that needs a like-for-like frame is run on the A1-only subset.

Edition vintages differ by city and must be recorded per city at enumeration:

| City | Edition | Published | Verified |
|---|---|---|---|
| Copenhagen | MICHELIN Guide Nordic Countries 2026 | 1 June 2026, Tivoli Concert Hall, Copenhagen | ☑ |
| Barcelona | MICHELIN Guide Spain (2026 edition) | to be recorded at enumeration | ☐ |
| London | MICHELIN Guide Great Britain & Ireland 2026 | 9 February 2026, Convention Centre, Dublin — 1,210 restaurants, 230 starred | ☑ |

### Route A2 — one named national guide per city

| City | Guide | Tier included | Notes |
|---|---|---|---|
| Copenhagen | White Guide Denmark | All listed Danish entries — **tier scope unresolved, see below** | Nordic-wide guide, Swedish publisher, running since 2005. **No dated edition — see below** |
| Barcelona | Guía Repsol — **Soles only** | 1, 2 and 3 Soles | *Restaurantes Guía Repsol* (formerly *Recomendados*) explicitly **excluded** — see below |
| London | Harden's Top 100 UK Restaurants — London entries | Top 100 only | The full Harden's London guide is **excluded** — see below |

**A2 is deliberately asymmetric, and this must be stated wherever it matters.** Copenhagen's A2 is broad, Barcelona's is moderate, London's is narrow. London's frame therefore leans hardest on Route B — which is defensible, because London has by far the densest press of the three, but it is a real difference in how the three frames were built. Q8 comparisons run on A1-only exist for exactly this reason.

**Open question on London's A2 (`D-029`, unresolved).** Calibration found Bouchon Racine ranked **first in the UK at the National Restaurant Awards, June 2026**, up from fifth. The NRA Top 100 is not a registered route. Michelin caught this venue anyway, so nothing was lost — but a venue one rung below Michelin's radar and top-ranked at the NRA would be invisible, and London's A2 was already the narrowest of the three. Registering the NRA Top 100 as a London A3 is an open decision for the operator.

**Two findings on Copenhagen's A2, recorded 2026-07-30. Neither is resolved, and both must be before enumeration.**

**1. White Guide Denmark has no edition.** §2 requires guide editions "current at the frame date." White Guide publishes new reviews weekly on a rolling website; there is no *White Guide Denmark 2026* volume to freeze against. As written, A2 for Copenhagen is not reproducible — a stranger re-running this in October gets a different set and has no way to reconstruct what 2026-07-28 looked like, which fails the standard in §1 directly. This is a defect in the rule, not a retrieval problem, and it does not exist for Michelin, Repsol or Harden's, all of which publish dated editions. **Open: what "current at the frame date" means for a rolling source, and what artefact gets stored to make the claim checkable later.** Listed in §12.1.

**2. The tier scope has not been tested against the Repsol precedent.** White Guide classifies across five levels — Global Masters, Masters, Very Fine, Fine, and Recommended. "All listed Danish entries" takes all five. Guía Repsol's second tier was excluded from Barcelona's A2 for a specific, stated reason: 1,605 national entries against 808 Soles would have made Barcelona's frame several times the size of the other two and swamped the sample. **That test has never been applied to White Guide's lower tiers**, and the structural situation looks similar. If Recommended is large, the consequence is not merely a bigger Copenhagen frame — it is that Copenhagen's A2 becomes non-comparable to the other two cities in a way §4's asymmetry note does not currently describe, which lands directly on Q8. Cannot be sized until the list is retrievable. **Open: confirm all five tiers, or set the cut, with the counts visible.** Listed in §12.1.

**Two exclusions inside A2, both deliberate:**

- **Guía Repsol's second tier is excluded** because it runs to roughly 1,605 entries nationally against 808 Soles, which would make Barcelona's frame several times the size of the other two and would swamp the sample. Note also that this tier was **renamed from *Recomendados* to *Restaurantes Guía Repsol* in the 2026 edition** — a source-definition change of exactly the kind that later gets mistaken for a real-world shift. Logged in `12-decision-log.md`.
- **The full Harden's London guide is excluded** because its ~1,700 London entries span pubs, cafés and street food, which is a different segment entirely, and because the complete listing is a commercial product. The Top 100 is published freely and annually, is dated, and is mechanical.

### Route B — dated press attention

The venue's name appears in the **headline or first paragraph** of at least **two** items, from at least **two different** publications on the registered list for that city, within the **24 months** before the frame date. Syndicated wire copy counts once, attributed to the originating agency.

The registry is `06-source-registry.md` §4A, set 2026-07-29 (`D-030`).

Three constraints, all load-bearing:

1. **The publication registry is fixed and change-logged.** It lives in `06-source-registry.md` §4. Adding a publication later shifts the frame; `08-trend-detection.md` §5 already treats source addition as the null hypothesis for any coincident signal.
2. **Headline-or-first-paragraph is the mechanical test for "subject".** A venue named in a roundup of twelve places does not qualify from that item.
3. **Keep the count.** A registered publication list makes the source defensible; the count of two is what makes the rule *mechanical*. Dropping the count and relying on "did this publication take it seriously?" reintroduces exactly the judgement this document exists to remove.

**Route B is load-bearing for Q12**, not merely a breadth supplement. Q12 asks whether venues that lead on diffusion receive critical recognition *later*. If every venue in the cohort is already guide-listed, there is no variance in recognition at t0 and the question is dead before collection starts. The cohort must contain venues with no guide listing. §6 enforces this.

---

## 5. The frame: enumeration and exclusion codes

**Enumerate the whole qualifying pool per city. Do not work it.**

The frame is a spreadsheet in Phase 1 (consistent with `D-018` — the ledger is a spreadsheet too; managed simplicity until it demonstrably fails). One row per venue, with these columns:

```
venue_name · address · neighbourhood · google_place_id
route_a1 · route_a1_tier · route_a2 · route_a2_tier · route_b · route_b_citations
ownership_scale · ownership_count · ownership_source · parent_group · opened_on (if published)
menu_publication_mode (full | price_only | none) · menu_source_url
cheapest_full_meal_price · currency
in_cohort (bool) · excluded_reason (nullable) · frame_date · added_by · notes
```

**On price:** record the figure, not a band. The cheapest price at which one person can eat a complete meal as the venue structures it — lowest set menu, or cheapest starter + main if à la carte. Banding is analysis and can be done later; a band recorded now cannot be un-banded.

### Exclusion codes

| Code | Meaning |
|---|---|
| `outside_boundary` | Fails F1 |
| `no_published_menu` | Fails F2 — `menu_publication_mode = none` |
| `unresolved` | Fails F0 — could not be resolved to exactly one venue. **Cause unknown** and must not be reported as any single cause. In Copenhagen the 14 rows adjudicated 12 outside-boundary / 2 closed (`D-044`); the mixture will differ by city |
| `not_trading` | Fails F4 — closed, or hiatus. Used wherever closure is *established*, including a venue identified only by hand after Places refused to return it |
| `opening_pending` | Fails F4 — announced, not yet open |
| `membership_only` | Fails F5 |
| `hotel_not_standalone` | Fails F6 |
| `duplicate_of` | Resolved to another frame row; record the target |

### The limit on this, which must be published alongside it

**Exclusion reasons are recordable for hard-filter failures. They are not recordable for route non-appearance.**

The frame is *constructed from* Routes A1, A2 and B. A venue that no guide lists and no registered publication has covered never enters the frame at all — there is no row on which to write a reason, because it was never seen. So the exclusion log will size the boundary, menu, closure, access and hotel categories precisely, and will size the below-attention population at exactly zero, in every city, permanently.

This matters because the log will *look* like a complete accounting of what is missing. It is a complete accounting of what is missing **among venues that something already noticed.**

The published form is therefore always two sentences, never one:

> "Menu analysis covers 278 of the 312 qualifying London venues; 34 publish no retrievable menu. The frame is bounded by guide and press attention, and the number of ambitious London venues below both is unmeasured."

The second sentence never gets a number. Not in any city, not ever.

---

## 6. The cohort: how the 20 per city are drawn

**Strata — two, on route only:**

| Stratum | Definition | Quota per city |
|---|---|---|
| Route A | Listed by A1 or A2 (regardless of B) | 12 |
| Route B-only | Qualifies on B alone, no guide listing | 8 |

If a city's B-only pool holds fewer than 8, take all of it and top up from Route A — and record that this happened, because it means that city's cohort has less recognition variance and Q12 is weaker there.

**Why these strata and no others.** Route is a proxy for *recognition at t0*, and Q12's outcome is recognition *change* — stratifying on the baseline and measuring the change is legitimate. Price, format, course count and rotation rate are **outcome variables** in the twenty questions, and the rule is absolute:

> **Never stratify on a variable that is an outcome in the twenty.** Quota-ing price bands makes Q15's answer "the price points I put in the quota."

Neighbourhood is not stratified either. It is *reported* — the cohort's neighbourhood distribution is compared against the frame's and published as a known property of the sample. This is weaker than proportional allocation and it is chosen deliberately, because allocation constraints create a temptation to redraw.

**The draw, reproducibly:**

1. Filter the frame to rows where `excluded_reason` is null.
2. Split into the two strata.
3. Sort each stratum ascending by `venue_name`, Unicode NFC-normalised and case-folded, ties broken by `google_place_id`.
4. Index 1…N.
5. Select with a documented PRNG: `random.Random(20260728).sample(range(N), k)`.

**Seed: 20260728.** Declared here, in writing, *before* the frame is enumerated. That ordering is the whole point — a seed chosen after seeing the frame is not a seed, it's a selection.

**No redraws. Ever.** Not for a bad neighbourhood spread, not for a boring-looking list, not for "the sample missed the obvious one." If the draw can be repeated on inspection, the rule is not mechanical and nothing else in this document holds. If the cohort looks wrong, that is information about the frame, and the response is to write down why — not to draw again.

This is the clause most likely to be broken, and it will be broken the first time the draw returns twenty venues the operator finds dull.

---

## 7. Refreshing the frame

**The rule has a refresh procedure, not an inbox.**

Venues are not added when noticed. The frame is re-run at a new frozen date — **quarterly**, aligned to the review in `13-operating-cadence.md` — and additions enter as a dated cohort with `entities.first_seen_at` set.

This exists because of cohort bias (`08-trend-detection.md` §5): adding twenty vegetable-forward venues in March spikes every vegetable tag in March. Ad-hoc addition makes that correction impossible, because there is no addition date to correct against.

Between refreshes, a venue that clearly qualifies but is not in the frame gets logged as a *pending frame entry* with the date it was noticed. It joins at the next refresh. Nothing is added mid-quarter.

---

## 8. What this captures, what it doesn't, and what each part protects

| Criterion | Protects | Cost |
|---|---|---|
| Frozen frame date, written rule | Q9, Q20; `08` §5 "your own bias" | Goes stale; §7 is mandatory, not optional |
| F1 named boundary | Q8, Q15 | Arbitrary at the edges |
| F2 three-state | Q1–Q7 on `full`; **Q4 and Q5 only** on `price_only` | Correlated with the outcome (§9.1); forces a second denominator on every Group A count |
| F4 trading at frame date | Q13 | *Causes* the survivorship bias Q13 flags |
| F5 public access | Q15 comparability | Loses members' clubs, a real London innovation site |
| F6 route-based hotel test | Q15, Q17 | Admits any hotel outlet a guide lists; the guide's threshold is now the project's |
| Ownership scale recorded, not filtered | **Q18** | Press-inflated large-group share; must not be quota-corrected |
| Route A1 Michelin | Q12 recognition baseline; Q8 comparability | Lags 12–24 months behind openings |
| Route A2 national guide | Q12, Q15 breadth | Asymmetric across the three cities by construction |
| Route B press | **Q12**, Q9 | Inherits press bias wholesale, including its anglophone skew |
| Frame enumerated, cohort sampled | Every denominator ever published; **Q15 and Q18 are answered from the frame** | Enumeration labour |
| Seeded draw, no redraws | Q20 — the hypothesis-blindness claim becomes auditable | Returns venues the operator finds dull |
| Exclusion codes | Sizes four of the eight blind spots | Sizes the biggest one at zero forever (§5) |
| F0 entity resolution | Prevents a wrong-venue merge, which `01` treats as invisible and unrecoverable | Adds a lookup before every verdict |

**The split worth memorising:** Group A questions (menus, Q1–Q7) live on the **cohort**. Q15 and Q18 live on the **frame**. That is why enumerating a frame you do not collect from is worth the hours.

---

## 9. What this systematically misses

Eight categories, ordered by cost.

**1. Venues that publish no menu at all (F2 = `none`).** Still the expensive one. The exclusion is correlated with what is being measured: the kitchens that change daily are least likely to publish a current menu. **Q6 — rotation rate — is biased by construction** and will be measured on venues that rotate slowly enough to publish.

Two qualifications from calibration. The three-state F2 recovers `price_only` venues for Q4 and Q5, so the loss is now confined to dish-level questions rather than everything. And publication turned out to be a venue-level choice rather than a property of format — Enigma publishes, Alchemist does not, and they are the same proposition — so the excluded set is not a clean category. The correlation remains untestable as a general claim and must not be published as one.

**1b. Venues below guide level that publish nothing.** Bar Brutal and Pompette both fail F2 *and* hold no route, in two different cities, for the same reason. They therefore generate no exclusion row at all — they are absent rather than excluded, and the natural-wine-bar category sizes at zero in both cities. This is §5's limit and §9.2 combined, and calibration showed it is structural rather than local.

**2. Venues below both guide and press attention.** The largest category and the only one that cannot be counted (§5). In Barcelona this is a substantial and interesting population; Route B's reliance on press also carries an anglophone skew into a Catalan- and Spanish-language city.

**3. Openings in months 0–6.** Too new for a guide, not yet covered twice by registered press. This is precisely the origin window for Q9.

**4. Pop-ups, residencies and takeovers.** Fail F1 and F4. A real origin site for practices.

**5. Non-restaurant origin points.** Coffee, retail bakeries, food halls, importers. Practices arrive in restaurants *from* these. Note that wine bars, cocktail bars and bakeries with a priced food menu are **already included** — they pass F2 and can qualify on either route. What is excluded is the drink-only and retail-only end.

**6. Closed venues.** The frame is built from venues trading at the frame date, so Q13 is survival-of-survivors. Partial mitigation: **once a venue is in the frame, closure is an observation, never a deletion.** Set `not_trading` and keep the row. Do not let the frame quietly repair itself.

**7. Members' clubs (F5).**

**8. Venues whose destination restaurant shares the hotel's name (F6).**

---

## 10. What this does to Q9, stated plainly

**Q9 in year one is diffusion shape, not origin.**

A random 20 of a 300-venue frame gives an unbiased read of how a practice spreads through the cohort, and an unreliable read of where it started. The earliest sampled venue will usually be a mid-chain adopter, not an originator. False attribution is worse than "unknown," because it looks publishable.

Categories 3, 4 and 5 in §9 are exactly where practices originate, and all three are excluded by construction.

**The rule that follows (`D-026`), to sit alongside the archive-bias rule in `08-trend-detection.md` §5:**

> No origin claim unless the frame is enumerated as a census for that city. Cohort-first is not origin, and must be published with the cohort definition attached.

Concretely: Copenhagen, the near-exhaustive city, is the only place an origin claim will ever come close to defensible — and even there it is origin-within-frame, not origin. **London and Barcelona get wave shape only.**

**The known fix, which is scope expansion and has not been taken.** A second cohort — a census of all frame venues opened within the last 24 months, tracked separately and never pooled into a penetration denominator — targets the origin window directly and overlaps work Q17 needs anyway. It roughly doubles Copenhagen's collection load. Deferred, not rejected; revisit at the month-6 review.

---

## 11. The calibration test

**Run 2026-07-29 on twelve venues. Results in §11.1. The rule was amended afterwards (`D-029`).**

Run this **before** relying on the rule. It takes about an hour.

### Choosing the five

Pick to slots, not to preference:

| Slot | What it tests |
|---|---|
| 1 | A certain-include | That the rule doesn't fail at the core |
| 2 | A certain-exclude — a good venue clearly outside the segment | That the rule isn't letting everything through |
| 3 | Open under 12 months, no guide listing | Route B |
| 4 | Format-borderline — wine bar, bakery, counter | F2 and the segment edge |
| 5 | Hotel F&B | F6 |

Optional sixth: **a venue one of the three hypotheses says is important.** If the rule excludes it, that is the rule working, and it is worth feeling that happen once before there is data at stake.

### Running it

1. **Write the expected verdict for all five before applying anything.** Pre-registration. Without this the test measures nothing, because the rule will look obviously right in hindsight for every case.
2. Apply §3 and §4 in order. Record which specific filter or route decided each case.
3. Compare.

### Reading it

Four or five agreements means calibrated. **Disagreement is the useful output**, and the two kinds are not symmetric:

**Rule excludes what you would include.** Ask: *can the reason for inclusion be stated in observable terms that do not reference what you expect to find?* If yes, the rule has a real gap — amend it and log the amendment. If the only available reason is "it's doing the interesting thing," that is the hypothesis speaking, and the rule is correct.

**Rule includes what you would exclude.** Usually leave it. Over-inclusion costs one dull venue. Under-inclusion is invisible and permanent — the same asymmetry as the entity-resolution rule, where a visible duplicate beats an invisible bad merge.

### Recording it

The five verdicts, the pre-registered expectations, and any amendment go in `12-decision-log.md`. If the rule is amended after seeing the results, that amendment is itself a hypothesis-exposure event and must be dated — an amended rule is fine; a quietly amended rule is not.

---

## 11.1 Calibration results — 2026-07-29

Twelve venues, verdicts pre-registered by the operator before the rule was applied.

| City | Venue | Expected | Rule | Decided by |
|---|---|---|---|---|
| BCN | Enigma | Include | INCLUDE | A1 — 2★ ES 2026 |
| BCN | McDonald's Pl. Catalunya | Exclude | EXCLUDE | No route |
| BCN | AMA | Uncertain | UNRESOLVED | F0 — entity not identified |
| BCN | Bar Brutal | Include | **EXCLUDE** | F2 |
| BCN | Moments | Include | INCLUDE | A1 — 1★ ES 2026 |
| LDN | The Arts Club | Exclude | EXCLUDE | F5 |
| LDN | Gymkhana | Include · large_group | INCLUDE | A1 — 2★ GB&I 2026 |
| LDN | Dishoom Covent Garden | Review | LIKELY EXCLUDE — unverified | No route (probable) |
| LDN | Bouchon Racine | Test Route B | INCLUDE | A1 — GB&I 2026 selection |
| LDN | Alain Ducasse at The Dorchester | Include | INCLUDE | A1 — 3★ GB&I 2026 |
| CPH | Alchemist | Include | INCLUDE (`price_only`) | A1 — 2★ Nordic 2026 |
| CPH | Pompette | Test segment edge | EXCLUDE | F2, no route |

**Seven clean expected-vs-actual comparisons: six agreements, one disagreement (Bar Brutal).** The rule tracks the operator's judgement. The value was in the rows that did not resolve cleanly.

**Amendments made as a result** — all dated `D-027`, `D-028`, `D-029`:

| Finding | Change |
|---|---|
| Alchemist: price published, no dish list | F2 becomes three states (§3.2) |
| Aggregators carry menus the venue does not | F2 publisher clause (§3.2) |
| Ducasse passes a name test containing the hotel's name; Moments passes on a sub-page | F6 collapses into the routes (§3.3) |
| "AMA" matched four venues | F0 added |
| JKS counts partnered and invested venues in its own tally | `ownership_scale` counts operated venues only (§3.1) |

**Findings recorded but not acted on:**

- **Route B does not exist.** `06-source-registry.md` §4 names a *category* of press per city, not publications. Route B could not be applied to any of the twelve. Until it is defined, the Route-B-only stratum is empty, the 12/8 split in §6 collapses, Q12 has no recognition variance, and sub-guide venues generate no exclusion rows. **This blocks enumeration.**
- **Members' clubs are invisible, not excluded.** The Arts Club holds no route, so `membership_only` never gets written. Unlike the below-attention population, members' clubs are an enumerable set and could be counted separately if the operator chooses.
- **London's A2 may be too narrow.** See §4.

**Untested after this round:** the matched pair across cities (A2 asymmetry), outer London against the F1 boundary, and Danish-language menu publication. Copenhagen was tested on two venues only.

## 12. Rules that follow from this document

Carried into `09-editorial-and-predictions.md` §2 and `18-publishing-and-brand.md` §9:

1. **Correlation is not diffusion.**
2. **Cohort-first is not origin.** (`D-026`)
3. **Absence from the cohort is not absence from the city.** (§5)
4. **Never infer intent from menus.** Consistent with Q3's existing caveat: menu language measures how restaurants write as much as how they cook.
5. **Predictions are timestamped before measurement.** (`D-018`)
6. **If plausible explanations are listed, at least one must be boring.** Seasonality, a coverage change, a source addition. A list containing only interesting mechanisms is an assertion with a disclaimer attached — readers keep the mechanism and discard the hedge.

---

## 12.1 Open items blocking enumeration

| # | Item | Owner | Status |
|---|---|---|---|
| 1 | **Route B publication registry** — 5–10 named titles per city, into `06` §4 | Operator | ☑ Closed 2026-07-29, `D-030` |
| 2 | Michelin Guide Spain 2026 edition date | Claude, at enumeration | ☐ |
| 3 | Whether to register the NRA Top 100 as a London A3 (§4) | Operator | ☐ |
| 4 | Whether to enumerate London members' clubs as a separate counted exclusion | Operator | ☐ |
| 5 | Matched-pair calibration across London and Copenhagen | Operator supplies venues | ☐ |
| 6 | **A1 retrieval.** `guide.michelin.com` is `robots_permitted` and `waf_blocked` simultaneously (`06` §4) | Claude tests; operator decides fallback | ☑ Closed 2026-07-30 — Firecrawl, `proxy: basic`, within `10` §2. Copenhagen A1 enumerated, 83 venues |
| 7 | **A2 vintage for Copenhagen.** Define "current at the frame date" for a rolling source, and the stored artefact that evidences it (§4) | Operator | ☑ Closed 2026-07-30, `D-033` — the stored snapshot is the edition |
| 8 | **A2 tier scope for Copenhagen.** All five White Guide tiers, or a cut, against the Repsol precedent (§4) | Operator, once counts are visible | ☑ Closed 2026-07-30, `D-036` — **all five tiers**. Recommended is 3 venues nationally |

**No hard blockers remain.** Items 1, 6, 7 and 8 are closed. One open question sits below enumeration: Anarki's `route_a2_tier` (one venue, one ID, two conflicting classifications at source).

**Copenhagen A1 is enumerated (2026-07-30).** 83 candidates, all five tier counts reconciled against the guide's own stated figures (`D-032`'s first live pass). 72 Danish rows resolved to an address and `google_place_id`; 68 pass F1 (62 Københavns, 6 Frederiksberg); 15 fail on boundary, of which 11 are in Malmö — Michelin's "Copenhagen and surroundings" crosses the Øresund. **This is not the frame.** A2 and Route B are not applied, so no frame size can be stated yet.

**The guide's city label is not a boundary test.** Enumeration confirmed this twice over: six venues labelled "Copenhagen" sit in Frederiksberg Kommune, and Restaurant VIE is filed under the separate locality "Nordhavn" while sitting inside Københavns Kommune. F1 must be applied to a resolved address, never to the guide's own geography.

**A note on item 6 that should not be lost.** Michelin's `robots.txt` grants named AI crawlers unrestricted access and advertises a sitemap; the refusal comes from edge bot-detection, not from stated policy. The permitted responses are: retry from different infrastructure in default mode, ask the publisher, or collect by hand. Circumventing the block with stealth mode or rotating proxies is prohibited by `10` §2 and is not available as a fallback, however convenient it becomes. Recorded here because this is the point in the project where that temptation will actually arrive.

## 13. Before the frame is enumerated

**Write the three current hypotheses into the prediction ledger, dated, first.**

They are the intuition-only baseline Q20 needs (`D-018`), and they are the only thing that makes the hypothesis-blindness claim in §1 auditable. Recorded after the frame exists, nobody — including the operator — can establish which came first.
