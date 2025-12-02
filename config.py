import os
from dotenv import load_dotenv
import json
import yaml

load_dotenv()

# Database connection string for PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost/data_pipeline")

# API configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Environment and logging configuration
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")  # development, testing, production
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


def loadConfigFile(file_path):
    '''
    Load configuration from YAML or JSON file. Returns dict with config values.
    '''
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Config file not found: {file_path}")
    
    file_ext = os.path.splitext(file_path)[1].lower()
    
    try:
        if file_ext == ".yaml" or file_ext == ".yml":
            with open(file_path, 'r') as f:
                config = yaml.safe_load(f) or {}
        elif file_ext == ".json":
            with open(file_path, 'r') as f:
                config = json.load(f)
        else:
            raise ValueError(f"Unsupported config file format: {file_ext}")
        
        # Returns loaded configuration dictionary
        return config
    except Exception as e:
        raise ValueError(f"Error parsing config file {file_path}: {e}")


def mergeConfigs(file_config):
    '''
    Merge file-based config with environment variables. Environment variables take precedence. Returns merged config dict.
    '''
    merged = file_config.copy() if file_config else {}
    
    # Environment variables override file config
    env_vars = {
        "DATABASE_URL": os.getenv("DATABASE_URL"),
        "API_HOST": os.getenv("API_HOST"),
        "API_PORT": os.getenv("API_PORT"),
        "DEBUG": os.getenv("DEBUG"),
        "ENVIRONMENT": os.getenv("ENVIRONMENT"),
        "LOG_LEVEL": os.getenv("LOG_LEVEL")
    }
    
    for key, value in env_vars.items():
        if value is not None:
            merged[key] = value
    
    # Returns merged configuration with env vars taking precedence
    return merged


def validateConfig():
    '''
    Validate required configuration variables are set. Returns True if all required configs present, raises exception otherwise.
    '''
    required_vars = ["DATABASE_URL"]
    missing = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)
    
    if missing:
        raise ValueError(f"Missing required configuration variables: {', '.join(missing)}")
    
    return True