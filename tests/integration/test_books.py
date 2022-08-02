import json
import pytest
import random
import string
from marshmallow import ValidationError
from sqlalchemy.orm import Session
from src.models.book import (
    Book,
    Order,
    OrderBook,
)
from src.models.primitives.book import (
    BookTitle,
    OrderBookCount,
    OrderStatus,
    OrderStatusValue
)

from src.repositories.books import SABooksRepo
from src.repositories.orders import SAOrdersRepo

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


def test_order_status_after_creation(db_session):
    orders_repo = SAOrdersRepo(db_session)

    order = Order(
        id=str(uuid4())
    )

    orders_repo.add(order)

    db_session.commit()

    order = orders_repo.get(order.id)

    assert order.status
    assert type(order.status) == OrderStatus
    assert order.status == OrderStatus(OrderStatusValue.CREATED)


def test_accept_order():
    order = Order(id=str(uuid4()))

    assert order.status == OrderStatus(OrderStatusValue.CREATED)

    order.accept()

    assert order.status == OrderStatus(OrderStatusValue.ACCEPTED)


def test_orders_repo_list_orders_by_status(db_session):
    orders_repo = SAOrdersRepo(db_session)

    order1 = Order(id=str(uuid4()))

    order2 = Order(id=str(uuid4()))
    order2.accept()

    orders_repo.add(order1)
    orders_repo.add(order2)

    assert order1.status == OrderStatus(OrderStatusValue.CREATED)
    assert order2.status == OrderStatus(OrderStatusValue.ACCEPTED)

    db_session.commit()

    orders = orders_repo.list_by_status(OrderStatus(OrderStatusValue.ACCEPTED))

    assert order1 not in orders
    assert order2 in orders
