# Justificación del modelo de base de datos IDS-ML

## Contexto

El proyecto IDS-ML requiere almacenar información técnica y académica relacionada con detección de intrusiones, entrenamiento de modelos, eventos de red, alertas, incidentes y reportes. En una red institucional hospitalaria, la trazabilidad y la separación de responsabilidades son esenciales para justificar resultados y auditoría.

## Criterios de diseño

1. **Normalización:** las entidades se separan para reducir duplicidad y permitir relaciones claras.
2. **Trazabilidad:** se registran usuarios, accesos, auditoría, entrenamientos, predicciones, alertas y reportes.
3. **Contexto institucional:** se modelan institución, sedes, áreas, responsables y activos.
4. **Explicabilidad académica:** se documentan datasets, preprocesamiento, métricas y selección por F1-score.
5. **Escalabilidad:** el esquema funciona en SQLite para pruebas y puede migrar a PostgreSQL.
6. **Seguridad:** no se almacenan secretos reales; los campos sensibles deben contener referencias seguras o hashes.

## Razón del número de tablas

El modelo contiene 60 tablas porque el sistema IDS-ML no es solo un clasificador ML; también incluye gestión de datasets, arquitectura institucional, activos de red, eventos, alertas, incidentes, reportes y cumplimiento. Separar estos conceptos permite defender el modelo en una tesis y demostrar que el prototipo puede evolucionar hacia un sistema institucional.

## Beneficios para la tesis

- Permite generar un diagrama entidad-relación completo.
- Facilita el diccionario de datos.
- Ayuda a explicar cómo se relaciona la evaluación ML con alertas IDS.
- Permite evidenciar trazabilidad y cumplimiento con prácticas de seguridad.
- Prepara el proyecto para una futura migración a PostgreSQL o integración con SIEM/SOC.

## Limitaciones

El proyecto Streamlit actual conserva una persistencia operativa ligera para el MVP. El modelo relacional formal queda preparado para evolución, integración o migración progresiva mediante la capa repository.

