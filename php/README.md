# Barisense PHP (Laragon)

Application PHP prête à déposer dans `E:\\laragon\\www\\barisenseV02` pour exposer l'API Barisense sans dépendance externe (pas de base de données à configurer). L'API est volontairement simple et stocke les données dans un fichier JSON.

## Structure
- `public/index.php` : point d'entrée (à placer dans le dossier web Laragon).
- `src/` : logique métier (données, calculs, routage).
- `storage/data.json` : persistance locale (créé automatiquement si absent).

## Installation rapide (Laragon)
1. Copier le dossier `php` dans `E:\\laragon\\www\\barisenseV02` (le contenu peut être directement au niveau racine : `E:\\laragon\\www\\barisenseV02\\public`, `E:\\laragon\\www\\barisenseV02\\src`, `E:\\laragon\\www\\barisenseV02\\storage`).
2. Dans Laragon, créer un site pointant vers `E:\\laragon\\www\\barisenseV02\\public`.
3. Démarrer Apache (ou Nginx) depuis Laragon puis accéder à `http://barisenseV02.test/api/health` pour vérifier que l'API répond.

## Configuration
Les paramètres de base se trouvent dans `src/config.php` :
- `api_prefix` : `/api/v1` (routes principales), `/api/health` pour le healthcheck.
- `api_key_header` : `X-API-Key`.
- `api_key` : clé optionnelle (défaut `null` = pas de vérification). Renseigner une valeur pour activer la protection.
- `storage_file` : chemin du fichier JSON (par défaut `storage/data.json`).

## Routes clés
- `GET /api/health` : disponibilité.
- `GET|POST|PUT|DELETE /api/v1/coffees` : lots de cafés.
- `GET|POST|PUT|DELETE /api/v1/waters` : eaux.
- `GET|POST|PUT|DELETE /api/v1/shots` : extractions.
- `GET|POST|PUT|DELETE /api/v1/tastings` : dégustations (génèrent automatiquement un verdict associé au café).
- `GET|POST|PUT|DELETE /api/v1/verdicts` : verdicts manuels.
- `GET /api/v1/analytics/rankings/{global|ristretto|expresso}` : classements.
- `GET /api/v1/analytics/quality-price` : rapport qualité/prix.
- `GET /api/v1/analytics/stability` : stabilité des cafés.
- `GET /api/v1/analytics/retest` : cafés à retester.

## Notes d'exploitation
- Les données sont stockées en JSON ; effectuer des sauvegardes régulières du dossier `storage/`.
- Chaque ressource retourne des horodatages ISO 8601 ; les identifiants sont en UUID v4.
- CORS est ouvert par défaut (origines `*`).
