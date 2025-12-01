from dotenv import load_dotenv
import os

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