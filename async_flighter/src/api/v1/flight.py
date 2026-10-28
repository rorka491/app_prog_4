import asyncio
from datetime import date
import random
from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Query
from src.schemas.flight import FlightSchema
from src.services.flight import FlightService
from src.core.settings import settings

router = APIRouter(prefix="/flights")


@router.get("/search")
@inject
async def search(
    service: FromDishka[FlightService],
    origin: str = Query(...),
    destination: str = Query(...),
    date: date = Query(...),
):
    return await service.get_flights(
        origin=origin,
        destination=destination,
        departure_date=date,
    )
    



