from dishka import Scope, Provider, provide
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.sqlalchemy.flight import FlightRepository

class RepositoryProvider(Provider):

    @provide(scope=Scope.REQUEST)
    def flight_repo(self, session: AsyncSession) -> FlightRepository:
        return FlightRepository(session=session)

