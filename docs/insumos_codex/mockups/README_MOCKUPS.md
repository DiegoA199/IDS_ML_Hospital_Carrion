# Mockups de Stitch

Los archivos de esta carpeta son insumos visuales generados con Stitch y exportados como imágenes PNG. Sirven para orientar la composición, jerarquía, navegación y presentación de información de las pantallas reales del IDS-ML.

## Alcance

- Son referencias de diseño y no implementaciones funcionales.
- No forman parte de un módulo visible dentro de la aplicación.
- No deben mostrarse como galería en el sistema desplegado.
- Los cambios reales de interfaz deben conservar reglas de negocio, permisos, persistencia y accesibilidad existentes.

## Organización

- `imagenes/`: copia documental de las diez pantallas normalizadas.
- `evidencias/`: comparaciones o capturas futuras de la implementación frente al mockup.
- `matriz_mockups.csv`: trazabilidad entre pantalla, requisito y dimensión de tesis.

Existe una segunda copia en `assets/mockups/` para que las herramientas de desarrollo puedan consultar los recursos sin depender de la ruta documental.
