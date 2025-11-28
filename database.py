from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DATABASE_URL

# PostgreSQL connection engine for data pipeline
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def initDatabase():
    '''
    Initialize database by creating all tables defined in models
    '''
    Base.metadata.create_all(bind=engine)


def getSession():
    '''
    Get database session for queries. Returns active SQLAlchemy session.
    '''
    return SessionLocal()