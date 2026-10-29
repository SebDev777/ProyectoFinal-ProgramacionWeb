#!/usr/bin/env bash
# Prepara el proyecto en macOS / Linux: crea .venv, instala librerías y copia .env
set -e
cd "$(dirname "$0")"

echo "→ Creando entorno virtual .venv"
py -m venv .venv

echo "→ Instalando librerías"
.venv/Scripts/python -m pip install --upgrade pip -q
.venv/Scripts/python -m pip install -r requirements-dev.txt -q

if [ ! -f .env ]; then
  cp .env.example .env
  echo "→ Se creó el archivo .env: edítalo con tu usuario y contraseña de PostgreSQL"
fi

source .venv/Scripts/activate