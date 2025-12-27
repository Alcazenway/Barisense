"""
Génère un jeu de données synthétique pour tester les calculs Barisense.

- >=20 cafés, >=100 shots, variation de l'eau et des ratios.
- Compatible avec le dépôt mémoire (JSON) ou pour pré-remplir une base.
"""

from __future__ import annotations

import json
import random
from datetime import datetime, timedelta
from pathlib import Path
from uuid import uuid4


def build_waters() -> list[dict]:
    return [
        {
            "id": str(uuid4()),
            "label": "Osmosée",
            "source": "robinet",
            "brand": None,
            "mineralization_ppm": 65.0,
            "hardness_ca_mg_l": 22.0,
            "alkalinity_hco3_mg_l": 38.0,
            "ph": 7.2,
            "filter_type": "Osmose + reminéralisation",
        },
        {
            "id": str(uuid4()),
            "label": "Volvic",
            "source": "bouteille",
            "brand": "Volvic",
            "mineralization_ppm": 110.0,
            "hardness_ca_mg_l": 30.0,
            "alkalinity_hco3_mg_l": 70.0,
            "ph": 7.0,
            "filter_type": "Naturelle",
        },
        {
            "id": str(uuid4()),
            "label": "Robinet filtrée",
            "source": "robinet",
            "brand": None,
            "mineralization_ppm": 140.0,
            "hardness_ca_mg_l": 45.0,
            "alkalinity_hco3_mg_l": 90.0,
            "ph": 7.5,
            "filter_type": "Brita",
        },
        {
            "id": str(uuid4()),
            "label": "Cristalline",
            "source": "bouteille",
            "brand": "Cristalline",
            "mineralization_ppm": 180.0,
            "hardness_ca_mg_l": 70.0,
            "alkalinity_hco3_mg_l": 110.0,
            "ph": 7.4,
            "filter_type": "Naturelle",
        },
    ]


def build_coffees() -> list[dict]:
    names = [
        ("Santa Barbara", "Prolog"),
        ("Kochere", "Tim Wendelboe"),
        ("Chelbesa", "Drop Coffee"),
        ("Nariño", "Colonna"),
        ("Kamwangi AA", "Kiss The Hippo"),
        ("Carmo", "Sey"),
        ("La Esperanza", "La Cabra"),
        ("Kayon Mountain", "Onyx"),
        ("Huehuetenango", "Caféothèque"),
        ("San Ignacio", "Gardelli"),
        ("Aricha", "Bonanza"),
        ("Kigoma", "Standout"),
        ("El Paraiso", "Friedhats"),
        ("Biftu Gudina", "Coffee Collective"),
        ("Sierra Mazateca", "April"),
        ("Tarrazú", "Square Mile"),
        ("Huila", "Coutume"),
        ("Shakiso", "Morgon"),
        ("Kiambu PB", "Five Elephant"),
        ("Kayanza", "La Main Noire"),
    ]
    coffees = []
    purchase_base = datetime(2024, 2, 1)
    for idx, (name, roaster) in enumerate(names):
        coffees.append(
            {
                "id": str(uuid4()),
                "name": name,
                "roaster": roaster,
                "reference": f"L{idx+1:02d}",
                "format": "grain",
                "weight_grams": 250,
                "price_eur": round(10 + idx * 0.4, 2),
                "purchased_at": (purchase_base + timedelta(days=idx)).date().isoformat(),
            }
        )
    return coffees


def build_shots(coffees: list[dict], waters: list[dict], nb: int = 120) -> list[dict]:
    random.seed(42)
    beverage_types = ["expresso", "ristretto", "cafe_long"]
    shots: list[dict] = []
    start = datetime(2024, 3, 1)
    for idx in range(nb):
        coffee = coffees[idx % len(coffees)]
        water = random.choice(waters)
        beverage_type = random.choice(beverage_types)
        dose = round(17.5 + (idx % 5) * 0.3, 2)
        target_ratio = 2.0 if beverage_type == "expresso" else 1.7 if beverage_type == "ristretto" else 2.7
        ratio_variation = random.uniform(-0.15, 0.18)
        brew_ratio = round(target_ratio + ratio_variation, 2)
        beverage_weight = round(dose * brew_ratio, 2)
        extraction_time = round(random.uniform(23.0, 35.0), 1)
        shots.append(
            {
                "id": str(uuid4()),
                "coffee_id": coffee["id"],
                "water_id": water["id"],
                "beverage_type": beverage_type,
                "grind_setting": f"{8 + (idx % 6)}",
                "dose_in_grams": dose,
                "beverage_weight_grams": beverage_weight,
                "extraction_time_seconds": extraction_time,
                "notes": f"Shot synthétique #{idx+1}",
                "created_at": (start + timedelta(hours=idx)).isoformat(),
            }
        )
    return shots


def build_tastings(shots: list[dict]) -> list[dict]:
    tastings: list[dict] = []
    random.seed(84)
    for shot in shots:
        # Favorise légèrement les shots proches de 2:1
        bias = 0.4 if 1.8 <= shot["beverage_weight_grams"] / shot["dose_in_grams"] <= 2.4 else 0
        base_score = random.randint(2, 5)
        tasting_scores = {
            "acidity": min(5, base_score + random.choice([0, 1])),
            "bitterness": max(1, base_score - random.choice([0, 1])),
            "body": min(5, base_score + random.choice([0, 1])),
            "aroma": min(5, base_score + bias),
            "balance": min(5, base_score + random.choice([0, 1])),
            "finish": min(5, base_score + random.choice([0, 1])),
            "overall": min(5, base_score + random.choice([0, 1])),
        }
        tastings.append(
            {
                "id": str(uuid4()),
                "shot_id": shot["id"],
                "comments": "Tasting synthétique",
                **{key: int(value) for key, value in tasting_scores.items()},
                "created_at": shot["created_at"],
            }
        )
    return tastings


def generate_dataset() -> dict:
    waters = build_waters()
    coffees = build_coffees()
    shots = build_shots(coffees, waters)
    tastings = build_tastings(shots)
    return {"waters": waters, "coffees": coffees, "shots": shots, "tastings": tastings}


def main() -> None:
    dataset = generate_dataset()
    output_path = Path(__file__).parent / "mock_dataset.json"
    output_path.write_text(json.dumps(dataset, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Dataset généré: {output_path} ({len(dataset['coffees'])} cafés, {len(dataset['shots'])} shots)")


if __name__ == "__main__":
    main()
