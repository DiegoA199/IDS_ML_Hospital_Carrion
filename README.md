# IDS-ML — MVP operativo (Hospital Daniel Alcides Carrión)

Sistema **IDS-ML** orientado al **Hospital Regional Docente Clínico Quirúrgico Daniel Alcides Carrión** (Huancayo, Perú), en modo **MVP** para **ambiente controlado** (CSV / datos autorizados). **No** interviene la red institucional sin autorización explícita del área TI.

Investigación asociada: *Diseño y evaluación comparativa de modelos de machine learning para un prototipo IDS-ML orientado a la detección de intrusiones e identificación de amenazas en la red institucional del Hospital Regional Docente Clínico Quirúrgico Daniel Alcides Carrión*.

## Qué hace el MVP

- Carga y perfilado de datasets (CSV).
- Preprocesamiento riguroso (train/test, sin fuga, `ColumnTransformer`, SMOTE opcional).
- Entrenamiento comparativo (scikit-learn), selección por **F1-score**, persistencia **Joblib** del mejor modelo + pipeline.
- **Inferencia** sobre CSV nuevo → predicciones → **alertas reales** con metadatos (modelo, backend, severidad, confianza).
- **Persistencia real**: experimentos, predicciones por fila, alertas, bitácora estructurada, errores, reportes exportados.
- **Repository Pattern**: **SQLite** (local/respaldo) y **Firestore** (nube); **fallback** automático a SQLite si Firestore no está o falla.
- **RBAC** mínimo (Administrador TI / Analista TI / Invitado).
- **Docker** + instrucciones para **Streamlit Cloud / Render**.

## Stack

Python · Streamlit · scikit-learn · Pandas · NumPy · Plotly · Matplotlib · Joblib · SQLite · Firebase/Firestore · Docker · GitHub.

## Arquitectura modular

| Ruta | Rol |
|------|-----|
| `app.py` | Orquestador mínimo (config, auth, router). |
| `src/ui/router.py` | Enrutador de módulos. |
| `src/ui/pages.py` | Páginas Streamlit (Dataset, Entrenamiento, Inferencia, …). |
| `src/preprocessing/` | Pipeline ML sin fuga. |
| `src/models/` | Entrenamiento, persistencia Joblib. |
| `src/alerts/` | Construcción de alertas. |
| `src/storage/` | `IDSMLRepository`, SQLite, Firestore, factory. |
| `src/audit/` | Bitácora (`log_action`). |
| `src/security/` | RBAC. |
| `src/services/` | Dashboard y estado del sistema. |
| `src/reports/` | Exportación CSV/PDF. |

## Instalación local

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

## Docker

```bash
docker compose build
docker compose up
```

Abrir `http://localhost:8501`. Los volúmenes montan `./data` y `./artifacts` para conservar reportes y modelos entre reinicios.

## Despliegue cloud (Streamlit Cloud / Render)

1. Repositorio en **GitHub** sin secretos.
2. Punto de entrada: `app.py`.
3. Secretos en el panel (equivalente a `.streamlit/secrets.toml`): ver **`.streamlit/secrets.toml.example`**.
4. Variables típicas: `IDSML_PERSISTENCE_BACKEND`, `FIREBASE_PROJECT_ID`, `GOOGLE_APPLICATION_CREDENTIALS` (ruta o configuración que provea el proveedor cloud).

## Usuarios demo (solo laboratorio / piloto)

| Usuario   | Contraseña   | Rol                | Capacidades resumidas        |
|-----------|--------------|--------------------|------------------------------|
| admin     | admin123     | Administrador TI   | Todo + cambio estado alertas |
| analista  | analista123  | Analista TI        | Dataset, train, infer, reportes |
| invitado  | invitado123  | Invitado/demo      | Dashboard + dataset (lectura carga) |

Sustituir por identidad institucional (LDAP/OAuth) antes de producción real.

## Seguridad

No versionar: `.streamlit/secrets.toml`, `.env`, JSON de Firebase, `*.db` con datos sensibles. Revisar `.gitignore` y `.dockerignore`.

## Licencia / uso

Uso académico y piloto controlado hasta completar criterios de seguridad y gobierno institucional.
