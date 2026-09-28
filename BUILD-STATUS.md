# BUILD-STATUS

**Last updated:** 2026-09-28, second session (Phase 1 collection done for all 39; issue #1 drafted; decisions delegated to Claude, `D-062`)
**Current phase:** Phase 1 — in progress; Phase 0 half-finished, not blocking

> Update this at the end of every working session. Two minutes. It's what lets you restart cold after three weeks away, and it's the first thing Claude should read at the start of a session.

---

## Where things stand

> **2026-09-28, later — read this first.** The operator delegated decisions to Claude (`D-062`); every delegated decision says so in its log entry. **Phase 1 collection is done:** all 39 venues re-collected on 2026-09-28 — 73 menu rows, 771 dish rows, 37 trading, 2 closed per source (Connection, Brasserie Barner). Public venue-level file: `data/phase1/phase1-menus-2026-09-28.csv`; the dish file is private and held by the operator (`D-063`). `D-057`, `D-059`, `D-060` accepted. **Five predictions opened** in `predictions/phase1-ledger.md`, written by Claude and labelled so (`D-064`). **Issue #1 is drafted** as a Claude Doc; the operator checks three claims and publishes. Next: the operator's transcription pass on the `original_language_url` list, then re-collection in late December for P3.
>
> **2026-09-28 — earlier the same day.** No work happened between 2026-08-12 and 2026-09-28. Issue #1 has **not** been published (it was due week 3, 11–17 August). Everything below from 2026-08-12 is still the live state. The project now lives in GitHub — `github.com/patokoller/mise`, **public** (`D-061`) — and the August files that never reached Project knowledge were recovered into it (`recovery/2026-08/README.md`).

**Working:** the twenty questions exist (`20-twenty-questions.md`). The venue inclusion rule exists (`21-venue-inclusion-criteria.md`) — mechanical, frozen at frame date 2026-07-28, cohort seed `20260728` declared before enumeration.

**Half-finished:** Phase 0. Two items remain — the venue list (now: enumerate the frame, then run the draw) and Substack setup. **Neither blocks Phase 1.** Phase 1 works **40 operator-chosen method-development venues** (`D-056`), not the cohort; issue #1 is due week 3 (11–17 August) on `11-roadmap.md`'s own schedule.

**Copenhagen's Route A frame is 132 venues (2026-08-01), and it now exists as an artefact** — `cph-route-a-frame-union.xlsx`, one row per venue, keyed on `google_place_id`, with 8 CHECK rows that fail loudly in plain English. Every published denominator will rest on it.

| | Count | Denominator |
|---|---|---|
| **A1 ∪ A2, passing F1** | **132** | of 282 candidate rows across both guides (83 + 199) |
| Both routes | 45 | of 132 |
| A1-only (MICHELIN, not White Guide) | 23 | of 132 |
| A2-only (White Guide, not MICHELIN) | 64 | of 132 |
| Københavns / Frederiksberg | 123 / 9 | of 132 |

Checked four ways that share no code — set intersection, a merge-walk over sorted ID lists, a kommune decomposition (62+101−123 = 40 and 6+8−9 = 5, summing to the same 45), and an independent rebuild from row-level data on 2026-08-01. 23+45+64 = 132; 68+109−45 = 132.

**This is F1 only.** F2, F4 and F5 are unapplied, so 132 will fall. Route B is unapplied, so it will then rise. It is Copenhagen's **Route A** frame, not Copenhagen's frame, and nothing may be published against it as a denominator yet.

**132 is no longer a floor.** The caveat "plus up to 14 unadjudicated A2 rows" is discharged — see the A2 line below.

**A1 — MICHELIN Guide Nordic Countries 2026.** 83 candidates, retrieved via Firecrawl at `proxy: basic`, within `10` §2. All five tier counts reconciled against the guide's own stated figures (`D-032`'s first live pass), and that reconciliation is now a CHECK row rather than a sentence. 72 Danish rows resolved to address and `google_place_id`. **68 pass F1** (62 Københavns, 6 Frederiksberg); 15 fail — 4 on the resolved address, 11 on country (Malmö, never resolved). Four CHECK rows added 2026-08-01, all PASS.

**A2 — White Guide Denmark.** 199 unique venues. No stated total exists, so completeness was asserted by tier reconciliation (`D-037`): 28/67/81/21/3. **109 pass F1** (101 Københavns, 8 Frederiksberg); **87 outside_boundary**; **3 not_trading**; **0 unresolved**. 109 + 87 + 3 + 0 = 199, and the file checks that itself. All five tiers kept (`D-036`).

**All 14 `unresolved` A2 rows were adjudicated by the operator on 2026-08-01, and the result reverses `D-040`'s interpretation (`D-044`).** 12 are trading venues **outside the boundary**; 2 no longer exist. `unresolved` in Copenhagen was overwhelmingly an **unrecognised-geography** failure, not an unrecognised-closure one — the earlier 2-of-2 sample pointed the wrong way. `D-040`'s underlying fact stands: Places does not return permanently closed venues.

**Two findings from those 14 that travel to the other cities.** First, **the F0 resolver was scoped to Copenhagen.** White Guide's address strings on these rows are truncated to street and number with no locality, so F1 could not be applied to the guide's own text and the rows fell through to Places, which was looking in the wrong place. **This will recur in London and Barcelona and will be harder to spot there**, because a wrong match in Greater London looks plausible. Second, **White Guide Denmark includes the Faroe Islands** — 5 of the 199 — which bears on `D-037`, where completeness was asserted against a guide whose territory had never been established.

**Only one of the 3 `not_trading` rows carries an F1 verdict.** Kiin Kiin Tok Tok's address was confirmed (`D-041`); VesterVenner and Toto's never were, so no boundary verdict is possible on either and they are counted in no F1 line. All three carry `D-041`'s dating caveat — closure observed four days after frame date, no published closure date, so the frame-date verdict is an inference and is not backfilled.

---

## Phase 1 — started 2026-08-12, partial

**Collection has begun.** The operator supplied 39 venue rows carrying 30 URLs, opened personally in
one batch at ~11:30 CEST on 2026-08-12. Claude fetched **8 of those 30** and stopped deliberately.

| | Count | Denominator |
|---|---|---|
| Pages fetched | **8** | of 30 URLs supplied, of 39 venue rows |
| F2 `full` | 6 | of 8 fetched |
| F2 `price_only` | 2 | of 8 fetched |
| Dish rows captured | 110 | — |
| Page served English only | 7 | of 8 fetched |
| Original-language menu reachable at the URL supplied | 2 | of 8 fetched |

**None of these are a sample.** `D-056` (confirmed by the operator 2026-08-12) holds: nothing
published from the Phase 1 forty carries a denominator.

**Why it stopped at 8.** The Enigma trilingual PDF showed machine extraction silently corrupting
original-language text — ÀNEC→ÅNEC, CIRERA→CIIRERA, El→EI. That is `D-020`'s unrecoverable field,
damaged invisibly, in a way review cannot catch because nobody on this project reads Catalan or
Danish (`D-022`). `D-059` proposed in response: original-language names are human-transcribed;
machine extraction may carry prices, structure, format, service and F2 only.

**Q7 — first evidence, unverified assumption since 2026-07-28.** 7 of 8 fetched pages served English
only; Enigma alone published multiple languages (es/en/ca in one artefact). But 5 of the 8 were
Copenhagen and **no Danish page was seen at all** — several URLs carried `-UK` or `English` in the
path, so Danish versions likely exist and were not the URLs collected. The assumption survives this
look and is **not** confirmed by it.

**Phase 1 capture template built** (`phase1-menu-capture-template.xlsx`) — Menus sheet, Dishes sheet,
Legend. Dropdowns on the controlled-vocabulary columns; no formulas, deliberately. Not yet filled.

**Findings that travel beyond Phase 1:**

- **akmē carries 1500 and 1300 DKK live on one page** — confirmed, not remembered. Two `Menu`
  blocks, set menu and tasting menu. No mechanical rule resolves this; flagged, not chosen.
- **The Ledbury's three prices are NOT that case** — £220 / £270 / £295 are labelled lunch-6,
  lunch-8 and dinner. Structure, not conflict. A rule that confuses the two would be wrong on both.
- **The Ledbury rendered every content block twice** in extraction (tabbed panels). Naive count 14,
  true count 7. Correct code over doubled input gives a wrong answer that looks right.
- **Page freshness ≠ menu freshness.** Geranium's menu page still carried a COVID-19 notice and a
  "closed 5–29 July" message, live on 12 August.
- **A venue's `/en/` path may be a translation, not the menu.** Prodigi's supplied URL is the
  venue's own English rendering; the Catalan original is elsewhere on the site, so
  `dish_name_original` cannot be filled from that URL at all.
- **Anarki's à la carte says "see the blackboard"** — an F2 ceiling no method crosses.
- **Anarki's PDF lost a dish name** in extraction ("& vanilla ice cream 115"). Logged as damaged,
  not guessed.

**Open on the source file itself:** Kadeau, Alchemist, Alouette, Humble Chicken, Disfrutar and Aleia
carry no URL and no F2 verdict — "not available" from a search is not F2 `none` from a human looking.
Noma's URL reads `noma.co.com`, which is expected to be wrong (`noma.dk`); unverified. **Connection
and Brasserie Barner are asserted closed with no source, and both are in the 132-venue frame.**

**Composition drift, recorded:** the Copenhagen twenty proposed by Claude were selected from the
frame file by documented non-random stratified fill (`D-058`). The returned file substituted
**Paula** — which is **not in the 132-venue frame** — for **a|o|c** and **Studio**, which both are.

---

**Noma is not in MICHELIN Nordic 2026.** Operator-verified 2026-08-01. It enters the frame on White Guide alone, so A1's enumeration is confirmed correct and the `D-032` tier reconciliation was not masking a substitution. **Still open:** Noma's F4 status needs an explicit decision when F4 runs, not before — the most prominent venue in the census city, holding one route of two.

**Naming is settled as a rule, not as a string (`D-043`).** The canonical name is the venue's **own published name in its own orthography**, captured at the F2 pass. Not source precedence, which would make the name a function of which guides list the venue and flip it when a listing lapses. The union file's column is `display_name_provisional` until then, and **no name may be published from it**. The schema half of this is `D-047`.

**14 name variants across the 45 dual-route venues** — 4 prefix, 8 orthography, 1 translation (Kadeau), 1 genuinely distinct name (Aotori / Kappo Ando, one venue, `D-046`). An earlier count of 9 was wrong: five case-only differences had been normalised away.

**`M1` is deleted (`D-042` reversed).** The operator declined to endorse it. The **Method predictions** sheet survives as a structure with no live prediction and a red-flagged record that `M1` must never be scored or reconstructed after F4 runs.

**Next: Route B** against the five registered Copenhagen titles — **blocked on operator decisions and archive access, not on build work.** Stage 0 recon ran 2026-08-02 and 2026-08-10; Stage 0b reach testing ran 2026-08-10. Access posture is established for **5 of 5** Copenhagen titles (3 `permitted`, 1 `blocked_by_robots`, 1 `pending_access`). **Archive reach is now demonstrated for 1 of 5 registered titles, 1 of 3 permitted** — Scandinavian Standard, by sitemap. **MigogKbh's sitemap fails on staleness; Berlingske remains unproven after four tests.** No press item has been collected and no Route B candidate exists. Records: `cph-route-b-stage0-recon.md`, `cph-route-b-stage0b-reach.md`. Decisions `D-048` to `D-055` accepted. **Route B Copenhagen is not runnable today** — the two-items-two-titles rule cannot function on one reachable title. **Then:** F2, F4, F5 and price across the whole frame in one pass.

**Route B registry** set 2026-07-29 (`06` §4A, `D-030`) — 7 Barcelona, 7 London, 5 Copenhagen. **Still frozen** (`D-052`), and unaffected in membership. Copenhagen's five now carry access statuses (`D-048`), and criterion 2 no longer counts as satisfied at registration (`D-051`).

**Then:** cohort draw with seed `20260728` → collection.

**Two open registry gaps, not blocking:** Barcelona has no Catalan-language title and no trade title, while London carries three trade titles. That asymmetry will inflate London's large-group share and damage Q8 and Q18 comparability. Recorded in `D-030`.

---

## Cities and languages — settled 2026-07-28

| Decision | Outcome | Log |
|---|---|---|
| Third city | **Barcelona.** Madrid out of scope; the Barcelona-vs-Madrid hypothesis is retired, not deferred | `D-021` |
| Danish | **Not read.** Copenhagen stays a full collection city. Menus expected mostly English — untested; Q7 measures it in Phase 1. Danish filings and trade press are readable via translation but not operator-verifiable | `D-022` |

**Why criteria before names.** Three strong hypotheses now exist about what the data will show. A venue list assembled by thinking of restaurants first will confirm them without anyone noticing. Q9 can only ever find originators inside the cohort, so whatever the rule excludes is permanently invisible.

---

## Venue criteria — settled 2026-07-29

| Decision | Outcome | Log |
|---|---|---|
| Selection method | **Mechanical rule.** Frozen frame date, three qualifying routes, frame enumerated in full, cohort drawn by seeded random sample. **No redraws** | `D-023` |
| Ownership size | **Recorded, not filtered.** The ≤10-venue exclusion is withdrawn — Q18 cannot measure concentration on a frame that excludes concentrators. Reverses a `00` §4 assumption | `D-024` |
| Exclusions | **Kept as rows with reason codes.** Closure never deletes. Coverage claims are two sentences, and the second never carries a number | `D-025` |
| Q9 origin claims | **Not publishable from a sampled frame.** Year one reports diffusion shape. Copenhagen only, and only as origin-within-frame | `D-026` |

**The clause most likely to break:** no redraws (`21` §6). It will be tested the first time the draw returns twenty venues that look dull.

---

## Calibration — run 2026-07-29

Twelve venues, three cities, verdicts pre-registered. **Six agreements, one disagreement** across seven clean comparisons. Full results in `21` §11.1.

**Four amendments, all dated:**

| Finding | Change | Log |
|---|---|---|
| Alchemist publishes a Tock price, no dish list — was excluded | F2 becomes three states: `full` / `price_only` / `none`. Published by the venue, not compiled about it | `D-027` |
| Ducasse passes a name test containing the hotel's name; Moments passes on a hotel sub-page | F6 withdrawn — hotel F&B qualifies on routes like anything else | `D-028` |
| "AMA" matched four Barcelona venues | F0 entity resolution added before any filter | `D-029` |
| JKS counts partnered and invested concepts in its own tally | `ownership_scale` counts operated venues only | `D-029` |

**The one disagreement:** Bar Brutal — expected include, excluded on F2. **Pompette in Copenhagen failed identically**, which makes the natural-wine-bar exclusion structural rather than a Barcelona artifact. Neither generates an exclusion row, because neither holds a route.

**Still untested:** the matched pair across cities (the A2 asymmetry, and the biggest live risk to Q8), outer London against the F1 boundary, and Danish-language menu publication. Copenhagen was tested on two venues only.

---

## What exists

| Component | Status | Where | Notes |
|---|---|---|---|
| Design documentation | ✅ Complete v1 | This Project | docs 00–20 |
| Twenty questions | ✅ Complete | `20-twenty-questions.md` | 9 of 20 need multi-year data; flagged in the file |
| Database schema | ✅ Ready to run | `schema.sql` | v1 + D-020 + **D-047**, folded in 2026-08-01 and parsed clean (69 statements). Not yet deployed. `schema-patch-D047.sql` is kept as the record of the change and is marked **do not run** |
| Venue inclusion criteria | ✅ Complete v1 | `21-venue-inclusion-criteria.md` | Mechanical, hypothesis-blind. Calibration test in §11 not yet run |
| Frame enumeration | 🟨 Partial | `cph-route-a-frame-union.xlsx`, `cph-route-a1-frame.xlsx`, `cph-route-a2-frame.xlsx` | **Copenhagen Route A frame = 132, artefact written 2026-08-01.** F1 only, 8 CHECK rows, all PASS. Route B not started. London and Barcelona not started |
| Venue list (cohort) | ⬜ Not started | — | 20/city, drawn by seed `20260728` once the frame exists |
| Prediction ledger — the three hypotheses | ✅ Recorded 2026-07-29 | `predictionledger.xlsx` | 3 hypotheses + 8 scoring clauses, dated before the frame exists. `M1` deleted unendorsed 2026-08-01 (`D-042` reversed). Held locally until the `predictions` table is deployed |
| Calibration test | ✅ Run 2026-07-29 | `21` §11.1 | 12 venues, 6 of 7 clean agreements. Rule amended after — `D-027`, `D-028`, `D-029` |
| Route B publication registry | ✅ Set 2026-07-29 | `06` §4A | 19 titles across 3 cities. Eater London removed — dead since Feb 2023. Award lists removed. `D-030` |
| Prediction ledger — ongoing practice | ✅ Opened 2026-09-28 — `predictions/phase1-ledger.md`, P1–P5, Claude-authored (`D-064`) | — | Opens Phase 1, by hand, spreadsheet is fine (`D-018`). **Confirmed 2026-08-01: distinct from the row above.** One records the three hypotheses (done); this is the running ledger (not started). Both stay |
| The Next Table (Substack) | 🟨 Issue #1 drafted 2026-09-28 (Claude Doc), not published; Substack account setup not confirmed | — | Free tier only until the §4 triggers in doc 18 |
| Extraction pipeline | ⬜ Not started | — | Phase 2 |
| Gold set | ⬜ Not started | — | 30 documents, ~3 hours once |
| Automated collection | ⬜ Not started | — | Phase 3 |
| Tagging | ⬜ Not started | — | Taxonomy v1 drafted. Load-bearing for Q3, Q9, Q12 |
| Statistics job | ⬜ Not started | — | Phase 5 |
| Chart production | ⬜ Not started | — | Metabase PNG first, generated script from Phase 5 |

---

## Credentials and accounts

Record *where* things live, never the secrets themselves.

| Service | Account | Where the key lives |
|---|---|---|
| GitHub | `patokoller/mise` (public) | Claude pushes via the Claude GitHub App; no key stored anywhere in the repo |

---

## Known issues

| Issue | Impact | Since | Fix planned |
|---|---|---|---|
| **`schema.sql` cannot hold a dish awaiting transcription** | `menu_items.name_original` is `NOT NULL`, but `D-059` leaves it empty until a person transcribes it. Loading Phase 1 into the schema as written would force a machine string into the one field that must not hold one | 2026-09-28 | Phase 2: relax to nullable and add `name_as_extracted` + `name_original_transcription`, matching `menu_item.schema.json` v1.1.0 |
| **Some published menus are labelled "sample"** | Da Terra, Restaurant Gordon Ramsay High, Casa Fofò. A sample tells you the style, not what was served; rotation (Q6, P3) measured on them would read as zero change | 2026-09-28 | Flag in `notes`; exclude or caveat sample menus when scoring P3 |
| **No menu carried a date** | All 73 rows have `observed_at_source = retrieval` (`D-057`). `16`'s Phase 2 "date test" would flag this as a bug; here it is correct | 2026-09-28 | Documented in `16` Phase 1 checks |
| **Delegated decisions are unchecked by a second person** | Under `D-062` Claude both makes and verifies decisions. The remaining by-eye checks are the operator's pre-publication read and the transcription pass | 2026-09-28 | Operator skims `12-decision-log.md` for entries marked "by Claude under `D-062`" at his convenience |
| **Project knowledge silently fell behind the work** | The 2026-08-12 session's four outputs, the A1 and A2 frame files, and one 2026-08-01 edit (the schema row, which then contradicted `schema.sql`) never reached Project knowledge. Found 2026-09-28, seven weeks later | 2026-09-28 | Recovered from transcripts into GitHub (`recovery/2026-08/`). The operator's own `list_and_menus.xlsx` (39 rows, URLs) is **not recoverable**. Guard: every session ends with a commit, and `D-061` makes one copy the master |
| **Repo documents are transcribed copies, not file copies** | The Project tool returns text, so the 2026-09-28 import was re-typed by Claude. No byte-level proof it matches. Same error class as the `ø` matcher and case-normalisation bugs | 2026-09-28 | Operator spot-check: open two documents on GitHub and compare a Danish-character passage against the Project copy |
| **Public repo holds guide-derived lists** | `data/` carries full MICHELIN and White Guide Copenhagen listings (names, tiers, addresses). `10` §3 permits collecting facts and forbids reproducing descriptive prose; it says nothing about publishing a whole enumerated list. No guide prose was found in the files | 2026-09-28 | Operator decision, made: public for now (`D-061`). The specialist hour `10` recommends before launch should cover this |
| "Copenhagen menus are mostly English" is unverified | Load-bearing for by-eye validation of a third of the corpus | 2026-07-28 | Q7 measures it in Phase 1. Record the answer; caveat Copenhagen menu claims if the share is low |
| Copenhagen financial/event data not operator-verifiable | Q11, Q13, Q14, Q17 rest on source links rather than a by-eye check. Weight London for money claims | 2026-07-28 | Accepted limitation (`D-022`), not a bug to fix |
| No place to log manually-read sources | Q19 needs "N of M documents read"; `documents` requires a stored artifact, which paywalled articles won't have | 2026-07-28 | **Phase 2**, once Phase 1 shows what's actually read. Deliberately not fixed now |
| `17-session-playbooks.md` has no brief for the venue criteria session | Minor; brief supplied in chat instead | 2026-07-28 | Add when convenient |
| Michelin Spain 2026 edition date unverified | Route A1 vintages differ by city and must be recorded for reproducibility | 2026-07-29 | Record at enumeration. GB&I verified: 9 Feb 2026, Dublin |
| Members' clubs are invisible, not excluded | The Arts Club holds no route, so `membership_only` never gets written. Unlike the below-attention population, members' clubs are enumerable | 2026-07-29 | Operator decision — count them separately, or state the silence |
| London's A2 may be too narrow | Bouchon Racine placed first in the UK at the National Restaurant Awards 2026; NRA Top 100 is not a registered route. Michelin caught it anyway | 2026-07-29 | Operator decision — register NRA Top 100 as a London A3? |
| Group A counts now need two denominators | `price_only` venues are in the cohort but answer no dish-level question | 2026-07-29 | Handled in `09` §2; a live chance to get a published number wrong |
| The below-attention venue population is unmeasurable | Largest blind spot in the frame; sized at zero forever by construction | 2026-07-29 | Not fixable (`D-025`). Stated in every coverage claim |
| Q6 rotation rate is biased by F2 | The kitchens that change daily are least likely to publish a current menu | 2026-07-29 | Exclusion codes size the gap per city; the correlation itself is untestable and must not be published as a claim |
| ~~MICHELIN unreachable~~ **RESOLVED 2026-07-30** | Firecrawl reaches it at `proxy: basic`. Method recorded in `06` §4 so the §7 quarterly refresh is repeatable | 2026-07-30 | Closed. Re-test at each refresh — the WAF may tighten, and the fallback is still *ask the publisher*, never stealth mode |
| White Guide Denmark has no dated edition | Copenhagen's A2 is not reproducible as written, which fails `21` §1's stranger test. Affects the frame, therefore Q15 and Q18 | 2026-07-30 | Operator defines the snapshot rule. `21` §4, §12.1 item 7 |
| White Guide tier scope never tested against the Repsol precedent | If the lower tiers are large, Copenhagen's A2 stops being comparable to the other two cities in a way `21` §4's asymmetry note doesn't cover. Lands on Q8 | 2026-07-30 | Decide with counts visible, once retrieval works. `21` §12.1 item 8 |
| Firecrawl carries two silent-failure modes | LLM extraction fabricating frame rows; truncated listings producing a frame that is quietly too small. Both invisible on inspection and both corrupt every denominator downstream | 2026-07-30 | Closed as rules: `D-031` (deterministic parsing only) and `D-032` (count assertion or halt). Enforcement is a build requirement on the first crawl, not a later addition |
| `api.firecrawl.dev` blocked by the egress allowlist | Key exists and is unused. Both A1 and A2 retrieval depend on it | 2026-07-30 | Operator adds the domain in network settings. Only remaining hard blocker (`21` §12.1 item 6) |
| F2 needed a human on 5 of 6 venues tested | Not one failure mode but five different ones — stale markup, single-page sites, multi-hop navigation, competing official domains, merged menus. Cost model for enumeration is therefore unknown | 2026-07-30 | Re-measure on a Bib/Selected sample once A1 retrieval works; the starred tier may be the worst case |
| `observed_at` cannot be derived from a menu page | No venue in the sample dated its menu. Rule #1 requires `observed_at` and `retrieved_at` as separate fields | 2026-07-30 | For menus, `observed_at` comes from the retrieval event unless the page carries its own date. Needs a written rule before Phase 2 |
| No mechanical rule decides competing prices on one page | akmē carried 1500 and 1300 DKK; only the operator could tell which was live | 2026-07-30 | Candidate rule: prefer the price whose companion artefact carries the later date, else flag. Not yet a decision |
| A correct-looking formula can assert the wrong thing | A summary formula returned 61 where the answer was 72. It recalculated green — `D-032` catches a row-count mismatch, not a wrong arithmetic expression. Caught by reading the number, before the file was shared | 2026-07-30 | Every summary figure gets eyeballed against a hand count before a file is presented. There is no automated guard for this class |
| Michelin's city label is not a boundary | Six "Copenhagen" venues are in Frederiksberg; Restaurant VIE is filed under "Nordhavn" but is inside Københavns Kommune | 2026-07-30 | F1 applies to resolved addresses only. Recorded in `21` §12.1 |
| White Guide's locality strings are worse than Michelin's | 'København' is used as a REGION prefix — 'København / Hellerup' and 'København / Gentofte' are outside the boundary while containing the word. 13 entries have no locality at all | 2026-07-30 | F1 on resolved addresses only. The 75 A2 exclusions rest on the guide's locality, which is weaker evidence than A1's exclusions and is labelled as such in the file |
| Cross-guide name matching fails on Danish characters | `ø` does not decompose under NFKD and was being deleted, not folded — `Kadeau København` did not match `Kadeau Copenhagen`. Would have created a duplicate in the union | 2026-07-30 | Fixed for `ø`, `æ`, `å`. Any future matcher needs the same handling; this is the class of bug that produces a silent duplicate venue |
| **Google Places does not return permanently closed venues** | A venue that shut before enumeration presents as a *wrong-venue match*, never as a closure. The fact stands; the inference drawn from it did not | 2026-08-01 | Rule written (`D-040`). **Interpretation amended by `D-044`:** on the full 14 Copenhagen cases, `unresolved` was 12 unrecognised *geography* and only 2 closure. Copenhagen's bucket is now empty. London and Barcelona still owe the same by-hand pass |
| **The F0 resolver was scoped to the target city** | A candidate outside the city returns a plausible wrong local match, is correctly rejected, and lands in `unresolved` — so out-of-territory venues masquerade as ambiguity. 12 of Copenhagen's 14 were this. **Will recur in London and Barcelona and will be harder to see there**, because a wrong match in Greater London looks plausible where a wrong match for a Faroese venue does not | 2026-08-01 | Before enumerating either city: resolve on the guide's full address text where it exists, and treat a truncated address (street and number, no locality) as its own state rather than letting it fall through to `unresolved` (`D-044`) |
| White Guide Denmark includes the Faroe Islands | 5 of 199. The guide's actual territory was never established before completeness was asserted by tier reconciliation | 2026-08-01 | Recorded in `D-044`. Check each guide's stated territory at enumeration, before reconciling counts against it (`D-037`) |
| White Guide's addresses are wrong in at least 3 of the 14 cases where they could be checked | Domæne (60 vs 62), Syttende (23 vs 25), Etika (a different street entirely, so possibly a relocation). **75 of A2's exclusions rest on this address text** | 2026-08-01 | Not fixable at source. Sized, stated, and labelled as weaker evidence than A1's exclusions, which is already the file's posture |
| A closure observed after the frame date is an inference, not an observation | Google publishes no closure date, so "closed on 2026-08-01" cannot establish "closed on 2026-07-28". Applies to every F4 verdict reached by hand after the frame date | 2026-08-01 | Labelled as an inference on the row and never backfilled (`D-041`). The spreadsheet cannot hold two observation dates per venue; `venue_facts.valid_from` handles it once the schema is deployed |
| Count blocks were shipped without recalculation | openpyxl writes formulas with no cached values, so `cph-route-a2-frame.xlsx` displayed six blank counts while being correct underneath. That is what produced the 110 error below | 2026-08-01 | Recalculate before sharing — now a line in the file's own legend. **Owed:** the same check on every future file |
| Sub-breakdowns were not conditioned on their parent's filter | A2's "of which Københavns" counted every row with that kommune, including excluded ones, so the breakdown could exceed the total it sat under. Introduced and caught within one session on 2026-08-01 | 2026-08-01 | **Closed 2026-08-01.** Fixed via `COUNTIFS`. Every count block now carries CHECK rows — A1 (4), A2 (3), the union (8), the ledger (1) |
| A normalisation can silently delete a real difference | Comparing names case-insensitively reported 9 variants where an exact comparison finds 14. The five it hid were case-only — `formel B`, `Jatak`, `Koan`, `Restaurant VIE`, `à terre` — which is exactly the venue's own styling that `D-020` exists to preserve. Same class as the `ø` matcher bug | 2026-08-01 | The union file's CHECK row recomputes the difference count from the strings themselves rather than trusting the classification. Any future matcher needs the same guard |
| Sources contradict themselves and only a person can settle it | Three cases so far: akmē's two prices, Anarki's two classifications, Michelin/White Guide naming one venue three ways | 2026-07-30 | No rule proposed. Each is decided individually and logged (`D-035`, `D-038`, `D-039`). Volume at this scale is manageable; at 3 cities it may not be |
| **Copenhagen Post disallows `ClaudeBot` by name** | 1 of 5 registered Copenhagen titles is unreachable under `10` §2. It was registered to carry the English-language requirement | 2026-08-02 | Carried as `blocked_by_robots` (`D-048`), not dropped. Disposition open — hand-qualify, request permission, or leave unreached |
| **Politiken `pending_access`** | `robots.txt` names `anthropic-ai` and `Claude-Web` site-wide; `ClaudeBot` absent, which is a gap not a grant (`D-049`). `/search` disallowed for all agents regardless | 2026-08-02 | Licence or explicit permission. No content fetched meanwhile |
| **Archive reach unverified for every Route B title in every city** | `06` §4A criterion 2 was treated as settled at registration. Berlingske — the easiest permitted Copenhagen title — failed on section index and sitemap and is unproven on search after four tests | 2026-08-02 | `D-051`. Reach demonstrated per title before any sweep is planned. 15 titles to check |
| **Berlingske `?page=N` is silently ignored** | Returns HTTP 200 and the identical first page. A paginator built on it would insert 10 articles as 4,289 with every CHECK row passing — invisible to the operator | 2026-08-10 | Any paginator must assert page N+1's first date is older than page N's last, and halt if not |
| **The Phase 1 forty could become the cohort by habit** | The 40 method-development venues are operator-chosen. If any of them enters the *frame* because it was worked in Phase 1, the seeded draw is contaminated and `D-023`'s whole purpose is lost. Overlap between the forty and the drawn cohort is fine; causation from one to the other is not | 2026-08-10 | `D-056`. The frame stays mechanical and hypothesis-blind. Nothing published from the forty carries a denominator |
| **A sitemap `lastmod` is not a publication date** | Scandinavian Standard's 2023-11-08 bulk re-save stamped hundreds of 2020 articles with that date. One verified article: sitemap `lastmod` 2024-08-01, real `article:published_time` 2024-06-30. Dating a Route B sweep from `lastmod` would silently misplace items by months or years | 2026-08-10 | `D-053`. Publication dates come from `article:published_time` on the article page, never from a sitemap. Applies to every title in every city |
| **MigogKbh's sitemap is ~12 weeks stale** | Retrieved 2026-08-10; newest entry anywhere in its 113-child index is 2026-05-19. The site is live and publishing. A sweep would silently miss the last ten weeks of the Route B window with well-formed XML and no error | 2026-08-10 | Cause **not** guessed at. Section index and on-site search still untested — both are the next test |
| **A category archive can serve real pagination over no content** | Scandinavian Standard's `/category/food-drink/page/2/` is a genuine server-side URL, but the page returns 18 links and zero articles at a 6s render delay. Real pagination is not evidence of a usable index | 2026-08-10 | `D-054`. Reach requires seeing dated items, not seeing a paginator |
| **Scandinavian Standard's inventory has changed shape** | 133 of 1,696 posts (7.8%) carry slugs over 90 chars; the historic 1,000 contain zero, longest 88. Items of this shape are cross-published on four other domains. Any count of "items published by this title" needs a denominator that separates them | 2026-08-10 | Precision, not reach. **Not** grounds to touch the frozen registry (`D-052`). Size before relying on the title |
| **Route B failure modes are title-specific and each looks like success** | Three distinct kinds now found: a paginator that lies (Berlingske), a date field that lies (Scandinavian Standard), an index that silently stops (MigogKbh). None visible on inspection | 2026-08-10 | `D-051` per-title testing is the only defence. 15 titles × 3 routes. This is the standing argument for a licensed archive |
| **Berlingske search is not demonstrably reproducible** | The same URL returned two different result sets within one session. Rule 1 needs a source URL that means something stable | 2026-08-10 | Cause unknown, deliberately not guessed. Must be understood before the route carries a frame |
| **Restaurant content is not confined to gastronomy sections** | A Copenhagen restaurant item sat under `/oplevelser/`. A section-named sweep undercounts and the index never reveals what it excluded. Applies to all three cities | 2026-08-02 | `D-051` — section lists established empirically per title. Section-agnostic search preferred where available |
| **Route B has no completeness anchor** | No title publishes how many items it ran, so `D-032`'s count-assertion-or-halt rule has nothing to bite on and a sweep cannot be shown complete | 2026-08-02 | Not otherwise fixable. A licensed archive's per-title source list would be the first real anchor |
| **Infomedia is now Retriever** | Merged; platform migrated 14 April 2026. Any procedure naming Infomedia is already stale | 2026-08-02 | Name Retriever if the licensed route is adopted |

---

## Corrections

Kept visible, because a correction history is what makes the rest trustworthy.

| Date | What was wrong | Correction |
|---|---|---|
| 2026-07-28 | Claude asserted `schema.sql` lacked seat count, opening date, head chef and price point, without reading the file | False. `venues.opened_on`, `venue_facts` (`seats`, `price_band`) and `relationships` (`chef_at`) all existed. The temporal-attribute design was already better than the fixed columns proposed. Three real gaps were found on actually reading it — logged as `D-020` and the two schema rows in the change log |
| 2026-08-01 | **Third instance of the same pattern, this time caught mid-session.** Claude reported that `cph-route-a2-frame.xlsx`'s count block held "labels but no numbers," implying missing or broken formulas — inferred from the symptom of blank values, without opening the formula view | False. All six formulas were present and correct, returning 199/109/101/8/75/15. The file had simply never been recalculated. Corrected to the operator in the same turn, before anything was written. **This is the 2026-07-28 and 2026-07-30 pattern exactly: a conclusion about a file's contents drawn from a symptom rather than from reading it.** Three instances now; treat any statement about a file Claude has not opened as unreliable by default |
| 2026-08-01 | `12-decision-log.md` recorded **"110 of 199 pass F1 (101 Københavns, 9 Frederiksberg)"** for A2 on 2026-07-30 | False — the figure is **109 (101 + 8)**. 110 + 75 + 15 = 200, one more venue than the file contains; 109 + 75 + 15 = 199 exactly. The union was computed from row-level data, so the frame of 132 is unaffected — but had the log been trusted, the first published frame size would have been 133. **A new error class:** not an unread file, but a number transcribed without being reconciled against anything |
| 2026-08-01 | Prediction ledger status tally read Open 6 / Void 1 / Resolved 0 | False — there are **8** clauses, not 7. `COUNTIF` matched `"Open"` exactly and skipped H3-b (`"Open — long horizon"`), and the mean-confidence line dropped the same clause, averaging 6 of 7. Mean corrects 0.608 → 0.600. Third instance of the known issue *a correct-looking formula can assert the wrong thing* |
| 2026-08-01 | **Fourth instance of the same pattern.** Claude told the operator the union file contains nine CHECK rows, and wrote "nine" into the file's own legend | False — there are **eight** (rows 143, 145, 147, 150, 152, 159, 160, 161). The number was miscounted from terminal output Claude had just been shown, then repeated as fact and shipped inside the artefact. Caught by the operator on inspection. **The pattern is now four deep and has widened:** it is no longer only claims about files Claude has not opened, but claims about files Claude *has* opened and did not verify. Legend corrected |
| 2026-08-01 | Claude reported **9** name variants between the two guides, in chat and in the union file | False — an exact, case-sensitive comparison finds **14**. Five pairs differ only in case and had been normalised away by a case-insensitive test. Claude also mis-grouped `Restaurant AOC / a\|o\|c` as prefix noise when the residual difference after stripping the prefix is orthographic. Corrected, and the file now carries a CHECK row that recomputes the count from the strings rather than trusting the classification |
| 2026-08-01 | `D-040` concluded that `unresolved` is principally **unrecognised closure**, on a sample of 2 of 2 | Wrong in direction. On the full 14, adjudicated by the operator, it was **12 geography and 2 closure**. The underlying fact — Places does not return closed venues — stands. The characterisation built on two data points did not. Amended by `D-044`, which is kept as a separate entry rather than an edit, because the sequence (small sample → confident inference → full check → reversal) is itself the finding |
| 2026-08-10 | **Fifth instance of the same pattern.** Claude told the operator MigogKbh's sitemap index had **112** children, from a glance at the XML rather than a count | False — it is **113** (70 post + 30 events + 6 canteens + 2 page + 2 shopping + 1 attractions + 1 category + 1 local). Corrected in the same turn, before anything was written to a file. The pattern is now five deep and unchanged in character: a number about a file stated without being counted |
| 2026-08-10 | Claude computed a "syndicated-shape share" of **10.1%** (171 of 1,696) for Scandinavian Standard using a slug-prefix regex | False — the regex matched legitimate slugs beginning `a-`, such as `a-nordic-take-on-a-french-classic`. **Discarded rather than reported.** Replaced with a purely mechanical slug-length test: 133 of 1,696 over 90 characters, zero in the historic 1,000. Same class as the 2026-07-30 issue *a correct-looking formula can assert the wrong thing*, caught this time before it reached the operator |
| 2026-07-30 | Claude asserted `06` §4's `robots_permitted` posture for MICHELIN was wrong, and advised on `10` §2 compliance, on the strength of a bot-detection block — without reading `robots.txt` | False. `guide.michelin.com/robots.txt` grants `ClaudeBot`, `GPTBot`, `ChatGPT-User` and `PetalBot` a group with no `Disallow` directives, and advertises a sitemap. The posture label was correct; the registry's defect was narrower — one column could not express *permitted but unreachable*, now split into Posture and Reach (`06` §1). **Same failure pattern as 2026-07-28: a conclusion about a file's contents inferred from a symptom rather than read.** Both instances are kept here deliberately — this is the error class the operator cannot catch by inspection, and two data points make it a pattern rather than an incident |

---

## Session log

Keep this short — one line each. It's a trail, not a diary.

| Date | What happened |
|---|---|
| 2026-07-28 | Design documentation set created (docs 00–14, schemas) |
| 2026-07-28 | Added operator-profile docs 15–17 + BUILD-STATUS; logged D-011, D-012 |
| 2026-07-28 | The Next Table / Substack defined in doc 18; logged D-013, D-014 |
| 2026-07-28 | Scope gaps closed: hotels = F&B only, technology facet, Google Trends; logged D-015, D-016 |
| 2026-07-28 | Data visualisation standards added as doc 19; logged D-017 |
| 2026-07-28 | Twenty questions completed as doc 20; logged D-018, D-019 |
| 2026-07-28 | Schema read properly; D-020 original-language preservation; docs 00, 11, 12, README, schema.sql updated; one prior Claude error corrected |
| 2026-07-28 | Cities and languages settled: Barcelona confirmed, Danish not read; logged D-021, D-022. Phase 0 unblocked |
| 2026-07-29 | Venue inclusion criteria written as doc 21. Guides verified and registered. Logged D-023–D-026; edited docs 00, 06, 08, 09, 18, README |
| 2026-07-29 | Prediction ledger created (3 hypotheses, 8 scoring clauses). Calibration run on 12 venues; rule amended — F2 three-state, F6 withdrawn, F0 added, ownership defined. Logged D-027–D-029 |
| 2026-07-29 | Route B registry set (`D-030`). Phase 0 rule work complete; enumeration unblocked |
| 2026-07-30 | Copenhagen Route A enumeration attempted, **produced no data**. Michelin unreachable (WAF) though `robots.txt` permits; White Guide client-side rendered. Two rule defects found in Copenhagen's A2 — no dated edition, untested tier scope. `06` posture column split into Posture + Reach; `21` §4 and §12.1 corrected; `D-031` and `D-032` logged; one Claude error logged in Corrections |
| 2026-07-30 | F2 test fixture built on the 21 starred Copenhagen venues (secondary source, **not frame data**). F1 cut 4 of 21. F2 tested on 7: 3 `full`, 4 `price_only`. Operator verified 2 of 2 checkable classifications correct. `D-033`, `D-034` logged. Firecrawl key supplied; API host blocked by egress allowlist |
| 2026-07-30 | **Copenhagen A1 enumerated — 83 candidates, 68 pass F1.** Firecrawl connected via MCP; Michelin retrievable at `proxy: basic`. 72 rows resolved via Places. `D-035` logged (Aotori, operator decision). `06`, `21`, `12` updated; `21` §12.1 items 6 and 7 closed, no hard blockers remain |
| 2026-08-01 | **A1 ∪ A2 union run — Copenhagen's Route A frame is 132** (45 both, 23 A1-only, 64 A2-only). Operator verified Noma absent from MICHELIN and checked both unresolved rows. `D-040`–`D-042` logged. Three count defects found and fixed: decision log 110→109, A2 shipped un-recalculated, ledger tally 7-of-8. F0 amended to identity-only; Places' closed-venue blind spot recorded. `M1` pre-registered. One Claude error logged in Corrections |
| 2026-08-01 | **Union file written — the frame is an artefact.** 132 rows, 8 CHECK rows. A1 got 4 CHECK rows, A2's rebuilt to 3. All 14 A2 `unresolved` rows adjudicated by the operator: 12 outside boundary (5 Faroese), 2 closed — frame unchanged at 132, caveat discharged. `M1` deleted unendorsed. `D-043`–`D-047` logged; `D-042` reversed, `D-035` closed, `D-040`'s interpretation amended. Three Claude errors logged in Corrections |
| 2026-07-30 | **A2 enumerated and resolved — 199 venues, 109 pass F1.** White Guide `robots.txt` absent (permissive); tier reconciliation per `D-037`. `D-036`–`D-039` logged. Operator resolved Anarki (Masters) and Propaganda (one venue). Danish-character matcher bug found and fixed. Union deferred to next session |
| 2026-08-02 | **Route B Stage 0 reconnaissance — no data collected, frame unchanged at 132.** Posture established 5 of 5 Copenhagen titles: 3 `permitted`, 1 `blocked_by_robots` (Copenhagen Post names `ClaudeBot`), 1 `pending_access` (Politiken). AOK found not to be a publication; `06` §4A corrected. MigogKbh empty `robots.txt` operator-verified. Berlingske reach tested — section index and sitemap both fail. Infomedia found renamed to Retriever. `D-048`–`D-052` accepted |
| 2026-08-10 | Berlingske search endpoint supplied by operator after a wrong guess at `/soeg`. Search is real, dated and states 4,289 results for `restaurant` — but `?page=N` is silently ignored and a browser-interaction test to measure recession rate **failed**. Reach still unproven. Two different result sets returned from one URL in one session; cause unknown |
| 2026-08-10 | **Route B Stage 0b — archive reach tested, no data collected, frame unchanged at 132.** `D-051` applied to Scandinavian Standard and MigogKbh. **Scandinavian Standard PASSES on sitemap** — 1,696 posts across 2 files, spans 2014–2026, encloses the window; first Route B title in the project to demonstrate reach. Its `lastmod` proven unusable as a publication date; real dates live in `article:published_time`. Section index fails (real pagination, no served articles). Search closed by robots, untested. 133 of 1,696 slugs over 90 chars, zero historically. **MigogKbh sitemap FAILS — 113 children, newest entry 2026-05-19, ~12 weeks stale**; its section index and search untested. Reach now 1 of 5. `D-053`–`D-055` logged. Two Claude errors logged in Corrections |
| 2026-08-10 | Phase 1 target confirmed at **40 venues** and declared method-development, not cohort (`D-056`). `11-roadmap.md` Phase 0 and Phase 1 venue lines corrected — they described the hand-selection method `D-023` replaced. Phase 1 unblocked; issue #1 due week 3 |
| 2026-08-12 | **Phase 1 collection started — 8 of 30 URLs fetched, stopped deliberately.** 6 `full` / 2 `price_only`, 110 dish rows, 7 of 8 pages English-only (denominator: 8 fetched, of 30 URLs, of 39 rows). Enigma trilingual PDF showed **machine extraction corrupting original-language text** (ÀNEC→ÅNEC, CIRERA→CIIRERA, El→EI) — `D-059` proposed, original-language names must be human-transcribed. akmē's 1500/1300 DKK conflict confirmed live. The Ledbury duplicated every block in extraction (14 vs true 7). Prodigi's supplied URL is a translation path. `D-056` confirmed by operator; `D-057`–`D-060` logged. One Claude claim withdrawn: batch timestamps do **not** disqualify rows from the gold set |
| 2026-08-12 | Phase 1 capture template built (Menus / Dishes / Legend, dropdowns, no formulas). Copenhagen twenty selected from the frame file by documented non-random stratified fill; London and Barcelona tens assembled by web search against registered guides and are **not enumerated** (`D-058`) |
| 2026-09-28 | **GitHub connected — `patokoller/mise`, public. No Phase 1 progress since 2026-08-12; issue #1 not published.** Project knowledge (31 docs, 3 spreadsheets) imported unchanged as commit 1. August recovery as commit 2: found that 2026-08-12's outputs, both Copenhagen frame files and one 2026-08-01 edit never reached the Project. Recovered from transcripts; rebuilt A1 and A2 frames cross-checked against the union file with 0 differences (68 of 68, 109 of 109). `D-057`–`D-060` restored to the log. Operator's 39-row upload unrecoverable. Dish lines held out of the public repo. `D-061` logged |
| 2026-09-28 | **Phase 1 collected; issue #1 drafted. Decisions delegated (`D-062`).** 39 venues re-collected by four parallel runs under one written spec (basic proxy only, clock readings per fetch, no original-language names): 73 menu rows, 771 dish rows; 37 trading, 2 closed per source. Connection's closure reported 2025-01-21 yet listed by White Guide at frame date — logged as `21` §12.1 item 11 and P5. `D-057`/`D-059`/`D-060` accepted; `D-061` master = GitHub; `D-062`–`D-064` logged. Docs fixed: `16` Phase 1 checks, `07` §2 + `menu_item.schema.json` v1.1.0, `21` §12.1 items 9–11. Predictions P1–P5 opened. Issue #1 drafted as a Claude Doc |
| 2026-09-28 | Operator clarified the editorial frame: issues are about trends, with the three cities as evidence for where cooking is heading, not city reports. Logged as `D-065` with guardrails; `09` §3 updated; issue #1 draft reframed (standfirst added, the price-without-menu item now shown in all three cities, Abigail & Co's move cut) |
