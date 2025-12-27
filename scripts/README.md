# Scripts

Outils d’import, d’export et de maintenance pour le dataset Barisense.

## Prérequis
- Python 3.11+
- Aucun package externe : tout repose sur la bibliothèque standard.

## Structure
- `cli.py` : point d’entrée CLI avec sous-commandes import/export/diagnostic.
- `dataset.py` : dataclasses centralisant les schémas de café/eau/shot/dégustation.
- `csv_io.py` : conversion CSV ↔︎ JSON.
- `diagnostics.py` : statistiques rapides (ratios, volumes, lacunes).

## Commandes principales

### Importer des CSV vers un dataset JSON
```bash
python -m scripts.cli import-csv \
  --coffees path/to/coffees.csv \
  --shots path/to/shots.csv \
  --tastings path/to/tastings.csv \
  --waters path/to/waters.csv \
  --output db/dataset.json
```

### Exporter un dataset JSON vers des CSV
```bash
python -m scripts.cli export-csv \
  --dataset db/dataset.json \
  --output-dir scripts/exports
```

### Afficher un diagnostic rapide
```bash
python -m scripts.cli summary --dataset db/dataset.json
```

## Schémas CSV attendus

### `coffees.csv`
| colonne        | type    | obligatoire | description                                 |
| -------------- | ------- | ----------- | ------------------------------------------- |
| id             | string  | oui         | Identifiant unique (slug ou UUID).          |
| name           | string  | oui         | Nom commercial.                             |
| roaster        | string  | oui         | Torréfacteur.                               |
| reference      | string  | non         | Référence / gamme.                          |
| type           | string  | non         | Grain / Moulu.                              |
| bag_weight_g   | int     | non         | Poids du paquet en grammes.                 |
| price_eur      | float   | non         | Prix payé en euros.                         |
| purchase_date  | string  | non         | Date d’achat (format libre).                |

### `waters.csv`
| colonne | type    | obligatoire | description                            |
| ------- | ------- | ----------- | -------------------------------------- |
| id      | string  | oui         | Identifiant unique.                    |
| label   | string  | oui         | Nom affiché (ex : Robinet, Volvic).    |
| source  | string  | non         | Origine libre (bouteille, osmose…).    |

### `shots.csv`
| colonne       | type    | obligatoire | description                                  |
| ------------- | ------- | ----------- | -------------------------------------------- |
| id            | string  | oui         | Identifiant unique du shot.                  |
| coffee_id     | string  | oui         | Référence le café utilisé.                   |
| water_id      | string  | non         | Référence l’eau utilisée.                    |
| beverage_type | string  | non         | Ristretto / Expresso / Long.                 |
| dose_g        | float   | non         | Dose sèche en grammes.                       |
| yield_g       | float   | non         | Liquéfaction en grammes.                     |
| duration_s    | float   | non         | Temps d’extraction en secondes.              |
| grind         | string  | non         | Réglage mouture (notation libre).            |

### `tastings.csv`
| colonne   | type   | obligatoire | description                                           |
| --------- | ------ | ----------- | ----------------------------------------------------- |
| id        | string | oui         | Identifiant unique de la dégustation.                 |
| shot_id   | string | oui         | Référence le shot dégusté.                            |
| acidity   | string | non         | Libellé d’acidité.                                    |
| bitterness| string | non         | Libellé d’amertume.                                   |
| body      | string | non         | Corps.                                                |
| aroma     | string | non         | Arômes.                                               |
| balance   | string | non         | Équilibre.                                            |
| finish    | string | non         | Longueur.                                             |
| overall   | string | non         | Appréciation globale.                                 |
| notes     | string | non         | Commentaires libres.                                  |

## Conseils d’usage
- Utiliser les mêmes identifiants entre fichiers (`coffee_id`, `shot_id`, `water_id`).
- Laisser les cellules vides pour les données inconnues : le script les transformera en `null` dans le JSON.
- Le diagnostic (`summary`) permet de vérifier rapidement la cohérence avant d’alimenter le backend ou les tests.

## Exemples prêts à l’emploi
Un jeu d’essai minimal est disponible dans `scripts/examples/`. Pour générer un dataset de démonstration :
```bash
python -m scripts.cli import-csv \
  --coffees scripts/examples/coffees.csv \
  --shots scripts/examples/shots.csv \
  --tastings scripts/examples/tastings.csv \
  --waters scripts/examples/waters.csv \
  --output db/dataset.json
```
