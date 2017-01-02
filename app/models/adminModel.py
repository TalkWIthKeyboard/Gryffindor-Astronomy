# -*- coding: utf-8 -*-

from app import db
from flask_login import UserMixin

class User(db.Document, UserMixin):

    myid = db.IntField(required=True)
    # 账号
    account = db.StringField(max_length=60, required=True)
    # 密码（md5加密）
    password = db.StringField(max_length=60, required=True)
    # 用户类型(0为管理员、1为用户)
    state = db.IntField(required=True)

    # 微信平台openId
    openId = db.StringField(max_length=60)
    # 头像
    headImgUrl = db.StringField(max_length=2400)
    # 用户名
    nickName = db.StringField(max_length=60)
    # 省份
    province = db.StringField(max_length=60)
    # 城市
    city = db.StringField(max_lengtg=60)
    # 性别
    sex = db.IntField()

    def get_id(self):
        return self.myid
