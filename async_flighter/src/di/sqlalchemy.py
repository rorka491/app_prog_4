from collections.abc import AsyncIterator
from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.core.settings import settings
from src.repositories.sqlalchemy.transaction import SQLAlchemyTransaction


class SQLAlchemyProvider(Provider):
    @provide(scope=Scope.APP)
    async def engine(self) -> AsyncIterator[AsyncEngine]:
        engine = create_async_engine(
            settings.POSTGRES_URL,
            pool_size=10,
            max_overflow=40,
        )
        yield engine
        await engine.dispose()

    @provide(scope=Scope.APP)
    def session_factory(
        self,
        engine: AsyncEngine,
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            bind=engine,
            expire_on_commit=False,
        )

    @provide(scope=Scope.REQUEST)
    async def sqlalchemy_session(
        self,
        session_factory: async_sessionmaker[AsyncSession],
    ) -> AsyncIterator[AsyncSession]:
        async with session_factory() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    def sqlalchemy_transaction(
        self,
        session: AsyncSession,
    ) -> SQLAlchemyTransaction:
        return SQLAlchemyTransaction(session=session)