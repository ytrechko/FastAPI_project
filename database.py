from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQL_DB_URL = "postgresql+psycopg2://testuser:1234@localhost:5432/fastapi_proj"

engine = create_engine(SQL_DB_URL)

db_session = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()
