-- Jeu de données de démonstration aligné sur le schéma v1
-- Réexécutable grâce au TRUNCATE CASCADE

TRUNCATE TABLE tastings, shots, verdicts, waters, coffees RESTART IDENTITY CASCADE;

-- Coffees
INSERT INTO coffees (id, name, roaster, reference, format, weight_grams, price_eur, purchased_at, cost_per_shot_eur)
VALUES
    ('c78745f8-0c7a-4a23-9c21-7cf9928476e2', 'Monte Verde', 'Loma', 'Lot 12', 'grain', 250, 14.50, '2024-05-01', 1.04),
    ('5adf4e35-86b8-4a4a-a538-4d6d87a8d30d', 'Kaffa Bloom', 'Oslo', 'Micro-lot', 'grain', 200, 12.00, '2024-04-15', 1.08),
    ('6f0b17d3-3a90-40b5-85a7-5d1cd9c9c8b0', 'Noir Urbain', 'Brûlerie 64', 'Batch Nuit', 'moulu', 250, 9.00, '2024-06-02', 0.65);

-- Waters
INSERT INTO waters (id, label, source, brand)
VALUES
    ('5f39de5d-a8c9-4bc0-9e94-a76090beacf9', 'Maison', 'robinet', NULL),
    ('d0726916-fb62-44a8-80f0-3c311f7febad', 'Volvic', 'bouteille', 'Volvic');

-- Shots
INSERT INTO shots (id, coffee_id, water_id, beverage_type, grind_setting, dose_in_grams, beverage_weight_grams, extraction_time_seconds, brew_ratio, notes)
VALUES
    ('587a0e63-a2d9-47c7-9f9d-4a7d0cc6ec84', 'c78745f8-0c7a-4a23-9c21-7cf9928476e2', '5f39de5d-a8c9-4bc0-9e94-a76090beacf9', 'ristretto', '10', 18, 32, 27, 1.78, 'Ristrettos serrés'),
    ('6b0bd4ba-7510-4828-9956-9e40f0c3d48c', 'c78745f8-0c7a-4a23-9c21-7cf9928476e2', 'd0726916-fb62-44a8-80f0-3c311f7febad', 'expresso', '11', 18, 38, 29, 2.11, 'Expresso classique'),
    ('2ac1d367-26fb-4f8d-907d-4d567ad9fe9a', '5adf4e35-86b8-4a4a-a538-4d6d87a8d30d', 'd0726916-fb62-44a8-80f0-3c311f7febad', 'expresso', '9', 17.5, 34, 30, 1.94, 'Tirage fluide'),
    ('a1c9c9d1-16b1-43e5-9a4d-5c6b0f50b4e1', '6f0b17d3-3a90-40b5-85a7-5d1cd9c9c8b0', '5f39de5d-a8c9-4bc0-9e94-a76090beacf9', 'ristretto', '13', 18.2, 33, 28, 1.81, 'Shot rapide');

-- Tastings (scores numériques uniquement, jamais renvoyés au front)
INSERT INTO tastings (id, shot_id, acidity_score, bitterness_score, body_score, aroma_score, balance_score, finish_score, overall_score, sensory_mean, comments)
VALUES
    ('a54f8ead-6f87-4ca4-9c10-5b05c2e331d5', '587a0e63-a2d9-47c7-9f9d-4a7d0cc6ec84', 4, 3, 4, 4, 4, 4, 4, 3.86, 'Beaucoup de chocolat, pointe de fruits secs'),
    ('1e7e368d-2f24-4a69-9f6d-7d7eb3b2af64', '6b0bd4ba-7510-4828-9956-9e40f0c3d48c', 5, 4, 4, 5, 4, 4, 5, 4.43, 'Crème généreuse, acidité maîtrisée'),
    ('a9ad9cb1-61a6-4a15-86a8-8d40c20997d2', '2ac1d367-26fb-4f8d-907d-4d567ad9fe9a', 2, 2, 3, 2, 3, 2, 3, 2.43, 'Sous-extraction ressentie'),
    ('a4c57f3b-27cf-4dd0-b28c-17fa7db07075', 'a1c9c9d1-16b1-43e5-9a4d-5c6b0f50b4e1', 3, 3, 3, 3, 3, 3, 3, 3.00, 'Profil neutre à retravailler');

-- Verdicts calculés
INSERT INTO verdicts (id, coffee_id, status, rationale)
VALUES
    ('15f8781f-4c44-44f5-9f28-d43b9b2116ed', 'c78745f8-0c7a-4a23-9c21-7cf9928476e2', 'a_affiner', 'Derniers shots très expressifs, poursuivre l\'optimisation'),
    ('d3adf3ef-f030-4dd5-9c3e-11552d2c8e7b', '5adf4e35-86b8-4a4a-a538-4d6d87a8d30d', 'a_eviter', 'Rendu irrégulier malgré l\'eau en bouteille'),
    ('8783a2d0-cb3a-4e9a-9e85-9ee20a2b67a3', '6f0b17d3-3a90-40b5-85a7-5d1cd9c9c8b0', 'en_observation', 'Profil stable mais encore neutre');
