from datetime import date
import requests
from src.enums import Supplier
from src.schemas.flight import FlightSchema, SearchResponseSchema
from src.services.base import BaseService
from src.repositories.sqlalchemy.flight import FlightRepository
from src.clients.flight import FlightClient
from src.utils.route_builder import RouteBuilder
from src.core.settings import settings 


class FlightService(BaseService[FlightRepository]): 
    def __init__(
        self, 
        repo: FlightRepository, 
        client: FlightClient,
        route_builder: RouteBuilder,
    ) -> None:
        super().__init__(repo)
        self.client = client
        self.route_builder = route_builder

    def get_flights(
        self,
        origin: str,
        destination: str,
        departure_date: date,
    ) -> SearchResponseSchema:
        flights = self.repo.get_flights(
            origin=origin,
            destination=destination,
            departure_date=departure_date,
        )
        flights = [
            FlightSchema.model_validate(flight)
            for flight in flights
        ]
        unavailable_suppliers: list[str] = []
        for supplier_url in settings.SUPPLIERS:
            try:
                supplier_flights = self.client.get_flights(
                    departure_date=departure_date,
                    url=supplier_url
                )
            except (requests.RequestException, ValueError):
                unavailable_suppliers.append(supplier_url)
                continue
            flights.extend(supplier_flights)

        routes = self.route_builder.build(
            flights=flights,
            origin=origin,
            destination=destination
        )
        return SearchResponseSchema(
            routes=routes,
            unavailable_suppliers=unavailable_suppliers,
        )

        
        


        
        
        
