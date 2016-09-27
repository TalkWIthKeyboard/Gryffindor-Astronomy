# -*- coding: utf-8 -*-
from app import db


class MtimeMixin(object):
    '''
        时光网上电影的id
    '''
    movieId = db.IntField(required=True)


class YearFinished(db.Document):
    '''
        完成电影的年份
    '''
    year = db.IntField(required=True)
    meta = {
        'indexes' : ['-year'],
        'ordering' : ['-year']
    }


class IdFinished(db.Document, MtimeMixin):
    '''
        按年份爬虫列表完成后保存电影的id
    '''
    year = db.IntField(required=True)
    ids = db.ListField(required=True)
    meta = {
        'indexes' : ['-year']
    }

