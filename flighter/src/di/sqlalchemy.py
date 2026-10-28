from collections.abc import Iterable
from dishka import Provider, Scope, provide
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker
from src.repositories.sqlalchemy.transaction import SQLAlchemyTransaction
from src.core.settings import settings


class SQLAlchemyProvider(Provider):
    @provide(scope=Scope.APP)
    def engine(self) -> Engine:
        return create_engine(
            settings.POSTGRES_URL,
            pool_size=10,
            max_overflow=40,
        )

    @provide(scope=Scope.APP)
    def session_factory(
        self,
        engine: Engine,
    ) -> sessionmaker[Session]:
        return sessionmaker(
            bind=engine,
            class_=Session,
            expire_on_commit=False,
        )

    @provide(scope=Scope.REQUEST)
    def sqlalchemy_session(
        self,
        session_factory: sessionmaker[Session],
    ) -> Iterable[Session]:
        with session_factory() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    def sqlalchemy_transaction(
        self,
        session: Session,
    ) -> SQLAlchemyTransaction:
        return SQLAlchemyTransaction(session=session)