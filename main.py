from fastapi import FastAPI
from contextlib import asynccontextmanager

app = FastAPI(title="Data Pipeline API", version="1.0.0")


@app.get("/health")
def checkHealth():
    '''
    Health check endpoint that returns API status
    '''
    return {"status": "healthy", "service": "data-pipeline"}


if __name__ == "__main__":
    import uvicorn
    from dotenv import load_dotenv
    import os
    
    load_dotenv()
    
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 8000))
    
    uvicorn.run(app, host=host, port=port)