# -*- coding: utf-8 -*-
from app import db

class Task(db.Document):

    _id = db.ObjectIdField()
    pushTime = db.StringField(max_length=255, required=True)
    beginDate = db.StringField(max_length=255, required=True)
    endDate = db.StringField(max_length=255, required=True)
    jobId = db.StringField(max_length=255, required=True)
    command = db.StringField(max_length=1024, required=True)
    description = db.StringField(max_length=1024)
    updateTime = db.StringField()
    isRunning = db.IntField()

    meta = {

        'ordering': ['-updateTime']
    }

    def to_dict(self):
        return dict(
            _id=self._id,
            pushTime=self.pushTime,
            beginDate=self.beginDate,
            endDate=self.endDate,
            jobId=self.jobId,
            command=self.command,
            description=self.description,
            updateTime=self.updateTime,
            isRunning=self.isRunning
        )

