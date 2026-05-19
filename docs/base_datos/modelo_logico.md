# Modelo lógico de base de datos IDS-ML

## 1. Propósito

El modelo lógico relacional del sistema IDS-ML organiza la información requerida para un prototipo académico de detección de intrusiones en una red institucional hospitalaria. El diseño permite documentar usuarios, activos, datasets, preprocesamiento, modelos de machine learning, predicciones, alertas, incidentes, reportes, auditoría y controles de cumplimiento.

## 2. Módulos de la base

| Módulo | Tablas principales | Propósito |
|---|---|---|
| Seguridad y usuarios | `usuarios`, `roles`, `permisos`, `usuarios_roles`, `roles_permisos`, `sesiones_usuario`, `bitacora_accesos`, `auditoria_sistema` | Control de acceso, trazabilidad e historial de acciones. |
| Institución hospitalaria | `instituciones`, `sedes`, `areas_hospitalarias`, `responsables_ti`, `cargos` | Representa el contexto organizacional donde opera el IDS-ML. |
| Activos y red | `activos_red`, `tipos_activo`, `dispositivos_red`, `segmentos_red`, `direcciones_ip`, `protocolos_red`, `servicios_red` | Relaciona eventos IDS con infraestructura institucional. |
| Datasets y calidad | `datasets`, `versiones_dataset`, `columnas_dataset`, `perfilado_dataset`, `calidad_dataset`, `clases_trafico`, `particiones_dataset` | Soporta carga, versionado, perfilado y validación de datos. |
| Preprocesamiento | `preprocesamientos`, `pasos_preprocesamiento`, `transformaciones_datos`, `seleccion_caracteristicas` | Documenta limpieza, codificación, escalado, partición y selección de variables. |
| Modelos ML | `modelos_ml`, `tipos_modelo_ml`, `parametros_modelo`, `entrenamientos`, `metricas_entrenamiento`, `comparaciones_modelo`, `modelos_seleccionados` | Permite comparar modelos y justificar la selección por F1-score. |
| Predicción y tráfico | `predicciones`, `eventos_red`, `flujos_trafico` | Registra lotes de inferencia, eventos y características de tráfico. |
| Amenazas y alertas | `tipos_amenaza`, `amenazas_detectadas`, `niveles_severidad`, `alertas`, `estados_alerta`, `evidencias_alerta`, `acciones_recomendadas`, `historial_alerta` | Gestiona detecciones, severidad, alertas y evidencias. |
| Incidentes | `incidentes_seguridad`, `atencion_incidente`, `escalamiento_incidente` | Formaliza respuesta, atención y escalamiento TI. |
| Reportes | `reportes`, `tipos_reporte`, `reportes_generados`, `exportaciones_reporte` | Documenta evidencias exportadas para revisión académica o institucional. |
| Cumplimiento y mejora | `configuracion_sistema`, `umbrales_alerta`, `normas_referencia`, `controles_cumplimiento` | Relaciona el prototipo con controles ISO/NIST y configuración operativa. |

## 3. Relaciones principales

- Un `usuario` puede tener uno o varios `roles` mediante `usuarios_roles`.
- Un `rol` puede tener múltiples `permisos` mediante `roles_permisos`.
- Una `institucion` contiene `sedes`; cada sede contiene `areas_hospitalarias`.
- Los `responsables_ti` vinculan usuarios, áreas y cargos.
- Los `activos_red` pertenecen a tipos, áreas y segmentos de red.
- Los `datasets` tienen `versiones_dataset`, columnas, perfilado, calidad y particiones.
- Un `preprocesamiento` pertenece a una versión de dataset y contiene pasos, transformaciones y selección de características.
- Los `modelos_ml` se entrenan mediante `entrenamientos`, que generan `metricas_entrenamiento`.
- Una `comparacion_modelo` permite registrar el criterio de selección y el modelo final en `modelos_seleccionados`.
- Las `predicciones` generan `eventos_red`; los eventos pueden generar `amenazas_detectadas`.
- Una amenaza detectada puede producir una `alerta`, evidencias, historial y eventualmente un `incidente_seguridad`.
- Los reportes generados registran trazabilidad de exportación y usuario responsable.
- Los controles de cumplimiento vinculan el sistema con normas de referencia como ISO/IEC 27001 y NIST CSF.

## 4. Justificación de 60 tablas

El número de tablas no busca inflar artificialmente el modelo, sino separar responsabilidades para una tesis revisable: seguridad, activos, datos, ML, predicción, alertas, incidentes, auditoría, reportes y cumplimiento. Esta separación evita una base monolítica, reduce redundancia, permite normalización y facilita explicar cada módulo durante sustentación.

## 5. Relación con el sistema IDS-ML

El sistema Streamlit actual usa un repositorio SQLite/Firestore operativo para el MVP. Este modelo relacional formal complementa ese MVP como diseño académico documentable y adaptable a PostgreSQL. A futuro, los repositorios pueden mapear las operaciones actuales hacia estas tablas sin cambiar la lógica de interfaz ni machine learning.

