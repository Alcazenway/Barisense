# Backend

API, logique métier et moteur de calcul de Barisense.

## Objectifs
- Séparer strictement extraction, dégustation, analyse et classement.
- Stocker les scores sensoriels de manière numérique sans exposition directe.
- Fournir des verdicts traçables et justifiables.

## Pistes techniques
- API REST/GraphQL avec authentification simple.
- Services dédiés pour extraction, dégustation, analyse, classement et gestion de l’eau.
- Couche de persistance connectée aux schémas `db`.
- Jobs / scripts pour import/export et calculs périodiques si besoin.

## À faire
- Initialiser le projet backend (framework, lint, tests).
- Définir les modèles et DTOs pour cafés, shots, dégustations et eaux.
- Implémenter les endpoints et le moteur de calcul des classements et verdicts.

