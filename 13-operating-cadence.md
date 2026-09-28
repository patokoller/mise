# 13 — Operating Cadence

**Status:** Draft v1
**Last reviewed:** 2026-07-28

---

## Why this document exists

The architecture in this folder is sound. That isn't what determines whether the project survives.

Side projects die from gaps. Not from bad decisions — from three good weeks, then a work crisis, then a holiday, then a vague sense of guilt, then nothing. And in *this* project a gap is unusually expensive: the asset is a time series, and a hole in a time series makes the data on both sides harder to interpret.

So the cadence is part of the design, not an afterthought. The target is a routine small enough to survive a bad month.

---

## The weekly loop (~2.5 hours)

Pick one fixed slot. Same day, same time. The consistency matters more than the day.

| Block | Time | What |
|---|---|---|
| **Review queues** | 30 min | Entity candidates, unmapped taxonomy, quarantined extractions |
| **Read the brief** | 20 min | The statistics brief. Look for anything that looks wrong before it looks interesting |
| **Editor pass** | 30 min | Run the agent, read the draft, cut a third, add what you actually saw |
| **Publish** | 20 min | Send it |
| **Housekeeping** | 20 min | Health check output, cost, any source that's gone quiet |
| **Slack** | 30 min | One improvement, or nothing. Sometimes nothing is right |

**The minimum viable week**, when everything is on fire: check that collection ran, publish three lines and the numbers. Twenty minutes. **This still counts.** The series stays intact and so does the habit.

---

## The monthly loop (~2 hours)

| Task | Time | Why |
|---|---|---|
| Gold-set evaluation | 45 min | The only defence against silent quality decay |
| Backup restore test | 15 min | An untested backup is not a backup |
| Venue list review | 20 min | Add venues, check against inclusion criteria, correct for your own drift |
| Unit economics reading | 30 min | Filed accounts, trade financial coverage. Closes the gap in `00-project-brief.md` §5 |
| Cost review | 10 min | Catch anything running away |

---

## The quarterly loop (~4 hours)

- Full taxonomy review — dead terms, inconsistent terms, watchlist graduations (`05-taxonomy-v1.md` §11)
- Review every open prediction; resolve what's resolvable
- Re-read `00-project-brief.md`. Is the scope still what you're actually doing? If not, fix the document or fix the behaviour
- Re-hand-extract five random recent documents and compare with pipeline output
- Coverage audit — what percentage of each city's defined segment is actually tracked
- One trip, if possible. Field observation is the proprietary layer

---

## The half-yearly loop

- Publish calibration: at each confidence band, what proportion of predictions came true
- Review the kill criteria in `00-project-brief.md` §8 honestly
- Re-read `10-legal-and-ethics.md`
- Ask whether this is still fun. That's a real criterion, not a soft one

---

## Failure protocols

**Missed one week.** Nothing. Publish next week, note the gap in the method note.

**Missed three weeks.** Do not attempt to catch up. Catching up is how people quit — the backlog becomes a wall. Restart from today, publish a short issue acknowledging the gap, run the pipeline forward. Backfill later or never.

**Missed two months.** Treat it as a restart. Spend one session checking what's broken (sources, credentials, schedules), one publishing something short, and resume. Do not redesign anything. The urge to redesign after a gap is procrastination wearing a lab coat.

**Lost interest.** Say so, in the decision log, with the date. Either park it deliberately — pipeline off, data backed up, documented — or stop. Both are respectable. Drifting is the only bad option, because it degrades the asset while producing nothing.

---

## What "on track" actually looks like

Not: elegant architecture, many agents, impressive dashboards.

**It's:** an unbroken run of weekly issues, however short. A database where every fact has a date and a source. A review queue under an hour. A gold-set score that hasn't dropped. And a slowly growing sense that you can answer questions nobody else can.

Everything in the other twelve documents exists to make that possible. If any of it starts obstructing it, the document is wrong and should be changed.
