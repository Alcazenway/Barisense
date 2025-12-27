-- Jeu de données de démonstration pour valider les calculs Barisense
-- Compatible Postgres : à exécuter après la migration 001_initial.sql

BEGIN;

-- Nettoyage pour rejouer le seed sans doublons
TRUNCATE verdicts, tastings, shots, waters, coffees RESTART IDENTITY CASCADE;

INSERT INTO waters (name, source, tds_ppm, hardness_ca_mg, alkalinity_hco3, ph, sodium_mg_l, magnesium_mg_l, notes) VALUES
('Osmosée reminéralisée', 'Filtration maison', 75, 25, 40, 7.2, 8, 4, 'Profil Langelier légèrement positif'),
('Cristalline', 'Eau en bouteille', 160, 40, 65, 7.4, 12, 9, 'Base neutre pour espresso'),
('Volvic', 'Eau en bouteille', 110, 10, 60, 7.0, 11, 8, 'Bon compromis pour V60'),
('Robinet filtrée', 'Brita', 130, 35, 70, 7.6, 15, 6, 'Variable selon cartouche'),
('Tiers-lieu', 'Réseau local', 200, 60, 90, 7.8, 20, 14, 'Suivre la dérive saisonnière'),
('Low-TDS compétition', 'Osmose + buffers', 60, 18, 35, 7.1, 6, 3, 'Profil pour cafés délicats');

INSERT INTO coffees (name, roaster, origin, variety, process, roast_level, roast_date, altitude_meters, flavor_notes) VALUES
('Santa Barbara', 'Prolog', 'Honduras', 'Pacas', 'Washed', 'light', '2024-02-20', 1450, ARRAY['cacao', 'prune', 'vanille']),
('Kochere', 'Tim Wendelboe', 'Ethiopia', 'Heirloom', 'Washed', 'light', '2024-02-25', 1950, ARRAY['bergamote', 'fleurs blanches', 'citron']),
('Chelbesa', 'Drop Coffee', 'Ethiopia', 'Heirloom', 'Natural', 'light', '2024-02-15', 2000, ARRAY['fraise', 'jasmin', 'miel']),
('Nariño', 'Colonna', 'Colombia', 'Caturra', 'Washed', 'medium', '2024-02-18', 1800, ARRAY['pomme', 'caramel', 'noisette']),
('Kamwangi AA', 'Kiss The Hippo', 'Kenya', 'SL28', 'Washed', 'light', '2024-02-22', 1900, ARRAY['cassis', 'pamplemousse', 'canneberge']),
('Carmo', 'Sey', 'Brazil', 'Yellow Bourbon', 'Pulped natural', 'medium', '2024-02-17', 1250, ARRAY['noix', 'chocolat au lait', 'sucre brun']),
('La Esperanza', 'La Cabra', 'Colombia', 'Castillo', 'Washed', 'light', '2024-02-19', 1750, ARRAY['floral', 'miel', 'abricot']),
('Kayon Mountain', 'Onyx', 'Ethiopia', 'Guji heirloom', 'Natural', 'light', '2024-02-16', 1900, ARRAY['fraise', 'banane', 'cacao']),
('Huehuetenango', 'Caféothèque', 'Guatemala', 'Bourbon', 'Washed', 'medium', '2024-02-21', 1700, ARRAY['caramel', 'pomme verte', 'cannelle']),
('San Ignacio', 'Gardelli', 'Peru', 'Typica', 'Washed', 'light', '2024-02-14', 1850, ARRAY['fleur d''oranger', 'pêche', 'noix']),
('Aricha', 'Bonanza', 'Ethiopia', 'Heirloom', 'Natural', 'light', '2024-02-12', 2000, ARRAY['myrtille', 'chocolat noir', 'fleurs']),
('Kigoma', 'Standout', 'Rwanda', 'Red Bourbon', 'Washed', 'light', '2024-02-23', 1780, ARRAY['fruits rouges', 'thé noir', 'miel']),
('El Paraiso', 'Friedhats', 'Colombia', 'Pink Bourbon', 'Anaerobic', 'light', '2024-02-10', 1650, ARRAY['litchi', 'rose', 'bonbon']),
('Biftu Gudina', 'Coffee Collective', 'Ethiopia', 'Heirloom', 'Washed', 'light', '2024-02-11', 1900, ARRAY['citron', 'jasmin', 'pêche']),
('Sierra Mazateca', 'April', 'Mexico', 'Mixteca', 'Washed', 'medium', '2024-02-09', 1550, ARRAY['cacao', 'amande', 'miel']),
('Tarrazú', 'Square Mile', 'Costa Rica', 'Catuai', 'Honey', 'medium', '2024-02-08', 1700, ARRAY['praliné', 'pêche', 'orange']),
('Huila', 'Coutume', 'Colombia', 'Caturra', 'Washed', 'medium', '2024-02-13', 1750, ARRAY['caramel', 'fruits secs', 'cacao']),
('Shakiso', 'Morgon', 'Ethiopia', 'Heirloom', 'Natural', 'light', '2024-02-07', 1950, ARRAY['mangue', 'ananas', 'fraise']),
('Kiambu PB', 'Five Elephant', 'Kenya', 'SL34', 'Washed', 'light', '2024-02-05', 1900, ARRAY['cassis', 'citron vert', 'sucre roux']),
('Kayanza', 'La Main Noire', 'Burundi', 'Red Bourbon', 'Washed', 'light', '2024-02-04', 1800, ARRAY['floral', 'agrumes', 'miel']);

WITH base_shots AS (
    SELECT
        gs AS seq,
        ((gs - 1) % 20) + 1 AS coffee_id,
        ((gs - 1) % 6) + 1 AS water_id,
        (ARRAY['espresso'::brew_method, 'pourover', 'aeropress', 'cold_brew', 'moka'])[((gs - 1) % 5) + 1] AS brew_method,
        DATE '2024-03-01' + ((gs - 1) % 45) AS brew_date,
        ROUND(17.5 + ((gs - 1) % 6) * 0.5, 2) AS dose_in_g,
        ROUND(32 + ((gs - 1) % 6) * 1.8 + (((gs - 1) / 10)::INT) * 0.2, 2) AS yield_out_g,
        24 + ((gs - 1) % 25) AS brew_time_seconds,
        'G-' || ((gs - 1) % 24) AS grind_setting,
        91 + ((gs - 1) % 5) AS brew_temperature_c,
        18 + ((gs - 1) % 7) AS water_temperature_c,
        jsonb_build_object('profile', 'flat', 'peak_pressure_bar', 8.5 + ((gs - 1) % 4)) AS pressure_profile,
        ROUND(8.2 + ((gs - 1) % 7) * 0.10, 2) AS refractometer_tds
    FROM generate_series(1, 100) AS gs
)
INSERT INTO shots (
    coffee_id, water_id, brew_method, brew_date, dose_in_g, yield_out_g, brew_time_seconds,
    grind_setting, brew_temperature_c, water_temperature_c, pressure_profile, refractometer_tds,
    extraction_yield, notes
)
SELECT
    coffee_id,
    water_id,
    brew_method,
    brew_date,
    dose_in_g,
    yield_out_g,
    brew_time_seconds,
    grind_setting,
    brew_temperature_c,
    water_temperature_c,
    pressure_profile,
    refractometer_tds,
    ROUND((refractometer_tds * (yield_out_g / dose_in_g) * 0.01)::NUMERIC, 2) AS extraction_yield,
    'Profil ' || brew_method || ' café ' || coffee_id || ', shot #' || seq
FROM base_shots;

WITH tasting_base AS (
    SELECT
        shot_id,
        'Taster ' || (((shot_id - 1) % 5) + 1) AS taster_name,
        6 + ((shot_id - 1) % 5) AS aroma,
        5 + ((shot_id - 1) % 4) AS acidity,
        6 + ((shot_id - 1) % 4) AS sweetness,
        3 + ((shot_id - 1) % 4) AS bitterness,
        5 + ((shot_id - 1) % 5) AS body,
        5 + ((shot_id - 1) % 4) AS aftertaste,
        6 + ((shot_id - 1) % 3) AS balance
    FROM shots
)
INSERT INTO tastings (
    shot_id, taster_name, aroma_score, acidity_score, sweetness_score, bitterness_score,
    body_score, aftertaste_score, balance_score, overall_score, comments
)
SELECT
    shot_id,
    taster_name,
    aroma,
    acidity,
    sweetness,
    bitterness,
    body,
    aftertaste,
    balance,
    LEAST(10, ROUND(((aroma + acidity + sweetness + body + aftertaste + balance) / 6.0)::NUMERIC, 0)) AS overall_score,
    'Session calibrée - impression ' || taster_name
FROM tasting_base;

INSERT INTO verdicts (shot_id, status, headline, rationale, recommended_action)
SELECT
    t.shot_id,
    CASE
        WHEN t.overall_score >= 9 THEN 'excellent'::verdict_status
        WHEN t.overall_score >= 8 THEN 'good'::verdict_status
        WHEN t.overall_score >= 6 THEN 'needs_work'::verdict_status
        ELSE 'discard'::verdict_status
    END,
    'Score ' || t.overall_score || '/10',
    'Basé sur la dégustation ' || t.taster_name || ' avec ratio ' || s.ratio,
    CASE
        WHEN t.overall_score >= 8 THEN 'Stabiliser la recette et documenter.'
        WHEN t.overall_score >= 6 THEN 'Ajuster mouture et temps d''extraction.'
        ELSE 'Changer d''eau ou revoir la torréfaction.'
    END
FROM tastings t
JOIN shots s ON s.shot_id = t.shot_id;

COMMIT;
