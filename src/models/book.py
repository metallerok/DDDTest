import sqlalchemy as sa
from sqlalchemy.orm import relation
from src.models.meta import Base
from src.models.primitives.book import (
    SABookTitle,
    SAOrderBookCount,
    OrderBookCount,
)
from uuid import uuid4


class Book(Base):
    __tablename__ = "book"

    id = sa.Column(sa.String, primary_key=True, nullable=False)

    title = sa.Column(SABookTitle, nullable=False)


class OrderBook(Base):
    __tablename__ = "order_book"

    id = sa.Column(sa.String, primary_key=True, nullable=False)

    book_id = sa.Column(sa.String, sa.ForeignKey("book.id"), nullable=False, index=True)
    book = relation("Book")

    order_id = sa.Column(sa.String, sa.ForeignKey("order.id"), nullable=False, index=True)

    count = sa.Column(SAOrderBookCount, nullable=False)


class Order(Base):
    __tablename__ = "order"
    id = sa.Column(sa.String, primary_key=True, nullable=False)

    _order_books = relation("OrderBook")

    @property
    def order_books(self):
        return tuple(self._order_books)

    def append_book(self, book: Book, count: OrderBookCount):
        self._order_books.append(
            OrderBook(
                id=str(uuid4()),
                book=book,
                count=count,
            )
        )
