# 01 — Data Architecture

**Status:** Draft v1
**Last reviewed:** 2026-07-28
**Executable DDL:** `schemas/schema.sql`

---

## 1. Principles

**Store facts, not documents.** An article about a restaurant is not data. "Noma seats 40, observed 2026-03-14, source X" is data. Documents are kept as raw artifacts for reprocessing, but the queryable layer is atomic, typed facts.

**Every fact is dated twice.** `observed_at` (when the fact was true in the world) and `retrieved_at` (when we saw it). These differ constantly — a menu page updated in January and read in March is an observation about January. Conflating them silently corrupts every time series.

**Facts are never updated in place.** A price change is a new row, not an edit. The old row gets `valid_to` set. This is what makes "how did tasting menu prices move in London over 18 months" answerable. Destructive updates are the single easiest way to permanently destroy this project's value.

**Every fact points at a source.** No exceptions, including your own observations — those cite you, with a date and a photo.

**Confidence is recorded, not assumed.** Extraction is probabilistic. A field carries how it was derived and how much to trust it.

**One database until it genuinely breaks.** Postgres with `pgvector`. See §7.

---

## 2. The temporal model

This is the part that most projects get wrong and cannot recover from.

Three time concepts, kept separate:

| Field | Meaning | Example |
|---|---|---|
| `observed_at` | When the fact was true / when the observation applies | Menu dated 2026-03-01 |
| `retrieved_at` | When we captured it | Crawled 2026-03-14 |
| `valid_from` / `valid_to` | The window during which we believe this fact held | 2026-03-01 → 2026-06-20 (superseded) |

`valid_to = NULL` means "still believed current."

**Rules:**
- When a new observation contradicts an existing current fact, close the old row (`valid_to` = new fact's `observed_at`) and insert the new one. Never overwrite.
- If `observed_at` is unknown, fall back to `retrieved_at` and set `date_precision` to record that. Never silently invent precision.
- `date_precision` ∈ `exact | month | quarter | year | inferred`. Trend queries filter on this; a chart built from `inferred` dates is not evidence.

**Why this is non-negotiable:** you cannot backfill history you didn't record. If the first 5,000 rows lack proper temporal fields, the first eighteen months produce a directory rather than a time series, and the entire thesis in `00-project-brief.md` fails.

---

## 3. Entity resolution

The hardest problem in the project. Not the agents — this.

**The problem:** "Noma", "noma", "Noma 2.0", "NOMA Copenhagen", "Restaurant Noma" must collapse to one venue. Chefs appear under transliterations, married names, nicknames, and misspellings. Groups get confused with their individual venues. If this isn't enforced, every count is wrong and every trend is an artifact of duplicate rows.

**The design:**

- `entities` — the canonical record. One row per real-world thing. Has a stable `entity_id` that never changes.
- `entity_aliases` — every observed string form, mapped to a canonical entity, with the source that produced it.
- `entity_candidates` — a review queue. Anything the resolver isn't confident about lands here for human adjudication.

**Resolution procedure, in order:**

1. **Exact match** on normalised alias (lowercased, accents folded, legal suffixes and leading articles stripped).
2. **Strong identifier match** — Google Place ID, official website domain, company registration number. These are the reliable ones; prefer them over name matching wherever available.
3. **Fuzzy match** — trigram similarity (`pg_trgm`) on name, constrained to the same city, above a threshold (start at 0.85 and tune).
4. **Embedding match** — cosine similarity on an embedded "name + city + cuisine" string, for cases 1–3 miss.
5. **Otherwise** → `entity_candidates` for human review.

**Never auto-merge below the threshold.** A wrong merge is much harder to detect and undo than a duplicate. Duplicates are visible; bad merges are invisible and silently corrupt counts.

**Human review budget:** ~20 minutes weekly. If the queue is consistently longer than that, the thresholds are wrong.

**Non-obvious cases to handle explicitly:**
- Venue closes and reopens with the same name, different ownership → *new entity*, linked via `succeeded_by`.
- Venue relocates → *same entity*, new address fact with dates.
- Venue is renamed → *same entity*, name change recorded as a fact, old name kept as alias.
- Pop-up becomes permanent → same entity, `venue_type` changes over time.

These distinctions are not pedantry. "How many venues that opened in 2026 survived to 2028" gives a different answer depending on whether they're handled correctly.

---

## 4. Core tables

Full DDL in `schemas/schema.sql`. Conceptually:

**Entity layer**
- `entities` — canonical registry, all types (venue, person, group, supplier, location)
- `entity_aliases`
- `entity_candidates`
- `relationships` — typed, dated edges between entities (`chef_at`, `owned_by`, `invested_in`, `supplies`, `succeeded_by`, `spun_off_from`)

**Venue layer**
- `venues` — venue-specific attributes, FK to `entities`
- `venue_facts` — the temporal attribute store: seats, price band, service style, opening hours pattern, capacity. One row per attribute-observation.

**Menu layer**
- `menus` — a menu as captured at a point in time, FK to venue, links to raw artifact
- `menu_items` — individual dishes with price, section, description
- `menu_item_tags` — the join to the taxonomy; this is what makes trends countable

**Event layer**
- `events` — dated occurrences: openings, closings, chef moves, awards, funding rounds, expansions, refurbishments. The backbone of narrative and of survival analysis.

**Source layer**
- `sources` — registry of every source, with access method and ToS posture
- `documents` — raw artifacts (HTML, PDF, image) with hash, storage path, retrieval metadata
- `extractions` — the link between a document, a model run, and the facts produced

**Analysis layer**
- `taxonomy_terms` — the controlled vocabulary
- `taxonomy_unmapped` — extraction output that didn't map; the weekly review queue and the growth path for the vocabulary
- `signals` — computed trend measurements with their statistics
- `predictions` — the public prediction ledger, with resolution
- `embeddings` — pgvector store for semantic search over text

---

## 5. Provenance and confidence

Every fact row carries:

```
source_id        -> which source
document_id      -> which specific artifact
extraction_id    -> which model run produced it (NULL for human entry)
method           -> 'api' | 'scrape' | 'llm_extraction' | 'ocr_llm' | 'human' | 'inferred'
confidence       -> 0.0–1.0
verified_by      -> 'none' | 'human' | 'second_source'
```

**Rules:**
- Anything published must be traceable to a source URL and a retrieval date.
- Facts with `confidence < 0.7` and `verified_by = 'none'` are excluded from published counts. They stay in the database — they're useful as weak evidence and for later reprocessing — but they don't appear in charts.
- A fact confirmed by two independent sources gets `verified_by = 'second_source'` and is preferred in conflicts.
- Human observations get `confidence = 1.0` for what was directly seen (a photographed menu) and lower for interpretation ("seemed busy").

---

## 6. Raw artifact retention

**Keep everything, forever.** Object storage is cheap; re-crawling is not always possible, and pages disappear.

- Store the raw HTML/PDF/image alongside the extracted facts.
- Content-hash it. If the hash is unchanged, skip re-extraction — this is the single biggest cost saver in the pipeline.
- Store the extraction prompt version and model ID with every extraction.

**Why this matters more than it looks:** in twelve months you will have a better taxonomy and better prompts. Being able to re-run extraction across every artifact ever captured — with dates preserved — means your *past* data improves as your method improves. That compounding is unavailable to anyone who only kept the parsed output.

---

## 7. Why one database

The originating plan called for Postgres + Neo4j + a vector database. At this scale that's three schemas to maintain, three backups, and two sync paths to break, in exchange for capabilities that aren't needed yet.

**Postgres handles all three roles:**
- Relational — natively, obviously.
- Vector — `pgvector` for embedding search over interviews, reviews, and descriptions. Adequate well past a million embeddings.
- Graph — a `relationships` table with recursive CTEs. Multi-hop traversal in SQL is uglier than Cypher, but at the scale of thousands of entities and tens of thousands of edges, it's fine and it's fast.

**Add Neo4j when** a genuinely graph-shaped question becomes central and slow — multi-hop influence propagation, community detection across supplier networks. Realistically year two, if ever.

**Add a dedicated vector DB when** embedding count exceeds a few million or hybrid search latency becomes a product problem. Realistically never for this project.

Recorded as decisions `D-002` and `D-003` in `12-decision-log.md`.

---

## 8. Query patterns to design for

The schema exists to answer these. If a design change makes one of these harder, it's the wrong change.

1. *"Which ingredients appeared on more London menus in Q2 2026 than Q4 2025?"* — tag counts over time, per city.
2. *"When did fermentation first appear on a Barcelona menu, and how did it spread?"* — first-appearance dates and diffusion.
3. *"What happened to venues that opened in Copenhagen in 2026?"* — survival analysis over events.
4. *"Where has this chef worked, and who did they work under?"* — relationship traversal.
5. *"How have tasting menu prices moved, adjusted for city?"* — temporal price series.
6. *"Which cities lead and which follow on a given tag?"* — lead/lag correlation.
7. *"Find interviews where chefs discuss simplicity"* — semantic search, no exact keyword.
8. *"Which formats have expanded internationally, and at what success rate?"* — the year-three question; entity relationships plus events plus survival.

---

## 9. What will break first, and the fix

| Failure | Symptom | Fix |
|---|---|---|
| Entity duplication | Counts inflate; the same venue appears twice in a chart | Weekly candidate review; tighten normalisation |
| Taxonomy drift | 400 spellings of "fermented" | `taxonomy_unmapped` review; controlled vocabulary discipline |
| Silent extraction degradation | Confidence stays high, accuracy falls | Monthly gold-set evaluation (`04-agent-workflows.md` §7) |
| Source rot | Sites change structure; extraction returns nulls | Null-rate alerting per source |
| Temporal contamination | Trend charts driven by when you crawled, not when things happened | `date_precision` filtering; never plot `inferred` dates |
| Collection gaps | Holes make surrounding data uninterpretable | Cadence discipline (`13-operating-cadence.md`) |
