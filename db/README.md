# DB

Schémas, migrations et dataset de test.

## Objectifs
- Modéliser les entités cafés, shots, dégustations, eaux et verdicts.
- Garantir la traçabilité des réglages et de l’impact de l’eau.
- Fournir un jeu de données ≥ 20 cafés et ≥ 100 shots pour valider les calculs.

## Choix techniques
- **SGBD** : Postgres (requis pour les types `ENUM`, les colonnes générées et les fonctions `jsonb_*` du seed).
- Les schémas utilisent des contraintes simples (CHECK 0-10 sur les scores) et des références fortes (`shots` → `coffees`/`waters`, `tastings`/`verdicts` → `shots`).
- Les profils d’eau sont stockés avec les minéraux clés pour suivre l’impact sur l’extraction.

## Structure
- `migrations/001_initial.sql` : création des tables `coffees`, `waters`, `shots`, `tastings`, `verdicts` et des `ENUM` `brew_method` / `verdict_status`.
- `seeds/demo_dataset.sql` : dataset de démonstration (20 cafés, 6 profils d’eau, 100 shots, 100 dégustations, 100 verdicts).

## Exécution
1. Appliquer la migration sur votre base Postgres :
   ```bash
   psql "$DATABASE_URL" -f db/migrations/001_initial.sql
   ```
2. Charger le dataset de test (ré-exécutable grâce au `TRUNCATE ... RESTART IDENTITY`) :
   ```bash
   psql "$DATABASE_URL" -f db/seeds/demo_dataset.sql
   ```

## Notes
- La colonne `ratio` des shots est générée automatiquement (`yield_out_g / dose_in_g`) pour faciliter les calculs.
- Les verdicts sont dérivés des dégustations seedées : `excellent/good/needs_work/discard` selon le score global.
