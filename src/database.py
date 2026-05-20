from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.config import DB_SERVER, DB_PORT, DB_NAME, DB_USERNAME, DB_PASSWORD, DB_DRIVER
from src.logger import setup_logger

logger = setup_logger(__name__)

from sqlalchemy import URL

def get_db_session() -> Session:
    if DB_PASSWORD is None or DB_DRIVER is None:
        raise ValueError("Database credentials missing. Please check your .env file.")

    # Fix driver name formatting (replace + with space if present)
    driver_name = DB_DRIVER.replace("+", " ")

    connection_url = URL.create(
        "mssql+pyodbc",
        username=DB_USERNAME,
        password=DB_PASSWORD,
        host=DB_SERVER,
        port=int(DB_PORT) if DB_PORT else 1433,
        database=DB_NAME,
        query={"driver": driver_name}
    )

    try:
        engine = create_engine(connection_url)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = SessionLocal()
        logger.info("Database connection established")
        return session
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        raise
