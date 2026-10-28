from datetime import date, datetime, time, timedelta
import hashlib
import random
from src.schemas.flight import FlightSchema
from src.enums import Airport


def generate_flights(
    departure_date: date,
    supplier_id: str,
    count: int = 500,
) -> list[FlightSchema]:
    seed = int.from_bytes(
        hashlib.sha256(
            f"{supplier_id}:{departure_date.isoformat()}".encode()
        ).digest()[:8],
        byteorder="big",
    )
    rng = random.Random(seed)
    airports = list(Airport)
    flights: list[FlightSchema] = []

    for index in range(count):
        origin, destination = rng.sample(airports, 2)

        departure_time = datetime.combine(
            departure_date,
            time.min,
        ) + timedelta(minutes=rng.randint(0, 1439))

        duration = timedelta(minutes=rng.randint(60, 360))
        arrival_time = departure_time + duration

        flights.append(
            FlightSchema(
                carrier=supplier_id,
                flight_number=f"{supplier_id.upper()}-{index + 1:04d}",
                origin=origin,
                destination=destination,
                departure_time=departure_time,
                arrival_time=arrival_time,
                price=rng.randint(3000, 30000),
            )
        )

    return flights

