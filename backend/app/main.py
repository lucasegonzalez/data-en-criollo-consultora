from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.config import settings
from app.routes import clients, contracts, meetings, tasks
from app.schemas import HealthResponse

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Consultora API",
    description="Backend para Data en Criollo Consultoría",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(clients.router, prefix="/api/v1/clients", tags=["Clients"])
app.include_router(contracts.router, prefix="/api/v1/contracts", tags=["Contracts"])
app.include_router(meetings.router, prefix="/api/v1/meetings", tags=["Meetings"])
app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["Tasks"])

@app.get("/api/v1/health", response_model=HealthResponse, tags=["Health"])
def health():
    return HealthResponse()
