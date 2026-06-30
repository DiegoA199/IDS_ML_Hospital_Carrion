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

INSERT INTO test_plan
(code, module, description, test_type, standard, input_data, expected_result, obtained_result, status, responsible, execution_date, evidence) VALUES
('CP-01', 'Carga de Dataset', 'Validar carga correcta del dataset.', 'Funcional', 'ISO/IEC 29119', 'CSV válido', 'El dataset se carga y perfila.', '', 'Pendiente', 'Analista TI', '2026-06-30', 'Caso base.'),
('CP-02', 'Preprocesamiento', 'Validar limpieza y preprocesamiento.', 'Funcional', 'ISO/IEC 25010', 'Dataset con nulos', 'Los datos quedan listos para entrenamiento.', '', 'Pendiente', 'Analista TI', '2026-06-30', 'Revisar pipeline.'),
('CP-03', 'Entrenamiento', 'Validar entrenamiento de Random Forest.', 'Integración', 'ISO/IEC 29119', 'Dataset preparado', 'El modelo y sus métricas son generados.', '', 'Pendiente', 'Analista TI', '2026-06-30', 'Modelo candidato.'),
('CP-04', 'Entrenamiento', 'Validar entrenamiento de SVM.', 'Rendimiento', 'ISO/IEC 25010', 'Dataset escalado', 'SVM finaliza y reporta métricas.', '', 'Pendiente', 'Analista TI', '2026-06-30', 'Medir duración.'),
('CP-05', 'Entrenamiento', 'Validar cálculo de Accuracy, Precision, Recall y F1-score.', 'Funcional', 'ISO/IEC 25010', 'Etiquetas reales y predichas', 'Las cuatro métricas son correctas.', '', 'Pendiente', 'Analista TI', '2026-06-30', 'Contrastar resultados.'),
('CP-06', 'Entrenamiento', 'Validar generación de matriz de confusión.', 'Funcional', 'ISO/IEC 29119', 'Resultados del modelo', 'La matriz representa todas las clases.', '', 'Pendiente', 'Analista TI', '2026-06-30', 'Validación visual.'),
('CP-07', 'Predicción', 'Validar predicción de nuevo tráfico.', 'Integración', 'ISO/IEC 25010', 'CSV de tráfico', 'Cada fila obtiene etiqueta y confianza.', '', 'Pendiente', 'Analista TI', '2026-06-30', 'Usar fixture.'),
('CP-08', 'Alertas', 'Validar generación de alerta IDS-ML.', 'Seguridad', 'ISO/IEC 27001', 'Predicción maliciosa', 'Se registra alerta y recomendación.', '', 'Pendiente', 'Administrador TI', '2026-06-30', 'Revisar alertas.'),
('CP-09', 'Base de Datos', 'Validar almacenamiento en PostgreSQL/Neon.', 'Integración', 'ISO/IEC 27001', 'Registro de prueba', 'El registro persiste y se consulta.', '', 'Pendiente', 'Administrador TI', '2026-06-30', 'SQLite como fallback.'),
('CP-10', 'Reportes', 'Validar exportación de reporte.', 'Usabilidad', 'ISO 9001', 'Registros existentes', 'Se descarga un CSV legible.', '', 'Pendiente', 'Analista TI', '2026-06-30', 'Abrir exportación.') ON CONFLICT DO NOTHING;

INSERT INTO literature_implementation
(article_code, authors, year, title, source, contribution_type, problem, method, technologies, main_results, relation_with_project, related_dimension, citation_format, link_or_doi, observations) VALUES
('A01', 'Buczak, A. L.; Guven, E.', 2016, 'A Survey of Data Mining and Machine Learning Methods for Cyber Security Intrusion Detection', 'IEEE Communications Surveys & Tutorials', 'Machine learning', 'Selección de métodos ML para IDS.', 'Revisión y taxonomía.', 'Machine learning, IDS, minería de datos', 'Compara familias de algoritmos.', 'Sustenta la comparación de clasificadores.', 'Entrenamiento y comparación de modelos', 'A. L. Buczak and E. Guven, IEEE Commun. Surveys Tuts., 2016.', 'https://doi.org/10.1109/COMST.2015.2494502', 'Artículo de revisión.'),
('A02', 'Sommer, R.; Paxson, V.', 2010, 'Outside the Closed World: On Using Machine Learning for Network Intrusion Detection', 'IEEE Symposium on Security and Privacy', 'Seguridad', 'Uso de ML en redes reales.', 'Análisis crítico operacional.', 'Network IDS, machine learning', 'Expone brechas de contexto y evaluación.', 'Justifica trazabilidad y supervisión humana.', 'Interpretabilidad, trazabilidad y utilidad institucional', 'R. Sommer and V. Paxson, Proc. IEEE S&P, 2010.', 'https://doi.org/10.1109/SP.2010.25', 'Validez externa.'),
('A03', 'Khraisat, A. et al.', 2019, 'Survey of Intrusion Detection Systems: Techniques, Datasets and Challenges', 'Cybersecurity', 'Arquitectura', 'Técnicas y datasets IDS fragmentados.', 'Revisión comparativa.', 'IDS, datasets, ML', 'Integra una taxonomía de IDS.', 'Sustenta arquitectura y datos.', 'Gestión y preparación del dataset', 'A. Khraisat et al., Cybersecurity, 2019.', 'https://doi.org/10.1186/s42400-019-0038-7', 'Acceso abierto.'),
('A04', 'Amershi, S. et al.', 2019, 'Software Engineering for Machine Learning: A Case Study', 'IEEE/ACM ICSE-SEIP', 'Calidad de software', 'Ingeniería de sistemas con ML.', 'Estudio de caso.', 'MLOps, pruebas, pipelines ML', 'Describe prácticas y desafíos de ingeniería.', 'Sustenta pruebas, modularidad y monitoreo.', 'Calidad y pruebas de software', 'S. Amershi et al., Proc. ICSE-SEIP, 2019.', 'https://doi.org/10.1109/ICSE-SEIP.2019.00042', 'Prácticas de implementación.'),
('A05', 'Sculley, D. et al.', 2015, 'Hidden Technical Debt in Machine Learning Systems', 'Advances in Neural Information Processing Systems', 'Implementación', 'Deuda técnica en sistemas ML.', 'Análisis de patrones de riesgo.', 'ML systems, pipelines, monitoreo', 'Expone acoplamiento y deuda de datos.', 'Justifica auditoría y versionado.', 'Implementación del prototipo software', 'D. Sculley et al., Advances in NIPS 28, 2015.', 'https://papers.nips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems', 'Mantenimiento del prototipo.') ON CONFLICT DO NOTHING;
