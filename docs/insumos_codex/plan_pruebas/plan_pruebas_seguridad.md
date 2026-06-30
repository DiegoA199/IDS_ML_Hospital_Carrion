# Pruebas de seguridad

## Objetivo

Verificar controles básicos de acceso, manejo de entradas y protección de información.

## Alcance recomendado

- Rechazo de credenciales inválidas y aplicación de RBAC.
- Restricción de entrenamiento, alertas y configuración por rol.
- Validación de archivos y entradas malformadas.
- Ausencia de secretos y datos sensibles en repositorio, interfaz y reportes.
- Consultas parametrizadas y manejo controlado de errores de persistencia.

## Criterio de aceptación

Las acciones no autorizadas deben bloquearse sin revelar detalles internos. Toda prueba debe utilizar cuentas demo y datos sintéticos.
