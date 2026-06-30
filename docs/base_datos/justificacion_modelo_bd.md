# Justificacion del modelo de base de datos IDS-ML

## Contexto

El proyecto IDS-ML requiere almacenar informacion tecnica y academica relacionada con deteccion de intrusiones, entrenamiento de modelos, eventos de red, alertas, incidentes y reportes. En una red institucional hospitalaria, la trazabilidad y la separacion de responsabilidades son esenciales para justificar resultados, auditoria y mejora continua.

## Evidencia visual del modelo

La evidencia real del motor PostgreSQL se muestra en la captura de Adminer:

![Captura real Adminer PostgreSQL](../evidencias/reales/adminer_postgresql_tablas_real.png)

Archivo de respaldo:

- `docs/evidencias/reales/postgresql_tablas_reales.txt`
- `docs/evidencias/reales/postgresql_conteo_tablas_reales.txt`

Lamina explicativa del modelo:

![Resumen visual de base de datos](../evidencias/base_datos_60_tablas.png)

El diseno documenta 62 tablas formales para la tesis. En PostgreSQL pueden visualizarse 70 tablas porque la aplicacion agrega 8 tablas operativas para guardar datos reales del prototipo: alertas, experimentos, predicciones, auditoria, errores, reportes y versiones de modelo.

## Criterios de diseno

1. **Normalizacion:** las entidades se separan para reducir duplicidad y permitir relaciones claras.
2. **Trazabilidad:** se registran usuarios, accesos, auditoria, entrenamientos, predicciones, alertas y reportes.
3. **Contexto institucional:** se modelan institucion, sedes, areas, responsables y activos.
4. **Explicabilidad academica:** se documentan datasets, preprocesamiento, metricas y seleccion por F1-score.
5. **Escalabilidad:** el esquema funciona en SQLite para pruebas y puede migrar a PostgreSQL.
6. **Seguridad:** no se almacenan secretos reales; los campos sensibles deben contener referencias seguras o hashes.
7. **Cumplimiento:** se incluyen normas de referencia y controles para relacionar el prototipo con ISO/IEC 27001, ISO/IEC 25010 y NIST CSF.

## Razon del numero de tablas

El modelo contiene 62 tablas porque el sistema IDS-ML no es solo un clasificador ML; tambien incluye gestion de datasets, arquitectura institucional, activos de red, eventos, alertas, incidentes, reportes, cumplimiento, plan de pruebas y sustento académico. Separar estos conceptos permite defender el modelo en una tesis y demostrar que el prototipo puede evolucionar hacia un sistema institucional.

## Orientacion normativa

![Orientacion ISO NIST referencial](../evidencias/orientacion_iso_nist_ids_ml.png)

La base de datos se relaciona con buenas practicas de seguridad porque registra eventos, alertas, incidentes, responsables, evidencias y reportes. Esta trazabilidad ayuda a sustentar controles como monitoreo de actividades, seguridad de redes, respuesta a incidentes, aprendizaje de incidentes y mejora continua.

## Beneficios para la tesis

- Permite generar un diagrama entidad-relacion completo.
- Facilita el diccionario de datos.
- Ayuda a explicar como se relaciona la evaluacion ML con alertas IDS.
- Permite evidenciar trazabilidad y cumplimiento con practicas de seguridad.
- Prepara el proyecto para una futura migracion a PostgreSQL o integracion con SIEM/SOC.

## Limitaciones

El proyecto Streamlit conserva una persistencia operativa ligera para el MVP. El modelo relacional formal queda preparado para evolucion, integracion o migracion progresiva mediante la capa repository.
