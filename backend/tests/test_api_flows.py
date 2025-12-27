from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_shot_rejects_unknown_coffee() -> None:
    response = client.post(
        "/api/v1/shots",
        json={
            "coffee_id": str(uuid4()),
            "beverage_type": "expresso",
            "grind_setting": "7.0",
            "dose_in_grams": 18,
            "beverage_weight_grams": 40,
            "extraction_time_seconds": 29,
            "water_id": None,
            "notes": None,
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Café introuvable"


def test_create_tasting_rejects_unknown_shot() -> None:
    response = client.post(
        "/api/v1/tastings",
        json={
            "shot_id": str(uuid4()),
            "acidity": 3,
            "bitterness": 2,
            "body": 3,
            "aroma": 4,
            "balance": 3,
            "finish": 3,
            "overall": 3,
            "comments": "No matching shot",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Shot introuvable"
