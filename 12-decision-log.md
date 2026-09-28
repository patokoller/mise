# 12 — Decision Log

**Status:** Living document — append only
**Last reviewed:** 2026-07-30

---

## Why this file exists

You will work on this intermittently for years. In month fourteen you will look at a design choice and think "that's stupid, I'll change it," having forgotten the reason it was made. This file is the defence against that.

**Rules:**
- Append only. Superseded decisions get a note, not a deletion.
- Every entry records: date, decision, alternatives considered, reasoning, and what would reverse it.
- Log source additions, taxonomy version bumps, prompt changes with eval results, and schema migrations here too. Anything that could later look like a trend but was actually a decision you made.

**Format:** `D-NNN` · date · title · status

---

### D-001 · 2026-07-28 · Three cities, not twelve · **Accepted**

**Decision:** Phase 1 covers Copenhagen, Barcelona, London. Tokyo and Seoul are read manually, not collected.

**Alternatives:** the original 12-city tier list; five cities; one city.

**Reasoning:** trend detection requires a baseline. Thin coverage of twelve cities produces twelve datasets too sparse to establish one, so nothing is detectable — volume without signal. Twelve cities also means simultaneous entity resolution across six languages, which is where the project would die. Copenhagen is small enough for near-exhaustive coverage, which makes counts meaningful; Barcelona is under-covered in English-language media, so effort buys more differentiated data; London provides volume and a validation control.

**Reverses if:** coverage in all three cities exceeds 85% of the defined segment and the weekly review takes under 45 minutes. Realistically month 21+.

---

### D-002 · 2026-07-28 · One database (Postgres) · **Accepted**

**Decision:** Postgres 16 with `pgvector` and `pg_trgm` serves relational, vector, and graph needs. No Neo4j, no dedicated vector database.

**Alternatives:** the original Postgres + Neo4j + Qdrant design.

**Reasoning:** three databases means three schemas, three backup regimes, and two sync paths that can break, in exchange for capabilities not needed at a scale of thousands of entities. `pgvector` handles well over a million embeddings. Multi-hop traversal via recursive CTEs is uglier than Cypher but fast enough at this size. Operator time is the binding constraint.

**Reverses if:** a graph query becomes central *and* measurably slow (Neo4j), or embeddings exceed ~2M (dedicated vector store).

---

### D-003 · 2026-07-28 · Append-only temporal facts · **Accepted**

**Decision:** facts are never updated in place. Changes close the old row via `valid_to` and insert a new one. `observed_at` and `retrieved_at` are always separate fields.

**Alternatives:** current-state tables with an audit log; simple upserts.

**Reasoning:** the entire product is change over time. Destructive updates permanently destroy the asset, and the loss is silent — you don't discover it until you try to run the query that would have justified two years of work.

**Reverses if:** never. This one is foundational.

---

### D-004 · 2026-07-28 · Statistics in SQL, interpretation in LLM · **Accepted**

**Decision:** no LLM computes a number that will be published. The Editor receives a prepared statistics brief and has no database access.

**Alternatives:** giving the model query access; asking it to analyse raw tables.

**Reasoning:** an LLM asked to find trends in raw data invents them, fluently and confidently, and the invented version reads better than the true one. The structural separation makes the failure impossible rather than merely unlikely.

**Reverses if:** never.

---

### D-005 · 2026-07-28 · Single LLM provider (Anthropic) · **Accepted**

**Decision:** Claude for extraction, tagging, and synthesis. Sonnet 5 for volume, Opus 5 for synthesis, Haiku 4.5 for bulk classification once the taxonomy stabilises.

**Alternatives:** multi-provider routing; separate vision provider.

**Reasoning:** one set of prompts to maintain, one billing surface, one set of quirks to learn. Sonnet reads menus, PDFs, and photographs directly, removing the need for a separate OCR stage for clean documents. No measured benefit to mixing at this stage, and prompt maintenance across providers is a real recurring cost.

**Reverses if:** a specific task measurably underperforms on the project's own gold set — not on a published benchmark. Speech transcription and image generation are the likely first exceptions.

---

### D-006 · 2026-07-28 · No separate OCR initially · **Accepted**

**Decision:** Sonnet 5 vision reads menus, PDFs, and photographs directly. Tesseract only as a fallback for documents that demonstrably fail.

**Alternatives:** Tesseract or a cloud vision API in the pipeline by default.

**Reasoning:** most target documents are digital PDFs or good phone photos, which modern vision models handle directly. A separate OCR stage adds a component, a failure mode, and a cost for the minority of cases. Keep the fallback path documented but unbuilt.

**Reverses if:** the gold set shows >10% failure on a document class.

---

### D-007 · 2026-07-28 · Three agents, not fifteen · **Accepted**

**Decision:** Scout, Extractor, Editor. Resolution and tagging are code plus a model call, not "agents." More agents only when a specific bottleneck is observed.

**Alternatives:** the original five; the eventual fifteen.

**Reasoning:** each agent is a prompt to maintain, an eval to run, and a failure mode. Evolving from three to eight when a bottleneck appears is far easier than starting with fifteen and spending months on coordination. The Weak Signal Agent in particular has no baseline to work against before month twelve and would produce confident coincidences.

**Reverses if:** a queue consistently exceeds its weekly time budget, or a task demonstrably underperforms.

---

### D-008 · 2026-07-28 · No social media scraping · **Accepted**

**Decision:** no automated collection from Instagram, TikTok, or Facebook. Manual observation of public accounts only.

**Alternatives:** scraping public posts; third-party data vendors.

**Reasoning:** breaches platform terms, technically hostile, real legal exposure, and — most importantly — the archive is a multi-year asset that shouldn't be put at risk for a marginal signal. Menus are better indicators than posts.

**Reverses if:** an official API becomes available on acceptable terms.

---

### D-009 · 2026-07-28 · Public prediction ledger from Phase 5 · **Accepted**

**Decision:** dated, falsifiable predictions with resolution criteria written in advance, scored publicly including failures.

**Alternatives:** no predictions; private predictions; unfalsifiable trend calls.

**Reasoning:** the database is replicable by anyone with money. A two-year public calibration record is not — it takes two years and requires having been willing to be wrong in public from the start. Nobody in food media does this.

**Reverses if:** never, though the cadence may change.

---

### D-010 · 2026-07-28 · Manual before automated · **Accepted**

**Decision:** publish four issues by hand before building any pipeline.

**Alternatives:** build the pipeline first.

**Reasoning:** the schema should be discovered from real data rather than imagined. And if the report isn't interesting when made by hand, no architecture makes it interesting — better to learn that in week 4 for the cost of five evenings than in month 8.

**Reverses if:** never.

---

### D-011 · 2026-07-28 · Operator is a product manager, not an engineer · **Accepted**

**Decision:** Claude builds and maintains all code. The operator specifies, judges output, and validates against reality rather than against source code. Every component must ship with a plain-English summary and a worked example checkable by eye.

**Alternatives:** operator learns to code; hire a contractor early; use no-code tools exclusively.

**Reasoning:** learning to build competently would consume the hours that should go into collection and editorial, which are where the operator's actual advantage lies. Hiring early means someone optimising for problems the project doesn't have yet, and wanting to rebuild a data model that isn't proven. The real risk of an AI-built system for a non-engineer isn't bad code — it's being unable to distinguish *working* from *appears to work*, so verifiability becomes the binding design constraint rather than capability.

**Reverses if:** the project takes paying customers with data-security obligations, or needs a public product with authentication. Then buy a few hours of engineering review, per `15-working-with-claude.md` §10.

---

### D-012 · 2026-07-28 · Prefer visible tools over powerful ones · **Accepted**

**Decision:** n8n workflows over Python scripts where equivalent. SQL views over application logic. Metabase questions over coded charts. Python reserved for API calls, JSON validation, and entity resolution — few, small, single-purpose, heavily commented.

**Alternatives:** a conventional Python codebase; a full no-code stack.

**Reasoning:** a workflow the operator can look at and reason about is more valuable than a script that is marginally more capable and completely opaque. Follows directly from D-011. Pure no-code was rejected because entity resolution and schema validation genuinely need real code.

**Reverses if:** a workflow becomes so convoluted that it's less comprehensible than the equivalent script — at which point visibility has been lost anyway.

---

### D-013 · 2026-07-28 · Publish on Substack as "The Next Table" · **Accepted**

**Decision:** the publication is The Next Table, hosted on Substack, subscription-enabled. MISE remains the internal system name and is not reader-facing.

**Alternatives:** Ghost or beehiiv (flat fee, more ownership); self-hosted; own site with memberships.

**Reasoning:** the binding constraint at launch is discovery, not fees. Substack's recommendation network directly addresses a cold start with no audience and no industry relationships, which is precisely this project's weakest point. Zero cost until revenue. The 10% only becomes the dominant cost at a revenue level that would already represent success. Keeping the publication name separate from the platform name preserves the option of serving clients directly later without newsletter branding.

**Reverses if:** subscription revenue exceeds roughly €2,000/month, at which point a flat-fee platform is cheaper — revisit then, not before. Also if Substack's terms change materially.

**Mitigation regardless:** export the subscriber list monthly from day one. Platform independence is a habit, not a migration project.

---

### D-014 · 2026-07-28 · Free until four triggers are met, then paid · **Accepted**

**Decision:** no paid tier until all four hold: 25+ issues published, 750+ free subscribers, 3+ predictions publicly resolved, and one quarterly report already produced free. Paid content is deeper, never earlier.

**Alternatives:** paid from launch; paid from month 3; permanently free.

**Reasoning:** a subscription with no archive and no track record converts nobody and signals nothing. The prediction ledger is what justifies payment, and it needs resolved predictions to exist — which takes time that cannot be compressed. Paywalling the weekly issue would kill the growth engine that makes a paid tier possible at all. Roughly month 12–15 on the current roadmap.

**Reverses if:** an inbound request arrives for something the database can already answer and someone offers to pay for it. That's the market speaking, and it outranks this schedule.

---

### D-015 · 2026-07-28 · Hotels are in scope for F&B only · **Accepted**

**Decision:** hotel restaurants and bars are tracked as venues when they compete with standalone restaurants on their own terms. Hotels themselves are not entities we track — no room counts, occupancy, development pipeline, or hotel groups as such. The hotel is recorded only as a venue's parent group.

**Alternatives:** hotels as a first-class category, per the original vision document; excluding hotel F&B entirely.

**Reasoning:** hotels as a category would require a second entity type with its own attributes, sources, economics, and trade press — effectively a parallel project, at the cost of depth in the one we're actually building. Hotel F&B uses the identical menu, format, and service model as restaurants, so it costs almost nothing extra. It's also disproportionately interesting: groups will experiment with formats in a hotel that they wouldn't risk standalone, because room revenue absorbs the downside, which makes hotel F&B a useful leading indicator.

**Inclusion test:** would someone not staying at the hotel go there specifically to eat?

**Reverses if:** hotel-side questions start arriving from readers or clients that F&B data can't answer. Year 3 at the earliest.

---

### D-016 · 2026-07-28 · Technology facet and Google Trends added · **Accepted**

**Decision:** add a `technology` facet to the taxonomy, and Google Trends as source Class G.

**Alternatives:** leaving both out, as in the original draft.

**Reasoning:** both were gaps against the vision document rather than deliberate exclusions. Restaurant technology turns out to be unusually cheap to observe accurately — the booking widget, checkout, and QR systems are embedded in the venue's own website and mechanically detectable, so adoption is visible without asking anyone. Google Trends is the only consumer-demand signal available through an official API without touching a platform that prohibits collection; it serves as a demand-side check on supply-side menu signals, and the cases where the two *disagree* are the interesting ones.

**Constraint:** Trends data is relative, not absolute. It may never be published as a count.

**Note:** bulk review and social scraping remain excluded on the grounds in `D-008` and `10-legal-and-ethics.md` §3. This decision does not reopen that.

---

### D-017 · 2026-07-28 · Charts generated from the database, never hand-built · **Accepted**

**Decision:** recurring charts are produced by a script reading directly from `signals`, applying house style and generating the denominator and footnote from the data. Manual charting tools are permitted only for one-off explanatory graphics, never for recurring series. Every chart carries its sample size inside the image.

**Alternatives:** Datawrapper or Flourish with hand-entered data; Metabase exports permanently; charts assembled by hand in a design tool.

**Reasoning:** a chart typed by hand can silently disagree with the database, and the operator cannot audit code to catch it (`D-011`). Mechanical derivation makes that class of error impossible rather than merely unlikely. Charts also get screenshotted and separated from their article, so a chart that only tells the truth alongside its caption will eventually mislead someone — hence the denominator inside the image.

**Constraint carried with it:** never chart anything below the publication thresholds in `08-trend-detection.md` §3. A chart is a stronger claim than a sentence, not a weaker one, and visual form confers confidence the sample may not have earned.

**Reverses if:** never for recurring charts. Metabase PNG export is an acceptable interim until Phase 5.

---

### D-018 · 2026-07-28 · Prediction ledger opens in Phase 1, not Phase 5 · **Accepted**

**Decision:** the public prediction ledger opens during Phase 1, written by hand, before any database exists. Five dated, falsifiable predictions in the first month, then a small number monthly. `11-roadmap.md` Phase 5 retains the ledger's *integration with `signals`*, not its opening.

**Alternatives:** opening it in Phase 5 as originally planned; keeping no formal ledger and evaluating the project by judgement at twelve months.

**Reasoning:** the project's stopping condition is whether the system produces insight beyond expert intuition (`20-twenty-questions.md` Q20). As originally scoped that is unfalsifiable — the operator would be judging their own investment retrospectively, from memory, after several hundred hours. The ledger is the only instrument that makes it decidable, but on Phase 5 timing the first predictions do not resolve until months 11–14, so almost nothing is scored at the twelve-month review. Opening in Phase 1 also produces something more valuable than early data: predictions made *before* the system existed are an intuition-only control group. Comparing their hit rate against predictions made in month ten with data measures directly whether the intelligence layer adds anything. A prediction needs a date, a claim and a resolution criterion — not a database.

**Carried with it:** `predictions.basis` added to the schema so the two populations are separable by query rather than by inference from an empty `supporting_signal_ids` array.

**Cost:** roughly an hour a month, from month one.

**Reverses if:** after twelve months fewer than ten predictions have reached resolution, indicating criteria are being written too loosely or with horizons too distant to score.

---

### D-019 · 2026-07-28 · The weekly issue is variable length; no fixed slot count · **Accepted**

**Decision:** the issue keeps the section structure in `09-editorial-and-predictions.md` §3 with a variable number of items per section. No format requiring a fixed number of observations per issue. Two substantive observations and a method note is a complete issue.

**Alternatives:** a fixed "five signals" format, proposed for consistency and reader expectation.

**Reasoning:** a fixed slot count is a narrative-manufacturing mechanism. In a good week there are eight things worth saying; in week nineteen there is one, the format demands five, and four get invented or inflated. This is the failure mode the project exists to avoid, and it arrives through the format rather than through bad intent. Doc 09 already anticipates this — its sections are specified as ranges. Publishing a thin issue on time also aligns with `11-roadmap.md` §"What to protect when time is short".

**Also settled:** the weekly issue's reliable spine is event data — openings, closures, chef moves, acquisitions — not menu data. At 60 venues with quarterly-ish rotation roughly five menus change per week, and `08-trend-detection.md` §3 requires 25 venues observed in a period before a signal may be emitted. Menu-derived counts are a quarterly instrument; expecting weekly menu statistics produces either silence or threshold violations.

**Reverses if:** venue count passes roughly 200 and weekly observed-venue counts clear the §3 threshold, at which point weekly menu statistics become legitimate.

---

### D-020 · 2026-07-28 · Original-language dish names are preserved separately from translations · **Accepted**

**Decision:** `menu_items` stores `name_original` and `name_translated` as distinct columns, and `description_original` / `description_translated` likewise. `menus` gains a `language` column. The original is never overwritten by a translation, and taxonomy tagging and all trigram search run against the original.

**Alternatives:** a single `name` column holding whichever the extractor returned; storing only the translation for queryability.

**Reasoning:** `menu_item_schema.json` already emits both fields and `04-agent-workflows.md` §4 instructs the model to preserve original-language names exactly, but the v1 schema had one `name` column with no rule for which value landed in it. A translated name silently replacing a Danish or Catalan original is unrecoverable, destroys the differentiated Barcelona material that is a stated reason for choosing the city (`D-001`), and corrupts ingredient counting where translation collapses distinctions. The language column additionally makes `20-twenty-questions.md` Q7 countable, which it was not.

**Reverses if:** never. This is a data-preservation rule, not a preference.

---

### D-021 · 2026-07-28 · Barcelona confirmed as third city; Madrid out of scope · **Accepted**

**Decision:** the three cities are Copenhagen, Barcelona, London. The Madrid substitution permitted in earlier drafts is declined. Madrid is neither collected nor read.

**Alternatives:** substituting Madrid for Barcelona; adding Madrid as a fourth city; treating Madrid as read-not-collected alongside Tokyo and Seoul.

**Reasoning:** operator preference, against a genuine trade. Madrid is where the operator's attention demonstrably goes — it surfaced unprompted in three separate Phase 0 answers while Barcelona surfaced in none — and attention is what sustains a multi-year side project. Barcelona wins on differentiation: Catalan-language material is the least-contested source pool available (`06-source-registry.md` §4), and English-language food media under-covers the city, so the same collection hours buy observations nobody else holds. `D-001` reasoning holds — three cities, depth over breadth.

**What this closes:** the Barcelona-vs-Madrid polarisation hypothesis from the Phase 0 interview is **retired, not deferred**. It cannot be tested with this cohort and must not be published as a claim. Q8 stands as a three-city question.

**Reverses if:** after six months the operator's own first-hand observations (`07-extraction-schemas.md` §6, `observation_type = 'visit'`) are near zero for Barcelona while non-trivial for the other two. That is the observable form of "attention didn't follow the decision," and it is the failure mode this choice risks. Count it at the month-6 quarterly review rather than relying on impression.

---

### D-022 · 2026-07-28 · Operator does not read Danish; Copenhagen carries a lower verification standard · **Accepted**

**Decision:** Danish is not a language the operator reads. Copenhagen remains a full collection city. Menu data is expected to be verifiable by eye because menus in the target segment are believed to be mostly published in English; Danish-language financial filings and trade press are read via translation and are **not** independently verifiable by the operator.

**Alternatives:** dropping Copenhagen; learning enough Danish to spot-check; treating Copenhagen as read-not-collected.

**Reasoning:** dropping Copenhagen would remove the city best suited to near-exhaustive coverage and the one with the most open company register, which is disproportionate cost for a gap that mostly does not touch menus. The build model in `15-working-with-claude.md` rests on the operator catching extraction errors by eye; that check survives for English-language menus and does not survive for Danish sources. Machine translation solves *reading*, not *verification* — the operator cannot confirm an extraction is faithful to a Danish original. The resulting failure mode is a wrong individual fact rather than a systematically wrong count, which is the less damaging of the two, but it is not nothing.

**Carried with it:** Copenhagen financial and event claims meet `09-editorial-and-predictions.md` §2 traceability by linking the source, not by asserting operator verification. The gold set (`04-agent-workflows.md` §7) still requires a Danish menu — it now tests the extractor against a document the operator cannot check, so its hand-extraction must be done with translation assistance and marked as such.

**Open, and load-bearing:** "Copenhagen menus are mostly in English" is currently an assumption. Q7 counts menu languages as a matter of routine, so Phase 1 tests it for free. Record the result.

**Reverses if:** Phase 1 shows a materially lower English share of Copenhagen menus than expected. The response is a stated coverage caveat on Copenhagen menu claims, not a workaround.

---

### D-023 · 2026-07-29 · Venue inclusion is a mechanical rule with a frozen frame and a seeded cohort draw · **Accepted**

**Decision:** venue selection is governed by `21-venue-inclusion-criteria.md`. Six hard filters plus three qualifying routes (A1 Michelin, A2 one named national guide per city, B two dated press mentions from the registered list), all evaluated at a frozen frame date of 2026-07-28. The qualifying pool is enumerated in full as a **frame** and is not collected from. The **cohort** — 20 venues per city — is drawn from the frame by seeded stratified random sample, seed `20260728`, strata on route only, with no redraws permitted under any circumstance.

**Alternatives:** the judgement-based criteria previously in `06-source-registry.md` §5; ranking the qualifying pool by guide tier and taking the top 20; proportional neighbourhood allocation; allowing a redraw when the sample looks unrepresentative.

**Reasoning:** three strong hypotheses existed before any venue list did. A list assembled by thinking of restaurants first would have confirmed them invisibly, and Q9 can only find originators inside the cohort, so whatever the rule excludes is permanently undiscoverable. Ranking by guide tier bakes in the guide's own hierarchy and skews fine-dining, which damages Q9 because diffusion frequently starts in casual formats. Redraws were the decisive rejection: a rule that can be re-run on inspection is not a rule, and the seed must be declared before the frame is enumerated or it is a selection rather than a seed. Stratifying on route rather than on price, format or neighbourhood follows the general constraint that **no variable which is an outcome in `20-twenty-questions.md` may be stratified on** — quota-ing price bands would make Q15's answer "the price points I put in the quota."

**Carried with it:** Route B is load-bearing for Q12, not a breadth supplement — if every cohort venue is guide-listed there is no recognition variance at t0 and the question is dead before collection starts. Hence the 12/8 quota. The frame refreshes quarterly at a new frozen date and never accepts ad-hoc additions, because `08-trend-detection.md` §5 cohort-bias correction requires an addition date to correct against.

**Reverses if:** enumeration shows a city's frame is too small to support a 12/8 split, or the calibration test in §11 produces three or more disagreements whose reasons can be stated in observable terms — that would mean the rule has real gaps rather than the operator having hypotheses.

---

### D-024 · 2026-07-29 · Ownership scale is a recorded attribute, not an exclusion filter · **Accepted** — reverses a `00-project-brief.md` §4 assumption

**Decision:** the previous exclusion of groups operating more than ~10 venues is withdrawn. Ownership scale is recorded per venue as `independent` / `small_group` (2–10) / `large_group` (>10). Press-inflated large-group share is measured and reported, **not** corrected with a quota.

**Alternatives:** keeping the filter; keeping the filter for the cohort while enumerating large groups in the frame; stratifying the cohort draw on ownership scale.

**Reasoning:** raised by an external reviewer on the grounds that group innovation is interesting, which is not sufficient. The decisive argument is narrower and harder: **Q18 asks how ownership concentration is changing per city, and concentration is arithmetically unmeasurable on a frame that excludes the concentrators.** The filter was also largely redundant — Routes A and B already exclude QSR and the mass market, since a chain outlet is neither guide-listed nor covered as a press subject. Stratifying on ownership scale was rejected under the same rule as D-023: ownership mix is part of Q18's answer, so quota-ing it fixes the answer in advance.

**What this changes:** `00-project-brief.md` §4 previously read "Not chains, not QSR, not the mass market." The QSR and mass-market exclusions stand; the size rule does not.

**Reverses if:** the enumerated frame turns out to be dominated by large-group venues to the point where the cohort draw rarely returns independents — that would mean press bias is doing more work than expected, and the response is a stated caveat plus a possible second stratum, not a reinstated filter.

---

### D-025 · 2026-07-29 · The frame records exclusions with reason codes; route non-appearance is not recordable · **Accepted**

**Decision:** venues that enter the frame via a qualifying route but fail a hard filter are **kept as rows** with an `excluded_reason` code (`outside_boundary`, `no_published_menu`, `not_trading`, `opening_pending`, `membership_only`, `hotel_not_standalone`, `duplicate_of`), not deleted. Closure sets `not_trading`; it never deletes a row. Every published coverage claim is two sentences: the cohort denominator, and the statement that the frame is attention-bounded and the population below it unmeasured. The second sentence never carries a number.

**Alternatives:** dropping non-qualifying venues silently; attempting to estimate the below-attention population.

**Reasoning:** exclusions become measurable data at almost no cost — "278 of 312 qualifying London venues publish a retrievable menu" is a publishable denominator that would otherwise be an unknown. The critical limit is that this only works for hard-filter failures. The frame is *constructed from* the routes, so a venue no guide lists and no registered publication has covered never generates a row at all. The exclusion log will therefore look like a complete accounting of what is missing while sizing the largest blind spot at exactly zero, permanently. Stating that limit alongside the log is the entire point of the decision.

**Reverses if:** a mechanical, reproducible way to enumerate below-attention venues appears — a comprehensive licensing or food-hygiene register with usable segment filtering would be the realistic candidate. Until then this is a stated limitation, not a gap to close.

---

### D-026 · 2026-07-29 · No origin claim without a census frame · **Accepted**

**Decision:** Q9 in year one reports diffusion shape, not origin. No first-originator claim may be published for a city whose frame is a sample rather than a census. Cohort-first appearances are publishable only with the cohort definition attached and the words "in the cohort" present. This sits alongside the existing archive-bias rule (no first-appearance claim within a city's first two coverage quarters) and is added to `08-trend-detection.md` §5 and §8.

**Alternatives:** publishing cohort-first as first with a footnote; adding a second cohort — a census of frame venues opened within the last 24 months — to target the origin window directly.

**Reasoning:** a random 20 of a ~300-venue frame gives an unbiased read of how a practice spreads and an unreliable read of where it started; the earliest sampled venue is usually a mid-chain adopter. The three categories where practices most plausibly originate — openings in months 0–6, pop-ups and residencies, and non-restaurant sites such as bakeries and coffee — are all excluded by construction. False attribution is worse than "unknown" because it looks publishable and a named venue makes it feel verified. Copenhagen, the near-exhaustive city, is the only place an origin claim comes close to defensible, and even there it is origin-within-frame.

**The deferred fix, recorded so it is not silently forgotten:** the recent-openings census cohort would target the origin window directly and overlaps work Q17 needs anyway. It roughly doubles Copenhagen's collection load and was declined on scope grounds, not on merit.

**Reverses if:** the month-6 review shows sustainable hours materially above the 4–5 assumed floor, in which case the recent-openings cohort becomes affordable and this constraint loosens for whichever city gets it.

---

### D-027 · 2026-07-29 · F2 records three publication states, not a pass/fail · **Accepted** — amends `D-023` after calibration

**Decision:** F2 becomes `menu_publication_mode` with three values. `full` (dish list and prices) passes and serves Q1–Q7. `price_only` (a venue-set price, no dish list) passes and serves **Q4 and Q5 only**. `none` fails. The artefact must be published by the venue or on its behalf — its own site, or its Tock / SevenRooms / Resy page where it sets the price — not compiled about it by an aggregator. `menu_publication_mode` is a tracked attribute, not merely an exclusion flag, so a venue moving between states is a dated event.

**Alternatives:** keeping the original single test; dropping F2 entirely and collecting whatever exists; accepting third-party aggregator menus.

**Reasoning:** calibration excluded **Alchemist** — two Michelin stars, top five in the world, the highest-profile venue in the census city — because it sells prepaid Tock tickets at a published price and publishes no dish list. Enigma, structurally the same proposition, publishes a dated menu PDF and passed. A price and a dish list are different artefacts and bundling them cost a venue that can answer two of the twenty questions perfectly well. Accepting aggregator menus was rejected because it would make F2 near-vacuous — TheFork and restaurantguru carry dishes for almost everything, including Bar Brutal, which the rule should continue to exclude.

**What this costs:** every Group A count now needs a second denominator — "17 of the 44 tracked venues that publish dish lists," not "17 of 60 tracked." More bookkeeping and one more place to get it wrong. Carried into `09-editorial-and-predictions.md` §2.

**What calibration also corrected:** menu publication is a venue-level choice, not a property of format. Enigma and Alchemist are the same format and differ. The F2-excluded set is therefore not the clean "fast-rotating venues" category previously assumed, which slightly weakens the Q6 bias claim in `21` §9.1 — the bias is real but cannot be characterised and dismissed.

**Reverses if:** `price_only` venues turn out to be so few that the second denominator is noise, or so many that Group A counts are routinely reported on under half the cohort — in which case the state boundaries need redrawing rather than the three-state design abandoning.

---

### D-028 · 2026-07-29 · F6 collapses into the qualifying routes · **Accepted** — amends `D-023` after calibration

**Decision:** the structural hotel test — a name distinct from the hotel's, and a menu page at its own URL — is withdrawn. A hotel F&B outlet is in scope if it holds a qualifying route **in its own right, listed as a restaurant under its own name** in the guide's restaurant selection rather than the hotel selection. `venue_type = 'hotel_restaurant'` and the hotel group as parent are recorded either way.

**Alternatives:** keeping both clauses; requiring a separate domain; reinstating the original judgement question from `06` §5.

**Reasoning:** calibration showed both clauses inert. **Alain Ducasse at The Dorchester** satisfies "a name distinct from the hotel's" while containing the hotel's name in full. **Moments** satisfies "its own URL" on a sub-page of the hotel's own site, and essentially every hotel provides one per outlet. Requiring a separate domain would have been worse, excluding Moments — a Michelin-starred destination restaurant — on a web-hosting decision. Third-party listing under the venue's own name is the independent-identity test, performed by someone other than the operator, and it is the same test every non-hotel venue already faces.

**What this costs:** the guide's threshold for listing a hotel restaurant is now the project's threshold. If Michelin becomes more or less inclined to list hotel F&B, the project's hotel coverage moves with it, and that movement will look like a real-world change. Note it before publishing anything about hotel F&B share.

**Reverses if:** hotel outlets enter the frame in numbers that suggest guides are listing guest-dining operations rather than destination restaurants.

---

### D-029 · 2026-07-29 · The calibration test was run, and the rule was amended after seeing the results · **Recorded**

**What happened:** twelve venues across three cities, verdicts pre-registered by the operator before the rule was applied. Seven clean expected-vs-actual comparisons produced **six agreements and one disagreement** (Bar Brutal, excluded on F2 against an expected include). Full results in `21-venue-inclusion-criteria.md` §11.1.

**Why this entry exists:** `21` §11 requires that any amendment made after seeing calibration results be dated, because an amended rule is fine and a quietly amended rule is not. Four amendments were made: `D-027` (F2), `D-028` (F6), a new **F0 entity-resolution step** — a supplied venue name matched four different Barcelona restaurants and no verdict could be issued — and a definition of what counts as one of a group's venues for `ownership_scale`, prompted by JKS Restaurants counting partnered and invested concepts in its own published tally. Only operated venues count.

**On the one disagreement:** Bar Brutal was excluded on F2 and the operator's stated reasons for inclusion — cultural importance, a site where practices originate — are hypothesis language rather than observable criteria, which under `21` §11 means the rule is correct and the expectation was hypothesis-driven. Recorded rather than acted on. **Pompette in Copenhagen failed identically**, which makes the natural-wine-bar exclusion structural rather than a Barcelona artifact.

**Findings recorded and not acted on:** Route B does not exist and blocks enumeration; members' clubs are invisible rather than excluded, but are enumerable if the operator wants them counted; London's A2 may be too narrow, since Bouchon Racine placed first in the UK at the National Restaurant Awards 2026 and the NRA Top 100 is not a registered route.

**Reverses if:** nothing — this is a record, not a decision. The amendments it describes each carry their own reversal conditions.

---

### D-030 · 2026-07-29 · Route B publication registry set · **Accepted** — unblocks enumeration

**Decision:** the Route B registry is `06-source-registry.md` §4A — 7 titles for Barcelona, 7 for London, 5 for Copenhagen — governed by four registration criteria: produces dated news rather than evergreen guides; has a searchable dated archive; is live within the trailing 24 months; is a publication rather than an award list. Two counting rules added: the two qualifying items must come from **two different** titles, and syndicated wire copy counts once. `source_language` is recorded per citation.

**Alternatives:** the operator's original list unamended; an English-only Copenhagen registry; including award lists as press.

**Reasoning:** the operator's framing — optimise for coverage rather than prestige, so the registry sees the ecosystem from several angles — is correct and was kept. Four amendments. **Eater London removed**: verified shut down February 2023, so it cannot produce an item inside the 24-month window; liveness became criterion 3 as a result. **World's 50 Best and 50 Best Discovery removed from Route B**: they are award lists, and admitting them collapses the recognition-versus-attention distinction Q12 is built on. **Bloomberg and Euroman removed** on yield. The two-different-publications rule was added because two items in one outlet is one outlet noticing, not attention — this shrinks the B-only stratum and is the right trade.

**Recorded and not fixed:** London carries three trade titles and Barcelona none, so London's Route B will catch operator and group news Barcelona's will not — inflating London's large-group share (`D-024`) and damaging Q8 and Q18 comparability. Barcelona also has no Catalan-language title despite `06` §4 identifying Catalan sources as the least-contested material available to the project. Copenhagen is the thinnest registry at five titles and is the census city.

**Reverses if:** enumeration shows a city's B-only pool below 8 venues, in which case that city's registry needs widening before the cohort draw — and the widening is logged, not quietly applied.

---

### D-031 · 2026-07-30 · No LLM extraction into the frame · **Accepted**

**Decision:** any source that determines **frame membership** is retrieved to raw markdown or HTML, stored as a dated artefact with `retrieved_at` and its source URL, and parsed into rows by deterministic code — DOM selectors or pattern matching, not a model. Firecrawl's LLM-extraction mode is not used against Class C guide listings, and the same rule governs the Route B headline/first-paragraph test.

**Scope, stated because it is narrow:** this constrains *what enters the frame*. It does not touch LLM extraction downstream of a stored artefact — menu dish parsing in Phase 2 works as designed in `07-extraction-schemas.md`, because a misread dish is visible against the stored menu and correctable under `D-003`. The distinction is recoverability, not distrust of models.

**Alternatives:** Firecrawl `/extract` with a JSON schema, which is the obvious and much faster route; an LLM parse of the stored markdown; manual transcription of every listing.

**Reasoning:** `D-004` already bars an LLM from computing a published number. The frame sits upstream of every number the project will ever publish — it is the denominator of every count, and `21` §5 requires that every count states one. A model that drops one entry or invents one produces a frame that is wrong in a way nothing can surface: the row is simply absent, and the exclusion log cannot show it, because a venue that never entered the frame generates no row to write a reason on (`21` §5). That is the same asymmetry as the entity-resolution rule — a visible duplicate beats an invisible bad merge. A deterministic parser fails loudly when a site is redesigned; it returns zero rows or throws, which is noticed. A model degrades quietly and returns a plausible list. The cost is real: selectors break, and each quarterly refresh (`21` §7) may need parser maintenance. Accepted, because a broken parser announces itself and a confabulated list does not.

**Reverses if:** a registered frame source publishes its listing in a form no deterministic parser can address — entries only as images, for instance. In that case LLM transcription may be used for that source **only** with a full manual check of the resulting row count and every venue name against the source, and the check recorded with its date. The exception is per-source and logged, never general.

---

### D-032 · 2026-07-30 · Listing scrapes assert their row count and halt on mismatch · **Accepted**

**Decision:** any crawl producing frame rows captures the source's own stated result total — the "N restaurants" label, the pagination count — and compares it to the rows parsed. On mismatch the run **fails and writes nothing**. Where a source publishes no total, the run records that absence explicitly and the operator verifies the count by hand once before the frame is used.

**Alternatives:** log a warning and continue; accept the rows and sample-check afterwards; trust the crawler's success response.

**Reasoning:** partial retrieval is the *default* failure mode for lazy-loaded and paginated listings, and it is silent — a scrape returning 20 of 180 entries reports success, and the resulting frame is indistinguishable from a correct one by inspection. `21` §5's coverage sentences quote frame totals, and Q15 and Q18 are answered from the frame, so an undersized frame does not produce a visibly wrong answer; it produces a confidently wrong one. This is the operating rule applied to collection: a pipeline that inserts garbage is worse than one that stops.

**Reverses if:** not as a principle. The *count source* for a given publisher can change — if a guide stops publishing totals, the manual verification described above becomes the standing procedure for that source, and that substitution is logged as a change-log row rather than applied quietly.

---

### D-033 · 2026-07-30 · A rolling source's vintage is the stored snapshot · **Accepted**

**Decision:** for a registered frame source that publishes no dated edition — White Guide Denmark is the first — the **stored snapshot is the edition.** The retrieval produces an artefact saved with `retrieved_at`, and that timestamp is cited as the vintage wherever an edition date would otherwise appear. Any later claim about what the source listed at a frame date is answered from the stored file, never from the live site.

**Alternatives:** treat the live site as authoritative and accept irreproducibility; drop White Guide as Copenhagen's A2 and leave the city on Michelin alone; require the publisher to supply a dated edition, which they do not offer.

**Reasoning:** `21` §1 sets one standard — a stranger with this documentation should reproduce the same frame. A rolling weekly-updated site cannot meet that on its own, because the October reader and the July reader see different lists with no way to reconstruct the difference. Snapshotting moves the reproducibility guarantee from the publisher to this project's own archive, which is where every other temporal guarantee in the design already sits (`D-003`, append-only facts; `01`'s `observed_at` / `retrieved_at` split). It also costs nothing that is not already being paid: `D-031` requires storing the raw artefact anyway. The operator asked Claude to decide this; recorded here so the decision is attributable rather than absorbed.

**The limitation, stated because it is not free:** the snapshot fixes *our* record, not the source's behaviour. A venue added to White Guide on 26 July and read on 30 July is in; the same venue read on 27 July is out. The frame date and the retrieval date are therefore not the same object for rolling sources, and both must be recorded per source. Where they differ, the retrieval date is the honest one to publish.

**Reverses if:** White Guide begins publishing a dated annual edition, in which case the edition supersedes the snapshot and the change is logged. Also revisit if the gap between frame date and retrieval date for any rolling source exceeds one month, which would make the two dates materially different rather than technically different.

---

### D-034 · 2026-07-30 · A `NOINDEX` page is collected and stored · **Accepted**

**Decision:** a `meta robots NOINDEX` directive on a venue's own page does **not** exclude it from collection. Such pages are fetched, stored, and cited like any other. Alouette's menu page is the first instance.

**Alternatives:** treat `NOINDEX` as a signal to skip; collect but do not store the artefact; ask each venue.

**Reasoning:** `NOINDEX` is an instruction to search engines about *listing a page in public search results*. It is not a crawl directive — the equivalent crawl directive is `Disallow` in `robots.txt`, which `10` §2 already commits to respecting and which is checked separately per source. This project does not republish menu pages, does not compete with the venue's search presence, and reproduces no descriptive text (`10` §3). Conflating the two directives would exclude venues on a web-hosting decision, which is the same error `D-028` corrected when F6 nearly excluded Moments over a sub-page URL.

**The boundary this does not cross:** `robots.txt` `Disallow` still means do not fetch. A login, paywall, or any technical access control still means do not bypass (`10` §2). `NOINDEX` is narrower than all of these and is the only one being ruled on here.

**Reverses if:** a venue asks this project to stop collecting its pages, which `10` §2 already requires be honoured immediately and without argument — that is a per-venue instruction and outranks this rule. Also revisit if a registered A2 or B source, as opposed to a venue, uses `NOINDEX` across its listings, since the intent at publisher scale may differ from one restaurant's menu page.

---

### D-035 · 2026-07-30 · Aotori is one venue · **Accepted** — operator decision

**Decision:** the MICHELIN entry whose URL slug is `kappo-ando`, whose display name is *Aotori*, and which Google Places returns as *"Aotori / Akaton"* at Øster Farimagsgade 93, is recorded as **one venue** under the name **Aotori**, with `Akaton` and `Kappo Ando` held as aliases.

**Alternatives:** two venues sharing an address; leave `unresolved` and collect nothing until the operator has visited.

**Reasoning:** F0 requires a candidate to resolve to exactly one trading venue, and this one presented three names across two sources. The operator, who knows the market, judged it a single operation. Recording the alternative names as aliases rather than discarding them matters, because the next quarterly refresh will hit the same ambiguity and a future reader needs to see that it was decided rather than missed.

**The precedent this sets, stated because it will be used again:** where a guide name, a URL slug and a Places listing disagree but share one address, the operator's judgement resolves it and the losing names become aliases. This does **not** license auto-merging on address alone — `01`'s rule stands that a visible duplicate beats an invisible bad merge, and address collision is not sufficient evidence by itself. What made this safe was a human who knows the venue, not the address match.

**Reverses if:** Akaton is found to trade as a distinct venue with its own menu and its own booking — in which case the row splits, both halves keep the shared address, and the split is logged.

**Closed 2026-08-01 by `D-046`.** The operator confirms one venue. The note carried on the A1 frame row — *"needs an operator decision before collection"* — is discharged.

---

### D-036 · 2026-07-30 · White Guide's Recommended tier is kept; the Repsol precedent does not transfer · **Accepted**

**Decision:** Copenhagen's Route A2 takes **all five** White Guide classifications — Global Masters, Masters, Very Fine, Fine and Recommended. No tier is cut.

**Alternatives:** cut Recommended by analogy with `D-023`-era reasoning on Guía Repsol's second tier; cut Fine and Recommended both.

**Reasoning:** the Repsol cut was made on a size argument, not a quality one — 1,605 national second-tier entries against 808 Soles would have made Barcelona's frame several times the size of the other two cities and swamped the sample. Measured on 2026-07-30, White Guide's Recommended tier is **3 restaurants nationally** (Masseria, Mejerigaarden, Royal Garden), two of them in Copenhagen, against 199 venues in total. That is 1.5% of the list. The swamping risk the Repsol cut existed to prevent is absent, and cutting the tier would remove two Copenhagen venues for no reason beyond a false analogy.

**The general point, recorded because it will recur:** two guides' bottom tiers can occupy the same structural position and be entirely different objects. Structural position is not evidence of size. Any future tier-scope decision measures the tier before reasoning about it.

**Reverses if:** White Guide's Recommended tier grows past roughly 15% of its Danish list, at which point the swamping argument becomes live and the cut should be reconsidered — measured at a quarterly refresh, not assumed.

---

### D-037 · 2026-07-30 · Where a source states no total, tier subtotals reconcile against the full list · **Accepted** — implements `D-032`'s fallback

**Decision:** for a frame source that publishes no result count, `D-032`'s assertion is satisfied by an **internal reconciliation**: enumerate the full list, enumerate each of the source's own categories separately, and require the category subtotals to sum exactly to the full-list row count. A mismatch fails the run exactly as a stated-total mismatch would.

**Alternatives:** accept the operator's one-off hand count as `D-032` originally specified; accept two identical scrapes as evidence of completeness; skip the assertion.

**Reasoning:** `D-032` was written assuming publishers state totals. Michelin does; White Guide does not. Two identical scrapes only prove the page renders consistently, not that it renders everything — a listing truncated at the same point twice looks identical both times. Reconciling against the source's *own* categorisation is a genuinely independent check, because a truncated list would leave category subtotals short of the whole. First applied 2026-07-30: 28 + 69 + 82 + 21 + 3 = 203 rendered rows, matching the unfiltered list exactly, with every entry carrying exactly one classification.

**The limitation, stated plainly:** this proves the list is internally complete, not that the publisher's database is fully exposed. If White Guide's search silently omits a category, no amount of internal reconciliation would reveal it. This is a stronger check than none and weaker than a stated total, and the frame documentation must say which kind it rests on.

**Reverses if:** a source's categories are found to overlap or to leave entries uncategorised, which would break the sum test — in which case the operator hand-count fallback in `D-032` applies instead.

---

### D-038 · 2026-07-30 · Anarki's A2 classification is Masters · **Accepted** — operator decision

**Decision:** Anarki (Vodroffsvej 47, Frederiksberg; White Guide venue ID 9638) is recorded at **Masters level**. The Very Fine listing is treated as a superseded classification still rendering in the source, and is not recorded as a second row.

**Alternatives:** record Very Fine; record both and let the venue carry two tiers; leave `unresolved`.

**Reasoning:** the source returns one venue ID under two classifications simultaneously, which is a contradiction the guide itself has not resolved. No mechanical rule can choose, because the page offers no dates, no ordering, and no precedence between the two renderings. The operator, who knows the venue, judged Masters current. This is the second case in this project where a source contradicted itself and only a person could settle it — the first was akmē's two prices — and both were caught because a human looked, not because a check fired.

**What this does not establish:** that the higher classification always wins. Anarki was decided on the operator's knowledge of the venue, not on a rule that Masters outranks Very Fine. If a second dual-classified venue appears, it gets the same individual treatment, not this outcome by analogy.

**Reverses if:** White Guide's own listing resolves to Very Fine on a later retrieval, in which case the change is recorded as a new fact under `D-003` with its own `observed_at` — a reclassification is a real event and belongs in the record, not a correction.

---

### D-039 · 2026-07-30 · "Propaganda – next door" is one venue with Propaganda · **Accepted** — operator decision

**Decision:** the White Guide entry *Propaganda – next door* (Vester Farimagsgade 2) resolves to the same venue as Propaganda, and is recorded as **one venue** under the name Propaganda, with "next door" held as an alias.

**Alternatives:** two venues at one address; leave `unresolved` pending a visit.

**Reasoning:** F0 requires resolution to exactly one trading venue. Google Places returns a single establishment; the guide lists a named sub-concept. The operator judged them one operation. Consistent with `D-035` (Aotori), and the same reasoning applies: guide naming and trading identity are different things, and the operator's market knowledge is the resolving evidence — not the shared address.

**The boundary this does not cross:** shared address alone still resolves nothing. Guldbergsgade 29 hosts Bæst, Mirabelle and Brus as three genuinely distinct venues, and Ryesgade 65 hosts Grim and Tèrra. An address-based auto-merge would have destroyed all five. `01`'s rule stands — a visible duplicate beats an invisible bad merge.

**Reverses if:** the two concepts are found to trade separately with distinct menus and bookings, in which case the row splits and both halves keep the shared address.

---

### D-040 · 2026-08-01 · F0 is an identity test; trading belongs to F4 · **Accepted** — amends `D-029`

**Decision:** F0's wording changes from "exactly one **trading** venue" to "exactly one venue." A venue that is closed but unambiguously identified passes F0, takes an F1 verdict on its resolved address, and fails F4 as `not_trading`. `google_place_id` becomes conditional — "where one exists" — because an exclusion row does not need one.

**Alternatives:** leave F0 as written and accept that confirmed closures sit in `unresolved`; add a third state to F0.

**Reasoning:** one filter was answering two questions and answering the second one badly. `unresolved` means *we could not tell what this is*; `not_trading` means *this closed*. Q13 is a survival question and can only be asked if the second category is countable, so a rule that pushes confirmed closures into the first bucket destroys the measurement it depends on. Kiin Kiin Tok Tok was the live case: identified by the operator at White Guide's own stated address, permanently closed, and filed as unidentifiable.

**The larger finding, which is why this is a rule and not a row edit:** the Google Places API **does not return permanently closed venues.** A candidate that shut before enumeration presents as a *wrong-venue match* — the query returns the nearest still-trading business, that match is correctly rejected, and the row lands in `unresolved`. Re-tested 2026-08-01 on both Copenhagen cases; both returned the same wrong venues as at enumeration. So `unresolved` is a mixture of ambiguity and unrecognised closure in unknown proportion, in every city, and no coverage claim may describe it as a measure of ambiguity.

**Reverses if:** a resolution source is adopted that returns closed listings with a closure date, at which point closure becomes observable at enumeration and the two categories separate automatically.

**Interpretation amended 2026-08-01 by `D-044`.** The finding above — that Places does not return permanently closed venues — **stands unchanged**. What does not stand is the characterisation built on it. This entry read `unresolved` as principally *unrecognised closure*, on a sample of 2 of 2. On the full 14 Copenhagen rows, adjudicated by the operator the same day, it was **12 unrecognised geography and 2 closure**. See `D-044` for the mechanism and for what it implies about London and Barcelona.

---

### D-041 · 2026-08-01 · Kiin Kiin Tok Tok is `not_trading`; Toto stays `unresolved` · **Accepted** — operator verification

**Decision:** **Kiin Kiin Tok Tok** — operator confirmed the venue on Google Maps at Vesterbrogade 55, 1620 København, White Guide's own stated address, showing permanently closed. Recorded F0-resolved, F1 pass, F4 fail `not_trading`, with no `google_place_id`. **Toto** — operator found no venue and an unreachable website. Stays `unresolved`.

**Alternatives:** record both as `not_trading`; leave both `unresolved`.

**Reasoning:** the two cases look identical and are not. For Kiin Kiin Tok Tok the address was independently confirmed, so an F1 verdict is possible and the closure is established. For Toto nothing was confirmed — Amagerbrogade 145 remains the guide's unverified assertion, so no boundary verdict can be issued, and "the venue seems to be gone" is not evidence of closure at the frame date. Closure is likely; likely is not recorded as established.

**Dating caveat, which travels with the row:** the closure was observed **2026-08-01**, four days *after* frame date 2026-07-28, and Google publishes no closure date. The frame-date verdict is therefore an **inference**, not an observation, and is labelled as one in the file. It is not backfilled. The spreadsheet cannot carry two observation dates on one row — `observed_at` there dates the White Guide listing — which is precisely what `venue_facts.valid_from` exists for once the schema is deployed.

**Effect on the frame: none.** Kiin Kiin Tok Tok has no place_id and could not have joined a place_id-keyed union. Copenhagen's A1 ∪ A2 frame is **132** before and after.

**Reverses if:** a dated closure notice places the closure after 2026-07-28, in which case the venue was trading at the frame date and re-enters as an F1 pass.

---

### D-042 · 2026-08-01 · A2's suspected staleness is pre-registered before F4 runs · **Reversed** 2026-08-01

**Decision:** prediction `M1` is recorded in the prediction ledger, on a separate **Method predictions** sheet, before F4 is applied to Copenhagen's frame: the closure rate among the 64 A2-only frame venues will exceed the closure rate among the 68 holding a MICHELIN listing.

**Alternatives:** add it to the Hypotheses sheet; wait until F4 runs and report the difference then.

**Reasoning:** MICHELIN Nordic 2026 is a dated edition, White Guide publishes none (`D-033`). If that asymmetry has a measurable cost it should show up as closures, and the claim is worth nothing if written after the numbers are seen. It goes on its own sheet for two reasons: it is a prediction about the *method*, not about restaurants, and it is **Claude-originated** — the Hypotheses sheet holds the operator's own words and must not be contaminated by a machine's guess. Operator confidence is left blank pending endorsement.

**Reverses if:** the operator declines to endorse it, in which case the row is deleted rather than left unowned.

**Reversed 2026-08-01, the same day.** The operator declined to endorse `M1` and it was deleted from the prediction ledger, which is exactly the reversal condition this entry specified. The **Method predictions** sheet remains as a structure but holds no live prediction. A red-flagged line records that `M1` was proposed and deleted **unendorsed**, and that it must never be scored, cited or reconstructed after F4 runs — a deleted prediction returning as a claimed pre-registration would be worse than never having written it. Note also that `M1` rested on the 2-of-2 closure sample that `D-044` has since shown to be misleading.

---

### D-043 · 2026-08-01 · The canonical name is the venue's own, not the best source's · **Accepted**

**Decision:** a venue's canonical name is **the name it publishes for itself, in its own orthography**, captured at the F2 pass when venue sites are fetched. It is not decided by source precedence. Until F2 runs, the union file's name column is called `display_name_provisional`, holds the MICHELIN string as a placeholder, and **no name may be published from it**.

**Alternatives:** MICHELIN string wins where present; White Guide/Danish string wins; longest string wins; first-observed string wins.

**Reasoning:** a source-precedence rule does not scale and is not stable. It says nothing about the 64 A2-only venues, nothing about London and Barcelona whose A2s are different guides, and nothing about Route B, which is 19 publications with no defensible ordering between them. Worse, it makes the name a function of source membership: a venue dropping out of the 2027 MICHELIN edition would have its canonical name flip, appearing as a rename in the very time series the project exists to read. The venue's own name is source-independent, survives guide churn, and satisfies `D-020` on original-language preservation. It also costs nothing extra, because F2 already fetches the venue's site.

**The structural half of the decision:** identity is `google_place_id` and nothing else. The name is a **label**, and the schema already has the right shape for it — `entity_aliases` holds every source's string; `entities` points at one nominated alias. See `D-047`.

**Reverses if:** F2 shows a material share of frame venues publish no name of their own in a stable form, in which case a precedence rule becomes the fallback and must be written down before it is applied.

---

### D-044 · 2026-08-01 · All 14 Copenhagen `unresolved` rows adjudicated; `unresolved` was a geography failure, not a closure failure · **Accepted** — amends the *interpretation* in `D-040`

**Decision:** the operator checked all 14 remaining `unresolved` rows in Copenhagen's A2 by hand against Google Maps. **12 are trading venues outside the F1 boundary** — reclassified `outside_boundary`, with the operator-confirmed address recorded on the row. **2 no longer exist** — VesterVenner - Strandgården Badehotel and Toto, reclassified `not_trading`. Copenhagen's `unresolved` count is now **zero**.

**A2 now reads: 199 = 109 pass F1 + 87 outside_boundary + 3 not_trading + 0 unresolved.** The frame is **unchanged at 132**, and the "132 plus up to 14 unadjudicated rows" caveat is discharged.

**Alternatives:** report `unresolved` as a residual and move on; check a sample rather than all 14.

**Reasoning, and why this amends `D-040`:** `D-040` concluded from 2 of 2 checked cases that `unresolved` mixes ambiguity with *unrecognised closure*. On the full 14 that is wrong by a wide margin — it was overwhelmingly **unrecognised out-of-boundary geography**, 12 of 14. `D-040`'s underlying finding stands unchanged: Google Places does not return permanently closed venues, and that remains true and load-bearing. What does not stand is the characterisation built on a sample of two. Recorded here rather than by editing `D-040`, because the sequence — small sample, confident inference, full check, reversal — is itself the finding.

**The mechanism, which is the part that travels:** White Guide's address strings on these rows are **truncated to street and number with no locality** ("Annebergparken 50,"). F1 could not be applied to the guide's own text, so the rows fell through to Places resolution — **which was scoped to Copenhagen**. A venue in Agger, Sønderborg or Tórshavn had no way to resolve, returned a wrong Copenhagen match, was correctly rejected, and landed in `unresolved`.

**This will recur in London and Barcelona, and will be harder to see there.** Both cities' guides cover far more territory than the target city, and a wrong match in Greater London or greater Catalonia looks plausible in a way that a wrong match for a Faroese venue does not.

**Second finding: White Guide Denmark includes the Faroe Islands** — 5 of the 199, all Tórshavn or Sandavágur. The guide's actual territory had never been established, which bears on `D-037`, where A2 completeness was asserted by tier reconciliation.

**Three address discrepancies against the guide, recorded not resolved:** Restaurant Domæne (guide Gødstrupvej 60, found 62), Syttende (guide Nørre Havnegade 23, found 25), Etika (guide Heiðavegur 35, found Áarvegur 3 — a different street, so possibly a relocation). None affects F1. All three matter because 75 of A2's original exclusions rest on the guide's own address text, which is now shown to be wrong in at least 3 of the 14 cases where it could be checked.

**The two closures keep `D-041`'s distinction.** Only Kiin Kiin Tok Tok carries a confirmed F1 pass. VesterVenner and Toto are closed, but neither address was independently confirmed, so **no F1 verdict is possible** on either; they are excluded on F4 and counted in no F1 line. All three carry `D-041`'s dating caveat: closure observed 2026-08-01, four days after frame date, no published closure date, so the frame-date verdict is an inference and is not backfilled.

**Reverses if:** a resolution source is adopted that accepts a bare street address without locality, or that returns closed listings with dates — at which point most of this bucket resolves mechanically.

---

### D-045 · 2026-08-01 · A1's four Danish out-of-boundary exclusions cite the wrong evidence · **Accepted** — correction

**Decision:** rows 73–76 of `cph-route-a1-frame.xlsx` (Jordnær, Parsley Salon, The Samuel, Søllerød Kro) had notes reading *"Fails F1 on the guide's city label."* All four have resolved addresses and resolved kommunes — Gentofte ×3, Rudersdal ×1 — so they fail on the **resolved address**. Notes corrected. The count-block label at row 96 now reads "4 on the resolved address, 11 on country," since the 11 Malmö rows never had a resolved address to fail on.

**Reasoning:** `21` §12.1 requires F1 to be applied to resolved addresses only, precisely because MICHELIN's city label is not a boundary — six "Copenhagen" venues are in Frederiksberg and Restaurant VIE is filed under "Nordhavn." The verdicts were right; the recorded basis contradicted the project's own rule, and a stranger auditing the file would have found the rule and the evidence disagreeing.

**Counts unaffected** — all four are outside the boundary on either basis. **Reverses if:** nothing. This is a correction.

---

### D-046 · 2026-08-01 · Aotori / Kappo Ando is one venue · **Accepted** — closes the open question in `D-035`

**Decision:** operator-confirmed as **one venue**, carrying one row and one `google_place_id` in the frame. `D-035`'s note that it "needs an operator decision before collection" is discharged.

**Reasoning:** one venue is named four ways across sources — MICHELIN display *Aotori*, MICHELIN URL slug *kappo-ando*, White Guide *Kappo Ando*, Places *Aotori / Akaton*. Both routes resolve to the same address, Øster Farimagsgade 93. It is classified `distinct_name` in the union file rather than as a spelling variant, because it is not a variant of one string and must not be filed alongside "Restaurant Levi / Levi."

**Reverses if:** the two names are found to trade as separate concepts with distinct menus and bookings — the same condition as `D-039`.

---

### D-047 · 2026-08-01 · Names become dated facts; `canonical_name` becomes a pointer · **Accepted**

**Decision:** two amendments to `schema.sql`. Written first as `schema-patch-D047.sql`, then **folded directly into `schema.sql` on 2026-08-01**, which now parses clean at 69 statements and needs no replay. The patch file is retained as the record of the change and marked *do not run*. (1) `entity_aliases` gains `observed_at`, `retrieved_at`, `valid_from`, `valid_to`; `source_id` becomes `NOT NULL`; the unique constraint moves from `(entity_id, normalised_alias)` to `(entity_id, normalised_alias, source_id, observed_at)`. (2) `entities` gains `canonical_alias_id`, a pointer into `entity_aliases`; `canonical_name` is deprecated to a denormalised mirror; two views are added — `v_entity_display_name` (one human string, for publication) and `v_entity_all_names` (every variant, for matching).

**Alternatives:** leave both as they are and handle naming in application logic; store a name-history table separately.

**Reasoning:** two gaps, both breaking a project rule. `entity_aliases` had `created_at` only, which is an insert timestamp and cannot say *MICHELIN called this venue X on 2026-07-28* — rule 1 requires the observation date, and `source_id` being nullable allowed an alias attached to nothing. Separately, `canonical_name` was a single mutable column with no history: changing it overwrote the previous value unless somebody remembered to write it as an alias, which nothing enforced, breaking rule 2. Making it a pointer means a display-name change is a repointing, and every name the project ever observed survives with its own dates and source.

**Why two views rather than one column:** publication wants one human string; matching wants every variant, fuzzy, via the existing trigram index. Collapsing them is how the Kadeau bug class returns — a matcher that misses because the single canonical string happened to be the English one. Copenhagen already carries 14 variants across 45 dual-route venues (4 prefix, 8 orthography, 1 translation, 1 distinct name), and 5 of the orthographic ones are case-only, which a naive normaliser discards along with the venue's own styling.

**One consequence found while folding it in, and left unresolved.** `v_venue_current` returns venue facts and **no name at all**, so any consumer wanting to publish a venue must reach into `entities.canonical_name` — the column this entry deprecates. Consumers should join `v_entity_display_name` instead. This is noted in `schema.sql` as a comment; changing `v_venue_current` is a separate decision and has not been made.

**A circular foreign key was unavoidable.** `entities` is created before `entity_aliases`, so `canonical_alias_id` cannot carry an inline `REFERENCES`; the constraint is added by `ALTER TABLE` immediately after both tables exist. That single `ALTER` is a circular-FK resolution, not migration history, and is commented as such so a future reader does not mistake it for a replayed patch.

**Reverses if:** deployment shows the alias table growing faster than it earns its keep — but note the cost of reversing after deployment is far higher than the cost of adding it now, which is why it is being done pre-deployment.

---

### D-048 · 2026-08-02 · An unreachable registered title is carried with a status, not dropped · **Accepted** — operator decision

**Decision:** every registered Route B title carries an **access status** independent of its registration — `permitted`, `blocked_by_robots`, or `pending_access` — recorded in `06` §4A with the date observed. A title we cannot retrieve is **not** removed from the registry or the frame. Every Route B coverage claim states how many titles were reachable out of how many were registered.

**Alternatives:** drop unreachable titles from the registry; fold reachability into `06` §4A criterion 2.

**Reasoning:** a venue's Route B status is a fact about what was published about it inside the window. It does not change because a publisher edited `robots.txt` afterwards. Copenhagen Post was registered on 2026-07-29 against a frame dated 2026-07-28 and became unreachable to us on 2026-08-02. Dropping it would shrink the frame for a reason that is not a property of the world, and the shrinkage would be invisible to any reader of the denominator. Criterion 2 asks whether a title *has* a searchable dated archive — a property of the publication. Whether we may crawl it is a property of our access. Conflating the two lets an access limitation masquerade as an editorial one.

**Still open, and not settled by this entry:** Copenhagen Post's disposition — hand-qualify, pursue permission under `10` §2, or leave unreached. Also open: whether to adopt a licensed archive (Retriever, formerly Infomedia), which cannot be decided before its demo.

**Reverses if:** a publisher grants explicit permission, or a licensed archive is adopted that makes site-level access irrelevant — in which case the status is updated, not the title moved.

---

### D-049 · 2026-08-02 · Absence from a `robots.txt` blocklist is not permission · **Accepted** — operator decision

**Decision:** where a publisher's `robots.txt` blocks AI crawlers by name, the **absence** of any particular agent string is not read as permission to retrieve. Politiken is recorded `pending_access`. No Politiken content is fetched pending a licence or explicit permission.

**Alternatives:** retrieve via an agent Politiken did not name; treat each publisher's list as exhaustive of its intent.

**Reasoning:** Politiken's `robots.txt` (observed 2026-08-02) names sixteen AI crawlers with a site-wide `Disallow`, including `anthropic-ai` and `Claude-Web`. `ClaudeBot` is absent. Against a list that comprehensive the omission is a gap, not a grant. The decision also does not stay contained: Firecrawl identifies as none of those strings, so "the string is not named" would equally license Copenhagen Post, which names `ClaudeBot` **explicitly**. Both cases collapse into one principle — that `robots.txt` does not constrain this project. That principle may be arguable, but it must be adopted deliberately and in writing, not arrived at because one publisher's list had a hole in it. `10` §2's prohibition on rotating identity to evade blocks covers the spirit even where its letter addresses residential proxies.

**Independent of the above:** Politiken disallows `/search` for **all** agents. The free-text search route into that archive is closed however the agent question resolves.

**Reverses if:** Politiken publishes terms permitting research retrieval, grants permission on request, or a licensed archive supplies the same content lawfully.

---

### D-050 · 2026-08-04 · The wire rule applies to any agency copy, registered or not · **Accepted** — operator decision

**Decision:** `06` §4A's wire rule applies to syndicated agency copy from **any** news agency, whether or not that agency is itself a registered title. Agency copy counts **once**, attributed to the originating agency, however many registered titles republish it. Explicitly covers Ritzau in Copenhagen.

**Alternatives:** apply the wire rule only to registered wire services; treat each republication as an independent item.

**Reasoning:** the rule was written with EFE Agro in mind, which *is* a registered Barcelona title, so its text reads as though wire status follows from registration. Ritzau is not registered but syndicates into both Politiken and Berlingske. Without this amendment a single Ritzau item republished by two titles manufactures a two-items-**two-titles** qualification out of one act of journalism — precisely the failure the rule exists to prevent. Copenhagen is where it bites hardest: the thinnest registry of the three, and two of its five titles are national broadsheets that both take Ritzau.

**Build consequence:** extraction must capture agency attribution as a field and not discard it. A candidate item whose byline or dateline indicates agency origin is tagged with the agency and deduplicated against other items from that agency **before** the two-items test is applied.

**Reverses if:** agency copy in a specific market is found to be substantially rewritten per title rather than republished, making each version genuinely independent — which would need evidence, not assertion.

---

### D-051 · 2026-08-02 · Archive reach is verified per title before any sweep is planned · **Accepted** — operator decision

**Decision:** a title's archive reach across the full 24-month window is **demonstrated** before any sweep is planned against it. The default inverts: an archive is presumed **not** sweepable until a test shows otherwise. Section index, sitemap and on-site search are tested **separately**.

**Alternatives:** treat `06` §4A criterion 2 as settled at registration; test reach only after a sweep fails.

**Reasoning:** Berlingske was recommended as the first sweep precisely because it looked like the easy case — a national broadsheet with a named gastronomy section. On 2026-08-02 its section index returned 30 articles with **no pagination, no dates, and a JavaScript load-more control**; its only advertised sitemap is a news sitemap spanning roughly two days. The missing dates are disqualifying: even clicking until the control stops gives no stopping rule and no denominator. On 2026-08-10 its search endpoint (`/search?query=`, supplied by the operator after a wrong guess at `/soeg`) proved real, dated and denominator-stating — 4,289 results for `restaurant` — but **the `page` parameter is silently ignored**, and a browser-interaction test to measure recession rate **failed**. Four tests in, reach remains undemonstrated for the easiest permitted Copenhagen title. The assumption that a publisher's own site exposes its own archive is false often enough to be worth inverting, and it currently sits unexamined inside criterion 2 for all fourteen London and Barcelona titles.

**Cost, stated plainly:** this adds a verification step to every title in every city — fifteen of them. It is cheaper than discovering the problem after the work is planned.

**Three findings recorded with this entry:**

1. **Restaurant content is not confined to gastronomy sections.** A Copenhagen restaurant item was filed under `/oplevelser/`; the gastronomi index links into `/metropol/`, `/vores-liv/` and `/kultur/`. A section-named sweep undercounts **invisibly**. Each title's section list is established empirically before its sweep. Berlingske's search is section-agnostic and is therefore the better instrument.
2. **Berlingske publishes a machine-readable paywall flag.** Sitemap entries carry `news:access`, frequently `Subscription`. This makes the paywall share **countable** without fetching articles. Not yet measured — the two-day sample is far too small and is not restaurant-specific.
3. **Berlingske search is not yet demonstrably reproducible.** The same URL returned two different result sets within one session on 2026-08-10 — a scrape led by an 8 Aug piece, a browser session led by five *Byens Bedste 2026* articles. Cause unknown and deliberately not guessed at. A route that returns different results on two retrievals cannot carry a frame: rule 1 requires a source URL that means something stable.

**Reverses if:** a licensed archive is adopted across all three cities, making reach a property of one vendor's stated coverage rather than of fifteen separate websites.

---

### D-052 · 2026-08-02 · Cheaper access is not grounds to reopen the frozen registry · **Accepted** — operator decision

**Decision:** the Route B registry stays frozen as of 2026-07-29. Improved or cheaper access to a title — a licensed archive, a granted permission, a newly discovered search endpoint — is **not** a reason to add a title. Adding one requires its own decision-log entry stating what it does to the frame date.

**Alternatives:** reopen the registry when access improves; treat the freeze as advisory.

**Reasoning:** adding a title after the frame date changes what qualifies, retroactively and asymmetrically — venues covered by the new title gain qualifications that venues assessed earlier never had the chance to. `08` §5 already treats source-definition changes as the null hypothesis for any coincident signal, so a registry addition would contaminate exactly the trend claims Route B exists to support. `06` §4A notes Copenhagen is the thinnest registry and that one more Danish title would be worth having; if a licensed archive lands, that line will read as an invitation. It is not one. Written **now, while the temptation is theoretical**, because a freeze decided in advance is far easier to hold than one argued about under the pressure of a specific attractive title.

**Reverses if:** the frame is deliberately re-cut with a new frame date and the whole registry re-frozen against it — in which case every city is re-registered together, not one title added to one city.

---

### D-053 · 2026-08-10 · A publication date never comes from a sitemap · **Accepted**

**Decision:** an item's publication date is taken from the article page's own published-date field
(`article:published_time` or equivalent) and **never** from a sitemap `<lastmod>`. Where an article
exposes no published date, the item is flagged `undated_source` and does not enter a Route B count.
`lastmod` may be used to prioritise what to fetch. It may never be written to `observed_at`.

**Alternatives:** use `lastmod` where a published date is absent; treat `lastmod` as a fallback.

**Reasoning:** demonstrated, not assumed. Scandinavian Standard's sitemap stamps articles about
*3 Days of Design 2020* and *CPHDOX 2020* with `lastmod` **2023-11-08**, from a bulk re-save. One
article checked directly carries `lastmod` **2024-08-01** and a real publication date of
**2024-06-30**. A Route B window bucketed on `lastmod` would have placed items in the wrong months
and, for the migrated ones, the wrong years — while every CHECK row passed, because the arithmetic
would be correct on the wrong field. This is rule 1's `observed_at` requirement: a modification
timestamp is not an observation of publication, and backfilling one as the other is the failure
mode `00`'s five rules exist to prevent.

**Cost, stated plainly:** publication dates now cost one article fetch each. **This is smaller than
it appears** — `21` §4's headline-or-first-paragraph test already requires the article text, so the
date arrives on a fetch that must happen anyway. It is a field, not a pass.

**Reverses if:** a title is found whose sitemap `lastmod` is verifiably equal to publication date
across a tested sample — in which case the exemption is recorded **per title, with its sample size**,
never granted generally.

---

### D-054 · 2026-08-10 · Reach means dated items retrieved, not a paginator observed · **Accepted**

**Decision:** a route is credited with reach only when **dated items** have been retrieved through
it. The existence of a working pagination mechanism, a stated result count, or a well-formed index
is **not** reach and is not recorded as partial reach.

**Alternatives:** credit a route once its pagination is shown to work; treat a stated denominator as
sufficient.

**Reasoning:** two live counter-examples, one per title. Scandinavian Standard's
`/category/food-drink/page/2/` is a genuine server-side pagination URL — better-shaped than anything
Berlingske offers — yet the page returns 18 links and **zero articles** at a six-second render
delay. Real pagination over content that is not served paginates nothing. MigogKbh's sitemap index
is real, large and well-formed, and stops twelve weeks before the window ends. Berlingske states
4,289 results and silently ignores `?page=N`. In all three the encouraging signal is structural and
the failure is in the content. Crediting structure would have marked all three reachable.

**Reverses if:** nothing foreseeable. This is a tightening of `D-051`, not a new direction.

---

### D-055 · 2026-08-10 · Route B coverage is reported as reachable-over-registered, per city · **Accepted**

**Decision:** every Copenhagen Route B statement carries two numbers — titles with **demonstrated
reach** over titles **registered**. As of 2026-08-10 that is **1 of 5** (and 1 of 3 permitted).
A title with posture `permitted` but reach undemonstrated counts in the denominator and **not** in
the numerator. Route B may not be run in a city where the reachable count is below 2, because the
two-items-two-titles rule cannot function on one title.

**Alternatives:** report registered titles only; report permitted titles as though reachable.

**Reasoning:** `D-048` established that posture and qualification are different things and that
coverage states both. Stage 0b shows a third quantity was hiding inside "permitted": three of
Copenhagen's five titles are permitted, and exactly one of them has been shown to reach the window.
Reporting "3 of 5 titles available" would be true about permission and false about capability, and
the gap is invisible to any reader of a published denominator. The floor of 2 is not a judgement
call — it is arithmetic from `06` §4A's own rule.

**Reverses if:** the two-items-two-titles rule is itself amended, which would need its own entry and
would change what qualifies retroactively.

---

### D-056 · 2026-08-10 · Phase 1 works 40 venues, and they are not the cohort · **Accepted** — operator decision

**Decision:** the Phase 1 target stays **40 venues**, as originally scoped in `11-roadmap.md`. Those
40 are **method-development venues chosen by the operator**, not the seeded cohort. Nothing published
from them carries a denominator, and when the cohort is drawn (20 per city, seed `20260728`,
`D-023`), collection restarts on the cohort. `11-roadmap.md` Phase 0's "list 60 candidate venues"
line is superseded — it described hand-selection, which `D-023` exists to prevent.

**Alternatives:** cut Phase 1 to the 20-per-city cohort size; hold Phase 1 until the frame is
complete and draw the 40 from it.

**Reasoning:** Phase 1's purpose is to discover the schema from real menus and to find out whether
the report is interesting when made by hand (`D-010`). Neither purpose needs a probability sample.
Holding publication until the frame is complete would block it indefinitely — Route B is currently
unreachable in Copenhagen (`D-055`) and untested in the fourteen London and Barcelona titles — and
`11-roadmap.md`'s own priority list is explicit that a dull issue published on time beats a good one
published a month late. Keeping 40 rather than 60 also removes the buffer logic, which only made
sense for a hand-picked list that might not survive contact with F2.

**The risk this creates, stated:** the Phase 1 forty could quietly become the cohort by habit. The
guard is that the cohort is drawn mechanically from the enumerated frame and the draw is not
informed by the forty. A venue appearing in both is fine and expected; a venue entering the frame
*because* it was in the forty is the failure.

**Carried with it:** at 40 venues and ~15 dishes each, Phase 1 produces roughly 600 dated items —
the month-1 milestone figure. The five Phase 1 predictions (`D-018`) are due by roughly 2026-08-28
and are independent of all of this.

**Reverses if:** collection cost per venue proves high enough that 40 cannot be reached inside
weeks 2–6 without breaking publication cadence — in which case the venue count is cut and the
cadence is protected, never the other way round.

---

### D-056 · addendum · 2026-08-12 · **Confirmed by the operator**

`D-056` was written on instruction but never endorsed. The operator confirmed it on 2026-08-12:
the Phase 1 forty are method-development venues, not the seeded cohort. No change to the entry.

---

### D-057 · 2026-08-12 · How `observed_at` is set for a menu · **Accepted 2026-09-28** — by Claude under `D-062`

**Decision:** `retrieved_at` is the clock reading at the moment the page was loaded, always present.
`observed_at` takes the first available of:

1. a date **printed on the menu artefact itself**;
2. a published-or-updated date **exposed by the page**;
3. failing both, `observed_at = retrieved_at`.

A field `observed_at_source` records which applied — `menu_artefact` / `page_published_date` /
`retrieval` — and is mandatory. Without it nobody can later distinguish a venue-dated menu from one
dated by the act of looking at it.

**Excluded outright as date sources:** PDF internal metadata, InDesign or export filenames, HTTP
`Last-Modified`, upload paths, and anything sitemap-derived. Same failure class as `D-053` — a
re-save stamp is not an observation.

**Never inferred.** "This looks like the winter menu" is not a date. Undated is undated.

**Evidence from the 2026-08-12 fetch (8 pages, of 30 URLs supplied, of 39 venue rows):**

- **Bobe** — PDF internal title `Bobe menu 073126.indd`. Excluded correctly.
- **Enigma** — the artefact prints "VERSIÓN VERANO 77. 2026". This is a **version and a season, not a
  date**, and category 1 as drafted does not cover it. Meanwhile the filename says *abril*, the
  content says summer, and the upload path says July — **three signals disagreeing on one artefact**,
  which is the strongest available argument for the exclusion list.
- **Prodigi** — the page exposes `og:updated_time = 2026-05-28T00:57:53+01:00`. Category 2 as
  drafted would make this the first row where `observed_at ≠ retrieved_at`. But WordPress/Divi
  stamps this on **any** page edit, including a typo fix, so it dates the page and not the menu.

**Two sub-questions this leaves open, and they need the operator, not Claude:**

- **(a)** Does a printed version/season string set `observed_at`, or only populate
  `menu_date_stated` while `observed_at` falls through to retrieval? Claude's recommendation:
  the latter — a season is not a date.
- **(b)** Is `og:updated_time` (and equivalent CMS auto-stamps) admissible under category 2, or does
  category 2 mean only a date the venue authored and displayed to a reader?
  Claude's recommendation: the latter, i.e. exclude CMS auto-stamps, on the same reasoning that
  excludes `Last-Modified`. This would leave Prodigi at `observed_at = retrieval`.

**Resolved 2026-09-28 (Claude, under `D-062`):** (a) a version, season or validity string — "VERSIÓN
VERANO 77", "Autumn Universe", Disfrutar's "Price valid until 07/08/2027" — goes in `menu_date_stated`
and `observed_at` falls through to retrieval. (b) Category 2 means only a date the venue authored and
displays to a reader; `og:updated_time` and every other CMS auto-stamp is excluded, with
`Last-Modified`. Applied to the 2026-09-28 collection: every menu row fell through to `retrieval`.

**Reverses if:** a material share of menus turn out to carry venue-authored page dates that
demonstrably track menu changes, making category 2 worth the ambiguity it introduces.

---

### D-058 · 2026-08-12 · Phase 1 city split is 20 / 10 / 10 · **Accepted** — operator decision

**Decision:** the Phase 1 forty split **20 Copenhagen, 10 London, 10 Barcelona**.

**Reasoning:** Copenhagen is the only city with an enumerated Route A frame, so its twenty could be
drawn from real rows with `google_place_id`s and reconciled tiers. Q7 (menu publication language)
also needs Copenhagen volume to be worth measuring. But a schema discovered on one currency and one
language pair would break on contact with Barcelona, so London and Barcelona are represented from
the start rather than added later.

**Stated asymmetry, which must travel with any Phase 1 output:** the Copenhagen twenty were selected
from the 132-venue frame file by a **documented, non-random, fixed-order stratified fill** across
guide tiers — deliberately not a random draw, so that it can never be mistaken for the `D-023`
cohort draw. Within each stratum, rows were taken in the file's own (alphabetical) order; that bias
is visible and is judged harmless for schema discovery. The London and Barcelona tens were assembled
by **web search against the registered A1/A2 guides**, are **not enumerated**, not resolved to
place IDs, and not F1-filtered. They are usable only because `D-056` means nothing published from
them carries a denominator.

**Reverses if:** London or Barcelona enumeration completes before Phase 1 collection ends, in which
case those tens are re-drawn from the real frames.

---

### D-059 · 2026-08-12 · `dish_name_original` may not come from automated extraction · **Accepted 2026-09-28** — by Claude under `D-062`

**Decision:** original-language dish and section names are **transcribed by a human from the
artefact**. Machine extraction may populate prices, structure, section order, format and service
notes, but not `dish_name_original`, `section_name_original`, or `description_original`. A field
`name_original_transcription` records `human` or `machine_unverified`; no row marked
`machine_unverified` is eligible for the Phase 2 gold set.

**Evidence — Enigma trilingual PDF, retrieved 2026-08-12.** Three corruptions caught in the
original-language text of a single artefact:

| Published | Extracted | Failure |
|---|---|---|
| ÀNEC (ca) | ÅNEC | wrong diacritic |
| CIRERA (ca) | CIIRERA | doubled letter |
| El PATO (es) | EI PATO | lowercase L read as capital I |

Three were caught. The number not caught is unknown and unknowable without the artefact.

**Reasoning:** `D-020` makes original-language preservation the one Phase 1 habit that cannot be
recovered later. The corruption is **silent and survives review** — "ÅNEC" reads as a plausible
Catalan word to anyone who does not read Catalan, and `D-022` establishes that nobody on this
project reads Danish. An error class that is both unrecoverable and invisible to the only available
check cannot be accepted on volume grounds.

**Carried with it:** this is a real cost. It means the Copenhagen and Barcelona originals need
operator time on the artefacts themselves. It does **not** block price, structure or F2 work, which
extract reliably — so the two passes can be separated and the expensive one confined to the venues
where an original-language menu actually exists.

**Related, same session:** **The Ledbury** rendered every content block **twice** in extraction
(tabbed panels). A naive dish count returns 14; the true count is 7. Deduplicated by hand. This is
the counting-in-code failure mode in a new place — the code would have been correct and the input
doubled.

**Resolved 2026-09-28 (Claude, under `D-062`):** accepted as written, with one clarification. Machine
text is not thrown away: it is kept in a separate column, `dish_text_as_extracted`, marked
`machine_unverified`, and `dish_name_original` stays **empty** until a person transcribes it. Nothing
in `dish_text_as_extracted` may be published as a venue's original wording. The collection records
`original_language_url` per menu, which is the operator's worklist for the transcription pass.

**Reverses if:** an extraction path is demonstrated to preserve diacritics exactly across a test set
of Danish, Catalan and Spanish artefacts, with the test designed before the run and the failures
counted.

---

### D-060 · 2026-08-12 · Retrieval timestamps carry a precision field · **Accepted 2026-09-28** — by Claude under `D-062`

**Decision:** `retrieved_at` is accompanied by `retrieved_at_precision`, one of `exact` or
`batch_approximate`, and by `collected_by`. A batch window is recorded as what it is rather than
being presented as per-page precision.

**Origin:** the operator's 2026-08-12 source file carried one timestamp — `12 Aug 2026, ~11:30
CEST` — on all 39 rows across three cities. The operator confirmed the pages were opened personally
and that the window is real. The defect was never the time; it was the file presenting a batch
window as though it were 39 per-page events.

**Consequence, and a correction to a Claude claim made earlier the same session:** Claude asserted
that batch timestamps would make these rows permanently ineligible for the Phase 2 gold set. **That
was wrong and is withdrawn.** Gold-set eligibility depends on who transcribed the content and from
what, not on timestamp granularity. The eligibility constraint that *does* apply is `D-059`.

**Reverses if:** a use is found that requires per-page retrieval precision, in which case affected
rows are re-collected rather than re-dated — `retrieved_at` is never backfilled.

**Resolved 2026-09-28 (Claude, under `D-062`):** accepted. Values are `exact_minute` (a clock reading
taken by the collector immediately after the fetch) and `batch_approximate`.

---

### D-061 · 2026-09-28 · The project lives in a public GitHub repository, and GitHub is the master copy · **Accepted** (public: operator decision; master copy: Claude under `D-062`, 2026-09-28)

**Decision:** everything built or written for MISE is committed to `github.com/patokoller/mise`. The
repository is **public** — the operator's decision, "for now". Proposed alongside it: GitHub is the
**master copy**, and Project knowledge is a mirror refreshed at the end of each session. Every
session ends with a commit.

**Alternatives:** Project knowledge as the master with GitHub as a backup; a private repository.

**Reasoning:** on 2026-09-28 Project knowledge was found seven weeks behind the work — one session's
outputs, both Copenhagen frame files and one edit had never been uploaded, and nothing signalled the
gap. Two copies with no declared master drift without anyone noticing; a commit that didn't happen is
visible in a way a missed upload is not.

**What this does not do.** A commit date is set by the computer that makes it and can be anything.
Git history is a record of the *documents*; it is never evidence for `observed_at`, and it cannot
prove a prediction was written before the data.

**Carried with it, public-specific:** raw menu content and machine-extracted dish text stay out of
the repository (`10` §5). Guide-derived frame lists are in it; see BUILD-STATUS known issues.

**Reverses if:** (public) the specialist legal review `10` recommends before launch advises against
publishing guide-derived lists or collected data, or anything in the repo draws a publisher
complaint; (master) the operator finds editing through the Project easier and accepts GitHub as a
backup only — in which case the end-of-session sync still runs, in the other direction.

---

### D-062 · 2026-09-28 · The operator delegates build decisions to Claude · **Accepted** — operator instruction

**Decision:** on 2026-09-28 the operator wrote: "I need you to do all of that work for me and take the
decision for me for whatever it is needed. I give you that liberty." From that date Claude settles open
design decisions itself and logs each one here as *by Claude under `D-062`*, so every delegated decision
stays identifiable and can be reversed without archaeology.

**What is not delegated, and why.** Publishing: Claude has no access to Substack, and each issue goes
out under the operator's name, so the operator reads it and checks at least one claim against a real
menu before sending. Human transcription under `D-059`: by definition a person does it. Those two are
the project's only by-eye checks; delegating them would leave nothing checked by anyone who isn't the
system.

**The risk this creates, stated:** the project was designed around an operator who judges output
against reality (`15`, `16`). With decisions delegated, the checks that remain are the CHECK rows,
the validation guide, and the operator's pre-publication read. A wrong decision by Claude now surfaces
later than one the operator would have caught in the session.

**Reverses if:** the operator takes any decision back — per entry, or wholesale. Nothing in a
delegated decision is harder to undo than an operator one.

---

### D-063 · 2026-09-28 · Collected menu content is private; the repository is not · **Accepted** — by Claude under `D-062`

**Decision:** menus and dish lists collected from venues' own sites are **not** committed to the public
repository. They are handed to the operator as files, to keep in private storage of his choice (a Google Drive folder is the obvious one). Claude does not re-type them into Drive: copying 90 KB of menu text by hand is exactly the silent-corruption risk `D-059` exists for.
The repository holds everything else: docs, schema, frames, decisions, method, and venue-level fields that
are facts (URL, F2 state, published price, trading status, dates).

**Reasoning:** `10` §5 permits facts and short descriptions and forbids republishing a menu in full or
raw artefacts; a public repository is publication. Venue-level facts are what the newsletter itself
publishes, so they carry no new exposure.

**Reverses if:** the repository is made private, or the legal hour `10` recommends clears it.

---

### D-064 · 2026-09-28 · The Phase 1 predictions are written by Claude, and say so · **Accepted** — operator request

**Decision:** the five month-one predictions (`D-018`) are authored by Claude at the operator's request
("I think you are more clever on predicting on this than me") and are recorded with `author = Claude`.

**What this costs, stated plainly.** `D-018` designed them as the operator's intuition-only baseline for
Q20. A Claude-authored baseline measures Claude's priors against a system Claude also runs, so Q20 can no
longer answer "does the system beat the operator's gut". It can still answer "does the system beat a
reasoned prior made before the data". They are also **not data-free**: they were written after 8 menus were
read on 2026-08-12 and 73 menu rows on 2026-09-28, and each prediction records which of that it could have
been influenced by. `M1` was deleted on 2026-08-01 because it was Claude-originated and unendorsed; these
differ in being explicitly requested.

**Reverses if:** the operator writes his own. His go into the same ledger alongside these, and Q20
scores the two authors separately.

---

## Template for new entries

```
### D-NNN · YYYY-MM-DD · Title · **Accepted | Superseded by D-NNN | Reversed**

**Decision:** what was decided, specifically.

**Alternatives:** what else was considered.

**Reasoning:** why. Include the constraint that drove it.

**Reverses if:** the observable condition that should trigger a rethink.
```

---

## Change log (non-architectural)

Source additions, taxonomy versions, prompt changes, schema migrations. Anything that could later be mistaken for a real-world trend.

| Date | Type | Change | Effect on data |
|---|---|---|---|
| 2026-07-28 | init | Documentation set created | none |
| 2026-07-28 | doc | `20-twenty-questions.md` added — Phase 0 deliverable | none |
| 2026-07-28 | schema | `menu_items.name` split into `name_original` / `name_translated`; `description` likewise; trigram index moved to `name_original` | none — pre-deployment |
| 2026-07-28 | schema | `menus.language` added | none — pre-deployment |
| 2026-07-28 | schema | `predictions.basis` added (`intuition` / `data` / `mixed`) | none — pre-deployment |
| 2026-07-29 | doc | `21-venue-inclusion-criteria.md` added — Phase 0 deliverable | none — no data collected yet |
| 2026-07-29 | source | MICHELIN Guide registered as Route A1 for all three cities. Nordic Countries 2026 edition verified as published 1 June 2026; Spain and GB&I edition dates to be recorded at enumeration | defines the frame |
| 2026-07-29 | source | Route A2 registered: White Guide Denmark (Copenhagen), Guía Repsol **Soles only** (Barcelona), Harden's Top 100 UK London entries (London) | defines the frame; deliberately asymmetric across cities, so Q8 like-for-like comparisons run on the A1-only subset |
| 2026-07-29 | source | Guía Repsol renamed its second tier from *Recomendados* to *Restaurantes Guía Repsol* in the 2026 edition. That tier is **excluded** from Route A2 | none — but recorded because a source renaming a category is exactly what later gets mistaken for a real-world shift |
| 2026-07-29 | doc | Frame date frozen at 2026-07-28; cohort draw seed `20260728` declared **before** enumeration | the seed's validity depends entirely on this row predating the frame |
| 2026-07-29 | source | MICHELIN Guide Great Britain & Ireland 2026 verified: unveiled 9 February 2026, Convention Centre Dublin, 1,210 restaurants, 230 starred | London A1 vintage now recorded; Spain 2026 date still outstanding |
| 2026-07-29 | rule | `F0` entity-resolution step added — every candidate resolves to an address and `google_place_id` before any filter applies | prevents a wrong-venue merge, which `01` treats as invisible and unrecoverable |
| 2026-07-29 | rule | `ownership_scale` counts **operated** venues only; investment, licensing and partnership concepts recorded in notes | changes the tag for groups near the 10-venue boundary |
| 2026-07-29 | open | Route B publication registry still undefined for all three cities | **blocks enumeration** |
| 2026-07-29 | open | Whether to register the NRA Top 100 as a London A3 | would widen London's A2, currently the narrowest of the three |
| 2026-07-29 | source | Route B registry set — `06` §4A. Eater London removed (dead since Feb 2023); World's 50 Best and 50 Best Discovery removed as award lists, not press | **unblocks enumeration** |
| 2026-07-29 | open | Consider World's 50 Best as Route **A3** — global, one method, all three cities, would improve Q8 comparability where A2 is asymmetric | operator decision |
| 2026-07-29 | open | Barcelona needs a Catalan-language title and a trade title | class-mix asymmetry vs London |
| 2026-07-30 | source | MICHELIN `robots.txt` read and recorded: `ClaudeBot`, `GPTBot`, `ChatGPT-User`, `PetalBot` granted a group with no `Disallow` directives; sitemap advertised. Edge bot-detection refuses requests regardless — three URLs tested on `guide.michelin.com` | none yet. **A1 unretrievable from tested infrastructure; blocks enumeration in all three cities** |
| 2026-07-30 | doc | `06` §1 posture column split into **Posture** (permission) and **Reach** (technical), with `waf_blocked` defined as distinct from `prohibited` | none — corrects a registry that could not express *permitted but unreachable*, which had already produced one wrong conclusion |
| 2026-07-30 | source | White Guide Denmark corrected from **annual** to **continuous** — weekly reviews, no dated edition | **Copenhagen A2 is not reproducible as written.** `21` §4; blocks enumeration |
| 2026-07-30 | open | White Guide tier scope — all five classification levels, or a cut, tested against the Repsol precedent (`D-023` era reasoning) | would change Copenhagen's frame size and its comparability to the other two cities; lands on Q8 |
| 2026-07-30 | rule | `D-031` — frame membership is parsed deterministically; no LLM extraction into the frame | prevents silent frame corruption; adds parser maintenance to each quarterly refresh |
| 2026-07-30 | rule | `D-032` — listing scrapes assert row count against the source's stated total and halt on mismatch | converts silent partial retrieval into a loud failure |
| 2026-07-30 | correction | Claude asserted `06`'s MICHELIN posture was wrong without reading `robots.txt`; posture was correct. Logged in BUILD-STATUS Corrections alongside the 2026-07-28 instance of the same pattern | none — no data affected, but the error class is one the operator cannot catch by inspection |
| 2026-07-30 | rule | `D-033` — a rolling source's vintage is the stored snapshot, cited by `retrieved_at` | closes `21` §12.1 item 7; Copenhagen A2 becomes reproducible from this project's archive rather than the publisher's site |
| 2026-07-30 | rule | `D-034` — `NOINDEX` does not exclude a page from collection; `robots.txt` `Disallow` still does | Alouette's menu page and any like it stay in scope |
| 2026-07-30 | source | Firecrawl API (`api.firecrawl.dev`) blocked by the container egress proxy — `host_not_allowed`. Key present and valid-looking; unused | **blocks enumeration** until the domain is allowlisted |
| 2026-07-30 | verification | Operator checked Geranium, AOC and akmē by eye against live pages. Two classifications confirmed correct; akmē price resolved to 1500 DKK | first independent check of a Claude-produced classification in this project — 2 of 2 correct |
| 2026-07-30 | source | MICHELIN retrievable via Firecrawl, `proxy: basic`, HTTP 200. Method recorded in `06` §4 | **unblocks A1 in all three cities**; `21` §12.1 item 6 closed |
| 2026-07-30 | data | Copenhagen A1 enumerated: 83 candidates, tier counts 3/5/14/29/32 reconciled against the guide's stated figures | first live pass of `D-032`; first real data in the project |
| 2026-07-30 | data | 72 Danish rows resolved to address + `google_place_id`; 68 pass F1 (62 Københavns, 6 Frederiksberg); 15 fail boundary, 11 of them Malmö | frame boundary now rests on addresses, not the guide's city labels |
| 2026-07-30 | rule | `D-035` — Aotori recorded as one venue, alternative names kept as aliases | sets the F0 precedent for name disagreement at a shared address |
| 2026-07-30 | source | White Guide `robots.txt` returns 404 — posture `no_robots_txt`, permissive. Retrieval method recorded in `06` §4 | A2 unblocked |
| 2026-07-30 | data | White Guide Denmark enumerated: **199 unique venues**, 203 rendered rows. Tiers 28/67/81/21/3 unique | first A2 data; not yet filtered to Copenhagen |
| 2026-07-30 | rule | `D-036` — all five White Guide tiers kept; Recommended is 3 venues nationally | `21` §12.1 item 8 closed |
| 2026-07-30 | rule | `D-037` — tier-subtotal reconciliation as `D-032`'s fallback where no total is stated | makes A2 assertable; sets the pattern for any future source without a stated count |
| 2026-07-30 | open | Anarki (`9638`) is classified Very Fine **and** Masters simultaneously by White Guide | `route_a2_tier` undecidable; operator judgement required |
| 2026-07-30 | data | ~~White Guide A2 resolved: **110 of 199 pass F1** (101 Københavns, 9 Frederiksberg)~~ **CORRECTED 2026-08-01 — the figure was wrong.** White Guide A2 resolved: **109 of 199 pass F1** (101 Københavns, **8** Frederiksberg); 75 excluded on the guide's own locality; 15 F0 unresolved | A2 frame complete except the union with A1. 110 is arithmetically impossible: 110 + 75 + 15 = 200, one more venue than the file contains. 109 + 75 + 15 = 199 exactly |
| 2026-07-30 | rule | `D-038` — Anarki recorded at Masters; `D-039` — Propaganda 'next door' is one venue | closes both open F0/tier questions on A2 |
| 2026-07-30 | correction | Name-matcher failed to link `Kadeau København` (A2) to `Kadeau Copenhagen` (A1): Danish `ø` does not decompose under NFKD and was being deleted rather than folded to `o`. Fixed for `ø`, `æ`, `å` | would have produced a duplicate venue in the A1∪A2 union |
| 2026-08-01 | data | **A1 ∪ A2 union run on `google_place_id`. Copenhagen's Route A frame is 132** — of 282 candidate rows across both guides. Overlap 45; A1-only 23; A2-only 64. Kommune split 123 Københavns / 9 Frederiksberg | **first frame size in the project.** F1 only — F2, F4, F5 and Route B are not applied, so this number will fall and then rise |
| 2026-08-01 | verification | Operator confirmed Noma is absent from MICHELIN Nordic 2026 and enters the frame on White Guide alone. A1 enumeration verified — the `D-032` tier reconciliation was not masking a substitution | closes the highest-priority open check from the union session. Noma's F4 status still needs an explicit decision when F4 runs |
| 2026-08-01 | correction | Change-log entry of 2026-07-30 stated **110 of 199 pass F1 (101 Københavns, 9 Frederiksberg)**. Wrong — the figure is **109 (101 + 8)**. 110 + 75 + 15 = 200, one more venue than the file holds | none: the union was computed from row-level data, not from this figure. Had it been trusted, the published frame would have been 133 |
| 2026-08-01 | correction | `cph-route-a2-frame.xlsx` was shipped **without recalculation**. openpyxl writes formulas with no cached values, so all six counts displayed blank. The formulas were correct throughout | this is *why* the 110 error happened — with no number visible, the log entry was written from memory. Recalculation before sharing is now a step in the file's own legend |
| 2026-08-01 | correction | Prediction ledger status tally read Open 6 / Void 1 / Resolved 0 = **7 against 8 clauses**. `COUNTIF` matched `"Open"` exactly and missed H3-b (`"Open — long horizon"`); the mean-confidence line silently averaged 6 of 7 open clauses for the same reason | mean confidence corrects 0.608 → 0.600. **Third instance** of the pattern in BUILD-STATUS known issues: a formula that recalculates green and asserts the wrong thing |
| 2026-08-01 | rule | Every count block now carries a **CHECK row** whose formula must equal a stated denominator, and sub-breakdowns are conditioned on the same filter as their parent | converts a silent miscount into a visible one. Added to A2 and the ledger; owed on A1 and every file after |
| 2026-08-01 | rule | `D-040` — F0 is identity-only; trading moves to F4. **Google Places does not return permanently closed venues**, so `unresolved` is a mixture of ambiguity and unrecognised closure in all three cities | `unresolved` can no longer be reported as a measure of ambiguity. Every `unresolved` row needs a by-hand check before its cause is stated |
| 2026-08-01 | data | `D-041` — Kiin Kiin Tok Tok reclassified `unresolved` → `not_trading` (operator-confirmed closure at the guide's stated address); Toto stays `unresolved`. A2 unresolved 15 → 14 | **frame unchanged at 132** — the venue has no place_id and could not have joined a place_id-keyed union |
| 2026-08-01 | rule | `D-042` — prediction `M1` pre-registered on a new **Method predictions** sheet, before F4 runs. Claude-originated; operator confidence left blank pending endorsement | none until F4. Kept off the Hypotheses sheet so it cannot contaminate the operator's three pre-registered predictions or their counts |
| 2026-08-01 | artefact | `cph-route-a-frame-union.xlsx` written — 132 rows, one per venue, keyed on `google_place_id`, 8 CHECK rows | The frame exists as an artefact, not only as a number. Route B has something to deduplicate against |
| 2026-08-01 | artefact | CHECK rows added to `cph-route-a1-frame.xlsx` (4) and rebuilt in `cph-route-a2-frame.xlsx` (3) | Every count block in the project now carries a guard. The gap noted on 2026-08-01 is closed |
| 2026-08-01 | data | `D-044` — 14 `unresolved` A2 rows adjudicated: 12 `outside_boundary`, 2 `not_trading`. A2 now 109 / 87 / 3 / 0 | Frame unchanged at **132**; the "up to 14" caveat discharged |
| 2026-08-01 | rule | `D-043` — canonical name is the venue's own published name, resolved at F2. Column renamed `display_name_provisional` | No name may be published before the F2 pass |
| 2026-08-01 | schema | `D-047` — `entity_aliases` gains observation and validity dates; `canonical_name` becomes a pointer; two views added | Pre-deployment. `schema.sql` needs the patch applied before the database is first run |
| 2026-08-01 | correction | `D-045` — A1 rows 73–76 exclusion notes cited the guide's city label; corrected to the resolved address | Counts unaffected |
| 2026-08-01 | correction | Union file reported **9** name variants; an exact, case-sensitive comparison finds **14**. Five case-only differences had been recorded as "no variant" | Classification corrected and a CHECK row added that recomputes the difference count from the strings rather than trusting the classification |
| 2026-08-01 | correction | Claude stated the union file has nine CHECK rows; it has **eight**. The file's own legend repeated the error | Legend corrected. Fourth instance of a claim about a file made without counting — see Corrections |
| 2026-08-01 | decision | Prediction ledger: the three-hypotheses record and the ongoing running ledger are **two distinct things**, operator-confirmed | The `⚠️` query in BUILD-STATUS is closed; both rows stay |
| 2026-08-02 | rule | `D-048` — Route B titles gain an **access status** (`permitted` / `blocked_by_robots` / `pending_access`). An unreachable registered title is carried with its date, not dropped | Route B coverage is reported as reachable-over-registered, both numbers stated |
| 2026-08-02 | rule | `D-049` — absence from a `robots.txt` AI blocklist is not permission. Politiken → `pending_access`; no content fetched | Copenhagen loses a general-news title pending licence or permission. Politiken also disallows `/search` for all agents |
| 2026-08-04 | rule | `D-050` — the wire rule covers **any** agency copy, registered or not; explicitly Ritzau | Extraction must capture agency attribution as a field. Without it the two-items-two-titles rule is unenforceable |
| 2026-08-02 | rule | `D-051` — archive reach is demonstrated per title before a sweep is planned; index, sitemap and search tested separately | Adds a verification step to all 15 titles across 3 cities. `06` §4A criterion 2 amended |
| 2026-08-02 | rule | `D-052` — cheaper access is not grounds to reopen the frozen registry | The "worth one more Danish title" line in `06` §4A is not an invitation |
| 2026-08-02 | finding | Copenhagen Route B posture established for **5 of 5** titles: 3 `permitted`, 1 `blocked_by_robots`, 1 `pending_access`. Archive reach verified for **0 of 5** | No Route B candidate exists. **Frame unchanged at 132** |
| 2026-08-02 | correction | `06` §4A described AOK as "the Copenhagen dining and culture arm." `aok.dk` → `berlingske.dk/aok` → HTTP 404; AOK is Berlingske's culture brand, not a publication | Registry note corrected. Berlingske/AOK is **one** title — counting it as two would breach the two-items-two-titles rule silently |
| 2026-08-10 | finding | Berlingske `/search?query=` is real, dated, and states a result count (4,289 for `restaurant`) — but **`?page=N` is silently ignored**, returning HTTP 200 and the identical first page | Any paginator must assert that page N+1's first date is older than page N's last, and halt if not. A `page=N` paginator would have inserted 10 articles as 4,289 with every CHECK row passing |
| 2026-08-10 | finding | The same Berlingske search URL returned two different result sets within one session. Cause unknown | Berlingske search cannot carry a frame until reproducibility is understood. Strengthens the case for a licensed archive |
| 2026-08-02 | finding | Infomedia is now **Retriever** — merged, platform migrated 14 April 2026. DK coverage from the 1980s (Politiken and Berlingske from 1990); DKK 32/article on a DKK 495/month base ex. VAT; per-outlet agreements govern access; a **Kildeinfo** source list states coverage and depth per title | The Kildeinfo list would be Route B's first real completeness anchor. Demo needed before any purchase decision |
| 2026-08-10 | rule | `D-053` — publication dates come from the article page, never from a sitemap `lastmod` | prevents Route B items being dated by a bulk site re-save; adds one fetch per item, already required by `21` §4 |
| 2026-08-10 | rule | `D-054` — reach is credited only on dated items retrieved, never on a working paginator or a stated count | would otherwise have marked all three tested titles reachable |
| 2026-08-10 | rule | `D-055` — Route B coverage reported as reachable-over-registered; a city needs 2+ reachable titles before Route B runs | Copenhagen currently 1 of 5. **Route B Copenhagen is blocked by this** |
| 2026-08-10 | source | Scandinavian Standard reach **demonstrated** by sitemap — 1,696 posts, 2014–2026, encloses the window. Section index fails; search closed by robots | first Route B title in the project with demonstrated reach |
| 2026-08-10 | source | MigogKbh sitemap index real (113 children) but newest entry 2026-05-19 as of 2026-08-10 — misses ~10 weeks of the window. Cause not investigated | reach **not** demonstrated; section index and search still untested |
| 2026-08-10 | open | Scandinavian Standard: 133 of 1,696 slugs over 90 chars, zero in the historic 1,000; items of that shape cross-published on four other domains | precision concern for any per-title item count. **Not** a registry question (`D-052`) |
| 2026-08-10 | doc | `D-056` — Phase 1 target confirmed at **40 venues**, declared method-development rather than cohort. `11-roadmap.md` Phase 0 "list 60 candidate venues" superseded; Phase 1 line annotated | none — no data collected yet. Removes a doc that described a selection method `D-023` had already replaced |
| 2026-09-28 | doc | Repository created and August recovery committed. `D-056` addendum and `D-057`–`D-060` (written 2026-08-12, never uploaded) restored; D-047 wording from 2026-08-01 restored; `D-061` logged | none on data. `schema.sql` was already correct; only the docs describing it were stale |
| 2026-09-28 | doc | `D-057`, `D-059`, `D-060` accepted under `D-062`; `D-062`–`D-064` logged; `07` §2 and `menu_item.schema.json` v1.1.0 (extractor never writes `name_original`; `menu_date_stated` is free text); `16` gains Phase 1 checks; `21` §12.1 items 9–11 | Phase 1 dish rows carry `name_original` empty until transcribed. No existing data changed |
