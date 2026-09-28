# Re-applies, verbatim, the edit script run in chat fb408a15 (2026-08-12), turn 25,
# to a copy of the 2026-08-10 BUILD-STATUS.md. Only change from the original: path is local.
p='BUILD-STATUS.md'
s=open(p).read()
old_hdr="**Last updated:** 2026-08-10 (Route B Stage 0b — reach)\n**Current phase:** Phase 0 — in progress"
assert old_hdr in s, "header anchor not found"
s=s.replace(old_hdr,
            "**Last updated:** 2026-08-12 (Phase 1 — collection started, partial)\n**Current phase:** Phase 1 — in progress; Phase 0 half-finished, not blocking")

new_block = """
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
"""

anchor = "**Only one of the 3 `not_trading` rows carries an F1 verdict.**"
i = s.index(anchor)
j = s.index("\n", s.index("counted in no F1 line", i))
# insert after that paragraph ends
j = s.index("\n\n", i)
s = s[:j+1] + new_block + s[j+1:]

log_rows = """| 2026-08-12 | **Phase 1 collection started — 8 of 30 URLs fetched, stopped deliberately.** 6 `full` / 2 `price_only`, 110 dish rows, 7 of 8 pages English-only (denominator: 8 fetched, of 30 URLs, of 39 rows). Enigma trilingual PDF showed **machine extraction corrupting original-language text** (ÀNEC→ÅNEC, CIRERA→CIIRERA, El→EI) — `D-059` proposed, original-language names must be human-transcribed. akmē's 1500/1300 DKK conflict confirmed live. The Ledbury duplicated every block in extraction (14 vs true 7). Prodigi's supplied URL is a translation path. `D-056` confirmed by operator; `D-057`–`D-060` logged. One Claude claim withdrawn: batch timestamps do **not** disqualify rows from the gold set |
| 2026-08-12 | Phase 1 capture template built (Menus / Dishes / Legend, dropdowns, no formulas). Copenhagen twenty selected from the frame file by documented non-random stratified fill; London and Barcelona tens assembled by web search against registered guides and are **not enumerated** (`D-058`) |
"""
s = s.rstrip("\n") + "\n" + log_rows
open(p,'w').write(s)
print("ok", len(s))
