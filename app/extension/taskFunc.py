#!/usr/bin/python
# -*- coding: utf-8 -*-
from app.models.taskModel import Task
from app.publics.variable import scheduler
from app.extension.tools import add_log
import datetime
import pytz
from multiprocessing.dummy import Pool as ThreadPool

utc=pytz.UTC

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

