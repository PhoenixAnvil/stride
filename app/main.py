from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db import Base, engine
from app.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Stride",
    description="A Python FastAPI to manage Agile iterations (sprints)",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(router)
