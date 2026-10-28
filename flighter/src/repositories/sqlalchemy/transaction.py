from sqlalchemy.orm import Session


class SQLAlchemyTransaction:

    def __init__(self, session: Session) -> None:
        self.session = session

    def __enter__(self):
        if not self.session.in_transaction():
            self.session.begin()
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc_type is None:
            self.session.commit()
        else:
            self.session.rollback()
        