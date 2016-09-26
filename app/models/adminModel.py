# -*- coding: utf-8 -*-

from app import db
from flask_login import UserMixin

class User(db.Document, UserMixin):

    _id = db.ObjectIdField()
    myid = db.IntField(required=True)
    account = db.StringField(max_length=255, required=True)
    password = db.StringField(max_length=255, required=True)
    userName = db.StringField(max_length=255, required=True)

    def get_id(self):
        return self.myid
