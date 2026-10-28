from dishka import Scope, Provider, provide
from sqlalchemy.orm import Session
from src.repositories.sqlalchemy.flight import FlightRepository

class RepositoryProvider(Provider):

    @provide(scope=Scope.REQUEST)
    def flight_repo(self, session: Session) -> FlightRepository:
        return FlightRepository(session=session)

