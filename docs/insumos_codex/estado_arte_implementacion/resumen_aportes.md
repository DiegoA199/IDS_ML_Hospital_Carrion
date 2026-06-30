# Resumen de aportes para la implementación

## Arquitectura y diseño IDS

Las referencias A03, A13 y A24 orientan una arquitectura por fases, componentes multicapa y frameworks de detección desplegables. Su aporte debe traducirse en contratos claros entre carga, preparación, entrenamiento, inferencia y alertas.

## Implementación de prototipos IDS

A04, A13 y A16 respaldan decisiones sobre ensambles, separación por capas, selección de modelos y criterios de implementación del prototipo.

## Procesamiento de datos

A02 y A06 sirven para discutir volumen de datos, series temporales y selección de características, considerando trazabilidad y crecimiento del tráfico.

## Evaluación y métricas

A04, A13, A15 y A19 sustentan la comparación de modelos y la evaluación mediante métricas complementarias como Accuracy, Precision, Recall y F1-score.

## Interpretabilidad y trazabilidad

A18 y A19 orientan la explicación de predicciones y alertas. Para el IDS-ML, esto implica conservar modelo, confianza, contexto de ejecución y evidencia suficiente para la revisión del personal TI.

## Despliegue y eficiencia

A02, A12, A15 y A24 aportan criterios de escalabilidad, edge, ejecución eficiente y cloud. Estas referencias permiten discutir límites del prototipo y alternativas futuras para infraestructura institucional.

## Relación con el sistema IDS-ML

En conjunto, los artículos justifican una arquitectura modular, el pipeline reproducible de datos, la comparación de algoritmos, la trazabilidad y la evolución controlada del prototipo. A26 aporta el vínculo más directo con redes médicas e IoMT. La matriz asociada debe actualizarse cuando una referencia se descarte, reemplace o se vincule con una decisión técnica concreta.
