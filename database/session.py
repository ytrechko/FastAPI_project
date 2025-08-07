from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import settings

engine = create_async_engine(settings.sql_db_url, echo=True)

asyncSessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()


async def get_db():
    async with asyncSessionLocal() as session:
        yield session
