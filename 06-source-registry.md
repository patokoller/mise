# 06 — Source Registry

**Status:** Draft v1 — a working template, to be populated during Phase 1
**Last reviewed:** 2026-07-28

---

## 1. How to use this

This document is the human-readable companion to the `sources` table. Every source gets registered before it is crawled, with its access method and legal posture recorded. **No source is crawled that isn't in the registry.** That rule is what keeps `10-legal-and-ethics.md` enforceable rather than aspirational.

**Posture values:**

| Posture | Meaning | Action |
|---|---|---|
| `api_permitted` | Official API, within terms | Automate freely |
| `robots_permitted` | Public page, `robots.txt` allows, ToS not violated | Automate politely |
| `manual_only` | Accessible but automation prohibited or unclear | Read by hand, log observations manually |
| `prohibited` | ToS forbids, or paywalled, or hostile | Do not touch |

When in doubt, `manual_only`. A manually-logged fact is worth the same as an automatically-logged one.

**Reachability values — added 2026-07-30.**

Posture is a *permission* question. Reachability is a *technical* one. They are recorded separately because they have already come apart in practice: MICHELIN's `robots.txt` explicitly permits AI crawlers and its edge bot-detection refuses them anyway. A single column forced those two facts into one cell, and the wrong conclusion was drawn about the source's legal status as a result (see BUILD-STATUS Corrections, 2026-07-30).

| Reach | Meaning | Action |
|---|---|---|
| `direct` | Plain automated request succeeds | Fetch directly |
| `js_rendered` | Content loads client-side; page shell returns without the data | Rendering fetch (Firecrawl, Playwright fallback) |
| `waf_blocked` | `robots.txt` permits, edge bot-detection refuses | **Do not evade.** Retry from other infrastructure in default mode; if still blocked, ask the publisher. Never stealth mode or rotating proxies — `10` §2 |
| `untested` | Not attempted at this frame date | Test before relying on it |

**A `waf_blocked` source is not `prohibited`.** The distinction matters and must not be collapsed: `prohibited` means the publisher has said no, `waf_blocked` means the publisher's security layer is running ahead of the publisher's stated policy. The response to the first is to stop; the response to the second is to ask.

---

## 2. Source classes

### Class A — Venue primary sources
The backbone. Menus, about pages, booking pages.

- **Access:** venue's own website; almost always `robots_permitted`
- **Frequency:** monthly
- **Yield:** menus, prices, service model, opening hours, seat counts, sustainability claims
- **Note:** the single highest-value class. A venue's own menu is the most reliable statement of what it serves.

### Class B — Reservation and listing platforms
- **Access:** varies widely; most prohibit scraping. Check each individually. Many offer partner APIs.
- **Posture:** default `manual_only` until an API is confirmed
- **Yield:** opening hours, booking availability patterns (a genuine demand proxy), seating configuration

### Class C — Guides and awards
Michelin, World's 50 Best, national guides, city guides.

- **Access:** published lists, usually public pages
- **Frequency:** on announcement, plus quarterly sweep
- **Yield:** the cleanest event data in the whole system — dated, structured, unambiguous
- **Reachability caveat (2026-07-30):** guide publishers are the class most likely to be `robots_permitted` and `waf_blocked` at the same time — public by policy, defended at the edge, and commercially motivated to be both. Test reachability separately from posture for every Class C source, and record the test date. Class C is also where a silent partial fetch does the most damage, because these lists *are* the frame (`21` §4).
- **Note:** guide *changes* are more informative than guide *contents*. A star gained or lost is an event; a star held is background.

### Class D — Trade and consumer press
- **Access:** RSS where available; check paywall terms carefully
- **Frequency:** daily
- **Yield:** openings, closings, chef moves, funding, expansion
- **Warning:** press is systematically biased toward openings and away from closings. Closings are underreported by a wide margin, which will distort survival analysis unless corrected with registry data (Class F).

### Class E — Mapping and place data
- **Access:** Google Places API — official, paid, terms-compliant. Note that Google's terms restrict long-term storage of certain fields; store the Place ID as an identifier and re-fetch volatile fields rather than caching them indefinitely.
- **Frequency:** monthly for tracked venues
- **Yield:** existence confirmation, permanent-closure flags, address, coordinates, the stable `google_place_id` that makes entity resolution tractable

### Class F — Company registries
Companies House (UK), CVR (Denmark), Registro Mercantil (Spain).

- **Access:** official open data; UK and Danish registries are genuinely open and well documented
- **Frequency:** quarterly
- **Yield:** incorporation, dissolution, directors, filed accounts, ownership structure
- **Note:** this is where unit economics becomes accessible without relationships. It is also the only reliable source for closures, and therefore essential to Class D's blind spot.

### Class G — Search demand
Google Trends.

- **Access:** official API. Legitimate, free, terms-compliant — this is the one consumer-demand signal available without touching a platform that prohibits collection.
- **Frequency:** monthly
- **Yield:** relative search interest for cuisines, formats, dishes, and named venues, by city and over time
- **How to use it:** as a *demand-side check on a supply-side signal*. If menus in Barcelona start featuring something and search interest for it rises in the same period, that's two independent sources agreeing. If menus move and search doesn't, that's a restaurant-led trend rather than a consumer-led one — a genuinely useful distinction that almost nobody makes.
- **Handle carefully:** Trends returns *relative* interest, normalised to its own range, not absolute volume. It cannot be compared across terms without care, and a rising line does not mean many people. Never publish a Trends figure as a count.

### Class H — Human observation
You, in a restaurant, with a phone.

- **Access:** yours
- **Frequency:** whenever you eat out
- **Yield:** menus, room design, service model, covers, plating, the design facet generally
- **Note:** the proprietary layer. Nobody else has it. Treat it as a first-class source, not a supplement.

### Class I — Long-form and interviews
Podcasts, chef interviews, trade features, conference talks.

- **Access:** varies; transcripts where legitimately available
- **Frequency:** weekly sweep
- **Yield:** stated intentions, relationships, influences, career moves. Feeds the semantic layer and relationship graph rather than counts.

---

## 3. Explicitly excluded

**Instagram, TikTok, Facebook.** Automated collection breaches their terms, they are technically hostile, and the legal exposure is real. Manual observation of public accounts is fine and can be logged as human observation — automated collection is not. The signal loss is smaller than it looks: menus are more reliable indicators than posts.

**Review platforms, in bulk.** Most prohibit scraping. Reviews are also weak evidence — they measure customer sentiment, not what the restaurant is doing, and they are heavily gamed. Thematic reading of a small manual sample is worth more than a scraped corpus.

**Paywalled trade publications, scraped.** Subscribe and read like everyone else. Log observations manually.

---

## 4. Per-city working list

To be populated in Phase 1. For each city, target roughly 8–12 non-venue sources — enough for coverage, few enough to maintain.

### Copenhagen
| Source | Class | Language | Posture | Reach | Frequency | Status |
|---|---|---|---|---|---|---|
| Venue websites (~60) | A | DA/EN | robots_permitted | untested | monthly | ☐ |
| MICHELIN Guide Nordic Countries 2026 — **Route A1** | C | EN | robots_permitted ☑ 2026-07-30 | `direct` via Firecrawl ☑ 2026-07-30 | on announcement | ☑ **Enumerated 2026-07-30, 83 venues** |
| White Guide Denmark — **Route A2** | C | DA/EN | no_robots_txt ☑ 2026-07-30 | `js_rendered` ☑ 2026-07-30 | **continuous — weekly reviews** | ☑ **Enumerated 2026-07-30, 199 venues** |
| Danish restaurant press | D | DA | check each | untested | daily | ☐ |
| CVR company registry | F | DA | api_permitted | untested | quarterly | ☐ |
| Google Places | E | — | api_permitted | `direct` | monthly | ☐ |
| Nordic food media | D/I | EN/DA | check each | untested | weekly | ☐ |
| Google Trends (DK) | G | — | api_permitted | untested | monthly | ☐ |

**Two corrections to this table, both 2026-07-30:**

- **RESOLVED 2026-07-30 — MICHELIN is retrievable.** Firecrawl (MCP connector) reaches `guide.michelin.com` where direct fetch is refused. HTTP 200 on both Copenhagen listing pages with `proxy: basic` — **no stealth mode, no proxy rotation**, so `10` §2 is satisfied and the `waf_blocked` state never had to be circumvented, only routed around. Reproducible method: `firecrawl_map` on the domain to find the canonical listing path, then `firecrawl_scrape` with `formats: ["markdown"]`, `onlyMainContent: true`, `proxy: basic`, `maxAge: 0` per page. **Do not use `formats: ["links"]` for enumeration** — it returns sidebar and recommendation links indistinguishable from listing entries.
- **MICHELIN posture verified, reachability was not.** `guide.michelin.com/robots.txt` names `ClaudeBot`, `GPTBot`, `ChatGPT-User` and `PetalBot` in a group carrying only `Crawl-delay: 0.1` and no `Disallow` directives — unrestricted access, and because that group is more specific than `User-agent: *`, those agents do not inherit the wildcard group's rules. The wildcard disallows are faceted-navigation hygiene (sort, region, `lat`/`lon`/`radius`/`boundingBox`, `showMap`, `/search?`, `/book`, `/account`, parameterised `restaurantlist?`). **The canonical listing path and individual restaurant pages are not disallowed, and a sitemap is advertised at `https://guide.michelin.com/sitemap.xml`.** Three URLs on that host — the Copenhagen restaurant index, the Bib Gourmand page, and the sitemap itself — were refused by edge bot-detection on 2026-07-30. Permitted, unreachable from the infrastructure tested. Untested from Firecrawl.
- **White Guide Denmark is not annual.** It publishes new reviews weekly and has no dated edition. The previous `annual` entry was wrong and is load-bearing — see `21` §4 and §12.1, item 6.

**White Guide posture resolved 2026-07-30.** `whiteguide.com/robots.txt` returns 404 — the file does not exist. Under RFC 9309 an absent `robots.txt` imposes no restrictions, and every page carries `robots: index,follow`. Recorded as `no_robots_txt`, which is permissive but is *not* the same as an explicit grant: if the file ever appears, posture must be re-read before the next crawl.

**Retrieval method (reproducible).** Listing URL `https://whiteguide.com/dk/da/search?query=&type=restaurant&execute=true`. The `query` parameter is the live one; `value`, which the site's own "advanced search" link uses, is dead. **Neither filters by location** — the unfiltered list is returned regardless, covering Denmark, the Faroe Islands and one Swedish entry. Copenhagen must be cut by resolved address. Classification filtering exists but is **client-side only and does not alter the URL**, so tier views have no citable address and must be reached through a browser session, not a link.

**Superseded note (kept):** `whiteguide.com/robots.txt` has not been read. The site's page-level meta tags say `index,follow`, which is not the same thing and must not be treated as clearance. Read the file before the first crawl.

### Barcelona
| Source | Class | Language | Posture | Reach | Frequency | Status |
|---|---|---|---|---|---|---|
| Venue websites (~70) | A | ES/CA/EN | robots_permitted | untested | monthly | ☐ |
| MICHELIN Guide Spain 2026 — **Route A1** | C | ES/EN | robots_permitted ☑ 2026-07-30 | `waf_blocked` — inferred, same host | on announcement | ☐ |
| Guía Repsol — Soles only, **Route A2** | C | ES | robots_permitted | untested | annual (Feb) | ☐ |
| Catalan & Spanish food press | D | ES/CA | check each | untested | daily | ☐ |
| Registro Mercantil | F | ES | check access | untested | quarterly | ☐ |
| Google Places | E | — | api_permitted | `direct` | monthly | ☐ |
| Google Trends (ES) | G | — | api_permitted | untested | monthly | ☐ |

**On the MICHELIN row:** `guide.michelin.com` is one host serving all three cities, so the 2026-07-30 finding applies here by inference, not by separate test. Confirm at enumeration rather than assuming.

**Note:** Catalan-language sources are the least-contested material available to this project. If you read Catalan even partially, weight this city heavily.

**Guía Repsol scope, recorded because it changes:** Route A2 includes **Soles only** (1, 2 and 3). The second tier — 1,605 entries nationally, renamed from *Recomendados* to *Restaurantes Guía Repsol* in the 2026 edition — is excluded, because it would make Barcelona's frame several times the size of the other two. The rename is logged in `12-decision-log.md` as a source-definition change, since it is exactly the kind of thing later mistaken for a real-world shift.

### London
| Source | Class | Language | Posture | Reach | Frequency | Status |
|---|---|---|---|---|---|---|
| Venue websites (~90) | A | EN | robots_permitted | untested | monthly | ☐ |
| MICHELIN Guide Great Britain & Ireland 2026 — **Route A1** | C | EN | robots_permitted ☑ 2026-07-30 | `waf_blocked` — inferred, same host | on announcement | ☑ 9 Feb 2026, Dublin |
| Harden's Top 100 UK — London entries, **Route A2** | C | EN | check | untested | annual | ☐ |
| UK restaurant trade press | D | EN | check each | untested | daily | ☐ |
| Companies House | F | EN | api_permitted | untested | quarterly | ☐ |
| Google Places | E | — | api_permitted | `direct` | monthly | ☐ |
| London food media | D | EN | check each | untested | daily | ☐ |
| Google Trends (UK) | G | — | api_permitted | untested | monthly | ☐ |

**Harden's scope, recorded because it is narrow:** Route A2 for London is the **Top 100 UK list only** (London entries), which is published freely and annually. The full Harden's London guide — roughly 1,700 entries spanning pubs, cafés and street food — is excluded on segment grounds and because the complete listing is a commercial product. London's frame therefore leans harder on Route B than the other two cities do. Stated, not hidden.

**Companies House is the standout.** Free API, structured, filed accounts for anything above the smallest thresholds. For London venues this makes real unit-economics analysis possible without knowing a single person in the industry.

---


---

## 4A. Route B publication registry — set 2026-07-29 (`D-030`)

**Frozen.** Improved or cheaper access to a title — a licensed archive, a granted permission, a newly found search endpoint — is **not** grounds to add one (`D-052`). Adding a title later shifts the frame and creates a false signal; `08-trend-detection.md` §5 treats source addition as the null hypothesis for anything spiking at the same time. Changes require a change-log entry.

### Registration criteria

A title qualifies only if all four hold:

1. **Produces dated news items about venues**, not evergreen recommendation guides. *(The Infatuation was considered and excluded on this basis — editorially strong, but its output is standing recommendations rather than timely reporting, and Route B's headline-or-first-paragraph test needs dated news.)*
2. **Has a searchable, dated archive.** **Registration does not establish this (`D-051`).** Reach across the full 24-month window is demonstrated per title before any sweep is planned against it, and section index, sitemap and on-site search are tested **separately** — a title can pass on one and fail the others. The default is that an archive is *not* sweepable until shown otherwise.
3. **Is live** — has published within the trailing 24 months. Re-checked at each quarterly refresh. *(Eater London was proposed and removed: shut down February 2023, no output inside the window.)*
4. **Is a publication, not an award list or directory.** Guides and rankings belong in Route A. Mixing them into B collapses the recognition-versus-attention distinction that Q12 depends on.

### Barcelona

| Publication | Class | Notes |
|---|---|---|
| Time Out Barcelona | City guide | Publishes in Catalan and Spanish |
| Barcelona Secreta | City guide | **High recall, low precision** — covers nearly every opening. Will inflate the B-only stratum |
| Bon Viveur | Consumer food | |
| La Vanguardia | General news | |
| El País | General news | |
| CN Traveller Spain | Tourism | **Tourist-facing skew** — bears directly on the Barcelona half of H3 |
| EFE Agro | Wire | Syndicated copy — see wire rule below |
| *Catalan-language daily — to be named* | General news | **GAP.** See below |
| *Spanish hospitality trade title — to be named* | Trade | **GAP.** See below |

### London

| Publication | Class | Notes |
|---|---|---|
| Hot Dinners | City guide | Strongest London opening coverage; dated and searchable |
| Time Out London | City guide | |
| The Standard | General news | |
| Financial Times | General news | Paywalled; archive searchable |
| CODE Hospitality | Trade | Paid newsletter — **archive searchability to verify at enumeration** |
| The Caterer | Trade | |
| Restaurant (restaurantonline.co.uk) | Trade | |

**Removed:** Eater London (dead since Feb 2023). Bloomberg (near-zero coverage with a venue as headline subject; high effort, low yield).

**Note the class mix.** London carries three trade titles; Barcelona currently carries none. Trade press covers operators and groups, so **London's Route B will catch group and operator news that Barcelona's will not** — which inflates London's large-group share (the risk logged in `D-024`) and damages Q8 and Q18 comparability. Stated, and unfixed until Barcelona gets a trade title.

### Copenhagen

| Publication | Class | Language | Access status (observed) | Notes |
|---|---|---|---|---|
| Politiken | General news | DA | `pending_access` (2026-08-02) | Strong food desk. `robots.txt` names `anthropic-ai` and `Claude-Web` site-wide among sixteen AI agents; `ClaudeBot` absent. `/search` disallowed for all agents. See `D-049` |
| Berlingske (incl. AOK) | General news | DA | `permitted` (2026-08-02) | **AOK is Berlingske's culture and lifestyle brand, not a separate publication and not Copenhagen-specific.** `aok.dk` redirects to `berlingske.dk/aok`, which returns HTTP 404. **Counts as ONE title.** Search at `/search?query=`; reach unproven, see `D-051` |
| MigogKbh | City guide | DA | `permitted` (2026-08-02) | `robots.txt` empty (operator-verified). Carries paid SEO filler alongside editorial — precision to be sized before reliance |
| Copenhagen Post | General news | EN | `blocked_by_robots` (2026-08-02) | Thin on restaurants; carries the English requirement. `robots.txt` contains `User-agent: ClaudeBot / Disallow: /`. Retained in the registry per `D-048`; disposition open |
| Scandinavian Standard | Consumer lifestyle | EN | `permitted` (2026-08-02) | Thin; verify restaurant-opening density at enumeration. Search paths disallowed; sitemap index available |

**Removed:** 50 Best Discovery (a directory, not a publication — criterion 4). Euroman (men's lifestyle; restaurant-opening density too low to justify the check — reinstate if enumeration shows otherwise).

**Copenhagen is the thinnest registry of the three, and it is the census city.** Five usable titles against seven for London. If Route B under-delivers anywhere it will be here, and Copenhagen is the only city where an origin claim will ever be defensible (`D-026`). Worth one more Danish title if one exists that meets the four criteria.

**Language dependency, recorded rather than declared.** The Copenhagen registry deliberately mixes Danish and English titles; Danish sources are translated at collection (`D-022`). Rather than stating this as a caveat, **`source_language` is recorded per citation**, so the dependency is countable — "62% of Copenhagen's Route B qualifications came from translated sources" is a measurable fact, a bare caveat is not. Same principle as `D-025`.

### Two counting rules

**Two items, two different publications.** Doc 21 originally required two items from registered publications. That permitted an opening announcement and a later review in the same outlet. One outlet noticing is not attention. **The two items must come from at least two different registered titles.**

**Wire copy counts once.** A syndicated item republished across multiple outlets is one item, attributed to the originating agency. Without this, EFE copy alone could manufacture a qualification.

**The wire rule applies to any agency, registered or not (`D-050`).** Agency copy counts once regardless of whether the agency is itself a registered title. Covers **Ritzau** (DK), EFE / EFE Agro (ES), PA Media and Reuters (UK). Ritzau is not registered but syndicates into both Politiken and Berlingske; without this, one Ritzau item republished twice would manufacture a two-items-two-titles qualification out of a single act of journalism. **Agency attribution is captured as a field at extraction and is not discarded** — the rule is unenforceable if the byline is thrown away.

### Two open gaps

**Barcelona has no Catalan-language title**, and `06` §4 states that Catalan-language sources are the least-contested material available to this project. The current Barcelona registry is Spanish and English only, which forfeits the project's own stated advantage in its own strongest city. Candidates to check: *Ara*, *VilaWeb*. Operator decision — these need someone who can judge their restaurant coverage.

**Barcelona has no trade title.** See the class-mix note above.

---

## 5. Venue selection

**Superseded 2026-07-29.** The criteria that stood here — independent or small group, ambitious end, has a menu or is reachable in person, in one of the three cities — were not mechanical. "Ambitious end" and the hotel test ("would someone not staying there go specifically to eat?") are judgement calls, and two people applying them produce two different lists. That is selection bias with a rule written on top of it.

**The rule now lives in `21-venue-inclusion-criteria.md`** (`D-023`). Summary only, so this file stays a source document rather than a second copy that drifts:

- **Frame date 2026-07-28**, frozen. Every test evaluated as of that date.
- **Six hard filters** — city boundary, published priced menu, trading, publicly accessible, hotel F&B structurally separable. No ownership-size filter (`D-024`; ownership scale is a recorded attribute, because Q18 needs the concentrators in the frame).
- **Three qualifying routes**, at least one required — A1 Michelin (all three cities, the comparability spine), A2 one named national guide per city, B two dated press mentions from the registered publication list in §4.
- **The frame is enumerated in full and not collected from.** The cohort — 20 per city — is drawn from it by seeded stratified random sample, seed `20260728`, strata on route only, **no redraws**.

**Amended 2026-07-29 after calibration** (`D-027`, `D-028`, `D-029`): F2 now records three publication states rather than passing or failing, and accepts booking-platform pages where the venue sets the price; the structural hotel test is withdrawn and hotel F&B qualifies on routes like anything else; an F0 entity-resolution step precedes every filter.

**Two things this file is responsible for.**

**First, the publication registry for Route B is §4 of this document — and it does not yet exist.** §4 currently names *categories* of press per city, not publications. Calibration on twelve venues could not apply Route B once. Until 5–10 titles per city are named here, the Route-B-only stratum is empty, the 12/8 cohort split collapses, Q12 has no recognition variance, and venues below guide level generate no exclusion rows. **This blocks frame enumeration.** Once named, the list is frozen. Adding a publication after the frame date changes what qualifies. Every addition needs a change-log entry in `12-decision-log.md`, because `08-trend-detection.md` §5 treats source addition as the null hypothesis for any coincident signal.

**Second, the guides in Route A are sources and are registered here** (see §4 tables). Michelin edition vintages differ by city and must be recorded at enumeration.

**Coverage target and its meaning:**

| City | Frame | Cohort target | Coverage claim |
|---|---|---|---|
| Copenhagen | enumerate in full | 60 | Near-exhaustive *for the frame*, which is not the same as for the city |
| Barcelona | enumerate in full | 70 | Substantial but not exhaustive |
| London | enumerate in full | 90 | Representative sample, explicitly not exhaustive |

**Publish the coverage claim with every count, in two sentences.** "17 of the 60 Copenhagen venues we track" is honest about the cohort. It is not honest about the frame, because the frame is bounded by guide and press attention and the population below both is unmeasured — see `21-venue-inclusion-criteria.md` §5. Both sentences, every time.

**Growing the list:** the rule has a refresh procedure, not an inbox. The frame is re-run quarterly at a new frozen date; additions enter as a dated cohort with `entities.first_seen_at` set. Nothing is added mid-quarter. If you add 20 vegetable-forward venues in March, every vegetable tag spikes in March — an artifact, not a trend — and `08-trend-detection.md` §5 can only correct that if the addition date exists.

**Record why each venue was added.** With a mechanical rule the answer is now short and checkable: which filter it passed and which route qualified it. `entities.notes` gets that line, not an impression.
