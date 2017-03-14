# -*- coding:utf-8 -*-

from flask import render_template
from werkzeug.exceptions import (
    HTTPException, InternalServerError, RequestTimeout,
)


def register(app):
    """ 在传输过来的app中添加错误句柄 """

    @app.errorhandler(400)
    @app.errorhandler(404)
    @app.errorhandler(500)
    def handle_error(e):
        if not isinstance(e, HTTPException):
            e = InternalServerError()

        return render_template(
            'error.jinja',
            code=e.code,
            name=e.name,
            description=e.description,
        ), e.code

    @app.errorhandler(EOFError)
    def handle_eof_error(e):
        return handle_error(RequestTimeout())
