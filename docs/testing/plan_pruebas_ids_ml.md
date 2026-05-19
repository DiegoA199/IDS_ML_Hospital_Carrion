# Plan de pruebas del sistema IDS-ML para detección de intrusiones en redes institucionales

## 1. Introducción

Este plan define la estrategia de verificación del prototipo IDS-ML orientado a una red institucional hospitalaria. El propósito es asegurar que la carga de datos, preprocesamiento, entrenamiento, comparación de modelos, inferencia, generación de alertas, reportes, trazabilidad y almacenamiento funcionen de manera reproducible y defendible en un contexto académico.

## 2. Objetivo del plan de pruebas

Validar que el sistema IDS-ML cumpla sus funciones principales sin romper la separación entre interfaz, lógica de negocio, machine learning y persistencia, y que produzca evidencias útiles para revisión de tesis y análisis con SonarQube/SonarCloud.

## 3. Alcance

Incluye pruebas unitarias, integración, funcionales, interfaz, seguridad básica, calidad de datos, rendimiento básico y aceptación. No incluye pruebas de penetración sobre una red hospitalaria real ni captura de tráfico institucional sin autorización.

## 4. Módulos evaluados

- Autenticación y roles.
- Carga de dataset.
- Validación de calidad de datos.
- Preprocesamiento.
- Entrenamiento de modelos.
- Comparación de métricas.
- Selección del mejor modelo por F1-score.
- Análisis de tráfico nuevo.
- Generación de alertas.
- Reportes.
- Trazabilidad.
- Almacenamiento SQLite/Firestore mediante repository.

## 5. Tipos de pruebas

- **Unitarias:** validan servicios y funciones aisladas.
- **Integración:** validan SQLite, pipeline ML y reportes.
- **Funcionales:** validan flujos completos del sistema.
- **Interfaz:** validan navegación, roles, tablas, KPIs y feedback visual.
- **Seguridad básica:** validan que no se expongan secretos y que RBAC restrinja operaciones.
- **Calidad de datos:** validan nulos, duplicados, columnas faltantes y perfilado.
- **Rendimiento básico:** validan tiempos razonables con datasets pequeños/medianos.
- **Aceptación:** validan que el prototipo sea apto para exposición y evaluación con usuarios TI.

## 6. Herramientas

- pytest.
- pytest-cov.
- coverage.py.
- SonarQube o SonarCloud.
- Streamlit.
- SQLite.
- Firebase/Firestore si aplica.

## 7. Criterios de entrada

- Dependencias instaladas con `pip install -r requirements.txt`.
- Dataset de prueba disponible.
- Base SQLite inicializable.
- No existen secretos reales en el repositorio.
- La aplicación arranca con `streamlit run app.py`.

## 8. Criterios de salida

- `pytest` ejecuta correctamente.
- `pytest --cov=src --cov-report=xml` genera `coverage.xml`.
- La aplicación ejecuta los flujos principales.
- SonarQube/SonarCloud puede analizar `src` excluyendo docs, database, design y prototypes.
- Los hallazgos críticos quedan documentados.

## 9. Matriz de casos de prueba

| ID | Módulo | Tipo de prueba | Objetivo | Precondición | Datos de entrada | Pasos | Resultado esperado | Resultado obtenido | Estado | Evidencia |
|---|---|---|---|---|---|---|---|---|---|---|
| CP-001 | Autenticación | Unitaria | Validar credenciales admin | Servicio disponible | admin/admin123 | Ejecutar authenticate | Usuario con rol Administrador TI | Pendiente ejecución | Pendiente | pytest |
| CP-002 | Autenticación | Unitaria | Rechazar contraseña inválida | Servicio disponible | admin/error | Ejecutar authenticate | Resultado None | Pendiente ejecución | Pendiente | pytest |
| CP-003 | RBAC | Unitaria | Validar permiso de entrenamiento | Roles definidos | Analista TI | Ejecutar can_train | True | Pendiente ejecución | Pendiente | pytest |
| CP-004 | RBAC | Unitaria | Bloquear entrenamiento a invitado | Roles definidos | Invitado/demo | Ejecutar can_train | False | Pendiente ejecución | Pendiente | pytest |
| CP-005 | Dataset | Unitaria | Detectar dataset vacío | DataFrame vacío | vacío | validate_dataset | Error controlado | Pendiente ejecución | Pendiente | pytest |
| CP-006 | Dataset | Unitaria | Detectar columnas faltantes | DataFrame parcial | columna requerida | find_missing_columns | Lista de faltantes | Pendiente ejecución | Pendiente | pytest |
| CP-007 | Dataset | Unitaria | Detectar nulos | Dataset con NA | sample_dataset.csv | build_dataset_profile | Conteo de nulos correcto | Pendiente ejecución | Pendiente | pytest |
| CP-008 | Dataset | Unitaria | Detectar duplicados | Dataset duplicado | sample_dataset.csv | build_dataset_profile | Conteo duplicados correcto | Pendiente ejecución | Pendiente | pytest |
| CP-009 | Calidad | Unitaria | Calcular score de calidad | Perfil generado | Dataset perfilado | calculate_quality_score | Valor 0..100 | Pendiente ejecución | Pendiente | pytest |
| CP-010 | Preprocesamiento | Integración | Generar matrices train/test | Dataset válido | sample_dataset.csv | run_preprocessing | X_train y X_test no vacíos | Pendiente ejecución | Pendiente | pytest |
| CP-011 | Preprocesamiento | Integración | Codificar categóricas | Dataset mixto | cat/num/label | run_preprocessing | Matriz numérica | Pendiente ejecución | Pendiente | pytest |
| CP-012 | Preprocesamiento | Integración | Aplicar split sin fuga | Dataset válido | label | run_preprocessing | train+test coherente | Pendiente ejecución | Pendiente | pytest |
| CP-013 | ML | Unitaria | Calcular métricas | Resultados sintéticos | y_true/y_pred | train_and_evaluate | Métricas en rango | Pendiente ejecución | Pendiente | pytest |
| CP-014 | ML | Unitaria | Seleccionar mejor F1 | Lista de resultados | f1 distintos | choose_best_by_f1 | Mayor F1 | Pendiente ejecución | Pendiente | pytest |
| CP-015 | ML | Integración | Entrenar Random Forest | Dataset válido | sample_dataset.csv | train_candidate_models | Resultado RF | Pendiente ejecución | Pendiente | pytest |
| CP-016 | ML | Integración | Entrenar SVM | Dataset válido | sample_dataset.csv | train_candidate_models | Resultado SVM | Pendiente ejecución | Pendiente | pytest |
| CP-017 | ML | Integración | Entrenar Naive Bayes | Dataset válido | sample_dataset.csv | train_candidate_models | Resultado NB | Pendiente ejecución | Pendiente | pytest |
| CP-018 | Predicción | Integración | Cargar bundle | Modelo guardado | joblib | load_prediction_bundle | Bundle válido | Pendiente ejecución | Pendiente | pytest |
| CP-019 | Predicción | Integración | Predecir tráfico nuevo | Bundle válido | sample_traffic.csv | predict_traffic | Columna predicción | Pendiente ejecución | Pendiente | pytest |
| CP-020 | Alertas | Unitaria | Severidad normal | Servicio alerta | normal | severity_from_label | Baja | Pendiente ejecución | Pendiente | pytest |
| CP-021 | Alertas | Unitaria | Severidad amenaza | Servicio alerta | DDoS | severity_from_label | Alta | Pendiente ejecución | Pendiente | pytest |
| CP-022 | Alertas | Integración | Generar alerta por predicción | Predicciones | etiquetas/confianza | build_alerts_from_predictions | Lista alertas | Pendiente ejecución | Pendiente | pytest |
| CP-023 | SQLite | Integración | Crear esquema | schema.sql | db temporal | init_db | 60 tablas | Pendiente ejecución | Pendiente | pytest |
| CP-024 | SQLite | Integración | Cargar seed | seed_demo.sql | db temporal | init_db | Datos demo | Pendiente ejecución | Pendiente | pytest |
| CP-025 | Repository | Integración | Persistir alerta | SQLite repo | alerta | save_alert/list_alerts | Alerta recuperada | Pendiente ejecución | Pendiente | pytest |
| CP-026 | Reportes | Integración | Generar CSV | Repo con datos | usuario demo | export_summary_csv | Archivo CSV | Pendiente ejecución | Pendiente | pytest |
| CP-027 | Reportes | Integración | Generar PDF | Repo con datos | usuario demo | export_summary_pdf | Archivo PDF o None controlado | Pendiente ejecución | Pendiente | pytest |
| CP-028 | UI | Funcional | Login visible | App Streamlit | navegador | abrir app | Formulario login | Pendiente ejecución | Pendiente | captura |
| CP-029 | UI | Funcional | Dashboard visible | Sesión válida | admin | navegar dashboard | KPIs renderizados | Pendiente ejecución | Pendiente | captura |
| CP-030 | Seguridad | Revisión | No versionar secretos | Git repo | .gitignore | revisar patrones | Secrets ignorados | Pendiente ejecución | Pendiente | git status |

## 10. Riesgos de prueba

- Datasets reales pueden tener columnas distintas al dataset de prueba.
- SVM puede tardar más con datasets grandes.
- Firestore depende de credenciales y conectividad externa.
- Streamlit puede requerir validación visual manual adicional.

## 11. Evidencias requeridas

- Salida de `pytest`.
- `coverage.xml`.
- Capturas de interfaz.
- Base SQLite generada.
- Diagrama DBML en dbdiagram.io.
- Reportes CSV/PDF generados.

## 12. Relación con ISO/IEC 25010

El plan cubre adecuación funcional, mantenibilidad, fiabilidad básica, seguridad de acceso y portabilidad local/cloud.

## 13. Relación con ISO/IEC 27001

El sistema se relaciona con trazabilidad, control de acceso, monitoreo de actividad y gestión de incidentes, especialmente en controles de registro, supervisión y respuesta.

## 14. Conclusión

El plan permite validar el prototipo IDS-ML con una estrategia reproducible, defendible y alineada con criterios de calidad de software y seguridad de información.

