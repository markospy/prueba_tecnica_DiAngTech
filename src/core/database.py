import os

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.models.models import Base

# Obtener la URL de la base de datos
# Prioridad: ASYNC_DATABASE_URL > DATABASE_URL (transformada) > SQLite por defecto
async_database_url = os.getenv("ASYNC_DATABASE_URL")

# Si no hay ASYNC_DATABASE_URL, intentar con DATABASE_URL
if not async_database_url:
    async_database_url = os.getenv("DATABASE_URL")

# Transformar la URL al formato correcto para asyncpg si es necesario
if async_database_url:
    if async_database_url.startswith("postgresql://"):
        # Transformar postgresql:// a postgresql+asyncpg://
        async_database_url = async_database_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    elif async_database_url.startswith("postgres://"):
        # Transformar postgres:// a postgresql+asyncpg://
        async_database_url = async_database_url.replace("postgres://", "postgresql+asyncpg://", 1)
else:
    # Fallback a SQLite para desarrollo local
    async_database_url = "sqlite+aiosqlite:///database.sqlite3"

ASYNC_DATABASE_URL = async_database_url

async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=False)

AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def create_db_and_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session():
    async with AsyncSessionLocal() as session:
        yield session
