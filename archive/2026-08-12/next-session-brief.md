# Next session — paste this in

I am a product manager, not a software engineer. You build; I specify, judge output
against reality, and publish. I know restaurants extremely well and technology only
conceptually.

Read BUILD-STATUS.md first, then 12-decision-log.md entries D-056 to D-060, then
17-session-playbooks.md Phase 1. Tell me where we are before you do anything.

## WHERE WE LEFT OFF (2026-08-12)

Phase 1 collection started. I supplied 39 venue rows with 30 URLs, opened by me in one
batch at ~11:30 CEST on 12 August. Claude fetched 8 of the 30 and stopped deliberately.

Result of those 8: 6 F2 `full`, 2 `price_only`, 110 dish rows captured, 7 of 8 pages
served English only. Denominator on every one of those numbers is 8 fetched pages, of
30 URLs, of 39 rows. Not a sample of anything.

The reason it stopped: machine extraction corrupted original-language dish names on the
Enigma artefact in three places (ÀNEC→ÅNEC, CIRERA→CIIRERA, El→EI). That is D-020's
unrecoverable field, damaged silently, in a way review cannot catch. D-059 was proposed
in response.

Frame unchanged at 132, Route A, F1 only. Route B Copenhagen still not runnable (D-055),
reach 1 of 5. No press item has ever been collected.

## THIS SESSION — pick up in this order

1. **Settle D-057, D-059 and D-060.** All three are proposed, none accepted. D-057 has
   two open sub-questions (version/season strings; CMS auto-stamps like og:updated_time).
   Do not let these drift — every row collected before they settle inherits whatever we
   do by default.
2. **Finish the remaining 22 URLs** for prices, structure, format, service notes and F2
   only. No original-language dish names from extraction.
3. **Separately, list the venues where an original-language menu exists at a real URL.**
   That becomes the human transcription pass, and it is mine to do.
4. Then draft issue #1 — 09-editorial-and-predictions.md §3, under 900 words, every
   claim with its denominator.

## STILL OWED, AND OVERDUE IN EFFECT

**Five dated falsifiable predictions with resolution criteria (D-018).** These must be
made before system data exists. Collection has now started, so the intuition-only window
is already compromised — say so plainly rather than pretending 28 August still holds.
Claude has five candidate frames drafted, anchored on the 132-venue frame rather than the
cohort; the numbers and confidences are mine to supply.

**H2-a's six-month lag threshold in the prediction ledger is still a Claude placeholder.**
Replace with my figure or the clause is scored against an invented number.

## THE FIVE THINGS THAT MUST NEVER BREAK

1. Every fact carries observed_at, retrieved_at, and a source URL. Dates cannot be
   backfilled later.
2. Facts are append-only. Corrections close the old row and insert a new one.
3. Entities resolve to a canonical ID. Never auto-merge below threshold.
4. Statistics are computed, not read off. You never state a number you did not calculate.
5. Every count states its denominator. No exceptions, ever.

## CARRY-IN — DO NOT RE-LEARN

- Ask whether you counted or remembered before stating any number about a file.
- Count in code, not by eye, and show me the check.
- The Ledbury rendered every block twice in extraction — a correct counter over doubled
  input gives a wrong answer that looks right. Deduplicate before counting.
- Do not guess URLs. Ask me for the real one.
- Do not guess causes. An unexplained result stays unexplained.
- Nothing published from these 40 venues carries a denominator (D-056, confirmed).
- No mechanical rule decides competing prices. akmē carries 1500 and 1300 DKK live on one
  page — confirmed 2026-08-12. Flag, never choose. The Ledbury's three prices are NOT this
  case: they are labelled lunch-6 / lunch-8 / dinner. Structure, not conflict.
- "See the blackboard" (Anarki) is an F2 ceiling no method crosses. Record and move on.
- Page freshness and menu freshness are different. Geranium still shows a COVID notice and
  a "closed 5–29 July" message live in August.
- A venue's /en/ URL may be a translation, not the menu (Prodigi). Capturing it means
  dish_name_original cannot be filled from that URL at all.

## DO NOT

- Do not touch Route B, the 132-venue frame, or F2/F4/F5 across it.
- Do not start Berlingske's reproducibility problem.
- Do not build a database, write a pipeline, or propose one.
- Answer my question before suggesting improvements.

## STILL OPEN, DO NOT SETTLE QUIETLY

Copenhagen Post's disposition; the Politiken agent question; whether to adopt Retriever;
MigogKbh's untested section index and search; Noma's F4 status; display_name_provisional;
whether v_venue_current exposes a name. Plus, new: Noma's URL (noma.co.com appears wrong,
noma.dk expected); Kadeau, Alchemist, Alouette, Humble Chicken, Disfrutar and Aleia have
no URL and no F2 verdict; Connection and Brasserie Barner are asserted closed with no
source, and both are in the 132-venue frame.

## ON YOUR ESTIMATES

Say what would make the estimate wrong. Last session's fetch ran 8 for 8, against a July
test where F2 needed a human on 5 of 6. Either that test hit a bad set or the remaining 22
are about to get much harder — this is unexplained and stays unexplained.

## END OF SESSION

Update BUILD-STATUS.md. Add any design decision to 12-decision-log.md with its reversal
condition. If a document in project knowledge is now wrong, tell me which and fix it.
