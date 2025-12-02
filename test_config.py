import pytest
import os
import json
import tempfile
import yaml
from config import validateConfig, loadConfigFile, mergeConfigs


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


def test_loadConfigFileYAML():
    '''
    Test loading YAML configuration file
    '''
    config_data = {
        "DATABASE_URL": "postgresql://user:pass@localhost/db",
        "API_PORT": 8000,
        "DEBUG": False
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        yaml.dump(config_data, f)
        temp_file = f.name
    
    try:
        loaded = loadConfigFile(temp_file)
        assert loaded["DATABASE_URL"] == "postgresql://user:pass@localhost/db"
        assert loaded["API_PORT"] == 8000
    finally:
        os.unlink(temp_file)


def test_loadConfigFileJSON():
    '''
    Test loading JSON configuration file
    '''
    config_data = {
        "DATABASE_URL": "postgresql://user:pass@localhost/db",
        "API_HOST": "127.0.0.1"
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(config_data, f)
        temp_file = f.name
    
    try:
        loaded = loadConfigFile(temp_file)
        assert loaded["DATABASE_URL"] == "postgresql://user:pass@localhost/db"
        assert loaded["API_HOST"] == "127.0.0.1"
    finally:
        os.unlink(temp_file)


def test_loadConfigFileNotFound():
    '''
    Test loading non-existent config file raises error
    '''
    with pytest.raises(FileNotFoundError):
        loadConfigFile("/nonexistent/path/config.yaml")


def test_mergeConfigs():
    '''
    Test merging file config with environment variables, env vars take precedence
    '''
    file_config = {
        "DATABASE_URL": "postgresql://file:file@localhost/db",
        "API_PORT": 9000
    }
    
    os.environ["DATABASE_URL"] = "postgresql://env:env@localhost/db"
    
    merged = mergeConfigs(file_config)
    assert merged["DATABASE_URL"] == "postgresql://env:env@localhost/db"
    assert merged["API_PORT"] == 9000
    
    del os.environ["DATABASE_URL"]