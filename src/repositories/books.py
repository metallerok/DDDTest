import abc
from sqlalchemy.orm import Session
from typing import Optional
from src.models.book import Book
from src.models.primitives BookTitle

class BooksRepoABC(abc.ABC):
    @abc.abstractmethod
    def add(self, book: Book):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id_: str) -> Optional[Book]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_title(self, title: string) -> Optional[Book]:
        raise NotImplementedError


class SABooksRepo(BooksRepoABC):
    def __init__(self, db_session: Session):
        self._db_session = db_session

    def add(self, book: Book):
        self._db_session.add(book)

    def get(self, id_: str) -> Optional[Book]:
        query = self._db_session.query(
            Book
        ).filter(
            Book.id == id_
        )

        result = query.one_or_none()

        return result

    def get_by_title(self, title: string) -> Optional[Book]:
        query = self._db_session.query(
            Book
        ).filter(
            sa.type_coerce(Book.title, sa.String).ilike(f"%{title}%"),
        )

        result = query.first()

        return result
