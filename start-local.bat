@echo off
setlocal enabledelayedexpansion

set "ROOT=%~dp0"
if not defined BACKEND_PORT set "BACKEND_PORT=8000"
if not defined FRONTEND_PORT set "FRONTEND_PORT=4173"

rem Détection de Python
where python >nul 2>&1
if %errorlevel%==0 (
  set "PYTHON_CMD=python"
) else (
  where py >nul 2>&1
  if %errorlevel%==0 (
    set "PYTHON_CMD=py"
  ) else (
    echo Python est requis pour lancer le backend. Installe-le puis relance le script.
    exit /b 1
  )
)

rem Vérification de npm
where npm >nul 2>&1
if %errorlevel% neq 0 (
  echo npm est requis pour lancer le frontend. Installe Node.js puis relance le script.
  exit /b 1
)

echo Installation/validation des dependances backend...
pushd "%ROOT%backend"
%PYTHON_CMD% -m pip install -r requirements.txt
start "Barisense API" %PYTHON_CMD% -m uvicorn app.main:app --host 0.0.0.0 --port %BACKEND_PORT%
popd

echo Installation/validation des dependances frontend...
pushd "%ROOT%frontend"
if not exist node_modules (
  npm install
)
start "Barisense UI" npm run dev -- --host --port %FRONTEND_PORT%
popd

start "Barisense" http://localhost:%FRONTEND_PORT%
echo.
echo Barisense est pret. Fermez les fenetres "Barisense API" et "Barisense UI" ou utilisez Ctrl+C dans ces consoles pour arreter.
pause
