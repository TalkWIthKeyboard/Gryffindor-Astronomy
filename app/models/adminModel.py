# -*- coding: utf-8 -*-

from app import db
from flask_login import UserMixin

class User(db.Document, UserMixin):

    myid = db.IntField(required=True)
    account = db.StringField(max_length=255, required=True)
    password = db.StringField(max_length=255, required=True)
    userName = db.StringField(max_length=255, required=True)
    state = db.IntField(required=True)
    userimage = db.StringField(max_length=255)

    def get_id(self):
        return self.myid
