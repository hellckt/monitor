# -*- coding:utf-8 -*-
from monitor.app.views.auth import auth as auth_blueprint
from monitor.app.views.ban import ban as ban_blueprint
from monitor.app.views.errors import \
    register as register_error_handlers
from monitor.app.views.flow import flow as flow_blueprint
from monitor.app.views.index import register as register_index


def register(app):
    register_error_handlers(app)
    register_index(app)

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(flow_blueprint, url_prefix='/flow')
    app.register_blueprint(ban_blueprint, url_prefix='/ban')
