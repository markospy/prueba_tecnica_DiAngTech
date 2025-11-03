Durante el desarrollo trabajé en un entorno local, prescindí Docker. Así que  la configuracion de desarrollo es para despliegue del entorno local sin usar docker.

Para el despliegue si use docker y también explicó los pasos que seguí.

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