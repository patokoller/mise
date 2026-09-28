# 20 — The Twenty Questions

**Status:** v1 — Phase 0 deliverable
**Last reviewed:** 2026-07-28

---

## What this file is for

Everything downstream is justified by this list or it gets cut. When a schema field, a source, a taxonomy facet, or a workflow is proposed, the test is: *which of these twenty does it serve?* If the answer is none, it doesn't get built.

Derived from an interview, 28 July 2026. Six questions asked; twenty extracted.

**Grouping is by what each question needs from the data model**, because that's what determines build order. A question is not "answerable" because it's interesting — it's answerable when the thing it counts exists in the database with a date and a source on it.

**Reading the flags:**

| Flag | Meaning |
|---|---|
| ✅ | Answerable within 12 months at planned scale |
| ⏳ | Answerable eventually; year one records the baseline only |
| ⚠️ | Answerable with a stated caveat that must be published alongside it |
| ❌ | Not answerable from public data. Listed so it stays dead |

---

## Group A — Menus and menu items

Needs: `menus`, `menu_items`, `observed_at`, price, language. Available from Phase 1 by hand, Phase 2 automatically.

**Q1** ✅ Among premium venues observed in both period A and period B, what is the median number of courses in the flagship tasting menu, and how has it changed?

**Q2** ✅ Among the same venues, how many à la carte dishes are on offer, and how has that changed?

**Q3** ⚠️ What is the median number of named ingredients per dish description, and how has that changed?
*Caveat: measures how restaurants write menus as much as how they cook. Directional only.*

**Q4** ✅ What is the price per course, and how has it changed?
*This is the sharpest test of the restraint hypothesis. The predicted signature is course count falling while price per course rises. Shorter and cheaper is a different story — cost pressure, not editing.*

**Q5** ⏳ Within each city, how wide is the spread between venues on course count, price per course, and rotation rate?
*Year one measures the spread. Whether the spread is widening needs several years and more venues per city than 20 — a bimodal distribution cannot be distinguished from a lumpy one at that N.*

**Q6** ✅ How often does each venue change its menu, and do venues cluster into distinct rotation behaviours?
*Rotation rate is the honest proxy for product-led versus concept-led operation. It is a behaviour, not a judgement.*

**Q7** ✅ In how many languages does each venue publish its menu, and does that correlate with anything else?

**Q8** ⏳ Does the same spread pattern appear in London and Copenhagen, or is Barcelona distinctive?
*A finding either way. Three cities that move identically is the genuine null result.*

---

## Group B — Venue attributes

Needs: `entities` with seat count, opening date, head chef, price point, neighbourhood. **Captured at first observation or lost permanently.**

**Q15** ✅ What formats, sizes and price points exist in each tracked neighbourhood, and how do those distributions differ?

**Q16** ⚠️ For a described concept, which venues in the corpus are the nearest comparables, what did they do over the observed period, and what became of them?
*Comparables, never probabilities. Typical N is 3–5. Publish as advisory work with evidence attached, never as a survival rate.*

---

## Group C — Events and relationships

Needs: `events`, `relationships`. Sources: trade press (Class D), guides (Class C), company registers (Class F).

**Q10** ✅ Which venues' former chefs and senior staff have opened or now lead other venues in the cohort?

**Q13** ⚠️ Which venues in the cohort closed, when, and how long had they been open?
*Two biases, both permanent: press under-reports closures by a wide margin, and the cohort is built from venues currently open and interesting enough to track. Survival rates computed on this are survival rates of survivors. Register data (Class F) partially corrects the first, nothing corrects the second.*

**Q14** ⏳ When a head chef departs, does the venue continue unchanged, change format, or close within 12 and 24 months?
*The 24-month version needs 24 months. The 12-month version is live from month 13.*

**Q17** ✅ How many openings, closures, and chef moves occurred in the tracked cities this period, and in what formats?
*The weekly spine. This is the one question that reliably produces something to publish every week.*

**Q18** ✅ Which groups are acquiring independents, and how is ownership concentration changing per city?

---

## Group D — Taxonomy and time

Needs: everything in Group A, plus taxonomy v1 applied consistently, plus enough history to see a lag. **The taxonomy is the instrument these are measured with, not an optional refinement.**

**Q9** ⏳ When a distinctive practice appears in the corpus, which venue showed it first, and how many months until it appears at others?
*The diffusion question — the operator's stated core interest. Two limits: co-occurrence is not copying, and if the originating venue is outside the cohort you see the wave with no source. Also bounded by `08-trend-detection.md` §5 archive bias — no first-appearance claim within the first two quarters of a city's coverage.*

**Q12** ⏳ Do venues that lead on diffusion receive critical recognition later, and with what lag?
*Tests the stated mechanism: that operator imitation precedes public awareness. Needs the lag to have elapsed.*

---

## Group E — Financial and registry

Needs: Class F sources. **Coverage is permanently uneven and this shapes which city can carry a money claim.**

**Q11** ⚠️ Among venues with publicly filed accounts, how do revenue per seat and margin differ by format?
*Denmark's CVR is unusually open; UK small-company filings give enough; Registro Mercantil access is unconfirmed and weaker. Expect to know most about Copenhagen, some about London, least about Barcelona. This is a shape of the data, not a gap to close.*

---

## Group F — Long-form and semantic

Needs: Class I sources, read manually. Automated weak-signal detection is deferred to month 21+.

**Q19** ⚠️ Among long-form pieces and interviews read this period, which themes recur — stated as *N of M documents read*?
*Publishable only with its denominator. Five mentions in twelve pieces read is a signal; five in two hundred is nothing. Below-threshold by construction — label as curiosity, never as trend.*

---

## Group G — The validation question

**Q20** ✅ Of the predictions in the public ledger, what share resolved correct — and do predictions made with system data outperform the intuition-only predictions made before the system existed?

*This is the stopping condition, made falsifiable. It requires the ledger to open in Phase 1 rather than Phase 5, so that early intuition-only predictions form a control group. Without that, the twelve-month evaluation is the operator judging their own investment from memory, which resolves nothing.*

---

## Permanently out of reach

Listed so they stay listed. Each was asked for; none has a public trace. Any system claiming to report these is inferring them and presenting the inference as observation.

- Staff turnover and retention
- Labour cost, food cost, any cost line
- Kitchen workload and brigade structure
- Supplier dependency
- Repeat visit rate and customer return behaviour
- Price elasticity — whether a price point suppresses return visits
- The room size at which service quality degrades
- Plating complexity
- Table-side theatre and service choreography
- Which restaurants operators are privately nervous about

**The last one is the operator's actual question.** It is not directly observable. Q9 and Q12 are its observable shadow: nervousness is invisible, but imitation is dated and public. That substitution is the single most important design move in this list, and it is the reason `observed_at` discipline is non-negotiable.

---

## What this list implies

**1. The payoff horizon is not twelve months.** Nine of twenty are ⏳ or need multiple years. The questions the operator most cares about — diffusion, divergence, survival — all need history that only exists if year one is recorded properly. Year one buys a baseline. This should be understood before month seven, not during it.

**2. Weekly publication rests on Group C, not Group A.** At 60 venues with quarterly-ish menu rotation, roughly five menus change per week, and `08-trend-detection.md` §3 requires 25 venues observed in a period before a signal may be emitted. Menu counting is structurally a quarterly instrument. Events are the weekly one.

**3. Four fields must be captured at first observation of every venue** — seat count, opening date, head chef, typical price point. None appear on a menu, all are findable when a venue is added, and none can be reconstructed later. Q14, Q15 and Q16 are dead without them.

**4. The taxonomy is load-bearing, not decorative.** Q3, Q9 and Q12 are measured with it. It cannot be deprioritised without losing the diffusion question.

**5. Venue selection determines what is discoverable.** Q9 can only find originators inside the cohort. Inclusion criteria must be mechanical and hypothesis-blind — a rule a stranger could apply to get the same list — or the corpus will confirm the hypotheses it was built around.

---

## Resolved 2026-07-28

**Third city: Barcelona** (`D-021`). Madrid is out of scope entirely. The Barcelona-vs-Madrid polarisation hypothesis raised during this interview is **retired, not deferred** — it cannot be tested with this cohort and must not be published as a claim. Q8 stands as written: a three-city comparison.

**Danish: not read** (`D-022`). Copenhagen stays a full collection city. Menu data is expected to remain operator-verifiable because menus in the target segment are believed mostly English — **an assumption Q7 tests for free in Phase 1, so record the answer.** The unverifiable material is Danish company filings and trade press, which is exactly what Q11, Q13, Q14 and Q17 depend on. Copenhagen claims in those four questions rest on source links rather than on the operator having checked them.

**Note what this does to Q11.** Denmark's CVR was the reason Copenhagen was expected to carry the strongest financial answer of the three cities. The filings are in Danish. The data is still gettable; the by-eye check on it is not. Weight London more heavily than the original plan implied for anything involving money.
