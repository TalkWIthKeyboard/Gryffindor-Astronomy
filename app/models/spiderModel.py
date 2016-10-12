# -*- coding: utf-8 -*-
from app import db
from datetime import datetime


class MtimeMixin(object):
    '''
        时光网上电影的id
    '''
    movieid = db.IntField(required=True)


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

class AliasName(db.Document):
    '''
        数据库中存在的名字和别名
    '''
    name = db.StringField(max_lenghth=60, required=True) # 数据库中存在的名字
    alias = db.ListField(db.StringField(max_length=60, required=True)) # 这个人的别名

class Actor(db.EmbeddedDocument):
    '''
        演员信息
    '''
    mid = db.IntField(default=0, required=True) # 演员链接的唯一ID
    poster = db.StringField(max_length=100) # 海报缩略图
    name = db.StringField(max_length=60, required=True) # 演员的名字
    play = db.StringField(max_length=60, required=True) #剧中人物

class Director(db.EmbeddedDocument):

    '''导演信息'''
    mid = db.IntField(default=0)  # 演员链接的唯一ID
    name = db.StringField(max_length=60)  # 导演名字
    cnname = db.StringField(max_length=60)  # 可能有中文翻译过来的名字
    poster =db. StringField(max_length=100)  # 海报缩略图

class Fullcredits(db.Document, MtimeMixin):
    '''
        演职员表
    '''
    director = db.ListField(db.EmbeddedDocumentField(Director))  # 导演
    writer = db.ListField(db.StringField(max_length=30, required=True))  # 编剧
    actor = db.ListField(db.EmbeddedDocumentField(Actor))  # 演员
    produced = db.ListField(db.StringField(max_length=60, required=True))  # 制作人
    originalmusic = db.ListField(
        db.StringField(max_length=60, required=True))  # 原创音乐
    cinematography = db.ListField(db.StringField(max_length=60, required=True))  # 摄影
    filmediting = db.ListField(db.StringField(max_length=60, required=True))  # 剪辑
    artdirection = db.ListField(db.StringField(max_length=60, required=True))  # 美术设计
    costumedesign = db.ListField(
        db.StringField(max_length=60, required=True))  # 服装设计
    assistantdirector = db.ListField(
        db.StringField(max_length=60, required=True))  # 副导演/助理导演


class EmbeddedReleaseInfo(db.EmbeddedDocument):
    encountry = db.StringField(max_length=30, required=True)  # 英文国家名
    cncountry = db.StringField(max_length=30, required=True)  # 中文国家名
    releasetime = db.DateTimeField(default=datetime.now(), required=True)  # 上映时间

class Movie(db.Document, MtimeMixin):
    '''
        电影信息
    '''
    rating = db.FloatField(required=True)  # 评分
    ratingcount = db.IntField(default=0, required=True)  # 评分人数
    want = db.IntField(default=0, required=True)  # 想看
    favorited = db.IntField(default=0, required=True)  # 收藏数

class Plot(db.Document, MtimeMixin):

    '''
        电影剧情
    '''
    content = db.ListField(db.StringField())  # 剧情片段

class EmbeddedScenes(db.EmbeddedDocument):
    title = db.StringField(max_length=30, required=True)  # 主题
    content = db.ListField(db.StringField())

class Scenes(db.Document, MtimeMixin):

    '''
        幕后揭秘
    '''
    scene = db.ListField(db.EmbeddedDocumentField(EmbeddedScenes))  # 花絮

class Company(db.EmbeddedDocument):

    '''
        制作/发行信息
    '''
    name = db.StringField(max_length=60, required=True)  # 公司名字
    country = db.StringField(max_length=30)  # 公司所在国家

class Details(db.Document, MtimeMixin):

    '''
        详细信息
    '''
    enalias = db.ListField(db.StringField())  # 中文片名
    cnalias = db.ListField(db.StringField())  # 外文片名
    time = db.StringField(max_length=60)  # 片长
    language = db.ListField(db.StringField(max_length=10))  # 对白语言
    cost = db.StringField()  # 制作成本
    date = db.ListField(db.DateTimeField())  # 拍摄日期
    release = db.ListField(db.EmbeddedDocumentField(EmbeddedReleaseInfo))  # 新增的发布情况
    publish = db.ListField(db.EmbeddedDocumentField(Company))  # 发行公司
    make = db.ListField(db.EmbeddedDocumentField(Company))  # 制作公司
    site = db.ListField(db.StringField(max_length=60, required=True))  # 官方网址

