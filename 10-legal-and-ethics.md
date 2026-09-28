# 10 — Legal and Ethics

**Status:** Draft v1
**Last reviewed:** 2026-07-28

**This is not legal advice.** It's an operating policy designed to keep the project well inside defensible territory without a lawyer. If the project starts generating revenue or a source objects, get actual advice. The Swiss/EU position (FADP and GDPR both plausibly in scope) is worth a single paid hour of a specialist's time before any commercial launch.

---

## 1. Posture

Conservative by default, for a practical reason as much as an ethical one: this project's value is a long-lived archive. Anything that risks having to delete data, or that would embarrass you if published, is a bad trade against a two-year asset. Being politely boring is strategically correct here.

---

## 2. Collection rules

**Always:**
- Respect `robots.txt`
- Identify with a descriptive user agent and a real contact address
- Rate limit — roughly one request per source every few seconds, never parallel bursts against one host
- Cache aggressively; never re-fetch what hasn't changed
- Honour any request to stop, immediately and without argument

**Never:**
- Bypass paywalls, logins, or technical access controls
- Scrape platforms whose terms prohibit it, regardless of technical feasibility
- Use residential proxies or rotate identity to evade rate limits or blocks
- Collect at a volume that could degrade a small restaurant's site

**The user agent should say what you are.** Something like `MISE-research-bot/1.0 (hospitality research; contact: you@example.com)`. This converts a potential complaint into an email, which is the outcome you want.

---

## 3. Platform-specific

| Platform | Position |
|---|---|
| Venue's own website | Collect. Public, low volume, no prohibition in practice. |
| Google Places | Use the official API. Note that Google's terms restrict indefinite caching of certain fields — store the Place ID as a stable identifier, re-fetch volatile data rather than warehousing it. |
| Michelin, 50 Best, guides | Published lists on public pages. Collect factual data (which venue, what award, what date). Do not reproduce descriptive text. |
| Companies House, CVR, Registro Mercantil | Official open data. Collect freely; that's what it's for. |
| Instagram, TikTok, Facebook | **No automated collection.** Terms prohibit it, enforcement is real, and the legal exposure is disproportionate to the signal. Manual observation of public accounts is fine and can be logged as human observation. |
| Reservation platforms | Default to no, unless a partner API exists. Most terms explicitly prohibit scraping. |
| Review platforms | No bulk collection. Manual reading of a small sample is fine. |
| Paywalled trade press | Subscribe. Read. Log facts manually. Do not scrape, do not reproduce. |

---

## 4. Personal data

Chefs and restaurateurs acting in a professional capacity are a legitimate subject of factual reporting, but GDPR/FADP still apply to the personal data you hold.

**Collect:** name, professional role, career history, public statements, verifiable professional relationships.

**Do not collect:** home address, personal phone or email, family details, health information, anything about their private life, anything about a person who isn't a public professional figure.

**Practical obligations:**
- Have a privacy notice on the site before publishing anything, even at zero subscribers
- State the lawful basis — legitimate interest for professional/journalistic factual reporting is the workable route
- Be able to correct or delete a person's data on request. Build a way to find every fact about an entity now, while it's easy
- Never publish a personal detail that isn't relevant to the professional analysis
- Newsletter subscriber data: standard consent, easy unsubscribe, no selling, no sharing

**The deletion capability matters more than it seems.** If someone asks you to remove their data in month twenty, a system that can't locate everything about an entity becomes a genuine problem. `entity_id` linkage on every fact solves this — which is another reason for the entity discipline in `01-data-architecture.md`.

---

## 5. Copyright

**Facts are not copyrightable. Expression is.**

- ✅ "This venue's tasting menu costs 2,800 DKK as of March 2026" — a fact
- ✅ "The dish is described as cauliflower with fermented elderflower" — a short factual description
- ✅ Structured extraction: ingredients, techniques, prices, dates
- ✅ Aggregated counts and analysis across many sources
- ❌ Reproducing a menu in full as published
- ❌ Reproducing an article's text, or a close paraphrase that tracks its structure
- ❌ Republishing photographs you didn't take
- ❌ Reproducing a guide's descriptive prose

**Practical rules:**
- Raw artifacts are held for internal processing and verification. That's a defensible internal use. Do not republish them.
- Published output contains your analysis, your numbers, and short factual references with links to sources.
- Photographs: use your own. For anything else, get permission or use nothing.
- When summarising an article, state the facts in your own words and link to it. Send readers to the source.

---

## 6. Analytical ethics

Distinct from legal compliance, and more likely to actually matter to you.

**Don't damage a business with a bad number.** A wrongly-attributed closure or an incorrect price can cost a small restaurant real money. Verify before publishing anything negative and specific about a named venue.

**Distinguish observation from judgement.** "Covers dropped from two seatings to one" is an observation. "Struggling" is a judgement. Both are publishable; conflating them is not.

**Don't pretend to certainty you lack.** Small samples are small. Say so, every time.

**Disclose your position.** If you ate somewhere for free, say so. If you have any interest in a venue, say so. Right now you have neither — establish the habit before you do, because the first time it happens is the worst time to invent a policy.

**Consider the effect of publishing a weak signal.** Naming a trend can create it. That's a real form of influence and worth being conscious of, even at small scale.

---

## 7. If someone objects

1. Stop collecting from that source immediately. Don't argue, don't negotiate first.
2. Set `sources.active = false` and record the reason.
3. Respond within 48 hours, politely, explaining what you collect and why.
4. Delete if asked. The archive is not worth a fight with a restaurant.
5. Record the whole thing in `12-decision-log.md`.

**Cost of compliance: one source. Cost of a fight: the project.** This is not close.

---

## 8. Review triggers

Re-read this document when:
- Adding a new source class
- Adding a city in a new jurisdiction
- Before charging anyone money
- Before publishing anything critical about a named business
- Annually, regardless
