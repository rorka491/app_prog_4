from datetime import date
import httpx
from src.schemas.flight import FlightSchema


class FlightClient:
    def __init__(self, timeout: float = 2.0) -> None:
        self.timeout = timeout

    async def get_flights(
        self,
        departure_date: date,
        url: str,
    ) -> list[FlightSchema]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                url=url,
                params={"date": departure_date.isoformat()},
            )

        response.raise_for_status()

        return [
            FlightSchema.model_validate(flight)
            for flight in response.json()
        ]