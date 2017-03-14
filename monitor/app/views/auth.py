# -*- coding:utf-8 -*-

from flask import Blueprint, flash, redirect, url_for, request, render_template
from flask_login import login_user, login_required, logout_user, current_user

from monitor.app import db
from monitor.app.forms.change import ChangePasswordForm
from monitor.app.forms.login import LoginForm
from monitor.app.forms.register import RegistrationForm
from monitor.app.models import User

auth = Blueprint('auth', 'monitor')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    exist_user = User.exists()
    if form.validate_on_submit():
        user = User.query(username=form.username.data).first()
        if user is not None and user.validate_password(form.password.data):
            login_user(user)
            flash(u'登录成功')
            return redirect(request.args.get('next') or url_for('index'))
        flash(u'错误的用户名或密码', 'error')
    return render_template('auth/login.jinja', form=form,
                           exist_user=exist_user)


@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash(u'已注销登录')
    return redirect(url_for('auth.login'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    exist_user = User.exists()
    if exist_user:
        return redirect(url_for('auth.login'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash(u'注册成功')
        return redirect(url_for('index'))
    return render_template('auth/register.jinja', form=form)


@auth.route('/changepassword', methods=['GET', 'POST'])
@login_required
def changepassword():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        current_user.password = form.password.data
        db.session.add(current_user)
        db.session.commit()
        logout_user()
        flash(u'修改成功，请重新登录')
        return redirect(url_for('auth.login'))
    return render_template('auth/changepassword.jinja', form=form)
