from src.clients.flight import FlightClient
from dishka import Provider, Scope, provide


class ClientProvider(Provider):

    @provide(scope=Scope.APP)
    def flight_client(self) -> FlightClient:
        return FlightClient()