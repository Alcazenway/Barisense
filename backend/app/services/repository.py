from __future__ import annotations

from collections import defaultdict
from uuid import UUID

from app.models.entities import Coffee, Shot, Tasting, Verdict, Water
from app.models.schemas import (
    CoffeeCreate,
    ShotCreate,
    TastingCreate,
    VerdictCreate,
    WaterCreate,
)
from app.services.analysis import (
    compute_brew_ratio,
    compute_cost_per_shot,
    compute_sensory_mean,
    label_to_score,
    mean_to_label,
    verdict_from_mean,
)


class Repository:
    """In-memory repository with business helpers."""

    def __init__(self) -> None:
        self._coffees: dict[UUID, Coffee] = {}
        self._waters: dict[UUID, Water] = {}
        self._shots: dict[UUID, Shot] = {}
        self._tastings: dict[UUID, Tasting] = {}
        self._verdicts: dict[UUID, Verdict] = {}

    # Coffee
    def list_coffees(self) -> list[Coffee]:
        return sorted(self._coffees.values(), key=lambda c: c.created_at, reverse=True)

    def get_coffee(self, coffee_id: UUID) -> Coffee | None:
        return self._coffees.get(coffee_id)

    def upsert_coffee(self, payload: CoffeeCreate, coffee_id: UUID | None = None) -> Coffee:
        instance = self._coffees.get(coffee_id) if coffee_id else None
        if instance is None:
            instance = Coffee(**payload.model_dump())
        else:
            for field, value in payload.model_dump().items():
                setattr(instance, field, value)
        instance.cost_per_shot_eur = compute_cost_per_shot(payload.price_eur, payload.weight_grams)
        self._coffees[instance.id] = instance
        return instance

    def delete_coffee(self, coffee_id: UUID) -> None:
        if coffee_id in self._coffees:
            # cascade shots/tastings/verdict
            for shot_id, shot in list(self._shots.items()):
                if shot.coffee_id == coffee_id:
                    self.delete_shot(shot_id)
            for verdict_id, verdict in list(self._verdicts.items()):
                if verdict.coffee_id == coffee_id:
                    self._verdicts.pop(verdict_id, None)
            self._coffees.pop(coffee_id, None)

    # Water
    def list_waters(self) -> list[Water]:
        return sorted(self._waters.values(), key=lambda w: w.created_at, reverse=True)

    def get_water(self, water_id: UUID) -> Water | None:
        return self._waters.get(water_id)

    def upsert_water(self, payload: WaterCreate, water_id: UUID | None = None) -> Water:
        instance = self._waters.get(water_id) if water_id else None
        if instance is None:
            instance = Water(**payload.model_dump())
        else:
            for field, value in payload.model_dump().items():
                setattr(instance, field, value)
        self._waters[instance.id] = instance
        return instance

    def delete_water(self, water_id: UUID) -> None:
        self._waters.pop(water_id, None)

    # Shots
    def list_shots(self) -> list[Shot]:
        return sorted(self._shots.values(), key=lambda s: s.created_at, reverse=True)

    def get_shot(self, shot_id: UUID) -> Shot | None:
        return self._shots.get(shot_id)

    def add_shot(self, payload: ShotCreate) -> Shot:
        if self.get_coffee(payload.coffee_id) is None:
            raise ValueError("coffee_not_found")
        if payload.water_id and self.get_water(payload.water_id) is None:
            raise ValueError("water_not_found")
        shot = Shot(**payload.model_dump())
        shot.brew_ratio = compute_brew_ratio(payload)
        self._shots[shot.id] = shot
        return shot

    def update_shot(self, shot_id: UUID, payload: ShotCreate) -> Shot:
        shot = self.get_shot(shot_id)
        if shot is None:
            raise ValueError("shot_not_found")
        if self.get_coffee(payload.coffee_id) is None:
            raise ValueError("coffee_not_found")
        if payload.water_id and self.get_water(payload.water_id) is None:
            raise ValueError("water_not_found")
        for field, value in payload.model_dump().items():
            setattr(shot, field, value)
        shot.brew_ratio = compute_brew_ratio(payload)
        self._shots[shot.id] = shot
        return shot

    def delete_shot(self, shot_id: UUID) -> None:
        if shot_id in self._shots:
            for tasting_id, tasting in list(self._tastings.items()):
                if tasting.shot_id == shot_id:
                    self._tastings.pop(tasting_id, None)
            self._shots.pop(shot_id, None)

    # Tastings
    def list_tastings(self) -> list[Tasting]:
        return sorted(self._tastings.values(), key=lambda t: t.created_at, reverse=True)

    def get_tasting(self, tasting_id: UUID) -> Tasting | None:
        return self._tastings.get(tasting_id)

    def add_tasting(self, payload: TastingCreate) -> Tasting:
        shot = self.get_shot(payload.shot_id)
        if shot is None:
            raise ValueError("shot_not_found")
        scores = {
            "acidity_score": label_to_score(payload.acidity_label),
            "bitterness_score": label_to_score(payload.bitterness_label),
            "body_score": label_to_score(payload.body_label),
            "aroma_score": label_to_score(payload.aroma_label),
            "balance_score": label_to_score(payload.balance_label),
            "finish_score": label_to_score(payload.finish_label),
            "overall_score": label_to_score(payload.overall_label),
        }
        sensory_mean = compute_sensory_mean(scores.values())
        tasting = Tasting(
            shot_id=payload.shot_id,
            comments=payload.comments,
            sensory_mean=sensory_mean,
            **scores,
        )
        self._tastings[tasting.id] = tasting
        # auto-upsert verdict based on freshest tasting
        status = verdict_from_mean(sensory_mean)
        rationale = f"Moyenne sensorielle {mean_to_label(sensory_mean)} sur le dernier shot"
        self.upsert_verdict(VerdictCreate(coffee_id=shot.coffee_id, status=status, rationale=rationale))
        return tasting

    def delete_tasting(self, tasting_id: UUID) -> None:
        self._tastings.pop(tasting_id, None)

    # Verdicts
    def list_verdicts(self) -> list[Verdict]:
        return list(self._verdicts.values())

    def get_verdict(self, verdict_id: UUID) -> Verdict | None:
        return self._verdicts.get(verdict_id)

    def upsert_verdict(self, payload: VerdictCreate, verdict_id: UUID | None = None) -> Verdict:
        instance = self._verdicts.get(verdict_id) if verdict_id else None
        if instance is None:
            # ensure uniqueness per coffee
            existing = next(
                (v for v in self._verdicts.values() if v.coffee_id == payload.coffee_id),
                None,
            )
            instance = existing or Verdict(coffee_id=payload.coffee_id, status=payload.status, rationale=payload.rationale)
        for field, value in payload.model_dump().items():
            setattr(instance, field, value)
        self._verdicts[instance.id] = instance
        return instance

    def delete_verdict(self, verdict_id: UUID) -> None:
        self._verdicts.pop(verdict_id, None)

    # Helpers for analytics
    def shots_by_coffee(self, coffee_id: UUID):
        return [shot for shot in self._shots.values() if shot.coffee_id == coffee_id]

    def tastings_by_coffee(self, coffee_id: UUID) -> list[Tasting]:
        coffee_shots = {shot.id for shot in self.shots_by_coffee(coffee_id)}
        return [t for t in self._tastings.values() if t.shot_id in coffee_shots]

    def tasting_counts(self) -> dict[UUID, int]:
        counts: dict[UUID, int] = defaultdict(int)
        for tasting in self._tastings.values():
            shot = self._shots.get(tasting.shot_id)
            if shot:
                counts[shot.coffee_id] += 1
        for coffee_id in self._coffees:
            counts.setdefault(coffee_id, 0)
        return counts
