import sqlalchemy as sa
from src.models.exc import AttributeValidationError
from copy import deepcopy
from enum import Enum


class BookTitle:
    MAX_LENGTH = 240
    PATTERN = r"^[a-zA-Z0-9а-яА-Я-_() ]{3,240}$"

    def __init__(self, title: str):
        if title is None:
            raise AttributeValidationError("BookTitle cannot be None")

        if len(title) == 0:
            raise AttributeValidationError("BookTitle cannot be empty")

        if len(title) > self.MAX_LENGTH:
            raise AttributeValidationError("BookTitle is too long")

        regexp = re.compile(self.PATTERN)

        if not bool(regexp.match(value)):
            raise AttributeValidationError("BookTitle does not match expected pattern")

        self._title = title

    @property
    def title(self):
        return deepcopy(self._title)

    def __eq__(self, other: 'BookTitle'):
        other_value = other.value if type(other) == BookTitle else None

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
        if value:
            return value.title

        return None

    def process_result_value(self, value, dialect):
        if value:
            return BookTitle(value)

        return None


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


class OrderStatusValue(Enum):
    CREATED = 1
    ACCEPTED = 2
    PAID = 3
    DELIVERED = 4


class OrderStatus:
    def __init__(self, status: OrderStatusValue = None):
        if status is None:
            self._status = OrderStatusValue.CREATED
        else:
            self._status = status

    @property
    def status(self):
        return deepcopy(self._status)

    def accept(self):
        if self._status not in [
            OrderStatusValue.CREATED
        ]:
            raise RuntimeError("Only created order can be accepted")

        self._status = OrderStatusValue.ACCEPTED

    def pay(self):
        if self._status not in [
            OrderStatusValue.ACCEPTED
        ]:
            raise RuntimeError("Payment process available only for created order")

        self._status = OrderStatusValue.PAID

    def delivery(self):
        if self._status not in [
            OrderStatusValue.PAID
        ]:
            raise RuntimeError("Not paid order cannot be delivered")

        self._status = OrderStatusValue.DELIVERED

    def __eq__(self, other: 'OrderStatus'):
        return self._status == other._status


class SAOrderStatus(sa.TypeDecorator):
    @property
    def python_type(self):
        return OrderStatus

    impl = sa.String

    cache_ok = True

    def process_bind_param(self, value: OrderStatus, dialect):
        return value.status.name

    def process_result_value(self, value, dialect):
        return OrderStatus(value)
