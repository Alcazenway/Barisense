import unicodedata
from statistics import mean

from app.models.schemas import ShotCreate, TastingCreate

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


def compute_cost_per_shot(price_eur: float, bag_weight_grams: int, dose_grams: float = REFERENCE_DOSE_GRAMS) -> float:
    """Estimate the cost per shot based on price, bag weight and expected dose."""
    unit_price = price_eur / bag_weight_grams
    return round(unit_price * dose_grams, 2)


def compute_brew_ratio(shot: ShotCreate) -> float:
    """Return the brew ratio (beverage weight / dry dose)."""
    ratio = shot.beverage_weight_grams / shot.dose_in_grams
    return round(ratio, 2)


def compute_sensory_mean(tasting: TastingCreate) -> float:
    """Average the sensoriel scores to simplify downstream analysis."""
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
        return "racheter"
    if score >= 3.5:
        return "à affiner"
    if score >= 2.5:
        return "en observation"
    return "à éviter"


def _normalize_label(label: str) -> str:
    return "".join(
        ch
        for ch in unicodedata.normalize("NFKD", label.strip().casefold())
        if unicodedata.category(ch) != "Mn"
    )
