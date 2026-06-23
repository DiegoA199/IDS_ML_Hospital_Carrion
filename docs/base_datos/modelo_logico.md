# Modelo logico de base de datos IDS-ML

## 1. Proposito

El modelo logico relacional del sistema IDS-ML organiza la informacion requerida para un prototipo academico de deteccion de intrusiones en una red institucional hospitalaria. El diseno permite documentar usuarios, activos, datasets, preprocesamiento, modelos de machine learning, predicciones, alertas, incidentes, reportes, auditoria y controles de cumplimiento.

## 2. Evidencia visual

El modelo formal de tesis contiene 60 tablas academicas. Al ejecutarse en PostgreSQL tambien se visualizan 8 tablas operativas que usa la aplicacion para guardar ejecuciones reales, por lo que el motor puede mostrar 68 tablas.

La evidencia real capturada desde Adminer/PostgreSQL es:

![Captura real Adminer PostgreSQL](../evidencias/reales/adminer_postgresql_tablas_real.png)

Archivos tecnicos reales:

- `docs/evidencias/reales/postgresql_tablas_reales.txt`
- `docs/evidencias/reales/postgresql_conteo_tablas_reales.txt`

Las siguientes laminas son referenciales para explicar el modelo:

![Resumen visual de base de datos](../evidencias/base_datos_60_tablas.png)

![Listado visual de 60 tablas](../evidencias/base_datos_listado_60_tablas.png)

## 3. Modulos de la base

| Modulo | Tablas principales | Proposito |
|---|---|---|
| Seguridad y usuarios | `usuarios`, `roles`, `permisos`, `usuarios_roles`, `roles_permisos`, `sesiones_usuario`, `bitacora_accesos`, `auditoria_sistema` | Control de acceso, trazabilidad e historial de acciones. |
| Institucion hospitalaria | `instituciones`, `sedes`, `areas_hospitalarias`, `responsables_ti`, `cargos` | Representa el contexto organizacional donde opera el IDS-ML. |
| Activos y red | `activos_red`, `tipos_activo`, `dispositivos_red`, `segmentos_red`, `direcciones_ip`, `protocolos_red`, `servicios_red` | Relaciona eventos IDS con infraestructura institucional. |
| Datasets y calidad | `datasets`, `versiones_dataset`, `columnas_dataset`, `perfilado_dataset`, `calidad_dataset`, `clases_trafico`, `particiones_dataset` | Soporta carga, versionado, perfilado y validacion de datos. |
| Preprocesamiento | `preprocesamientos`, `pasos_preprocesamiento`, `transformaciones_datos`, `seleccion_caracteristicas` | Documenta limpieza, codificacion, escalado, particion y seleccion de variables. |
| Modelos ML | `modelos_ml`, `tipos_modelo_ml`, `parametros_modelo`, `entrenamientos`, `metricas_entrenamiento`, `comparaciones_modelo`, `modelos_seleccionados` | Permite comparar modelos y justificar la seleccion por F1-score. |
| Prediccion y trafico | `predicciones`, `eventos_red`, `flujos_trafico` | Registra lotes de inferencia, eventos y caracteristicas de trafico. |
| Amenazas y alertas | `tipos_amenaza`, `amenazas_detectadas`, `niveles_severidad`, `alertas`, `estados_alerta`, `evidencias_alerta`, `acciones_recomendadas`, `historial_alerta` | Gestiona detecciones, severidad, alertas y evidencias. |
| Incidentes | `incidentes_seguridad`, `atencion_incidente`, `escalamiento_incidente` | Formaliza respuesta, atencion y escalamiento TI. |
| Reportes | `reportes`, `tipos_reporte`, `reportes_generados`, `exportaciones_reporte` | Documenta evidencias exportadas para revision academica o institucional. |
| Cumplimiento y mejora | `configuracion_sistema`, `umbrales_alerta`, `normas_referencia`, `controles_cumplimiento` | Relaciona el prototipo con controles ISO/NIST y configuracion operativa. |

## 4. Relaciones principales

- Un `usuario` puede tener uno o varios `roles` mediante `usuarios_roles`.
- Un `rol` puede tener multiples `permisos` mediante `roles_permisos`.
- Una `institucion` contiene `sedes`; cada sede contiene `areas_hospitalarias`.
- Los `responsables_ti` vinculan usuarios, areas y cargos.
- Los `activos_red` pertenecen a tipos, areas y segmentos de red.
- Los `datasets` tienen `versiones_dataset`, columnas, perfilado, calidad y particiones.
- Un `preprocesamiento` pertenece a una version de dataset y contiene pasos, transformaciones y seleccion de caracteristicas.
- Los `modelos_ml` se entrenan mediante `entrenamientos`, que generan `metricas_entrenamiento`.
- Una `comparacion_modelo` permite registrar el criterio de seleccion y el modelo final en `modelos_seleccionados`.
- Las `predicciones` generan `eventos_red`; los eventos pueden generar `amenazas_detectadas`.
- Una amenaza detectada puede producir una `alerta`, evidencias, historial y eventualmente un `incidente_seguridad`.
- Los reportes generados registran trazabilidad de exportacion y usuario responsable.
- Los controles de cumplimiento vinculan el sistema con normas de referencia como ISO/IEC 27001, ISO/IEC 25010 y NIST CSF.

## 5. Justificacion de 60 tablas

El numero de tablas no busca inflar artificialmente el modelo, sino separar responsabilidades para una tesis revisable: seguridad, activos, datos, ML, prediccion, alertas, incidentes, auditoria, reportes y cumplimiento. Esta separacion evita una base monolitica, reduce redundancia, permite normalizacion y facilita explicar cada modulo durante sustentacion.

## 6. Relacion con el sistema IDS-ML

El sistema Streamlit usa repositorios desacoplados para SQLite, PostgreSQL y Firestore. El modelo relacional formal complementa el MVP como diseno academico documentable y adaptable a PostgreSQL. A futuro, los repositorios pueden mapear progresivamente todas las operaciones hacia estas tablas sin cambiar la logica de interfaz ni machine learning.
