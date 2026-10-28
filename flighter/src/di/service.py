from dishka import Provider, provide, Scope
from src.repositories.sqlalchemy.flight import FlightRepository
from src.services.flight import FlightService
from src.clients.flight import FlightClient
from src.utils.route_builder import RouteBuilder


class ServiceProvider(Provider):
    @provide(scope=Scope.APP)
    def route_builder(self) -> RouteBuilder:
        return RouteBuilder()

    @provide(scope=Scope.REQUEST)
    def flight_service(self, repo: FlightRepository, client: FlightClient, route_builder: RouteBuilder) -> FlightService:
        return FlightService(repo=repo, client=client, route_builder=route_builder)