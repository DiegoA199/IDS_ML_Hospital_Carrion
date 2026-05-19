# Casos de prueba IDS-ML

Los siguientes casos desarrollan la matriz principal del plan de pruebas. Deben ejecutarse con datos demo y evidencias controladas.

| ID | Módulo | Tipo | Caso de prueba | Resultado esperado |
|---|---|---|---|---|
| CP-001 | Autenticación | Unitaria | Autenticar usuario `admin` con contraseña demo válida. | Devuelve usuario activo con rol Administrador TI. |
| CP-002 | Autenticación | Unitaria | Autenticar usuario válido con contraseña incorrecta. | La autenticación devuelve `None`. |
| CP-003 | RBAC | Unitaria | Validar permiso de entrenamiento para Analista TI. | Permiso concedido. |
| CP-004 | RBAC | Unitaria | Validar permiso de entrenamiento para Invitado/demo. | Permiso denegado. |
| CP-005 | Dataset | Unitaria | Validar DataFrame vacío. | Error controlado de validación. |
| CP-006 | Dataset | Unitaria | Validar columnas requeridas faltantes. | Se reportan columnas faltantes. |
| CP-007 | Dataset | Unitaria | Perfilar dataset con valores nulos. | Conteo de nulos correcto. |
| CP-008 | Dataset | Unitaria | Perfilar dataset con duplicados. | Conteo de duplicados correcto. |
| CP-009 | Calidad | Unitaria | Calcular score de calidad desde perfil. | Score entre 0 y 100. |
| CP-010 | Preprocesamiento | Integración | Ejecutar pipeline con columnas numéricas y categóricas. | Matrices train/test generadas. |
| CP-011 | Preprocesamiento | Integración | Codificar variables categóricas. | Salida transformada numérica. |
| CP-012 | Preprocesamiento | Integración | Verificar partición train/test. | Tamaños coherentes sin fuga. |
| CP-013 | ML | Unitaria | Calcular métricas de clasificación. | Accuracy, precision, recall y F1 en rango válido. |
| CP-014 | ML | Unitaria | Seleccionar mejor modelo por F1-score. | Modelo con mayor F1 seleccionado. |
| CP-015 | ML | Integración | Entrenar Random Forest. | Resultado disponible en tabla comparativa. |
| CP-016 | ML | Integración | Entrenar SVM. | Resultado SVM calculado. |
| CP-017 | ML | Integración | Entrenar Naive Bayes. | Resultado Naive Bayes calculado. |
| CP-018 | Predicción | Integración | Guardar y cargar bundle `.joblib`. | Bundle recuperado con metadatos. |
| CP-019 | Predicción | Integración | Predecir tráfico nuevo. | DataFrame con `prediccion_etiqueta`. |
| CP-020 | Alertas | Unitaria | Etiqueta `normal`. | Severidad baja. |
| CP-021 | Alertas | Unitaria | Etiqueta `DDoS`. | Severidad alta. |
| CP-022 | Alertas | Integración | Convertir predicciones en alertas. | Lista de alertas persistibles. |
| CP-023 | SQLite | Integración | Inicializar esquema relacional. | 60 tablas creadas. |
| CP-024 | SQLite | Integración | Insertar seed demo. | Roles, usuarios y catálogos básicos cargados. |
| CP-025 | Repository | Integración | Guardar/listar alerta en SQLite. | Alerta recuperada. |
| CP-026 | Reportes | Integración | Generar reporte CSV. | Archivo creado y registro persistido. |
| CP-027 | Reportes | Integración | Generar reporte PDF. | Archivo creado o fallo controlado si falta dependencia. |
| CP-028 | UI | Funcional | Abrir login Streamlit. | Pantalla institucional visible. |
| CP-029 | UI | Funcional | Iniciar sesión y abrir dashboard. | KPIs y navegación lateral visibles. |
| CP-030 | Seguridad | Revisión | Revisar `.gitignore`. | Secrets, `.env`, JSON privados y coverage ignorados. |

