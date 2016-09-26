# -*- coding: utf-8 -*-
from app import db

class YearFinished(db.Document):
    '''
        完成电影的年份
    '''
    year = db.IntField(required=True)
    meta = {
        'indexes' : ['-year'],
        'ordering' : ['-year']
    }

