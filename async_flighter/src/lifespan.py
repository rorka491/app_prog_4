from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.infrastructure.data_generator import execute


@asynccontextmanager
async def lifespan(app: FastAPI):
    await execute()
    yield