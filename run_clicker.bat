@echo on
setlocal EnableExtensions
title Clicker Pygame - Lancement

REM Always run from this script's folder
cd /d "%~dp0"

echo.
echo ===== Clicker Pygame =====
echo Dossier: %CD%
echo.

REM Prefer the Python Launcher on Windows (py), fallback to python
set "PY="
where py >nul 2>&1
if not errorlevel 1 (
  set "PY=py -3"
) else (
  where python >nul 2>&1
  if not errorlevel 1 (
    set "PY=python"
  )
)

if "%PY%"=="" (
  echo ERREUR: Python est introuvable.
  echo - Installe Python 3
  echo - Coche "Add python.exe to PATH" ^(ou utilise le launcher 'py'^)
  goto :end
)

echo Utilisation de: %PY%
%PY% --version
if errorlevel 1 (
  echo.
  echo ATTENTION: %PY% ne fonctionne pas.
  echo Tentative avec: python
  where python >nul 2>&1
  if errorlevel 1 (
    echo ERREUR: Impossible d'executer Python.
    goto :end
  )
  set "PY=python"
  echo Utilisation de: %PY%
  %PY% --version
  if errorlevel 1 (
    echo ERREUR: Impossible d'executer Python.
    goto :end
  )
)

REM Install dependencies only if pygame is missing
%PY% -c "import pygame" >nul 2>&1
if errorlevel 1 (
  echo.
  echo Pygame non detecte. Installation des dependances...
  %PY% -m pip --version
  if errorlevel 1 (
    echo ERREUR: pip est indisponible. Essaie: %PY% -m ensurepip --upgrade
    goto :end
  )
  %PY% -m pip install --upgrade pip
  if errorlevel 1 goto :end
  %PY% -m pip install -r requirements.txt
  if errorlevel 1 goto :end
)

echo.
echo Lancement du jeu...
%PY% main.py
echo.
echo Code de retour: %ERRORLEVEL%

:end
echo.
echo (La fenetre reste ouverte pour afficher les messages.)
pause
