from __future__ import annotations

import argparse
from pathlib import Path

from .csv_io import export_to_csv, import_from_csv
from .dataset import Dataset
from .diagnostics import summarize


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Outils d'import/export et diagnostics pour les données Barisense."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    _configure_import_parser(subparsers)
    _configure_export_parser(subparsers)
    _configure_summary_parser(subparsers)

    args = parser.parse_args()
    if args.command == "import-csv":
        dataset = import_from_csv(
            coffees_csv=args.coffees,
            shots_csv=args.shots,
            tastings_csv=args.tastings,
            waters_csv=args.waters,
        )
        dataset.save(args.output)
        print(f"Dataset sauvegardé dans {args.output}")
    elif args.command == "export-csv":
        dataset = Dataset.load(args.dataset)
        export_to_csv(dataset, args.output_dir)
        print(f"Exports CSV générés dans {args.output_dir}")
    elif args.command == "summary":
        dataset = Dataset.load(args.dataset)
        summary = summarize(dataset, top=args.top)
        _print_summary(summary)


def _configure_import_parser(subparsers: argparse._SubParsersAction) -> None:
    importer = subparsers.add_parser("import-csv", help="Importer des fichiers CSV vers un dataset JSON.")
    importer.add_argument("--coffees", type=Path, required=True, help="CSV des cafés.")
    importer.add_argument("--shots", type=Path, required=True, help="CSV des extractions.")
    importer.add_argument("--tastings", type=Path, required=True, help="CSV des dégustations.")
    importer.add_argument("--waters", type=Path, help="CSV des eaux (optionnel).")
    importer.add_argument(
        "--output", type=Path, default=Path("db") / "dataset.json", help="Destination du dataset JSON."
    )


def _configure_export_parser(subparsers: argparse._SubParsersAction) -> None:
    exporter = subparsers.add_parser("export-csv", help="Exporter un dataset JSON vers des fichiers CSV.")
    exporter.add_argument(
        "--dataset", type=Path, default=Path("db") / "dataset.json", help="Chemin du dataset JSON à exporter."
    )
    exporter.add_argument(
        "--output-dir",
        type=Path,
        default=Path("scripts") / "exports",
        help="Dossier de sortie pour les fichiers CSV générés.",
    )


def _configure_summary_parser(subparsers: argparse._SubParsersAction) -> None:
    summary = subparsers.add_parser("summary", help="Afficher un diagnostic rapide du dataset.")
    summary.add_argument(
        "--dataset", type=Path, default=Path("db") / "dataset.json", help="Chemin du dataset JSON à analyser."
    )
    summary.add_argument(
        "--top", type=int, default=5, help="Nombre de cafés à afficher dans le classement par volume de shots."
    )


def _print_summary(summary) -> None:
    print("=== Diagnostic dataset ===")
    print(f"Cafés            : {summary.coffees}")
    print(f"Eaux             : {summary.waters}")
    print(f"Shots            : {summary.shots}")
    print(f"Dégustations     : {summary.tastings}")
    print(f"Shots sans dégustation : {summary.shots_without_tasting}")
    print(
        "Ratio moyen      : "
        + (_format_float(summary.average_brew_ratio) if summary.average_brew_ratio is not None else "n/a")
    )
    print(
        "Temps moyen (s)  : "
        + (_format_float(summary.average_extraction_time) if summary.average_extraction_time is not None else "n/a")
    )
    print("Top cafés (nb shots) :")
    for coffee_id, count in summary.top_coffees_by_shots.items():
        print(f"  - {coffee_id}: {count}")


def _format_float(value: float) -> str:
    return f"{value:.2f}"


if __name__ == "__main__":
    main()
