from datetime import date
from src.schemas.flight import FlightSchema
import requests

class FlightClient: 
    def __init__(self, timeout: float = 2.0) -> None:
        self.timeout = timeout

    def get_flights(
        self,
        departure_date: date,
        url: str,
    ) -> list[FlightSchema]:
        response = requests.get(
            url=url,
            params={"date": departure_date.isoformat()},
            timeout=self.timeout,
        )
        response.raise_for_status()
        return [
            FlightSchema.model_validate(flight)
            for flight in response.json()
        ]