from __future__ import annotations

from datetime import date, datetime
from typing import Annotated, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, PositiveFloat, PositiveInt

from app.models.entities import (
    BeverageType,
    CoffeeFormat,
    VerdictStatus,
    WaterSource,
)

SensoryLabel = Literal["insipide", "doux", "équilibré", "expressif", "intense"]
SensoryLabelField = Annotated[SensoryLabel, Field(description="Libellé sensoriel 1-5 (jamais de chiffres)")]


class CoffeeBase(BaseModel):
    name: str = Field(..., description="Nom commercial du café")
    roaster: str = Field(..., description="Torréfacteur ou marque")
    reference: str | None = Field(None, description="Référence commerciale")
    format: CoffeeFormat = Field(..., description="Grain ou moulu")
    weight_grams: PositiveInt = Field(..., description="Poids du paquet en grammes")
    price_eur: PositiveFloat = Field(..., description="Prix payé en euros")
    purchased_at: date = Field(..., description="Date d'achat du lot")


class CoffeeCreate(CoffeeBase):
    """Payload pour créer ou mettre à jour un café."""


class CoffeeRead(CoffeeBase):
    id: UUID
    cost_per_shot_eur: float = Field(..., description="Coût estimé par shot")
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


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
    """Payload pour créer ou mettre à jour une eau."""


class WaterRead(WaterBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


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
    """Payload pour créer ou mettre à jour un shot."""


class ShotRead(ShotBase):
    id: UUID
    brew_ratio: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TastingBase(BaseModel):
    shot_id: UUID = Field(..., description="Référence du shot dégusté")
    acidity_label: SensoryLabelField
    bitterness_label: SensoryLabelField
    body_label: SensoryLabelField
    aroma_label: SensoryLabelField
    balance_label: SensoryLabelField
    finish_label: SensoryLabelField
    overall_label: SensoryLabelField
    comments: str | None = Field(None, description="Notes libres ou rappel du ressenti humain")


class TastingCreate(TastingBase):
    """Payload pour enregistrer une dégustation (libellés uniquement)."""


class TastingRead(BaseModel):
    id: UUID
    shot_id: UUID
    acidity_label: SensoryLabelField
    bitterness_label: SensoryLabelField
    body_label: SensoryLabelField
    aroma_label: SensoryLabelField
    balance_label: SensoryLabelField
    finish_label: SensoryLabelField
    overall_label: SensoryLabelField
    mean_label: SensoryLabelField
    verdict_label: Literal["racheter", "à affiner", "en observation", "à éviter"]
    comments: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class VerdictBase(BaseModel):
    coffee_id: UUID
    status: VerdictStatus
    rationale: str | None = None


class VerdictCreate(VerdictBase):
    """Payload CRUD verdict."""


class VerdictRead(VerdictBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RankedCoffee(BaseModel):
    position: int
    coffee_id: UUID
    name: str
    roaster: str
    score_label: SensoryLabel
    verdict_label: str
    water_filter: str | None = None
    beverage_filter: str | None = None


class QualityPriceInsight(BaseModel):
    coffee_id: UUID
    name: str
    roaster: str
    cost_per_shot_eur: float
    quality_label: SensoryLabel
    verdict_label: str
    ratio_label: str


class StabilityInsight(BaseModel):
    coffee_id: UUID
    name: str
    roaster: str
    stability: str
    sample_size: int


class RetestCandidate(BaseModel):
    coffee_id: UUID
    name: str
    roaster: str
    reason: str
