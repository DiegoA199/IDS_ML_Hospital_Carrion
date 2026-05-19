# Diccionario de datos IDS-ML

Diccionario generado a partir de `database/schema.sql`. Las descripciones son acad?micas y pueden ampliarse con reglas institucionales reales.

| Tabla | Campo | Tipo de dato | Clave | Descripci?n | Restricciones |
|---|---|---|---|---|---|
| usuarios | id | INTEGER | PK | Campo id de la tabla usuarios. | PRIMARY KEY AUTOINCREMENT |
| usuarios | username | TEXT | - | Campo username de la tabla usuarios. | NOT NULL UNIQUE |
| usuarios | email | TEXT | - | Campo email de la tabla usuarios. | UNIQUE |
| usuarios | nombre_completo | TEXT | - | Campo nombre_completo de la tabla usuarios. | NOT NULL |
| usuarios | password_hash | TEXT | - | Campo password_hash de la tabla usuarios. | - |
| usuarios | estado | TEXT | - | Estado operativo del registro. | NOT NULL DEFAULT 'activo' |
| usuarios | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| usuarios | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| roles | id | INTEGER | PK | Campo id de la tabla roles. | PRIMARY KEY AUTOINCREMENT |
| roles | nombre | TEXT | - | Campo nombre de la tabla roles. | NOT NULL UNIQUE |
| roles | descripcion | TEXT | - | Campo descripcion de la tabla roles. | - |
| roles | estado | TEXT | - | Estado operativo del registro. | NOT NULL DEFAULT 'activo' |
| roles | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| roles | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| permisos | id | INTEGER | PK | Campo id de la tabla permisos. | PRIMARY KEY AUTOINCREMENT |
| permisos | codigo | TEXT | - | Campo codigo de la tabla permisos. | NOT NULL UNIQUE |
| permisos | nombre | TEXT | - | Campo nombre de la tabla permisos. | NOT NULL |
| permisos | descripcion | TEXT | - | Campo descripcion de la tabla permisos. | - |
| permisos | modulo | TEXT | - | Campo modulo de la tabla permisos. | NOT NULL |
| permisos | estado | TEXT | - | Estado operativo del registro. | NOT NULL DEFAULT 'activo' |
| permisos | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| permisos | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| usuarios_roles | id | INTEGER | PK | Campo id de la tabla usuarios_roles. | PRIMARY KEY AUTOINCREMENT |
| usuarios_roles | usuario_id | INTEGER | FK -> usuarios.id | Identificador relacional asociado. | NOT NULL |
| usuarios_roles | rol_id | INTEGER | FK -> roles.id | Identificador relacional asociado. | NOT NULL |
| usuarios_roles | estado | TEXT | - | Estado operativo del registro. | NOT NULL DEFAULT 'activo' |
| usuarios_roles | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| usuarios_roles | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| roles_permisos | id | INTEGER | PK | Campo id de la tabla roles_permisos. | PRIMARY KEY AUTOINCREMENT |
| roles_permisos | rol_id | INTEGER | FK -> roles.id | Identificador relacional asociado. | NOT NULL |
| roles_permisos | permiso_id | INTEGER | FK -> permisos.id | Identificador relacional asociado. | NOT NULL |
| roles_permisos | estado | TEXT | - | Estado operativo del registro. | NOT NULL DEFAULT 'activo' |
| roles_permisos | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| roles_permisos | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| sesiones_usuario | id | INTEGER | PK | Campo id de la tabla sesiones_usuario. | PRIMARY KEY AUTOINCREMENT |
| sesiones_usuario | usuario_id | INTEGER | FK -> usuarios.id | Identificador relacional asociado. | NOT NULL |
| sesiones_usuario | token_referencia | TEXT | - | Campo token_referencia de la tabla sesiones_usuario. | - |
| sesiones_usuario | ip_origen | TEXT | - | Campo ip_origen de la tabla sesiones_usuario. | - |
| sesiones_usuario | user_agent | TEXT | - | Campo user_agent de la tabla sesiones_usuario. | - |
| sesiones_usuario | inicio_sesion | TEXT | - | Campo inicio_sesion de la tabla sesiones_usuario. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| sesiones_usuario | fin_sesion | TEXT | - | Campo fin_sesion de la tabla sesiones_usuario. | - |
| sesiones_usuario | estado | TEXT | - | Estado operativo del registro. | NOT NULL DEFAULT 'activa' |
| sesiones_usuario | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| sesiones_usuario | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| bitacora_accesos | id | INTEGER | PK | Campo id de la tabla bitacora_accesos. | PRIMARY KEY AUTOINCREMENT |
| bitacora_accesos | usuario_id | INTEGER | FK -> usuarios.id | Identificador relacional asociado. | - |
| bitacora_accesos | accion | TEXT | - | Campo accion de la tabla bitacora_accesos. | NOT NULL |
| bitacora_accesos | resultado | TEXT | - | Campo resultado de la tabla bitacora_accesos. | NOT NULL |
| bitacora_accesos | ip_origen | TEXT | - | Campo ip_origen de la tabla bitacora_accesos. | - |
| bitacora_accesos | detalle | TEXT | - | Campo detalle de la tabla bitacora_accesos. | - |
| bitacora_accesos | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| bitacora_accesos | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| auditoria_sistema | id | INTEGER | PK | Campo id de la tabla auditoria_sistema. | PRIMARY KEY AUTOINCREMENT |
| auditoria_sistema | usuario_id | INTEGER | FK -> usuarios.id | Identificador relacional asociado. | - |
| auditoria_sistema | modulo | TEXT | - | Campo modulo de la tabla auditoria_sistema. | NOT NULL |
| auditoria_sistema | accion | TEXT | - | Campo accion de la tabla auditoria_sistema. | NOT NULL |
| auditoria_sistema | entidad | TEXT | - | Campo entidad de la tabla auditoria_sistema. | - |
| auditoria_sistema | entidad_id | TEXT | - | Identificador relacional asociado. | - |
| auditoria_sistema | resultado | TEXT | - | Campo resultado de la tabla auditoria_sistema. | NOT NULL |
| auditoria_sistema | detalle | TEXT | - | Campo detalle de la tabla auditoria_sistema. | - |
| auditoria_sistema | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| auditoria_sistema | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| instituciones | id | INTEGER | PK | Campo id de la tabla instituciones. | PRIMARY KEY AUTOINCREMENT |
| instituciones | nombre | TEXT | - | Campo nombre de la tabla instituciones. | NOT NULL |
| instituciones | ruc | TEXT | - | Campo ruc de la tabla instituciones. | UNIQUE |
| instituciones | tipo | TEXT | - | Campo tipo de la tabla instituciones. | NOT NULL DEFAULT 'hospital' |
| instituciones | direccion | TEXT | - | Campo direccion de la tabla instituciones. | - |
| instituciones | estado | TEXT | - | Estado operativo del registro. | NOT NULL DEFAULT 'activo' |
| instituciones | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| instituciones | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| sedes | id | INTEGER | PK | Campo id de la tabla sedes. | PRIMARY KEY AUTOINCREMENT |
| sedes | institucion_id | INTEGER | FK -> instituciones.id | Identificador relacional asociado. | NOT NULL |
| sedes | nombre | TEXT | - | Campo nombre de la tabla sedes. | NOT NULL |
| sedes | ciudad | TEXT | - | Campo ciudad de la tabla sedes. | - |
| sedes | direccion | TEXT | - | Campo direccion de la tabla sedes. | - |
| sedes | estado | TEXT | - | Estado operativo del registro. | NOT NULL DEFAULT 'activo' |
| sedes | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| sedes | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| areas_hospitalarias | id | INTEGER | PK | Campo id de la tabla areas_hospitalarias. | PRIMARY KEY AUTOINCREMENT |
| areas_hospitalarias | sede_id | INTEGER | FK -> sedes.id | Identificador relacional asociado. | NOT NULL |
| areas_hospitalarias | nombre | TEXT | - | Campo nombre de la tabla areas_hospitalarias. | NOT NULL |
| areas_hospitalarias | codigo | TEXT | - | Campo codigo de la tabla areas_hospitalarias. | - |
| areas_hospitalarias | descripcion | TEXT | - | Campo descripcion de la tabla areas_hospitalarias. | - |
| areas_hospitalarias | estado | TEXT | - | Estado operativo del registro. | NOT NULL DEFAULT 'activo' |
| areas_hospitalarias | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| areas_hospitalarias | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| cargos | id | INTEGER | PK | Campo id de la tabla cargos. | PRIMARY KEY AUTOINCREMENT |
| cargos | nombre | TEXT | - | Campo nombre de la tabla cargos. | NOT NULL UNIQUE |
| cargos | descripcion | TEXT | - | Campo descripcion de la tabla cargos. | - |
| cargos | estado | TEXT | - | Estado operativo del registro. | NOT NULL DEFAULT 'activo' |
| cargos | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| cargos | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| responsables_ti | id | INTEGER | PK | Campo id de la tabla responsables_ti. | PRIMARY KEY AUTOINCREMENT |
| responsables_ti | usuario_id | INTEGER | FK -> usuarios.id | Identificador relacional asociado. | - |
| responsables_ti | area_id | INTEGER | FK -> areas_hospitalarias.id | Identificador relacional asociado. | - |
| responsables_ti | cargo_id | INTEGER | FK -> cargos.id | Identificador relacional asociado. | - |
| responsables_ti | telefono | TEXT | - | Campo telefono de la tabla responsables_ti. | - |
| responsables_ti | correo_institucional | TEXT | - | Campo correo_institucional de la tabla responsables_ti. | - |
| responsables_ti | estado | TEXT | - | Estado operativo del registro. | NOT NULL DEFAULT 'activo' |
| responsables_ti | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| responsables_ti | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| tipos_activo | id | INTEGER | PK | Campo id de la tabla tipos_activo. | PRIMARY KEY AUTOINCREMENT |
| tipos_activo | nombre | TEXT | - | Campo nombre de la tabla tipos_activo. | NOT NULL UNIQUE |
| tipos_activo | descripcion | TEXT | - | Campo descripcion de la tabla tipos_activo. | - |
| tipos_activo | estado | TEXT | - | Estado operativo del registro. | NOT NULL DEFAULT 'activo' |
| tipos_activo | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| tipos_activo | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| segmentos_red | id | INTEGER | PK | Campo id de la tabla segmentos_red. | PRIMARY KEY AUTOINCREMENT |
| segmentos_red | sede_id | INTEGER | FK -> sedes.id | Identificador relacional asociado. | - |
| segmentos_red | nombre | TEXT | - | Campo nombre de la tabla segmentos_red. | NOT NULL |
| segmentos_red | cidr | TEXT | - | Campo cidr de la tabla segmentos_red. | NOT NULL |
| segmentos_red | criticidad | TEXT | - | Campo criticidad de la tabla segmentos_red. | NOT NULL DEFAULT 'media' |
| segmentos_red | estado | TEXT | - | Estado operativo del registro. | NOT NULL DEFAULT 'activo' |
| segmentos_red | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| segmentos_red | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| activos_red | id | INTEGER | PK | Campo id de la tabla activos_red. | PRIMARY KEY AUTOINCREMENT |
| activos_red | tipo_activo_id | INTEGER | FK -> tipos_activo.id | Identificador relacional asociado. | - |
| activos_red | area_id | INTEGER | FK -> areas_hospitalarias.id | Identificador relacional asociado. | - |
| activos_red | segmento_red_id | INTEGER | FK -> segmentos_red.id | Identificador relacional asociado. | - |
| activos_red | nombre | TEXT | - | Campo nombre de la tabla activos_red. | NOT NULL |
| activos_red | codigo_inventario | TEXT | - | Campo codigo_inventario de la tabla activos_red. | UNIQUE |
| activos_red | criticidad | TEXT | - | Campo criticidad de la tabla activos_red. | NOT NULL DEFAULT 'media' |
| activos_red | estado | TEXT | - | Estado operativo del registro. | NOT NULL DEFAULT 'activo' |
| activos_red | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| activos_red | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| dispositivos_red | id | INTEGER | PK | Campo id de la tabla dispositivos_red. | PRIMARY KEY AUTOINCREMENT |
| dispositivos_red | activo_red_id | INTEGER | FK -> activos_red.id | Identificador relacional asociado. | NOT NULL |
| dispositivos_red | fabricante | TEXT | - | Campo fabricante de la tabla dispositivos_red. | - |
| dispositivos_red | modelo | TEXT | - | Campo modelo de la tabla dispositivos_red. | - |
| dispositivos_red | sistema_operativo | TEXT | - | Campo sistema_operativo de la tabla dispositivos_red. | - |
| dispositivos_red | mac_address | TEXT | - | Campo mac_address de la tabla dispositivos_red. | - |
| dispositivos_red | estado | TEXT | - | Estado operativo del registro. | NOT NULL DEFAULT 'activo' |
| dispositivos_red | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| dispositivos_red | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| direcciones_ip | id | INTEGER | PK | Campo id de la tabla direcciones_ip. | PRIMARY KEY AUTOINCREMENT |
| direcciones_ip | segmento_red_id | INTEGER | FK -> segmentos_red.id | Identificador relacional asociado. | - |
| direcciones_ip | activo_red_id | INTEGER | FK -> activos_red.id | Identificador relacional asociado. | - |
| direcciones_ip | direccion_ip | TEXT | - | Campo direccion_ip de la tabla direcciones_ip. | NOT NULL UNIQUE |
| direcciones_ip | version_ip | TEXT | - | Campo version_ip de la tabla direcciones_ip. | NOT NULL DEFAULT 'IPv4' |
| direcciones_ip | es_estatica | INTEGER | - | Campo es_estatica de la tabla direcciones_ip. | NOT NULL DEFAULT 1 |
| direcciones_ip | estado | TEXT | - | Estado operativo del registro. | NOT NULL DEFAULT 'activo' |
| direcciones_ip | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| direcciones_ip | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| protocolos_red | id | INTEGER | PK | Campo id de la tabla protocolos_red. | PRIMARY KEY AUTOINCREMENT |
| protocolos_red | nombre | TEXT | - | Campo nombre de la tabla protocolos_red. | NOT NULL UNIQUE |
| protocolos_red | numero_protocolo | INTEGER | - | Campo numero_protocolo de la tabla protocolos_red. | - |
| protocolos_red | descripcion | TEXT | - | Campo descripcion de la tabla protocolos_red. | - |
| protocolos_red | estado | TEXT | - | Estado operativo del registro. | NOT NULL DEFAULT 'activo' |
| protocolos_red | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| protocolos_red | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| servicios_red | id | INTEGER | PK | Campo id de la tabla servicios_red. | PRIMARY KEY AUTOINCREMENT |
| servicios_red | protocolo_red_id | INTEGER | FK -> protocolos_red.id | Identificador relacional asociado. | - |
| servicios_red | nombre | TEXT | - | Campo nombre de la tabla servicios_red. | NOT NULL |
| servicios_red | puerto | INTEGER | - | Campo puerto de la tabla servicios_red. | - |
| servicios_red | descripcion | TEXT | - | Campo descripcion de la tabla servicios_red. | - |
| servicios_red | estado | TEXT | - | Estado operativo del registro. | NOT NULL DEFAULT 'activo' |
| servicios_red | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| servicios_red | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| datasets | id | INTEGER | PK | Campo id de la tabla datasets. | PRIMARY KEY AUTOINCREMENT |
| datasets | nombre | TEXT | - | Campo nombre de la tabla datasets. | NOT NULL |
| datasets | descripcion | TEXT | - | Campo descripcion de la tabla datasets. | - |
| datasets | origen | TEXT | - | Campo origen de la tabla datasets. | NOT NULL |
| datasets | formato | TEXT | - | Campo formato de la tabla datasets. | NOT NULL DEFAULT 'csv' |
| datasets | responsable_id | INTEGER | FK -> responsables_ti.id | Identificador relacional asociado. | - |
| datasets | estado | TEXT | - | Estado operativo del registro. | NOT NULL DEFAULT 'registrado' |
| datasets | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| datasets | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| versiones_dataset | id | INTEGER | PK | Campo id de la tabla versiones_dataset. | PRIMARY KEY AUTOINCREMENT |
| versiones_dataset | dataset_id | INTEGER | FK -> datasets.id | Identificador relacional asociado. | NOT NULL |
| versiones_dataset | version | TEXT | - | Campo version de la tabla versiones_dataset. | NOT NULL |
| versiones_dataset | ruta_archivo | TEXT | - | Campo ruta_archivo de la tabla versiones_dataset. | - |
| versiones_dataset | hash_archivo | TEXT | - | Campo hash_archivo de la tabla versiones_dataset. | - |
| versiones_dataset | total_filas | INTEGER | - | Campo total_filas de la tabla versiones_dataset. | NOT NULL DEFAULT 0 |
| versiones_dataset | total_columnas | INTEGER | - | Campo total_columnas de la tabla versiones_dataset. | NOT NULL DEFAULT 0 |
| versiones_dataset | estado | TEXT | - | Estado operativo del registro. | NOT NULL DEFAULT 'activo' |
| versiones_dataset | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| versiones_dataset | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| columnas_dataset | id | INTEGER | PK | Campo id de la tabla columnas_dataset. | PRIMARY KEY AUTOINCREMENT |
| columnas_dataset | version_dataset_id | INTEGER | FK -> versiones_dataset.id | Identificador relacional asociado. | NOT NULL |
| columnas_dataset | nombre_columna | TEXT | - | Campo nombre_columna de la tabla columnas_dataset. | NOT NULL |
| columnas_dataset | tipo_dato | TEXT | - | Campo tipo_dato de la tabla columnas_dataset. | NOT NULL |
| columnas_dataset | es_objetivo | INTEGER | - | Campo es_objetivo de la tabla columnas_dataset. | NOT NULL DEFAULT 0 |
| columnas_dataset | descripcion | TEXT | - | Campo descripcion de la tabla columnas_dataset. | - |
| columnas_dataset | estado | TEXT | - | Estado operativo del registro. | NOT NULL DEFAULT 'activo' |
| columnas_dataset | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| columnas_dataset | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| perfilado_dataset | id | INTEGER | PK | Campo id de la tabla perfilado_dataset. | PRIMARY KEY AUTOINCREMENT |
| perfilado_dataset | version_dataset_id | INTEGER | FK -> versiones_dataset.id | Identificador relacional asociado. | NOT NULL |
| perfilado_dataset | total_nulos | INTEGER | - | Campo total_nulos de la tabla perfilado_dataset. | NOT NULL DEFAULT 0 |
| perfilado_dataset | total_duplicados | INTEGER | - | Campo total_duplicados de la tabla perfilado_dataset. | NOT NULL DEFAULT 0 |
| perfilado_dataset | porcentaje_nulos | REAL | - | Campo porcentaje_nulos de la tabla perfilado_dataset. | NOT NULL DEFAULT 0 |
| perfilado_dataset | columnas_numericas | INTEGER | - | Campo columnas_numericas de la tabla perfilado_dataset. | NOT NULL DEFAULT 0 |
| perfilado_dataset | columnas_categoricas | INTEGER | - | Campo columnas_categoricas de la tabla perfilado_dataset. | NOT NULL DEFAULT 0 |
| perfilado_dataset | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| perfilado_dataset | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| calidad_dataset | id | INTEGER | PK | Campo id de la tabla calidad_dataset. | PRIMARY KEY AUTOINCREMENT |
| calidad_dataset | version_dataset_id | INTEGER | FK -> versiones_dataset.id | Identificador relacional asociado. | NOT NULL |
| calidad_dataset | score_calidad | REAL | - | Campo score_calidad de la tabla calidad_dataset. | NOT NULL DEFAULT 0 |
| calidad_dataset | regla_evaluada | TEXT | - | Campo regla_evaluada de la tabla calidad_dataset. | NOT NULL |
| calidad_dataset | resultado | TEXT | - | Campo resultado de la tabla calidad_dataset. | NOT NULL |
| calidad_dataset | observacion | TEXT | - | Campo observacion de la tabla calidad_dataset. | - |
| calidad_dataset | estado | TEXT | - | Estado operativo del registro. | NOT NULL DEFAULT 'evaluado' |
| calidad_dataset | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| calidad_dataset | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| clases_trafico | id | INTEGER | PK | Campo id de la tabla clases_trafico. | PRIMARY KEY AUTOINCREMENT |
| clases_trafico | nombre | TEXT | - | Campo nombre de la tabla clases_trafico. | NOT NULL UNIQUE |
| clases_trafico | descripcion | TEXT | - | Campo descripcion de la tabla clases_trafico. | - |
| clases_trafico | es_benigna | INTEGER | - | Campo es_benigna de la tabla clases_trafico. | NOT NULL DEFAULT 0 |
| clases_trafico | estado | TEXT | - | Estado operativo del registro. | NOT NULL DEFAULT 'activo' |
| clases_trafico | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| clases_trafico | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| particiones_dataset | id | INTEGER | PK | Campo id de la tabla particiones_dataset. | PRIMARY KEY AUTOINCREMENT |
| particiones_dataset | version_dataset_id | INTEGER | FK -> versiones_dataset.id | Identificador relacional asociado. | NOT NULL |
| particiones_dataset | tipo_particion | TEXT | - | Campo tipo_particion de la tabla particiones_dataset. | NOT NULL |
| particiones_dataset | porcentaje | REAL | - | Campo porcentaje de la tabla particiones_dataset. | NOT NULL |
| particiones_dataset | total_filas | INTEGER | - | Campo total_filas de la tabla particiones_dataset. | NOT NULL DEFAULT 0 |
| particiones_dataset | semilla | INTEGER | - | Campo semilla de la tabla particiones_dataset. | - |
| particiones_dataset | estado | TEXT | - | Estado operativo del registro. | NOT NULL DEFAULT 'activo' |
| particiones_dataset | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| particiones_dataset | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| preprocesamientos | id | INTEGER | PK | Campo id de la tabla preprocesamientos. | PRIMARY KEY AUTOINCREMENT |
| preprocesamientos | version_dataset_id | INTEGER | FK -> versiones_dataset.id | Identificador relacional asociado. | NOT NULL |
| preprocesamientos | nombre | TEXT | - | Campo nombre de la tabla preprocesamientos. | NOT NULL |
| preprocesamientos | descripcion | TEXT | - | Campo descripcion de la tabla preprocesamientos. | - |
| preprocesamientos | configuracion_json | TEXT | - | Campo configuracion_json de la tabla preprocesamientos. | - |
| preprocesamientos | estado | TEXT | - | Estado operativo del registro. | NOT NULL DEFAULT 'ejecutado' |
| preprocesamientos | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| preprocesamientos | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| pasos_preprocesamiento | id | INTEGER | PK | Campo id de la tabla pasos_preprocesamiento. | PRIMARY KEY AUTOINCREMENT |
| pasos_preprocesamiento | preprocesamiento_id | INTEGER | FK -> preprocesamientos.id | Identificador relacional asociado. | NOT NULL |
| pasos_preprocesamiento | nombre | TEXT | - | Campo nombre de la tabla pasos_preprocesamiento. | NOT NULL |
| pasos_preprocesamiento | orden | INTEGER | - | Campo orden de la tabla pasos_preprocesamiento. | NOT NULL |
| pasos_preprocesamiento | resultado | TEXT | - | Campo resultado de la tabla pasos_preprocesamiento. | - |
| pasos_preprocesamiento | estado | TEXT | - | Estado operativo del registro. | NOT NULL DEFAULT 'completado' |
| pasos_preprocesamiento | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| pasos_preprocesamiento | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| transformaciones_datos | id | INTEGER | PK | Campo id de la tabla transformaciones_datos. | PRIMARY KEY AUTOINCREMENT |
| transformaciones_datos | paso_preprocesamiento_id | INTEGER | FK -> pasos_preprocesamiento.id | Identificador relacional asociado. | NOT NULL |
| transformaciones_datos | columna_origen | TEXT | - | Campo columna_origen de la tabla transformaciones_datos. | - |
| transformaciones_datos | tipo_transformacion | TEXT | - | Campo tipo_transformacion de la tabla transformaciones_datos. | NOT NULL |
| transformaciones_datos | parametros_json | TEXT | - | Campo parametros_json de la tabla transformaciones_datos. | - |
| transformaciones_datos | estado | TEXT | - | Estado operativo del registro. | NOT NULL DEFAULT 'activo' |
| transformaciones_datos | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| transformaciones_datos | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| seleccion_caracteristicas | id | INTEGER | PK | Campo id de la tabla seleccion_caracteristicas. | PRIMARY KEY AUTOINCREMENT |
| seleccion_caracteristicas | preprocesamiento_id | INTEGER | FK -> preprocesamientos.id | Identificador relacional asociado. | NOT NULL |
| seleccion_caracteristicas | metodo | TEXT | - | Campo metodo de la tabla seleccion_caracteristicas. | NOT NULL |
| seleccion_caracteristicas | columna | TEXT | - | Campo columna de la tabla seleccion_caracteristicas. | NOT NULL |
| seleccion_caracteristicas | score | REAL | - | Campo score de la tabla seleccion_caracteristicas. | - |
| seleccion_caracteristicas | seleccionada | INTEGER | - | Campo seleccionada de la tabla seleccion_caracteristicas. | NOT NULL DEFAULT 1 |
| seleccion_caracteristicas | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| seleccion_caracteristicas | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| tipos_modelo_ml | id | INTEGER | PK | Campo id de la tabla tipos_modelo_ml. | PRIMARY KEY AUTOINCREMENT |
| tipos_modelo_ml | nombre | TEXT | - | Campo nombre de la tabla tipos_modelo_ml. | NOT NULL UNIQUE |
| tipos_modelo_ml | descripcion | TEXT | - | Campo descripcion de la tabla tipos_modelo_ml. | - |
| tipos_modelo_ml | requiere_escalamiento | INTEGER | - | Campo requiere_escalamiento de la tabla tipos_modelo_ml. | NOT NULL DEFAULT 0 |
| tipos_modelo_ml | estado | TEXT | - | Estado operativo del registro. | NOT NULL DEFAULT 'activo' |
| tipos_modelo_ml | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| tipos_modelo_ml | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| modelos_ml | id | INTEGER | PK | Campo id de la tabla modelos_ml. | PRIMARY KEY AUTOINCREMENT |
| modelos_ml | tipo_modelo_ml_id | INTEGER | FK -> tipos_modelo_ml.id | Identificador relacional asociado. | NOT NULL |
| modelos_ml | nombre | TEXT | - | Campo nombre de la tabla modelos_ml. | NOT NULL |
| modelos_ml | libreria | TEXT | - | Campo libreria de la tabla modelos_ml. | NOT NULL DEFAULT 'scikit-learn' |
| modelos_ml | version_libreria | TEXT | - | Campo version_libreria de la tabla modelos_ml. | - |
| modelos_ml | descripcion | TEXT | - | Campo descripcion de la tabla modelos_ml. | - |
| modelos_ml | estado | TEXT | - | Estado operativo del registro. | NOT NULL DEFAULT 'candidato' |
| modelos_ml | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| modelos_ml | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| parametros_modelo | id | INTEGER | PK | Campo id de la tabla parametros_modelo. | PRIMARY KEY AUTOINCREMENT |
| parametros_modelo | modelo_ml_id | INTEGER | FK -> modelos_ml.id | Identificador relacional asociado. | NOT NULL |
| parametros_modelo | nombre_parametro | TEXT | - | Campo nombre_parametro de la tabla parametros_modelo. | NOT NULL |
| parametros_modelo | valor_parametro | TEXT | - | Campo valor_parametro de la tabla parametros_modelo. | - |
| parametros_modelo | tipo_dato | TEXT | - | Campo tipo_dato de la tabla parametros_modelo. | - |
| parametros_modelo | estado | TEXT | - | Estado operativo del registro. | NOT NULL DEFAULT 'activo' |
| parametros_modelo | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| parametros_modelo | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| entrenamientos | id | INTEGER | PK | Campo id de la tabla entrenamientos. | PRIMARY KEY AUTOINCREMENT |
| entrenamientos | modelo_ml_id | INTEGER | FK -> modelos_ml.id | Identificador relacional asociado. | NOT NULL |
| entrenamientos | preprocesamiento_id | INTEGER | FK -> preprocesamientos.id | Identificador relacional asociado. | - |
| entrenamientos | version_dataset_id | INTEGER | FK -> versiones_dataset.id | Identificador relacional asociado. | - |
| entrenamientos | usuario_id | INTEGER | FK -> usuarios.id | Identificador relacional asociado. | - |
| entrenamientos | fecha_inicio | TEXT | - | Campo fecha_inicio de la tabla entrenamientos. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| entrenamientos | fecha_fin | TEXT | - | Campo fecha_fin de la tabla entrenamientos. | - |
| entrenamientos | estado | TEXT | - | Estado operativo del registro. | NOT NULL DEFAULT 'iniciado' |
| entrenamientos | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| entrenamientos | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| metricas_entrenamiento | id | INTEGER | PK | Campo id de la tabla metricas_entrenamiento. | PRIMARY KEY AUTOINCREMENT |
| metricas_entrenamiento | entrenamiento_id | INTEGER | FK -> entrenamientos.id | Identificador relacional asociado. | NOT NULL |
| metricas_entrenamiento | accuracy | REAL | - | Campo accuracy de la tabla metricas_entrenamiento. | NOT NULL DEFAULT 0 |
| metricas_entrenamiento | precision_score | REAL | - | Campo precision_score de la tabla metricas_entrenamiento. | NOT NULL DEFAULT 0 |
| metricas_entrenamiento | recall | REAL | - | Campo recall de la tabla metricas_entrenamiento. | NOT NULL DEFAULT 0 |
| metricas_entrenamiento | f1_score | REAL | - | Campo f1_score de la tabla metricas_entrenamiento. | NOT NULL DEFAULT 0 |
| metricas_entrenamiento | matriz_confusion_json | TEXT | - | Campo matriz_confusion_json de la tabla metricas_entrenamiento. | - |
| metricas_entrenamiento | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| metricas_entrenamiento | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| comparaciones_modelo | id | INTEGER | PK | Campo id de la tabla comparaciones_modelo. | PRIMARY KEY AUTOINCREMENT |
| comparaciones_modelo | version_dataset_id | INTEGER | FK -> versiones_dataset.id | Identificador relacional asociado. | - |
| comparaciones_modelo | nombre_comparacion | TEXT | - | Campo nombre_comparacion de la tabla comparaciones_modelo. | NOT NULL |
| comparaciones_modelo | criterio_seleccion | TEXT | - | Campo criterio_seleccion de la tabla comparaciones_modelo. | NOT NULL DEFAULT 'f1_score' |
| comparaciones_modelo | observacion | TEXT | - | Campo observacion de la tabla comparaciones_modelo. | - |
| comparaciones_modelo | estado | TEXT | - | Estado operativo del registro. | NOT NULL DEFAULT 'cerrada' |
| comparaciones_modelo | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| comparaciones_modelo | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| modelos_seleccionados | id | INTEGER | PK | Campo id de la tabla modelos_seleccionados. | PRIMARY KEY AUTOINCREMENT |
| modelos_seleccionados | comparacion_modelo_id | INTEGER | FK -> comparaciones_modelo.id | Identificador relacional asociado. | - |
| modelos_seleccionados | entrenamiento_id | INTEGER | FK -> entrenamientos.id | Identificador relacional asociado. | NOT NULL |
| modelos_seleccionados | ruta_artefacto | TEXT | - | Campo ruta_artefacto de la tabla modelos_seleccionados. | NOT NULL |
| modelos_seleccionados | f1_score | REAL | - | Campo f1_score de la tabla modelos_seleccionados. | NOT NULL |
| modelos_seleccionados | version_modelo | TEXT | - | Campo version_modelo de la tabla modelos_seleccionados. | NOT NULL |
| modelos_seleccionados | estado | TEXT | - | Estado operativo del registro. | NOT NULL DEFAULT 'activo' |
| modelos_seleccionados | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| modelos_seleccionados | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| predicciones | id | INTEGER | PK | Campo id de la tabla predicciones. | PRIMARY KEY AUTOINCREMENT |
| predicciones | modelo_seleccionado_id | INTEGER | FK -> modelos_seleccionados.id | Identificador relacional asociado. | - |
| predicciones | usuario_id | INTEGER | FK -> usuarios.id | Identificador relacional asociado. | - |
| predicciones | nombre_lote | TEXT | - | Campo nombre_lote de la tabla predicciones. | NOT NULL |
| predicciones | total_registros | INTEGER | - | Campo total_registros de la tabla predicciones. | NOT NULL DEFAULT 0 |
| predicciones | fecha_prediccion | TEXT | - | Campo fecha_prediccion de la tabla predicciones. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| predicciones | estado | TEXT | - | Estado operativo del registro. | NOT NULL DEFAULT 'procesado' |
| predicciones | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| predicciones | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| eventos_red | id | INTEGER | PK | Campo id de la tabla eventos_red. | PRIMARY KEY AUTOINCREMENT |
| eventos_red | prediccion_id | INTEGER | FK -> predicciones.id | Identificador relacional asociado. | - |
| eventos_red | timestamp_evento | TEXT | - | Campo timestamp_evento de la tabla eventos_red. | - |
| eventos_red | ip_origen | TEXT | - | Campo ip_origen de la tabla eventos_red. | - |
| eventos_red | ip_destino | TEXT | - | Campo ip_destino de la tabla eventos_red. | - |
| eventos_red | protocolo | TEXT | - | Campo protocolo de la tabla eventos_red. | - |
| eventos_red | servicio | TEXT | - | Campo servicio de la tabla eventos_red. | - |
| eventos_red | etiqueta_predicha | TEXT | - | Campo etiqueta_predicha de la tabla eventos_red. | - |
| eventos_red | confianza | REAL | - | Campo confianza de la tabla eventos_red. | - |
| eventos_red | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| eventos_red | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| flujos_trafico | id | INTEGER | PK | Campo id de la tabla flujos_trafico. | PRIMARY KEY AUTOINCREMENT |
| flujos_trafico | evento_red_id | INTEGER | FK -> eventos_red.id | Identificador relacional asociado. | NOT NULL |
| flujos_trafico | bytes_origen | INTEGER | - | Campo bytes_origen de la tabla flujos_trafico. | DEFAULT 0 |
| flujos_trafico | bytes_destino | INTEGER | - | Campo bytes_destino de la tabla flujos_trafico. | DEFAULT 0 |
| flujos_trafico | paquetes_origen | INTEGER | - | Campo paquetes_origen de la tabla flujos_trafico. | DEFAULT 0 |
| flujos_trafico | paquetes_destino | INTEGER | - | Campo paquetes_destino de la tabla flujos_trafico. | DEFAULT 0 |
| flujos_trafico | duracion_segundos | REAL | - | Campo duracion_segundos de la tabla flujos_trafico. | - |
| flujos_trafico | estado | TEXT | - | Estado operativo del registro. | NOT NULL DEFAULT 'analizado' |
| flujos_trafico | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| flujos_trafico | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| tipos_amenaza | id | INTEGER | PK | Campo id de la tabla tipos_amenaza. | PRIMARY KEY AUTOINCREMENT |
| tipos_amenaza | nombre | TEXT | - | Campo nombre de la tabla tipos_amenaza. | NOT NULL UNIQUE |
| tipos_amenaza | descripcion | TEXT | - | Campo descripcion de la tabla tipos_amenaza. | - |
| tipos_amenaza | categoria | TEXT | - | Campo categoria de la tabla tipos_amenaza. | - |
| tipos_amenaza | estado | TEXT | - | Estado operativo del registro. | NOT NULL DEFAULT 'activo' |
| tipos_amenaza | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| tipos_amenaza | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| niveles_severidad | id | INTEGER | PK | Campo id de la tabla niveles_severidad. | PRIMARY KEY AUTOINCREMENT |
| niveles_severidad | nombre | TEXT | - | Campo nombre de la tabla niveles_severidad. | NOT NULL UNIQUE |
| niveles_severidad | peso | INTEGER | - | Campo peso de la tabla niveles_severidad. | NOT NULL |
| niveles_severidad | descripcion | TEXT | - | Campo descripcion de la tabla niveles_severidad. | - |
| niveles_severidad | estado | TEXT | - | Estado operativo del registro. | NOT NULL DEFAULT 'activo' |
| niveles_severidad | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| niveles_severidad | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| amenazas_detectadas | id | INTEGER | PK | Campo id de la tabla amenazas_detectadas. | PRIMARY KEY AUTOINCREMENT |
| amenazas_detectadas | evento_red_id | INTEGER | FK -> eventos_red.id | Identificador relacional asociado. | NOT NULL |
| amenazas_detectadas | tipo_amenaza_id | INTEGER | FK -> tipos_amenaza.id | Identificador relacional asociado. | - |
| amenazas_detectadas | nivel_severidad_id | INTEGER | FK -> niveles_severidad.id | Identificador relacional asociado. | - |
| amenazas_detectadas | probabilidad | REAL | - | Campo probabilidad de la tabla amenazas_detectadas. | - |
| amenazas_detectadas | descripcion | TEXT | - | Campo descripcion de la tabla amenazas_detectadas. | - |
| amenazas_detectadas | estado | TEXT | - | Estado operativo del registro. | NOT NULL DEFAULT 'detectada' |
| amenazas_detectadas | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| amenazas_detectadas | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| estados_alerta | id | INTEGER | PK | Campo id de la tabla estados_alerta. | PRIMARY KEY AUTOINCREMENT |
| estados_alerta | nombre | TEXT | - | Campo nombre de la tabla estados_alerta. | NOT NULL UNIQUE |
| estados_alerta | descripcion | TEXT | - | Campo descripcion de la tabla estados_alerta. | - |
| estados_alerta | estado | TEXT | - | Estado operativo del registro. | NOT NULL DEFAULT 'activo' |
| estados_alerta | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| estados_alerta | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| acciones_recomendadas | id | INTEGER | PK | Campo id de la tabla acciones_recomendadas. | PRIMARY KEY AUTOINCREMENT |
| acciones_recomendadas | tipo_amenaza_id | INTEGER | FK -> tipos_amenaza.id | Identificador relacional asociado. | - |
| acciones_recomendadas | nombre | TEXT | - | Campo nombre de la tabla acciones_recomendadas. | NOT NULL |
| acciones_recomendadas | descripcion | TEXT | - | Campo descripcion de la tabla acciones_recomendadas. | NOT NULL |
| acciones_recomendadas | prioridad | TEXT | - | Campo prioridad de la tabla acciones_recomendadas. | NOT NULL DEFAULT 'media' |
| acciones_recomendadas | estado | TEXT | - | Estado operativo del registro. | NOT NULL DEFAULT 'activo' |
| acciones_recomendadas | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| acciones_recomendadas | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| alertas | id | INTEGER | PK | Campo id de la tabla alertas. | PRIMARY KEY AUTOINCREMENT |
| alertas | amenaza_detectada_id | INTEGER | FK -> amenazas_detectadas.id | Identificador relacional asociado. | - |
| alertas | estado_alerta_id | INTEGER | FK -> estados_alerta.id | Identificador relacional asociado. | - |
| alertas | accion_recomendada_id | INTEGER | FK -> acciones_recomendadas.id | Identificador relacional asociado. | - |
| alertas | titulo | TEXT | - | Campo titulo de la tabla alertas. | NOT NULL |
| alertas | descripcion | TEXT | - | Campo descripcion de la tabla alertas. | - |
| alertas | fecha_alerta | TEXT | - | Campo fecha_alerta de la tabla alertas. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| alertas | revisado_por | INTEGER | FK -> usuarios.id | Campo revisado_por de la tabla alertas. | - |
| alertas | estado | TEXT | - | Estado operativo del registro. | NOT NULL DEFAULT 'nueva' |
| alertas | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| alertas | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| evidencias_alerta | id | INTEGER | PK | Campo id de la tabla evidencias_alerta. | PRIMARY KEY AUTOINCREMENT |
| evidencias_alerta | alerta_id | INTEGER | FK -> alertas.id | Identificador relacional asociado. | NOT NULL |
| evidencias_alerta | tipo_evidencia | TEXT | - | Campo tipo_evidencia de la tabla evidencias_alerta. | NOT NULL |
| evidencias_alerta | ruta_evidencia | TEXT | - | Campo ruta_evidencia de la tabla evidencias_alerta. | - |
| evidencias_alerta | hash_evidencia | TEXT | - | Campo hash_evidencia de la tabla evidencias_alerta. | - |
| evidencias_alerta | descripcion | TEXT | - | Campo descripcion de la tabla evidencias_alerta. | - |
| evidencias_alerta | estado | TEXT | - | Estado operativo del registro. | NOT NULL DEFAULT 'activo' |
| evidencias_alerta | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| evidencias_alerta | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| incidentes_seguridad | id | INTEGER | PK | Campo id de la tabla incidentes_seguridad. | PRIMARY KEY AUTOINCREMENT |
| incidentes_seguridad | alerta_id | INTEGER | FK -> alertas.id | Identificador relacional asociado. | - |
| incidentes_seguridad | titulo | TEXT | - | Campo titulo de la tabla incidentes_seguridad. | NOT NULL |
| incidentes_seguridad | descripcion | TEXT | - | Campo descripcion de la tabla incidentes_seguridad. | - |
| incidentes_seguridad | prioridad | TEXT | - | Campo prioridad de la tabla incidentes_seguridad. | NOT NULL DEFAULT 'media' |
| incidentes_seguridad | estado | TEXT | - | Estado operativo del registro. | NOT NULL DEFAULT 'abierto' |
| incidentes_seguridad | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| incidentes_seguridad | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| atencion_incidente | id | INTEGER | PK | Campo id de la tabla atencion_incidente. | PRIMARY KEY AUTOINCREMENT |
| atencion_incidente | incidente_seguridad_id | INTEGER | FK -> incidentes_seguridad.id | Identificador relacional asociado. | NOT NULL |
| atencion_incidente | usuario_id | INTEGER | FK -> usuarios.id | Identificador relacional asociado. | - |
| atencion_incidente | descripcion_atencion | TEXT | - | Campo descripcion_atencion de la tabla atencion_incidente. | NOT NULL |
| atencion_incidente | resultado | TEXT | - | Campo resultado de la tabla atencion_incidente. | - |
| atencion_incidente | estado | TEXT | - | Estado operativo del registro. | NOT NULL DEFAULT 'registrado' |
| atencion_incidente | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| atencion_incidente | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| escalamiento_incidente | id | INTEGER | PK | Campo id de la tabla escalamiento_incidente. | PRIMARY KEY AUTOINCREMENT |
| escalamiento_incidente | incidente_seguridad_id | INTEGER | FK -> incidentes_seguridad.id | Identificador relacional asociado. | NOT NULL |
| escalamiento_incidente | responsable_ti_id | INTEGER | FK -> responsables_ti.id | Identificador relacional asociado. | - |
| escalamiento_incidente | nivel_escalamiento | TEXT | - | Campo nivel_escalamiento de la tabla escalamiento_incidente. | NOT NULL |
| escalamiento_incidente | motivo | TEXT | - | Campo motivo de la tabla escalamiento_incidente. | NOT NULL |
| escalamiento_incidente | estado | TEXT | - | Estado operativo del registro. | NOT NULL DEFAULT 'pendiente' |
| escalamiento_incidente | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| escalamiento_incidente | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| historial_alerta | id | INTEGER | PK | Campo id de la tabla historial_alerta. | PRIMARY KEY AUTOINCREMENT |
| historial_alerta | alerta_id | INTEGER | FK -> alertas.id | Identificador relacional asociado. | NOT NULL |
| historial_alerta | usuario_id | INTEGER | FK -> usuarios.id | Identificador relacional asociado. | - |
| historial_alerta | estado_anterior | TEXT | - | Campo estado_anterior de la tabla historial_alerta. | - |
| historial_alerta | estado_nuevo | TEXT | - | Campo estado_nuevo de la tabla historial_alerta. | NOT NULL |
| historial_alerta | comentario | TEXT | - | Campo comentario de la tabla historial_alerta. | - |
| historial_alerta | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| historial_alerta | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| tipos_reporte | id | INTEGER | PK | Campo id de la tabla tipos_reporte. | PRIMARY KEY AUTOINCREMENT |
| tipos_reporte | nombre | TEXT | - | Campo nombre de la tabla tipos_reporte. | NOT NULL UNIQUE |
| tipos_reporte | descripcion | TEXT | - | Campo descripcion de la tabla tipos_reporte. | - |
| tipos_reporte | formato | TEXT | - | Campo formato de la tabla tipos_reporte. | NOT NULL |
| tipos_reporte | estado | TEXT | - | Estado operativo del registro. | NOT NULL DEFAULT 'activo' |
| tipos_reporte | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| tipos_reporte | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| reportes | id | INTEGER | PK | Campo id de la tabla reportes. | PRIMARY KEY AUTOINCREMENT |
| reportes | tipo_reporte_id | INTEGER | FK -> tipos_reporte.id | Identificador relacional asociado. | - |
| reportes | titulo | TEXT | - | Campo titulo de la tabla reportes. | NOT NULL |
| reportes | descripcion | TEXT | - | Campo descripcion de la tabla reportes. | - |
| reportes | parametros_json | TEXT | - | Campo parametros_json de la tabla reportes. | - |
| reportes | estado | TEXT | - | Estado operativo del registro. | NOT NULL DEFAULT 'configurado' |
| reportes | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| reportes | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| reportes_generados | id | INTEGER | PK | Campo id de la tabla reportes_generados. | PRIMARY KEY AUTOINCREMENT |
| reportes_generados | reporte_id | INTEGER | FK -> reportes.id | Identificador relacional asociado. | - |
| reportes_generados | usuario_id | INTEGER | FK -> usuarios.id | Identificador relacional asociado. | - |
| reportes_generados | titulo | TEXT | - | Campo titulo de la tabla reportes_generados. | NOT NULL |
| reportes_generados | ruta_archivo | TEXT | - | Campo ruta_archivo de la tabla reportes_generados. | NOT NULL |
| reportes_generados | resumen_json | TEXT | - | Campo resumen_json de la tabla reportes_generados. | - |
| reportes_generados | estado | TEXT | - | Estado operativo del registro. | NOT NULL DEFAULT 'generado' |
| reportes_generados | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| reportes_generados | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| exportaciones_reporte | id | INTEGER | PK | Campo id de la tabla exportaciones_reporte. | PRIMARY KEY AUTOINCREMENT |
| exportaciones_reporte | reporte_generado_id | INTEGER | FK -> reportes_generados.id | Identificador relacional asociado. | NOT NULL |
| exportaciones_reporte | formato | TEXT | - | Campo formato de la tabla exportaciones_reporte. | NOT NULL |
| exportaciones_reporte | ruta_exportacion | TEXT | - | Campo ruta_exportacion de la tabla exportaciones_reporte. | NOT NULL |
| exportaciones_reporte | hash_archivo | TEXT | - | Campo hash_archivo de la tabla exportaciones_reporte. | - |
| exportaciones_reporte | estado | TEXT | - | Estado operativo del registro. | NOT NULL DEFAULT 'exportado' |
| exportaciones_reporte | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| exportaciones_reporte | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| configuracion_sistema | id | INTEGER | PK | Campo id de la tabla configuracion_sistema. | PRIMARY KEY AUTOINCREMENT |
| configuracion_sistema | clave | TEXT | - | Campo clave de la tabla configuracion_sistema. | NOT NULL UNIQUE |
| configuracion_sistema | valor | TEXT | - | Campo valor de la tabla configuracion_sistema. | - |
| configuracion_sistema | descripcion | TEXT | - | Campo descripcion de la tabla configuracion_sistema. | - |
| configuracion_sistema | es_secreto | INTEGER | - | Campo es_secreto de la tabla configuracion_sistema. | NOT NULL DEFAULT 0 |
| configuracion_sistema | estado | TEXT | - | Estado operativo del registro. | NOT NULL DEFAULT 'activo' |
| configuracion_sistema | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| configuracion_sistema | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| umbrales_alerta | id | INTEGER | PK | Campo id de la tabla umbrales_alerta. | PRIMARY KEY AUTOINCREMENT |
| umbrales_alerta | tipo_amenaza_id | INTEGER | FK -> tipos_amenaza.id | Identificador relacional asociado. | - |
| umbrales_alerta | nombre | TEXT | - | Campo nombre de la tabla umbrales_alerta. | NOT NULL |
| umbrales_alerta | valor_minimo | REAL | - | Campo valor_minimo de la tabla umbrales_alerta. | - |
| umbrales_alerta | valor_maximo | REAL | - | Campo valor_maximo de la tabla umbrales_alerta. | - |
| umbrales_alerta | nivel_severidad_id | INTEGER | FK -> niveles_severidad.id | Identificador relacional asociado. | - |
| umbrales_alerta | estado | TEXT | - | Estado operativo del registro. | NOT NULL DEFAULT 'activo' |
| umbrales_alerta | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| umbrales_alerta | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| normas_referencia | id | INTEGER | PK | Campo id de la tabla normas_referencia. | PRIMARY KEY AUTOINCREMENT |
| normas_referencia | codigo | TEXT | - | Campo codigo de la tabla normas_referencia. | NOT NULL UNIQUE |
| normas_referencia | nombre | TEXT | - | Campo nombre de la tabla normas_referencia. | NOT NULL |
| normas_referencia | descripcion | TEXT | - | Campo descripcion de la tabla normas_referencia. | - |
| normas_referencia | version | TEXT | - | Campo version de la tabla normas_referencia. | - |
| normas_referencia | estado | TEXT | - | Estado operativo del registro. | NOT NULL DEFAULT 'activo' |
| normas_referencia | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| normas_referencia | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| controles_cumplimiento | id | INTEGER | PK | Campo id de la tabla controles_cumplimiento. | PRIMARY KEY AUTOINCREMENT |
| controles_cumplimiento | norma_referencia_id | INTEGER | FK -> normas_referencia.id | Identificador relacional asociado. | NOT NULL |
| controles_cumplimiento | codigo_control | TEXT | - | Campo codigo_control de la tabla controles_cumplimiento. | NOT NULL |
| controles_cumplimiento | descripcion | TEXT | - | Campo descripcion de la tabla controles_cumplimiento. | NOT NULL |
| controles_cumplimiento | aplicabilidad | TEXT | - | Campo aplicabilidad de la tabla controles_cumplimiento. | - |
| controles_cumplimiento | estado | TEXT | - | Estado operativo del registro. | NOT NULL DEFAULT 'activo' |
| controles_cumplimiento | created_at | TEXT | - | Fecha de creaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| controles_cumplimiento | updated_at | TEXT | - | Fecha de ?ltima actualizaci?n del registro. | NOT NULL DEFAULT CURRENT_TIMESTAMP |
