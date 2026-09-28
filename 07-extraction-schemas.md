# 07 — Extraction Schemas

**Status:** Draft v1
**Last reviewed:** 2026-09-28 (§2 amended for `D-057` and `D-059`)
**Machine-readable:** `schemas/venue.schema.json`, `schemas/menu_item.schema.json`, `schemas/event.schema.json`

---

## 1. The contract

Every extraction returns JSON conforming to one of these schemas. Validation happens before anything touches a fact table. A validation failure quarantines the whole extraction — never a partial insert.

**Universal rules, restated in every extraction prompt:**

1. **Extract only what is present.** Absent → `null`. Never infer, estimate, or complete.
2. **Per-field confidence**, 0–1.
3. **Original language preserved.** Translation is an additional field, never a replacement.
4. **Dates from the document**, or `null`. The model never invents a date.
5. **JSON only.** No preamble, no commentary, no markdown fences.

Rule 1 carries the most weight. A model handed a schema will fill it — that is what it is for. It must be told, every single time, that empty is the correct answer when the information isn't there.

---

## 2. Menu extraction

```json
{
  "is_menu": true,
  "venue_name_as_written": "Restaurant Noma",
  "city_as_written": "København",
  "menu_type": "tasting",
  "menu_date_stated": "Efterårsmenu 2026",
  "menu_date_confidence": 0.9,
  "currency": "DKK",
  "menu_price": 2800,
  "language": "da",
  "sections": [
    {
      "section_name": "Snacks",
      "items": [
        {
          "name_as_extracted": "Blomkål og fermenteret hyldeblomst",
          "name_original_transcription": "machine_unverified",
          "name_original": null,
          "name_translated": "Cauliflower and fermented elderflower",
          "description_as_extracted": null,
          "description_original": null,
          "price": null,
          "position": 1,
          "confidence": 0.95
        }
      ]
    }
  ],
  "notes_visible_on_menu": "Allergens on request",
  "extraction_confidence": 0.92,
  "fields_uncertain": ["menu_price"]
}
```

**Notes:**
- `venue_name_as_written` is deliberately raw. Resolution happens later; the extractor must not normalise names, because the raw form is evidence for the alias table.
- `price: null` on a tasting menu item is correct and expected.
- `fields_uncertain` gives the reviewer a fast path to what needs checking.
- **The extractor never writes `name_original` or `description_original` (`D-059`, schema v1.1.0).** It writes
  `name_as_extracted` and flags it `machine_unverified`. Machine extraction corrupts accents silently —
  ÀNEC became ÅNEC on Enigma's menu in August 2026 — and nobody on the project reads Danish or Catalan
  well enough to catch it. `name_original` is filled only by a person reading the artefact, and only rows
  with a human transcription are eligible for the gold set. `name_as_extracted` is good enough to detect
  that a dish changed; it is never quoted as the venue's wording.
- **`menu_date_stated` is free text as printed (`D-057`).** A season, version or "valid until" string goes
  here and does not set `observed_at`. Only a full date printed on the artefact does.
- **Open for Phase 2:** `schema.sql` still declares `menu_items.name_original TEXT NOT NULL`, which cannot
  hold a row awaiting transcription. Phase 2 adjusts the DDL (roadmap: "adjust for what Phase 1 taught you").

---

## 3. Venue extraction

```json
{
  "venue_name_as_written": "Restaurant Noma",
  "city_as_written": "København",
  "address": "Refshalevej 96, 1432 København",
  "website": "https://noma.dk",
  "venue_type": "restaurant",
  "opened_date_stated": null,
  "seats_stated": null,
  "service_model_stated": ["reservation-only", "ticketed-prepaid"],
  "price_band_stated": null,
  "opening_days_stated": ["wed","thu","fri","sat"],
  "people_mentioned": [
    {"name_as_written": "René Redzepi", "role_stated": "chef-owner", "confidence": 0.95}
  ],
  "group_mentioned": null,
  "sustainability_claims": ["own-fermentation-programme"],
  "extraction_confidence": 0.88,
  "fields_uncertain": ["price_band_stated"]
}
```

**Note:** `opening_days_stated` is more analytically useful than it looks. A venue moving from six days to four is a labour-cost signal, and it's visible on the website months before anyone writes about it.

---

## 4. Event extraction

From news articles, press releases, guide announcements.

```json
{
  "events": [
    {
      "event_type": "opening",
      "headline": "New vegetable-focused restaurant opens in Poblenou",
      "primary_entity_name": "Casa Verde",
      "secondary_entity_name": null,
      "city": "Barcelona",
      "date_stated": "2026-07-15",
      "date_precision": "exact",
      "detail": "40 seats, tasting menu only, chef previously at Disfrutar",
      "amount": null,
      "currency": null,
      "confidence": 0.9
    }
  ],
  "relationships_implied": [
    {
      "from_name": "Marta Sanz",
      "to_name": "Casa Verde",
      "rel_type": "chef_at",
      "date_stated": "2026-07-15",
      "confidence": 0.85
    }
  ],
  "extraction_confidence": 0.87
}
```

**Note:** one article frequently contains several events and several relationships. The schema is plural by default. `relationships_implied` is where the graph gets built, quietly, from routine news reading.

---

## 5. Tagging

Separate call, separate schema. Input: menu item name, description, and the full active taxonomy (cached).

```json
{
  "item_id": "uuid",
  "tags": [
    {"facet": "ingredient", "term": "brassica", "confidence": 0.95},
    {"facet": "ingredient", "term": "wild herb", "confidence": 0.7},
    {"facet": "technique", "term": "lacto-fermented", "confidence": 0.9}
  ],
  "unmapped": [
    {"facet": "ingredient", "raw_value": "hyldeblomst"}
  ]
}
```

**The critical constraint:** `tags[].term` must exist in the active taxonomy. Anything else goes to `unmapped`. The model is explicitly told that returning an unmapped value is correct behaviour and not a failure — otherwise it will force a bad match to appear helpful, which quietly poisons the counts.

---

## 6. Human observation

Same schemas, different entry path. Photographs go to an inbox folder; the Extractor processes them with `method = 'human'`.

Additional wrapper:

```json
{
  "observed_by": "operator",
  "observed_at": "2026-08-14",
  "venue_name_as_written": "Casa Verde",
  "city": "Barcelona",
  "observation_type": "visit",
  "photos": ["r2://inbox/2026-08-14-casaverde-menu-1.jpg"],
  "structured": { "...menu or venue schema..." },
  "field_notes": "Counter seating for 12, dining room ~28. Open kitchen. Two seatings. Menu changes weekly per staff.",
  "interpretation": "Feels like a bistronomy model with a fine-dining kitchen discipline.",
  "confidence_observed": 1.0,
  "confidence_interpretation": 0.6
}
```

**The two confidence fields are the point.** What you saw is fact. What you concluded is a hypothesis. Keeping these apart is what stops your own impressions from contaminating the dataset — which is the specific risk of being an enthusiast with a database.

---

## 7. Validation rules

Beyond JSON Schema:

| Rule | Action on failure |
|---|---|
| Price within plausible range for city and menu type | Flag, reduce confidence, don't reject |
| Currency matches city (DKK/EUR/GBP) unless explicitly stated | Flag for review |
| Date not in the future | Reject the field, set null |
| Date not before 1990 | Reject the field, set null |
| Item count 1–60 | Above 60, flag — likely a parsing error |
| Section names non-empty | Default to "unspecified" |
| `extraction_confidence >= 0.5` | Below → quarantine whole extraction |
| Venue name non-empty | Reject extraction — nothing is usable without it |

---

## 8. Schema versioning

- Every schema carries a version string, recorded on every `extractions` row.
- Additive changes (new optional field) → minor bump, no reprocessing needed.
- Breaking changes (renamed or newly required field) → major bump, and a decision recorded in `12-decision-log.md` about whether to reprocess history.
- Never silently change a field's meaning. Add a new field and deprecate the old one. A field whose meaning changed halfway through the corpus is undetectable later and corrupts every query that touches it.
