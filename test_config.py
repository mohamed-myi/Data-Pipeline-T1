import pytest
import os
from config import validateConfig


def test_validateConfig():
    '''
    Test configuration validation with required DATABASE_URL set
    '''
    os.environ["DATABASE_URL"] = "postgresql://test:test@localhost/test_db"
    assert validateConfig() == True


def test_validateConfigMissing():
    '''
    Test configuration validation raises error when DATABASE_URL missing
    '''
    original_db_url = os.environ.get("DATABASE_URL")
    
    if "DATABASE_URL" in os.environ:
        del os.environ["DATABASE_URL"]
    
    with pytest.raises(ValueError, match="Missing required configuration variables"):
        validateConfig()
    
    if original_db_url:
        os.environ["DATABASE_URL"] = original_db_url