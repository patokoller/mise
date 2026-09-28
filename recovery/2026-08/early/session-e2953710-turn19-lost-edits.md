# Lost edits from session e2953710 (2026-08-01), turn 19

Source: chat "Copenhagen venue frame union file and Route B setup", turn 19. That turn folded D-047 into
`schema.sql` and made the three string replacements below. `schemas/schema.sql` and
`schemas/schema-patch-D047.sql` on disk already carry the fold-in. The three replacements below are **not** in
the current `BUILD-STATUS.md` or `12-decision-log.md`. Later sessions built on copies without them, so the
schema row still says "Patch pending", which contradicts `schema.sql`.

Transcribed verbatim from the transcript's own replacement script. Each OLD string was checked
against the current file on 2026-09-28 and occurs exactly once, so each edit can be applied as a
direct replacement.

## 1. BUILD-STATUS.md, "What exists" table, schema row

OLD:
```
| Database schema | 🟨 Patch pending | `schema.sql`, `schema-patch-D047.sql` | v1 + D-020. Parses clean. Not yet deployed. **`D-047` must be applied before first run** — `entity_aliases` cannot date a name as a fact, and `canonical_name` has no history |
```
NEW:
```
| Database schema | ✅ Ready to run | `schema.sql` | v1 + D-020 + **D-047**, folded in 2026-08-01 and parsed clean (69 statements). Not yet deployed. `schema-patch-D047.sql` is kept as the record of the change and is marked **do not run** |
```

## 2. 12-decision-log.md, D-047 "Decision" sentence

OLD:
```
**Decision:** two amendments to `schema.sql`, written as `schema-patch-D047.sql` and not yet deployed.
```
NEW:
```
**Decision:** two amendments to `schema.sql`. Written first as `schema-patch-D047.sql`, then **folded directly into `schema.sql` on 2026-08-01**, which now parses clean at 69 statements and needs no replay. The patch file is retained as the record of the change and marked *do not run*.
```

## 3. 12-decision-log.md, D-047 "Reverses if" paragraph (two paragraphs inserted before it)

OLD:
```
**Reverses if:** deployment shows the alias table growing faster than it earns its keep — but note the cost of reversing after deployment is far higher than the cost of adding it now, which is why it is being done pre-deployment.
```
NEW:
```
**One consequence found while folding it in, and left unresolved.** `v_venue_current` returns venue facts and **no name at all**, so any consumer wanting to publish a venue must reach into `entities.canonical_name` — the column this entry deprecates. Consumers should join `v_entity_display_name` instead. This is noted in `schema.sql` as a comment; changing `v_venue_current` is a separate decision and has not been made.

**A circular foreign key was unavoidable.** `entities` is created before `entity_aliases`, so `canonical_alias_id` cannot carry an inline `REFERENCES`; the constraint is added by `ALTER TABLE` immediately after both tables exist. That single `ALTER` is a circular-FK resolution, not migration history, and is commented as such so a future reader does not mistake it for a replayed patch.

**Reverses if:** deployment shows the alias table growing faster than it earns its keep — but note the cost of reversing after deployment is far higher than the cost of adding it now, which is why it is being done pre-deployment.
```
