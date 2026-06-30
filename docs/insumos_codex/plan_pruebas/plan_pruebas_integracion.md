# Pruebas de integración

## Objetivo

Comprobar que los componentes del IDS-ML intercambian datos correctamente.

## Alcance recomendado

- Carga, preprocesamiento, entrenamiento y predicción en un flujo completo.
- Persistencia y consulta mediante el repository pattern.
- Generación de alertas a partir de predicciones.
- Exportación y registro de reportes.
- Inicialización del esquema relacional.

## Criterio de aceptación

Los flujos deben terminar sin pérdida de trazabilidad ni inconsistencias entre capas. Ejecutar con `pytest tests/integration` usando datos sintéticos o fixtures autorizados.
