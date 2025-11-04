# Stage 1: Builder - Instalación de dependencias
FROM python:3.12-slim AS builder

WORKDIR /code

# Copiar archivos de configuración de dependencias
COPY pyproject.toml /code/

# Crear venv e instalar dependencias
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir --upgrade pip && \
    /opt/venv/bin/pip install --no-cache-dir .

# Stage 2: Runtime - Imagen final optimizada
FROM python:3.12-slim AS runtime

WORKDIR /code

# Copiar el venv desde el builder
COPY --from=builder /opt/venv /opt/venv

# Configurar variables de entorno
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Copiar código de la aplicación
COPY . /code/

# Exponer puerto
EXPOSE 10000

# Comando por defecto
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
