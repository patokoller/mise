-- ============================================================================
-- SUPERSEDED 2026-08-01 — DO NOT RUN THIS FILE.
--
-- These changes have been folded directly into schema.sql, which is now correct
-- as written and needs no replay. This file is kept as the RECORD of what
-- changed and why, alongside D-047 in 12-decision-log.md.
--
-- Running it against the current schema.sql would fail: the columns already
-- exist and the old constraint it drops is no longer there.
-- ============================================================================

-- ============================================================================
-- D-047 · 2026-08-01 · Names become dated facts; canonical_name becomes a pointer
-- Applies to schema.sql v1 + D-020. NOT YET DEPLOYED — the database has never
-- been run, so this is an amendment to the DDL, not a live migration.
-- ============================================================================

-- ---------------------------------------------------------------------------
-- GAP 1. A name is a fact, and entity_aliases could not date it.
--
-- The table had created_at only, which is the INSERT timestamp. It cannot say
-- "MICHELIN called this venue X on 2026-07-28" — the observation date and the
-- row-creation date are different things, and rule 1 requires the first.
-- source_id was also nullable, so an alias could exist attached to nothing.
-- ---------------------------------------------------------------------------

ALTER TABLE entity_aliases
    ADD COLUMN observed_at   DATE NOT NULL,   -- when the SOURCE said it
    ADD COLUMN retrieved_at  DATE NOT NULL,   -- when WE fetched it
    ADD COLUMN valid_from    DATE NOT NULL,   -- append-only, per rule 2
    ADD COLUMN valid_to      DATE,            -- NULL = still current
    ALTER COLUMN source_id SET NOT NULL;

-- The old constraint was UNIQUE (entity_id, normalised_alias), which forbids
-- the same name being observed from a second source or on a later date. That
-- is exactly what we need to record: two guides using one string is evidence,
-- not a duplicate.
ALTER TABLE entity_aliases DROP CONSTRAINT entity_aliases_entity_id_normalised_alias_key;
ALTER TABLE entity_aliases
    ADD CONSTRAINT entity_aliases_observation_uniq
    UNIQUE (entity_id, normalised_alias, source_id, observed_at);

ALTER TABLE entity_aliases
    ADD CONSTRAINT entity_aliases_valid_range
    CHECK (valid_to IS NULL OR valid_to >= valid_from);

CREATE INDEX idx_aliases_current ON entity_aliases (entity_id) WHERE valid_to IS NULL;

-- ---------------------------------------------------------------------------
-- GAP 2. entities.canonical_name was a single mutable column with no history.
--
-- If it changed, the previous value survived only if somebody remembered to
-- write it as an alias, and nothing enforced that. Rule 2 says corrections
-- close a row and insert a new one; a name overwritten in place breaks it.
--
-- Fix: canonical_name stops being a stored string and becomes a POINTER at
-- one alias row. Changing the display name means repointing. Every name the
-- project has ever observed stays in entity_aliases with its own dates and
-- its own source. Nothing is ever overwritten.
-- ---------------------------------------------------------------------------

ALTER TABLE entities
    ADD COLUMN canonical_alias_id UUID REFERENCES entity_aliases(alias_id);

COMMENT ON COLUMN entities.canonical_name IS
    'DEPRECATED as a source of truth. Kept only as a denormalised convenience
     mirror of the alias pointed at by canonical_alias_id. Never write to it
     directly; rebuild it from v_entity_display_name.';

COMMENT ON COLUMN entities.canonical_alias_id IS
    'D-043: points at the alias carrying the venue''s OWN published name in its
     OWN orthography, captured at the F2 pass. NOT chosen by source precedence
     — a precedence rule makes the name a function of which guides list the
     venue, and flips it when a listing lapses, which reads as a rename in the
     time series.';

CREATE VIEW v_entity_display_name AS
SELECT e.entity_id,
       e.google_place_id,
       a.alias        AS display_name,
       a.language     AS display_language,
       a.source_id    AS display_name_source,
       a.observed_at  AS display_name_observed_at,
       (e.canonical_alias_id IS NULL) AS display_name_provisional
FROM entities e
LEFT JOIN entity_aliases a ON a.alias_id = e.canonical_alias_id;

-- Every name ever observed for a venue, with provenance. This is what Route B
-- matching and any outward join should read — NOT display_name.
CREATE VIEW v_entity_all_names AS
SELECT ea.entity_id,
       ea.alias,
       ea.normalised_alias,
       ea.language,
       ea.source_id,
       ea.observed_at,
       ea.valid_from,
       ea.valid_to,
       (ea.valid_to IS NULL) AS current
FROM entity_aliases ea;

-- ---------------------------------------------------------------------------
-- WHY BOTH VIEWS EXIST, which is the point of the whole patch:
-- one string cannot serve both purposes.
--
--   v_entity_display_name  -> ONE human string, for publication.
--   v_entity_all_names     -> EVERY variant, for matching, via the existing
--                             trigram index on normalised_alias.
--
-- Collapsing these is how the Kadeau bug class returns: a matcher that misses
-- because the single canonical string happened to be the English one. The
-- Copenhagen frame carries 14 name variants across 45 dual-route venues —
-- 4 prefix, 8 orthography, 1 translation, 1 genuinely distinct name — and
-- five of those orthographic differences are case-only, which a naive
-- normaliser silently discards along with the venue's own styling (formel B,
-- akmē, a|o|c).
-- ---------------------------------------------------------------------------
