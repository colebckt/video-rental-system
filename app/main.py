from fastapi import FastAPI
from app.routes.reports import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Analytics Service",
    version="1.0.0"
)

app.include_router(router)

@app.get("/")
def root():
    return {
        "service": "Analytics Service",
        "status": "running"
    }
    
@app.get("/health")
def health():
    return {
        "status": "UP",
        "service": "analytics-service"
    }

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# activate: .\venv\Scripts\Activate.ps1
# start: uvicorn app.main:app --reload --port 8006