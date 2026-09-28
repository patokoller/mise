# Copenhagen Route B — Stage 0 reconnaissance

**Retrieved:** 2026-08-02. **Frame date:** 2026-07-28. **Registry frozen:** 2026-07-29 (`06` §4A, `D-030`).
**Window Route B must cover:** 2024-07-28 → 2026-07-28.

**What this is.** A posture-and-reach record for the five registered Copenhagen titles. No press
items were collected. Only `/robots.txt` was fetched on each host — four by tool, one confirmed by
the operator in a browser — plus two structural checks on Berlingske and one on MigogKbh. Nothing
here is a frame row.

**What this is not.** Archive depth over the 24-month window is **verified for 0 of the 5 titles.**
That test has not been run: one title is dropped on robots, one waits on an operator decision, and
the remaining three are permitted but were not swept, because sweeping them before the two open
questions are settled would build a frame on an unsettled registry.

---

## The five titles

### 1. Politiken — `politiken.dk`
**robots.txt:** retrieved, HTTP 200.
- `User-agent: *` — `Disallow: /search`, `/deadsections`, and two `srsltid` query patterns.
- Site-wide `Disallow: /` for a long list of named AI agents, including **`anthropic-ai`** and
  **`Claude-Web`**, alongside `GPTBot`, `ChatGPT-User`, `CCBot`, `Google-Extended`, `Amazonbot`,
  `Bytespider`, `cohere-ai`, `DeepSeek`, `DeepSeekBot`, `DuckAssistBot`, `YouBot`, `omgili`,
  `omgilibot`, `Timpibot`, `dotbot`.
- `ClaudeBot` is **not** named.
- `Sitemap: https://politiken.dk/sitemaps/sitemap.xml`

**Verdict: BLOCKED PENDING OPERATOR DECISION.** Two Anthropic-operated agents are named with a
site-wide disallow. `ClaudeBot`'s absence from an otherwise comprehensive AI-crawler blocklist is a
gap, not a grant of permission, and reading it as permission is the kind of technicality `10` §2
exists to rule out. Separately, `/search` is disallowed for **every** agent, so the free-text search
route into this archive is closed regardless of how the agent question resolves.

**No Politiken content was fetched.** Only `robots.txt`.

---

### 2. Berlingske / AOK — `berlingske.dk`
**robots.txt:** retrieved, HTTP 200.
- `User-agent: *` — `Disallow: /preview/` only.
- Site-wide `Disallow: /` for `GPTBot` and `CCBot`. No Anthropic agent named.
- `Sitemap: https://www.berlingske.dk/news-sitemap.xml` — a **news** sitemap. News sitemaps
  conventionally carry only the last ~48 hours, so this is not an archive index and cannot by itself
  reach back over the window.

**Verdict: PERMITTED. Reach unverified.**

**Two structural findings, both of which correct the registry:**

- **`aok.dk` is not a live standalone site.** It redirects to `https://www.berlingske.dk/aok`,
  which returns **HTTP 404** ("Siden kunne ikke findes"). Berlingske's own site describes its four
  strength areas as "Nyheder, Opinion, Business og AOK"; an article titled *"Derfor hedder vi AOK"*
  records that Berlingske's culture and lifestyle coverage was **renamed** AOK; and a staff
  biography refers to "byguiden AOK.dk" in the **past tense**. AOK is a desk brand inside
  Berlingske, not a publication.
  **Consequence: Berlingske and AOK are ONE title, not two.** `06` §4A already lists them on one
  row, which is correct — but its note ("AOK is the Copenhagen dining and culture arm") is wrong in
  two ways: the brand is culture-wide, not Copenhagen-specific, and the standalone site is gone.
  If any future pass counts a Berlingske item and an AOK item as two different titles, it breaches
  the two-items-two-titles rule silently.
- **`/gastronomi` is not a section index.** It redirects to a single article dated 31 July 2021.
  The section path is `/kultur/gastronomi`. Pagination depth not yet tested.

---

### 3. MigogKbh — `migogkbh.dk`
**robots.txt: empty. Operator-verified in a browser, 2026-08-02.** My two automated attempts failed
at the fetch layer; the operator opened `https://migogkbh.dk/robots.txt` directly and saw nothing,
and the downloaded file was zero bytes. That is consistent with the tool failures — the extraction
engines had no content to extract — and it resolves them. `/robots.txt` at the host root is the
only location a crawler consults, so there is no other file to look for. The site itself is
reachable and live: a dated guide for August 2026 is present, alongside restaurant and venue
content.

**Verdict: PERMITTED.** A robots file that is empty carries no rules, and a robots file that is
absent is treated the same way. Both states leave the host unrestricted, which means the one thing
still unmeasured here — whether the response was HTTP 200 with a zero-byte body or a 404 — **does
not change the verdict**, and is therefore not worth chasing.

**Two limits on what that verdict licenses.** Permissive is not a volume allowance: `10` §2's rate
limiting, descriptive user agent and contact address all still apply, and a site with no stated
crawl preferences is if anything the case for being conservative rather than less so. And an empty
robots file says nothing about whether the archive is *searchable* over the window, which is
criterion 2 and is still untested here as it is for every other title.

**Precedent, recorded so it is not re-derived each time.** This is the third posture state the
project has met — MICHELIN permitted-but-unreachable (`06` §1, Posture vs Reach), White Guide
absent-therefore-permissive, and now MigogKbh empty-therefore-permissive. Absent and empty land in
the same place. Reachable-but-forbidden (Copenhagen Post, below) is the genuinely different one,
and it is the only state that cannot be worked around.

**Separate concern, precision not posture.** The URLs surfaced alongside the restaurant content
include tax-lawyer advertorial, crochet-pattern guides and workwear copy. This looks like a site
carrying paid SEO filler next to editorial. That is the same class of problem as Barcelona
Secreta's "high recall, low precision" note and should be sized before the title is relied on.

---

### 4. Copenhagen Post — `cphpost.dk`
**robots.txt:** retrieved, HTTP 200.

```
User-agent: ClaudeBot
Disallow: /
```

Explicit, site-wide, by name. Also bans `GPTBot`, `CCBot`, `Applebot`, `Amazonbot`, `PetalBot`,
`Bytespider`, `python-requests`, `bingbot`, `GoogleOther`, `AhrefsBot`, `SemrushBot`, `SeznamBot`,
`YandexBot` and `dotbot`. `Crawl-delay: 5` for Googlebot, `10` for `*`.

**Verdict: DROP.** There is no reading of this that permits retrieval under `10` §2. This is the
title `06` §4A registered to "carry the English requirement."

---

### 5. Scandinavian Standard — `scandinaviastandard.com`
**robots.txt:** retrieved, HTTP 200.
- No AI-agent bans of any kind.
- `User-agent: *` disallows admin, CDN and **search** paths: `/?s=`, `/page/*/?s=`, `/search/`,
  `/wp-admin/`, `/wp-json/`, `/cdn-cgi/`, cart parameters.
- `Sitemap: https://www.scandinaviastandard.com/sitemap_index.xml` — a real sitemap **index**, which
  is the right shape for an archive sweep.

**Verdict: PERMITTED. Reach unverified.** Free-text search is closed; a sitemap sweep is open.
Restaurant-opening density — the thing `06` §4A already flagged for verification — is untested.

---

## Stage 0b — Berlingske archive depth, tested 2026-08-02

**Window that must be reachable:** 2024-07-28 → 2026-07-28.

### Route 1 — the section index. Fails.

`https://www.berlingske.dk/kultur/gastronomi` returns HTTP 200, titled *Gastronomi | Berlingske*.

- **30 distinct `/gastronomi/` article links on initial load.** Counted from the returned link set, not estimated.
- **Zero pagination URLs.** No `?page=`, no `/side/`, no `page/` pattern anywhere in 119 Berlingske links on the page.
- **One `Vis flere` control**, i.e. a JavaScript load-more button. No underlying API or `.json` endpoint exposed in the markup.
- **Zero dates rendered on the index.** I searched the full page text for Danish date patterns and found none.

The last point is the disqualifying one. Even if `Vis flere` is clicked until it stops, the index gives no way to tell how far back you have travelled without opening every article individually to date it. You cannot know when to stop, and you cannot state a denominator.

### Route 2 — the sitemap. Fails.

`https://www.berlingske.dk/news-sitemap.xml` returns HTTP 200. Newest entry `2026-08-02T11:44:41Z`; oldest entry `2026-07-31T12:21:35Z`. **A span of roughly two days.** (I read the first and last entries; I did not count the entries in between.) This is a news sitemap behaving exactly as news sitemaps do. It is not an archive, and `robots.txt` advertises no other sitemap. No `/arkiv` index was linked from the section page.

### Route 3 — on-site search. WORKS. Reach still undemonstrated.

**Correct endpoint: `https://www.berlingske.dk/search?query=` — supplied by the operator, 2026-08-10.**
HTTP 200, titled *Søg | Berlingske*. My earlier `/soeg` guess was simply wrong.

**What it does well.**
- Results are **date-stamped and date-sorted**, newest first. 10 per page.
- It **states a result count** — 4,289 for the single keyword `restaurant`, all sections, all time.
  This is the first stated denominator Route B has had from any source.
- It is **section-agnostic**: page one returned hits under `/gastronomi/`, `/business/`,
  `/internationalt/` and `/danmark/`. This directly confirms finding 1 below, and means search is a
  better instrument than any section sweep.
- Date filters offered: *Alle / I dag / I går / Seneste uge / Seneste år*. **There is no 24-month
  filter**, so the window must be reached by paging under *Alle* and stopping at 2024-07-28.

**The dangerous finding — a silent failure.**
`https://www.berlingske.dk/search?query=restaurant&page=20` returns **HTTP 200 and the byte-identical
first page** — same ten articles, same dates, 8 Aug down to 2 Aug. The `page` parameter is **silently
ignored**. Nothing in the response indicates failure.

A paginator built on `?page=N` would have fetched page one four hundred times, reported success,
inserted ten articles as if they were four thousand, and produced a Route B frame that was wrong by
two orders of magnitude with every CHECK row passing. This is precisely the class of failure the
operator cannot see and the reason `10`-adjacent build rules demand loud failure. **Any paginator
built against this endpoint must assert that the date of the first result on page N+1 is older than
the last result on page N, and halt if it is not.**

Other parameter names — `offset`, `from`, `p`, `start` — were **not** tested. I am not guessing at
more of them; that is what produced the `/soeg` error.

**What remains undemonstrated.** I have not seen a Berlingske result older than **2 August 2026**.
Pagination is the JavaScript *Vis flere* control again, so reach back to 2024-07-28 is not shown.
At 10 results per page, exhausting one keyword's 4,289 results would take roughly 429 activations of
that control.

**Precision is low, by design.** The search matches **body text**, not just headline and lede: page
one included a piece on Russian generals and one on a cement company, both matching because
*restaurant* appears somewhere in the body. Search therefore yields **candidates**; `21` §4's
headline-or-first-paragraph test is applied afterwards, on retrieved text. Search cannot be used to
apply the rule directly.

### Verdict

Berlingske **has** a searchable, dated archive with a stated result count. `06` §4A criterion 2 is
**substantially closer to met but not yet met**, because reach across the full window is
undemonstrated and blocked on pagination rather than on search.

**Next test, bounded:** drive the *Vis flere* control through browser interaction five to ten times.
That establishes three things at once — that the mechanism works under automation, whether older
date stamps carry a year (recent ones show only *8. aug.*), and how many activations buy one month
of recession. The last converts the whole sweep into arithmetic.

**A commitment I did not keep:** I said one fetch after receiving the URL would settle criterion 2.
It took three and did not settle it. The obstacle moved from the endpoint to the pagination
mechanism, which I had not anticipated.

### Route 3, follow-up — browser interaction test, 2026-08-10. FAILED.

Drove the *Vis flere* control through a live browser session to measure how far each activation
recedes in time. **The run failed: exit code 1, "input token count exceeds the maximum allowed."**
The page's accessibility tree outgrew the agent's limit before it could report. 21 credits,
roughly three minutes, no answer to the question asked. Session stopped.

**What the partial payload nonetheless shows.**
- Clicking **does** work. Result dates ran past page one's floor of 2 Aug, reaching **30 Jul**.
  The control extends the list rather than reloading it.
- A date string carrying a **year** (`1. april 2025`) appears in the payload, suggesting older items
  are stamped with years while recent ones show only `8. aug.`. **Not confirmed** — I cannot tell
  whether that string belongs to a search result or to surrounding page furniture.
- **I do not know how many activations completed** before the failure, so no clicks-per-month rate
  can be derived. The arithmetic this test existed to produce does not exist.

**An unexplained discrepancy, recorded because it matters more than the failure.**
The same URL returned **two different result sets** within one session. The scrape returned
date-sorted results led by a Cementgigant piece (8 Aug). The browser session returned a different
set led by five *Byens Bedste 2026* nomination articles. Same query, same day, same host.

I cannot explain it. Candidate causes — result ordering differing between rendered and indexed
retrieval, Firecrawl serving indexed rather than live content on the scrape, personalisation
following cookie acceptance, or an A/B variant — are untested guesses, and I am not recording any
of them as findings. **What is established is only this: Berlingske's search is not yet
demonstrably reproducible, and a route that returns different results on two retrievals cannot
carry a frame until that is understood.** Rule 1 requires a source URL that means something stable.

**Criterion 2 for Berlingske: still not met.** Search exists, is dated, and states a denominator.
Reach across the window is undemonstrated, pagination is JavaScript-only with a silently-ignored
`page` parameter, and retrieval is not yet reproducible.

**Bearing on `D-048`.** Berlingske is the *permitted, unpaywalled, technically easy* Copenhagen
title, and four tests in it still cannot be shown to yield a reproducible dated sweep across 24
months. A licensed archive offers dated filtering, a stated source list, deduplication and
reproducible result sets by construction. The case for the Retriever demo is now materially
stronger than when `D-048` was written, and it rests on evidence rather than convenience.

### Two findings that change the sweep design regardless of how this resolves

**1. Restaurant content is not confined to `/kultur/gastronomi`.** The news sitemap carried a Copenhagen restaurant piece — five new Japanese openings — filed under `/oplevelser/`. The gastronomi index itself links out to `/oplevelser/`, `/metropol/`, `/vores-liv/` and `/kultur/`. **A gastronomi-only sweep would undercount, and would do so invisibly**, because nothing in the section index reveals what it excludes. Any section-based sweep of any title needs its section list established first, empirically, not assumed from the section name.

**2. Berlingske publishes a machine-readable paywall flag.** Sitemap entries carry `news:access`, set to `Subscription` on a substantial share of items. This is directly useful: it would let us **count** what proportion of candidate items sit behind the paywall without fetching any of them, turning the first-paragraph-visibility problem from an unknown into a measured quantity. The share is not yet measured — the two-day sample is far too small and is not restricted to restaurant content.

Denominator throughout is **5 registered Copenhagen titles** (`06` §4A, frozen 2026-07-29).

| | Count | of |
|---|---|---|
| Posture established | 5 | 5 |
| — of which by tool fetch, HTTP 200 with rules | 4 | 5 |
| — of which by operator browser check, empty file | 1 | 5 |
| Cleanly permitted | 3 | 5 |
| Explicitly disallows ClaudeBot by name | 1 | 5 |
| Names other Anthropic agents site-wide, ClaudeBot absent | 1 | 5 |
| Posture undetermined | 0 | 5 |
| Disallows free-text search for all agents | 2 | 5 |
| Archive depth verified across the 24-month window | **0** | 5 |
| Titles whose section-index path was verified | 0 | 5 |

**CHECK — the posture classes must partition the registry.**
3 permitted + 1 ClaudeBot-banned + 1 pending + 0 undetermined = 5. **PASS.**

**CHECK — the two retrieval methods must sum to the titles with an established posture.**
4 by tool + 1 by operator = 5, and posture established = 5. **PASS.**

**CHECK — a title counted as permitted must have a posture actually observed, not inferred.**
Berlingske and Scandinavian Standard: `robots.txt` retrieved HTTP 200, rules read. MigogKbh: file
opened by the operator and found empty. Three observations, three permitted titles. **PASS.**

---

## The thing that must not be decided quietly

**Retrievability is not qualification, and confusing the two changes the frame.**

`06` §4A criterion 2 asks whether a title **has a searchable dated archive**. That is a property of
the publication. Whether *we* are permitted to crawl it is a property of our access. A venue's
Route B status is a fact about what was published about it in the window — it does not change
because a publisher added a line to `robots.txt` on some later date.

Copenhagen Post is now unreachable to us. It was registered on 2026-07-29 against a frame dated
2026-07-28. If we drop it, we are shrinking the frame for a reason that is not a property of the
world, and the shrinkage is invisible to any reader of the published numbers.

Three options, all yours, none mine:

1. **Drop the title and state it.** Route B Copenhagen runs on the titles we can reach; the
   exclusion is recorded as an access limitation with its date, not as a property of the venues.
2. **Keep the title and qualify by hand.** Its archive is readable by a person in a browser. Volume
   unknown — `06` §4A already calls it thin on restaurants, which cuts both ways.
3. **Ask the publisher.** `10` §2's stated fallback. Slow, but it is the only route that converts
   the block into a permission rather than working around it.

---

## What this means for Route B in Copenhagen

**MigogKbh being permitted improves the worst case, and it was the worst case that mattered.**

Worst case is now: Politiken falls to the agent question, and Route B runs on **Berlingske,
MigogKbh and Scandinavian Standard** — three titles, so the two-items-**two-titles** rule has room
to work rather than collapsing into "must be covered by both of the only two." That is the
difference between a thin Route B and an empty one, in the one city where `D-026` says an origin
claim could ever be defended and where Q12's recognition variance has to come from.

It is still thin. Scandinavian Standard is flagged in the registry as thin on restaurants and
untested for density; MigogKbh carries the precision concern above; and neither has had its archive
depth checked. Three permitted titles is a floor for the rule to function, not comfort.

`06` §4A already says Copenhagen is the thinnest registry of the three and that it is "worth one
more Danish title if one exists that meets the four criteria." That line has gone from prudent to
load-bearing.

---

## Next, in order

1. ~~You open `migogkbh.dk/robots.txt`.~~ **Done 2026-08-02 — empty file, title permitted.**
2. You decide the Politiken agent question.
3. You decide the retrievability-versus-qualification question above.
4. Only then do I test archive depth on the three permitted titles — and if the archives will not
   sweep back to 2024-07-28, Route B Copenhagen needs a registry amendment before it needs any code.
