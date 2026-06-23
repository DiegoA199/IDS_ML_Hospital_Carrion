# Procesos institucionales hospitalarios para el prototipo IDS-ML

## 1. Objetivo

Documentar el proceso institucional que seguiria un hospital para operar un prototipo IDS-ML: monitoreo de trafico, deteccion de amenazas, gestion de alertas, atencion de incidentes, reportes y mejora continua.

## 2. Diagrama tipo Bizagi/BPMN

No se encontro en el repositorio ni en las carpetas locales un archivo real de Bizagi (`.bpm`, `.bpmn`) ni una imagen externa del proceso hospitalario ya elaborada. Por ese motivo, la siguiente imagen debe tratarse como referencia conceptual, no como evidencia real externa.

![Proceso hospitalario IDS-ML](../evidencias/proceso_hospital_ids_ml_bpmn.png)

Para presentar evidencia real, se debe exportar desde Bizagi Modeler alguno de estos archivos:

- `.bpm`
- `.bpmn`
- `.png` o `.jpg`
- `.pdf`

## 3. Actores del proceso

| Actor | Responsabilidad |
|---|---|
| Red hospitalaria | Genera trafico institucional y eventos que pueden analizarse de forma controlada. |
| Area TI / SOC | Supervisa activos, revisa alertas, atiende incidentes y documenta acciones. |
| Sistema IDS-ML | Carga datos, preprocesa, entrena modelos, compara metricas, selecciona el mejor modelo y genera alertas. |
| Responsables / Direccion | Revisan reportes, priorizan riesgos y aprueban acciones de mejora. |

## 4. Flujo principal

1. Identificar activos y segmentos criticos de la red hospitalaria.
2. Capturar trafico autorizado o cargar datasets de investigacion.
3. Validar calidad, nulos, duplicados y estructura del dataset.
4. Preprocesar datos: limpieza, codificacion, escalamiento y seleccion de caracteristicas.
5. Entrenar modelos de machine learning.
6. Comparar Accuracy, Precision, Recall y F1-score.
7. Seleccionar el mejor modelo por F1-score.
8. Analizar trafico nuevo.
9. Generar alertas segun prediccion y severidad.
10. Atender o escalar incidentes.
11. Generar reportes y registrar trazabilidad.
12. Aplicar mejora continua.

## 5. Relacion con ISO/IEC 27001:2022

| Control | Relacion con el prototipo IDS-ML |
|---|---|
| A.5.7 Inteligencia de amenazas | El sistema clasifica amenazas y documenta patrones observados. |
| A.5.24 Planificacion de respuesta | El flujo define atencion, escalamiento y responsables. |
| A.5.25 Evaluacion de eventos | Las alertas se analizan con severidad, probabilidad y evidencia. |
| A.5.26 Respuesta a incidentes | El modulo de incidentes permite registrar acciones de atencion. |
| A.5.27 Aprendizaje de incidentes | Los reportes permiten mejora continua y retroalimentacion. |
| A.8.15 Registro de eventos | La auditoria registra acciones del sistema y del usuario. |
| A.8.16 Monitoreo de actividades | El dashboard y alertas apoyan el monitoreo institucional. |
| A.8.20 Seguridad de redes | El modelo relaciona eventos con segmentos, IP, servicios y protocolos. |
| A.8.22 Segmentacion de redes | La base documenta segmentos y activos criticos. |
| A.8.28 Codificacion segura | SonarCloud y pruebas automatizadas respaldan calidad del codigo. |

## 6. Relacion con ISO/IEC 25010

| Caracteristica | Evidencia en el proyecto |
|---|---|
| Mantenibilidad | Arquitectura modular, capas separadas y repository pattern. |
| Confiabilidad | Pruebas automatizadas y flujo de CI. |
| Seguridad | Roles, permisos, auditoria y manejo de secretos fuera del repo. |
| Usabilidad | Interfaz Streamlit con dashboard, alertas, filtros y reportes. |
| Portabilidad | Docker, Render y compatibilidad SQLite/PostgreSQL. |
| Eficiencia | Comparacion de modelos y seleccion por F1-score. |

## 7. Relacion con NIST CSF

| Funcion NIST CSF | Evidencia |
|---|---|
| Identify | Inventario de activos, segmentos, datasets y responsables. |
| Protect | Roles, permisos, configuracion segura y controles. |
| Detect | Analisis IDS-ML, predicciones y alertas. |
| Respond | Gestion de alertas, atencion y escalamiento de incidentes. |
| Recover | Reportes, trazabilidad y mejora continua. |

## 8. Imagen de orientacion normativa

![Orientacion ISO NIST](../evidencias/orientacion_iso_nist_ids_ml.png)
