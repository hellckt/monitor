# -*- coding:utf-8 -*-

from flask import (Blueprint, abort, flash, redirect, render_template, url_for)
from flask_login import login_required

from monitor.app import db
from monitor.app.forms.ban import FlowBanForm
from monitor.app.models import Flow, Ban
from monitor.app.models import Path

flow = Blueprint('flow', 'monitor')


@flow.route('/<int:flow_id>', methods=['GET', 'POST'])
@login_required
def detail(flow_id):
    f = Flow.get(flow_id)
    form = FlowBanForm()
    if not f:
        abort(404)
    form.url.data = f.url
    form.netloc.data = f.netloc
    form.full_path.data = f.full_path
    if form.validate_on_submit():
        ban = Ban.query(netloc=form.netloc.data).first()
        if not ban:
            newban = Ban(netloc=form.netloc.data,
                         only_netloc=form.only_netloc.data)
            if not form.only_netloc.data:
                path = Path(full_path=form.full_path.data)
                newban.path.append(path)
            db.session.add(newban)
            db.session.commit()
        else:
            ban.only_netloc = form.only_netloc.data
            if not form.only_netloc.data:
                path = Path(full_path=form.full_path.data)
                ban.path.append(path)
            db.session.add(ban)
            db.session.commit()
        flash(u'添加成功')
        return redirect(url_for('index'))
    return render_template('flow/detail.jinja', form=form)
