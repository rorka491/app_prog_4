from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class FlightSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    carrier: str = Field(max_length=100)
    flight_number: str = Field(max_length=20)

    origin: str = Field(min_length=3, max_length=3)
    destination: str = Field(min_length=3, max_length=3)

    departure_time: datetime
    arrival_time: datetime

    price: int = Field(ge=0)