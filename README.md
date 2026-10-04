# Broker API

Servidor backend desarrollado con **FastAPI** para registrar y consultar datos de
geolocalización de dispositivos. La información se almacena en **PostgreSQL** y
la evolución del esquema se gestiona con **Alembic**.

## Características

- Registro de coordenadas, altitud y fecha/hora por dispositivo.
- Consulta de todas las ubicaciones de un dispositivo, con filtros opcionales
  por fecha y límite de resultados.
- Consulta de la última ubicación conocida de un dispositivo.
- Listado de los identificadores de dispositivos con datos registrados.
- Rutas de health check para comprobar el estado de la aplicación y de la base
  de datos.
- Documentación interactiva generada por FastAPI.

## Requisitos

- Python 3.13 o superior.
- [Poetry](https://python-poetry.org/).
- Docker, para ejecutar PostgreSQL localmente.

## Setup inicial

### 1. Instalar las dependencias

Desde la raíz del proyecto:

```bash
poetry install
```

Poetry creará o utilizará el entorno virtual del proyecto e instalará FastAPI,
SQLAlchemy, Alembic, el driver de PostgreSQL y Uvicorn, entre otras dependencias.

### 2. Iniciar PostgreSQL

El siguiente comando crea una base de datos PostgreSQL 16 llamada `geodb` y la
expone en el puerto `5432`:

```bash
docker run --name geo-db \
  -e POSTGRES_PASSWORD=pass \
  -e POSTGRES_DB=geodb \
  -p 5432:5432 \
  -d postgres:16
```

Si el contenedor ya existe pero está detenido, puede iniciarse nuevamente con:

```bash
docker start geo-db
```

### 3. Configurar las variables de conexión

La aplicación carga el archivo `.env` desde la raíz del proyecto. Para la base
de datos creada en el paso anterior, el archivo debe contener:

```dotenv
postgres_user=postgres
postgres_pass=pass
postgres_port=5432
postgres_db=geodb
```

La URL utilizada por SQLAlchemy se construye con estos valores y tiene el
formato:

```text
postgresql://postgres:pass@localhost:5432/geodb
```

No se deben subir credenciales reales al repositorio. En entornos compartidos o
de producción, utilice valores seguros y gestione el archivo `.env` como secreto.

### 4. Crear o actualizar las tablas

El repositorio ya contiene el directorio `migrations/` y sus migraciones. Para
crear todas las tablas pendientes en una base de datos nueva, ejecute:

```bash
poetry run alembic upgrade head
```

### 5. Ejecutar el backend

```bash
poetry run uvicorn --host 0.0.0.0 --port 8000 broker_api.main:app --reload
```

La API estará disponible en `http://localhost:8000`.

## Alembic y migraciones

Alembic mantiene el historial versionado del esquema de PostgreSQL en
`migrations/versions/`. El flujo habitual es:

1. Modificar el modelo SQLAlchemy en `src/broker_api/models.py`.
2. Generar una migración a partir de la diferencia entre los modelos y la base
   de datos:

   ```bash
   poetry run alembic revision --autogenerate -m "descripcion del cambio"
   ```

3. Revisar y, si es necesario, ajustar el archivo generado en
   `migrations/versions/`.
4. Aplicar la migración:

   ```bash
   poetry run alembic upgrade head
   ```

Comandos útiles:

```bash
# Ver la revisión actual de la base de datos
poetry run alembic current

# Ver el historial de revisiones
poetry run alembic history

# Aplicar solo la siguiente migración
poetry run alembic upgrade +1

# Volver una migración atrás (usar con precaución)
poetry run alembic downgrade -1
```

`alembic init` solo es necesario al crear un proyecto nuevo desde cero. No debe
ejecutarse como parte del setup normal de este repositorio, porque la
configuración y las migraciones ya existen:

```bash
poetry run alembic init migrations
```

## Endpoints principales

### Health checks

```http
GET /health
```

Comprueba que la aplicación está levantada:

```json
{"status": "ok"}
```

```http
GET /health/db
```

Comprueba además la conexión ejecutando `SELECT 1` en PostgreSQL. Devuelve
`200` cuando la base de datos está disponible y `503` con
`{"detail": "database unavailable"}` cuando no lo está.

### Registrar una ubicación

```http
POST /geolocation/create
Content-Type: application/json
```

Ejemplo de solicitud:

```json
{
  "device_id": "collar-001",
  "latitude": 4.711,
  "longitude": -74.072,
  "altitude": 2600,
  "timestamp": "2026-10-04T20:15:00Z"
}
```

`timestamp` es opcional; si se omite, se utiliza la fecha y hora UTC actuales.
La respuesta exitosa tiene código `201` e incluye el identificador generado:

```json
{"id": "uuid-generado"}
```

### Consultar ubicaciones de un dispositivo

```http
GET /devices/{device_id}/locations
```

Parámetros opcionales:

- `start`: fecha/hora mínima, por ejemplo `2026-10-01T00:00:00Z`.
- `end`: fecha/hora máxima.
- `limit`: cantidad máxima de resultados; por defecto `100`, máximo `1000`.

Los resultados se ordenan de la ubicación más reciente a la más antigua.

```http
GET /devices/collar-001/latest
```

Devuelve la última ubicación registrada para el dispositivo. Si no existe
información, la API responde `404`.

```http
GET /devices/ids
```

Devuelve la lista de identificadores de dispositivos que tienen ubicaciones
registradas.

## Documentación interactiva

Con el servidor ejecutándose, FastAPI expone:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- Esquema OpenAPI: `http://localhost:8000/openapi.json`

## Estructura relevante

```text
src/broker_api/
├── main.py                 # Creación de la aplicación FastAPI y routers
├── config.py               # Configuración de la conexión a PostgreSQL
├── db.py                   # Motor, sesiones y dependencia de base de datos
├── models.py               # Modelos SQLAlchemy
├── schemas.py              # Esquemas de entrada y salida
└── routes/
    ├── devices.py          # Consultas por dispositivo
    ├── geolocation.py      # Registro de ubicaciones
    └── health.py           # Health checks
migrations/                 # Configuración y versiones de Alembic
```

## Detener el entorno local

Para detener PostgreSQL sin eliminar sus datos:

```bash
docker stop geo-db
```

Para eliminar el contenedor (los datos almacenados dentro del contenedor se
perderán si no se utiliza un volumen):

```bash
docker rm geo-db
```