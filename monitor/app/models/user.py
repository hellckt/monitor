# -*- coding:utf-8 -*-
from datetime import datetime

import os
from flask_login import AnonymousUserMixin, UserMixin
from hashlib import sha256
from sqlalchemy.ext.hybrid import hybrid_property

from monitor.app.ext.database import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    username = db.Column(db.Unicode(255), nullable=False)

    # Hashed password

    _password = db.Column('password', db.Unicode(128), nullable=False)

    def __init__(self, *args, **kw):
        super(User, self).__init__(*args, **kw)

    def __repr__(self):
        return '<User: username=%s>' % str(self.username)

    def __unicode__(self):
        return self.username

    @staticmethod
    def initialize() -> None:
        if not User.exist():
            user = User(username='admin', password='admin')
            db.session.add(user)
            db.session.commit()

    @staticmethod
    def by_username(username: str) -> object:
        return User.query(username=username).first()

    @staticmethod
    def by_credentials(username: str, password: str, *args, **kwargs):
        user = User.by_username(username)
        if user and user.validate_password(password):
            return user

    ################################

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = self._hash_password(password)

    @classmethod
    def _hash_password(cls, password) -> str:
        if isinstance(password, str):
            password = password.encode('utf-8')
        salt = sha256()
        salt.update(os.urandom(60))
        hash = sha256()
        hash.update(password + salt.hexdigest().encode('utf-8'))
        password = salt.hexdigest() + hash.hexdigest()
        if not isinstance(password, str):
            password = password.decode('utf-8')
        return password

    def validate_password(self, password) -> bool:
        # Make sure accounts without a password can't log in
        if not self.password or not password:
            return False

        hash = sha256()
        if isinstance(password, str):
            password = password.encode('utf-8')
        hash.update(password + str(self.password[:64]).encode('utf-8'))
        return self.password[64:] == hash.hexdigest()


class AnonymousUser(AnonymousUserMixin):
    pass
