# -*- coding:utf-8 -*-
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(u'旧密码',
                                 validators={DataRequired(), Length(1, 64)})
    password = PasswordField(u'新密码', validators=[
        DataRequired(), EqualTo('password2', message=u'两次输入的密码必须相同！')])
    password2 = PasswordField(u'确认密码', validators=[DataRequired()])
    submit = SubmitField(u'提交')

    def validate_old_password(self, field) -> bool:
        if not current_user:
            raise ValidationError(u'当前用户未登录')
        if not current_user.validate_password(field.data):
            raise ValidationError(u'密码错误')
