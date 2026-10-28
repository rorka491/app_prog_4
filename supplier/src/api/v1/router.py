from fastapi import APIRouter
from src.api.v1.flight import router as flight_router

router = APIRouter(prefix="/api/v1")
router.include_router(flight_router)

@router.get("/health")
async def health():
    return {"status": "ok"}