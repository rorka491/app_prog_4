from src.repositories.sqlalchemy.base import BaseSQLAlchemyRepository


class BaseService[R: BaseSQLAlchemyRepository]:

    def __init__(self, repo: R) -> None:
        self.repo = repo

