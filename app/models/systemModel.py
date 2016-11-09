# -*- coding: utf-8 -*-
from app import db

class System(db.Document):

    _id = db.ObjectIdField()
    key = db.StringField(max_length=255, required=True)
    value = db.IntField(required=True)

    def to_dict(self):
        return dict(
            _id = self._id,
            key = self.key,
            value = self.value
        )