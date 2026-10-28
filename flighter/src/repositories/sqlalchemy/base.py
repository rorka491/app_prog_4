from typing import Generic, Sequence
import uuid
from sqlalchemy import Select, delete, select
from sqlalchemy.orm import Session
from sqlalchemy.sql.base import ExecutableOption
from sqlalchemy.orm import Session
from src.exceptions import ObjectNotFound
from src.models.sqlalchemy.base import BaseModelPK



class BaseSQLAlchemyRepository[M: BaseModelPK]:
    model: type[M]

    def __init__(self, session: Session) -> None:
        self.session = session 


    def create(self, *args, **kwargs) -> M: ...

    def _get_query(
        self,
        *,
        options: Sequence[ExecutableOption] = (),
    ) -> Select[M]:
        return select(self.model).options(*options)

    def get_by_id(
        self,
        id: uuid.UUID,
        *,
        options: Sequence[ExecutableOption] = (),
    ) -> M | None:
        stmt = self._get_query(options=options).where(self.model.id == id)
        result = self.session.execute(stmt)
        return result.scalar_one_or_none()

    def get_or_raise(self, id: uuid.UUID) -> M:
        obj = self.session.get(self.model, id)
        if obj is None:
            raise ObjectNotFound(f"{self.model.__name__} with id={id} not found")
        return obj

    def get(self, *where) -> M | None:
        result = self.session.execute(select(self.model).where(*where))
        return result.scalar_one_or_none()

    def save(self, obj: M) -> M:
        self.session.add(obj)
        self.session.flush()
        return obj

    def delete(self, obj: M) -> None:
        self.session.delete(obj)
        self.session.flush()

    def delete_by_id(self, id: uuid.UUID) -> bool:
        result = self.session.execute(
            delete(self.model).where(self.model.id == id)
        )
        self.session.flush()
        return result.rowcount > 0  # type: ignore

    def all(self) -> list[M]:
        result = self.session.execute(select(self.model))
        return list(result.scalars().all())