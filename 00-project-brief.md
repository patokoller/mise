# 00 — Project Brief

**Status:** Draft v1
**Last reviewed:** 2026-07-28

---

## 1. The one-sentence version

A dated, structured, source-linked record of what restaurants in a small number of influential cities are actually doing — menus, formats, openings, closings, people, money — accumulated patiently enough that it becomes possible to see changes while they are still happening.

## 2. The thesis

Everyone has the same foundation models. Nobody has a longitudinal, structured record of hospitality. Trade press covers openings and forgets them. Guides publish annual snapshots with no history and no continuity of method. Consultancies produce trend reports built on interviews and vibes, unfalsifiable and unaudited.

The gap is **memory**. A menu is a public document that expires; nobody archives them systematically with dates and structure. Eighteen months of disciplined collection produces something that cannot be bought, cannot be quickly replicated, and gets more valuable every week — because the value is in the *deltas*, and deltas require history.

The corollary matters as much: **this project has no value at month three and considerable value at month twenty-four.** Anything that trades long-term data integrity for short-term output is a bad trade. That principle resolves most design arguments in this folder.

## 3. Who this is for

**Now (months 0–12):** the operator. The audience is a few hundred people who care — chefs, operators, food writers, curious diners. **The Next Table**, free on Substack. The point is discipline and feedback, not revenue. Paid tier gated on the four triggers in `18-publishing-and-brand.md` §4.

**Later (months 12–36), in rough order of willingness to pay:**

- **Restaurant groups and hotel F&B teams** deciding what concept to put in what space. Their question is "what format works here, and is it early or late?"
- **Investors and family offices** in hospitality. Their question is "which models have travelled well, and what's the failure rate?"
- **Suppliers and producers** — ingredient, equipment, and beverage companies wanting to see demand shift before their sales figures show it.
- **Design and architecture practices** pitching hospitality clients.

**Explicitly not for:** consumers looking for restaurant recommendations. That market is saturated, low-value, and structurally different.

## 4. Scope — Phase 1

**Cities: Copenhagen, Barcelona, London.**

- *Copenhagen* — small enough for near-exhaustive coverage, which is what makes counts meaningful rather than anecdotal. Disproportionate influence on global fine dining. Well documented in English. Reachable from Zürich in under two hours.

  **Danish: the operator does not read it** (`D-022`, 2026-07-28). Menus in the target segment are believed to be mostly published in English, so the by-eye verification model in `16-validation-guide.md` §3 is expected to hold for menu data. **That belief is an assumption, not a finding, and Phase 1 must test it** — Q7 counts menu languages, so the answer falls out of ordinary collection. Record it rather than carrying it.

  **Where the gap actually bites is money, not menus.** CVR is the most open company register of the three cities and is the reason Q11 was expected to be strongest here — and CVR filings are in Danish. Danish trade press (`06-source-registry.md` §4, Class D) is likewise the primary channel for Copenhagen openings, closures and chef moves, which feed Q13, Q14 and Q17. Machine translation is adequate for *reading* these; what is lost is *verification* — the operator cannot independently confirm that an extraction from a Danish source is faithful. An error there produces a wrong fact rather than a systematically wrong count, which is the less damaging failure, but it is not zero.

  **Consequence to hold:** Copenhagen financial and event claims carry a lower verification standard than London's, and `09-editorial-and-predictions.md` §2 traceability should be met by linking the source rather than by asserting the operator checked it.
- *Barcelona* — **confirmed 2026-07-28** (`D-021`). Systematically under-covered by English-language food media, so the same effort buys more differentiated observation. Spanish and Catalan sources are usable, and Catalan-language material is the least-contested source pool available to the project (`06-source-registry.md` §4).

  **What this closes.** The Madrid substitution permitted in earlier drafts is not taken. Madrid is neither collected nor read; it is out of scope. The Barcelona-vs-Madrid polarisation hypothesis raised during the Phase 0 interview is therefore **retired, not deferred** — it cannot be tested with this cohort and should not be published as a claim. `20-twenty-questions.md` Q8 stands as a three-city question: does the spread pattern in Barcelona differ from London and Copenhagen? Adding Madrid is a Phase 8 question at the earliest (`D-001`).
- *London* — high volume, dense press coverage, easy to validate the pipeline against. Acts as the control case: if a signal appears in Copenhagen and London but not Barcelona, that's information.

**Why three and not twelve.** Trend detection requires a baseline. To know that buckwheat desserts are rising, you must know what a normal dessert section looked like six months ago in that city. Thin coverage of twelve cities yields twelve datasets too sparse to establish any baseline — you get volume without signal. Twelve cities also means simultaneous entity resolution across Japanese, Korean, Thai, Danish, Spanish, and French. That is where this project would die.

**Tokyo and Seoul are read, not collected.** Follow the press, log notable observations manually into the `events` table. Promote to full collection cities in year two. Their web presence is thin, menus are frequently in-person only, and the aggregators are hostile to automated collection.

**Segment:** the ambitious end of the market — the places that set direction. Not QSR, not the mass market. Those move slowly and are covered adequately elsewhere.

**Ambition is established mechanically, and ownership size is not part of it** (`21-venue-inclusion-criteria.md`, `D-024`, 2026-07-29). Earlier drafts of this brief excluded groups operating more than ~10 venues. That exclusion is withdrawn, for a specific reason: **Q18 asks how ownership concentration is changing per city, and concentration cannot be measured on a frame that excludes the concentrators.** Ownership scale is now recorded as a venue attribute (`independent` / `small_group` ≤10 / `large_group` >10) rather than used as a filter. QSR and mass-market chains remain out in practice because they fail both qualifying routes — they are not guide-listed and are not covered as press subjects — not because a size rule removes them.

*The consequence to hold:* press over-covers group openings, so the frame will contain a larger large-group share than the world does. This is **not** corrected with a quota, because ownership mix is part of Q18's answer and quota-ing it fixes the answer in advance. It is measured and reported.

**Hotels: F&B only.** A hotel restaurant or bar is in scope when it competes with standalone restaurants on its own terms — its own name, its own menu, people going there to eat rather than because they're staying there. The hotel itself is not the entity; its restaurant is. We do not track room counts, occupancy, hotel development, or hotel groups as such.

*Why the line is drawn here:* hotels as a category would mean a second entity type with its own attributes, its own sources, its own economics, and its own trade press — effectively a parallel project. Hotel F&B, by contrast, uses exactly the same menu, format, and service model that restaurants do, so it costs almost nothing extra and it's genuinely where a lot of interesting movement happens. Recorded as `D-015`.

*How this shows up in the data:* `venues.venue_type = 'hotel_restaurant'`, with the hotel recorded as a `parent_group_id` entity so the relationship exists without the hotel being tracked in its own right.

**Target coverage by end of Phase 3:** ~250 venues in the **cohort**, ~4,000 dated menu items, all sourced and resolved.

**The cohort is not the frame.** `21-venue-inclusion-criteria.md` defines a *frame* — every venue per city satisfying the mechanical rule, enumerated in full including exclusions and their reasons — and a *cohort* drawn from it by seeded random sample. The frame is expected to be several times the cohort's size. It is not collected from; it exists so that every published count has a real denominator, and because Q15 and Q18 are answered from the frame rather than the cohort.

## 5. The operator's honest position

No industry background. No relationships. Genuine and sustained enthusiasm. This is not disqualifying, but it changes what the advantage has to be:

**Available advantages:**
- *Time and patience.* The dataset is built by consistency, not access.
- *Independence.* No access to protect, no relationships to preserve. Able to write "this group's expansion is quietly failing" — which is precisely why trade coverage is uniformly positive and analytically worthless.
- *Physical reach.* Copenhagen, Barcelona, London, Paris, Milan are all short flights from Zürich. First-hand observation is a real data layer for European cities.

**The gap to close deliberately:** unit economics. Concepts fail on rent-to-revenue, labour cost, covers per service, and lease terms — almost never on aesthetics. Analysis that can't touch cost structure caps out at "these things are trendy," which is the ceiling of every existing newsletter. This gap is closed by reading, not by relationships: listed hospitality groups file real numbers, annual reports and investor decks are public, and trade financial coverage is public. Budget explicit monthly hours for it. See `11-roadmap.md`.

## 6. Non-goals

Stated so they can be pointed at when tempted.

- **Not a restaurant recommendation product.** Different market, different data, saturated.
- **Not real-time.** Weekly is the fastest useful cadence. Real-time creates operational burden with no analytical gain — trends move in months.
- **Not comprehensive globally.** Depth in three cities beats thinness in thirty, permanently, not just at the start.
- **Not scraping social platforms.** Against ToS, technically hostile, legally exposed, and lower signal than menus. See `10-legal-and-ethics.md`.
- **Not an AI product.** AI is the extraction and synthesis layer. The product is the record. If the models vanished, the database would still be valuable; the reverse is not true.
- **Not building custom infrastructure early.** Managed services until they demonstrably fail.

## 7. Success criteria

**Month 1** — Prediction ledger open with at least 5 dated, falsifiable calls, made without system data (`D-018`). These are the intuition baseline; they cannot be created retrospectively.

**Month 3** — 12 consecutive weekly reports published. ~60 venues with structured, dated menu data. Schema stable enough that it hasn't needed breaking changes in a month.

**Month 6** — Extraction pipeline running unattended weekly. ~150 venues. First trend claim supported by counts rather than impressions. Ledger has 15+ open predictions and the first few resolving.

**Month 12** — ~250 venues, 12+ months of history on the earliest cohort. Demonstrable lead/lag observation between cities. First scored predictions. At least one inbound enquiry from someone who wants something the data can answer. That enquiry is the real signal — it means the asset is legible to people who might pay.

**Month 24** — Enough history that questions like "which formats opened in Copenhagen in 2026 are still trading in 2028" are answerable from the database alone. This is the point at which the moat exists.

## 8. Kill criteria

Also stated in advance, because side projects usually die by drift rather than decision.

- Four consecutive weeks with no data collection and no publication, twice in a six-month period. The time series is the asset; if it isn't being maintained, the project has ended whether or not it's been admitted.
- Month 9 with no trend detectable that wasn't already obvious from reading the trade press. That would mean the data model is measuring the wrong things — fixable, but requires a real redesign rather than more collection. **This is judged against the ledger, not from memory:** if data-supported predictions score no better than the Phase 1 intuition-only ones (`20-twenty-questions.md` Q20, `v_prediction_score`), the intelligence layer is adding nothing. Note the honest limit — at month 9 the resolved sample will be small, so treat it as a warning rather than a verdict; the real reading is month 14.
- Running cost exceeding enthusiasm. If it's not fun and it's not paying, stop.

## 9. Confirmed assumptions

Update as they're resolved. Listed in `README.md` under Open assumptions.

| Assumption | Current value | Confirmed? |
|---|---|---|
| Languages read | EN, ES, some FR/IT. **Not Danish** | ☑ 2026-07-28 |
| Copenhagen menus mostly in English | believed true; **unverified** | ☐ tests itself in Phase 1 via Q7 |
| Third city | **Barcelona.** Madrid out of scope | ☑ 2026-07-28 (`D-021`) |
| Sustainable hours, bad week | 4–5 | ☐ |
| Monthly budget ceiling | ~€50 | ☐ |
| Role | Product manager — specifies and validates, does not code | ☑ |
| Build model | Claude builds; operator judges output against reality | ☑ |

**The one still open that matters.** "Copenhagen menus are mostly in English" is currently load-bearing — it's what keeps the by-eye verification model intact for a third of the corpus. It is also the cheapest assumption in this document to test, because Q7 counts menu languages as a matter of routine. If Phase 1 shows a materially lower English share than expected, the honest response is a stated coverage caveat on Copenhagen menu claims, not a workaround.

**Consequence of the role.** The binding constraint is not engineering capability — Claude covers that — it's *verifiability*. Anything built must be checkable by someone who knows restaurants and doesn't read code. See `15-working-with-claude.md` and `16-validation-guide.md`. The operator's domain knowledge is a genuine quality-control asset: knowing that a Copenhagen restaurant does not have 60 dishes on its menu catches bugs that no automated test would flag.
