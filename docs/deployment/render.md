# Despliegue en Render

Esta guia deja el prototipo IDS-ML como un servicio web Docker en Render y una base PostgreSQL externa. Esta es la opcion mas practica si Render solicita pago al crear una base administrada propia.

Render mantiene instancia Free para servicios web, pero Render Postgres gratuito tiene limite temporal y los planes persistentes son de pago. Por eso el repositorio ya no crea una base PostgreSQL dentro de `render.yaml`; ahora el Blueprint pide `DATABASE_URL` como variable secreta.

Referencias oficiales:

- Precios de Render: https://render.com/pricing
- Servicios gratuitos en Render: https://render.com/docs/free
- Blueprints: https://render.com/docs/blueprint-spec
- Docker en Render: https://render.com/docs/docker

## Preparacion del repositorio

El proyecto ya incluye:

- `Dockerfile`: construye la aplicacion Streamlit.
- `render.yaml`: define solo el servicio web Docker.
- `scripts/start_render.sh`: inicializa la base y arranca Streamlit.
- `database/init_postgres.py`: crea el modelo PostgreSQL de 62 tablas y carga datos demo si la base esta vacia.
- `database/postgresql/schema.sql`: estructura relacional para produccion.
- `database/postgresql/seed_demo.sql`: datos demo para sustentacion.

## Opcion sin pago: Render + PostgreSQL externo

1. Crear una base PostgreSQL gratuita en un proveedor externo como Neon o Supabase.
2. Copiar la cadena de conexion PostgreSQL. Debe tener formato similar a:

```text
postgresql://usuario:password@host:5432/base?sslmode=require
```

3. Entrar a `https://dashboard.render.com`.
4. Seleccionar **New > Blueprint**.
5. Conectar el repositorio `DiegoA199/IDS_ML_Hospital_Carrion`.
6. Confirmar que Render detecte `render.yaml`.
7. Cuando Render solicite `DATABASE_URL`, pegar la cadena de conexion externa.
8. Crear el Blueprint.
9. Esperar a que termine el build y el primer deploy.

Render asignara una URL similar a:

```text
https://ids-ml-hospital-carrion.onrender.com
```

Durante el primer arranque, `scripts/start_render.sh` ejecuta `database/init_postgres.py`. Ese script crea las 62 tablas y carga datos demo si todavia no existen registros iniciales.

## Variables de entorno

El Blueprint configura:

| Variable | Valor | Uso |
|---|---|---|
| `IDSML_PERSISTENCE_BACKEND` | `postgres` | Fuerza uso de PostgreSQL. |
| `DATABASE_URL` | Se ingresa manualmente en Render | DSN usado por la capa repository. |
| `PYTHONUNBUFFERED` | `1` | Logs inmediatos en Render. |

No subir `.env`, `secrets.toml` ni JSON privados. Si se usa Firebase en otra etapa, cargar sus credenciales en Render como secretos, no en Git.

## Opcion manual

Si no se usa Blueprint:

1. Crear un servicio en **New > Web Service** desde GitHub.
2. Elegir runtime **Docker**.
3. Usar branch `main`.
4. Configurar el comando Docker:

```bash
/bin/sh scripts/start_render.sh
```

5. Configurar health check:

```text
/_stcore/health
```

6. Agregar variables:

```text
IDSML_PERSISTENCE_BACKEND=postgres
DATABASE_URL=<URL externa de PostgreSQL>
PYTHONUNBUFFERED=1
```

7. Crear el servicio y esperar el deploy.

## Si se desea usar Render Postgres

Tambien se puede usar una base administrada por Render, pero esa opcion puede pedir metodo de pago o pasar a plan pagado despues del periodo gratuito.

Pasos:

1. Crear una base en **New > Postgres**.
2. Copiar el valor **Internal Database URL** o **External Database URL**.
3. Pegar ese valor en `DATABASE_URL` del servicio web.
4. Ejecutar un nuevo deploy.

Esta opcion es valida para produccion si se acepta el costo del motor administrado.

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
5. Confirmar que no aparezcan errores de `DATABASE_URL`.

## Ver la base fisica

La base no se revisa dentro de Render si se usa Neon, Supabase u otro motor externo. Se revisa en el panel del proveedor o desde DBeaver/pgAdmin.

En DBeaver o pgAdmin:

1. Crear una nueva conexion PostgreSQL.
2. Pegar host, puerto, base, usuario y password desde la cadena `DATABASE_URL`.
3. Activar SSL si el proveedor lo solicita.
4. Probar conexion.
5. Abrir el esquema `public` y revisar las tablas.

Para revisar las tablas esperadas:

```sql
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;
```

El modelo formal debe mostrar 62 tablas academicas, ademas de tablas operativas internas si la aplicacion ya registro ejecuciones.

## Consideraciones de produccion

- Cambiar las credenciales demo antes de exponer el sistema fuera de una sustentacion.
- No publicar gestores como Adminer en Internet.
- Usar PostgreSQL para datos persistentes; SQLite no es recomendable en Render porque el filesystem del servicio web puede ser efimero.
- Los archivos subidos, modelos `joblib` y reportes generados dentro del contenedor pueden perderse en redeploys si no se configura disco persistente u object storage.
- Para tesis, Render + PostgreSQL externo es suficiente como prototipo demostrable; para uso institucional real faltaria IAM/LDAP/OAuth, hardening y monitoreo.
