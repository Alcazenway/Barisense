from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4


class BeverageType(str, Enum):
    RISTRETTO = "ristretto"
    EXPRESSO = "expresso"
    CAFE_LONG = "cafe_long"


class WaterSource(str, Enum):
    TAP = "robinet"
    BOTTLED = "bouteille"


class CoffeeFormat(str, Enum):
    GRAIN = "grain"
    MOULU = "moulu"


class VerdictStatus(str, Enum):
    RACHETER = "racheter"
    A_AFFINER = "a_affiner"
    EN_OBSERVATION = "en_observation"
    A_EVITER = "a_eviter"


@dataclass
class Coffee:
    name: str
    roaster: str
    reference: Optional[str]
    format: CoffeeFormat
    weight_grams: int
    price_eur: float
    purchased_at: date
    cost_per_shot_eur: float = 0.0
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Water:
    label: str
    source: WaterSource
    brand: Optional[str]
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Shot:
    coffee_id: UUID
    beverage_type: BeverageType
    grind_setting: str
    dose_in_grams: float
    beverage_weight_grams: float
    extraction_time_seconds: float
    water_id: Optional[UUID] = None
    notes: Optional[str] = None
    brew_ratio: float = 0.0
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Tasting:
    shot_id: UUID
    acidity_score: int
    bitterness_score: int
    body_score: int
    aroma_score: int
    balance_score: int
    finish_score: int
    overall_score: int
    sensory_mean: float
    comments: Optional[str] = None
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Verdict:
    coffee_id: UUID
    status: VerdictStatus
    rationale: Optional[str] = None
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.utcnow)
