from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1.health import router as health_router
from api.v1.business_plan import router as business_plan_router
from api.v1.loan import router as loan_router
from api.v1.pdf import router as pdf_router
from api.v1.tax import router as tax_router
from api.v1.copilot import router as copilot_router
from database import engine
from models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create local SQLite tables on application startup."""
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="AI FinAdvisor", version="2.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:4173",
        "http://127.0.0.1:4173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api/v1")
app.include_router(business_plan_router, prefix="/api/v1")
app.include_router(loan_router, prefix="/api/v1")
app.include_router(pdf_router, prefix="/api/v1")
app.include_router(tax_router, prefix="/api/v1")
app.include_router(copilot_router, prefix="/api/v1")
