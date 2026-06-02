#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

python -m pytest --cov=src --cov-report=xml

if command -v sonar-scanner >/dev/null 2>&1; then
  sonar-scanner
else
  echo "sonar-scanner no esta instalado. Coverage generado en coverage.xml."
  echo "Para SonarCloud, use .github/workflows/quality-sonar.yml con el secreto SONAR_TOKEN."
fi
