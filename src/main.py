from fastapi import FastAPI
from src.routers import admin_routers, user_routers
from src.config import settings
from contextlib import asynccontextmanager

from src.database import engine
from src.models import Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(admin_routers.admin_router)
app.include_router(user_routers.router)

@app.get("/", tags=["Health Check"])
def health_check():
    return {"status": "healthy", "project": settings.PROJECT_NAME}
