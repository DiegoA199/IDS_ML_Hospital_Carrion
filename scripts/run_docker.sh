#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

if [ ! -f ".env" ]; then
  cp .env.example .env
  echo "Archivo .env creado desde .env.example. Revise POSTGRES_PASSWORD antes de produccion."
fi

docker compose up -d --build
docker compose ps
