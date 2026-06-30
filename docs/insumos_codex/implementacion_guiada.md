# Implementación guiada por mockups y artículos

## Objetivo

Registrar cómo los insumos visuales y académicos fueron traducidos a decisiones verificables del producto, sin exponer documentación interna como módulos de Streamlit.

## Decisiones visuales aplicadas

La segunda navegación interna del prototipo anterior fue retirada. La interfaz usa ahora la composición común de Stitch: barra lateral de nueve módulos, cabecera superior compacta, tarjetas blancas sobre lienzo clínico y jerarquía azul/rojo para operación y riesgo. Un selector global sincronizado conserva el acceso a todos los módulos cuando Streamlit colapsa el lateral o la aplicación se usa desde un móvil.

| Insumo | Aplicación en el producto |
|---|---|
| MK-01 Login | Acceso centrado, identidad hospitalaria, tarjeta blanca y acción primaria azul. |
| MK-02 Dashboard | Cinco indicadores operativos, barra superior, distribución normal/sospechosa, amenazas por tipo y eventos recientes. |
| MK-03 Carga de datos | Nombre funcional, carga destacada, métricas de calidad y vista previa tabular. |
| MK-04 Preparación | Flujo visible de limpieza, codificación, normalización y partición. |
| MK-05 Entrenamiento | Configuración separada de resultados y acción principal inequívoca. |
| MK-06 Comparación | Gráfico comparativo junto a panel oscuro de modelo recomendado, matriz detallada y exportación CSV. |
| MK-07 Predicción | Entrada y resultado diferenciados, confianza visible y persistencia controlada. |
| MK-08 Alertas | Severidad semántica, filtros, trazabilidad y cambio de estado según rol. |
| MK-09 Reportes | Filtros automáticos y funcionales por fecha, contenido y estado; secciones de modelos, alertas, historial, actividad y exportación. |
| MK-10 Configuración | Preferencias reales de sesión, estado de persistencia y controles administrativos sin mostrar secretos. |

## Decisiones técnicas sustentadas

| Artículo | Decisión relacionada |
|---|---|
| A03 | Mantener el flujo por etapas: carga, preparación, entrenamiento, comparación, predicción y respuesta. |
| A06 | Conservar preparación y selección de características antes del entrenamiento, evitando fuga de datos. |
| A13 | Separar entrenamiento, comparación y alertas como responsabilidades funcionales distintas. |
| A16 | Comparar varios algoritmos mediante métricas homogéneas y seleccionar por F1-score. |
| A18 y A19 | Mostrar modelo, confianza, severidad, recomendación y trazabilidad para apoyar explicación humana. |
| A26 | Mantener lenguaje, controles y contexto orientados a una red institucional hospitalaria. |

La revisión de usabilidad eliminó controles puramente decorativos (búsqueda, ayuda, notificaciones, recordar sesión y recuperación de contraseña sin servicio asociado). Todo elemento que conserva apariencia interactiva ejecuta ahora una acción o comunica explícitamente que es un estado de solo lectura.

## Límites

- Los mockups no aportan datos reales ni autorizan acciones defensivas automáticas inexistentes.
- Cuando no existen inferencias persistidas, el dashboard presenta valores sintéticos con la etiqueta visible `Vista demostrativa`; se reemplazan automáticamente al existir datos reales.
- Carga de datos incluye un dataset sintético identificable para recorrer preparación, entrenamiento, comparación y predicción sin confundirlo con evidencia hospitalaria real.
- Las recomendaciones científicas se adoptan solo cuando son compatibles con el alcance y las pruebas actuales.
- Plan de pruebas, estado del arte, mockups e insumos Codex permanecen fuera del menú productivo.
