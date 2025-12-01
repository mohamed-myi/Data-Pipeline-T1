from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import initDatabase
from config import validateConfig, ENVIRONMENT

@asynccontextmanager
async def lifespan(app: FastAPI):
    '''
    Startup and shutdown event handler for FastAPI application
    '''
    try:
        validateConfig()
        initDatabase()
        print(f"Database initialized (Environment: {ENVIRONMENT})")
    except ValueError as e:
        print(f"Configuration error: {e}")
        raise
    
    yield
    print("Application shutdown")


app = FastAPI(title="Data Pipeline API", version="1.0.0", lifespan=lifespan)


@app.get("/health")
def checkHealth():
    '''
    Health check endpoint that returns API status
    '''
    return {"status": "healthy", "service": "data-pipeline"}


if __name__ == "__main__":
    import uvicorn
    from config import API_HOST, API_PORT
    
    uvicorn.run(app, host=API_HOST, port=API_PORT)