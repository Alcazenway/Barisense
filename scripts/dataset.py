from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional


@dataclass
class Coffee:
    id: str
    name: str
    roaster: str
    reference: Optional[str] = None
    type: Optional[str] = None
    bag_weight_g: Optional[int] = None
    price_eur: Optional[float] = None
    purchase_date: Optional[str] = None


@dataclass
class Water:
    id: str
    label: str
    source: Optional[str] = None


@dataclass
class Shot:
    id: str
    coffee_id: str
    beverage_type: Optional[str] = None
    dose_g: Optional[float] = None
    yield_g: Optional[float] = None
    duration_s: Optional[float] = None
    grind: Optional[str] = None
    water_id: Optional[str] = None

    @property
    def brew_ratio(self) -> Optional[float]:
        if self.dose_g and self.yield_g:
            return self.yield_g / self.dose_g
        return None


@dataclass
class Tasting:
    id: str
    shot_id: str
    acidity: Optional[str] = None
    bitterness: Optional[str] = None
    body: Optional[str] = None
    aroma: Optional[str] = None
    balance: Optional[str] = None
    finish: Optional[str] = None
    overall: Optional[str] = None
    notes: Optional[str] = None


@dataclass
class Dataset:
    coffees: List[Coffee] = field(default_factory=list)
    waters: List[Water] = field(default_factory=list)
    shots: List[Shot] = field(default_factory=list)
    tastings: List[Tasting] = field(default_factory=list)

    @classmethod
    def from_dict(cls, payload: Dict) -> "Dataset":
        return cls(
            coffees=[Coffee(**item) for item in payload.get("coffees", [])],
            waters=[Water(**item) for item in payload.get("waters", [])],
            shots=[Shot(**item) for item in payload.get("shots", [])],
            tastings=[Tasting(**item) for item in payload.get("tastings", [])],
        )

    @classmethod
    def load(cls, path: Path) -> "Dataset":
        with path.open("r", encoding="utf-8") as handle:
            return cls.from_dict(json.load(handle))

    def dump(self) -> Dict:
        return {
            "coffees": _to_dict_list(self.coffees),
            "waters": _to_dict_list(self.waters),
            "shots": _to_dict_list(self.shots),
            "tastings": _to_dict_list(self.tastings),
        }

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as handle:
            json.dump(self.dump(), handle, ensure_ascii=False, indent=2)

    def coffee_index(self) -> Dict[str, Coffee]:
        return {coffee.id: coffee for coffee in self.coffees}

    def shot_index(self) -> Dict[str, Shot]:
        return {shot.id: shot for shot in self.shots}

    def tasting_index(self) -> Dict[str, Tasting]:
        return {tasting.id: tasting for tasting in self.tastings}

    def shots_by_coffee(self) -> Dict[str, List[Shot]]:
        grouped: Dict[str, List[Shot]] = {}
        for shot in self.shots:
            grouped.setdefault(shot.coffee_id, []).append(shot)
        return grouped

    def tastings_by_shot(self) -> Dict[str, List[Tasting]]:
        grouped: Dict[str, List[Tasting]] = {}
        for tasting in self.tastings:
            grouped.setdefault(tasting.shot_id, []).append(tasting)
        return grouped


def _to_dict_list(items: Iterable) -> List[Dict]:
    return [asdict(item) for item in items]
