from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

SQL_DB_URL = "postgresql+asyncpg://testuser:1234@localhost:5432/fastapi_proj"

engine = create_async_engine(SQL_DB_URL, echo=True)

asuncSessionLocal = sessionmaker(autoflush=False,
                          autocommit=False,
                          bind=engine,
                          class_=AsyncSession,
                          expire_on_commit=False)

Base = declarative_base()
