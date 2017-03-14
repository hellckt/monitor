# -*- coding:utf-8 -*-

import os
from flask import Flask

from monitor.app.ext.bootstrap import bootstrap
from monitor.app.ext.database import db
from monitor.app.ext.login_manager import login_manager
from monitor.app.views import register
from monitor.config import config

basedir = os.path.abspath(os.path.dirname(__file__))


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    config[config_name].init_app(app)

    # Set up extensions in there
    db.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)

    # Register app blueprints
    register(app)

    with app.test_request_context():
        if set(db.get_tables_for_bind()) != {'bans', 'flows', 'paths',
                                             'users'}:
            db.create_all()

    return app
