from statistics import mean

from app.models.schemas import ShotCreate, TastingCreate

REFERENCE_DOSE_GRAMS = 18.0


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


def verdict_from_mean(score: float) -> str:
    """Map a sensory mean to a simple verdict."""
    if score >= 4.5:
        return "racheter"
    if score >= 3.5:
        return "à affiner"
    if score >= 2.5:
        return "en observation"
    return "à éviter"
