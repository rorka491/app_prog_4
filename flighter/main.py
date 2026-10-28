import logging
import time
from fastapi import FastAPI, Request
from dishka.integrations.fastapi import setup_dishka
from src.di.container import container
from src.api.v1.router import router
from src.lifespan import lifespan

logger = logging.getLogger(__name__)

app = FastAPI(lifespan=lifespan)
app.include_router(router)
setup_dishka(container=container, app=app)


@app.middleware("http")
async def log_request_duration(request: Request, call_next):
    started_at = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - started_at) * 1000
    print(
        f"{request.method} {request.url.path} "
        f"{response.status_code} {duration_ms:.2f} ms",
        flush=True,

    )

    return response