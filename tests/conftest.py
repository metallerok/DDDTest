import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.meta import Base
from src import models
import venusian


@pytest.fixture()
def db_engine():
    venusian.Scanner().scan(models)
    engine = create_engine("sqlite:///app.sqlite3")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    yield engine


@pytest.fixture()
def db_session(db_engine):
    session = sessionmaker(
        db_engine, expire_on_commit=False
    )()

    yield session

    session.close()
