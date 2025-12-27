# Backend

API, logique métier et moteur de calcul de Barisense.

## Objectifs
- Séparer strictement extraction, dégustation, analyse et classement.
- Stocker les scores sensoriels de manière numérique sans exposition directe.
- Fournir des verdicts traçables et justifiables.

## Architecture actuelle
- **FastAPI** pour l’API et les validations.
- **Pydantic** pour les modèles métiers (café, shot, dégustation, eau).
- Services dédiés pour les calculs (coût par shot, ratio d’extraction, moyenne sensorielle).
- Dépôt mémoire pour prototyper les flux avant la couche de persistance réelle.

Arborescence :
```
backend/
├── app/
│   ├── api/routes/         # Endpoints versionnés (coffees, shots, tastings, waters)
│   ├── core/               # Configuration et dépendances communes
│   ├── models/             # Schémas Pydantic
│   └── services/           # Calculs et dépôt en mémoire
├── requirements.txt        # Dépendances runtime
├── requirements-dev.txt    # Dépendances dev/tests
└── tests/                  # Tests rapides (pytest + TestClient)
```

## Développement local
1) Installer les dépendances :
```bash
cd backend
python -m pip install -r requirements-dev.txt
```

2) Lancer l’API :
```bash
uvicorn app.main:app --reload --port 8000
```

3) Exécuter les tests :
```bash
pytest
```

> Astuce : FastAPI expose une documentation interactive sur http://localhost:8000/docs.

## Prochaines étapes
- Brancher la persistance (SQL ou NoSQL) pour remplacer le dépôt en mémoire.
- Ajouter l’authentification et la gestion des utilisateurs.
- Traduire les calculs métier complets (classements, verdicts détaillés, effets de l’eau).
