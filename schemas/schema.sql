-- MISE — Hospitality Intelligence Platform
-- Postgres schema v1
-- Target: PostgreSQL 16+ with pgvector and pg_trgm
--
-- Design notes:
--   * Facts are append-only. Corrections close the old row via valid_to.
--   * Every fact carries provenance (source, document, extraction, method, confidence).
--   * observed_at and retrieved_at are always distinct fields.
--   * Original-language text is never overwritten by a translation. See D-020.
--
-- Changes since v1 (2026-07-28), all pre-deployment:
--   * menu_items.name  -> name_original + name_translated
--   * menu_items.description -> description_original + description_translated
--   * menus.language added        (20-twenty-questions.md Q7)
--   * predictions.basis added     (20-twenty-questions.md Q20, D-018)
--
-- Changes since D-020 (2026-08-01, D-047), all pre-deployment:
--   * entity_aliases gains observed_at, retrieved_at, valid_from, valid_to
--     -- a name is a FACT and must be datable under rule 1. created_at is an
--     insert timestamp and cannot say "MICHELIN called it X on 2026-07-28".
--   * entity_aliases.source_id becomes NOT NULL -- an alias attached to no
--     source is not evidence of anything.
--   * entity_aliases UNIQUE moves to (entity_id, normalised_alias, source_id,
--     observed_at) -- two guides using one string is evidence, not a duplicate.
--   * entities.canonical_alias_id added; canonical_name DEPRECATED as a source
--     of truth. The display name becomes a POINTER, so changing it is a
--     repointing and every name ever observed survives with its own dates.
--   * views v_entity_display_name and v_entity_all_names added.

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS unaccent;
CREATE EXTENSION IF NOT EXISTS vector;

-- ============================================================
-- ENUMS
-- ============================================================

CREATE TYPE entity_type      AS ENUM ('venue','person','group','supplier','location','publication');
CREATE TYPE date_precision   AS ENUM ('exact','month','quarter','year','inferred');
CREATE TYPE extraction_method AS ENUM ('api','scrape','llm_extraction','ocr_llm','human','inferred');
CREATE TYPE verification      AS ENUM ('none','human','second_source');
CREATE TYPE tos_posture       AS ENUM ('api_permitted','robots_permitted','manual_only','prohibited');
CREATE TYPE prediction_status AS ENUM ('open','correct','incorrect','partial','void');
-- 'intuition' = made without system data. The control group for Q20. See D-018.
CREATE TYPE prediction_basis  AS ENUM ('intuition','data','mixed');

-- ============================================================
-- SOURCE LAYER
-- ============================================================

CREATE TABLE sources (
    source_id       UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name            TEXT NOT NULL,
    base_url        TEXT,
    source_type     TEXT NOT NULL,          -- 'venue_site','guide','trade_press','api','registry','human'
    city            TEXT,
    language        TEXT,
    access_method   extraction_method NOT NULL,
    tos             tos_posture NOT NULL DEFAULT 'robots_permitted',
    tos_reviewed_at DATE,
    crawl_frequency TEXT,                   -- 'daily','weekly','monthly','on_demand'
    reliability     NUMERIC(3,2) DEFAULT 0.80 CHECK (reliability BETWEEN 0 AND 1),
    active          BOOLEAN NOT NULL DEFAULT TRUE,
    notes           TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE documents (
    document_id     UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_id       UUID NOT NULL REFERENCES sources(source_id),
    url             TEXT,
    content_hash    TEXT NOT NULL,          -- dedupe key: unchanged hash = skip extraction
    content_type    TEXT,                   -- 'text/html','application/pdf','image/jpeg'
    storage_path    TEXT NOT NULL,          -- object storage key for the raw artifact
    title           TEXT,
    language        TEXT,
    published_at    DATE,                   -- date the source claims, if any
    retrieved_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    http_status     INT,
    UNIQUE (source_id, content_hash)
);

CREATE INDEX idx_documents_source     ON documents(source_id);
CREATE INDEX idx_documents_retrieved  ON documents(retrieved_at);
CREATE INDEX idx_documents_hash       ON documents(content_hash);

CREATE TABLE extractions (
    extraction_id   UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_id     UUID NOT NULL REFERENCES documents(document_id),
    agent_name      TEXT NOT NULL,
    model_id        TEXT NOT NULL,          -- e.g. 'claude-sonnet-5'
    prompt_version  TEXT NOT NULL,          -- e.g. 'menu_extract_v3'
    schema_version  TEXT NOT NULL,
    input_tokens    INT,
    output_tokens   INT,
    cost_usd        NUMERIC(10,6),
    status          TEXT NOT NULL DEFAULT 'ok',   -- 'ok','schema_fail','empty','error'
    error_detail    TEXT,
    raw_output      JSONB,                  -- keep the unvalidated output for debugging
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_extractions_document ON extractions(document_id);
CREATE INDEX idx_extractions_agent    ON extractions(agent_name, created_at);

-- ============================================================
-- ENTITY LAYER
-- ============================================================

CREATE TABLE entities (
    entity_id       UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    entity_type     entity_type NOT NULL,
    canonical_name  TEXT NOT NULL,          -- DEPRECATED as truth (D-047). Denormalised mirror
                                            -- of the alias in canonical_alias_id. Do not write
                                            -- to it directly; rebuild from v_entity_display_name.
    canonical_alias_id UUID,                -- FK added below, after entity_aliases exists.
                                            -- D-043: points at the venue's OWN published name in
                                            -- its OWN orthography, captured at the F2 pass. NOT
                                            -- chosen by source precedence -- precedence makes the
                                            -- name a function of which guides list the venue and
                                            -- flips it when a listing lapses, which then reads as
                                            -- a rename in the time series.
    normalised_name TEXT NOT NULL,          -- lowercased, unaccented, suffixes stripped
    city            TEXT,
    country         TEXT,
    website         TEXT,
    google_place_id TEXT,
    company_number  TEXT,
    first_seen_at   DATE NOT NULL,
    last_seen_at    DATE,
    active          BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (google_place_id)
);

CREATE INDEX idx_entities_norm_trgm ON entities USING gin (normalised_name gin_trgm_ops);
CREATE INDEX idx_entities_type_city ON entities(entity_type, city);

-- Every name the project has ever observed for an entity, from any source,
-- with its own dates. This is the record; entities.canonical_name is not.
CREATE TABLE entity_aliases (
    alias_id        UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    entity_id       UUID NOT NULL REFERENCES entities(entity_id) ON DELETE CASCADE,
    alias           TEXT NOT NULL,
    normalised_alias TEXT NOT NULL,
    language        TEXT,
    source_id       UUID NOT NULL REFERENCES sources(source_id),
    observed_at     DATE NOT NULL,          -- when the SOURCE said it       (rule 1)
    retrieved_at    DATE NOT NULL,          -- when WE fetched it            (rule 1)
    valid_from      DATE NOT NULL,          -- append-only                   (rule 2)
    valid_to        DATE,                   -- NULL = still current
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),  -- row insert time, NOT an observation
    -- The old constraint was UNIQUE (entity_id, normalised_alias), which forbade
    -- the same name being observed from a second source or on a later date --
    -- exactly what needs recording. Two guides using one string is evidence.
    UNIQUE (entity_id, normalised_alias, source_id, observed_at),
    CHECK (valid_to IS NULL OR valid_to >= valid_from)
);

CREATE INDEX idx_aliases_norm_trgm ON entity_aliases USING gin (normalised_alias gin_trgm_ops);
CREATE INDEX idx_aliases_current   ON entity_aliases (entity_id) WHERE valid_to IS NULL;

-- Circular reference: entities points at an alias, aliases point at an entity.
-- entities is created first, so this FK cannot be declared inline above.
-- This is a circular-FK resolution, not migration history.
ALTER TABLE entities
    ADD CONSTRAINT entities_canonical_alias_fk
    FOREIGN KEY (canonical_alias_id) REFERENCES entity_aliases(alias_id);

-- Anything the resolver is not confident about lands here for human adjudication.
CREATE TABLE entity_candidates (
    candidate_id    UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    raw_name        TEXT NOT NULL,
    city            TEXT,
    entity_type     entity_type NOT NULL,
    suggested_entity_id UUID REFERENCES entities(entity_id),
    match_score     NUMERIC(4,3),
    match_method    TEXT,                   -- 'exact','identifier','trigram','embedding','none'
    document_id     UUID REFERENCES documents(document_id),
    resolved        BOOLEAN NOT NULL DEFAULT FALSE,
    resolution      TEXT,                   -- 'merged','new_entity','rejected'
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    resolved_at     TIMESTAMPTZ
);

CREATE INDEX idx_candidates_open ON entity_candidates(resolved) WHERE resolved = FALSE;

CREATE TABLE relationships (
    relationship_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    from_entity_id  UUID NOT NULL REFERENCES entities(entity_id),
    to_entity_id    UUID NOT NULL REFERENCES entities(entity_id),
    rel_type        TEXT NOT NULL,          -- 'chef_at','owned_by','invested_in','supplies',
                                            -- 'succeeded_by','spun_off_from','trained_under','operates_in'
    role_detail     TEXT,
    observed_at     DATE NOT NULL,
    valid_from      DATE,
    valid_to        DATE,
    date_precision  date_precision NOT NULL DEFAULT 'exact',
    source_id       UUID REFERENCES sources(source_id),
    document_id     UUID REFERENCES documents(document_id),
    extraction_id   UUID REFERENCES extractions(extraction_id),
    method          extraction_method NOT NULL,
    confidence      NUMERIC(3,2) NOT NULL DEFAULT 0.80,
    verified_by     verification NOT NULL DEFAULT 'none',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    CHECK (from_entity_id <> to_entity_id)
);

CREATE INDEX idx_rel_from ON relationships(from_entity_id, rel_type);
CREATE INDEX idx_rel_to   ON relationships(to_entity_id, rel_type);
CREATE INDEX idx_rel_open ON relationships(valid_to) WHERE valid_to IS NULL;

-- ============================================================
-- VENUE LAYER
-- ============================================================

CREATE TABLE venues (
    entity_id       UUID PRIMARY KEY REFERENCES entities(entity_id) ON DELETE CASCADE,
    address         TEXT,
    neighbourhood   TEXT,
    lat             NUMERIC(9,6),
    lon             NUMERIC(9,6),
    opened_on       DATE,
    opened_precision date_precision DEFAULT 'inferred',
    closed_on       DATE,
    closed_precision date_precision,
    venue_type      TEXT,                   -- 'restaurant','bar','hotel_restaurant','popup','bakery','cafe'
    parent_group_id UUID REFERENCES entities(entity_id)
);

CREATE INDEX idx_venues_geo    ON venues(lat, lon);
CREATE INDEX idx_venues_opened ON venues(opened_on);

-- Temporal attribute store. One row per attribute-observation. Never updated in place.
CREATE TABLE venue_facts (
    fact_id         UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    entity_id       UUID NOT NULL REFERENCES entities(entity_id) ON DELETE CASCADE,
    attribute       TEXT NOT NULL,          -- 'seats','price_band','service_style','covers_per_service',
                                            -- 'tasting_menu_price','opening_days','sustainability_claim'
    value_text      TEXT,
    value_numeric   NUMERIC(12,2),
    value_currency  CHAR(3),
    observed_at     DATE NOT NULL,
    retrieved_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    valid_from      DATE,
    valid_to        DATE,                   -- NULL = still believed current
    date_precision  date_precision NOT NULL DEFAULT 'exact',
    source_id       UUID REFERENCES sources(source_id),
    document_id     UUID REFERENCES documents(document_id),
    extraction_id   UUID REFERENCES extractions(extraction_id),
    method          extraction_method NOT NULL,
    confidence      NUMERIC(3,2) NOT NULL DEFAULT 0.80,
    verified_by     verification NOT NULL DEFAULT 'none'
);

CREATE INDEX idx_vfacts_entity_attr ON venue_facts(entity_id, attribute, observed_at DESC);
CREATE INDEX idx_vfacts_current     ON venue_facts(entity_id, attribute) WHERE valid_to IS NULL;

-- ============================================================
-- MENU LAYER
-- ============================================================

CREATE TABLE menus (
    menu_id         UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    entity_id       UUID NOT NULL REFERENCES entities(entity_id) ON DELETE CASCADE,
    menu_type       TEXT,                   -- 'a_la_carte','tasting','lunch','breakfast','bar','wine','dessert'
    language        TEXT,                   -- ISO 639-1 of the menu as published. One row per
                                            -- language version; counting distinct values per
                                            -- venue answers Q7.
    currency        CHAR(3),
    menu_price      NUMERIC(10,2),          -- for fixed-price menus
    observed_at     DATE NOT NULL,
    retrieved_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    valid_from      DATE,
    valid_to        DATE,
    date_precision  date_precision NOT NULL DEFAULT 'exact',
    source_id       UUID REFERENCES sources(source_id),
    document_id     UUID REFERENCES documents(document_id),
    extraction_id   UUID REFERENCES extractions(extraction_id),
    method          extraction_method NOT NULL,
    confidence      NUMERIC(3,2) NOT NULL DEFAULT 0.80,
    item_count      INT
);

CREATE INDEX idx_menus_entity ON menus(entity_id, observed_at DESC);
CREATE INDEX idx_menus_date   ON menus(observed_at);

CREATE TABLE menu_items (
    item_id         UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    menu_id         UUID NOT NULL REFERENCES menus(menu_id) ON DELETE CASCADE,
    entity_id       UUID NOT NULL REFERENCES entities(entity_id),  -- denormalised for query speed
    section         TEXT,                   -- 'starters','mains','desserts','snacks'
    position        INT,
    -- Exactly as written on the menu. Never overwritten by a translation (D-020).
    -- Tagging and all trigram search run against this column, not the translation.
    name_original   TEXT NOT NULL,
    name_translated TEXT,                   -- NULL when the menu is already in English
    description_original  TEXT,
    description_translated TEXT,
    price           NUMERIC(10,2),
    currency        CHAR(3),
    observed_at     DATE NOT NULL,          -- denormalised from menu, for direct time queries
    confidence      NUMERIC(3,2) NOT NULL DEFAULT 0.80
);

CREATE INDEX idx_items_menu   ON menu_items(menu_id);
CREATE INDEX idx_items_entity ON menu_items(entity_id, observed_at);
CREATE INDEX idx_items_name_trgm ON menu_items USING gin (name_original gin_trgm_ops);

-- ============================================================
-- TAXONOMY
-- ============================================================

CREATE TABLE taxonomy_terms (
    term_id         UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    facet           TEXT NOT NULL,          -- 'ingredient','technique','format','service_model','technology',
                                            -- 'cuisine','beverage','design','sustainability'
    term            TEXT NOT NULL,
    parent_term_id  UUID REFERENCES taxonomy_terms(term_id),
    synonyms        TEXT[],
    definition      TEXT,
    added_at        DATE NOT NULL DEFAULT CURRENT_DATE,
    active          BOOLEAN NOT NULL DEFAULT TRUE,
    UNIQUE (facet, term)
);

CREATE INDEX idx_tax_facet ON taxonomy_terms(facet) WHERE active;

CREATE TABLE menu_item_tags (
    item_id         UUID NOT NULL REFERENCES menu_items(item_id) ON DELETE CASCADE,
    term_id         UUID NOT NULL REFERENCES taxonomy_terms(term_id),
    confidence      NUMERIC(3,2) NOT NULL DEFAULT 0.80,
    extraction_id   UUID REFERENCES extractions(extraction_id),
    PRIMARY KEY (item_id, term_id)
);

CREATE INDEX idx_tags_term ON menu_item_tags(term_id);

-- Extraction output that did not map to a controlled term. Reviewed weekly;
-- frequent entries get promoted into taxonomy_terms.
CREATE TABLE taxonomy_unmapped (
    unmapped_id     UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    facet           TEXT NOT NULL,
    raw_value       TEXT NOT NULL,
    occurrence_count INT NOT NULL DEFAULT 1,
    first_seen_at   DATE NOT NULL DEFAULT CURRENT_DATE,
    last_seen_at    DATE NOT NULL DEFAULT CURRENT_DATE,
    resolved        BOOLEAN NOT NULL DEFAULT FALSE,
    mapped_to_term_id UUID REFERENCES taxonomy_terms(term_id),
    UNIQUE (facet, raw_value)
);

CREATE INDEX idx_unmapped_open ON taxonomy_unmapped(occurrence_count DESC) WHERE resolved = FALSE;

-- ============================================================
-- EVENT LAYER
-- ============================================================

CREATE TABLE events (
    event_id        UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    event_type      TEXT NOT NULL,          -- 'opening','closing','chef_move','award','funding',
                                            -- 'expansion','refurbishment','concept_change','relocation'
    primary_entity_id UUID REFERENCES entities(entity_id),
    secondary_entity_id UUID REFERENCES entities(entity_id),
    city            TEXT,
    headline        TEXT NOT NULL,
    detail          TEXT,
    amount          NUMERIC(14,2),          -- funding rounds, investment
    currency        CHAR(3),
    observed_at     DATE NOT NULL,
    retrieved_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    date_precision  date_precision NOT NULL DEFAULT 'exact',
    source_id       UUID REFERENCES sources(source_id),
    document_id     UUID REFERENCES documents(document_id),
    extraction_id   UUID REFERENCES extractions(extraction_id),
    method          extraction_method NOT NULL,
    confidence      NUMERIC(3,2) NOT NULL DEFAULT 0.80,
    verified_by     verification NOT NULL DEFAULT 'none'
);

CREATE INDEX idx_events_type_date ON events(event_type, observed_at DESC);
CREATE INDEX idx_events_entity    ON events(primary_entity_id, observed_at DESC);
CREATE INDEX idx_events_city      ON events(city, observed_at DESC);

-- ============================================================
-- SEMANTIC LAYER
-- ============================================================

CREATE TABLE embeddings (
    embedding_id    UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    object_type     TEXT NOT NULL,          -- 'menu_item','document_chunk','entity','event'
    object_id       UUID NOT NULL,
    chunk_index     INT DEFAULT 0,
    content         TEXT NOT NULL,
    embedding       vector(1024),
    model_id        TEXT NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_embeddings_object ON embeddings(object_type, object_id);
CREATE INDEX idx_embeddings_vec    ON embeddings USING hnsw (embedding vector_cosine_ops);

-- ============================================================
-- ANALYSIS LAYER
-- ============================================================

-- Computed trend measurements. Written by the statistics job, read by the Trend Analyst.
CREATE TABLE signals (
    signal_id       UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    term_id         UUID REFERENCES taxonomy_terms(term_id),
    city            TEXT,
    period_start    DATE NOT NULL,
    period_end      DATE NOT NULL,
    metric          TEXT NOT NULL,          -- 'venue_penetration','item_share','price_median','first_appearance'
    value           NUMERIC(12,4) NOT NULL,
    baseline_value  NUMERIC(12,4),
    z_score         NUMERIC(8,3),
    sample_size     INT NOT NULL,           -- denominator: how many venues/items in scope
    computed_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (term_id, city, period_start, period_end, metric)
);

CREATE INDEX idx_signals_z ON signals(z_score DESC) WHERE z_score IS NOT NULL;

-- The public prediction ledger. See 09-editorial-and-predictions.md.
CREATE TABLE predictions (
    prediction_id   UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    made_on         DATE NOT NULL,
    horizon_date    DATE NOT NULL,          -- when it becomes resolvable
    statement       TEXT NOT NULL,          -- must be falsifiable
    resolution_criteria TEXT NOT NULL,      -- written BEFORE the outcome is known
    basis           prediction_basis NOT NULL DEFAULT 'intuition',
                                            -- Phase 1 predictions are 'intuition' by definition.
                                            -- Q20 compares hit rates across this column; without
                                            -- it the control group is unidentifiable after the fact.
    confidence      NUMERIC(3,2) NOT NULL CHECK (confidence BETWEEN 0 AND 1),
    city            TEXT,
    term_id         UUID REFERENCES taxonomy_terms(term_id),
    supporting_signal_ids UUID[],
    published_in    TEXT,                   -- issue reference
    status          prediction_status NOT NULL DEFAULT 'open',
    resolved_on     DATE,
    resolution_note TEXT,
    CHECK (horizon_date > made_on)
);

CREATE INDEX idx_predictions_open ON predictions(horizon_date) WHERE status = 'open';

-- ============================================================
-- HELPER VIEWS
-- ============================================================

-- Current value of every venue attribute.
-- ---- Entity naming (D-043, D-047) -------------------------------------
-- ONE human string, for publication. display_name_provisional is TRUE until
-- the F2 pass captures the venue's own name -- while TRUE, publish no name.
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

-- EVERY variant, for matching -- Route B, press mentions, any outward join.
-- Reads through the trigram index on normalised_alias.
CREATE VIEW v_entity_all_names AS
SELECT ea.entity_id, ea.alias, ea.normalised_alias, ea.language, ea.source_id,
       ea.observed_at, ea.valid_from, ea.valid_to,
       (ea.valid_to IS NULL) AS current
FROM entity_aliases ea;

-- WHY BOTH: one string cannot serve both purposes. Publication wants one human
-- name; matching wants every variant. Collapsing them is how a matcher misses a
-- venue because the single canonical string happened to be the English one.
-- Copenhagen's frame already carries 14 name variants across 45 dual-route
-- venues -- 4 prefix, 8 orthography, 1 translation, 1 genuinely distinct name --
-- and 5 of the orthographic ones are case-only, which a naive normaliser
-- discards along with the venue's own styling (formel B, akme, a|o|c).

-- NOTE (D-047, unresolved): v_venue_current below returns venue facts and no
-- name, so any consumer wanting to publish a venue must reach into
-- entities.canonical_name -- the column this patch deprecates. Consumers should
-- join v_entity_display_name instead. Changing v_venue_current is a separate
-- decision and has not been made.

CREATE VIEW v_venue_current AS
SELECT DISTINCT ON (entity_id, attribute)
       entity_id, attribute, value_text, value_numeric, value_currency,
       observed_at, confidence, source_id
FROM venue_facts
WHERE valid_to IS NULL
ORDER BY entity_id, attribute, observed_at DESC;

-- Latest menu per venue per menu_type.
CREATE VIEW v_menu_latest AS
SELECT DISTINCT ON (entity_id, menu_type)
       menu_id, entity_id, menu_type, observed_at, item_count, currency, menu_price
FROM menus
ORDER BY entity_id, menu_type, observed_at DESC;

-- Publishable facts only: confident or verified.
CREATE VIEW v_menu_items_publishable AS
SELECT mi.*
FROM menu_items mi
JOIN menus m ON m.menu_id = mi.menu_id
WHERE mi.confidence >= 0.70
  AND m.date_precision <> 'inferred';

-- The Q20 test: do data-supported predictions beat intuition-only ones?
-- Denominator is included by construction — resolved predictions only, never open ones.
CREATE VIEW v_prediction_score AS
SELECT basis,
       COUNT(*)                                              AS resolved_count,
       COUNT(*) FILTER (WHERE status = 'correct')            AS correct_count,
       COUNT(*) FILTER (WHERE status = 'partial')            AS partial_count,
       ROUND(
         COUNT(*) FILTER (WHERE status = 'correct')::numeric
         / NULLIF(COUNT(*), 0), 3)                           AS hit_rate
FROM predictions
WHERE status IN ('correct','incorrect','partial')
GROUP BY basis;

-- Tag penetration by city and quarter: the core trend query.
CREATE VIEW v_tag_penetration AS
SELECT t.term_id,
       t.facet,
       t.term,
       e.city,
       date_trunc('quarter', mi.observed_at)::date AS period,
       COUNT(DISTINCT mi.entity_id)                AS venues_with_tag,
       COUNT(*)                                    AS item_count
FROM menu_item_tags mit
JOIN taxonomy_terms t ON t.term_id = mit.term_id
JOIN menu_items mi    ON mi.item_id = mit.item_id
JOIN entities e       ON e.entity_id = mi.entity_id
WHERE mit.confidence >= 0.70
GROUP BY t.term_id, t.facet, t.term, e.city, period;
