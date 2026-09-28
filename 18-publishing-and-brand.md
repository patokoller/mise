# 18 — Publishing and Brand

**Status:** Draft v1
**Last reviewed:** 2026-07-28

---

## 1. The publication

**Name:** The Next Table
**Platform:** Substack
**Model:** Free tier with a paid subscription layer, introduced on a trigger rather than a date (§4)

The name works because it carries both meanings the product needs: the table you'll be sitting at next, and the table you haven't heard of yet. It's a restaurant word, not a data word, which is right — the analysis is the method, not the pitch.

**Relationship to the platform:** The Next Table is the publication. MISE is the internal system that produces it. Readers never need to hear the second name. Keep them separable — if the platform later serves clients directly, it shouldn't be branded as a newsletter.

---

## 2. Positioning

**The one line:** *Where hospitality is going, measured rather than guessed.*

**What makes it different, in order of importance:**

1. **Numbers with denominators.** "Nine of the fifty-four Copenhagen restaurants we track" is a sentence no other food publication writes, because no other food publication has a denominator.
2. **A public prediction record.** Dated, falsifiable, scored, failures included (`09-editorial-and-predictions.md` §4). This is the thing nobody else will do, and after two years it's the whole moat.
3. **Independence.** No access to protect, no relationships to preserve. Able to publish the unflattering finding.
4. **An outsider's eye with an insider's data.** You're a diner with a database, not an industry veteran. That's an honest and interesting position — write from it rather than performing authority you don't have.

**Who it's for, in the reader's own words:**
- *"I run restaurants and I need to know whether this format is early or late."*
- *"I invest in hospitality and I want to know what actually survives."*
- *"I supply this industry and I want demand shifts before my sales figures show them."*
- *"I love restaurants and I want to understand them, not just read about them."*

The fourth group is the largest and pays least. It's still worth having — it's where credibility and word of mouth come from.

---

## 3. Free and paid

The free tier has to be good enough that people would pay for it. That's what makes the paid tier credible.

### Free — the weekly issue
- What moved, with numbers and denominators
- Notable events: openings, closings, moves
- One thing worth watching
- Prediction resolutions as they happen
- Method note

### Paid — depth, not access
- **Quarterly city reports.** A full read on one city: what opened, what closed, what changed on menus, price movement, survival rates for recent cohorts.
- **The full prediction ledger** with calibration data and the reasoning behind each call.
- **Data appendix** — the actual counts behind published claims, so a reader can check the work or reuse it.
- **Format deep-dives.** One format traced across three cities, with the unit economics where filed accounts allow.
- **Ask the database.** Paid subscribers submit a question; the best ones get answered publicly each month using real queries.

**The design principle:** paid content is *deeper*, never *earlier*. Withholding the weekly issue from free readers kills the growth engine that makes the paid tier possible. Every paid feature above requires the database — which is exactly right, because that's what nobody else can copy.

---

## 4. When to turn on payments

**Not at launch.** A paid subscription with no audience, no archive, and no track record converts nobody and signals nothing. Worse, it removes the pressure that makes the free product good.

**Turn on paid when all four are true:**

| Trigger | Threshold | Why |
|---|---|---|
| Archive | 25+ issues published | Proof of consistency; something to buy into |
| Audience | 750+ free subscribers | Below this, 2–5% conversion isn't a business |
| Track record | 3+ predictions resolved publicly | The thing that justifies paying |
| Depth capability | One quarterly report already produced free | Proof the paid product can actually be made |

Realistically that's month 12–15 on the roadmap in `11-roadmap.md`. Recorded as `D-014`.

**The signal to watch for before any of this:** an inbound question you can only answer because of the database. That's the market telling you what it wants — pay far more attention to it than to subscriber growth.

---

## 5. Pricing

**Benchmark:** free-to-paid conversion for newsletters typically lands between 2% and 5%.

**Suggested opening prices:**

| Tier | Price | Note |
|---|---|---|
| Monthly | €12 | Anchors the annual |
| Annual | €110 | ~24% saving; one transaction instead of twelve |
| Founding | €250 | Early supporters; add a real perk, not just a badge |
| Professional | €400+/yr | For operators and investors expensing it. Add: quarterly data extract, priority on questions |

**Price on value to a business, not on word count.** A restaurant group that avoids one bad concept decision has saved six figures. €400 is not the constraint; credibility is. This is also why the professional tier should exist from the moment paid launches — the buyers who matter aren't price-sensitive, they're evidence-sensitive.

**Annual over monthly, deliberately.** Stripe's flat per-transaction fee makes monthly subscriptions meaningfully worse at low price points, and annual subscribers churn less.

**Platform economics (verified 28 July 2026 — recheck before launching):** <cite index="18-1">Substack charges no monthly fee and takes 10% of paid subscription revenue, with Stripe taking roughly 3% on top, so on a €10/month subscription you keep about €8.70.</cite> <cite index="20-1">Publishing and email are free at any list size; connecting a custom domain is a one-time $50 fee.</cite>

**When to reconsider the platform:** <cite index="18-1">the arithmetic turns against Substack somewhere above roughly €1,000/month in subscription revenue, where a flat-fee platform starts costing less than the percentage.</cite> Don't optimise for this early — Substack's recommendation network is worth more than the fee when you have no audience. Revisit at €2,000 MRR, and log it as a decision when you do.

---

## 6. Why Substack, honestly

**For:** zero cost until revenue, no infrastructure, built-in discovery through recommendations and Notes, credible with the media-literate audience you want, subscriber list is exportable.

**Against:** 10% forever, limited design control, limited data on subscriber behaviour, and the audience is partly rented rather than owned.

**The verdict for this project:** correct for now, wrong eventually. The recommendation network solves the cold-start problem, which is your actual constraint. The fee only becomes the binding issue at a revenue level that would itself be a success.

**One thing to do from day one:** export the subscriber list monthly and keep it. Platform independence is a habit, not a migration project.

---

## 7. Launch sequence

**Before issue #1:**
- [ ] Publication created, named, described in one sentence
- [ ] About page: what this is, how the data is collected, who you are, why an outsider
- [ ] Privacy notice (required — see `10-legal-and-ethics.md` §4)
- [ ] Method page: how counts are produced, what a denominator means, what the confidence thresholds are. **Publish this before you need it.** It's the credibility document, and writing it early forces honesty.
- [ ] Custom domain, if you want one

**Issues 1–12 (Phase 1–2):** weekly, free, no paid tier, no promotion beyond people you know. Get good.

**Issues 13–25:** start the prediction ledger publicly. Begin using Notes. Answer questions in public. Let the recommendation network do its work.

**Issue 25+:** if the four triggers in §4 are met, turn on paid.

---

## 8. Growth, without doing anything undignified

**What works for this specific product:**
- **Being right in public, on the record.** A resolved prediction is a shareable artifact. Nobody else in the space has any.
- **Naming venues.** Named restaurants get shared by the people who work in them.
- **Publishing the failures.** A correction or a wrong prediction, handled well, generates more trust than three correct ones.
- **The data appendix.** Journalists and researchers cite sources that show their work. Citations are the best growth channel available to a publication like this.
- **Charts.** A penetration curve travels further than 900 words and carries the publication name with it. Standards in `19-data-visualisation.md`.
- **Substack Notes and recommendations.** The reason to be on the platform at all.

**What doesn't:** SEO, list swaps, posting frequency, "10 restaurant trends for 2027" listicles. The audience you want is small, specific, and allergic to that.

**A realistic trajectory:** 100 subscribers by month 6, 500 by month 12, 1,500 by month 20. Slow. The compounding is in the archive and the record, not the list.

---

## 9. Editorial constraints that don't bend

Restated here because publication pressure is what erodes them.

- Every number states its denominator
- Every claim is traceable to a query in under a minute
- Predictions are written by you, never by the model (`09-editorial-and-predictions.md` §6)
- Corrections are published prominently, in the next issue
- Free comps, hosted meals, or any interest in a venue are disclosed
- A dull week gets a short honest issue, not a manufactured one

The last one is the hardest and the most important. The pressure to make every week significant is exactly what makes existing trend coverage worthless.

### The methods note — published, not internal

Six rules go on a standing page, linked from every issue. Not marketing. Methodology. Readers who care will use it to judge each claim on its own merits, which is the whole proposition.

1. **Correlation is not diffusion.**
2. **Cohort-first is not origin.** The earliest appearance in our data is the earliest we could see, which is rarely the earliest there was.
3. **Absence from the cohort is not absence from the city.** Our sample is bounded by guide listings and press attention. What sits below both is unmeasured, and we will never give it a number.
4. **We never infer intent from menus.** A menu records what a restaurant serves and how it writes, not why.
5. **Predictions are timestamped before measurement**, in a public ledger, and scored whether or not they were right.
6. **Where we list plausible explanations, at least one is boring.**

Full derivation in `21-venue-inclusion-criteria.md` §12.

**Two cautions.** Publishing rules you then break is worse than never publishing them — rule 3 is the one a headline will break first. And the denominators and thresholds *are* the voice: nobody else publishes them, so they are the differentiator rather than the dull part. Write them as confidence, not apology. "That's below our publication threshold of 8 venues in a single city, so we're logging it rather than calling it" is shorter and more memorable than any hedge.
