from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from models.models import Base

ASYNC_DATABASE_URL = "sqlite+aiosqlite:///database.sqlite3"

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
