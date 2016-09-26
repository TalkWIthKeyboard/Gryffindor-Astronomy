#!/usr/bin/python
# -*- coding: utf-8 -*-
from app.models.taskModel import Task
from app.models.logModel import Log
from app.publics.variable import scheduler
import app.publics.variable as variable
import datetime
import requests
import leancloud
import json
import pytz
import re
from multiprocessing.dummy import Pool as ThreadPool
from config import TEST_LEANCLOUD_APP_ID,TEST_LEANCLOUD_APP_KEY,PRO_LEANCLOUD_APP_ID,PRO_LEANCLOUD_APP_KEY

utc=pytz.UTC

leancloud.init(PRO_LEANCLOUD_APP_ID,PRO_LEANCLOUD_APP_KEY)

def add_log(content,fromTask,parameter):
    log = Log(content=content,
              fromTask=fromTask,
              parameter=parameter,
              createTime=datetime.datetime.now())
    log.save()









#添加任务
def add_task():
    try:
        date = str(datetime.datetime.now().strftime("%Y-%m-%d"))
        taskList = Task.objects(beginDate__lte=date,
                                endDate__gte=date,
                                isRunning=0 or 2).all()
        if taskList:
            for each in taskList:
                exec(str(each.command))
                each.isRunning = 1
                each.save()
                add_log('成功将任务 ' + each.jobId + ' 添加到任务队列中',
                        'system',
                        '')
    except Exception,e:
        add_log('add_task出现异常: ' + e.message,
                'system',
                '')

#删除任务
def delete_task():
    try:
        date = str(datetime.datetime.now().strftime("%Y-%m-%d"))
        taskList = Task.objects(endDate__lt=date,
                                isRunning=1).all()
        if taskList:
            for each in taskList:
                scheduler.delete_job(str(each['jobId']))
                each.isRunning = 0
                each.save()
                add_log('成功将任务 ' + each.jobId + ' 从任务队列中踢出',
                        'system',
                        '')
    except Exception,e:
        add_log('delete_task出现异常: ' + e.message,
                'system',
                '')


def job3(a,b):
    answer = '>>>>>>>>>>job3带参数测试' + str(a) + ' ' + str(b) + '<<<<<<<<<<'
    add_log('job3任务执行成功,输出: ' + answer,
            'system',
            '')

def job4(a,b):
    answer = '>>>>>>>>>>job4带参数测试' + str(a) + ' ' + str(b) + '<<<<<<<<<<'
    add_log('job4任务执行成功,输出: ' + answer,
            'system',
            '')

# if __name__ == '__main__':
#     clazz = '57aa69611532bc0060e5b104'
#     push_gambition_task(clazz,'job5')
#     add_task()
