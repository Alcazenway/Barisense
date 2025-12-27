# Barisense
Mon Appli Barista


☕ Barisense

Barisense est une application web personnelle dédiée au pilotage, à l’analyse et au classement objectif des cafés, principalement orientée Ristretto et Expresso, en lien avec une machine Sage Barista Express.

L’application transforme des données techniques, des jugements sensoriels exprimés en mots humains, des paramètres machine, de l’eau utilisée et des données de consommation / coût en décisions claires, traçables et justifiables.

🎯 Objectifs du projet

Identifier dans le temps les cafés réellement appréciés

Séparer strictement :

l’extraction (technique),

la dégustation (sensorielle),

l’analyse (calcul),

la décision (classement / verdict)

Garantir une évaluation fiable, indépendante des réglages hasardeux

Offrir une expérience fluide, moderne et ergonomique

Limiter la saisie manuelle au strict minimum grâce à l’automatisation

🧭 Principes fondamentaux
🔒 Séparation stricte des étapes
Étape	Rôle
Shot	Fait technique, sans jugement
Dégustation	Jugement sensoriel humain
Analyse	Calculs internes invisibles
Classement	Décision argumentée
🧠 Sensoriel dominant

Le ressenti humain prime

La technique sert uniquement à fiabiliser l’évaluation

👀 Chiffres invisibles

Les scores sensoriels sont stockés numériquement (1–5)

Aucun chiffre n’est jamais affiché

L’interface ne montre que des mots humains

🌐 Application web multi-périphériques

Accessible via navigateur Internet

Compatible :

PC

Tablette Android

Smartphone

Interface responsive (mobile-first)

Aucune installation locale requise pour l’utilisateur final

📝 Formulaires (piliers du système)

L’application repose volontairement sur 3 formulaires seulement.

1️⃣ Café — Achat & référentiel

Permet d’enregistrer un lot de café :

Marque / torréfacteur

Référence

Type (Grain / Moulu)

Poids du paquet

Prix payé

Date d’achat

👉 Calculs automatiques :

prix au kilo

coût estimé par shot

2️⃣ Shot — Extraction

Journal factuel et technique de chaque extraction :

Café utilisé

Type de boisson (Ristretto / Expresso / Café long)

Paramètres machine :

mouture

dose

poids en tasse

temps d’extraction

Eau utilisée (robinet ou bouteille)

👉 Aucun jugement sensoriel à ce stade.

3️⃣ Dégustation — Sensoriel humain

Jugement exprimé exclusivement avec des mots :

Acidité

Amertume

Corps

Arômes

Équilibre

Longueur en bouche

Appréciation globale

➡️ Les libellés sont convertis en valeurs numériques uniquement en back-end.

💧 Gestion de l’eau

L’eau est considérée comme un paramètre clé de l’extraction.

L’application permet :

de déclarer l’eau utilisée :

Robinet

Eau en bouteille (Volvic, Cristalline, etc.)

d’associer une eau à chaque shot

d’analyser l’impact de l’eau sur :

l’extraction

le rendu sensoriel

de filtrer les classements par type d’eau

🤖 Automatisation & intelligence applicative

MonEXpresso automatise :

les calculs de ratios et diagnostics d’extraction

l’historisation des réglages machine

les suggestions de paramètres par café / boisson

les moyennes et pondérations sensorielle

les scores globaux par café

les classements et verdicts

👉 L’utilisateur saisit, l’application apprend, calcule et décide.

📊 Analyses & classements

L’application produit automatiquement :

Classement global des cafés

Classement Ristretto

Classement Expresso

Meilleur rapport qualité / prix

Cafés les plus stables

Cafés à retester (manque de données)

Verdicts possibles

✅ Racheter

⚠️ À affiner

❌ À éviter

🔄 En observation

Chaque verdict est :

justifié

traçable

explicable

🧬 Architecture du projet
/frontend      → Interface utilisateur (responsive)
/backend       → API + logique métier + moteur de calcul
/db            → Schémas, migrations, dataset de test
/docs          → Règles métier, mappings, documentation
/scripts       → Import / export / maintenance

🧪 Dataset & tests

Dataset de test fourni :

≥ 20 cafés

≥ 100 shots

variations de réglages et d’eau

Objectif :

valider la robustesse des calculs

garantir la cohérence des classements

🔐 Usage & confidentialité

Application à usage personnel

Données privées

Authentification simple

Exports CSV / JSON possibles

Aucune donnée partagée par défaut

🚀 État du projet

📦 Version actuelle : en cours de construction
🧩 Méthode : développement assisté par Codex
🐙 Plateforme : GitHub
🧠 Vision : long terme, évolutive, rigoureuse

☕ Philosophie

MonEXpresso n’est pas un carnet de notes.

C’est un outil d’aide à la décision, pensé pour transformer une pratique quotidienne en connaissance fiable.

## Lancement simplifié (double-clic)

Objectif : ouvrir Barisense via un simple raccourci qui pointe vers l’URL locale.

1. **Démarrage en un double-clic**
   - macOS / Linux : double-clique sur `start-local.sh` (ou lance `./start-local.sh` dans un terminal).
   - Windows : double-clique sur `start-local.bat`.
   - Le script installe les dépendances si besoin, démarre l’API FastAPI (port `8000`) et le frontend (port `4173`), puis ouvre automatiquement le navigateur sur `http://localhost:4173`.

2. **Créer le raccourci/icone vers l’URL**
   - Crée un favori ou un raccourci de bureau pointant vers `http://localhost:4173`.
   - Tant que les fenêtres lancées par le script restent ouvertes, un double-clic sur ce raccourci ouvre l’application prête à l’emploi.

3. **Arrêt**
   - macOS / Linux : `Ctrl+C` dans le terminal du script.
   - Windows : ferme les fenêtres « Barisense API » et « Barisense UI » ou `Ctrl+C` dans la fenêtre principale.
