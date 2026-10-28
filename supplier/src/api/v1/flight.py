import asyncio
from datetime import date
import random

from fastapi import APIRouter, HTTPException, Query
from src.data_generator import generate_flights
from src.core.config import settings
from src.schemas.flight import FlightSchema

router = APIRouter(prefix="/flights")


@router.get("")
async def get_flights(
    date: date = Query(...),
) -> list[FlightSchema]:
    if random.random() < 0.05:
        raise HTTPException(
            status_code=500,
            detail="Internal error",
        ) 
    if settings.IS_ON_3_SECOND_DELAY:
        target = random.random() < 0.1
        if target:
            await asyncio.sleep(3)
    else:
        await asyncio.sleep(
            random.uniform(
                settings.REQUEST_MIN_DELAY / 1000,
                settings.REQUEST_MAX_DELAY / 1000,
            )
        )
    return generate_flights(
        departure_date=date,
        supplier_id=settings.SUPLIER_ID
    )
