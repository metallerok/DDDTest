import json
import pytest
import random
import string
from marshmallow import ValidationError
from sqlalchemy.orm import Session
from src.models.book import (
    Book,
    Order,
    OrderBookCount,
    OrderBook,
)
from src.models.primitives.book import BookTitle, OrderBookCount
from src.repositories.books import SABooksRepo
from src.schemas.book import BookSchema
from src.models.exc import AttributeValidationError
from uuid import uuid4


def test_book_title_cannot_be_none():
    with pytest.raises(AttributeValidationError) as e:
        BookTitle(None)

    assert e.value.message == "BookTitle cannot be None"


def test_book_title_cannot_be_empty():
    with pytest.raises(AttributeValidationError) as e:
        BookTitle("")

    assert e.value.message == "BookTitle cannot be empty"


def test_book_title_cannot_be_too_long():
    with pytest.raises(AttributeValidationError) as e:
        BookTitle(
            ''.join(random.choices(
                string.ascii_uppercase + string.digits, k=BookTitle.MAX_LENGTH + 1)
            )
        )

    assert e.value.message == "BookTitle is too long"


def test_try_create_null_order_book_count():
    with pytest.raises(AttributeValidationError) as e:
        OrderBookCount(None)

    assert e.value.message == "OrderBookCount cannot be None"


def test_try_create_negative_order_book_count():
    with pytest.raises(AttributeValidationError) as e:
        OrderBookCount(-1)

    assert e.value.message == "OrderBookCount must be positive"


def test_book_model(db_session: Session):
    invalid_book_json = json.loads('{"title": ""}')

    with pytest.raises(ValidationError):
        BookSchema().load(invalid_book_json)

    book_json = json.loads('{"title": "valid book title"}')
    book_data = BookSchema().load(book_json)

    book_id = str(uuid4())
    book = Book(
        id=book_id,
        title=book_data["title"]
    )

    books_repo = SABooksRepo(db_session)

    books_repo.add(book)

    db_session.commit()

    book = books_repo.get(book_id)

    assert book
    assert book.id == book_id
    assert type(book.title) == BookTitle
    assert book.title == BookTitle(book_json["title"])


def test_add_book_to_order():
    book = Book(
        id=str(uuid4()),
        title=BookTitle("test book")
    )

    order = Order(
        id=str(uuid4())
    )

    assert len(order.order_books) == 0

    order.append_book(book, OrderBookCount(1))

    assert len(order.order_books) == 1


def test_try_directly_update_order_books():
    book = Book(
        id=str(uuid4()),
        title=BookTitle("test book")
    )

    order = Order(
        id=str(uuid4())
    )

    order_books = order.order_books

    with pytest.raises(AttributeError) as e:
        order_books.append(
            OrderBook(
                id=str(uuid4()),
                book=book,
                count=OrderBookCount(2),
            )
        )

    assert e.value.args[0] == "'tuple' object has no attribute 'append'"
