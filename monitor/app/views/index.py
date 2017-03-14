# -*- coding:utf-8 -*-

from flask import render_template, request
from flask_login import login_required
from sqlalchemy import desc

from monitor.app import db
from monitor.app.models import Flow


def register(app):
    @app.route('/')
    @login_required
    def index():
        page = request.args.get('page', 1, type=int)
        pagination = db.session.query(Flow.id, Flow.scheme, Flow.netloc,
                                      Flow.full_path,
                                      db.func.count(Flow.id).label('total'),
                                      Flow.create_timestamp) \
            .order_by(desc(Flow.create_timestamp)) \
            .group_by(Flow.netloc, Flow.full_path) \
            .order_by(desc(Flow.create_timestamp)) \
            .paginate(page, per_page=30, error_out=False)
        flows = pagination.items
        return render_template('index.jinja', flows=flows,
                               pagination=pagination)
