from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

from .dataset import Dataset, Shot


@dataclass
class DatasetSummary:
    coffees: int
    waters: int
    shots: int
    tastings: int
    shots_without_tasting: int
    average_brew_ratio: Optional[float]
    average_extraction_time: Optional[float]
    top_coffees_by_shots: Dict[str, int]


def summarize(dataset: Dataset, top: int = 5) -> DatasetSummary:
    tastings_by_shot = dataset.tastings_by_shot()
    ratios = _brew_ratios(dataset.shots)
    return DatasetSummary(
        coffees=len(dataset.coffees),
        waters=len(dataset.waters),
        shots=len(dataset.shots),
        tastings=len(dataset.tastings),
        shots_without_tasting=_count_shots_without_tasting(dataset.shots, tastings_by_shot),
        average_brew_ratio=_mean(ratios),
        average_extraction_time=_mean([shot.duration_s for shot in dataset.shots if shot.duration_s is not None]),
        top_coffees_by_shots=_top_counts(dataset.shots_by_coffee(), top),
    )


def _count_shots_without_tasting(shots: List[Shot], tastings_by_shot: Dict[str, List]) -> int:
    return sum(1 for shot in shots if not tastings_by_shot.get(shot.id))


def _brew_ratios(shots: List[Shot]) -> List[float]:
    ratios: List[float] = []
    for shot in shots:
        if shot.brew_ratio is not None:
            ratios.append(shot.brew_ratio)
    return ratios


def _mean(values: List[float]) -> Optional[float]:
    if not values:
        return None
    return sum(values) / len(values)


def _top_counts(items_by_key: Dict[str, List], limit: int) -> Dict[str, int]:
    counts = {key: len(items) for key, items in items_by_key.items()}
    return dict(sorted(counts.items(), key=lambda item: item[1], reverse=True)[:limit])
