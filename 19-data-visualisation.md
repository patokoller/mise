# 19 — Data Visualisation

**Status:** Draft v1
**Last reviewed:** 2026-07-28

---

## 1. Why charts matter more here than usual

Every other food publication uses photographs. A chart signals immediately that this publication is doing something different — it's the visual proof of the claim in `18-publishing-and-brand.md` §2 that this is measured rather than guessed.

Charts are also the most shareable artifact you'll produce. A screenshot of a well-made penetration curve travels further than 900 words, and it carries your publication name with it.

**But the same property makes them dangerous.** See §6, which is the most important section in this document.

---

## 2. The seven charts

Resist inventing new chart types weekly. A small, consistent set builds visual literacy in your readers — they learn to read your charts, which is worth more than novelty.

### 1. Penetration over time — the workhorse
Multi-line, one line per city, quarters on the x-axis, % of venues observed on the y-axis.

Answers: *is this spreading, where, and how fast?* This is the signature chart of the publication and will be 60% of what you publish.

### 2. City comparison at a point in time
Horizontal bar, one bar per city, sorted by value.

Answers: *where is this most established right now?* Use when the time dimension isn't the story.

### 3. Diffusion timeline
Dot plot. One row per city, a dot at first appearance, a second dot at the point it crossed a threshold.

Answers: *who led, who followed, how long was the lag?* Only usable once you have the history — see the archive-bias warning in `08-trend-detection.md` §5.

### 4. Price series
Line, local currency, one chart per city. **Never combine currencies on one chart.** If you must compare, index each city to 100 at a base quarter and say so in the subtitle.

### 5. Survival curve
Step chart. Cohort of venues opened in a period, % still trading over months since opening.

The most commercially interesting chart you'll ever publish, and the hardest — it needs reliable closure data from company registries (`06-source-registry.md` Class F), because press systematically underreports closings.

### 6. Menu composition
Stacked horizontal bar. Share of menu items by category, one bar per venue or per city.

Answers: *what does a menu here actually look like, and is that changing?*

### 7. Calibration plot — the signature chart
Scatter. Stated confidence on the x-axis, actual hit rate on the y-axis, with the diagonal drawn in. Published every six months per `09-editorial-and-predictions.md` §4.

**Nobody else in food media can publish this chart, because nobody else makes falsifiable predictions.** It's the single most persuasive visual the project will ever produce, and it's worth designing carefully when the time comes. A point sitting near the diagonal at 0.6 confidence is a stronger credibility claim than any amount of prose.

---

## 3. House style

Consistency matters more than beauty. Set these once, never fiddle.

| Element | Rule |
|---|---|
| Colour | One colour per city, fixed forever. Copenhagen, Barcelona, London keep their colours across every chart in every issue |
| Series distinction | Colour *plus* a line style (solid, dashed, dotted). Charts get screenshotted in greyscale and read by colourblind readers |
| Y-axis | Always starts at zero for penetration and share. Truncating a percentage axis exaggerates change and is the oldest trick in the book |
| Axis label | States the denominator: "% of venues observed that quarter" |
| Footnote | Sample size per city per period, and the coverage claim. Every chart, no exceptions |
| Gridlines | Horizontal only, hairline, recessive. No vertical gridlines on a time axis |
| Title | States what is measured, not what it means. "Buckwheat on dessert menus" — the interpretation goes in the prose |
| Dual axes | Never. Two scales means two charts |

**The rule that distinguishes you:** the denominator lives *inside* the chart image, not in the caption. Charts get screenshotted and separated from their text. A chart that misleads when detached from its article is a chart that will eventually mislead someone.

---

## 4. Production

**The constraint:** Substack takes images, not live charts. Everything ships as a static PNG. Export at 2× resolution — most readers are on retina screens and a soft chart looks amateurish.

**The recommended path, in order of how much you should prefer it:**

1. **Metabase → export PNG.** Zero extra tooling, already in the stack, adequate for internal use and fine for simple charts. Start here.
2. **A chart script Claude writes for you.** Reads directly from `signals`, applies house style automatically, outputs a PNG at the right size. This is the right answer from Phase 5 onward — one command, consistent output, denominator and footnote generated from the data rather than typed by hand.
3. **Manual tools (Datawrapper, Flourish).** Good output, but the data gets copied by hand, which means it can drift from the database. Use only for one-off explanatory graphics, never for recurring charts.

**Strong recommendation: option 2, generated from the database.** The reason isn't convenience — it's that a chart typed by hand can disagree with the database and nobody would ever know. A generated chart cannot. Given that you can't audit the code, "the chart is mechanically derived from the same rows as the claim" is a guarantee worth having.

**Ask for this when the time comes:**
> Build me a chart script that reads a signal from the database and produces a PNG in house style — city colours fixed, zero-based axis, denominator in the axis label, sample sizes in the footnote, all generated from the data rather than typed. One command, one chart. Show me one worked example I can check against the numbers.

---

## 5. Alt text and accessibility

Every chart needs a text description — for screen readers, for email clients that block images, and because Substack search doesn't index pixels.

**Format:** what it shows, the direction, the headline number with its denominator.

> "Line chart of buckwheat on dessert menus, 2025 Q3 to 2026 Q3. Copenhagen rises from 4% to 15% of venues observed; Barcelona from 2% to 7%; London flat near 4%."

Write this yourself. It's also a useful discipline — if you can't describe the chart in one sentence, the chart is doing too much.

---

## 6. The honesty problem

**This is the section to reread before publishing any chart.**

A chart looks authoritative regardless of what's behind it. A line drawn through five quarters of data from eight restaurants looks exactly as convincing as one drawn from eight thousand. The visual form confers a confidence the underlying sample has not earned, and readers — including sophisticated ones — respond to the form.

This is the specific way a project like this loses credibility: not by lying, but by drawing a smooth line through sparse data and letting the reader supply the certainty.

**Rules that follow:**

- **Never chart anything below the thresholds in `08-trend-detection.md` §3.** If it isn't publishable as a number, it isn't publishable as a picture. The chart is a stronger claim than the sentence, not a weaker one.
- **Sample size is always visible.** In the footnote at minimum; annotated at each point when n is small.
- **Under 8 venues, use dots, not lines.** A line implies continuity between measurements you didn't take. Dots are honest about being discrete observations.
- **Never smooth or interpolate.** No trend lines, no curve fitting, no projections into the future. If a quarter is missing, show the gap — a broken line is accurate; a bridged one is fiction.
- **Never extrapolate visually.** A dotted line extending past your last data point is a prediction, and predictions belong in the ledger where they get scored, not in a chart where they don't.
- **Cohort effects get annotated on the chart itself.** If you added 15 venues in Q2, mark it. Otherwise you're showing your own behaviour and calling it a trend.
- **A chart with n under 25 in the denominator carries a visible caveat**, in the chart, not the caption.

**The test before publishing:** *if a sceptical chef screenshots this and posts it saying "this is nonsense," does the chart contain enough information to defend itself?* If the answer is no, add what's missing or don't publish it.

---

## 7. What not to chart

- Anything from Google Trends as if it were a count. Trends is relative and self-normalised (`08-trend-detection.md` §2) — it can support a direction, never a quantity
- Individual venues' prices in a way that invites comparison shopping. That's a consumer product, not this one
- Anything where the interesting variation is in the denominator rather than the numerator
- Sentiment, until there's a defensible method behind it
- Anything you'd have to explain for two paragraphs before the reader could read it

---

## 8. When to add a chart to an issue

Not every week. A chart should earn its place by showing something prose can't — a shape, a divergence, a lag.

**Good reasons:** three cities moving differently; a curve that changed direction; a distribution that isn't what readers would assume.

**Bad reasons:** the issue looks thin; charts perform well; you built the script and want to use it.

**A realistic cadence:** one chart in most weekly issues, three to six in a quarterly report, one calibration plot every six months. The quarterly report is where visuals should be genuinely dense — that's the paid artifact, and it's where the data earns its keep.
