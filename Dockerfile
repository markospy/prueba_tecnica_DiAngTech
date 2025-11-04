# Stage 1: Builder - Instalación de dependencias con uv
FROM python:3.12-slim AS builder

# Instalar uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Configurar variables de entorno para uv
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos de configuración de dependencias
COPY pyproject.toml uv.lock ./

# Instalar dependencias del proyecto
RUN uv sync --frozen --no-dev

# Stage 2: Runtime - Imagen final optimizada
FROM python:3.12-slim AS runtime

# Instalar solo uv runtime (más ligero)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Crear usuario no root para seguridad
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Configurar variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app"

# Crear directorio de trabajo
WORKDIR /app

# Copiar el entorno virtual desde el builder
COPY --from=builder /app/.venv /app/.venv

# Copiar código de la aplicación
COPY --chown=appuser:appuser . .

# Cambiar a usuario no root
USER appuser

# Exponer puerto
EXPOSE 10000

# Comando por defecto
CMD ["uv", "run", "uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "10000"]

