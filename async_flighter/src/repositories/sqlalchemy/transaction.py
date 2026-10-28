from sqlalchemy.ext.asyncio import AsyncSession


class SQLAlchemyTransaction:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def __aenter__(self) -> "SQLAlchemyTransaction":
        if not self.session.in_transaction():
            await self.session.begin()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if exc_type is None:
            await self.session.commit()
        else:
            await self.session.rollback()