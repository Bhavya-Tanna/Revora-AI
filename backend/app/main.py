from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends

from app.api.revenue import router as revenue_router
from app.core.database import Base, engine, get_db
from app.models import Merchant
from app.api.agent import router as agent_router

from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Revora AI API",
    description="AI-powered merchant growth and agentic commerce platform.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(revenue_router)
app.include_router(agent_router)

@app.get("/")
def root():
    return {
        "name": "Revora AI",
        "status": "running",
        "version": "0.1.0",
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/merchants")
def get_merchants(db=Depends(get_db)):
    from app.api.revenue import list_merchants
    return list_merchants(db=db)