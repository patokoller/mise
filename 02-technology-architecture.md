# 02 — Technology Architecture

**Status:** Draft v1
**Last reviewed:** 2026-07-28

---

## 1. Selection principles

- **Managed over self-hosted.** Operator time is the binding constraint, not money. Never run a database you could rent.
- **Boring over clever.** Every component must be debuggable at 11pm after three weeks away from the project.
- **One of each thing.** One database, one orchestrator, one language, one LLM provider.
- **Reversible over optimal.** Prefer choices that are cheap to undo. Standard Postgres, plain Python, portable object storage.
- **Nothing added without a demonstrated need.** Every component is a maintenance obligation forever.
- **Visible over powerful.** The operator is a product manager, not an engineer (`D-011`). n8n workflows over Python scripts, SQL views over application logic, managed dashboards over coded ones. A tool that can be inspected and reasoned about beats one that is marginally more capable and completely opaque.

---

## 2. The stack

| Layer | Choice | Why | Cost |
|---|---|---|---|
| Database | **Postgres 16** (Supabase or Neon) + `pgvector`, `pg_trgm` | Relational, vector, and graph-enough in one place. Managed backups. | Free tier → ~€25/mo |
| Object storage | **Cloudflare R2** or **Backblaze B2** | Raw artifacts forever. No egress fees on R2. | ~€1–5/mo |
| Crawling | **Firecrawl** (primary), **Playwright** (fallback) | Firecrawl returns clean markdown, handles most JS. Playwright only where genuinely needed and permitted. | ~€16–30/mo |
| Extraction | **Claude Sonnet 5** | Reads menus, PDFs, images directly. Vision included — no separate OCR pipeline for clean documents. | See §5 |
| Synthesis | **Claude Opus 5** | Weekly analysis, trend interpretation, adversarial review. | See §5 |
| Cheap classification | **Claude Haiku 4.5** | High-volume tagging once the taxonomy is stable. | See §5 |
| Embeddings | Third-party embedding model → `pgvector` | Anthropic doesn't serve embeddings; use any provider, store the vectors locally. | ~€1/mo |
| Orchestration | **n8n** (cloud or self-hosted) | Scheduling, retries, error notifications, visual debugging. | Free self-host → €20/mo cloud |
| Pipeline code | **Python 3.12** | Scripts called by n8n. Not a framework. | — |
| Dashboard | **Metabase** (managed or Docker) | SQL-native BI. No frontend to build. | Free → €85/mo |
| Newsletter | **Buttondown** or **Ghost** | Plain, exportable, no lock-in. | Free → €10/mo |
| Version control | **GitHub** | Code, prompts, taxonomy, and these docs. Prompts are versioned artifacts. | Free |
| Secrets | n8n credentials + `.env`, never committed | — | Free |

**Realistic total, Phase 1–3: €25–60/month.**

---

## 3. What we chose against, and when to revisit

| Rejected | Reason | Revisit when |
|---|---|---|
| Neo4j | `relationships` + recursive CTEs cover multi-hop at this scale | A graph query becomes central *and* slow — realistically year 2+ |
| Qdrant / Pinecone | `pgvector` is adequate past 1M embeddings | Embedding count > ~2M or hybrid search latency hurts |
| LangGraph | Agents are sequential and database-mediated; no stateful branching needed | An agent genuinely needs loops, branching, and retry-with-memory |
| Temporal | Massive operational overhead for weekly jobs | Never, at this scale |
| Multiple LLM providers | Splits attention, doubles prompt maintenance, no measured benefit | A specific task is measurably better elsewhere on *your* eval set |
| Separate OCR (Tesseract, Cloud Vision) | Sonnet reads clean PDFs and photos directly | A specific document class fails; then Tesseract locally before paying anyone |
| Custom dashboard | Metabase answers the questions; nobody is looking at it but you | A paying customer needs a specific view |
| Kubernetes / microservices | It's a weekly cron job and a database | Never |

Recorded as decisions `D-002` through `D-008` in `12-decision-log.md`.

---

## 4. Component topology

```
                    SOURCES
   venue sites · guides · trade press · registries
   Google Places API · your own photographs
                       │
              ┌────────┴────────┐
              │  COLLECTION     │   Firecrawl / Playwright / API clients
              │                 │   → raw artifact to R2 + documents row
              └────────┬────────┘   → content hash; unchanged = stop here
                       │
              ┌────────┴────────┐
              │  EXTRACTION     │   Claude Sonnet 5, structured output
              │                 │   → JSON validated against schema
              └────────┬────────┘   → schema fail = quarantine, never insert
                       │
              ┌────────┴────────┐
              │  RESOLUTION     │   entity matching, deduplication
              │                 │   → confident: link. unsure: review queue
              └────────┬────────┘
                       │
              ┌────────┴────────┐
              │   TAGGING       │   map to controlled vocabulary
              │                 │   → unmapped values to review queue
              └────────┬────────┘
                       │
              ╔════════╧════════╗
              ║    POSTGRES     ║   the actual product
              ╚════════╤════════╝
                       │
              ┌────────┴────────┐
              │   STATISTICS    │   SQL. counts, shares, z-scores, lead/lag
              │                 │   → signals table
              └────────┬────────┘   ← NO LLM IN THIS STEP
                       │
              ┌────────┴────────┐
              │ INTERPRETATION  │   Claude Opus 5 reads the numbers
              │                 │   → candidate trends, hypotheses
              └────────┬────────┘
                       │
              ┌────────┴────────┐
              │   CHALLENGE     │   Opus, adversarial prompt
              │                 │   → survives or dies
              └────────┬────────┘
                       │
         ┌─────────────┼─────────────┐
    Newsletter     Metabase      Prediction
                                  ledger
```

**The critical boundary is between STATISTICS and INTERPRETATION.** The LLM never counts. It never reports a number it wasn't given. Every figure in every published claim traces to a SQL query. An LLM asked "what trends do you see in this data" produces fluent invention with total confidence, and it will be wrong in ways that are extremely hard to notice.

---

## 5. Model routing and cost

Current API rates (verified against Anthropic's pricing documentation, 28 July 2026; re-check before budgeting):

| Model | Model ID | Input / Output per MTok | Use |
|---|---|---|---|
| Claude Haiku 4.5 | `claude-haiku-4-5-20251001` | $1 / $5 | Bulk classification, tagging against a stable taxonomy |
| Claude Sonnet 5 | `claude-sonnet-5` | $2 / $10 introductory through 31 Aug 2026, then $3 / $15 | Extraction, summarisation, menu and PDF reading. ~90% of volume |
| Claude Opus 5 | `claude-opus-5` | $5 / $25 | Weekly synthesis, trend interpretation, adversarial review |
| Claude Fable 5 | `claude-fable-5` | $10 / $50 | Not needed. Listed for completeness |

**Cost controls, in order of impact:**

1. **Content hashing.** Unchanged page → no extraction. Most menus change quarterly at most. This alone cuts extraction volume by 70–90% after the first pass.
2. **Batch API.** Extraction is never urgent. 50% discount for asynchronous processing. Use it for everything except interactive work.
3. **Prompt caching.** The extraction system prompt and taxonomy are large and constant. Cache hits cost roughly a tenth of base input rate.
4. **Model routing.** Never use Opus for extraction. Never use Sonnet for a task Haiku handles once the taxonomy is fixed.
5. **Truncate before sending.** Firecrawl markdown is already clean; strip navigation and footers before the model sees them.

**Estimated monthly LLM spend:**

| Phase | Volume | Estimate |
|---|---|---|
| Phase 1–2 | ~200 documents/mo, manual review | $5–15 |
| Phase 3–4 | ~1,000 documents/mo, batched and cached | $20–40 |
| Phase 5+ | ~2,500 documents/mo + weekly Opus synthesis | $40–80 |

Extraction volume dominates, not synthesis. Opus runs a handful of times a week.

---

## 6. Environments

Two, not three.

- **local** — Docker Postgres, real schema, small seeded dataset. Where extraction prompts are developed and broken.
- **prod** — managed Postgres, n8n schedules, real data. Also where you read.

No staging. At this scale it's ceremony. Guard prod instead with: append-only fact tables, nightly managed backups, and a weekly `pg_dump` to R2 that is *restored and verified* monthly. An untested backup is not a backup.

---

## 7. Failure handling

Assume unattended operation for weeks at a time. Design for silence, not for supervision.

| Failure | Behaviour | Alert |
|---|---|---|
| Source unreachable | Retry ×3, exponential backoff, then mark degraded and continue | Weekly digest only |
| Extraction schema violation | Quarantine to `extractions.raw_output`, `status='schema_fail'`, do not insert facts | Weekly digest |
| Entity unresolved | Route to `entity_candidates`, do not guess | Weekly review queue |
| Unmapped taxonomy value | Insert to `taxonomy_unmapped`, increment count | Weekly review queue |
| Null rate spike on a source | Likely site restructure; pause that source | Immediate email |
| Cost anomaly | Hard monthly cap in the API console; jobs fail closed | Immediate email |
| n8n job silently stops | Heartbeat check — if no successful run in 8 days, alert | Immediate email |

**The last one matters most.** The characteristic side-project failure isn't a crash, it's a job that quietly stopped in week 6 and wasn't noticed until week 14, leaving a hole in the time series. The heartbeat is the cheapest insurance in the whole system.

**Fail closed, never fail silent.** A pipeline that inserts garbage is far worse than one that stops, because garbage is discovered months later and by then it's mixed into everything.
