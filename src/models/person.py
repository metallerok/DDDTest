from sqlalchemy import Column, Integer, String, ForeignKey
from .meta import Base


class Person(Base):
    __tablename__ = 'person'

    id = Column(String, primary_key=True)
    name = Column(String(250), nullable=False)
