# 11 — Roadmap

**Status:** Draft v1
**Last reviewed:** 2026-07-28

**Sizing assumption:** 4–5 hours in a bad week, 8–10 in a good one. Every phase is scoped against the *floor*. A plan built on good weeks fails in month two, when the first bad month arrives.

**Whose hours these are.** Claude does the building; the hours here are yours — specifying, checking output against reality, reviewing queues, and publishing. Session briefs for every phase below are in `17-session-playbooks.md`, and the checks that tell you a phase is genuinely done are in `16-validation-guide.md` §3. Where a task below reads like engineering work, it's a thing to *ask for and verify*, not to build.

---

## Phase 0 — Decide (week 1, ~3 hours, no code)

Nothing is built until this is written down.

- [x] **Write 20 questions you want answerable in 12 months.** Done — `20-twenty-questions.md`. Everything downstream is justified by that list or it gets cut.
- [x] **Confirm the three cities.** Copenhagen, Barcelona, London. Madrid declined (`D-021`).
- [x] **Confirm languages.** No Danish (`D-022`). Copenhagen menu coverage rests on an untested assumption that Q7 will measure in Phase 1.
- [ ] **Draft the venue inclusion criteria.** Mechanical and hypothesis-blind — a rule a stranger could apply and return the same list. Write the criteria before naming a single restaurant; three strong hypotheses now exist and a hand-picked list will confirm them without anyone noticing. **This is the next session.**
- [ ] **Enumerate the frame, then draw the cohort** — seeded stratified random sample, 20 per city, seed `20260728`, no redraws (`D-023`, `21` §6). **This supersedes the original "list 60 candidate venues" line**, which described hand-selection and would have confirmed the three live hypotheses invisibly. Copenhagen's Route A frame is 132 (F1 only, 2026-08-01); Route B is unapplied and currently **blocked** (`D-055`). **The draw is not a precondition for Phase 1** — see below.
- [ ] Confirm the remaining assumptions in `README.md` — hours and budget. Neither blocks anything.
- [ ] Set up The Next Table on Substack — about page, method page, privacy notice (`18-publishing-and-brand.md` §7). Write no issues yet.

**Exit:** the 20 questions exist in a file. ✅ Met.

---

## Phase 1 — Publish by hand (weeks 2–6, ~5 hrs/week)

**No pipeline. No database. Spreadsheet and browser.**

- [ ] **40 venues** (confirmed 2026-08-10, `D-056`), menus collected by hand into a spreadsheet with dates and source URLs. **These are method-development venues, not the cohort.** The 40 are chosen by the operator to discover the schema and test whether the report is interesting by hand (`D-010`). They are **not** a sample: nothing published from them may carry a denominator, and when the cohort is drawn, collection restarts on the cohort. Same posture as the 2026-07-30 F2 test fixture — *secondary source, not frame data*. **40 is the Phase 1 exit target across weeks 2–6 (~8 per week), not the precondition for issue #1**, which needs only enough menus to support two or three observations that survive being argued against (`D-019`)
- [ ] **Record dish names in the original language.** A separate column for any translation, never in place of the original (`D-020`). This is the one Phase 1 habit that is unrecoverable if skipped
- [ ] Use Claude in the chat interface to read menus and suggest structure — this is where the schema gets *discovered* rather than guessed
- [ ] Publish issue #1 in week 3, then weekly. Variable length; no fixed number of observations (`D-019`)
- [ ] **Open the prediction ledger** (`D-018`). Five dated, falsifiable calls in month one, a few each month after. These are made *without* system data and are the intuition-only control group for Q20. A spreadsheet is sufficient; it needs a date, a claim, and a resolution criterion written before the outcome is known
- [ ] Log every field you wished you had

**Exit:** four issues published. A field list that came from real data rather than imagination. At least five predictions open with resolution dates.

**Why manual first:** if this report isn't interesting when you make it by hand, no architecture will make it interesting. Better to find that out in week 4 for the cost of five evenings.

---

## Phase 2 — Database and first extraction (weeks 7–12, ~5 hrs/week)

- [ ] Managed Postgres. Run `schemas/schema.sql`. Adjust for what Phase 1 taught you
- [ ] Backfill the 40 venues, with correct dates and sources
- [ ] Build the gold set: 30 hand-extracted documents (`04-agent-workflows.md` §7)
- [ ] One extraction script: menu URL or PDF → Sonnet 5 → validated JSON → database
- [ ] Get it working on one city, one document type, end to end
- [ ] Then broaden to the other formats
- [ ] Keep publishing weekly throughout

**Exit:** 60 venues, ~1,000 dated menu items, extraction running on demand. Weekly publication unbroken.

**The trap:** building the whole pipeline before one path works end to end. One document, all the way through, first.

---

## Phase 3 — Automate collection (months 4–5, ~5 hrs/week)

- [ ] n8n installed, `daily_scout` running
- [ ] Firecrawl integrated, source registry populated (`06-source-registry.md`)
- [ ] Entity resolution ladder implemented, review queue live
- [ ] Content hashing (the big cost saver)
- [ ] `health_check` workflow — heartbeat, null rates, queue depths
- [ ] Weekly human review habit established (~1 hour)
- [ ] Add Companies House and CVR for closure and financial data

**Exit:** the pipeline runs a week without intervention. 120 venues. Backups tested by restoring one.

**The trap:** skipping `health_check` because nothing has broken yet. It's the cheapest insurance in the system and it protects against the failure mode that actually kills these projects.

---

## Phase 4 — Make it countable (months 6–7, ~5 hrs/week)

- [ ] Taxonomy v1 loaded (`05-taxonomy-v1.md`)
- [ ] Tagging pipeline running; `taxonomy_unmapped` queue live
- [ ] Retroactively tag the whole corpus
- [ ] First monthly gold-set evaluation
- [ ] 150 venues

**Exit:** you can run a penetration query and get a number you believe.

---

## Phase 5 — Measure (months 8–10, ~5 hrs/week)

- [ ] Weekly statistics job writing to `signals`
- [ ] Bias corrections implemented — cohort, observation, seasonal (`08-trend-detection.md` §5)
- [ ] Metabase connected; build the six queries you actually look at
- [ ] Chart script generating PNGs in house style directly from `signals` (`19-data-visualisation.md` §4)
- [ ] Editor agent, three-pass, weekly
- [ ] **Migrate the prediction ledger into `predictions`** and link new calls to `supporting_signal_ids`. The ledger itself opened in Phase 1 (`D-018`); what happens here is that predictions start being *data-supported* rather than intuition-only, recorded via `predictions.basis`
- [ ] 200 venues

**Exit:** a published trend claim supported by counts with a denominator, that you'd defend to a sceptical chef.

---

## Phase 6 — Deepen (months 11–14)

- [ ] Unit economics: systematic reading of filed accounts. This is the gap identified in `00-project-brief.md` §5 and it closes here
- [ ] Relationship graph populated from event extraction
- [ ] First lead/lag analysis — only once 8 quarters exist in all three cities
- [ ] First predictions resolve. Publish the failures
- [ ] **Run Q20 for the first time:** `v_prediction_score` — do data-supported predictions beat the Phase 1 intuition-only ones? This is the project's stopping condition, and it is the first moment it can be answered with a number rather than a feeling
- [ ] Semantic layer: embed interviews and long-form, enable thematic search
- [ ] 250 venues

**Exit:** twelve months of history on the earliest cohort. First scored predictions published.

---

## Phase 7 — Test the value (months 15–20)

Nothing is built here until someone asks for something.

- [ ] Publish a deeper quarterly report — free. This is the proof the paid product can be made
- [ ] Check the four paid triggers in `18-publishing-and-brand.md` §4. If met, turn on subscriptions
- [ ] Talk to ten people in the target segments (`00-project-brief.md` §3). Ask what they'd pay for, not whether they like it
- [ ] Prototype the "ask the database a question" interface — Claude with SQL access over your schema
- [ ] Consider a paid tier only if there's specific demand

**Exit:** either a paying customer, or clarity that this stays a hobby — which is a perfectly good outcome, so long as it's chosen rather than drifted into.

---

## Phase 8 — Expand (month 21+)

**Only now.** Adding cities before this dilutes the depth that makes the data worth anything.

- [ ] Fourth and fifth cities — Paris and Milan are the obvious European next steps; Tokyo when the collection problem is solvable
- [ ] Consider Neo4j if graph queries have become central and slow
- [ ] Weak Signal Agent — now it has a baseline to work against

---

## What to protect when time is short

In a bad month, cut in this order. Cut from the bottom of the list only.

**Never cut:**
1. Collection continuity. A gap is unfillable and makes the surrounding data harder to interpret.
2. Dates and sources on every fact.

**Cut early:**
3. The weekly essay (publish three lines and the numbers instead)
4. New venue additions
5. New features of any kind
6. Reading, analysis, ambition

**A short, dull issue published on time is worth more than a good one published a month late** — because the dull one keeps the series intact and the habit alive.

---

## Milestone summary

| Month | Venues | Items | Capability |
|---|---|---|---|
| 1 | 40 | ~600 | Manual, publishing, **ledger open (intuition baseline)** |
| 3 | 60 | 1,000 | Database, extraction on demand |
| 5 | 120 | 2,000 | Automated collection |
| 7 | 150 | 3,000 | Tagged and countable |
| 10 | 200 | 4,500 | Signals; predictions become data-supported |
| 14 | 250 | 7,000 | 12 months history; first Q20 comparison scoreable |
| 20 | 250+ | 10,000+ | Testable commercial value |
