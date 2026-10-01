from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import router
from app.database.database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Smart Support",
    description="MVP automation for customer support requests.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "smart-support"}
