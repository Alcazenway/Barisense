from __future__ import annotations

from collections.abc import Iterable
from uuid import UUID

from app.models.schemas import (
    Coffee,
    CoffeeCreate,
    Shot,
    ShotCreate,
    Tasting,
    TastingCreate,
    Water,
    WaterCreate,
)
from app.services.analysis import (
    compute_brew_ratio,
    compute_cost_per_shot,
    compute_sensory_mean,
    compute_weighted_sensory_mean,
)


class InMemoryRepository:
    """Simple in-memory repository useful for prototyping the backend flows."""

    def __init__(self) -> None:
        self._coffees: dict[UUID, Coffee] = {}
        self._waters: dict[UUID, Water] = {}
        self._shots: dict[UUID, Shot] = {}
        self._tastings: dict[UUID, Tasting] = {}

    # Coffee
    def list_coffees(self) -> Iterable[Coffee]:
        return self._coffees.values()

    def add_coffee(self, payload: CoffeeCreate) -> Coffee:
        coffee = Coffee(
            **payload.model_dump(),
            cost_per_shot_eur=compute_cost_per_shot(payload.price_eur, payload.weight_grams),
        )
        self._coffees[coffee.id] = coffee
        return coffee

    def get_coffee(self, coffee_id: UUID) -> Coffee | None:
        return self._coffees.get(coffee_id)

    # Water
    def list_waters(self) -> Iterable[Water]:
        return self._waters.values()

    def add_water(self, payload: WaterCreate) -> Water:
        water = Water(**payload.model_dump())
        self._waters[water.id] = water
        return water

    def get_water(self, water_id: UUID) -> Water | None:
        return self._waters.get(water_id)

    # Shots
    def list_shots(self) -> Iterable[Shot]:
        return self._shots.values()

    def list_shots_for_coffee(self, coffee_id: UUID) -> list[Shot]:
        return [shot for shot in self._shots.values() if shot.coffee_id == coffee_id]

    def add_shot(self, payload: ShotCreate) -> Shot:
        if payload.coffee_id not in self._coffees:
            raise ValueError("coffee_not_found")
        if payload.water_id and payload.water_id not in self._waters:
            raise ValueError("water_not_found")
        shot = Shot(**payload.model_dump(), brew_ratio=compute_brew_ratio(payload))
        self._shots[shot.id] = shot
        return shot

    def get_shot(self, shot_id: UUID) -> Shot | None:
        return self._shots.get(shot_id)

    # Tastings
    def list_tastings(self) -> Iterable[Tasting]:
        return self._tastings.values()

    def list_tastings_for_shot(self, shot_id: UUID) -> list[Tasting]:
        return [tasting for tasting in self._tastings.values() if tasting.shot_id == shot_id]

    def add_tasting(self, payload: TastingCreate) -> Tasting:
        if payload.shot_id not in self._shots:
            raise ValueError("shot_not_found")
        tasting = Tasting(
            **payload.model_dump(),
            sensory_mean=compute_sensory_mean(payload),
            weighted_sensory_mean=compute_weighted_sensory_mean(payload),
        )
        self._tastings[tasting.id] = tasting
        return tasting
