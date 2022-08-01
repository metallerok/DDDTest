# Description: init declarative Base
# Author: Kireev Georgiy <metallerok@gmail.com>
# Copyright (C) 2019 by Kireev Georgiy

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from src.lib.sqlalchemy import model

DBSession = scoped_session(sessionmaker())
Base = declarative_base(cls=model(DBSession))
