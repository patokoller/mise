# 03 — Data Flow

**Status:** Draft v1
**Last reviewed:** 2026-07-28

---

## 1. The nine stages

Every fact in the system takes this path. Each stage has an explicit contract: what it accepts, what it emits, and what it does when it fails.

```
1. SCHEDULE  → 2. FETCH  → 3. DEDUPE  → 4. EXTRACT  → 5. VALIDATE
                                                            │
6. RESOLVE  → 7. TAG  → 8. PERSIST  →  9. MEASURE  ─────────┘
                                            │
                                       INTERPRET → CHALLENGE → PUBLISH
```

---

## 2. Stage contracts

### Stage 1 — Schedule
**Trigger:** n8n cron.
**Reads:** `sources` where `active = true` and the crawl interval has elapsed.
**Emits:** a work queue of source + URL pairs.

Frequencies: venue menus monthly (they don't change weekly, and pretending otherwise wastes money); trade press and news daily; guides and awards on announcement; registries quarterly.

Stagger the schedule. Do not crawl 250 venues in one burst — spread across the week, both to be a polite client and to avoid a single failure taking out a whole cycle.

### Stage 2 — Fetch
**Accepts:** source + URL.
**Emits:** raw artifact → object storage; a `documents` row.
**Rules:** respect `robots.txt`; identify with a real user agent and contact address; rate-limit to roughly one request per source per few seconds; never fetch a source whose `tos` is `prohibited` or `manual_only`.
**On failure:** retry ×3 with backoff, then mark the source degraded and move on. Never block the queue.

### Stage 3 — Dedupe
**Accepts:** raw artifact.
**Logic:** hash the content. If `(source_id, content_hash)` already exists → stop. Record that the document was re-observed unchanged (this is itself information: it tells you the menu is stable) and skip extraction.
**Why it's a separate stage:** this is the single biggest cost saver in the pipeline and it must be impossible to accidentally bypass.

### Stage 4 — Extract
**Accepts:** new artifact + document metadata.
**Model:** Claude Sonnet 5, structured output, schema enforced.
**Emits:** JSON conforming to `07-extraction-schemas.md`.
**Rules:**
- Extract only what is present. The prompt must explicitly forbid inference — a model asked to fill a schema will happily invent a plausible seat count.
- Every field gets a per-field confidence.
- Unknown → `null`, never a guess.
- Record `model_id` and `prompt_version` on the extraction row.
- Batch API unless interactive.

### Stage 5 — Validate
**Accepts:** raw model output.
**Logic:** JSON Schema validation, then sanity rules — prices within plausible bounds for the city, dates not in the future, item counts not absurd, currency matching the city unless flagged.
**On failure:** quarantine. `extractions.status = 'schema_fail'`, raw output retained, nothing inserted into fact tables.
**Rule:** a validation failure never partially inserts. All or nothing.

### Stage 6 — Resolve
**Accepts:** validated extraction containing entity names.
**Logic:** the resolution ladder in `01-data-architecture.md` §3 — exact, identifier, trigram, embedding, else queue.
**Emits:** facts linked to canonical `entity_id`, or rows in `entity_candidates`.
**Rule:** never auto-merge below threshold. A duplicate is visible and fixable; a bad merge is invisible and corrupts counts silently.

### Stage 7 — Tag
**Accepts:** menu items and text facts.
**Model:** Sonnet 5 initially; Haiku 4.5 once the taxonomy stabilises.
**Logic:** map to controlled vocabulary from `05-taxonomy-v1.md`. The full active taxonomy goes in the prompt (cached).
**Emits:** `menu_item_tags` rows; anything unmapped → `taxonomy_unmapped`.
**Rule:** the model may not invent terms. It selects from the list or returns unmapped. This constraint is what keeps trends countable.

### Stage 8 — Persist
**Accepts:** resolved, tagged, validated facts.
**Logic:** append-only. If this fact contradicts a current fact for the same entity and attribute, close the old row (`valid_to` = new `observed_at`) and insert the new one.
**Rule:** no destructive updates, ever. Corrections are new rows with higher confidence, not edits.

### Stage 9 — Measure
**Trigger:** weekly, after ingestion completes.
**Logic:** pure SQL. No LLM. Computes penetration, share, medians, first appearances, z-scores against trailing baseline. Writes to `signals`.
**Rule:** this is the only stage permitted to produce a number that will be published.

### Interpret → Challenge → Publish
Covered in `04-agent-workflows.md` §4–6 and `09-editorial-and-predictions.md`.

---

## 3. The human-in-the-loop points

Four, and only four. Everything else runs unattended.

| Queue | Cadence | Time | Consequence of neglect |
|---|---|---|---|
| `entity_candidates` | Weekly | ~15 min | Counts drift; duplicates accumulate |
| `taxonomy_unmapped` | Weekly | ~10 min | Vocabulary stops growing; new trends invisible |
| Quarantined extractions | Weekly | ~5 min | Silent data loss from a broken source |
| Trend candidates | Weekly | ~30 min | No publication |

**Total: about an hour a week.** If any queue consistently exceeds its budget, the thresholds upstream are miscalibrated — fix the threshold, don't work harder.

---

## 4. The human observation path

This is the proprietary layer and it deserves a real pipeline, not a notes app.

```
You visit a restaurant
        │
Photograph the menu, the room, the plate
Note: covers, service style, what surprised you
        │
Upload to a single inbox folder in object storage
        │
Sonnet 5 reads the images directly (no OCR needed for a decent phone photo)
        │
Extracted to the same schemas as any other source
        │
source_type = 'human', confidence = 1.0 for observed facts,
lower for interpretation
        │
Same resolution, tagging, and persistence path
```

**Design rule:** capture must take under two minutes at the table, or it won't happen. Photograph now, process later. Never make the field step depend on typing.

**What to capture every time, without exception:** the full menu, the date, the city, the venue name. Everything else is optional. The four mandatory fields are what make the observation usable; a beautiful photo with no date is decoration.

---

## 5. Data quality gates

A fact must pass all of these to appear in a published claim:

1. `confidence >= 0.70`
2. `date_precision <> 'inferred'`
3. Resolved to a canonical entity (not a candidate)
4. Source URL present and retrievable
5. For counts: denominator known — you must be able to state *out of how many venues*

Gate 5 is the one most often skipped and most damaging. "Twelve venues now serve X" is meaningless without "out of the forty we track in that city." Every published count states its denominator or it doesn't get published.

---

## 6. Reprocessing

Because raw artifacts are kept forever and every extraction records its prompt version, the pipeline can be re-run over history when the method improves.

**When to reprocess:**
- Taxonomy gains a significant new facet → re-tag everything
- Extraction prompt materially improves → re-extract a sample, compare against the gold set, and if better, re-run the corpus
- A bug is found in a parser → re-extract affected sources

**Rules:**
- Reprocessing creates *new* extraction rows and *new* fact rows. It never rewrites history. The old facts get `valid_to` set with a note.
- `observed_at` always comes from the original document, never from the reprocessing date. Getting this wrong silently shifts your entire time series to the present.

This is why the artifact archive matters: your past data improves as your method improves. That compounding isn't available to anyone who only kept the parsed output.
