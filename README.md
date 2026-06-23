# IDS-ML Hospital Carrion

Sistema IDS-ML en Python y Streamlit para tesis:

**"Diseno y evaluacion comparativa de modelos de machine learning para un sistema de deteccion de intrusiones orientado a la identificacion de amenazas en redes institucionales".**

El prototipo esta orientado a una red institucional hospitalaria. Trabaja con datasets CSV autorizados, compara modelos de machine learning y registra inferencias, alertas, reportes y trazabilidad.

## Inicio rapido

### Opcion A: Docker recomendado

Requisitos: Git y Docker Desktop.

```powershell
git clone https://github.com/DiegoA199/IDS_ML_Hospital_Carrion.git
cd IDS_ML_Hospital_Carrion
copy .env.example .env
docker compose up -d --build
```

Servicios:

| Servicio | URL / host | Uso |
|---|---|---|
| Streamlit | `http://localhost:8501` | Aplicacion IDS-ML |
| Adminer | `http://localhost:8080` | Gestor grafico de PostgreSQL |
| PostgreSQL | `localhost:5432` | Motor relacional |

Credenciales por defecto para Adminer si no se cambia `.env`:

```text
Sistema: PostgreSQL
Servidor: db
Usuario: idsml
Contrasena: idsml_dev_password
Base de datos: idsml
```

Para produccion, cambie `POSTGRES_PASSWORD` en `.env` o en el gestor de secretos del proveedor.

### Opcion B: ejecucion local con Python

Windows:

```powershell
.\scripts\run_local.ps1
```

Linux/macOS:

```bash
bash scripts/run_local.sh
```

Tambien puede hacerse manualmente:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

Abrir `http://localhost:8501`.

## Credenciales demo de la app

| Usuario | Contrasena | Rol |
|---|---|---|
| `admin` | `admin123` | Administrador TI |
| `analista` | `analista123` | Analista TI |
| `invitado` | `invitado123` | Invitado/demo |

Estas credenciales son solo para laboratorio y sustentacion. Antes de produccion real deben reemplazarse por IAM, LDAP, OAuth o un servicio institucional equivalente.

## Modulos del sistema

- Login por roles.
- Dashboard ejecutivo IDS.
- Carga y perfilado de dataset.
- Preprocesamiento de datos.
- Entrenamiento y comparacion de modelos.
- Seleccion automatica del mejor modelo por F1-score.
- Analisis de trafico nuevo.
- Centro de alertas TI.
- Reportes y trazabilidad.
- Administracion de usuarios y roles.
- Configuracion y estado del sistema.
- Vista academica del modelo de base de datos.
- Persistencia desacoplada por repository pattern.

## Arquitectura

| Ruta | Rol |
|---|---|
| `app.py` | Orquestador Streamlit minimo. |
| `src/app/` | Componentes, estilos y estructura de aplicacion. |
| `src/core/` | Configuracion no sensible, constantes, excepciones y seguridad auxiliar. |
| `src/domain/entities/` | Entidades de dominio. |
| `src/domain/services/` | Servicios testeables sin dependencia de Streamlit. |
| `src/ml/` | Facades ML para carga, preprocesamiento, entrenamiento, evaluacion y prediccion. |
| `src/preprocessing/` | Pipeline de preprocesamiento sin fuga de datos. |
| `src/models/` | Entrenamiento, evaluacion y persistencia Joblib. |
| `src/storage/` | Repositorios SQLite, PostgreSQL, Firestore y `repository_factory`. |
| `src/ui/` | Vistas Streamlit y tema visual. |
| `database/` | Modelo relacional academico de 60 tablas. |
| `docs/` | Documentacion de base de datos, pruebas y SonarQube. |
| `tests/` | Pruebas unitarias, integracion y fixtures. |

## Base de datos

El proyecto contiene un modelo relacional formal de 60 tablas para el IDS-ML hospitalario:

- `database/schema.sql`: version SQLite para pruebas locales.
- `database/postgresql/schema.sql`: version PostgreSQL para Docker/produccion.
- `database/seed_demo.sql`: datos demo para SQLite.
- `database/postgresql/seed_demo.sql`: datos demo para PostgreSQL.
- `docs/base_datos/modelo_er_ids_ml.dbml`: modelo para dbdiagram.io.
- `docs/base_datos/diccionario_datos.md`: diccionario de datos.

Crear una base SQLite local:

```powershell
py -3 database/init_db.py --db idsml_relational.db
```

Ver graficamente:

- Docker: Adminer en `http://localhost:8080`.
- SQLite local: SQLiteStudio o DBeaver abriendo el archivo `.db`.
- Diagrama ER: pegar `docs/base_datos/modelo_er_ids_ml.dbml` en dbdiagram.io.

## Machine learning

Modelos incluidos:

- Random Forest.
- Decision Tree.
- Logistic Regression.
- SVM.
- KNN.
- Naive Bayes.

El sistema mantiene carga de dataset, validacion, limpieza, codificacion, escalamiento, particion train/test, entrenamiento, comparacion por Accuracy/Precision/Recall/F1-score, seleccion por F1-score, guardado de modelo, prediccion de trafico nuevo y generacion de alertas.

## Pruebas

```powershell
pytest
pytest --cov=src --cov-report=xml
```

Ejecucion completa de calidad:

```powershell
.\scripts\run_quality.ps1
```

Documentacion:

- `docs/testing/plan_pruebas_ids_ml.md`
- `docs/testing/casos_prueba_ids_ml.md`

## SonarQube / SonarCloud

El proyecto incluye:

- `sonar-project.properties`
- `.coveragerc`
- `pytest.ini`
- `.github/workflows/quality-sonar.yml`
- `scripts/run_quality.ps1`
- `scripts/run_quality.sh`
- `docs/sonarqube/configuracion_sonar.md`
- `docs/sonarqube/evidencia_quality_gate_sonarcloud.md`
- `docs/sonarqube/reporte_calidad_sonar_ids_ml.md`

Flujo local:

```powershell
pytest --cov=src --cov-report=xml
sonar-scanner
```

Flujo recomendado en GitHub:

1. Crear el proyecto en SonarCloud con:

   ```text
   sonar.projectKey=DiegoA199_IDS_ML_Hospital_Carrion
   sonar.organization=diegoa199
   ```

2. Crear el secreto `SONAR_TOKEN` en:

   ```text
   GitHub > Repository > Settings > Secrets and variables > Actions
   ```

3. Hacer `push` a `main`. GitHub Actions ejecuta tests, genera `coverage.xml` y lanza el analisis Sonar.

Estado verificado:

- `44 passed`
- cobertura efectiva: `92%`
- reporte local de calidad: `docs/sonarqube/reporte_calidad_sonar_ids_ml.md`
- evidencia oficial: `docs/sonarqube/evidencia_quality_gate_sonarcloud.md`
- SonarCloud oficial: `Quality Gate OK`, `0 bugs`, `0 vulnerabilities`, `0 code smells`, `0 security hotspots`, `0.0%` duplicacion.

Dashboard oficial:

```text
https://sonarcloud.io/project/overview?id=DiegoA199_IDS_ML_Hospital_Carrion
```

## Evidencias para tesis

El repositorio incluye evidencias reales y material visual listo para anexar al informe.

Evidencias reales capturadas desde herramientas:

- `docs/evidencias/reales/informe_evidencias_reales_ids_ml.md`
- `docs/evidencias/reales/streamlit_dashboard_real.png`
- `docs/evidencias/reales/adminer_postgresql_tablas_real.png`
- `docs/evidencias/reales/sonarcloud_dashboard_real.png`
- `docs/evidencias/reales/github_actions_success_real.png`
- `docs/evidencias/reales/postgresql_tablas_reales.txt`
- `docs/evidencias/reales/sonarcloud_quality_gate_api_real.txt`

Material explicativo/referencial:

- `docs/evidencias/informe_evidencias_ids_ml.md`
- `docs/INFORME_EVIDENCIAS_TECNICAS_IDSML.docx`
- `docs/evidencias/sonarqube_quality_gate.png`
- `docs/evidencias/base_datos_60_tablas.png`
- `docs/evidencias/base_datos_listado_60_tablas.png`
- `docs/evidencias/proceso_hospital_ids_ml_bpmn.png`
- `docs/evidencias/orientacion_iso_nist_ids_ml.png`
- `docs/procesos/procesos_hospital_ids_ml.md`

Nota: no se encontro un archivo real de Bizagi/BPMN del proceso hospitalario; ese insumo debe exportarse desde Bizagi Modeler si el asesor lo exige como evidencia externa.

## Seguridad de credenciales

No versionar:

- `.streamlit/secrets.toml`
- `.env`
- `secrets.toml`
- archivos `*.json` privados
- bases `*.db` con datos sensibles
- `coverage.xml`
- `htmlcov/`

`Firestore` se mantiene desacoplado mediante `repository_factory`. Si no hay credenciales validas, el sistema usa SQLite como fallback. Para despliegues con Docker, el backend recomendado es PostgreSQL.

## Despliegue en servidor

### Render

El repo esta preparado para Render con Docker y PostgreSQL externo. Esta configuracion evita que Render cree una base administrada propia y pida pago por el motor de base de datos.

- `render.yaml` define solo el web service.
- `scripts/start_render.sh` inicializa las 60 tablas y arranca Streamlit.
- `database/init_postgres.py` ejecuta `database/postgresql/schema.sql` y carga seed demo si la base esta vacia.

Flujo recomendado:

1. Subir cambios a GitHub.
2. Crear una base PostgreSQL gratuita externa, por ejemplo en Neon o Supabase.
3. Copiar la cadena de conexion PostgreSQL.
4. En Render: **New > Blueprint**.
5. Conectar este repositorio.
6. Confirmar el archivo `render.yaml`.
7. Cuando Render solicite `DATABASE_URL`, pegar la cadena de conexion externa.
8. Crear el Blueprint y esperar el deploy.

La URL final sera similar a:

```text
https://ids-ml-hospital-carrion.onrender.com
```

Guia completa: `docs/deployment/render.md`.

Variables relevantes si se configura manualmente:

```text
IDSML_PERSISTENCE_BACKEND=postgres
DATABASE_URL=<URL externa de PostgreSQL>
PYTHONUNBUFFERED=1
```

Render debe arrancar Streamlit con el puerto asignado por `PORT`; el `Dockerfile` ya esta preparado para eso.

### VPS o servidor propio

En un VPS o servidor con Docker:

```bash
git clone https://github.com/DiegoA199/IDS_ML_Hospital_Carrion.git
cd IDS_ML_Hospital_Carrion
cp .env.example .env
docker compose up -d --build
```

Recomendacion para produccion:

- Exponer solo Streamlit detras de Nginx, Caddy o un proxy HTTPS.
- No publicar Adminer hacia Internet sin VPN, autenticacion adicional o firewall.
- Cambiar credenciales demo.
- Cambiar `POSTGRES_PASSWORD`.
- Guardar secretos en variables del proveedor, no en Git.

## Pendientes

- Integrar progresivamente las 60 tablas formales con todos los repositorios operativos.
- Reemplazar autenticacion demo por IAM institucional.
- Validar el flujo completo con datasets reales de tesis.
- Mantener actualizada la evidencia SonarQube/SonarCloud despues de cambios grandes.
- Revisar rendimiento con datasets grandes antes de uso institucional.
