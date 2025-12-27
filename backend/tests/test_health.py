def test_healthcheck_returns_ok(client) -> None:
    response = client.get("/health")
    payload = response.json()

    assert response.status_code == 200
    assert payload["status"] == "ok"
    assert "version" in payload


def test_coffee_lifecycle(client) -> None:
    # Create a coffee
    coffee_payload = {
        "name": "Test Espresso",
        "roaster": "Test Roastery",
        "reference": "Lot A",
        "format": "grain",
        "weight_grams": 250,
        "price_eur": 12.5,
        "purchased_at": "2024-06-01",
    }
    coffee_response = client.post("/api/v1/coffees", json=coffee_payload)
    created_coffee = coffee_response.json()

    assert coffee_response.status_code == 201
    assert created_coffee["name"] == coffee_payload["name"]
    assert created_coffee["cost_per_shot_eur"] > 0

    # Declare water
    water_response = client.post(
        "/api/v1/waters",
        json={"label": "Maison", "source": "robinet", "brand": None},
    )
    water = water_response.json()
    assert water_response.status_code == 201

    # Register a shot
    shot_payload = {
        "coffee_id": created_coffee["id"],
        "beverage_type": "expresso",
        "grind_setting": "10",
        "dose_in_grams": 18,
        "beverage_weight_grams": 36,
        "extraction_time_seconds": 28.5,
        "water_id": water["id"],
        "notes": None,
    }
    shot_response = client.post("/api/v1/shots", json=shot_payload)
    shot = shot_response.json()

    assert shot_response.status_code == 201
    assert shot["brew_ratio"] == 2.0

    # Record tasting
    tasting_payload = {
        "shot_id": shot["id"],
        "acidity_label": "équilibré",
        "bitterness_label": "doux",
        "body_label": "expressif",
        "aroma_label": "expressif",
        "balance_label": "équilibré",
        "finish_label": "équilibré",
        "overall_label": "expressif",
        "comments": "Crémeux, notes de chocolat",
    }
    tasting_response = client.post("/api/v1/tastings", json=tasting_payload)
    tasting = tasting_response.json()

    assert tasting_response.status_code == 201
    assert tasting["mean_label"]
    assert tasting["verdict_label"]


def test_authentication_guard(client) -> None:
    import os
    from app.core.config import get_settings

    os.environ["BARISENSE_API_KEY"] = "secret"
    get_settings.cache_clear()

    unauthorized = client.get("/api/v1/coffees")
    assert unauthorized.status_code == 401

    authorized = client.get("/api/v1/coffees", headers={"X-API-Key": "secret"})
    assert authorized.status_code == 200
