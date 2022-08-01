from sqlalchemy import inspect
from sqlalchemy.orm import scoped_session
from sqlalchemy.ext.hybrid import hybrid_property

from typing import Type


class Model:
    db_session = None

    def save(self):
        self.db_session.add(self)
        return self

    def delete(self):
        self.db_session.delete(self)

    def commit(self):
        self.db_session.commit()

    def flush(self):
        self.db_session.flush()

    @hybrid_property
    def query(self):
        return self.db_session.query(self)

    def to_dict(self):
        return dict((prop.key, getattr(self, prop.key))
                    for prop in inspect(self).mapper.iterate_properties)

    def update(self, params: dict):
        for key, value in params.items():
            setattr(self, key, value)


def model(session: scoped_session) -> Type[Model]:
    class BaseModel(Model):
        db_session = session
    return BaseModel
