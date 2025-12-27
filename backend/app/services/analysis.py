from collections import defaultdict
from statistics import mean, pstdev
from typing import Iterable

from app.models.entities import VerdictStatus
from app.models.schemas import ShotCreate

REFERENCE_DOSE_GRAMS = 18.0
SENSORY_LABEL_TO_SCORE = {
    "absent": 1,
    "faible": 2,
    "leger": 2,
    "léger": 2,
    "doux": 3,
    "moyen": 3,
    "equilibre": 3,
    "équilibre": 3,
    "marque": 4,
    "marqué": 4,
    "prononce": 4,
    "prononcé": 4,
    "intense": 5,
    "punchy": 5,
    "sirupeux": 5,
    "sirupé": 5,
}

SENSORY_LABEL_TO_SCORE = {
    "insipide": 1,
    "doux": 2,
    "équilibré": 3,
    "expressif": 4,
    "intense": 5,
}


def label_to_score(label: str) -> int:
    normalized = label.lower().strip()
    if normalized not in SENSORY_LABEL_TO_SCORE:
        raise ValueError(f"unknown_label:{label}")
    return SENSORY_LABEL_TO_SCORE[normalized]


def score_to_label(score: int) -> str:
    bounded = max(1, min(5, score))
    for label, numeric in SENSORY_LABEL_TO_SCORE.items():
        if numeric == bounded:
            return label
    return "équilibré"


def mean_to_label(score: float) -> str:
    return score_to_label(round(score))


def compute_cost_per_shot(price_eur: float, bag_weight_grams: int, dose_grams: float = REFERENCE_DOSE_GRAMS) -> float:
    """Estimate the cost per shot based on price, bag weight and expected dose."""
    unit_price = price_eur / bag_weight_grams
    return round(unit_price * dose_grams, 2)


def compute_brew_ratio(shot: ShotCreate) -> float:
    """Return the brew ratio (beverage weight / dry dose)."""
    ratio = shot.beverage_weight_grams / shot.dose_in_grams
    return round(ratio, 2)


def compute_sensory_mean(scores: Iterable[int]) -> float:
    """Average the sensoriel scores to simplify downstream analysis."""
    return round(mean(list(scores)), 2)


def verdict_from_mean(score: float) -> VerdictStatus:
    scores = [
        tasting.acidity,
        tasting.bitterness,
        tasting.body,
        tasting.aroma,
        tasting.balance,
        tasting.finish,
        tasting.overall,
    ]
    return round(mean(scores), 2)


def label_to_score(label: str) -> int:
    """Convert a human-friendly sensory label into a numeric score between 1 and 5.

    The mapping is intentionally simple to keep the UI free of numbers while
    preserving a deterministic, testable scale in the backend.
    """

    normalized = _normalize_label(label)

    if normalized.isdigit():
        parsed = int(normalized)
        if 1 <= parsed <= 5:
            return parsed
    if normalized in SENSORY_LABEL_TO_SCORE:
        return SENSORY_LABEL_TO_SCORE[normalized]

    raise ValueError(f"Unknown sensory label: {label}")


def verdict_from_mean(score: float) -> str:
    """Map a sensory mean to a simple verdict."""
    if score >= 4.5:
        return VerdictStatus.RACHETER
    if score >= 3.5:
        return VerdictStatus.A_AFFINER
    if score >= 2.5:
        return VerdictStatus.EN_OBSERVATION
    return VerdictStatus.A_EVITER


def verdict_label(status: VerdictStatus) -> str:
    return {
        VerdictStatus.RACHETER: "racheter",
        VerdictStatus.A_AFFINER: "à affiner",
        VerdictStatus.EN_OBSERVATION: "en observation",
        VerdictStatus.A_EVITER: "à éviter",
    }.get(status, "en observation")


def stability_label(scores: list[float]) -> str:
    if len(scores) < 2:
        return "données insuffisantes"
    spread = pstdev(scores)
    if spread < 0.25:
        return "très stable"
    if spread < 0.5:
        return "assez stable"
    if spread < 1:
        return "variable"
    return "très variable"


def aggregate_quality_per_price(avg_quality: float, cost_per_shot: float) -> str:
    if cost_per_shot == 0:
        return "non renseigné"
    ratio = avg_quality / cost_per_shot
    if ratio >= 0.2:
        return "excellent rapport Q/P"
    if ratio >= 0.15:
        return "bon rapport Q/P"
    if ratio >= 0.1:
        return "moyen"
    return "défavorable"


def summarize_rankings(means_by_coffee: dict) -> list[tuple]:
    ordered = sorted(means_by_coffee.items(), key=lambda item: item[1]["mean"], reverse=True)
    enriched: list[tuple] = []
    for position, (coffee_id, payload) in enumerate(ordered, start=1):
        enriched.append((position, coffee_id, payload))
    return enriched


def summarize_retest_needed(tasting_counts: dict[object, int]) -> list[object]:
    return [coffee_id for coffee_id, count in tasting_counts.items() if count < 2]


def mean_by_key(items: Iterable[tuple[object, float]]) -> dict[object, float]:
    grouped: dict[object, list[float]] = defaultdict(list)
    for key, value in items:
        grouped[key].append(value)
    return {key: mean(values) for key, values in grouped.items()}
        return "en observation"
    return "à éviter"


def _normalize_label(label: str) -> str:
    return "".join(
        ch
        for ch in unicodedata.normalize("NFKD", label.strip().casefold())
        if unicodedata.category(ch) != "Mn"
    )
