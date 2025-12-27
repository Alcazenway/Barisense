-- Barisense - schéma initial Postgres
-- Cette migration définit les tables principales pour cafés, eaux, shots,
-- dégustations et verdicts afin d’assurer la traçabilité des réglages.

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE coffees (
    coffee_id       BIGSERIAL PRIMARY KEY,
    name            TEXT        NOT NULL,
    roaster         TEXT        NOT NULL,
    origin          TEXT        NOT NULL,
    variety         TEXT,
    process         TEXT,
    roast_level     TEXT        CHECK (roast_level IN ('light', 'medium', 'medium-dark', 'dark')),
    roast_date      DATE,
    altitude_meters INTEGER,
    flavor_notes    TEXT[],
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE waters (
    water_id            BIGSERIAL PRIMARY KEY,
    name                TEXT        NOT NULL,
    source              TEXT,
    tds_ppm             NUMERIC(6,2),
    hardness_ca_mg      NUMERIC(6,2),
    alkalinity_hco3     NUMERIC(6,2),
    ph                  NUMERIC(3,2),
    sodium_mg_l         NUMERIC(6,2),
    magnesium_mg_l      NUMERIC(6,2),
    notes               TEXT,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TYPE brew_method AS ENUM ('espresso', 'pourover', 'aeropress', 'cold_brew', 'moka');

CREATE TABLE shots (
    shot_id             BIGSERIAL PRIMARY KEY,
    coffee_id           BIGINT      NOT NULL REFERENCES coffees(coffee_id),
    water_id            BIGINT      NOT NULL REFERENCES waters(water_id),
    brew_method         brew_method NOT NULL,
    brew_date           DATE        NOT NULL DEFAULT CURRENT_DATE,
    dose_in_g           NUMERIC(5,2) NOT NULL CHECK (dose_in_g > 0),
    yield_out_g         NUMERIC(5,2) NOT NULL CHECK (yield_out_g > 0),
    brew_time_seconds   INTEGER      NOT NULL CHECK (brew_time_seconds > 0),
    grind_setting       TEXT,
    brew_temperature_c  NUMERIC(4,1),
    water_temperature_c NUMERIC(4,1),
    pressure_profile    JSONB,
    refractometer_tds   NUMERIC(4,2),
    extraction_yield    NUMERIC(4,2),
    ratio               NUMERIC(5,2) GENERATED ALWAYS AS (
        CASE WHEN dose_in_g > 0 THEN yield_out_g / dose_in_g END
    ) STORED,
    notes               TEXT,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE tastings (
    tasting_id          BIGSERIAL PRIMARY KEY,
    shot_id             BIGINT      NOT NULL REFERENCES shots(shot_id) ON DELETE CASCADE,
    taster_name         TEXT,
    aroma_score         SMALLINT    CHECK (aroma_score BETWEEN 0 AND 10),
    acidity_score       SMALLINT    CHECK (acidity_score BETWEEN 0 AND 10),
    sweetness_score     SMALLINT    CHECK (sweetness_score BETWEEN 0 AND 10),
    bitterness_score    SMALLINT    CHECK (bitterness_score BETWEEN 0 AND 10),
    body_score          SMALLINT    CHECK (body_score BETWEEN 0 AND 10),
    aftertaste_score    SMALLINT    CHECK (aftertaste_score BETWEEN 0 AND 10),
    balance_score       SMALLINT    CHECK (balance_score BETWEEN 0 AND 10),
    overall_score       SMALLINT    CHECK (overall_score BETWEEN 0 AND 10),
    comments            TEXT,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TYPE verdict_status AS ENUM ('excellent', 'good', 'needs_work', 'discard');

CREATE TABLE verdicts (
    verdict_id          BIGSERIAL PRIMARY KEY,
    shot_id             BIGINT      NOT NULL UNIQUE REFERENCES shots(shot_id) ON DELETE CASCADE,
    status              verdict_status NOT NULL,
    headline            TEXT        NOT NULL,
    rationale           TEXT,
    recommended_action  TEXT,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_shots_coffee_water ON shots (coffee_id, water_id);
CREATE INDEX idx_shots_brew_method ON shots (brew_method);
CREATE INDEX idx_tastings_shot_id ON tastings (shot_id);
CREATE INDEX idx_verdicts_status ON verdicts (status);
