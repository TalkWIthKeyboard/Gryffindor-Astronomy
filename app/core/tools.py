#!/usr/bin/python
# -*- coding: utf-8 -*-
import hashlib
import datetime

from flask_apscheduler import APScheduler
from app.models.logModel import Log


'''
    全局公用部分
'''
scheduler = APScheduler()
taskUrl = ""

'''
    工具部分
'''

def get_md5(str1=None):
    '''
        md5加密
    '''
    md5 = hashlib.md5()
    md5.update(str1)
    return md5.hexdigest()

def add_log(content,fromTask,parameter):
    '''
        添加日志
    '''
    log = Log(content=content,
              fromTask=fromTask,
              parameter=parameter,
              createTime=datetime.datetime.now())
    log.save()