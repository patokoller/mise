# 04 — Agent Workflows

**Status:** Draft v1
**Last reviewed:** 2026-07-28

---

## 1. Principles

**Agents don't talk to each other.** They read from Postgres and write to Postgres. The database is the message bus. Agent-to-agent conversation is where these systems become unreliable, expensive, and impossible to debug — you cannot inspect a conversation that happened three weeks ago, but you can always inspect a table.

**Each agent is stateless.** Everything needed is in the input. This makes them independently testable, retryable, and cheap to reason about.

**Start with three.** The originating plan proposed five, then dozens. Three is enough to publish. Split an agent only when a specific bottleneck is observed, not in anticipation.

**Every agent run is logged** with model ID, prompt version, token counts, cost, and status. Without this you cannot tell whether quality changed because of your prompt or the model.

---

## 2. Roster

### Phase 1–3: three agents

| Agent | Model | Cadence | Job |
|---|---|---|---|
| **Scout** | Sonnet 5 | Daily | Find new documents worth extracting |
| **Extractor** | Sonnet 5 | Daily (batch) | Turn documents into structured facts |
| **Editor** | Opus 5 | Weekly | Interpret the numbers, draft, self-challenge |

Resolution and tagging in this phase are deterministic code plus a Sonnet call, not "agents." Don't dignify a function with a job title.

### Phase 4+: add as bottlenecks appear

| Agent | Model | Added when |
|---|---|---|
| **Curator** | Sonnet 5 | Entity/taxonomy queues exceed the weekly time budget |
| **Analyst** | Opus 5 | Trend interpretation needs separating from writing |
| **Menu Specialist** | Sonnet 5 | Menu extraction becomes materially more complex than other extraction |
| **Finance Agent** | Opus 5 | Unit-economics reading becomes systematic (see `00-project-brief.md` §5) |
| **Weak Signal Agent** | Opus 5 | Only once ≥12 months of history exists. Before that it has nothing to detect |

**The Weak Signal Agent is the most attractive and the most premature.** Cross-city pattern detection requires a baseline it will not have until year two. Building it early produces confident nonsense.

---

## 3. Scout

**Runs:** daily, 06:00.
**Model:** Claude Sonnet 5.
**Reads:** `sources` (active), `documents` (recent hashes).
**Writes:** `documents`, work queue for Extractor.

**Job:** decide what is new and worth extracting. Not to analyse — to triage.

**Procedure:**
1. Pull scheduled sources from n8n.
2. Fetch via Firecrawl / API.
3. Hash and compare. Unchanged → record re-observation, stop.
4. For changed or new documents, classify: relevance (in scope? one of our cities? our segment?), document type (menu / news / interview / report / listing), and which entities are mentioned.
5. Queue relevant documents for extraction. Store irrelevant ones anyway — storage is cheap and relevance judgments change.

**Prompt shape:**
> You are triaging documents for a hospitality intelligence system covering Copenhagen, Barcelona, and London. Independent and small-group restaurants at the ambitious end; not chains or QSR. For this document return: `in_scope` (bool), `city`, `doc_type`, `entities_mentioned` (array of names as written), `priority` (high/medium/low), `reason` (one sentence). If uncertain about scope, return `in_scope: true` — a false positive costs one extraction; a false negative loses a fact permanently.

**Failure modes:**
- *Over-inclusion* → extraction cost rises. Tolerable. Tighten later.
- *Under-inclusion* → permanent data loss, invisible. Bias hard toward inclusion.
- *Hallucinated entities* → caught downstream at resolution.

---

## 4. Extractor

**Runs:** daily, batched, after Scout.
**Model:** Claude Sonnet 5, Batch API, prompt caching on.
**Reads:** queued documents + raw artifacts.
**Writes:** `extractions`, and on validation, facts.

**Job:** convert one document into schema-conforming JSON. Nothing else.

**Rules, in priority order:**
1. **Extract only what is present.** Never infer. A missing seat count is `null`, not an estimate. This is the single most important instruction in the whole system, and it must be restated in every extraction prompt.
2. **Per-field confidence.** A clearly printed price is 1.0. A price read from a blurry photo corner is 0.5.
3. **Preserve original language.** Store the dish name as written. Translation is a separate, additional field — never a replacement. `bacallà a la llauna` is not `cod`.
4. **Dates from the document.** If the document states a date, use it. Otherwise `null` and let the pipeline fall back to `retrieved_at` with `date_precision` set accordingly. The model must never invent a date.
5. **No commentary.** JSON only.

**Prompt shape (menu extraction):**
> Extract structured data from this restaurant menu. Return only JSON matching the provided schema. Rules: extract only what is visibly present; use null for anything absent; never infer, estimate, or complete partial information; preserve dish names in the original language exactly as written; include a confidence score 0–1 per field; if the document is not a menu, return `{"is_menu": false}`.

**Document types and handling:**

| Type | Handling |
|---|---|
| Digital PDF | Sonnet reads directly. No OCR. |
| Clean photo of a menu | Sonnet vision reads directly. |
| Scanned / low-quality PDF | Attempt Sonnet first. On failure, Tesseract → text → Sonnet. |
| HTML menu page | Firecrawl → markdown → Sonnet. |
| News article | Event extraction schema, not menu schema. |
| Interview | Chunk, embed, extract entities and relationships. |

**Failure modes:**
- *Schema violation* → quarantine, alert in weekly digest. Never partial-insert.
- *Silent quality drift* → the dangerous one. Caught only by the monthly gold-set eval (§7).
- *Hallucinated completeness* → the model fills a nine-course tasting menu when six courses were legible. Mitigated by the explicit no-inference rule and spot-checking.

---

## 5. Editor

**Runs:** weekly, after the statistics job.
**Model:** Claude Opus 5.
**Reads:** `signals`, recent `events`, prior issues, open `predictions`.
**Writes:** newsletter draft, candidate predictions, a list of things to look into.

**Critical constraint:** the Editor receives *computed numbers*, never raw tables to count. Its input is a prepared statistics brief. It may not produce a figure that wasn't given to it.

**Three-pass structure, in one session:**

**Pass 1 — Interpretation.** Given this week's signals, what might be happening? Produce 5–8 candidate observations, each stating: what changed, the magnitude, the denominator, the timeframe, and the most plausible mundane explanation.

**Pass 2 — Challenge.** Adversarial, explicitly instructed:
> For each candidate observation, argue against it. Consider: is the sample too small? Is the denominator changing rather than the numerator? Is this seasonal? Is this an artifact of which venues we happened to add recently? Is this coverage bias — did we start tracking a source that skews this way? Would this look like a trend if we shuffled the dates? Kill anything that cannot survive.

Pass 2 is the highest-value step in the entire system. Without it you publish coverage artifacts as trends, which is exactly what existing trend reports do and precisely what would make this project worthless.

**Pass 3 — Draft.** Write the surviving observations into the issue. Every claim carries its number, denominator, and timeframe. Every trend claim links to the underlying signal. Prediction candidates are proposed but not auto-published — the human writes the falsifiable statement and its resolution criteria.

**Failure modes:**
- *Narrative gravity* → the model prefers a good story to a true one. Pass 2 is the counterweight.
- *Number invention* → structurally prevented: it never sees raw data to count.
- *Repetition across weeks* → give it the last four issues and instruct it to avoid restating.

---

## 6. Orchestration

n8n, five workflows:

| Workflow | Schedule | Steps |
|---|---|---|
| `daily_scout` | 06:00 daily | Select sources → fetch → hash → triage → queue |
| `daily_extract` | 08:00 daily | Batch submit → poll → validate → resolve → tag → persist |
| `weekly_stats` | Mon 06:00 | SQL statistics job → `signals` |
| `weekly_editor` | Mon 08:00 | Build brief → Opus three-pass → draft to inbox |
| `health_check` | 07:00 daily | Heartbeat, null rates, queue depths, cost. Alert on anomaly |

**`health_check` is not optional.** The characteristic failure of an unattended side project is a job that stopped quietly in week 6, discovered in week 14, leaving an unfillable hole in the time series.

---

## 7. Evaluation

Without this, quality degrades invisibly. Prompts drift, models update, sites change, and confidence scores stay reassuringly high while accuracy falls.

**The gold set.** 30 documents, hand-extracted by you, completely correct. Diverse: a clean HTML menu, a messy PDF, a phone photo, a Catalan menu, a Danish menu, a tasting menu, a news article, an interview. Version-controlled in GitHub, never used in prompt development.

**Monthly:** run the current pipeline over the gold set. Measure per-field precision and recall. Log to a tracking file. If accuracy drops more than 5 points, stop and investigate before collecting more data.

**Every prompt change:** run the gold set before and after. No prompt goes to production on vibes. Record the result in `12-decision-log.md`.

**Quarterly:** re-hand-extract 5 random recent documents and compare with what the pipeline produced. This catches drift in document types the gold set doesn't cover.

**Metrics worth tracking:**
- Field-level extraction accuracy, per document type
- Entity resolution precision (bad merges are the expensive error) and recall
- Tagging accuracy against the controlled vocabulary
- Null rate per source over time — a rising null rate means a site changed
- Cost per document, per agent

---

## 8. Agent development order

1. **Extractor first.** It's the whole pipeline in miniature and where all the hard problems live. Get one menu type, one city, one document format working end to end.
2. **Then Scout.** Automating discovery is pointless before extraction works.
3. **Then the statistics job.** Plain SQL, no agent.
4. **Then Editor.** Only once there's enough data for signals to be real.
5. **Everything else** only when a queue overflows or a specific task demonstrably underperforms.
