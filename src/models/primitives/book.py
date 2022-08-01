import sqlalchemy as sa
from src.models.exc import AttributeValidationError
from copy import deepcopy


class BookTitle:
    MAX_LENGTH = 240

    def __init__(self, title: str):
        if title is None:
            raise AttributeValidationError("BookTitle cannot be None")

        if len(title) == 0:
            raise AttributeValidationError("BookTitle cannot be empty")

        if len(title) > self.MAX_LENGTH:
            raise AttributeValidationError("BookTitle is too long")

        self._title = title

    @property
    def title(self):
        return deepcopy(self._title)

    def __eq__(self, other: 'BookTitle'):
        return self._title == other.title

    def __str__(self):
        return self._title

    def __repr__(self):
        return f"<BookTitle title={self._title}>"


class SABookTitle(sa.TypeDecorator):
    @property
    def python_type(self):
        return BookTitle

    impl = sa.String

    cache_ok = True

    def process_bind_param(self, value: BookTitle, dialect):
        return value.title

    def process_result_value(self, value, dialect):
        return BookTitle(value)


class OrderBookCount:
    def __init__(self, value: int):
        if value is None:
            raise AttributeValidationError("OrderBookCount cannot be None")

        if value <= 0:
            raise AttributeValidationError("OrderBookCount must be positive")

        self._value = value

    @property
    def value(self):
        return deepcopy(self._value)

    def __eq__(self, other: 'OrderBookCount'):
        return self.value == other.value

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"<OrderBookCount value={self._value}>"


class SAOrderBookCount(sa.TypeDecorator):
    @property
    def python_type(self):
        return OrderBookCount

    impl = sa.Integer

    cache_ok = True

    def process_bind_param(self, value: OrderBookCount, dialect):
        return value.value

    def process_result_value(self, value, dialect):
        return OrderBookCount(value)
