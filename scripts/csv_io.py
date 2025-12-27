from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable, List, Optional

from .dataset import Coffee, Dataset, Shot, Tasting, Water


def import_from_csv(
    coffees_csv: Path,
    shots_csv: Path,
    tastings_csv: Path,
    waters_csv: Optional[Path] = None,
) -> Dataset:
    return Dataset(
        coffees=[_coffee_from_row(row) for row in _read_csv(coffees_csv)],
        shots=[_shot_from_row(row) for row in _read_csv(shots_csv)],
        tastings=[_tasting_from_row(row) for row in _read_csv(tastings_csv)],
        waters=[_water_from_row(row) for row in _read_csv(waters_csv)] if waters_csv else [],
    )


def export_to_csv(dataset: Dataset, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(
        output_dir / "coffees.csv",
        dataset.coffees,
        [
            "id",
            "name",
            "roaster",
            "reference",
            "type",
            "bag_weight_g",
            "price_eur",
            "purchase_date",
        ],
    )
    _write_csv(
        output_dir / "waters.csv",
        dataset.waters,
        [
            "id",
            "label",
            "source",
        ],
    )
    _write_csv(
        output_dir / "shots.csv",
        dataset.shots,
        [
            "id",
            "coffee_id",
            "water_id",
            "beverage_type",
            "dose_g",
            "yield_g",
            "duration_s",
            "grind",
        ],
    )
    _write_csv(
        output_dir / "tastings.csv",
        dataset.tastings,
        [
            "id",
            "shot_id",
            "acidity",
            "bitterness",
            "body",
            "aroma",
            "balance",
            "finish",
            "overall",
            "notes",
        ],
    )


def _read_csv(path: Path) -> Iterable[dict]:
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            yield {key: value.strip() if isinstance(value, str) else value for key, value in row.items()}


def _write_csv(path: Path, items: List, fieldnames: List[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for item in items:
            writer.writerow({field: getattr(item, field) for field in fieldnames})


def _coffee_from_row(row: dict) -> Coffee:
    return Coffee(
        id=row["id"],
        name=row["name"],
        roaster=row.get("roaster", ""),
        reference=_empty_to_none(row.get("reference")),
        type=_empty_to_none(row.get("type")),
        bag_weight_g=_as_int(row.get("bag_weight_g")),
        price_eur=_as_float(row.get("price_eur")),
        purchase_date=_empty_to_none(row.get("purchase_date")),
    )


def _water_from_row(row: dict) -> Water:
    return Water(
        id=row["id"],
        label=row["label"],
        source=_empty_to_none(row.get("source")),
    )


def _shot_from_row(row: dict) -> Shot:
    return Shot(
        id=row["id"],
        coffee_id=row["coffee_id"],
        water_id=_empty_to_none(row.get("water_id")),
        beverage_type=_empty_to_none(row.get("beverage_type")),
        dose_g=_as_float(row.get("dose_g")),
        yield_g=_as_float(row.get("yield_g")),
        duration_s=_as_float(row.get("duration_s")),
        grind=_empty_to_none(row.get("grind")),
    )


def _tasting_from_row(row: dict) -> Tasting:
    return Tasting(
        id=row["id"],
        shot_id=row["shot_id"],
        acidity=_empty_to_none(row.get("acidity")),
        bitterness=_empty_to_none(row.get("bitterness")),
        body=_empty_to_none(row.get("body")),
        aroma=_empty_to_none(row.get("aroma")),
        balance=_empty_to_none(row.get("balance")),
        finish=_empty_to_none(row.get("finish")),
        overall=_empty_to_none(row.get("overall")),
        notes=_empty_to_none(row.get("notes")),
    )


def _empty_to_none(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    return value or None


def _as_float(value: Optional[str]) -> Optional[float]:
    if value is None or value == "":
        return None
    return float(value)


def _as_int(value: Optional[str]) -> Optional[int]:
    if value is None or value == "":
        return None
    return int(value)
