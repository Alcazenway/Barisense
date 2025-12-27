-- Barisense - schéma aligné avec les modèles FastAPI/SQLAlchemy
-- Entités : cafés, eaux, shots, dégustations, verdicts.

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

DO $$ BEGIN
    CREATE TYPE coffee_format AS ENUM ('grain', 'moulu');
EXCEPTION
    WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
    CREATE TYPE water_source AS ENUM ('robinet', 'bouteille');
EXCEPTION
    WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
    CREATE TYPE beverage_type AS ENUM ('ristretto', 'expresso', 'cafe_long');
EXCEPTION
    WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
    CREATE TYPE verdict_status AS ENUM ('racheter', 'a_affiner', 'en_observation', 'a_eviter');
EXCEPTION
    WHEN duplicate_object THEN NULL;
END $$;

CREATE TABLE IF NOT EXISTS coffees (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name                TEXT        NOT NULL,
    roaster             TEXT        NOT NULL,
    reference           TEXT,
    format              coffee_format NOT NULL,
    weight_grams        INTEGER     NOT NULL CHECK (weight_grams > 0),
    price_eur           NUMERIC(8,2) NOT NULL CHECK (price_eur > 0),
    purchased_at        DATE        NOT NULL,
    cost_per_shot_eur   NUMERIC(8,2) NOT NULL,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS waters (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    label       TEXT        NOT NULL,
    source      water_source NOT NULL,
    brand       TEXT,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS shots (
    id                      UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    coffee_id               UUID        NOT NULL REFERENCES coffees(id) ON DELETE CASCADE,
    water_id                UUID        REFERENCES waters(id) ON DELETE SET NULL,
    beverage_type           beverage_type NOT NULL,
    grind_setting           TEXT        NOT NULL,
    dose_in_grams           NUMERIC(5,2) NOT NULL CHECK (dose_in_grams > 0),
    beverage_weight_grams   NUMERIC(5,2) NOT NULL CHECK (beverage_weight_grams > 0),
    extraction_time_seconds NUMERIC(5,2) NOT NULL CHECK (extraction_time_seconds > 0),
    brew_ratio              NUMERIC(5,2) NOT NULL,
    notes                   TEXT,
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_shots_coffee ON shots(coffee_id);
CREATE INDEX IF NOT EXISTS idx_shots_water_beverage ON shots(water_id, beverage_type);

CREATE TABLE IF NOT EXISTS tastings (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    shot_id         UUID        NOT NULL REFERENCES shots(id) ON DELETE CASCADE,
    acidity_score   SMALLINT    NOT NULL CHECK (acidity_score BETWEEN 1 AND 5),
    bitterness_score SMALLINT   NOT NULL CHECK (bitterness_score BETWEEN 1 AND 5),
    body_score      SMALLINT    NOT NULL CHECK (body_score BETWEEN 1 AND 5),
    aroma_score     SMALLINT    NOT NULL CHECK (aroma_score BETWEEN 1 AND 5),
    balance_score   SMALLINT    NOT NULL CHECK (balance_score BETWEEN 1 AND 5),
    finish_score    SMALLINT    NOT NULL CHECK (finish_score BETWEEN 1 AND 5),
    overall_score   SMALLINT    NOT NULL CHECK (overall_score BETWEEN 1 AND 5),
    sensory_mean    NUMERIC(3,2) NOT NULL,
    comments        TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_tastings_shot ON tastings(shot_id);

CREATE TABLE IF NOT EXISTS verdicts (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    coffee_id   UUID        NOT NULL REFERENCES coffees(id) ON DELETE CASCADE,
    status      verdict_status NOT NULL,
    rationale   TEXT,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_verdict_coffee UNIQUE (coffee_id)
);

CREATE INDEX IF NOT EXISTS idx_verdict_status ON verdicts(status);
