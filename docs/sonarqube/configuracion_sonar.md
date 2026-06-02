# Configuracion de SonarQube/SonarCloud para IDS-ML

## 1. Que se evalua

El analisis de calidad revisa el codigo Python del sistema IDS-ML para detectar:

- bugs;
- vulnerabilities;
- security hotspots;
- code smells;
- duplicacion;
- cobertura de pruebas;
- maintainability;
- reliability;
- security.

El codigo fuente analizable esta en `src/`. Se excluyen documentos, esquemas SQL, prototipos, notebooks, bases locales y archivos generados.

## 2. Por donde tiene que pasar

El flujo recomendado para que el proyecto pase por SonarCloud es:

1. Desarrollador hace `push` a GitHub.
2. GitHub Actions ejecuta `.github/workflows/quality-sonar.yml`.
3. El workflow instala dependencias con `requirements.txt`.
4. Ejecuta:

   ```bash
   python -m pytest --cov=src --cov-report=xml
   ```

5. Se genera `coverage.xml`.
6. Si existe el secreto `SONAR_TOKEN`, se ejecuta el analisis Sonar.
7. SonarCloud calcula el Quality Gate.
8. El resultado queda visible en GitHub Actions y en el dashboard de SonarCloud.

Tambien puede ejecutarse manualmente desde GitHub:

```text
GitHub > Actions > Quality and Sonar > Run workflow
```

Esta ejecucion manual funciona despues de importar el proyecto en SonarCloud y crear el secreto `SONAR_TOKEN`.

## 3. Archivos configurados

- `sonar-project.properties`: configuracion principal del analisis.
- `.coveragerc`: reglas de cobertura para Python.
- `pytest.ini`: configuracion de pytest.
- `.github/workflows/quality-sonar.yml`: CI para tests, coverage y Sonar.
- `scripts/run_quality.ps1`: ejecucion local en Windows.
- `scripts/run_quality.sh`: ejecucion local en Linux/macOS.

## 4. Configurar SonarCloud

En SonarCloud:

1. Entrar a `https://sonarcloud.io`.
2. Iniciar sesion con GitHub.
3. Importar el repositorio `DiegoA199/IDS_ML_Hospital_Carrion`.
4. Crear o verificar el proyecto con:

   ```text
   sonar.projectKey=DiegoA199_IDS_ML_Hospital_Carrion
   sonar.organization=diegoa199
   ```

5. Generar un token de analisis.
6. En GitHub abrir:

   ```text
   Repository > Settings > Secrets and variables > Actions > New repository secret
   ```

7. Crear el secreto:

   ```text
   Name: SONAR_TOKEN
   Value: <token generado por SonarCloud>
   ```

No subir el token al repositorio.

Sin `SONAR_TOKEN`, GitHub Actions puede ejecutar pruebas y cobertura, pero el paso oficial de SonarCloud queda omitido.

## 5. Ejecutar localmente

Windows:

```powershell
.\scripts\run_quality.ps1
```

Manual:

```powershell
pytest --cov=src --cov-report=xml
sonar-scanner
```

Si `sonar-scanner` no esta instalado, el script genera `coverage.xml` y deja el analisis para GitHub Actions.

## 6. Quality Gate esperado

Para considerar el proyecto listo para sustentacion:

- `pytest` debe finalizar sin errores.
- `coverage.xml` debe generarse correctamente.
- SonarCloud debe importar la cobertura.
- El Quality Gate no debe reportar bugs criticos ni vulnerabilidades bloqueantes.
- La duplicacion debe mantenerse baja.
- Los code smells deben estar justificados o corregidos.
- La cobertura debe concentrarse en logica de negocio, ML, repositorios y servicios.

## 7. Exclusiones justificadas

Se excluyen de cobertura:

- vistas Streamlit y componentes visuales (`src/ui/**`, `src/app/**`);
- entidades tipo dataclass (`src/domain/entities/**`);
- facades simples de ML (`src/ml/**`);
- adaptador PostgreSQL opcional hasta contar con CI con servicio PostgreSQL;
- documentos, SQL y prototipos.

Estas exclusiones evitan medir como deuda de pruebas partes visuales o documentales. El analisis de mantenibilidad sigue revisando `src/`.

## 8. Evidencias para la tesis

Guardar capturas de:

- GitHub Actions con tests exitosos;
- `coverage.xml` generado;
- dashboard de SonarCloud;
- Quality Gate;
- lista de issues relevantes y acciones correctivas.

## 9. Recomendaciones

- No versionar `.env`, `secrets.toml`, JSON privados ni `coverage.xml`.
- Mantener la logica de negocio fuera de vistas Streamlit.
- Agregar pruebas cuando se modifiquen servicios, repositorios o pipeline ML.
- Si SonarCloud falla por project key u organizacion, ajustar `sonar-project.properties` segun el proyecto creado en SonarCloud.
