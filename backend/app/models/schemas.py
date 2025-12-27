from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from typing import Annotated, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, PositiveFloat, PositiveInt

SensoryScore = Annotated[int, Field(ge=1, le=5, description="Échelle sensorielle 1-5")]


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


class CoffeeBase(BaseModel):
    name: str = Field(..., description="Nom commercial du café")
    roaster: str = Field(..., description="Torréfacteur ou marque")
    reference: str | None = Field(None, description="Référence commerciale")
    format: CoffeeFormat = Field(..., description="Grain ou moulu")
    weight_grams: PositiveInt = Field(..., description="Poids du paquet en grammes")
    price_eur: PositiveFloat = Field(..., description="Prix payé en euros")
    purchased_at: date = Field(..., description="Date d'achat du lot")


class CoffeeCreate(CoffeeBase):
    pass


class Coffee(CoffeeBase):
    id: UUID = Field(default_factory=uuid4, description="Identifiant du lot")
    cost_per_shot_eur: float = Field(..., description="Coût estimé par shot")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class WaterBase(BaseModel):
    label: str = Field(..., description="Nom court pour différencier les eaux")
    source: WaterSource = Field(..., description="Robinet ou bouteille")
    brand: str | None = Field(None, description="Marque si bouteille")
    mineralization_ppm: PositiveFloat | None = Field(
        None, description="TDS ou minéralisation totale estimée en ppm"
    )
    hardness_ca_mg_l: PositiveFloat | None = Field(None, description="Dureté (CaCO3 mg/L)")
    alkalinity_hco3_mg_l: PositiveFloat | None = Field(None, description="Alcalinité (HCO3 mg/L)")
    ph: PositiveFloat | None = Field(None, description="pH mesuré")
    filter_type: str | None = Field(
        None,
        description="Type de traitement ou de filtre (ex: Brita, osmose, bouteille)",
    )


class WaterCreate(WaterBase):
    pass


class Water(WaterBase):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ShotBase(BaseModel):
    coffee_id: UUID = Field(..., description="Lot de café utilisé")
    beverage_type: BeverageType = Field(..., description="Ristretto, expresso ou café long")
    grind_setting: str = Field(..., description="Réglage de mouture")
    dose_in_grams: PositiveFloat = Field(..., description="Dose de café sec en grammes")
    beverage_weight_grams: PositiveFloat = Field(..., description="Poids en tasse en grammes")
    extraction_time_seconds: PositiveFloat = Field(..., description="Durée d'extraction en secondes")
    water_id: UUID | None = Field(None, description="Eau associée")
    notes: str | None = Field(None, description="Notes libres sur l'extraction")


class ShotCreate(ShotBase):
    pass


class Shot(ShotBase):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    brew_ratio: float = Field(..., description="Ratio infusion (poids en tasse / dose)")


class TastingBase(BaseModel):
    shot_id: UUID = Field(..., description="Référence du shot dégusté")
    acidity: SensoryScore
    bitterness: SensoryScore
    body: SensoryScore
    aroma: SensoryScore
    balance: SensoryScore
    finish: SensoryScore
    overall: SensoryScore
    comments: str | None = Field(None, description="Notes libres ou rappel du ressenti humain")


class TastingCreate(TastingBase):
    pass


class Tasting(TastingBase):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    sensory_mean: float = Field(..., description="Moyenne des scores sensoriels")
    weighted_sensory_mean: float | None = Field(
        None, description="Moyenne sensorielle pondérée par critère"
    )


class ExtractionSnapshot(BaseModel):
    shot_id: UUID
    beverage_type: BeverageType
    grind_setting: str
    brew_ratio: float
    extraction_time_seconds: float
    water_id: UUID | None
    water_label: str | None
    diagnosis: str
    recommendations: list[str]
    created_at: datetime


class ParameterSuggestion(BaseModel):
    beverage_type: BeverageType
    recommended_ratio: float
    recommended_extraction_time: float
    suggested_grind: str | None
    rationale: str


class SensorySummary(BaseModel):
    mean: float | None
    weighted_mean: float | None
    sample_size: int


class GlobalScore(BaseModel):
    score: float
    verdict: Literal["racheter", "à affiner", "à éviter", "en observation"]
    details: str


class WaterImpact(BaseModel):
    water_id: UUID
    label: str
    source: WaterSource
    classification: str
    impact_on_extraction: str
    impact_on_sensory: str
    average_brew_ratio: float | None
    average_sensory_mean: float | None
    rank: int


class CoffeeAnalytics(BaseModel):
    coffee: Coffee
    extraction_history: list[ExtractionSnapshot]
    parameter_suggestions: list[ParameterSuggestion]
    sensory_summary: SensorySummary
    global_score: GlobalScore
    water_impacts: list[WaterImpact]


class AnalyticsSummary(BaseModel):
    coffees: list[CoffeeAnalytics]
    water_rankings: list[WaterImpact]
