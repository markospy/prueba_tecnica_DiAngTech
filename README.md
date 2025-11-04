Durante el desarrollo trabajé en un entorno local, por lo que la configuracion de desarrollo es para despliegue del entorno local sin usar docker.

Para el despliegue si use docker, explicó los pasos que seguí.

## ✅ CHECKLIST FINAL

### Requisitos Obligatorios
- ✅ Entidad principal (User) + 2 secundarias (Post, Comment)
- ✅ Relación uno a muchos (User → Post, Post → Comment)
- ✅ Relación muchos a muchos (Post ↔ Tag)
- ✅ Migraciones incrementales con Alembic
- ✅ Operaciones asíncronas con AsyncSession
- ✅ Soft-delete con mixin
- ✅ Query personalizado filtrando deleted
- ✅ Timestamps genéricos (created_at, updated_at)
- ✅ OAuth2 + JWT
- ✅ Endpoints protegidos
- ✅ Registro + Login
- ✅ Routers separados por entidad
- ✅ Middleware de tiempo de respuesta

### Extras Opcionales
- ✅ Paginación (offset/limit)
- ✅ Validaciones Pydantic (EmailStr + validators)
- ✅ Docker (multi-stage, optimizado)
- ✅ Sistema de permisos (owner-only)
- ✅ DECISIONS.md profesional

### Pendientes y mejoras posibles
- Actualizar tests unitarios y de integracion.
- Crear tests de extremo a extremo para probar endpoints.

## Preparar entorno virtual con uv (en linux) para desarrollo (sin docker):

```shell
# Instalar uv si no lo tienes (macOS/Linux)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 1. Crear el entorno virtual (si no existe)
uv venv

# 2. Sincronizar (instala las dependencias de pyproject.toml)
uv sync

# Activar el entorno virtual
source .venv/bin/activate

## Declaracion de variables de entorno
export ASYNC_DATABASE_URL="sqlite+aiosqlite:///database.sqlite3"
export SECRET_KEY="0aa70dd7899111cd13c90ee18ac26318241c9457a14d1cef7e302abe4c259b99"
export ALGORITHM="HS256"
export ACCESS_TOKEN_EXPIRE_MINUTES=25200

fastapi dev  src/api/main.py
```

## Desplegar API desde un contenedor de Docker

```shell
export POSTGRES_USER="miusuario"
export POSTGRES_PASSWORD="miclave"
export POSTGRES_DB="midb"
export ASYNC_DATABASE_URL="postgresql+asyncpg://miusuario:miclave@db:5432/midb"
export SECRET_KEY="0aa70dd7899111cd13c90ee18ac26318241c9457a14d1cef7e302abe4c259b99"
export ALGORITHM="HS256"
export ACCESS_TOKEN_EXPIRE_MINUTES=25200

docker compose up
```

## 📊 Decisiones Técnicas

Para entender el razonamiento detrás de las decisiones arquitectónicas
y técnicas tomadas durante el desarrollo, consulta [DECISIONS.md](./DECISIONS.md)