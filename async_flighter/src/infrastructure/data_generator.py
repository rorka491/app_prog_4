import asyncio
import random
from datetime import date, datetime, time, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)

from src.core.settings import settings
from src.enums import Airport, Carriers
from src.models.sqlalchemy.flight import Flight


FLIGHTS_PER_DAY = 1500
DAYS_TO_GENERATE = 100


def generate_flight_data(
    departure_date: date,
    count: int = FLIGHTS_PER_DAY,
) -> list[dict]:
    flights: list[dict] = []

    for _ in range(count):
        origin, destination = random.sample(list(Airport), 2)

        departure_datetime = datetime.combine(
            departure_date,
            time.min,
        ) + timedelta(seconds=random.randint(0, 86399))

        duration = timedelta(minutes=random.randint(60, 360))
        arrival_datetime = departure_datetime + duration

        flights.append(
            {
                "carrier": random.choice(list(Carriers)),
                "flight_number": (
                    f"{random.choice(['SU', 'S7', 'U6', 'DP', 'UT'])}"
                    f"{random.randint(100, 9999)}"
                ),
                "origin": origin,
                "destination": destination,
                "departure_time": departure_datetime,
                "arrival_time": arrival_datetime,
                "price": random.randrange(3000, 30001, 100),
            }
        )

    return flights


async def execute() -> None:
    engine = create_async_engine(settings.POSTGRES_URL)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    try:
        async with session_factory() as session:
            has_flights = await session.scalar(
                select(select(Flight.id).exists())
            )

            if has_flights:
                return

            flights = [
                flight_data
                for day in range(DAYS_TO_GENERATE)
                for flight_data in generate_flight_data(
                    date.today() + timedelta(days=day)
                )
            ]

            session.add_all(
                Flight(**flight_data)
                for flight_data in flights
            )
            await session.commit()
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(execute())