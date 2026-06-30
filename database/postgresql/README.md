# PostgreSQL para IDS-ML

Este directorio contiene la versión PostgreSQL del modelo relacional académico de 62 tablas.

## Archivos

- `schema.sql`: estructura formal compatible con PostgreSQL.
- `seed_demo.sql`: datos demo no sensibles.

## Uso con Docker Compose

Desde la raíz del proyecto:

```powershell
copy .env.example .env
docker compose up --build
```

Servicios:

- Streamlit: `http://localhost:8501`
- Adminer: `http://localhost:8080`
- PostgreSQL: puerto `5432`

Credenciales por defecto de desarrollo:

- Sistema: `PostgreSQL`
- Servidor: `db`
- Usuario: valor de `POSTGRES_USER`
- Contraseña: valor de `POSTGRES_PASSWORD`
- Base de datos: valor de `POSTGRES_DB`

En producción, cambie `POSTGRES_PASSWORD` en `.env` o en el gestor de secretos del proveedor.

