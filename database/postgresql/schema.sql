-- ============================================================
-- IDS-ML Hospital Carrion - Modelo relacional academico
-- Compatible con SQLite para pruebas locales.
-- Adaptable a PostgreSQL reemplazando INTEGER PRIMARY KEY
-- AUTOINCREMENT por BIGSERIAL/IDENTITY y TEXT por tipos especificos.
-- ============================================================

CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT UNIQUE,
    nombre_completo TEXT NOT NULL,
    password_hash TEXT,
    estado TEXT NOT NULL DEFAULT 'activo',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS roles (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL UNIQUE,
    descripcion TEXT,
    estado TEXT NOT NULL DEFAULT 'activo',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS permisos (
    id SERIAL PRIMARY KEY,
    codigo TEXT NOT NULL UNIQUE,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    modulo TEXT NOT NULL,
    estado TEXT NOT NULL DEFAULT 'activo',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS usuarios_roles (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL,
    rol_id INTEGER NOT NULL,
    estado TEXT NOT NULL DEFAULT 'activo',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (usuario_id, rol_id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (rol_id) REFERENCES roles(id)
);

CREATE TABLE IF NOT EXISTS roles_permisos (
    id SERIAL PRIMARY KEY,
    rol_id INTEGER NOT NULL,
    permiso_id INTEGER NOT NULL,
    estado TEXT NOT NULL DEFAULT 'activo',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (rol_id, permiso_id),
    FOREIGN KEY (rol_id) REFERENCES roles(id),
    FOREIGN KEY (permiso_id) REFERENCES permisos(id)
);

CREATE TABLE IF NOT EXISTS sesiones_usuario (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL,
    token_referencia TEXT,
    ip_origen TEXT,
    user_agent TEXT,
    inicio_sesion TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fin_sesion TEXT,
    estado TEXT NOT NULL DEFAULT 'activa',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

CREATE TABLE IF NOT EXISTS bitacora_accesos (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER,
    accion TEXT NOT NULL,
    resultado TEXT NOT NULL,
    ip_origen TEXT,
    detalle TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

CREATE TABLE IF NOT EXISTS auditoria_sistema (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER,
    modulo TEXT NOT NULL,
    accion TEXT NOT NULL,
    entidad TEXT,
    entidad_id TEXT,
    resultado TEXT NOT NULL,
    detalle TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

CREATE TABLE IF NOT EXISTS instituciones (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    ruc TEXT UNIQUE,
    tipo TEXT NOT NULL DEFAULT 'hospital',
    direccion TEXT,
    estado TEXT NOT NULL DEFAULT 'activo',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sedes (
    id SERIAL PRIMARY KEY,
    institucion_id INTEGER NOT NULL,
    nombre TEXT NOT NULL,
    ciudad TEXT,
    direccion TEXT,
    estado TEXT NOT NULL DEFAULT 'activo',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (institucion_id) REFERENCES instituciones(id)
);

CREATE TABLE IF NOT EXISTS areas_hospitalarias (
    id SERIAL PRIMARY KEY,
    sede_id INTEGER NOT NULL,
    nombre TEXT NOT NULL,
    codigo TEXT,
    descripcion TEXT,
    estado TEXT NOT NULL DEFAULT 'activo',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sede_id) REFERENCES sedes(id)
);

CREATE TABLE IF NOT EXISTS cargos (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL UNIQUE,
    descripcion TEXT,
    estado TEXT NOT NULL DEFAULT 'activo',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS responsables_ti (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER,
    area_id INTEGER,
    cargo_id INTEGER,
    telefono TEXT,
    correo_institucional TEXT,
    estado TEXT NOT NULL DEFAULT 'activo',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (area_id) REFERENCES areas_hospitalarias(id),
    FOREIGN KEY (cargo_id) REFERENCES cargos(id)
);

CREATE TABLE IF NOT EXISTS tipos_activo (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL UNIQUE,
    descripcion TEXT,
    estado TEXT NOT NULL DEFAULT 'activo',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS segmentos_red (
    id SERIAL PRIMARY KEY,
    sede_id INTEGER,
    nombre TEXT NOT NULL,
    cidr TEXT NOT NULL,
    criticidad TEXT NOT NULL DEFAULT 'media',
    estado TEXT NOT NULL DEFAULT 'activo',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sede_id) REFERENCES sedes(id)
);

CREATE TABLE IF NOT EXISTS activos_red (
    id SERIAL PRIMARY KEY,
    tipo_activo_id INTEGER,
    area_id INTEGER,
    segmento_red_id INTEGER,
    nombre TEXT NOT NULL,
    codigo_inventario TEXT UNIQUE,
    criticidad TEXT NOT NULL DEFAULT 'media',
    estado TEXT NOT NULL DEFAULT 'activo',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tipo_activo_id) REFERENCES tipos_activo(id),
    FOREIGN KEY (area_id) REFERENCES areas_hospitalarias(id),
    FOREIGN KEY (segmento_red_id) REFERENCES segmentos_red(id)
);

CREATE TABLE IF NOT EXISTS dispositivos_red (
    id SERIAL PRIMARY KEY,
    activo_red_id INTEGER NOT NULL,
    fabricante TEXT,
    modelo TEXT,
    sistema_operativo TEXT,
    mac_address TEXT,
    estado TEXT NOT NULL DEFAULT 'activo',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (activo_red_id) REFERENCES activos_red(id)
);

CREATE TABLE IF NOT EXISTS direcciones_ip (
    id SERIAL PRIMARY KEY,
    segmento_red_id INTEGER,
    activo_red_id INTEGER,
    direccion_ip TEXT NOT NULL UNIQUE,
    version_ip TEXT NOT NULL DEFAULT 'IPv4',
    es_estatica INTEGER NOT NULL DEFAULT 1,
    estado TEXT NOT NULL DEFAULT 'activo',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (segmento_red_id) REFERENCES segmentos_red(id),
    FOREIGN KEY (activo_red_id) REFERENCES activos_red(id)
);

CREATE TABLE IF NOT EXISTS protocolos_red (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL UNIQUE,
    numero_protocolo INTEGER,
    descripcion TEXT,
    estado TEXT NOT NULL DEFAULT 'activo',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS servicios_red (
    id SERIAL PRIMARY KEY,
    protocolo_red_id INTEGER,
    nombre TEXT NOT NULL,
    puerto INTEGER,
    descripcion TEXT,
    estado TEXT NOT NULL DEFAULT 'activo',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (protocolo_red_id) REFERENCES protocolos_red(id)
);

CREATE TABLE IF NOT EXISTS datasets (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    origen TEXT NOT NULL,
    formato TEXT NOT NULL DEFAULT 'csv',
    responsable_id INTEGER,
    estado TEXT NOT NULL DEFAULT 'registrado',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (responsable_id) REFERENCES responsables_ti(id)
);

CREATE TABLE IF NOT EXISTS versiones_dataset (
    id SERIAL PRIMARY KEY,
    dataset_id INTEGER NOT NULL,
    version TEXT NOT NULL,
    ruta_archivo TEXT,
    hash_archivo TEXT,
    total_filas INTEGER NOT NULL DEFAULT 0,
    total_columnas INTEGER NOT NULL DEFAULT 0,
    estado TEXT NOT NULL DEFAULT 'activo',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (dataset_id, version),
    FOREIGN KEY (dataset_id) REFERENCES datasets(id)
);

CREATE TABLE IF NOT EXISTS columnas_dataset (
    id SERIAL PRIMARY KEY,
    version_dataset_id INTEGER NOT NULL,
    nombre_columna TEXT NOT NULL,
    tipo_dato TEXT NOT NULL,
    es_objetivo INTEGER NOT NULL DEFAULT 0,
    descripcion TEXT,
    estado TEXT NOT NULL DEFAULT 'activo',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (version_dataset_id) REFERENCES versiones_dataset(id)
);

CREATE TABLE IF NOT EXISTS perfilado_dataset (
    id SERIAL PRIMARY KEY,
    version_dataset_id INTEGER NOT NULL,
    total_nulos INTEGER NOT NULL DEFAULT 0,
    total_duplicados INTEGER NOT NULL DEFAULT 0,
    porcentaje_nulos DOUBLE PRECISION NOT NULL DEFAULT 0,
    columnas_numericas INTEGER NOT NULL DEFAULT 0,
    columnas_categoricas INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (version_dataset_id) REFERENCES versiones_dataset(id)
);

CREATE TABLE IF NOT EXISTS calidad_dataset (
    id SERIAL PRIMARY KEY,
    version_dataset_id INTEGER NOT NULL,
    score_calidad DOUBLE PRECISION NOT NULL DEFAULT 0,
    regla_evaluada TEXT NOT NULL,
    resultado TEXT NOT NULL,
    observacion TEXT,
    estado TEXT NOT NULL DEFAULT 'evaluado',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (version_dataset_id) REFERENCES versiones_dataset(id)
);

CREATE TABLE IF NOT EXISTS clases_trafico (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL UNIQUE,
    descripcion TEXT,
    es_benigna INTEGER NOT NULL DEFAULT 0,
    estado TEXT NOT NULL DEFAULT 'activo',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS particiones_dataset (
    id SERIAL PRIMARY KEY,
    version_dataset_id INTEGER NOT NULL,
    tipo_particion TEXT NOT NULL,
    porcentaje DOUBLE PRECISION NOT NULL,
    total_filas INTEGER NOT NULL DEFAULT 0,
    semilla INTEGER,
    estado TEXT NOT NULL DEFAULT 'activo',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (version_dataset_id) REFERENCES versiones_dataset(id)
);

CREATE TABLE IF NOT EXISTS preprocesamientos (
    id SERIAL PRIMARY KEY,
    version_dataset_id INTEGER NOT NULL,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    configuracion_json TEXT,
    estado TEXT NOT NULL DEFAULT 'ejecutado',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (version_dataset_id) REFERENCES versiones_dataset(id)
);

CREATE TABLE IF NOT EXISTS pasos_preprocesamiento (
    id SERIAL PRIMARY KEY,
    preprocesamiento_id INTEGER NOT NULL,
    nombre TEXT NOT NULL,
    orden INTEGER NOT NULL,
    resultado TEXT,
    estado TEXT NOT NULL DEFAULT 'completado',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (preprocesamiento_id) REFERENCES preprocesamientos(id)
);

CREATE TABLE IF NOT EXISTS transformaciones_datos (
    id SERIAL PRIMARY KEY,
    paso_preprocesamiento_id INTEGER NOT NULL,
    columna_origen TEXT,
    tipo_transformacion TEXT NOT NULL,
    parametros_json TEXT,
    estado TEXT NOT NULL DEFAULT 'activo',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (paso_preprocesamiento_id) REFERENCES pasos_preprocesamiento(id)
);

CREATE TABLE IF NOT EXISTS seleccion_caracteristicas (
    id SERIAL PRIMARY KEY,
    preprocesamiento_id INTEGER NOT NULL,
    metodo TEXT NOT NULL,
    columna TEXT NOT NULL,
    score DOUBLE PRECISION,
    seleccionada INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (preprocesamiento_id) REFERENCES preprocesamientos(id)
);

CREATE TABLE IF NOT EXISTS tipos_modelo_ml (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL UNIQUE,
    descripcion TEXT,
    requiere_escalamiento INTEGER NOT NULL DEFAULT 0,
    estado TEXT NOT NULL DEFAULT 'activo',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS modelos_ml (
    id SERIAL PRIMARY KEY,
    tipo_modelo_ml_id INTEGER NOT NULL,
    nombre TEXT NOT NULL,
    libreria TEXT NOT NULL DEFAULT 'scikit-learn',
    version_libreria TEXT,
    descripcion TEXT,
    estado TEXT NOT NULL DEFAULT 'candidato',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tipo_modelo_ml_id) REFERENCES tipos_modelo_ml(id)
);

CREATE TABLE IF NOT EXISTS parametros_modelo (
    id SERIAL PRIMARY KEY,
    modelo_ml_id INTEGER NOT NULL,
    nombre_parametro TEXT NOT NULL,
    valor_parametro TEXT,
    tipo_dato TEXT,
    estado TEXT NOT NULL DEFAULT 'activo',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (modelo_ml_id) REFERENCES modelos_ml(id)
);

CREATE TABLE IF NOT EXISTS entrenamientos (
    id SERIAL PRIMARY KEY,
    modelo_ml_id INTEGER NOT NULL,
    preprocesamiento_id INTEGER,
    version_dataset_id INTEGER,
    usuario_id INTEGER,
    fecha_inicio TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_fin TEXT,
    estado TEXT NOT NULL DEFAULT 'iniciado',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (modelo_ml_id) REFERENCES modelos_ml(id),
    FOREIGN KEY (preprocesamiento_id) REFERENCES preprocesamientos(id),
    FOREIGN KEY (version_dataset_id) REFERENCES versiones_dataset(id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

CREATE TABLE IF NOT EXISTS metricas_entrenamiento (
    id SERIAL PRIMARY KEY,
    entrenamiento_id INTEGER NOT NULL,
    accuracy DOUBLE PRECISION NOT NULL DEFAULT 0,
    precision_score DOUBLE PRECISION NOT NULL DEFAULT 0,
    recall DOUBLE PRECISION NOT NULL DEFAULT 0,
    f1_score DOUBLE PRECISION NOT NULL DEFAULT 0,
    matriz_confusion_json TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (entrenamiento_id) REFERENCES entrenamientos(id)
);

CREATE TABLE IF NOT EXISTS comparaciones_modelo (
    id SERIAL PRIMARY KEY,
    version_dataset_id INTEGER,
    nombre_comparacion TEXT NOT NULL,
    criterio_seleccion TEXT NOT NULL DEFAULT 'f1_score',
    observacion TEXT,
    estado TEXT NOT NULL DEFAULT 'cerrada',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (version_dataset_id) REFERENCES versiones_dataset(id)
);

CREATE TABLE IF NOT EXISTS modelos_seleccionados (
    id SERIAL PRIMARY KEY,
    comparacion_modelo_id INTEGER,
    entrenamiento_id INTEGER NOT NULL,
    ruta_artefacto TEXT NOT NULL,
    f1_score DOUBLE PRECISION NOT NULL,
    version_modelo TEXT NOT NULL,
    estado TEXT NOT NULL DEFAULT 'activo',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (comparacion_modelo_id) REFERENCES comparaciones_modelo(id),
    FOREIGN KEY (entrenamiento_id) REFERENCES entrenamientos(id)
);

CREATE TABLE IF NOT EXISTS predicciones (
    id SERIAL PRIMARY KEY,
    modelo_seleccionado_id INTEGER,
    usuario_id INTEGER,
    nombre_lote TEXT NOT NULL,
    total_registros INTEGER NOT NULL DEFAULT 0,
    fecha_prediccion TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    estado TEXT NOT NULL DEFAULT 'procesado',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (modelo_seleccionado_id) REFERENCES modelos_seleccionados(id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

CREATE TABLE IF NOT EXISTS eventos_red (
    id SERIAL PRIMARY KEY,
    prediccion_id INTEGER,
    timestamp_evento TEXT,
    ip_origen TEXT,
    ip_destino TEXT,
    protocolo TEXT,
    servicio TEXT,
    etiqueta_predicha TEXT,
    confianza DOUBLE PRECISION,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (prediccion_id) REFERENCES predicciones(id)
);

CREATE TABLE IF NOT EXISTS flujos_trafico (
    id SERIAL PRIMARY KEY,
    evento_red_id INTEGER NOT NULL,
    bytes_origen INTEGER DEFAULT 0,
    bytes_destino INTEGER DEFAULT 0,
    paquetes_origen INTEGER DEFAULT 0,
    paquetes_destino INTEGER DEFAULT 0,
    duracion_segundos DOUBLE PRECISION,
    estado TEXT NOT NULL DEFAULT 'analizado',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (evento_red_id) REFERENCES eventos_red(id)
);

CREATE TABLE IF NOT EXISTS tipos_amenaza (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL UNIQUE,
    descripcion TEXT,
    categoria TEXT,
    estado TEXT NOT NULL DEFAULT 'activo',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS niveles_severidad (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL UNIQUE,
    peso INTEGER NOT NULL,
    descripcion TEXT,
    estado TEXT NOT NULL DEFAULT 'activo',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS amenazas_detectadas (
    id SERIAL PRIMARY KEY,
    evento_red_id INTEGER NOT NULL,
    tipo_amenaza_id INTEGER,
    nivel_severidad_id INTEGER,
    probabilidad DOUBLE PRECISION,
    descripcion TEXT,
    estado TEXT NOT NULL DEFAULT 'detectada',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (evento_red_id) REFERENCES eventos_red(id),
    FOREIGN KEY (tipo_amenaza_id) REFERENCES tipos_amenaza(id),
    FOREIGN KEY (nivel_severidad_id) REFERENCES niveles_severidad(id)
);

CREATE TABLE IF NOT EXISTS estados_alerta (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL UNIQUE,
    descripcion TEXT,
    estado TEXT NOT NULL DEFAULT 'activo',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS acciones_recomendadas (
    id SERIAL PRIMARY KEY,
    tipo_amenaza_id INTEGER,
    nombre TEXT NOT NULL,
    descripcion TEXT NOT NULL,
    prioridad TEXT NOT NULL DEFAULT 'media',
    estado TEXT NOT NULL DEFAULT 'activo',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tipo_amenaza_id) REFERENCES tipos_amenaza(id)
);

CREATE TABLE IF NOT EXISTS alertas (
    id SERIAL PRIMARY KEY,
    amenaza_detectada_id INTEGER,
    estado_alerta_id INTEGER,
    accion_recomendada_id INTEGER,
    titulo TEXT NOT NULL,
    descripcion TEXT,
    fecha_alerta TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    revisado_por INTEGER,
    estado TEXT NOT NULL DEFAULT 'nueva',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (amenaza_detectada_id) REFERENCES amenazas_detectadas(id),
    FOREIGN KEY (estado_alerta_id) REFERENCES estados_alerta(id),
    FOREIGN KEY (accion_recomendada_id) REFERENCES acciones_recomendadas(id),
    FOREIGN KEY (revisado_por) REFERENCES usuarios(id)
);

CREATE TABLE IF NOT EXISTS evidencias_alerta (
    id SERIAL PRIMARY KEY,
    alerta_id INTEGER NOT NULL,
    tipo_evidencia TEXT NOT NULL,
    ruta_evidencia TEXT,
    hash_evidencia TEXT,
    descripcion TEXT,
    estado TEXT NOT NULL DEFAULT 'activo',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (alerta_id) REFERENCES alertas(id)
);

CREATE TABLE IF NOT EXISTS incidentes_seguridad (
    id SERIAL PRIMARY KEY,
    alerta_id INTEGER,
    titulo TEXT NOT NULL,
    descripcion TEXT,
    prioridad TEXT NOT NULL DEFAULT 'media',
    estado TEXT NOT NULL DEFAULT 'abierto',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (alerta_id) REFERENCES alertas(id)
);

CREATE TABLE IF NOT EXISTS atencion_incidente (
    id SERIAL PRIMARY KEY,
    incidente_seguridad_id INTEGER NOT NULL,
    usuario_id INTEGER,
    descripcion_atencion TEXT NOT NULL,
    resultado TEXT,
    estado TEXT NOT NULL DEFAULT 'registrado',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (incidente_seguridad_id) REFERENCES incidentes_seguridad(id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

CREATE TABLE IF NOT EXISTS escalamiento_incidente (
    id SERIAL PRIMARY KEY,
    incidente_seguridad_id INTEGER NOT NULL,
    responsable_ti_id INTEGER,
    nivel_escalamiento TEXT NOT NULL,
    motivo TEXT NOT NULL,
    estado TEXT NOT NULL DEFAULT 'pendiente',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (incidente_seguridad_id) REFERENCES incidentes_seguridad(id),
    FOREIGN KEY (responsable_ti_id) REFERENCES responsables_ti(id)
);

CREATE TABLE IF NOT EXISTS historial_alerta (
    id SERIAL PRIMARY KEY,
    alerta_id INTEGER NOT NULL,
    usuario_id INTEGER,
    estado_anterior TEXT,
    estado_nuevo TEXT NOT NULL,
    comentario TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (alerta_id) REFERENCES alertas(id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

CREATE TABLE IF NOT EXISTS tipos_reporte (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL UNIQUE,
    descripcion TEXT,
    formato TEXT NOT NULL,
    estado TEXT NOT NULL DEFAULT 'activo',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS reportes (
    id SERIAL PRIMARY KEY,
    tipo_reporte_id INTEGER,
    titulo TEXT NOT NULL,
    descripcion TEXT,
    parametros_json TEXT,
    estado TEXT NOT NULL DEFAULT 'configurado',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tipo_reporte_id) REFERENCES tipos_reporte(id)
);

CREATE TABLE IF NOT EXISTS reportes_generados (
    id SERIAL PRIMARY KEY,
    reporte_id INTEGER,
    usuario_id INTEGER,
    titulo TEXT NOT NULL,
    ruta_archivo TEXT NOT NULL,
    resumen_json TEXT,
    estado TEXT NOT NULL DEFAULT 'generado',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (reporte_id) REFERENCES reportes(id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

CREATE TABLE IF NOT EXISTS exportaciones_reporte (
    id SERIAL PRIMARY KEY,
    reporte_generado_id INTEGER NOT NULL,
    formato TEXT NOT NULL,
    ruta_exportacion TEXT NOT NULL,
    hash_archivo TEXT,
    estado TEXT NOT NULL DEFAULT 'exportado',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (reporte_generado_id) REFERENCES reportes_generados(id)
);

CREATE TABLE IF NOT EXISTS configuracion_sistema (
    id SERIAL PRIMARY KEY,
    clave TEXT NOT NULL UNIQUE,
    valor TEXT,
    descripcion TEXT,
    es_secreto INTEGER NOT NULL DEFAULT 0,
    estado TEXT NOT NULL DEFAULT 'activo',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS umbrales_alerta (
    id SERIAL PRIMARY KEY,
    tipo_amenaza_id INTEGER,
    nombre TEXT NOT NULL,
    valor_minimo DOUBLE PRECISION,
    valor_maximo DOUBLE PRECISION,
    nivel_severidad_id INTEGER,
    estado TEXT NOT NULL DEFAULT 'activo',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tipo_amenaza_id) REFERENCES tipos_amenaza(id),
    FOREIGN KEY (nivel_severidad_id) REFERENCES niveles_severidad(id)
);

CREATE TABLE IF NOT EXISTS normas_referencia (
    id SERIAL PRIMARY KEY,
    codigo TEXT NOT NULL UNIQUE,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    version TEXT,
    estado TEXT NOT NULL DEFAULT 'activo',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS controles_cumplimiento (
    id SERIAL PRIMARY KEY,
    norma_referencia_id INTEGER NOT NULL,
    codigo_control TEXT NOT NULL,
    descripcion TEXT NOT NULL,
    aplicabilidad TEXT,
    estado TEXT NOT NULL DEFAULT 'activo',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (norma_referencia_id) REFERENCES normas_referencia(id)
);

CREATE TABLE IF NOT EXISTS test_plan (
    id SERIAL PRIMARY KEY,
    code TEXT NOT NULL UNIQUE,
    module TEXT NOT NULL,
    description TEXT NOT NULL,
    test_type TEXT NOT NULL CHECK (test_type IN ('Funcional', 'Integración', 'Rendimiento', 'Seguridad', 'Usabilidad')),
    standard TEXT NOT NULL,
    input_data TEXT,
    expected_result TEXT NOT NULL,
    obtained_result TEXT,
    status TEXT NOT NULL DEFAULT 'Pendiente' CHECK (status IN ('Pendiente', 'Aprobado', 'Observado', 'Fallido')),
    responsible TEXT NOT NULL,
    execution_date DATE NOT NULL,
    evidence TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS literature_implementation (
    id SERIAL PRIMARY KEY,
    article_code TEXT NOT NULL UNIQUE,
    authors TEXT NOT NULL,
    year INTEGER NOT NULL CHECK (year >= 1900),
    title TEXT NOT NULL,
    source TEXT NOT NULL,
    contribution_type TEXT NOT NULL,
    problem TEXT NOT NULL,
    method TEXT NOT NULL,
    technologies TEXT NOT NULL,
    main_results TEXT NOT NULL,
    relation_with_project TEXT NOT NULL,
    related_dimension TEXT NOT NULL,
    citation_format TEXT NOT NULL,
    link_or_doi TEXT,
    observations TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

