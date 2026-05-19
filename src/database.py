from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.config import DB_SERVER, DB_PORT, DB_NAME, DB_USERNAME, DB_PASSWORD, DB_DRIVER
from src.logger import setup_logger

logger = setup_logger(__name__)

def get_db_session() -> Session:
    password = quote_plus(DB_PASSWORD)

    connection_string = (
        f"mssql+pyodbc://{DB_USERNAME}:{password}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"
        f"?driver={DB_DRIVER}"
    )

    try:
        engine = create_engine(connection_string)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = SessionLocal()
        logger.info("Database connection established")
        return session
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        raise
