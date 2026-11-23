import os 
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


load_dotenv()


def get_database_url() -> str:
    user = os.getenv("DB_USERNAME", "postgres")
    password = quote_plus(os.environ["DB_PASSWORD"]) 
    db_sslmode = os.getenv("DB_SSLMODE", "require") 
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    name = os.getenv("DB_NAME", "produtos_db")
    return f"postgresql+psycopg://{user}:{password}@{host}:{port}/{name}?sslmode={db_sslmode}"


engine = create_engine(get_database_url(), pool_pre_ping=True)
SessionLocal= sessionmaker(bind=engine, autoflush=False)
