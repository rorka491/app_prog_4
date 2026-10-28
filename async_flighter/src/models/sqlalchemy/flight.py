from datetime import datetime
from sqlalchemy import DateTime, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from src.models.sqlalchemy.base import BaseModelPK


class Flight(BaseModelPK):
    __tablename__ = "flights"

    carrier: Mapped[str] = mapped_column(String(100), nullable=False)
    flight_number: Mapped[str] = mapped_column(String(20), nullable=False)

    origin: Mapped[str] = mapped_column(String(3), nullable=False)
    destination: Mapped[str] = mapped_column(String(3), nullable=False)

    departure_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    arrival_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    price: Mapped[int] = mapped_column(Integer, nullable=False)
    __table_args__ = (
        Index("idx_flights_departure_time", "departure_time"),
    )
