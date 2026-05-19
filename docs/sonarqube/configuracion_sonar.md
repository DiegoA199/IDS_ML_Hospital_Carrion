# Configuración de SonarQube/SonarCloud para IDS-ML

## 1. Análisis de calidad aplicado al proyecto

El análisis de calidad permite revisar bugs, vulnerabilidades, code smells, duplicación, cobertura y mantenibilidad del código Python del sistema IDS-ML. Para este proyecto se analiza principalmente `src/`, dejando fuera documentos, prototipos, base de datos y artefactos generados.

## 2. Uso de SonarQube o SonarCloud

Opciones:

- **SonarQube local:** instalar Docker y ejecutar un contenedor de SonarQube Community.
- **SonarCloud:** conectar el repositorio GitHub y configurar `sonar-project.properties`.

## 3. Generar coverage.xml

```powershell
pytest --cov=src --cov-report=xml
```

El archivo `coverage.xml` se genera en la raíz del proyecto y no debe versionarse.

## 4. Ejecutar pytest

```powershell
pytest
```

## 5. Ejecutar análisis

Con SonarScanner instalado:

```powershell
sonar-scanner
```

En SonarCloud se requiere configurar token de forma segura en variables de entorno o secrets del proveedor CI/CD, nunca en el repositorio.

## 6. Carpetas excluidas

Se excluyen:

- entornos virtuales: `.venv`, `venv`;
- cachés: `__pycache__`, `.pytest_cache`;
- prototipos y diseño: `design`, `prototypes`;
- documentación: `docs`;
- base de datos documental: `database`;
- notebooks y artefactos generados.

## 7. Métricas revisadas

- Bugs.
- Vulnerabilities.
- Code smells.
- Duplicación.
- Cobertura.
- Maintainability.
- Reliability.
- Security.

## 8. Interpretar Quality Gate

El Quality Gate debe revisarse como criterio de control de calidad. Un fallo puede indicar baja cobertura, duplicación excesiva, problemas de seguridad o mantenibilidad. Para tesis, se recomienda adjuntar captura del Quality Gate y explicar hallazgos relevantes.

## 9. Recomendaciones

- Mantener funciones pequeñas y con responsabilidad única.
- Evitar SQL en vistas de Streamlit.
- Escribir pruebas para servicios y repositorios.
- Excluir documentos/prototipos del análisis de código.
- No versionar `coverage.xml`, credenciales, `.env`, JSON privados ni secrets.
- Revisar deuda técnica antes de la sustentación.

