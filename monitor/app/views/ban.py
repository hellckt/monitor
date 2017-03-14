# -*- coding:utf-8 -*-

from flask import (Blueprint, render_template, request, abort, flash, redirect,
                   url_for)
from flask_login import login_required

from mitmproxy.net.http.url import parse
from monitor.app import db
from monitor.app.forms.ban import BanForm
from monitor.app.models import Ban, Path

ban = Blueprint('ban', 'monitor')


@ban.route('/', methods=['GET', 'POST'])
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Ban.query().paginate(page, per_page=30, error_out=False)
    bans = pagination.items

    form = BanForm()
    if form.validate_on_submit():
        # parse 返回的是bytes类型
        scheme, netloc, port, full_path = parse(form.url.data)
        scheme = scheme.decode('utf-8')
        netloc = netloc.decode('utf-8')
        full_path = full_path.decode('utf-8')
        ban = Ban.query(netloc=netloc).first()
        if not ban:
            newban = Ban(netloc=netloc, only_netloc=form.only_netloc.data)
            if not form.only_netloc.data:
                path = Path(full_path=full_path)
                newban.path.append(path)
            db.session.add(newban)
            db.session.commit()
        else:
            ban.only_netloc = form.only_netloc.data
            if not form.only_netloc.data:
                path = Path(full_path=full_path)
                ban.path.append(path)
            db.session.add(ban)
            db.session.commit()
        flash(u'添加成功')
        return redirect(url_for('ban.index'))
    return render_template('ban/index.jinja', bans=bans,
                           pagination=pagination, form=form)


@ban.route('/<int:ban_id>', methods=['GET'])
@login_required
def detail(ban_id):
    b = Ban.get(ban_id)
    if not b:
        abort(404)
    if not b.path.first():
        redirect(url_for('ban.index'))
    return render_template('ban/detail.jinja', ban=b)


@ban.route('/<int:ban_id>/<int:path_id>', methods=['GET'])
@login_required
def delete_path(ban_id, path_id):
    path = Path.get(path_id)
    if not path:
        abort(404)
    db.session.delete(path)
    b = Ban.get(ban_id)
    if b and not b.path.first():
        b.only_netloc = True
        db.session.add(b)
        db.session.commit()
        return redirect(url_for('ban.index'))
    return redirect(url_for('ban.detail', ban_id=ban_id))


@ban.route('/<int:ban_id>/delete', methods=['GET'])
def delete_ban(ban_id):
    b = Ban.get(ban_id)
    if not b:
        abort(404)
    db.session.delete(b)
    db.session.commit()
    return redirect(url_for('ban.index'))
