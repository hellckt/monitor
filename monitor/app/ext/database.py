# -*- coding:utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from monitor.config import config


def query(cls, **kw):
    q = db.session.query(cls)
    if kw:
        q = q.filter_by(**kw)
    return q


def get(cls, id):
    return cls.query().get(id)


def exists(cls, **kw):
    return cls.query(**kw).first() is not None


db = SQLAlchemy(session_options=dict(expire_on_commit=False))
db.Model.flask_query = db.Model.query
db.Model.query = classmethod(query)
db.Model.get = classmethod(get)
db.Model.exists = classmethod(exists)

# sqlalchemy db session without flask application instance
# TODO: 优化路径导入，使config由master传入
engine = create_engine(config['default'].SQLALCHEMY_DATABASE_URI)
DBSession = scoped_session(
    sessionmaker(bind=engine, autocommit=False, autoflush=True))
