# -*- coding: utf-8 -*-
from app import db

class Log(db.Document):

    _id = db.ObjectIdField()
    createTime = db.DateTimeField()
    content = db.StringField(max_length=255, required=True)
    fromTask = db.StringField(max_length=255, required=True)
    parameter = db.StringField(max_length=1024, required=True)

    meta = {

        'ordering' : ['-createTime']
    }


    def to_dict(self):
        return dict(
            _id=self._id,
            createTime=self.createTime,
            content=str(self.content),
            fromTask=self.fromTask,
            parameter=self.parameter
        )