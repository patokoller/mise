### D-056 · addendum · 2026-08-12 · **Confirmed by the operator**

`D-056` was written on instruction but never endorsed. The operator confirmed it on 2026-08-12:
the Phase 1 forty are method-development venues, not the seeded cohort. No change to the entry.

---

### D-057 · 2026-08-12 · How `observed_at` is set for a menu · **Proposed** — awaiting operator

**Decision:** `retrieved_at` is the clock reading at the moment the page was loaded, always present.
`observed_at` takes the first available of:

1. a date **printed on the menu artefact itself**;
2. a published-or-updated date **exposed by the page**;
3. failing both, `observed_at = retrieved_at`.

A field `observed_at_source` records which applied — `menu_artefact` / `page_published_date` /
`retrieval` — and is mandatory. Without it nobody can later distinguish a venue-dated menu from one
dated by the act of looking at it.

**Excluded outright as date sources:** PDF internal metadata, InDesign or export filenames, HTTP
`Last-Modified`, upload paths, and anything sitemap-derived. Same failure class as `D-053` — a
re-save stamp is not an observation.

**Never inferred.** "This looks like the winter menu" is not a date. Undated is undated.

**Evidence from the 2026-08-12 fetch (8 pages, of 30 URLs supplied, of 39 venue rows):**

- **Bobe** — PDF internal title `Bobe menu 073126.indd`. Excluded correctly.
- **Enigma** — the artefact prints "VERSIÓN VERANO 77. 2026". This is a **version and a season, not a
  date**, and category 1 as drafted does not cover it. Meanwhile the filename says *abril*, the
  content says summer, and the upload path says July — **three signals disagreeing on one artefact**,
  which is the strongest available argument for the exclusion list.
- **Prodigi** — the page exposes `og:updated_time = 2026-05-28T00:57:53+01:00`. Category 2 as
  drafted would make this the first row where `observed_at ≠ retrieved_at`. But WordPress/Divi
  stamps this on **any** page edit, including a typo fix, so it dates the page and not the menu.

**Two sub-questions this leaves open, and they need the operator, not Claude:**

- **(a)** Does a printed version/season string set `observed_at`, or only populate
  `menu_date_stated` while `observed_at` falls through to retrieval? Claude's recommendation:
  the latter — a season is not a date.
- **(b)** Is `og:updated_time` (and equivalent CMS auto-stamps) admissible under category 2, or does
  category 2 mean only a date the venue authored and displayed to a reader?
  Claude's recommendation: the latter, i.e. exclude CMS auto-stamps, on the same reasoning that
  excludes `Last-Modified`. This would leave Prodigi at `observed_at = retrieval`.

**Reverses if:** a material share of menus turn out to carry venue-authored page dates that
demonstrably track menu changes, making category 2 worth the ambiguity it introduces.

---

### D-058 · 2026-08-12 · Phase 1 city split is 20 / 10 / 10 · **Accepted** — operator decision

**Decision:** the Phase 1 forty split **20 Copenhagen, 10 London, 10 Barcelona**.

**Reasoning:** Copenhagen is the only city with an enumerated Route A frame, so its twenty could be
drawn from real rows with `google_place_id`s and reconciled tiers. Q7 (menu publication language)
also needs Copenhagen volume to be worth measuring. But a schema discovered on one currency and one
language pair would break on contact with Barcelona, so London and Barcelona are represented from
the start rather than added later.

**Stated asymmetry, which must travel with any Phase 1 output:** the Copenhagen twenty were selected
from the 132-venue frame file by a **documented, non-random, fixed-order stratified fill** across
guide tiers — deliberately not a random draw, so that it can never be mistaken for the `D-023`
cohort draw. Within each stratum, rows were taken in the file's own (alphabetical) order; that bias
is visible and is judged harmless for schema discovery. The London and Barcelona tens were assembled
by **web search against the registered A1/A2 guides**, are **not enumerated**, not resolved to
place IDs, and not F1-filtered. They are usable only because `D-056` means nothing published from
them carries a denominator.

**Reverses if:** London or Barcelona enumeration completes before Phase 1 collection ends, in which
case those tens are re-drawn from the real frames.

---

### D-059 · 2026-08-12 · `dish_name_original` may not come from automated extraction · **Proposed** — awaiting operator

**Decision:** original-language dish and section names are **transcribed by a human from the
artefact**. Machine extraction may populate prices, structure, section order, format and service
notes, but not `dish_name_original`, `section_name_original`, or `description_original`. A field
`name_original_transcription` records `human` or `machine_unverified`; no row marked
`machine_unverified` is eligible for the Phase 2 gold set.

**Evidence — Enigma trilingual PDF, retrieved 2026-08-12.** Three corruptions caught in the
original-language text of a single artefact:

| Published | Extracted | Failure |
|---|---|---|
| ÀNEC (ca) | ÅNEC | wrong diacritic |
| CIRERA (ca) | CIIRERA | doubled letter |
| El PATO (es) | EI PATO | lowercase L read as capital I |

Three were caught. The number not caught is unknown and unknowable without the artefact.

**Reasoning:** `D-020` makes original-language preservation the one Phase 1 habit that cannot be
recovered later. The corruption is **silent and survives review** — "ÅNEC" reads as a plausible
Catalan word to anyone who does not read Catalan, and `D-022` establishes that nobody on this
project reads Danish. An error class that is both unrecoverable and invisible to the only available
check cannot be accepted on volume grounds.

**Carried with it:** this is a real cost. It means the Copenhagen and Barcelona originals need
operator time on the artefacts themselves. It does **not** block price, structure or F2 work, which
extract reliably — so the two passes can be separated and the expensive one confined to the venues
where an original-language menu actually exists.

**Related, same session:** **The Ledbury** rendered every content block **twice** in extraction
(tabbed panels). A naive dish count returns 14; the true count is 7. Deduplicated by hand. This is
the counting-in-code failure mode in a new place — the code would have been correct and the input
doubled.

**Reverses if:** an extraction path is demonstrated to preserve diacritics exactly across a test set
of Danish, Catalan and Spanish artefacts, with the test designed before the run and the failures
counted.

---

### D-060 · 2026-08-12 · Retrieval timestamps carry a precision field · **Proposed** — awaiting operator

**Decision:** `retrieved_at` is accompanied by `retrieved_at_precision`, one of `exact` or
`batch_approximate`, and by `collected_by`. A batch window is recorded as what it is rather than
being presented as per-page precision.

**Origin:** the operator's 2026-08-12 source file carried one timestamp — `12 Aug 2026, ~11:30
CEST` — on all 39 rows across three cities. The operator confirmed the pages were opened personally
and that the window is real. The defect was never the time; it was the file presenting a batch
window as though it were 39 per-page events.

**Consequence, and a correction to a Claude claim made earlier the same session:** Claude asserted
that batch timestamps would make these rows permanently ineligible for the Phase 2 gold set. **That
was wrong and is withdrawn.** Gold-set eligibility depends on who transcribed the content and from
what, not on timestamp granularity. The eligibility constraint that *does* apply is `D-059`.

**Reverses if:** a use is found that requires per-page retrieval precision, in which case affected
rows are re-collected rather than re-dated — `retrieved_at` is never backfilled.
