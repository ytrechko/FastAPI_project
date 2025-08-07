from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    sql_db_url: str = os.getenv("SQL_DB_URL")


settings = Settings()
