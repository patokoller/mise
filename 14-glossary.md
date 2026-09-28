# 14 — Glossary

**Status:** Draft v1
**Last reviewed:** 2026-07-28

Terms used precisely throughout this documentation. Where a word has a loose everyday meaning and a strict meaning here, the strict one governs.

---

**Artifact** — a raw captured document: HTML, PDF, or image, stored unchanged in object storage. Kept forever, so extraction can be re-run when methods improve.

**Baseline** — the trailing average against which a measurement is compared to determine whether it's unusual. Without one, there is no trend detection, only description.

**Candidate** — an entity name the resolver couldn't confidently match, awaiting human adjudication in `entity_candidates`.

**Cohort** — a set of venues added to tracking at the same time. Cohorts must be tracked separately because adding venues creates apparent trends that are artifacts of your own behaviour.

**Coverage** — the proportion of a city's defined segment actually tracked. Published alongside every count. Distinct from *observation*.

**Denominator** — the "out of how many." Every published count states one. Its absence is the most common way trend reporting misleads.

**Entity** — a canonical real-world thing: a venue, person, group, supplier, or location. Has a stable `entity_id` that never changes, however many names it accumulates.

**Entity resolution** — collapsing every observed name form to one canonical entity. The hardest problem in the project and the one that quietly ruins counts when neglected.

**Fact** — an atomic, dated, sourced statement. "Noma seats 40, observed 2026-03-14, source X." Not a document, not an article, not an opinion.

**Facet** — a dimension of the taxonomy: ingredient, technique, format, service model, cuisine, beverage, design, sustainability.

**Gold set** — 30 hand-extracted documents, completely correct, used only to measure pipeline accuracy. Never used to develop prompts, or it stops measuring anything.

**Observed** — a venue whose data was actually captured in a given period. An unobserved venue is *absent*, never zero. Confusing the two manufactures declines.

**`observed_at`** — when a fact was true in the world.

**Penetration** — the share of observed venues in a city featuring a given term. The primary trend metric; robust to menu length.

**Prediction ledger** — the public record of dated, falsifiable calls with resolution criteria fixed in advance, scored including failures. The most defensible asset in the project.

**Provenance** — the chain from a published claim back to the source URL, retrieval date, model, and prompt version that produced it.

**Quarantine** — the state of an extraction that failed validation. Retained for debugging; never partially inserted into fact tables.

**`retrieved_at`** — when we captured a fact. Frequently much later than `observed_at`, and conflating the two silently corrupts every time series.

**Signal** — a computed measurement that has cleared the sample, magnitude, persistence, and z-score thresholds in `08-trend-detection.md` §3. Below those thresholds it is noise, whatever it looks like.

**Taxonomy** — the controlled vocabulary. What makes trends countable. Extractors select from it; they may not invent terms.

**Unmapped** — an extracted value that didn't match the taxonomy. Queued for weekly review and possible promotion. Returning unmapped is correct behaviour, not failure.

**`valid_from` / `valid_to`** — the window during which a fact is believed to have held. `valid_to = NULL` means still current.

**Weak signal** — a pattern below the publication threshold, present in multiple cities, rising independently, and *not yet discussed in trade press*. The last condition is what makes it weak rather than merely small — and what makes it worth publishing.
