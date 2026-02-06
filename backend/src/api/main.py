import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.middleware.logging_middleware import LoggingMiddleware
from api.routers import goals_router

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title="Chimera API", version="0.1.0", lifespan=lifespan)
app.add_middleware(LoggingMiddleware)
app.include_router(goals_router, prefix="/api/v1")


def run() -> None:
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
