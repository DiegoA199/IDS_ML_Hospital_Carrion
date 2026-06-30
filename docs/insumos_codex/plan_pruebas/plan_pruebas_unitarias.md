# Pruebas unitarias

## Objetivo

Verificar reglas y transformaciones aisladas sin depender de Streamlit ni de servicios externos.

## Alcance recomendado

- Validadores de archivos, campos y configuraciones.
- Limpieza, codificación y preparación de datos.
- Cálculo de métricas y selección de modelos.
- Servicios de dominio y formateadores.
- Operaciones básicas del repositorio SQLite temporal.

## Criterio de aceptación

Cada función debe producir resultados deterministas para entradas válidas y errores controlados para entradas inválidas. Ejecutar con `pytest tests/unit` y conservar el reporte como evidencia cuando corresponda.
