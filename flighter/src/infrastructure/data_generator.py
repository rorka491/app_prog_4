import random
from datetime import date, datetime, time, timedelta
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from src.core.settings import settings
from src.models.sqlalchemy.flight import Flight
from src.enums import Airport, Carriers



FLIGHTS_PER_DAY = 1500

MIN_FLIGHT_DURATION = timedelta(hours=1)
MAX_FLIGHT_DURATION = timedelta(hours=6)


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
        ) + timedelta(
            seconds=random.randint(0, 86399),
        )

        duration = timedelta(
            minutes=random.randint(60, 360),
        )

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


def execute() -> None:
    engine = create_engine(settings.POSTGRES_URL)
    flights = []
    dates = [
        date.today() + timedelta(days=day)
        for day in range(100)
    ]
    for departure_date in dates:
        flights.extend(generate_flight_data(departure_date))

    with Session(engine) as session:
        has_flights = session.scalar(
            select(select(Flight).exists())
        )
        if not has_flights:
            session.add_all(
                Flight(**flight_data)
                for flight_data in flights
            )
            session.commit()

