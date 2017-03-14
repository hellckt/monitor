# -*- coding:utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, BooleanField, HiddenField
from wtforms.validators import URL, DataRequired


class FlowBanForm(FlaskForm):
    url = StringField(u'URL',
                      validators=[URL(message=u"错误的网址"), DataRequired()])
    only_netloc = BooleanField(u'仅屏蔽域名', default=True)
    netloc = HiddenField(u'netloc', validators=[DataRequired()])
    full_path = HiddenField(u'full_path', validators=[DataRequired()])
    submit = SubmitField(u'提交')


class BanForm(FlaskForm):
    url = StringField(u'URL', validators=[URL(), DataRequired()])
    only_netloc = BooleanField(u'仅屏蔽域名', default=True)
    submit = SubmitField(u'添加')
