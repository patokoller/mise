# 17 — Session Playbooks

**Status:** Draft v1
**Last reviewed:** 2026-07-28

---

## How to use these

Each playbook is a session brief you can paste directly into a new conversation in the Project. They're written in business language on purpose — you shouldn't have to translate your intent into engineering terms, because that's where non-engineers accidentally specify the wrong thing.

**Every session ends the same way.** Paste this at the end, always:

> Before we finish: update BUILD-STATUS.md with what now exists and what's next. If we made a design decision, add it to 12-decision-log.md. If any document in the Project is now wrong, tell me which and fix it.

---

## Session 0 — Orientation (do this first, every time)

> Read BUILD-STATUS.md and 11-roadmap.md. Tell me where the project stands, what's working, what's half-finished, and what the next sensible piece of work is. Don't build anything yet.

If BUILD-STATUS.md doesn't exist yet, ask Claude to create it in Session 1.

---

## Phase 0 — The twenty questions

> I'm starting Phase 0. I want to produce the list of 20 questions this system should be able to answer in 12 months, which will justify or cut everything downstream.
>
> Interview me. Ask me one question at a time about what I actually want to know about restaurants in Copenhagen, Barcelona, and London. Push me toward questions that are specific and answerable from data — not "what's the next big thing" but things with a number and a timeframe in them.
>
> When we have 20, write them to a file, grouped by which part of the data model each depends on. Flag any that our current design can't answer, because those are either scope changes or things to drop.

---

## Phase 1 — Manual issue #1

> Phase 1. No code, no database. I want to publish the first newsletter issue by hand.
>
> Here are menus from [N] restaurants I collected this week: [paste or attach]. For each one, pull out the dishes, prices, and anything notable about format or service.
>
> Then: what's actually interesting here? Give me 3 candidate observations, and for each one argue against it — is the sample too small, is it seasonal, is it just what I happened to pick? Kill anything that doesn't survive.
>
> Then draft the issue using the structure in 09-editorial-and-predictions.md §3. Keep it under 900 words. Every claim states its denominator.
>
> Last: list every field you wished I'd captured. That becomes the schema.

---

## Phase 2a — Database setup

> Phase 2. I'm not an engineer, so build this so I can operate it without reading code. Read 15-working-with-claude.md before we start.
>
> Goal: get a working database running that I can put restaurant data into.
>
> 1. Recommend a managed Postgres host — I want free-to-start, easy backups, and a web interface I can click around in. Give me the setup steps as clicks, not commands, wherever possible.
> 2. Then run schemas/schema.sql against it and confirm it worked.
> 3. Then show me how to look at the tables myself, in a browser, without SQL.
> 4. Then insert one real restaurant with one real menu, end to end, and walk me through where every piece of it landed and why.
>
> Do these one at a time. Stop after each and tell me how to check it worked.

---

## Phase 2b — First extraction

> Phase 2 continued. Goal: I give you a restaurant's menu page URL, and its dishes end up in the database with the right date and source.
>
> Before writing anything: tell me what you'll build, what it will and won't handle, and how I'll check the result.
>
> Requirements:
> - It reads the menu and produces JSON matching schemas/menu_item.schema.json
> - It never invents anything — missing means null (see 07-extraction-schemas.md §1)
> - It records where the data came from and when it was retrieved, separately from when the menu was dated
> - If anything fails validation, nothing goes into the database and I get told
> - It prints a plain-English summary of what it did
>
> Start with one restaurant whose menu is a simple web page. Get that fully working before we touch PDFs or photos.
>
> Then: show me the raw page, the JSON, and the database rows side by side so I can check it by eye against the actual menu.

---

## Phase 2c — Gold set

> I need to build the gold set described in 04-agent-workflows.md §7 — 30 documents I've extracted by hand, which we'll use forever to measure whether extraction quality is degrading.
>
> Help me do this efficiently. Set up the file structure, tell me exactly what format to record my hand-extraction in, and make sure the mix covers: a clean HTML menu, a messy PDF, a phone photo, a Catalan menu, a Danish menu, a tasting menu with no prices, a news article, and an interview.
>
> Then build the script that runs the pipeline over the gold set and reports accuracy per field, in a table I can read. I want to run this monthly with one command and see immediately whether anything got worse.

---

## Phase 3 — Automation

> Phase 3. Goal: this runs itself daily without me touching it, and tells me if it stops.
>
> Read 03-data-flow.md and 04-agent-workflows.md §6.
>
> Build these in order, one per session if needed:
> 1. The source registry — populated from 06-source-registry.md, so nothing gets crawled that isn't registered
> 2. Daily collection — checks sources, skips anything unchanged since last time
> 3. The health check — heartbeat, error rates, queue depths, and an email if anything looks wrong
>
> Strong preference for n8n workflows over Python scripts wherever they're equivalent — I can look at a workflow and understand it; I can't do that with a script. Tell me when a script is genuinely necessary.
>
> After each piece: how do I break it on purpose to confirm the alerting works?

---

## Phase 4 — Tagging

> Phase 4. Goal: dishes get tagged against the taxonomy in 05-taxonomy-v1.md so I can count things.
>
> Requirements:
> - The model picks from the taxonomy only. It may not invent terms
> - Anything it can't map goes to the unmapped queue — that's correct behaviour, not failure, and the prompt should say so explicitly
> - Give me a simple weekly review screen for the unmapped queue, ordered by how often each unmapped value appeared
> - Then re-tag everything we've already collected
>
> Then pull 20 tagged dishes at random and show them to me so I can eyeball whether the tags are sensible.

---

## Phase 5 — Signals

> Phase 5. Goal: turn the data into trend measurements I can trust.
>
> Read 08-trend-detection.md carefully, especially §5 on bias corrections — those are the difference between analysis and fooling myself.
>
> Build the weekly statistics job. Pure SQL, no LLM anywhere in the counting. It must:
> - Use venues *observed* in the period as the denominator, never venues *known*
> - Apply the fixed-cohort correction so venues I added recently don't create fake trends
> - Flag seasonally plausible terms
> - Only emit signals that clear every threshold in §3
>
> Then build the interpretation brief from §6 — the prepared document the Editor sees. It must not have database access.
>
> Then: run it, show me the output, and tell me honestly whether we have enough data yet for any of it to mean anything.

---

## Weekly operating session

> Weekly run. Read 13-operating-cadence.md §"The weekly loop".
>
> 1. Health check summary — did everything run?
> 2. My three review queues, in a form I can work through quickly
> 3. This week's statistics brief
> 4. Run the Editor's three passes from 04-agent-workflows.md §5 — including the challenge pass, and be genuinely hard on the candidates
> 5. Draft the issue
>
> For anything you want me to publish as a number: tell me the denominator and the query it came from, or leave it out.

---

## Debugging session

> Something's wrong. Here's what I expected: [X]. Here's what I got: [Y].
>
> Don't fix it yet. First tell me what you think is happening and how we'd confirm it. Then walk me through the check. Then fix it.
>
> After the fix: what else might have been affected by this? Is any data already in the database wrong because of it? If so, how do we identify and correct those rows — remembering that we don't overwrite, we supersede (01-data-architecture.md §2).

---

## Quarterly review session

> Quarterly review. Read 00-project-brief.md, 12-decision-log.md, and BUILD-STATUS.md.
>
> 1. Is what I'm actually doing still what the brief says? Where has it drifted?
> 2. Which decisions in the log have hit their "reverses if" condition?
> 3. What in these documents is now wrong or misleading?
> 4. Coverage audit: what percentage of each city's defined segment are we actually tracking?
> 5. Which taxonomy terms have never been used, and which watchlist terms have graduated or died?
>
> Be blunt. I'd rather hear that something isn't working.

---

## A note on the ones that matter

If you only ever use three of these: **Session 0** (orientation, so you never restart cold), **the weekly operating session** (which is the project actually running), and **the debugging session** (because the "what else was affected" question is what stops one bug from becoming a year of quietly wrong data).
