import os

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.models.models import Base

# Obtener la URL de la base de datos
# Prioridad: ASYNC_DATABASE_URL > DATABASE_URL (transformada) > SQLite por defecto
async_database_url = os.getenv("ASYNC_DATABASE_URL")
if not async_database_url:
    database_url = os.getenv("DATABASE_URL")
    if database_url and database_url.startswith("postgres://"):
        # Transformar postgresql:// a postgresql+asyncpg:// para asyncpg
        async_database_url = database_url.replace("postgres://", "postgresql+asyncpg://", 1)
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
