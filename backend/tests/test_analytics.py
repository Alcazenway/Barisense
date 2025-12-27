from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def _create_coffee(name: str) -> dict:
    payload = {
        "name": name,
        "roaster": "Test Roastery",
        "reference": None,
        "format": "grain",
        "weight_grams": 250,
        "price_eur": 14.5,
        "purchased_at": "2024-06-10",
    }
    response = client.post("/api/v1/coffees", json=payload)
    assert response.status_code == 201
    return response.json()


def _create_water(label: str, mineralization: float) -> dict:
    payload = {
        "label": label,
        "source": "bouteille",
        "brand": label,
        "mineralization_ppm": mineralization,
        "hardness_ca_mg_l": mineralization / 3,
        "alkalinity_hco3_mg_l": mineralization / 2,
        "ph": 7.2,
        "filter_type": "Test",
    }
    response = client.post("/api/v1/waters", json=payload)
    assert response.status_code == 201
    return response.json()


def _create_shot(coffee_id: str, water_id: str, beverage_type: str, ratio: float, time_s: float, grind: str) -> dict:
    dose = 18.0
    payload = {
        "coffee_id": coffee_id,
        "beverage_type": beverage_type,
        "grind_setting": grind,
        "dose_in_grams": dose,
        "beverage_weight_grams": ratio * dose,
        "extraction_time_seconds": time_s,
        "water_id": water_id,
        "notes": None,
    }
    response = client.post("/api/v1/shots", json=payload)
    assert response.status_code == 201
    return response.json()


def _create_tasting(shot_id: str, base_score: int) -> dict:
    payload = {
        "shot_id": shot_id,
        "acidity": min(5, base_score),
        "bitterness": max(1, base_score - 1),
        "body": min(5, base_score + 1),
        "aroma": min(5, base_score + 1),
        "balance": min(5, base_score),
        "finish": min(5, base_score),
        "overall": min(5, base_score + 1),
        "comments": "Test tasting",
    }
    response = client.post("/api/v1/tastings", json=payload)
    assert response.status_code == 201
    return response.json()


def test_analytics_summary_exposes_diagnostics_and_rankings() -> None:
    coffee_a = _create_coffee("Analytics A")
    coffee_b = _create_coffee("Analytics B")

    water_soft = _create_water("Douce", 60.0)
    water_mineral = _create_water("Minérale", 190.0)

    shot_a1 = _create_shot(coffee_a["id"], water_soft["id"], "expresso", ratio=2.0, time_s=28.0, grind="8")
    shot_a2 = _create_shot(coffee_a["id"], water_mineral["id"], "cafe_long", ratio=2.9, time_s=32.0, grind="11")
    shot_b1 = _create_shot(coffee_b["id"], water_soft["id"], "ristretto", ratio=1.6, time_s=25.0, grind="7")

    _create_tasting(shot_a1["id"], base_score=4)
    _create_tasting(shot_a2["id"], base_score=3)
    _create_tasting(shot_b1["id"], base_score=5)

    response = client.get("/api/v1/analytics")
    assert response.status_code == 200

    payload = response.json()
    assert len(payload["coffees"]) == 2
    assert payload["water_rankings"][0]["rank"] == 1

    coffee_block = next(c for c in payload["coffees"] if c["coffee"]["id"] == coffee_a["id"])
    assert coffee_block["extraction_history"]
    assert coffee_block["parameter_suggestions"]
    assert coffee_block["global_score"]["verdict"] in ["racheter", "à affiner", "en observation", "à éviter"]

    water_impacts = coffee_block["water_impacts"]
    assert any(impact["classification"] == "faible minéralisation" for impact in water_impacts)
    assert any(impact["classification"] == "fortement minéralisée" for impact in water_impacts)
