# -*- coding:utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError, \
    EqualTo

from monitor.app.models import User


class RegistrationForm(FlaskForm):
    username = StringField(u'用户名', validators={DataRequired(), Length(1, 64)})
    password = PasswordField(u'密码', validators=[
        DataRequired(), EqualTo('password2', message=u'两次输入的密码必须相同！')])
    password2 = PasswordField(u'确认密码', validators=[DataRequired()])
    submit = SubmitField(u'注册')

    def validate_username(self, field):
        if User.exists():
            raise ValidationError(u'Monitor只能有一个用户')
