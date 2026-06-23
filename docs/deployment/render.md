# Despliegue en Render

Esta guia deja el prototipo IDS-ML como un servicio web Docker con PostgreSQL administrado por Render. No se despliega Adminer en Internet; la base se revisa desde el panel de Render o desde DBeaver/pgAdmin usando la URL externa cuando sea necesario.

## Preparacion del repositorio

El proyecto ya incluye:

- `Dockerfile`: construye la aplicacion Streamlit.
- `render.yaml`: define el servicio web y la base PostgreSQL.
- `scripts/start_render.sh`: inicializa la base y arranca Streamlit.
- `database/init_postgres.py`: crea el modelo PostgreSQL de 60 tablas y carga datos demo si la base esta vacia.
- `database/postgresql/schema.sql`: estructura relacional para produccion.
- `database/postgresql/seed_demo.sql`: datos demo para sustentacion.

## Opcion recomendada: Blueprint

1. Subir los ultimos cambios a GitHub.
2. Entrar a `https://dashboard.render.com`.
3. Seleccionar **New > Blueprint**.
4. Conectar el repositorio `DiegoA199/IDS_ML_Hospital_Carrion`.
5. Confirmar que Render detecte `render.yaml`.
6. Revisar los recursos:
   - Web service: `ids-ml-hospital-carrion`.
   - PostgreSQL: `idsml-hospital-carrion-db`.
7. Crear el Blueprint.
8. Esperar a que termine el build y el primer deploy.

Render asignara una URL similar a:

```text
https://ids-ml-hospital-carrion.onrender.com
```

## Variables de entorno

El Blueprint configura:

| Variable | Valor | Uso |
|---|---|---|
| `IDSML_PERSISTENCE_BACKEND` | `postgres` | Fuerza uso de PostgreSQL. |
| `DATABASE_URL` | Conexion interna de Render PostgreSQL | DSN usado por la capa repository. |
| `PYTHONUNBUFFERED` | `1` | Logs inmediatos en Render. |

No subir `.env`, `secrets.toml` ni JSON privados. Si se usa Firebase en otra etapa, cargar sus credenciales en Render como secretos, no en Git.

## Opcion manual

Si no se usa Blueprint:

1. Crear una base en **New > Postgres**.
2. Crear un servicio en **New > Web Service** desde GitHub.
3. Elegir runtime **Docker**.
4. Usar branch `main`.
5. Configurar el comando Docker:

```bash
/bin/sh scripts/start_render.sh
```

6. Configurar health check:

```text
/_stcore/health
```

7. Agregar variables:

```text
IDSML_PERSISTENCE_BACKEND=postgres
DATABASE_URL=<Internal Database URL de Render PostgreSQL>
PYTHONUNBUFFERED=1
```

8. Crear el servicio y esperar el deploy.

## Verificacion posterior

1. Abrir la URL publica de Render.
2. Iniciar sesion con credenciales demo:

```text
admin / admin123
analista / analista123
invitado / invitado123
```

3. En el dashboard verificar que el motor indique `PostgreSQL`.
4. En Render, abrir el servicio web y revisar **Logs**.
5. En Render, abrir la base PostgreSQL y revisar **Info / Connect** para copiar la URL externa si se quiere conectar desde DBeaver o pgAdmin.

## Ver la base fisica

Desde Render:

1. Abrir la base `idsml-hospital-carrion-db`.
2. Entrar a **Connect**.
3. Copiar el comando `psql` o la **External Database URL**.
4. En DBeaver:
   - Nueva conexion.
   - PostgreSQL.
   - Pegar host, puerto, base, usuario y password desde Render.
   - Activar SSL si DBeaver lo solicita.
   - Probar conexion.

Para revisar las tablas esperadas:

```sql
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;
```

El modelo formal debe mostrar 60 tablas academicas, ademas de tablas operativas internas si la aplicacion ya registro ejecuciones.

## Consideraciones de produccion

- Cambiar las credenciales demo antes de exponer el sistema fuera de una sustentacion.
- No publicar gestores como Adminer en Internet.
- Usar PostgreSQL administrado para datos persistentes; SQLite no es recomendable en Render porque el filesystem del servicio web puede ser efimero.
- Los archivos subidos, modelos `joblib` y reportes generados dentro del contenedor pueden perderse en redeploys si no se configura disco persistente u object storage.
- Para tesis, el despliegue Render + PostgreSQL es suficiente como prototipo demostrable; para uso institucional real faltaria IAM/LDAP/OAuth, hardening y monitoreo.
