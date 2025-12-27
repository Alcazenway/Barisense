from uuid import uuid4

import pytest

from app.models.schemas import ShotCreate, TastingCreate
from app.services.analysis import (
    compute_brew_ratio,
    compute_cost_per_shot,
    compute_sensory_mean,
    label_to_score,
    verdict_from_mean,
)


def test_compute_cost_per_shot_uses_reference_dose() -> None:
    assert compute_cost_per_shot(price_eur=14.5, bag_weight_grams=250) == 1.04
    assert compute_cost_per_shot(price_eur=12.0, bag_weight_grams=250) == 0.86


def test_compute_brew_ratio_rounds_to_two_decimals() -> None:
    shot = ShotCreate(
        coffee_id=uuid4(),
        beverage_type="expresso",
        grind_setting="5.5",
        dose_in_grams=18.3,
        beverage_weight_grams=37.8,
        extraction_time_seconds=29.4,
        water_id=None,
        notes=None,
    )
    assert compute_brew_ratio(shot) == 2.07


def test_compute_sensory_mean_and_verdict() -> None:
    tasting = TastingCreate(
        shot_id=uuid4(),
        acidity=4,
        bitterness=2,
        body=5,
        aroma=5,
        balance=4,
        finish=4,
        overall=5,
        comments="rich and sweet",
    )
    mean = compute_sensory_mean(tasting)

    assert mean == 4.14
    assert verdict_from_mean(mean) == "à affiner"


@pytest.mark.parametrize(
    ("label", "expected"),
    [
        ("Absente", 1),
        ("faible", 2),
        ("léger", 2),
        ("Equilibre", 3),
        ("marqué", 4),
        ("Prononce", 4),
        ("INTENSE", 5),
        ("5", 5),
    ],
)
def test_label_to_score_accepts_common_labels(label: str, expected: int) -> None:
    assert label_to_score(label) == expected


def test_label_to_score_rejects_unknown_label() -> None:
    with pytest.raises(ValueError):
        label_to_score("mystery")
