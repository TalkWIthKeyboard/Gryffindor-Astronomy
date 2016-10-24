# coding=utf-8

from app import db

class Token(db.Document):
    '''
        获取最新的token存入数据库
    '''

    token = db.StringField(max_length=1200, required=True)
    createTime = db.DateTimeField(required=True)
    expires_in = db.IntField(required=True)

    def to_dict(self):
        return dict(
            token=self.token,
            expires_in=self.expires_in,
            createTime=self.createTime
        )

