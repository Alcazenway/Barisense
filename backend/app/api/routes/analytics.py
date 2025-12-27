from __future__ import annotations

from statistics import mean

from fastapi import APIRouter, Depends

from app.core.dependencies import get_repository, require_api_key
from app.models.entities import BeverageType
from app.models.schemas import (
    QualityPriceInsight,
    RankedCoffee,
    RetestCandidate,
    StabilityInsight,
)
from app.services.analysis import (
    aggregate_quality_per_price,
    mean_to_label,
    stability_label,
    summarize_rankings,
    summarize_retest_needed,
    verdict_label,
    verdict_from_mean,
)
from app.services.repository import Repository

router = APIRouter(prefix="/analytics", tags=["analytics"], dependencies=[Depends(require_api_key)])


def _average_for_coffee(repository: Repository, coffee_id, beverage_filter: BeverageType | None = None):
    tastings = repository.tastings_by_coffee(coffee_id)
    if beverage_filter:
        shot_ids = {
            shot.id for shot in repository.shots_by_coffee(coffee_id) if shot.beverage_type == beverage_filter
        }
        tastings = [t for t in tastings if t.shot_id in shot_ids]
    if not tastings:
        return None
    return mean([t.sensory_mean for t in tastings])


def _verdict_label(repository: Repository, coffee_id) -> str:
    verdict = next((v for v in repository.list_verdicts() if v.coffee_id == coffee_id), None)
    if verdict:
        return verdict_label(verdict.status)
    avg = _average_for_coffee(repository, coffee_id)
    if avg is None:
        return "en observation"
    return verdict_label(verdict_from_mean(avg))


@router.get("/rankings/global", response_model=list[RankedCoffee], summary="Classement global des cafés")
def global_ranking(repository: Repository = Depends(get_repository)) -> list[RankedCoffee]:
    means = {}
    for coffee in repository.list_coffees():
        avg = _average_for_coffee(repository, coffee.id)
        if avg is not None:
            means[coffee.id] = {"coffee": coffee, "mean": avg}
    ranking = summarize_rankings(means)
    return [
        RankedCoffee(
            position=position,
            coffee_id=coffee_id,
            name=data["coffee"].name,
            roaster=data["coffee"].roaster,
            score_label=mean_to_label(data["mean"]),
            verdict_label=_verdict_label(repository, coffee_id),
        )
        for position, coffee_id, data in ranking
    ]


@router.get(
    "/rankings/ristretto",
    response_model=list[RankedCoffee],
    summary="Classement ristretto (boissons serrées uniquement)",
)
def ristretto_ranking(repository: Repository = Depends(get_repository)) -> list[RankedCoffee]:
    means = {}
    for coffee in repository.list_coffees():
        avg = _average_for_coffee(repository, coffee.id, beverage_filter=BeverageType.RISTRETTO)
        if avg is not None:
            means[coffee.id] = {"coffee": coffee, "mean": avg}
    ranking = summarize_rankings(means)
    return [
        RankedCoffee(
            position=position,
            coffee_id=coffee_id,
            name=data["coffee"].name,
            roaster=data["coffee"].roaster,
            score_label=mean_to_label(data["mean"]),
            verdict_label=_verdict_label(repository, coffee_id),
            beverage_filter=BeverageType.RISTRETTO.value,
        )
        for position, coffee_id, data in ranking
    ]


@router.get(
    "/rankings/expresso",
    response_model=list[RankedCoffee],
    summary="Classement expresso",
)
def expresso_ranking(repository: Repository = Depends(get_repository)) -> list[RankedCoffee]:
    means = {}
    for coffee in repository.list_coffees():
        avg = _average_for_coffee(repository, coffee.id, beverage_filter=BeverageType.EXPRESSO)
        if avg is not None:
            means[coffee.id] = {"coffee": coffee, "mean": avg}
    ranking = summarize_rankings(means)
    return [
        RankedCoffee(
            position=position,
            coffee_id=coffee_id,
            name=data["coffee"].name,
            roaster=data["coffee"].roaster,
            score_label=mean_to_label(data["mean"]),
            verdict_label=_verdict_label(repository, coffee_id),
            beverage_filter=BeverageType.EXPRESSO.value,
        )
        for position, coffee_id, data in ranking
    ]


@router.get(
    "/quality-price",
    response_model=list[QualityPriceInsight],
    summary="Rapport qualité / prix par café",
)
def quality_price(repository: Repository = Depends(get_repository)) -> list[QualityPriceInsight]:
    insights: list[QualityPriceInsight] = []
    ratio_priority = {
        "excellent rapport Q/P": 4,
        "bon rapport Q/P": 3,
        "moyen": 2,
        "défavorable": 1,
        "non renseigné": 0,
    }
    for coffee in repository.list_coffees():
        avg = _average_for_coffee(repository, coffee.id)
        if avg is None:
            continue
        ratio_label = aggregate_quality_per_price(avg, coffee.cost_per_shot_eur)
        insights.append(
            QualityPriceInsight(
                coffee_id=coffee.id,
                name=coffee.name,
                roaster=coffee.roaster,
                cost_per_shot_eur=coffee.cost_per_shot_eur,
                quality_label=mean_to_label(avg),
                verdict_label=_verdict_label(repository, coffee.id),
                ratio_label=ratio_label,
            )
        )
    return sorted(insights, key=lambda i: ratio_priority.get(i.ratio_label, 0), reverse=True)


@router.get(
    "/stability",
    response_model=list[StabilityInsight],
    summary="Cafés les plus stables (écart-type des dégustations)",
)
def stability(repository: Repository = Depends(get_repository)) -> list[StabilityInsight]:
    insights: list[StabilityInsight] = []
    for coffee in repository.list_coffees():
        means = [t.sensory_mean for t in repository.tastings_by_coffee(coffee.id)]
        if not means:
            continue
        insights.append(
            StabilityInsight(
                coffee_id=coffee.id,
                name=coffee.name,
                roaster=coffee.roaster,
                stability=stability_label(means),
                sample_size=len(means),
            )
        )
    return insights


@router.get(
    "/retest",
    response_model=list[RetestCandidate],
    summary="Cafés à retester (pas assez de dégustations)",
)
def to_retest(repository: Repository = Depends(get_repository)) -> list[RetestCandidate]:
    counts = repository.tasting_counts()
    candidates_ids = summarize_retest_needed(counts)
    coffees = [c for c in repository.list_coffees() if c.id in candidates_ids]
    return [
        RetestCandidate(
            coffee_id=coffee.id,
            name=coffee.name,
            roaster=coffee.roaster,
            reason="Une seule dégustation ou aucune",
        )
        for coffee in coffees
    ]
