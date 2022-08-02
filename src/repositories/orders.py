import abc
from typing import Optional, List
from sqlalchemy.orm import Session
from src.models.book import Order
from src.models.primitives.book import OrderStatusValue, OrderStatus


class OrdersRepoABC(abc.ABC):
    @abc.abstractmethod
    def add(self, order: Order):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id_: str) -> Optional[Order]:
        raise NotImplementedError

    @abc.abstractmethod
    def list_by_status(self, status: OrderStatus) -> List[Order]:
        raise NotImplementedError


class SAOrdersRepo(OrdersRepoABC):
    def __init__(self, db_session: Session):
        self._db_session = db_session

    def add(self, order: Order):
        self._db_session.add(order)

    def get(self, id_: str) -> Optional[Order]:
        query = self._db_session.query(
            Order
        ).filter(
            Order.id == id_
        )

        result = query.one_or_none()

        return result

    def list_by_status(self, status: OrderStatus) -> List[Order]:
        query = self._db_session.query(
            Order
        ).filter(
            Order.status == status
        )

        result = query.all()

        return result
