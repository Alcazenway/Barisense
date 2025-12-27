from collections import defaultdict
from statistics import mean, pstdev
from typing import Iterable

from app.models.entities import VerdictStatus
from app.models.schemas import ShotCreate

REFERENCE_DOSE_GRAMS = 18.0
TARGET_BREW_RATIOS: dict[BeverageType, float] = {
    BeverageType.RISTRETTO: 1.6,
    BeverageType.EXPRESSO: 2.0,
    BeverageType.CAFE_LONG: 2.8,
}
DEFAULT_SENSORY_WEIGHTS: dict[str, float] = {
    "acidity": 0.15,
    "bitterness": 0.1,
    "body": 0.15,
    "aroma": 0.2,
    "balance": 0.2,
    "finish": 0.1,
    "overall": 0.1,
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


def compute_weighted_sensory_mean(
    tasting: TastingCreate, weights: dict[str, float] | None = None
) -> float:
    """Compute a weighted sensory mean to emphasise balance/aroma while keeping other axes."""
    weights = weights or DEFAULT_SENSORY_WEIGHTS
    weight_sum = sum(weights.values())
    weighted_total = (
        tasting.acidity * weights["acidity"]
        + tasting.bitterness * weights["bitterness"]
        + tasting.body * weights["body"]
        + tasting.aroma * weights["aroma"]
        + tasting.balance * weights["balance"]
        + tasting.finish * weights["finish"]
        + tasting.overall * weights["overall"]
    )
    return round(weighted_total / weight_sum, 2)


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


def compute_extraction_score(shot: Shot) -> float:
    """Score extraction consistency against target brew ratios and shot duration."""
    target = TARGET_BREW_RATIOS.get(shot.beverage_type, 2.0)
    ratio_penalty = abs(shot.brew_ratio - target) * 1.4
    time_penalty = 0.0
    if shot.extraction_time_seconds < 22:
        time_penalty = (22 - shot.extraction_time_seconds) * 0.04
    elif shot.extraction_time_seconds > 36:
        time_penalty = (shot.extraction_time_seconds - 36) * 0.04
    score = 5 - min(4, ratio_penalty + time_penalty)
    return round(max(1.0, min(score, 5.0)), 2)


def diagnose_extraction(shot: Shot, water: Water | None) -> tuple[str, list[str]]:
    """Generate a concise extraction diagnosis and remediation advice."""
    target = TARGET_BREW_RATIOS.get(shot.beverage_type, 2.0)
    ratio_delta = shot.brew_ratio - target
    advice: list[str] = []
    diagnosis = "dans la cible"

    if ratio_delta < -0.2:
        diagnosis = "sous-extrait"
        advice.append("Resserrer la mouture ou prolonger l'extraction.")
    elif ratio_delta > 0.3:
        diagnosis = "sur-extrait"
        advice.append("Ouvrir légèrement la mouture ou réduire le yield.")

    if shot.extraction_time_seconds < 22:
        advice.append("Augmenter la finesse pour rallonger le débit.")
    elif shot.extraction_time_seconds > 36:
        advice.append("Baisser la dose ou ouvrir la mouture pour accélérer.")

    if water:
        classification, impact_extraction, impact_sensory = classify_water_profile(water)
        advice.append(f"Eau {classification}: {impact_extraction}.")
        if impact_sensory not in impact_extraction:
            advice.append(impact_sensory)
    return diagnosis, advice


def classify_water_profile(water: Water) -> tuple[str, str, str]:
    """Classify water into intuitive buckets and state expected impacts."""
    mineralization = water.mineralization_ppm or 0
    hardness = water.hardness_ca_mg_l or 0
    alkalinity = water.alkalinity_hco3_mg_l or 0
    classification = "équilibrée"
    extraction_bias = "Extraction stable"
    sensory_bias = "Profil aromatique neutre"

    if mineralization < 70 or hardness < 25:
        classification = "faible minéralisation"
        extraction_bias = "Risque de sous-extraction, peu de résistance au débit"
        sensory_bias = "Acidité plus tranchante, corps plus léger"
    elif mineralization > 180 or hardness > 90 or alkalinity > 120:
        classification = "fortement minéralisée"
        extraction_bias = "Peut pousser la sur-extraction et la lenteur de débit"
        sensory_bias = "Amertume accrue, texture plus lourde"
    elif alkalinity < 40:
        classification = "tampon faible"
        extraction_bias = "Ph instable, variations sensibles"
        sensory_bias = "Acidité perçue plus haute"

    return classification, extraction_bias, sensory_bias


def compute_water_impact(
    water: Water, shots: Iterable[Shot], tastings: Iterable[Tasting], rank: int
) -> WaterImpact:
    """Aggregate extraction and sensoriel impacts for a given water."""
    shots_with_water = [shot for shot in shots if shot.water_id == water.id]
    tastings_with_water = [t for t in tastings if t.shot_id in {s.id for s in shots_with_water}]
    avg_ratio = round(mean([s.brew_ratio for s in shots_with_water]), 2) if shots_with_water else None
    avg_sensory = (
        round(mean([t.sensory_mean for t in tastings_with_water]), 2) if tastings_with_water else None
    )
    classification, impact_extraction, impact_sensory = classify_water_profile(water)
    return WaterImpact(
        water_id=water.id,
        label=water.label,
        source=water.source,
        classification=classification,
        impact_on_extraction=impact_extraction,
        impact_on_sensory=impact_sensory,
        average_brew_ratio=avg_ratio,
        average_sensory_mean=avg_sensory,
        rank=rank,
    )


def compute_global_score(sensory_mean: float | None, extraction_scores: list[float]) -> float:
    """Blend sensory and extraction consistency into a global score."""
    sensory_component = sensory_mean or 0
    extraction_component = mean(extraction_scores) if extraction_scores else 0
    score = 0.65 * sensory_component + 0.35 * extraction_component
    return round(score, 2)


class AnalyticsEngine:
    """Centralise the analytics logic to keep routers slim."""

    def __init__(self, repository, sensory_weights: dict[str, float] | None = None) -> None:
        self.repository = repository
        self.sensory_weights = sensory_weights or DEFAULT_SENSORY_WEIGHTS

    def build_summary(self) -> AnalyticsSummary:
        coffees = list(self.repository.list_coffees())
        waters = list(self.repository.list_waters())
        shots = list(self.repository.list_shots())
        tastings = list(self.repository.list_tastings())

        coffee_blocks = [
            self._build_coffee_analytics(coffee, waters, shots, tastings) for coffee in coffees
        ]
        water_rankings = self._rank_waters(waters, shots, tastings)
        return AnalyticsSummary(coffees=coffee_blocks, water_rankings=water_rankings)

    def _build_coffee_analytics(
        self, coffee: Coffee, waters: list[Water], shots: list[Shot], tastings: list[Tasting]
    ) -> CoffeeAnalytics:
        coffee_shots = [shot for shot in shots if shot.coffee_id == coffee.id]
        tasting_index: dict[UUID, list[Tasting]] = defaultdict(list)
        for tasting in tastings:
            tasting_index[tasting.shot_id].append(tasting)

        extraction_history: list[ExtractionSnapshot] = []
        extraction_scores: list[float] = []
        for shot in sorted(coffee_shots, key=lambda s: s.created_at):
            water = next((w for w in waters if w.id == shot.water_id), None)
            diagnosis, recos = diagnose_extraction(shot, water)
            extraction_history.append(
                ExtractionSnapshot(
                    shot_id=shot.id,
                    beverage_type=shot.beverage_type,
                    grind_setting=shot.grind_setting,
                    brew_ratio=shot.brew_ratio,
                    extraction_time_seconds=shot.extraction_time_seconds,
                    water_id=shot.water_id,
                    water_label=water.label if water else None,
                    diagnosis=diagnosis,
                    recommendations=recos,
                    created_at=shot.created_at,
                )
            )
            extraction_scores.append(compute_extraction_score(shot))

        sensory_scores = [t.sensory_mean for t in tastings if t.shot_id in {s.id for s in coffee_shots}]
        weighted_scores = [
            t.weighted_sensory_mean or t.sensory_mean
            for t in tastings
            if t.shot_id in {s.id for s in coffee_shots}
        ]
        sensory_summary = SensorySummary(
            mean=round(mean(sensory_scores), 2) if sensory_scores else None,
            weighted_mean=round(mean(weighted_scores), 2) if weighted_scores else None,
            sample_size=len(sensory_scores),
        )
        global_score_value = compute_global_score(sensory_summary.weighted_mean, extraction_scores)
        global_score = GlobalScore(
            score=global_score_value,
            verdict=verdict_from_score(global_score_value),
            details="Mélange pondéré extraction/sensoriel",
        )

        parameter_suggestions = self._build_parameter_suggestions(coffee_shots, tasting_index)
        water_impacts = self._summarise_water_impacts(coffee_shots, waters, tasting_index)

        return CoffeeAnalytics(
            coffee=coffee,
            extraction_history=extraction_history,
            parameter_suggestions=parameter_suggestions,
            sensory_summary=sensory_summary,
            global_score=global_score,
            water_impacts=water_impacts,
        )

    def _build_parameter_suggestions(
        self, shots: list[Shot], tasting_index: dict
    ) -> list[ParameterSuggestion]:
        suggestions: list[ParameterSuggestion] = []
        for beverage_type in {shot.beverage_type for shot in shots}:
            relevant_shots = [shot for shot in shots if shot.beverage_type == beverage_type]
            if not relevant_shots:
                continue
            shot_scores = []
            for shot in relevant_shots:
                tastings = tasting_index.get(shot.id, [])
                best_tasting_score = max((t.weighted_sensory_mean or t.sensory_mean for t in tastings), default=0)
                shot_scores.append((best_tasting_score, shot))
            _, best_shot = max(shot_scores, key=lambda pair: pair[0])
            target_ratio = TARGET_BREW_RATIOS.get(beverage_type, 2.0)
            rationale = "Basé sur le meilleur score sensoriel disponible"
            if not tasting_index.get(best_shot.id):
                rationale = "Basé sur la stabilité d'extraction faute de dégustation"
            suggestions.append(
                ParameterSuggestion(
                    beverage_type=beverage_type,
                    recommended_ratio=round(best_shot.brew_ratio, 2) if best_shot else target_ratio,
                    recommended_extraction_time=best_shot.extraction_time_seconds if best_shot else 28.0,
                    suggested_grind=best_shot.grind_setting if best_shot else None,
                    rationale=rationale,
                )
            )
        return suggestions

    def _summarise_water_impacts(
        self, shots: list[Shot], waters: list[Water], tasting_index: dict
    ) -> list[WaterImpact]:
        impacts: list[WaterImpact] = []
        for water in waters:
            shots_with_water = [shot for shot in shots if shot.water_id == water.id]
            tastings_with_water = [t for shot in shots_with_water for t in tasting_index.get(shot.id, [])]
            if not shots_with_water and not tastings_with_water:
                continue
            impacts.append(compute_water_impact(water, shots_with_water, tastings_with_water, rank=0))
        # local ranking by weighted sensory
        impacts_sorted = sorted(
            impacts,
            key=lambda impact: (impact.average_sensory_mean or 0, impact.average_brew_ratio or 0),
            reverse=True,
        )
        for idx, impact in enumerate(impacts_sorted, start=1):
            impact.rank = idx
        return impacts_sorted

    def _rank_waters(
        self, waters: list[Water], shots: list[Shot], tastings: list[Tasting]
    ) -> list[WaterImpact]:
        ranking: list[WaterImpact] = []
        tastings_by_water: dict[UUID, list[Tasting]] = defaultdict(list)
        for tasting in tastings:
            ranking_shot = next((s for s in shots if s.id == tasting.shot_id), None)
            if ranking_shot and ranking_shot.water_id:
                tastings_by_water[ranking_shot.water_id].append(tasting)
        for water in waters:
            ranking.append(
                compute_water_impact(water, [s for s in shots if s.water_id == water.id], tastings_by_water[water.id], 0)
            )
        ranking_sorted = sorted(
            ranking,
            key=lambda impact: (impact.average_sensory_mean or 0, impact.average_brew_ratio or 0),
            reverse=True,
        )
        for idx, impact in enumerate(ranking_sorted, start=1):
            impact.rank = idx
        return ranking_sorted
