# -*- coding:utf-8 -*-

from flask_login import LoginManager

from monitor.app.models.user import AnonymousUser, User

login_manager = LoginManager()

login_manager.anonymous_user = AnonymousUser
login_manager.login_view = "auth.login"
login_manager.login_message = "请先登录"


@login_manager.user_loader
def load_user(user_id):
    return User.get(int(user_id))
