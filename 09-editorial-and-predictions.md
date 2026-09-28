# 09 — Editorial and Predictions

**Status:** Draft v1
**Last reviewed:** 2026-07-28

**Publication:** The Next Table, on Substack. Positioning, tiers, pricing, and launch sequence are in `18-publishing-and-brand.md`. This document covers standards and the prediction ledger — the things that don't change with the platform.

---

## 1. Why publish at all

Three reasons, in order of importance:

1. **Discipline.** A weekly deadline forces you to interrogate the data. Without it, collection drifts and quality decays unobserved. This is the main reason.
2. **Error discovery.** Readers who know the industry will tell you when you're wrong. That is free, high-quality validation that you have no other way to buy.
3. **Distribution.** The audience becomes the customer base, eventually.

Note that revenue is third and distant. The newsletter is not the business; it's the practice that makes the business possible.

---

## 2. Standards

**Every claim states its denominator.** "8 of the 54 Copenhagen venues observed this quarter" — never "8 Copenhagen restaurants."

**Every claim states its timeframe.** A trend without a period is an assertion.

**Every claim is traceable.** You must be able to produce the source for anything published, within a minute.

**Uncertainty is stated, not hedged.** "We're not sure" is fine. "Some observers suggest" is not — it's cowardice dressed as balance.

**Group A counts state the publishing denominator, not the cohort size.** Venues recorded as `price_only` (a published price, no dish list — `D-027`) are in the cohort and answer Q4 and Q5, but cannot answer anything at dish level. So a course-count figure is "17 of the 44 tracked venues that publish dish lists," never "17 of 60 tracked." Using the cohort size on a dish-level count silently inflates the denominator.

**Every count states its frame as well as its denominator.** Two sentences, not one. "17 of the 60 Copenhagen venues we track" is honest about the cohort; it says nothing about the venues no guide lists and no publication has covered, and that population is unmeasured in every city (`21-venue-inclusion-criteria.md` §5). The second sentence never carries a number.

**Cohort-first is not origin.** A practice's earliest appearance in the data is its earliest appearance *in the cohort*, which is usually a mid-chain adopter. Origin claims require a census frame (`D-026`). False attribution is worse than "we don't know," because it looks publishable.

**If plausible explanations are listed, at least one must be boring.** Seasonality, a coverage change, a source addition. A list containing only interesting mechanisms is an assertion with a disclaimer attached — readers keep the mechanism and discard the hedge, and you will have published a claim you never wrote.

**Below-threshold observations are labelled as such.** They can be published as curiosities. They may not be published as trends.

**Corrections are published prominently**, in the next issue, with what went wrong and why. A visible correction history is an asset — it's evidence that the numbers are real, because nobody corrects invented ones.

**Name venues.** Anonymised claims can't be checked, and unfalsifiable claims are what makes existing trend reporting worthless.

**Independence is the differentiator.** You have no access to protect and no relationships to preserve. Write the unflattering finding. Trade press cannot, which is precisely why yours will be worth reading.

---

## 3. Issue structure

**Framing (`D-065`, 2026-09-28).** Each issue is about trends, not about a city. It opens with a one-line
standfirst stating the bet — that Copenhagen, Barcelona and London show direction early — as a bet. Each item
leads with the pattern and says which of the three cities it appears in; a claim about anywhere else needs a
dated, linked source from there. Origin claims stay under `D-026`.

Roughly 800–1,200 words. Consistency of format matters more than variety.

| Section | Content |
|---|---|
| **What moved** | 1–3 signals above threshold, with numbers and denominators |
| **What happened** | Notable events — openings, closings, moves, awards |
| **Worth watching** | 1–2 below-threshold observations, clearly labelled as speculative |
| **From the road** | Your own observations, when you've been somewhere |
| **Ledger** | Any predictions resolved this issue; running score |
| **Method note** | Coverage this period; anything that changed about how you measure |

A chart belongs in an issue when it shows something prose can't — a shape, a divergence, a lag. Not every week. Standards and the small-sample rules are in `19-data-visualisation.md`.

The method note is unglamorous and non-negotiable. It's what separates this from a trend report, and over time it's what makes the archive trustworthy.

---

## 4. The prediction ledger

**This is the most defensible thing in the entire project.**

A database can be replicated by someone with money. A two-year public record of dated, falsifiable calls — scored honestly, including the failures — cannot be replicated at any speed. It takes two years, and it requires having been willing to be wrong in public from the beginning.

Nobody in food media does this. It is the single clearest way to prove that the analysis works.

### Rules

**Falsifiable.** A prediction must have a resolution criterion that a stranger could apply without asking you.

- Good: *"By Q2 2027, at least 12 of the 60 Copenhagen venues we track will feature a non-alcoholic pairing as a listed menu option."*
- Bad: *"Non-alcoholic pairings will become more important."*

**Resolution criteria written before the outcome is known.** Recorded in the `predictions` table at the time of publication. This prevents the retrospective goalpost movement that everybody does unconsciously.

**Confidence stated numerically.** 0.6 means you expect to be wrong four times in ten. Calibration is the skill being demonstrated — a forecaster who is right 100% of the time at stated confidence 0.6 is *badly calibrated*, not brilliant.

**Every prediction resolves.** No quiet abandonment. `correct`, `incorrect`, `partial`, or `void` — and `void` only for genuinely unresolvable cases, with the reason published.

**Failures are published as loudly as successes.** A ledger with no failures is not credible and everyone knows it.

### Cadence

- 2–4 new predictions per month
- Horizons of 6–24 months, mixed
- All open predictions reviewed quarterly
- Calibration published every six months: at each confidence band, what proportion came true

### Prediction types

| Type | Example shape |
|---|---|
| Diffusion | Term X reaches N venues in city Y by date Z |
| Lead/lag | What appeared in Copenhagen appears in Barcelona within N quarters |
| Survival | Of the venues opened in cohort C, at least N% still trading at date Z |
| Price | Median tasting menu price in city Y exceeds P by date Z |
| Format | At least N new venues in city Y adopt format F by date Z |
| Negative | Format F does *not* exceed N venues — the most valuable and least common kind |

Negative predictions deserve particular attention. Calling that something *won't* happen, against consensus, and being right, is the most persuasive demonstration available. It is also where every trend report is silent, because there's no upside for them in being unfashionable.

---

## 5. Voice

- Plain. No industry jargon where a normal word exists.
- Specific. Named venues, real numbers, actual dates.
- Curious rather than authoritative. You are an outsider with a dataset, which is a genuinely interesting position — write from it rather than pretending otherwise.
- Short. A reader who finishes is worth more than one who is impressed.
- No hype. If the week's data is dull, say so and publish a short issue. Manufacturing significance is how credibility dies.

---

## 6. The role of the LLM in writing

The Editor agent drafts. **You publish.** Never automated end to end.

Reasons: reputational exposure is yours; the model does not know what you saw last week in Barcelona; and the act of editing is where you notice that a number looks wrong.

**Practical division:** the model produces the draft and the challenge pass. You cut it by a third, add whatever you actually observed, and write the prediction statements yourself. Prediction wording is too consequential to delegate — a slightly vague statement is unresolvable, and you won't discover that until eighteen months later.
