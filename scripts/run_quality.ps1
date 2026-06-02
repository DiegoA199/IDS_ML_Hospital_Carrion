$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

& ".\.venv\Scripts\python.exe" -m pytest --cov=src --cov-report=xml

if (Get-Command sonar-scanner -ErrorAction SilentlyContinue) {
    sonar-scanner
} else {
    Write-Host "sonar-scanner no esta instalado. Coverage generado en coverage.xml."
    Write-Host "Para SonarCloud, use el workflow .github/workflows/quality-sonar.yml con el secreto SONAR_TOKEN."
}
