# -*- coding: utf-8 -*-
from app import db

class Ip(db.Document):
    '''
        爬虫ip
    '''
    ip = db.StringField(max_lenghth=60, required=True)
    port = db.StringField(max_lenghth=60, required=True)
    date = db.StringField(max_lenghth=60, required=True)

    meta = {

        'ordering': ['-date']
    }

    def to_dict(self):
        return dict(
            ip = self.ip,
            port = self.port,
            date = self.date
        )