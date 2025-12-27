#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_PORT="${BACKEND_PORT:-8000}"
FRONTEND_PORT="${FRONTEND_PORT:-4173}"

command_exists() {
  command -v "$1" >/dev/null 2>&1
}

# Find Python
if command_exists python3; then
  PYTHON_CMD="python3"
elif command_exists python; then
  PYTHON_CMD="python"
else
  echo "Python n'est pas installé (python ou python3 introuvable)." >&2
  exit 1
fi

if ! command_exists npm; then
  echo "npm est requis pour lancer le frontend. Installe Node.js puis relance le script." >&2
  exit 1
fi

cleanup() {
  echo ""
  echo "Arrêt des services Barisense..."
  if [[ -n "${BACKEND_PID:-}" ]] && ps -p "${BACKEND_PID}" >/dev/null 2>&1; then
    kill "${BACKEND_PID}" >/dev/null 2>&1 || true
  fi
  if [[ -n "${FRONTEND_PID:-}" ]] && ps -p "${FRONTEND_PID}" >/dev/null 2>&1; then
    kill "${FRONTEND_PID}" >/dev/null 2>&1 || true
  fi
}
trap cleanup EXIT INT TERM

echo "Installation/validation des dépendances backend..."
"${PYTHON_CMD}" -m pip install -r "${ROOT_DIR}/backend/requirements.txt"

echo "Installation/validation des dépendances frontend..."
(
  cd "${ROOT_DIR}/frontend"
  if [[ ! -d node_modules ]]; then
    npm install
  fi
)

echo "Démarrage de l'API FastAPI sur le port ${BACKEND_PORT}..."
(
  cd "${ROOT_DIR}/backend"
  "${PYTHON_CMD}" -m uvicorn app.main:app --host 0.0.0.0 --port "${BACKEND_PORT}"
) &
BACKEND_PID=$!

echo "Démarrage du frontend React sur le port ${FRONTEND_PORT}..."
(
  cd "${ROOT_DIR}/frontend"
  npm run dev -- --host --port "${FRONTEND_PORT}"
) &
FRONTEND_PID=$!

# Laisser le temps aux serveurs de démarrer puis ouvrir le navigateur.
"${PYTHON_CMD}" - <<PY
import time
import webbrowser

url = f"http://localhost:${FRONTEND_PORT}"
print(f"\nOuverture du navigateur sur {url} ...")

for _ in range(6):
    time.sleep(1)

webbrowser.open(url)
print("Barisense est prêt. Appuyez sur Ctrl+C pour arrêter les services.")
PY

wait
