import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from models import DataSource


# In-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def test_initDatabase():
    '''
    Test database initialization creates tables
    '''
    session = TestingSessionLocal()
    
    # Create test data source
    test_source = DataSource(name="test_api", source_type="api", endpoint="https://api.example.com")
    session.add(test_source)
    session.commit()
    
    # Verify it was created
    result = session.query(DataSource).filter(DataSource.name == "test_api").first()
    assert result is not None
    assert result.source_type == "api"
    
    session.close()