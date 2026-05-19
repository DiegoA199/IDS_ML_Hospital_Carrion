INSERT INTO roles (nombre, descripcion) VALUES
('Administrador TI', 'Acceso completo al prototipo IDS-ML'),
('Analista TI', 'Operación de dataset, entrenamiento, inferencia y reportes'),
('Invitado/demo', 'Acceso limitado para demostración académica') ON CONFLICT DO NOTHING;

INSERT INTO permisos (codigo, nombre, descripcion, modulo) VALUES
('dataset.read', 'Ver datasets', 'Permite acceder a datasets cargados', 'dataset'),
('dataset.write', 'Cargar datasets', 'Permite registrar datasets autorizados', 'dataset'),
('ml.train', 'Entrenar modelos', 'Permite ejecutar entrenamiento comparativo', 'ml'),
('ml.predict', 'Ejecutar inferencia', 'Permite analizar tráfico nuevo', 'ml'),
('alerts.manage', 'Gestionar alertas', 'Permite revisar alertas IDS', 'alertas'),
('reports.generate', 'Generar reportes', 'Permite exportar evidencias', 'reportes'),
('system.admin', 'Administrar sistema', 'Permite revisar configuración y usuarios', 'sistema') ON CONFLICT DO NOTHING;

INSERT INTO usuarios (username, email, nombre_completo, password_hash) VALUES
('admin', 'admin@hospital.local', 'Administrador TI Demo', 'demo-no-produccion'),
('analista', 'analista@hospital.local', 'Analista TI Demo', 'demo-no-produccion'),
('invitado', 'invitado@hospital.local', 'Invitado Demo', 'demo-no-produccion') ON CONFLICT DO NOTHING;

INSERT INTO usuarios_roles (usuario_id, rol_id)
SELECT u.id, r.id FROM usuarios u, roles r
WHERE u.username = 'admin' AND r.nombre = 'Administrador TI' ON CONFLICT DO NOTHING;

INSERT INTO usuarios_roles (usuario_id, rol_id)
SELECT u.id, r.id FROM usuarios u, roles r
WHERE u.username = 'analista' AND r.nombre = 'Analista TI' ON CONFLICT DO NOTHING;

INSERT INTO usuarios_roles (usuario_id, rol_id)
SELECT u.id, r.id FROM usuarios u, roles r
WHERE u.username = 'invitado' AND r.nombre = 'Invitado/demo' ON CONFLICT DO NOTHING;

INSERT INTO roles_permisos (rol_id, permiso_id)
SELECT r.id, p.id FROM roles r, permisos p
WHERE r.nombre = 'Administrador TI' ON CONFLICT DO NOTHING;

INSERT INTO roles_permisos (rol_id, permiso_id)
SELECT r.id, p.id FROM roles r, permisos p
WHERE r.nombre = 'Analista TI'
  AND p.codigo IN ('dataset.read', 'dataset.write', 'ml.train', 'ml.predict', 'alerts.manage', 'reports.generate') ON CONFLICT DO NOTHING;

INSERT INTO roles_permisos (rol_id, permiso_id)
SELECT r.id, p.id FROM roles r, permisos p
WHERE r.nombre = 'Invitado/demo'
  AND p.codigo IN ('dataset.read') ON CONFLICT DO NOTHING;

INSERT INTO instituciones (nombre, ruc, tipo, direccion) VALUES
('Hospital Regional Docente Clínico Quirúrgico Daniel Alcides Carrión', '00000000000', 'hospital', 'Huancayo, Perú') ON CONFLICT DO NOTHING;

INSERT INTO sedes (institucion_id, nombre, ciudad, direccion)
SELECT id, 'Sede principal', 'Huancayo', 'Red institucional hospitalaria'
FROM instituciones
WHERE nombre LIKE 'Hospital Regional%' ON CONFLICT DO NOTHING;

INSERT INTO areas_hospitalarias (sede_id, nombre, codigo, descripcion)
SELECT id, 'Unidad TI', 'TI', 'Área responsable de infraestructura y seguridad'
FROM sedes
WHERE nombre = 'Sede principal' ON CONFLICT DO NOTHING;

INSERT INTO cargos (nombre, descripcion) VALUES
('Jefe de TI', 'Responsable de gobierno tecnológico'),
('Analista SOC', 'Responsable de monitoreo y respuesta') ON CONFLICT DO NOTHING;

INSERT INTO responsables_ti (usuario_id, area_id, cargo_id, correo_institucional)
SELECT u.id, a.id, c.id, u.email
FROM usuarios u, areas_hospitalarias a, cargos c
WHERE u.username = 'admin' AND a.codigo = 'TI' AND c.nombre = 'Jefe de TI' ON CONFLICT DO NOTHING;

INSERT INTO tipos_activo (nombre, descripcion) VALUES
('Servidor', 'Servidor institucional'),
('Switch', 'Equipo de conmutación'),
('Firewall', 'Equipo perimetral'),
('Estación clínica', 'Equipo usado en área asistencial') ON CONFLICT DO NOTHING;

INSERT INTO segmentos_red (sede_id, nombre, cidr, criticidad)
SELECT id, 'Segmento SOC demo', '192.168.10.0/24', 'alta'
FROM sedes
WHERE nombre = 'Sede principal' ON CONFLICT DO NOTHING;

INSERT INTO activos_red (tipo_activo_id, area_id, segmento_red_id, nombre, codigo_inventario, criticidad)
SELECT t.id, a.id, s.id, 'Servidor IDS-ML Demo', 'IDSML-SRV-001', 'alta'
FROM tipos_activo t, areas_hospitalarias a, segmentos_red s
WHERE t.nombre = 'Servidor' AND a.codigo = 'TI' AND s.nombre = 'Segmento SOC demo' ON CONFLICT DO NOTHING;

INSERT INTO dispositivos_red (activo_red_id, fabricante, modelo, sistema_operativo, mac_address)
SELECT id, 'Demo', 'Virtual', 'Linux/Windows', '00:00:00:00:00:01'
FROM activos_red
WHERE codigo_inventario = 'IDSML-SRV-001' ON CONFLICT DO NOTHING;

INSERT INTO direcciones_ip (segmento_red_id, activo_red_id, direccion_ip, version_ip)
SELECT s.id, a.id, '192.168.10.10', 'IPv4'
FROM segmentos_red s, activos_red a
WHERE s.nombre = 'Segmento SOC demo' AND a.codigo_inventario = 'IDSML-SRV-001' ON CONFLICT DO NOTHING;

INSERT INTO protocolos_red (nombre, numero_protocolo, descripcion) VALUES
('TCP', 6, 'Transmission Control Protocol'),
('UDP', 17, 'User Datagram Protocol'),
('ICMP', 1, 'Internet Control Message Protocol') ON CONFLICT DO NOTHING;

INSERT INTO servicios_red (protocolo_red_id, nombre, puerto, descripcion)
SELECT id, 'HTTPS', 443, 'Servicio web seguro'
FROM protocolos_red
WHERE nombre = 'TCP' ON CONFLICT DO NOTHING;

INSERT INTO clases_trafico (nombre, descripcion, es_benigna) VALUES
('normal', 'Tráfico sin amenaza identificada', 1),
('DDoS', 'Denegación de servicio distribuida', 0),
('PortScan', 'Escaneo de puertos', 0),
('BruteForce', 'Intento de fuerza bruta', 0) ON CONFLICT DO NOTHING;

INSERT INTO tipos_modelo_ml (nombre, descripcion, requiere_escalamiento) VALUES
('Random Forest', 'Ensamble de árboles de decisión', 0),
('Decision Tree', 'Árbol de decisión interpretable', 0),
('Logistic Regression', 'Modelo lineal de clasificación', 1),
('SVM', 'Máquina de vectores de soporte', 1),
('KNN', 'Vecinos más cercanos', 1),
('Naive Bayes', 'Clasificador probabilístico bayesiano', 0) ON CONFLICT DO NOTHING;

INSERT INTO niveles_severidad (nombre, peso, descripcion) VALUES
('Baja', 1, 'Evento informativo o tráfico normal'),
('Media', 2, 'Evento que requiere revisión'),
('Alta', 3, 'Amenaza probable para infraestructura'),
('Crítica', 4, 'Amenaza confirmada o de alto impacto') ON CONFLICT DO NOTHING;

INSERT INTO tipos_amenaza (nombre, descripcion, categoria) VALUES
('DDoS', 'Patrón de denegación de servicio', 'Disponibilidad'),
('PortScan', 'Reconocimiento de servicios expuestos', 'Reconocimiento'),
('BruteForce', 'Intentos repetidos de autenticación', 'Acceso'),
('Malware', 'Comportamiento asociado a software malicioso', 'Integridad') ON CONFLICT DO NOTHING;

INSERT INTO estados_alerta (nombre, descripcion) VALUES
('nueva', 'Alerta generada y pendiente de revisión'),
('revisada', 'Alerta evaluada por personal TI'),
('cerrada', 'Alerta cerrada con atención documentada') ON CONFLICT DO NOTHING;

INSERT INTO acciones_recomendadas (tipo_amenaza_id, nombre, descripcion, prioridad)
SELECT id, 'Aislar equipo sospechoso', 'Validar origen/destino y aislar temporalmente el activo si procede', 'alta'
FROM tipos_amenaza
WHERE nombre = 'DDoS' ON CONFLICT DO NOTHING;

INSERT INTO tipos_reporte (nombre, descripcion, formato) VALUES
('Resumen ejecutivo IDS-ML', 'Reporte de métricas, alertas y trazabilidad', 'pdf'),
('Experimentos ML', 'Reporte tabular de comparación de modelos', 'csv') ON CONFLICT DO NOTHING;

INSERT INTO configuracion_sistema (clave, valor, descripcion, es_secreto) VALUES
('IDSML_PERSISTENCE_BACKEND', 'auto', 'Backend de persistencia activo', 0),
('MAX_ALERTS_PER_BATCH', '100', 'Máximo de alertas generadas por lote', 0) ON CONFLICT DO NOTHING;

INSERT INTO normas_referencia (codigo, nombre, descripcion, version) VALUES
('ISO27001', 'ISO/IEC 27001', 'Sistema de gestión de seguridad de la información', '2022'),
('NIST-CSF', 'NIST Cybersecurity Framework', 'Marco de referencia de ciberseguridad', '2.0') ON CONFLICT DO NOTHING;

INSERT INTO controles_cumplimiento (norma_referencia_id, codigo_control, descripcion, aplicabilidad)
SELECT id, 'A.8.16', 'Monitoreo de actividades', 'Trazabilidad de eventos IDS-ML'
FROM normas_referencia
WHERE codigo = 'ISO27001' ON CONFLICT DO NOTHING;
