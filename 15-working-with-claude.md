# 15 — Working With Claude

**Status:** Draft v1
**Last reviewed:** 2026-07-28

---

## 1. The operating model

**You are the product manager. Claude is the engineering team.** That division works, but only if you hold the roles properly.

**What you own — never delegate these:**
- What gets built and in what order
- Whether the output is *correct*, judged against reality
- What counts as a trend, what gets published, how predictions are worded
- The venue list, the taxonomy, the editorial judgement
- Deciding when something is good enough to stop

**What Claude owns:**
- All code — SQL, Python, n8n configuration, prompts
- Debugging, error handling, edge cases
- Explaining what it built in language you can check
- Telling you when something can't be verified and what to do about it

**The failure mode this is guarding against:** a non-engineer building with AI usually can't distinguish *working* from *appears to work*. Code that runs without errors and produces plausible-looking numbers is the most dangerous possible output, because it's indistinguishable from success until you try to use it eight months later. Everything below exists to close that gap.

---

## 2. The self-evidencing principle

**Design rule, applying to everything built for this project: the system must prove it works in terms you can check without reading code.**

In practice this means every component ships with:

1. **A plain-English summary of what it did.** Not logs. "Checked 43 venue websites. 12 had changed. Extracted 187 menu items from those 12. 3 failed validation and are waiting for review."
2. **A number you can sanity-check against reality.** If it says it extracted 62 items from a menu you've seen, and that menu has 14 dishes, you've just caught a bug without reading a line of code.
3. **A way to see one example end to end.** "Show me the raw menu, then the JSON, then the database rows, for this one restaurant."

**Always ask for this.** A component that can only be verified by reading its source is a component you can't own. Tell Claude: *"Add a plain-English summary output and one worked example I can check by eye."*

---

## 3. How to run a build session

Use the playbooks in `17-session-playbooks.md` — they're written to be pasted directly. The shape of every session:

**1. Set context.** Say which phase you're in and which documents are relevant. In a Claude Project, the files are already there; just name them. *"We're in Phase 2. Relevant: 01-data-architecture, 07-extraction-schemas, schemas/schema.sql."*

**2. State the goal in business terms, not technical ones.** *"I want to be able to point at a restaurant's menu page and end up with its dishes in the database, with the date and the source."* Not *"build an ETL pipeline."* You'll specify the wrong thing if you try to speak engineering, and Claude will build exactly what you asked for.

**3. Ask for the plan before the code.** *"Before writing anything, tell me what you're going to build, what it will and won't do, and how I'll check it worked."* Read that. If any part doesn't make sense to you, that's a problem with the plan, not with you.

**4. Build one thing.** One script, one workflow, one query. Not a system.

**5. Demand the verification step.** *"How do I check this is right? Give me something specific to look at."*

**6. Actually check it.** This is the step that gets skipped and it's the only one that matters.

**7. Record it.** If a design decision was made, it goes in `12-decision-log.md`. If a document is now wrong, fix the document in the same session.

---

## 4. Phrases worth using

These reliably produce better output. Keep them handy.

> **"Explain what this does as if I'm a product manager, not an engineer."**

> **"What could go wrong with this that I wouldn't notice?"** — the single most valuable question in the whole project. Ask it about everything.

> **"Show me one worked example, from raw source to final database row."**

> **"What are you assuming that I haven't told you?"**

> **"Is there a simpler way to do this that's 80% as good?"** — usually yes, and at this scale usually correct.

> **"If I come back to this in three months having forgotten everything, what will confuse me?"**

> **"Don't build it yet. Tell me what you'd build and what it would cost me to maintain."**

> **"This looks wrong to me because [X]. Am I misunderstanding, or is it wrong?"** — trust this instinct. Business intuition catches real bugs, and "the number seems too high" is a legitimate bug report.

---

## 5. What to insist on in everything built

**Plain-language comments.** Every script explains, in normal English at the top, what it does, what it expects, and what it produces. You should be able to read the first paragraph of any file and know what it's for.

**Fails loudly, never silently.** If something breaks, you get an email. A pipeline that quietly stops is the characteristic way this project dies (see `13-operating-cadence.md`).

**No clever code.** Boring, obvious, repetitive code is correct here. If Claude suggests something elegant, ask what it costs in comprehensibility.

**A test you can run.** One command, or one button in n8n, that says "everything is working" or "here's what's broken."

**No new dependencies without justification.** Each one is a thing that can break and that you can't fix. Ask: *"Do we need this, or is it convenience?"*

---

## 6. Where to build

| Phase | Environment | Why |
|---|---|---|
| Phase 0–1 | This chat interface | No code. Reading menus, structuring data, drafting issues |
| Phase 2+ | **Claude Code** | It can write, run, test, and fix code in one loop. For a non-engineer this is the difference between "here's a script, good luck" and "it's working, here's the output" |
| Ongoing analysis | Chat + Metabase | Asking questions of the data, drafting issues |
| Heavier multi-step work | **Cowork** | Research, analysis, and file-producing tasks that span many steps |

**Claude Code matters more for you than it would for an engineer.** An engineer can take a script and make it run. You need the thing that runs it, sees the error, and fixes it — without you being the messenger between the code and the fix.

---

## 7. Prefer visible tools over invisible ones

A design bias worth applying throughout, and a real change from how I'd advise an engineer:

**Prefer n8n workflows over Python scripts wherever the two are equivalent.** An n8n workflow is a picture you can look at, click through, and reason about. A Python script is opaque unless you read it. n8n is slightly less powerful and considerably more inspectable, and inspectable wins here.

**Prefer SQL views over application logic.** A view is a saved question you can read in Metabase. Logic buried in a script is invisible.

**Prefer Metabase questions over custom charts.** You can modify a Metabase question yourself. You can't modify a chart someone coded.

**Keep Python for the parts that genuinely need it:** calling the Claude API, validating JSON, the entity resolution logic. Those should be few, small, single-purpose, and heavily commented.

Recorded as `D-012` in the decision log.

---

## 8. Continuity across sessions

You'll work on this in gaps, with weeks between sessions. Claude doesn't remember previous sessions unless you carry the context.

**What makes this work:**

- **The Project holds the documents.** They're the durable memory. Keep them current — a stale doc actively misleads.
- **`12-decision-log.md` is the "why" record.** Update it in the session where the decision is made, not later. Later doesn't happen.
- **Keep a `BUILD-STATUS.md`** at the top of the Project: what exists, what works, what's half-finished, what's next. Update it at the end of every session. Two minutes, and it's what lets you restart cold.
- **Start sessions by orienting Claude:** *"Read BUILD-STATUS.md and 11-roadmap.md. Tell me where we are and what's next before we do anything."*

---

## 9. When you're stuck

**If you don't understand an explanation**, that's information about the explanation, not about you. *"That didn't land. Try again with an analogy, and assume I know what a spreadsheet is and nothing more."*

**If something doesn't work and you can't say why**, describe what you expected and what you got. That's a complete bug report. You do not need to diagnose it.

**If you're being asked to make a technical decision you can't evaluate**, say so: *"I can't judge this. What would you choose, what's the tradeoff, and what would make us regret it?"* Then decide on the business consequence, which is your domain.

**If it feels too complicated**, it probably is. `02-technology-architecture.md` §1 says managed over self-hosted, boring over clever, nothing added without demonstrated need. Complexity is usually a sign that a step was skipped, not that the problem is hard.

---

## 10. What genuinely needs a human engineer

Honestly, and in scope order:

**Nothing, for Phases 0–5.** Managed Postgres, n8n, Firecrawl, the Claude API, and Metabase are all designed to be operated without an engineer, and Claude Code covers the code.

**Worth paying for a few hours if:**
- You start handling paying customers' data (security review)
- You want a public-facing product with logins (auth is easy to get subtly wrong)
- Something breaks that Claude can't fix across two or three sessions — usually an infrastructure or permissions problem rather than a code one
- Before any commercial launch: one hour of a data-protection lawyer, per `10-legal-and-ethics.md`

**Don't hire early.** An engineer joining before the data model is proven will want to rebuild it, and they'll be optimising for problems you don't have yet.
