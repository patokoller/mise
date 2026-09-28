# 16 — Validation Guide

**Status:** Draft v1
**Last reviewed:** 2026-09-28 (Phase 1 checks added)

**Who this is for:** you, checking work you didn't write, in a domain you know well, using a technology you know partially.

---

## 1. The core move

You cannot audit code. You can audit *reality*, and that's actually the stronger check.

**The move is always the same: pick something you can verify with your own eyes, and trace it all the way through.**

You know what a restaurant menu looks like. You can open a website and count the dishes. So:

> Open a restaurant's menu page. Count the dishes yourself. Then ask: *"Show me every row in the database for this restaurant's menu from this date."* Compare.

If the menu has 14 dishes and the database has 14 dishes with the right names and prices, the pipeline works for that case. If it has 9, or 22, something is wrong and you've found it without reading anything.

**This single technique catches most real bugs.** An engineer would test the code. You test the output against the world, which is what actually matters and what an engineer often forgets to do.

---

## 2. The five questions

Ask these about anything built. They're ordered by how much trouble they catch.

**1. "Show me one complete example, from source to database."**
The raw menu, the extracted JSON, the final rows. If Claude can't produce this easily, the system isn't observable enough — fix that before building more.

**2. "What does this do when it fails?"**
Correct answers: stops, logs, emails you, changes nothing. Wrong answers: guesses, uses a default, continues with partial data. Silent partial failure is the thing that poisons a dataset.

**3. "What could be wrong here that I wouldn't notice?"**
Forces the failure modes into the open. Write the answer down.

**4. "How would I know if this stopped working next month?"**
If the answer is "you'd notice eventually," it needs a health check.

**5. "What's the denominator?"**
For any number the system produces. If it can't tell you what the count is out of, the number isn't publishable (`08-trend-detection.md`, `09-editorial-and-predictions.md`).

---

## 3. Phase-by-phase checks

Concrete things to do, matched to `11-roadmap.md`. None require reading code.

### Phase 1 — Publish by hand

Added 2026-09-28. These are the checks that would have caught what actually went wrong in August. Each
takes a few minutes and needs a browser, not code. The collection lives in two files:
`data/phase1/phase1-menus-<date>.csv` (public, one row per menu) and the dish file you hold privately (`D-063`).

☐ **The count-the-page test.** Pick one venue marked `full`. Open its `source_url`. Count the dishes on the
page yourself. Filter the dish file to that `menu_id` and count the rows. They must match. If the file has
about twice as many, a tabbed page was read twice — The Ledbury did exactly this (14 extracted, 7 real).

☐ **The one-name test.** Pick one Danish or Catalan venue. Take one dish name from the menu on screen and
compare it letter by letter with `dish_text_as_extracted`. Look at ø, æ, å, à, ç and at l versus I. If
anything differs, you have just re-found the `D-059` problem — note it; nothing to fix, because
`dish_name_original` is empty until you transcribe it.

☐ **The price test.** Pick one `price_only` venue. Open the page. Is the number in `menu_price` the number on
the page, in the same currency? If the page shows two prices, the row must say `competing_prices = yes` and
leave the choice to you (akmē does this).

☐ **The date test, Phase 1 version.** Every row should have `observed_at_source`. If it says `retrieval`,
`observed_at` is the day of collection — that is correct and expected for undated menus (`D-057`). If it says
`menu_artefact`, the date must be printed on the menu itself; check it's there. A season, a version number
or "valid until" is not a date and must sit in `menu_date_stated` instead.

☐ **The closed-venue test.** Any row marked `closed_per_source` must have a URL in `trading_status_source`.
Open it. It must actually say the place closed. Absence of a website is never enough.

☐ **The denominator test, before anything is published.** Nothing from the Phase 1 forty carries a count
or a share (`D-056`). If an issue draft contains "N of M" about these venues, it is wrong, however true the
arithmetic.

### Phase 2 — Database and first extraction

☐ **The eye test.** Three menus you can open in a browser. Count dishes and prices by hand. Compare to the database. Any mismatch is a real problem, no matter how small.

☐ **The date test.** Ask: *"Show me a fact where `observed_at` and `retrieved_at` are different, and explain why."* If they're always identical, dates are probably being set to "now" — which silently ruins the time series and is the single most expensive bug available in this project.

☐ **The source test.** Pick a random row. *"Where did this come from?"* You should get a URL and a retrieval date within seconds.

☐ **The absence test.** Find a menu where a dish has no price. Confirm the database says `null`, not `0` and not a guess. A zero where a null belongs will show up later as a fake price crash.

☐ **The gold set.** Hand-extract 30 documents yourself. This is genuinely tedious — do it anyway. It's the only objective measure of quality you will ever have, and it takes about three hours once.

### Phase 3 — Automated collection

☐ **The unplug test.** Turn off a source and confirm the pipeline notices and reports it, rather than quietly recording zero.

☐ **The duplicate test.** Ask: *"Show me every venue whose name is similar to another venue's."* Read the list. You'll spot duplicates immediately because you know these restaurants — this is domain knowledge doing work no algorithm can.

☐ **The heartbeat test.** Deliberately break something small. Confirm you get an email. If you don't, the health check is decorative.

☐ **The restore test.** Have Claude restore last week's backup into a scratch database and count the rows. An untested backup is not a backup, and this is the check people skip until the week they need it.

### Phase 4 — Tagging

☐ **The taste test.** Pull 20 tagged dishes. Read them. Do the tags make sense to you as someone who eats out constantly? You are better at this than any metric.

☐ **The unmapped test.** Look at the unmapped queue. If it's empty, tagging is probably forcing bad matches to look successful. An empty queue is a red flag, not a green one.

☐ **The consistency test.** Same dish, two restaurants, different wording. Do both get the same tags? If not, the taxonomy needs synonyms.

### Phase 5 — Statistics and signals

☐ **The reality test.** Take a signal the system reports. Do you *believe* it? Go look at three of the venues it names. If a claimed trend doesn't survive contact with your own knowledge of these restaurants, trust yourself and investigate.

☐ **The denominator test.** Every number. Every time. Out of how many?

☐ **The cohort test.** *"Did we add venues during this period that would explain this?"* The answer is yes more often than feels reasonable.

☐ **The shuffle test.** Ask Claude to recompute a signal with the dates randomly shuffled. If a "trend" still appears, it was an artifact of your sample, not of time.

---

## 4. Red flags

Things that should stop you, even when everything appears fine.

🚩 **Numbers that are suspiciously round or suspiciously clean.** Real data is messy.

🚩 **No failures anywhere.** A pipeline processing hundreds of documents with a 100% success rate is not succeeding — it's hiding failures. Ask where they went.

🚩 **You can't explain what a component does.** Not "can't explain the code" — can't explain the *purpose*. That means it shouldn't exist, or you weren't told properly.

🚩 **A trend that appeared suddenly and completely.** Real diffusion is gradual and patchy. Sudden and total usually means you changed something.

🚩 **Confidence scores that are all high, or all identical.** The extractor isn't actually assessing anything.

🚩 **Anything you'd have to trust rather than check.** Redesign it so it can be checked.

🚩 **A number in a draft issue that you can't trace to a query in under a minute.** Do not publish it. This is the rule that protects your credibility.

---

## 5. The weekly two-minute check

Fold into the review block in `13-operating-cadence.md`.

1. Did collection run every day this week? (health check output)
2. How many documents processed, how many failed? Is the failure rate similar to last week?
3. Queue depths: entities, unmapped, quarantined. Growing faster than you can review?
4. Cost: in line with last month?
5. Pick one random new fact. Where did it come from? Does it look right?

Point 5 is the one to protect. One random spot-check a week, sustained over a year, catches things no automated test will — because you're checking against knowledge that isn't in the system.

---

## 6. When you disagree with the system

You know restaurants. The system knows rows. When you conflict:

**You are usually right about the world.** If a signal says something you know to be untrue about a restaurant you've been to, the data is wrong. Investigate before dismissing your own knowledge.

**The system is usually right about the counting.** If it says 8 venues and you *feel* like it's more, check before overriding — feelings about frequency are exactly where human judgement is weak, and this is precisely what the database is for.

**The productive question is always: what would explain both?** Usually coverage. You've been to fifteen places doing X; the system tracks eight of them. Both true.

---

## 7. What "good" looks like at each stage

Not a technical standard — the practical one.

**Phase 2 good:** you can point at any dish in the database and get back the menu it came from and when.

**Phase 3 good:** you go on holiday for two weeks, come back, and the data is complete and you got no alarming emails.

**Phase 4 good:** you can ask "which venues serve fermented things" and the answer matches your own sense of these cities.

**Phase 5 good:** the system tells you something about your own cities that you didn't already know, and you check it, and it's true.

**That last one is the whole project.** Everything else is scaffolding for it.
