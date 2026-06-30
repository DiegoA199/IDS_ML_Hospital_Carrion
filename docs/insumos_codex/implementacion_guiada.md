# Implementación guiada por mockups y artículos

## Objetivo

Registrar cómo los insumos visuales y académicos fueron traducidos a decisiones verificables del producto, sin exponer documentación interna como módulos de Streamlit.

## Decisiones visuales aplicadas

| Insumo | Aplicación en el producto |
|---|---|
| MK-01 Login | Acceso centrado, identidad hospitalaria, tarjeta blanca y acción primaria azul. |
| MK-02 Dashboard | Lienzo clínico claro, métricas jerarquizadas, gráficos sobrios y rojo reservado para amenazas. |
| MK-03 Carga de datos | Nombre funcional, carga destacada, métricas de calidad y vista previa tabular. |
| MK-04 Preparación | Flujo visible de limpieza, codificación, normalización y partición. |
| MK-05 Entrenamiento | Configuración separada de resultados y acción principal inequívoca. |
| MK-06 Comparación | Módulo funcional con modelo recomendado, métricas, gráfico, tabla y exportación CSV. |
| MK-07 Predicción | Entrada y resultado diferenciados, confianza visible y persistencia controlada. |
| MK-08 Alertas | Severidad semántica, filtros, trazabilidad y cambio de estado según rol. |
| MK-09 Reportes | Acciones de exportación e historial persistido. |
| MK-10 Configuración | Agrupación de controles administrativos sin mostrar secretos. |

## Decisiones técnicas sustentadas

| Artículo | Decisión relacionada |
|---|---|
| A03 | Mantener el flujo por etapas: carga, preparación, entrenamiento, comparación, predicción y respuesta. |
| A06 | Conservar preparación y selección de características antes del entrenamiento, evitando fuga de datos. |
| A13 | Separar entrenamiento, comparación y alertas como responsabilidades funcionales distintas. |
| A16 | Comparar varios algoritmos mediante métricas homogéneas y seleccionar por F1-score. |
| A18 y A19 | Mostrar modelo, confianza, severidad, recomendación y trazabilidad para apoyar explicación humana. |
| A26 | Mantener lenguaje, controles y contexto orientados a una red institucional hospitalaria. |

## Límites

- Los mockups no aportan datos reales ni autorizan acciones defensivas automáticas inexistentes.
- Los valores mostrados por la aplicación provienen de sesión o persistencia, no de ejemplos dibujados.
- Las recomendaciones científicas se adoptan solo cuando son compatibles con el alcance y las pruebas actuales.
- Plan de pruebas, estado del arte, mockups e insumos Codex permanecen fuera del menú productivo.
