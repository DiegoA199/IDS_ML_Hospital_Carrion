# Evidencias reales capturadas

Esta carpeta contiene capturas y archivos reales obtenidos desde herramientas ejecutadas o servicios vinculados al proyecto. A diferencia de las laminas explicativas de `docs/evidencias/`, estos archivos no son mockups: provienen de SonarCloud, GitHub Actions, Adminer/PostgreSQL y la aplicacion Streamlit corriendo en Docker.

| Archivo | Origen real | Uso |
|---|---|---|
| `sonarcloud_dashboard_real.png` | Dashboard publico de SonarCloud | Evidencia visual del Quality Gate aprobado. |
| `github_actions_success_real.png` | GitHub Actions | Evidencia visual del workflow `Quality and Sonar` en estado `success`. |
| `adminer_postgresql_tablas_real.png` | Adminer conectado a PostgreSQL Docker | Evidencia fisica de las tablas en el motor de base de datos. |
| `streamlit_dashboard_real.png` | Aplicacion Streamlit local | Evidencia de la interfaz real del sistema ejecutandose. |
| `sonarcloud_quality_gate_api_real.json` | API publica de SonarCloud | Respuesta tecnica del Quality Gate. |
| `sonarcloud_metrics_api_real.json` | API publica de SonarCloud | Metricas reales: bugs, vulnerabilidades, code smells, hotspots y duplicacion. |
| `github_actions_latest_run_real.json` | API publica de GitHub | Datos reales de la ultima corrida del workflow. |
| `postgresql_tablas_reales.txt` | `psql` dentro del contenedor PostgreSQL | Listado real de tablas en el esquema `public`. |
| `postgresql_conteo_tablas_reales.txt` | `psql` dentro del contenedor PostgreSQL | Conteo real de tablas visibles. |

## Nota sobre Bizagi

No se encontro un archivo real de Bizagi (`.bpm`, `.bpmn`) ni una imagen externa ya elaborada del proceso hospitalario en las carpetas locales revisadas. Para evidencia real de procesos, se debe exportar desde Bizagi Modeler o entregar el archivo fuente del diagrama.
