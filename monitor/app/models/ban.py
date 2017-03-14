# -*- coding:utf-8 -*-

from monitor.app.ext.database import db


class Ban(db.Model):
    __tablename__ = 'bans'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # 域名
    netloc = db.Column(db.String, nullable=False, unique=True)
    only_netloc = db.Column(db.Boolean, default=True)
    path = db.relation("Path",
                       backref='ban',
                       order_by="Path.full_path",
                       lazy='dynamic', cascade="all, delete")

    def __init__(self, netloc, only_netloc):
        self.netloc = netloc
        self.only_netloc = only_netloc


class Path(db.Model):
    __tablename__ = 'paths'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ban_id = db.Column(db.Integer, db.ForeignKey('bans.id'))
    full_path = db.Column(db.String, nullable=False)

    def __init__(self, full_path):
        self.full_path = full_path
