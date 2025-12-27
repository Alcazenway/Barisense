# DB

Schémas, migrations et dataset de test.

## Objectifs
- Modéliser les entités cafés, shots, dégustations, eaux et verdicts.
- Garantir la traçabilité des réglages et de l’impact de l’eau.
- Fournir un jeu de données ≥ 20 cafés et ≥ 100 shots pour valider les calculs.

## Choix techniques
- **SGBD** : Postgres (requis pour les `ENUM` et le support natif UUID).
- Contraintes fortes (`CHECK 1-5` pour les scores sensoriels, FK en cascade) et index ciblés (`shots` par café/eau/type, `tastings` par shot, `verdicts` par statut).
- Le backend peut fonctionner sur SQLite pour les tests rapides ; Postgres reste la cible de prod.

## Structure
- `migrations/001_initial.sql` : création des tables `coffees`, `waters`, `shots`, `tastings`, `verdicts` avec leurs enums (`coffee_format`, `water_source`, `beverage_type`, `verdict_status`) et index nécessaires pour les filtres par eau et classements.
- `seeds/demo_dataset.sql` : dataset de démonstration cohérent avec l’API actuelle (coffees/eaux/shots/tastings/verdicts).

## Exécution
1. Appliquer la migration sur votre base Postgres :
   ```bash
   psql "$DATABASE_URL" -f db/migrations/001_initial.sql
   ```
2. Charger le dataset de test (ré-exécutable grâce au `TRUNCATE ... RESTART IDENTITY`) :
   ```bash
   psql "$DATABASE_URL" -f db/seeds/demo_dataset.sql
   ```

3. Utiliser le JSON léger pour des tests locaux ou des imports rapides :
   - Le fichier `db/demo_dataset.json` est prêt à l’emploi et peut être consommé par les utilitaires du dossier `scripts/` ou adapté pour précharger un dépôt en mémoire côté backend.
   - Vous pouvez aussi regénérer un dataset à partir des CSV d’exemple :
     ```bash
     python -m scripts.cli import-csv \
       --coffees scripts/examples/coffees.csv \
       --shots scripts/examples/shots.csv \
       --tastings scripts/examples/tastings.csv \
       --waters scripts/examples/waters.csv \
       --output db/demo_dataset.json
     ```

## Notes
- La colonne `ratio` des shots est générée automatiquement (`yield_out_g / dose_in_g`) pour faciliter les calculs.
- Les verdicts sont dérivés des dégustations seedées : `excellent/good/needs_work/discard` selon le score global.
