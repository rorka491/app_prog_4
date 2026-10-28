from datetime import date, datetime, time, timedelta

from sqlalchemy import select

from src.models.sqlalchemy.flight import Flight
from src.repositories.sqlalchemy.base import BaseSQLAlchemyRepository


class FlightRepository(BaseSQLAlchemyRepository[Flight]):
    model = Flight

    def get_flights(
        self,
        origin: str,
        destination: str,
        departure_date: date,
    ) -> list[Flight]:
        start = datetime.combine(departure_date, time.min)
        end = start + timedelta(days=1)

        stmt = (
            select(self.model)
            .where(
                self.model.origin == origin,
                self.model.destination == destination,
                self.model.departure_time >= start,
                self.model.departure_time < end,
            )
        )

        result = self.session.execute(stmt)
        return list(result.scalars().all())