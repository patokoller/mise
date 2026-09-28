# MISE — Hospitality Intelligence Platform

**Publication:** The Next Table (Substack)

**Working name:** MISE (from *mise en place*). Rename freely; the name appears only here and in the brief.

**What this is:** the design documentation for a continuously-learning intelligence system about global hospitality — restaurants, hotels, chefs, menus, formats, and the money behind them. Built and operated by one person, part time.

**What this is not:** a newsletter with a database attached. The newsletter is the forcing function and the distribution channel. The asset is the dated, structured, source-linked record of what hospitality actually did, week by week, in a small number of cities.

---

## Who is building this

**A product manager, not a software engineer.** Business-oriented, comfortable with technology conceptually, not writing the code.

That isn't a footnote — it shapes real design decisions throughout these documents:

- **Claude does the building.** The operator specifies, judges, and validates. See `15-working-with-claude.md`.
- **Everything must be checkable without reading code.** Every component ships with a plain-English summary and a worked example you can verify against a real menu. See `16-validation-guide.md`.
- **Visible tools beat powerful ones.** n8n workflows over Python scripts, SQL views over application logic, managed services over anything self-hosted. Slightly less capable, considerably more inspectable — and inspectable wins.
- **The operator's real advantage is domain knowledge.** You know these restaurants. That catches bugs no test will, and it's why §3 of the validation guide works.

---

## How to use these files

Add this whole folder to a Claude Project as project knowledge. Then:

- **Starting a work session?** The relevant doc is your context. Say which phase you're in and paste or reference the doc.
- **Making a decision that contradicts a doc?** Don't silently diverge. Add an entry to `12-decision-log.md` and update the affected doc. The decision log is what makes this survivable across months of intermittent work.
- **Doc and reality disagree?** Reality wins, and the doc gets fixed the same day. Stale design docs are worse than none — they make you confident about things that aren't true anymore.

These are living documents. Every one has a `Status` and `Last reviewed` line at the top. If a doc hasn't been reviewed in three months and the project is active, it's probably lying to you.

---

## The document set

| # | File | What it answers |
|---|------|-----------------|
| 00 | `00-project-brief.md` | What are we building, for whom, and what are we deliberately not doing |
| 01 | `01-data-architecture.md` | How facts are modelled, stored, versioned, and resolved to entities |
| 02 | `02-technology-architecture.md` | What software runs where, what it costs, what we chose against |
| 03 | `03-data-flow.md` | The path a fact takes from source to published claim |
| 04 | `04-agent-workflows.md` | What each agent does, its inputs, outputs, model, and failure modes |
| 05 | `05-taxonomy-v1.md` | The controlled vocabulary that makes trends countable |
| 06 | `06-source-registry.md` | Where data comes from, per city, with access method and legal posture |
| 07 | `07-extraction-schemas.md` | The JSON contracts between LLM output and the database |
| 08 | `08-trend-detection.md` | How a signal is distinguished from noise, statistically |
| 09 | `09-editorial-and-predictions.md` | Publishing standards and the public prediction ledger |
| 10 | `10-legal-and-ethics.md` | Scraping, ToS, GDPR/FADP, copyright, what we will not do |
| 11 | `11-roadmap.md` | Phased build plan sized for a side project |
| 12 | `12-decision-log.md` | Every significant decision, dated, with the reasoning |
| 13 | `13-operating-cadence.md` | The weekly and monthly rituals that keep the time series unbroken |
| 14 | `14-glossary.md` | Shared vocabulary so terms mean one thing |
| 15 | `15-working-with-claude.md` | How to run build sessions when you're not the engineer |
| 16 | `16-validation-guide.md` | How to verify it works without reading code |
| 17 | `17-session-playbooks.md` | Copy-pasteable session briefs for every phase |
| 18 | `18-publishing-and-brand.md` | The Next Table: positioning, tiers, pricing, launch sequence |
| 19 | `19-data-visualisation.md` | Chart types, house style, and the small-sample honesty rules |
| 20 | `20-twenty-questions.md` | The twenty questions everything downstream is justified against |
| 21 | `21-venue-inclusion-criteria.md` | The mechanical venue rule: frame, routes, seeded cohort draw, what it misses |
| — | `BUILD-STATUS.md` | Live state of the build — updated every session |
| — | `schemas/schema.sql` | Executable Postgres DDL |
| — | `schemas/venue.schema.json` | JSON Schema for venue extraction |
| — | `schemas/menu_item.schema.json` | JSON Schema for menu item extraction |
| — | `schemas/event.schema.json` | JSON Schema for event extraction |

---

## The five things that matter most

If everything else in this folder is forgotten, keep these.

**1. Every fact carries a date and a source.** `observed_at`, `source_url`, `retrieved_at`. A fact without a date is not evidence of a trend, it's trivia. This is unrecoverable if you skip it — you cannot backfill dates you never captured. The same class of error applies to original-language dish names: a translation stored over a Danish or Catalan original cannot be undone (`D-020`).

**2. Entities are resolved, not typed.** "Noma", "noma", "Noma 2.0" are one venue. If this isn't enforced from the first row, every count you ever publish is wrong.

**3. The statistics come from SQL, the interpretation comes from the LLM.** Never ask a model "what trends do you see in this data." It will produce fluent, confident, invented patterns. Compute the counts, then ask the model what they might mean.

**4. Consistency beats intensity.** Twelve unglamorous weeks of logging beat three heroic weekends and a two-month gap. Gaps in a time series are not neutral — they make the surrounding data uninterpretable.

**5. Nothing gets built that you can't check.** Code that runs without errors and produces plausible numbers is the most dangerous output there is, because it looks exactly like success. Every component must prove itself against something you can see with your own eyes.

---

## Open assumptions

These were assumed, not confirmed. Correct them in `00-project-brief.md` when known.

- **Languages read comfortably:** English + Spanish, some French/Italian. **Not Danish** — confirmed 2026-07-28 (`D-022`). Copenhagen menus are believed to be mostly published in English, which keeps the by-eye verification model intact for menu data; that belief is untested and Phase 1 measures it via Q7. The real exposure is Danish-language company filings and trade press, which feed Q11, Q13, Q14 and Q17 — readable via translation, but not independently verifiable. See `00-project-brief.md` §4.
- **Third city:** **Barcelona**, confirmed 2026-07-28 (`D-021`). Madrid is out of scope — neither collected nor read.
- **Sustainable weekly hours on a *bad* week:** assumed 4–5. All timelines in `11-roadmap.md` are built on the floor, not the ceiling. Still unconfirmed.
- **Budget tolerance:** assumed under ~€50/month for the first six months.
- **Technical starting point:** confirmed — product manager, not an engineer. Comfortable with technology conceptually; not writing or maintaining code. Claude builds; the operator specifies and validates.
