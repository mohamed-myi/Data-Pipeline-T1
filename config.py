from dotenv import load_dotenv
import os

load_dotenv()

# Database connection string for PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost/data_pipeline")

# API configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))
DEBUG = os.getenv("DEBUG", "False").lower() == "true"