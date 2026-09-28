# 08 — Trend Detection

**Status:** Draft v1
**Last reviewed:** 2026-07-28

---

## 1. The rule that governs everything here

**Statistics are computed in SQL. Interpretation is done by an LLM. The two never merge.**

An LLM given raw data and asked "what trends do you see" will produce fluent, specific, confident patterns that do not exist. It will invent percentages. It will describe a rise that is a fall. This failure is not rare and it is not obvious in the output — the invented version reads better than the true one.

So: SQL produces numbers into `signals`. The Editor reads `signals` and proposes what they might mean. Every published figure traces to a query.

---

## 2. Metrics

### Venue penetration
*What share of tracked venues in a city feature this term?*

```
penetration(term, city, period) =
    venues_with_term / venues_tracked_and_observed_in_period
```

The primary metric. Robust to menu length, which varies enormously.

**Critical:** the denominator is venues *observed in that period*, not venues *in the database*. A venue whose menu wasn't captured in Q2 is not a zero — it's absent. Treating absence as zero manufactures declines out of nothing.

### Item share
*What share of all menu items in scope carry this term?*

Sensitive to menu length and to which venues happened to be captured. Use as a secondary confirmation, never alone.

### First appearance
*When did this term first appear in this city, and at which venue?*

The diffusion metric. Underpins every lead/lag claim.

Guard hard against the archive effect: an early appearance may just be the oldest document you happen to hold. Only count first appearances within a period where the city had stable coverage.

### Price series
*Median tasting menu price, median main course price, by city and quarter.*

Report in local currency with a converted figure alongside. Currency movement is not a menu trend — conflating them produces confident nonsense about "London pricing power."

### Lead/lag
*Does city A's penetration curve for a term predict city B's, at some offset?*

Cross-correlation at lags of 1–8 quarters. **Requires at least 8 quarters of history in both cities.** Before that, do not compute it. Any lead/lag claim made in year one is noise dressed as insight.

### Demand corroboration
*Does search interest move with the menu signal?*

For a term above threshold, compare its menu penetration curve against Google Trends interest for the same city and period.

- **Both rise** — two independent sources agree. The strongest evidence available at this scale.
- **Menus rise, search flat** — a restaurant-led trend. Chefs are pushing it; diners haven't asked for it yet. Genuinely interesting and almost nobody distinguishes this.
- **Search rises, menus flat** — unmet demand, or a signal from outside restaurants entirely (a TV programme, a health story). Check before treating it as hospitality news.

**Constraint:** Trends data is relative and self-normalised. Use it to confirm *direction*, never to state a quantity. It may not be published as a count.

### Survival
*What proportion of venues that opened in cohort X are still trading at month N?*

Requires reliable closure data, which press does not provide. Company registries (Class F in `06-source-registry.md`) are essential here.

---

## 3. What counts as a signal

A measurement is a candidate signal when **all** of these hold:

1. **Sample floor** — at least 5 venues carrying the term, in at least 2 cities, or 8 venues in one city
2. **Denominator floor** — at least 25 venues observed in the period
3. **Magnitude** — penetration change of at least 5 percentage points, or a doubling from a base of at least 3 venues
4. **Persistence** — visible in at least 2 consecutive periods
5. **z-score** — at least 2.0 against the trailing 4-period baseline
6. **Not explained** — survives the checks in §5

Below these thresholds it is noise. Publishing it anyway is how a project like this destroys its own credibility in month four, permanently.

Thresholds are deliberately conservative for a small dataset. Loosen them only with a decision-log entry explaining why.

---

## 4. The statistics job

Weekly, pure SQL, writes to `signals`.

```sql
-- Quarterly tag penetration with a correct denominator.
WITH observed AS (
    -- venues whose menus were actually captured in the period
    SELECT DISTINCT e.city,
           date_trunc('quarter', m.observed_at)::date AS period,
           m.entity_id
    FROM menus m
    JOIN entities e ON e.entity_id = m.entity_id
    WHERE m.date_precision <> 'inferred'
      AND m.confidence >= 0.70
),
denom AS (
    SELECT city, period, COUNT(DISTINCT entity_id) AS venues_observed
    FROM observed GROUP BY city, period
),
numer AS (
    SELECT e.city,
           date_trunc('quarter', mi.observed_at)::date AS period,
           mit.term_id,
           COUNT(DISTINCT mi.entity_id) AS venues_with_term
    FROM menu_item_tags mit
    JOIN menu_items mi ON mi.item_id = mit.item_id
    JOIN entities e    ON e.entity_id = mi.entity_id
    WHERE mit.confidence >= 0.70
    GROUP BY e.city, period, mit.term_id
)
SELECT n.city, n.period, n.term_id,
       n.venues_with_term,
       d.venues_observed,
       ROUND(n.venues_with_term::numeric / d.venues_observed, 4) AS penetration
FROM numer n
JOIN denom d USING (city, period)
WHERE d.venues_observed >= 25;
```

Then z-scores against the trailing four periods, written to `signals` with `sample_size` always populated.

---

## 5. Bias corrections

These are the difference between analysis and self-deception. Each one has produced a false trend in someone's dataset.

### Cohort bias
Adding 20 vegetable-forward venues in March spikes every vegetable tag in March.

**Correction:** compute penetration over a *fixed cohort* — venues tracked since the start of the comparison window. Report new-venue effects separately and explicitly. `entities.first_seen_at` exists for exactly this.

### Observation bias
A term appears to rise because you captured more menus, not because more venues serve it.

**Correction:** denominator is always venues *observed*, never venues *known*. Report the observation rate alongside every signal.

### Seasonality
Asparagus in spring is not a trend. Game in autumn is not a trend.

**Correction:** compare year-over-year for the same quarter once 8 quarters exist. Before that, flag every seasonal-plausible ingredient and let the Editor's challenge pass kill it.

### Archive bias
Your first-appearance dates are bounded by when you started collecting.

**Correction:** never claim a first appearance within the first two quarters of a city's coverage. Record `coverage_start` per city and enforce it in queries.

### Source bias
Adding a source that covers one segment heavily shifts everything it touches.

**Correction:** log source additions with dates in the decision log. When a signal coincides with a source addition, that's the null hypothesis until disproved.

### Language bias
An English-only extraction pipeline systematically undercounts Catalan and Danish terms.

**Correction:** measure per-language extraction accuracy on the gold set. Report coverage by language.

### Frame bias
Your first-appearance dates are bounded by *which venues could ever have been seen*, not only by when you started looking. The frame in `21-venue-inclusion-criteria.md` is built from guide listings and press attention, so venues below both are absent from every count and absent from the exclusion log too — there is no row on which to record them.

**Correction:** none is available. This one is stated rather than corrected. **No origin claim unless the frame is enumerated as a census for that city** (`D-026`). Cohort-first is not origin. Copenhagen is the only city where an origin claim comes close to defensible, and even there it is origin-within-frame. London and Barcelona get wave shape only.

### Your own bias
You choose which venues to add. You are an enthusiast with preferences. Your sample will drift toward what you find interesting.

**Correction:** as of 2026-07-29 this is handled structurally rather than by self-discipline — the cohort is drawn from the frame by seeded random sample and cannot be edited (`21-venue-inclusion-criteria.md` §6, `D-023`). What remains discretionary is the *refresh*: the frame is re-run quarterly at a new frozen date, never topped up ad hoc, and each venue's addition date is recorded. The quarterly review now checks that the draw was honoured and that nothing entered outside a refresh, which is a checkable question rather than an act of self-knowledge.

---

## 6. The interpretation brief

What the Editor receives — a prepared document, never raw tables:

```
PERIOD: 2026 Q3
COVERAGE: Copenhagen 54/60 observed · Barcelona 61/70 · London 78/90

SIGNALS ABOVE THRESHOLD (7)
  1. ingredient:buckwheat · Copenhagen
     Q3 penetration 0.148 (8/54) · Q2 0.058 (3/52) · Q1 0.038 (2/52)
     z = 2.8 · fixed-cohort penetration 0.135 (7/52)
     Seasonal flag: no · Source additions this period: none

  [...]

EVENTS THIS PERIOD (23)
  openings 11 · closings 4 · chef_moves 5 · awards 3

OPEN PREDICTIONS RESOLVABLE THIS PERIOD (2)
  [...]

BELOW-THRESHOLD OBSERVATIONS (context only, NOT publishable)
  [...]
```

**Everything the Editor might publish is in this brief.** It has no access to the database. This is a structural guarantee against invented figures, and it is worth the small inconvenience.

---

## 7. Weak signals — and when they become possible

The most attractive idea in the original plan: the same thing appearing in four cities before anyone writes about it.

**It requires at least 12 months of history across all three cities.** Before that, a weak-signal detector has no baseline and will produce coincidences with confident narration attached.

**When it becomes viable, the method is:**
1. Terms below the publication threshold but non-zero in ≥2 cities
2. Rising in each, independently
3. Not present in trade press coverage for the period (check against a text index of collected articles)
4. Not seasonal
5. Traceable to specific venues you can name and check

Condition 3 is what makes it a *weak* signal rather than a trend — you are looking for things that are happening but not yet being discussed. That is the whole product.

**Handle with unusual care.** Weak signals are where the project either proves itself or embarrasses itself. Publish them as explicitly labelled speculation with named venues, so readers can check, and log them as predictions so you're scored on them.

---

## 8. Never do these

- Ask an LLM to count anything
- Publish a percentage without its denominator
- Compare periods with different coverage without saying so
- Compute lead/lag on under 8 quarters
- Claim a first appearance inside a city's first two quarters of coverage
- Claim an origin for a practice where the frame is a sample rather than a census (`D-026`)
- Publish a coverage claim in one sentence — the cohort denominator and the frame's attention bound are two separate statements
- Report a price change across currencies without separating FX movement
- Treat an unobserved venue as a zero
- Let a signal survive that coincides with a source or cohort addition, without saying so
