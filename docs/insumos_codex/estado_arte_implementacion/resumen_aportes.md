# Resumen de aportes para la implementación

## Arquitectura y diseño IDS

Las referencias A03, A06 y A30 orientan la separación por fases, la taxonomía de técnicas de detección y las alternativas de procesamiento distribuido. Su aporte debe traducirse en componentes desacoplados y contratos claros entre carga, preparación, entrenamiento, inferencia y alertas.

## Implementación de prototipos IDS

A16, A39 y A40 respaldan el desarrollo de un prototipo reproducible con Python, scikit-learn y estructuras de datos adecuadas. También ayudan a justificar el uso de componentes verificables y persistencia independiente de la interfaz.

## Procesamiento de datos

A02, A18 y A40 sirven para organizar la carga, validación, limpieza y transformación de datos, considerando trazabilidad y crecimiento del volumen de tráfico.

## Evaluación y métricas

A21, A27, A29 y A35 sustentan la comparación de modelos, la selección de características, el uso de datasets benchmark y la evaluación mediante métricas complementarias como Accuracy, Precision, Recall y F1-score.

## Interpretabilidad y trazabilidad

A33 orienta la explicación de predicciones y alertas. Para el IDS-ML, esto implica conservar modelo, confianza, contexto de ejecución y evidencia suficiente para la revisión del personal TI.

## Despliegue y eficiencia

A02, A17 y A30 aportan criterios de escalabilidad, ejecución eficiente y distribución. Estas referencias permiten discutir límites del prototipo y alternativas futuras para infraestructura institucional o nube.

## Relación con el sistema IDS-ML

En conjunto, los artículos justifican una arquitectura modular, el pipeline reproducible de datos, la comparación de algoritmos, la trazabilidad operacional y la evolución controlada del prototipo. La matriz asociada debe actualizarse cuando una referencia se descarte, reemplace o se vincule con una decisión técnica concreta.
