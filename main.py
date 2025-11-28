from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import initDatabase

@asynccontextmanager
async def lifespan(app: FastAPI):
    '''
    Startup and shutdown event handler for FastAPI application
    '''
    initDatabase()
    print("Database initialized")
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