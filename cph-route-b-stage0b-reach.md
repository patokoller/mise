# Copenhagen Route B — Stage 0b: archive reach, MigogKbh and Scandinavian Standard

**Retrieved:** 2026-08-10. **Frame date:** 2026-07-28. **Window Route B must cover:** 2024-07-28 → 2026-07-28.
**Rule applied:** `D-051` — reach demonstrated per title before any sweep is planned. Section index,
sitemap and on-site search tested **separately**.

**What this is.** A reach record for two of the three permitted Copenhagen titles. **No press item
was collected. No frame row was created. The frame is unchanged at 132, F1 only.**

**Retrieval method, recorded for reproducibility.** All fetches via Firecrawl, `proxy: basic`,
**`maxAge: 0` (forced live fetch, no reuse of indexed content)**. `maxAge: 0` was set deliberately
because Firecrawl serving indexed rather than live content was one of the untested candidate causes
of Berlingske's two-result-sets problem on 2026-08-10. Setting it removes that variable from this
session's results. It does not explain Berlingske, which stays unexplained.

**Parsing method.** Both Scandinavian Standard post sitemaps exceeded the context limit and were
written to disk, then parsed **deterministically with `xml.etree`** — no LLM extraction (`D-031`).
Every count below that concerns those files was computed, not read off. Counts concerning the
MigogKbh sitemap index were made by hand from the XML and are labelled as such.

---

## Verdict table

Denominator: **2 titles × 3 routes = 6 route-title cells.**

| | Section index | Sitemap | On-site search |
|---|---|---|---|
| **Scandinavian Standard** | FAIL — listing not in served HTML | **PASS, with a cost** | **NOT TESTED — closed by robots** |
| **MigogKbh** | not tested (budget) | **FAIL — stale by ~12 weeks** | not tested (budget) |

| | Count | of |
|---|---|---|
| Route-title cells tested | 3 | 6 |
| Cells passing | 1 | 6 |
| Cells failing | 2 | 6 |
| Cells closed by robots before testing | 1 | 6 |
| Cells untested for budget | 2 | 6 |

**CHECK — the cell classes must partition the grid.**
1 pass + 2 fail + 1 closed + 2 untested = 6. **PASS.**

**CHECK — a cell marked "closed by robots" must rest on a rule actually read, not inferred.**
Scandinavian Standard `robots.txt`, read 2026-08-02 and recorded in `cph-route-b-stage0-recon.md`,
disallows `/search/`, `/?s=` and `/page/*/?s=` for `User-agent: *`. One rule, one cell. **PASS.**

---

## 1. Scandinavian Standard — REACH DEMONSTRATED, dating is the cost

### Search — closed by robots, not tested
`robots.txt` disallows `/search/` and `/?s=` for all agents. A `/search` URL without the trailing
slash does appear in the site's own link set. **It was not fetched.** Treating a trailing-slash
difference as permission is the same technicality `D-049` exists to rule out. This cell is
`closed_by_robots` — a **posture** fact, not a reach fact. The two columns stay separate (`06` §1).

### Sitemap — PASS
`sitemap_index.xml` is a real Yoast index, **6 children**. Two carry posts.

| file | posts | lastmod range |
|---|---|---|
| `post-sitemap.xml` | 1,000 | 2014-04-28 → 2023-11-08 |
| `post-sitemap2.xml` | 696 | 2023-11-08 → 2026-08-10 |
| **total** | **1,696** | |

**CHECK — the two files must sum to the total.** 1,000 + 696 = 1,696. **PASS.**
**CHECK — every URL unique across both files.** 1,696 unique of 1,696. **PASS.**

The corpus spans 2014 to 2026 and therefore **encloses the window**. The inventory is complete,
finite, static XML, and states its own denominator. That satisfies three of `D-051`'s four
conditions: stopping rule, reproducibility, and reach.

### The trap, demonstrated rather than argued
**`<lastmod>` on this site is not a publication date and must never be used as one.**

The five oldest entries in `post-sitemap2.xml` are articles about *3 Days of Design 2020*,
*Copenhagen Fashion Week SS21* and *CPHDOX 2020* — all stamped `2023-11-08`. A bulk re-save on that
date overwrote modification dates across hundreds of posts.

Verified against a single article: `whats-on-in-copenhagen-july-2024` carries sitemap
`lastmod` **2024-08-01** and page metadata `article:published_time` **2024-06-30**. A 32-day gap on
one article, and several years on the 2020 ones.

**Consequence.** A bucketing of the 696 recent entries by `lastmod` against the window gives
337 before / 175 inside / 184 after. **Those three numbers are not a measure of publication and are
recorded here only so that nobody re-derives them and believes them.**

### Where real dates live
Article pages expose `article:published_time` and `article:modified_time` in metadata —
machine-readable and unambiguous. **Dating therefore costs one fetch per article.**

**This is less bad than it sounds.** `21` §4's headline-or-first-paragraph test already requires
retrieving the article text. The date arrives on the same fetch that the qualification test needs.
Dating is not an additional pass; it is a field on a pass we must make anyway.

### Section index — FAIL
`category-sitemap.xml` gives **15 real categories**. `/denmark`, `/sweden` etc. are **not** among
them, so the obvious guess would have been wrong.

`/category/food-drink/` returns HTTP 200 with the correct `og:title` ("Food & Drink Archives"),
and **`/category/food-drink/page/2/` is a genuine server-side pagination URL** — a better shape than
anything Berlingske offered. But the same fetch, with a 6-second render delay and main-content
filtering off, returned **18 links, none of them an article**. The listing is not in the served HTML.

The route is therefore unusable without browser rendering, which is what failed on token limits last
session. **The pagination being real does not rescue it**: a paginator over content that isn't
served paginates nothing.

**Two findings for sweep design.** The 15 categories are **topical, not geographic** — there is no
Copenhagen or Denmark category, so a `food-drink` sweep mixes five countries. This is `D-051`
finding 1 inverted: the section is too broad rather than too narrow. And the correct category URLs
had to be read out of the category sitemap; assuming them from the site's top-level nav would have
produced four wrong URLs.

### A precision problem, measured
**133 of 1,696 posts (7.8%) carry a URL slug longer than 90 characters.** All 133 sit in the recent
file; the historic 1,000 contain **zero**, longest 88. The longest on the domain is 200 characters.

That is a structural break, not a gradient. By eye on one article page, items of this shape are
headlined as sentence-long psychology and wellness claims, are cross-published on
`siliconcanals.com`, `vegoutmag.com`, `scienceblog.com` and `thelawdictionary.org`, and carry
`utm_campaign=editorial` parameters.

**What is established:** a slug shape absent from the site's first 1,000 posts now accounts for
7.8% of its inventory. **What is not established:** who writes them, or whether they are
machine-generated. I have not tested that and am not asserting it.

**Why it matters anyway.** `06` §4A already flags Scandinavian Standard as thin on restaurants.
Any Route B count of "items published by Scandinavian Standard" now needs a denominator that
distinguishes its editorial output from this. That is a precision problem, not a reach problem,
and it is **not** grounds to touch the registry (`D-052`).

---

## 2. MigogKbh — SITEMAP FAILS ON STALENESS

`sitemap_index.xml` exists and is a real Rank Math index. **113 children**, counted by hand from
the XML: 70 post, 30 events, 6 canteens, 2 page, 2 shopping, 1 attractions, 1 category, 1 local.
70+2+6+2+1+30+1+1 = 113.

**CHECK — the child classes must sum to the index total.** 113. **PASS.**

### The finding
`post-sitemap1.xml` is ordered **newest first**. Its entries run from **2026-05-19** down to
**2026-04-28**. Every one of the 113 children carries an index `lastmod` between **2026-05-06 and
2026-05-13**.

**Retrieved 2026-08-10, the newest item anywhere in this sitemap set is dated 2026-05-19 — roughly
twelve weeks stale.**

The site is live and publishing: `cph-route-b-stage0-recon.md` records a dated August 2026 guide
present on 2026-08-02. So content exists that the sitemap does not list.

**Consequence for the window.** The Route B window runs to 2026-07-28. A sitemap that stops at
2026-05-19 **misses roughly the last ten weeks of the window**, and misses them silently — the XML
is well-formed, the index is large, and nothing in it announces that it stopped.

**I am not guessing the cause.** Candidates — a broken regeneration cron, Rank Math caching, a
CDN serving a stale object, a deliberate configuration — are untested. Per the carry-in rule from
last session, they stay untested guesses and are not recorded as findings. **The observation is the
finding: the file's newest entry is 2026-05-19 as of 2026-08-10.**

### What was not tested
MigogKbh's **section index** and **on-site search** were not tested. The session budget went on
Scandinavian Standard's sitemap, which required two 2 MB payloads and a written parser. Both cells
remain open. Neither can be assumed from the sitemap result — a stale sitemap says nothing about
whether the site's own archive pages or search reach further back.

### What the one file did show, uncounted
`post-sitemap1.xml` contains a visibly high density of Copenhagen restaurant items — venue
openings, closures, Michelin news, and "best of" guides. It also contains consumer-loan, CBD-oil,
credit-card, dog-food, insurance and construction-materials items, which is the paid-SEO-filler
concern `06` §4A already records.

**I did not count either class.** These are impressions from reading one file of 70, and no number
should be attached to them. Sizing the editorial-versus-advertorial split is a separate job with
its own denominator.

---

## What this means for the session question

**The question was whether Copenhagen Route B is runnable from the open web at all.**

**Partial yes, and it is thinner than it looked.**

- **Scandinavian Standard is the first Route B title in this project to demonstrate archive reach
  across the full window.** Complete inventory, stated denominator, reproducible, dates recoverable
  at one fetch per article. It is also the title `06` §4A calls thin on restaurants, and 7.8% of
  its inventory is now of a shape that did not exist in its first 1,000 posts.
- **MigogKbh — the Danish, Copenhagen-specific, restaurant-dense title, the one that actually
  matters — fails on its sitemap and has two routes still untested.**
- **Berlingske remains unproven** after four tests across two prior sessions.

So the reachable-title count for Copenhagen Route B currently stands at **1 of 5 registered, 1 of 3
permitted.** The two-items-**two-titles** rule cannot function on one title. Route B Copenhagen is
not runnable today.

**Bearing on the Retriever question.** `D-048` left adoption of a licensed archive open, and
`cph-route-b-stage0-recon.md` already judged the case "materially stronger" after Berlingske. This
session strengthens it further and from a different direction: the failure modes are now
**three distinct kinds** — a paginator that lies (Berlingske), a date field that lies (Scandinavian
Standard), and an index that silently stops (MigogKbh). Each was invisible on inspection. Each was
found only by testing the specific thing. **Fifteen titles across three cities, each needing three
separate route tests, each capable of failing in a way that looks like success, is the argument.**

It is still your decision, and it is still not made here.

---

## Next, in order

1. Test MigogKbh's **section index** and **on-site search**. Both need real URLs read from the
   site's own navigation, not guessed. This is the highest-value remaining test in Copenhagen,
   because MigogKbh is the title with the restaurant density.
2. Decide Copenhagen Post's disposition (`D-048`, still open).
3. Decide the Politiken agent question (`D-049`, still open).
4. Berlingske's reproducibility problem — its own session, untouched here.
5. Only then: whether Route B Copenhagen needs a registry amendment, which under `D-052` needs a
   new frame date and a re-freeze of all three cities, not a patch.
