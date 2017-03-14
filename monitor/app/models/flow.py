# -*- coding:utf-8 -*-
from datetime import datetime

from mitmproxy.net.http.url import parse, unparse

from monitor.app.ext.database import db


class Flow(db.Model):
    __tablename__ = "flows"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    scheme = db.Column(db.String(5))
    netloc = db.Column(db.String)
    port = db.Column(db.Integer)
    full_path = db.Column(db.String)
    create_timestamp = db.Column(db.TIMESTAMP, default=datetime.now())

    def __init__(self, scheme, netloc, port, full_path):
        self.scheme = scheme
        self.netloc = netloc
        self.port = port
        self.full_path = full_path

    @staticmethod
    def add_url(url) -> None:
        scheme, netloc, port, full_path = parse(url)
        flow = Flow(scheme=scheme, netloc=netloc, port=port,
                    full_path=full_path)
        db.session.add(flow)
        db.session.commit()

    @property
    def url(self) -> str:
        return unparse(self.scheme, self.netloc, self.port, self.full_path)
