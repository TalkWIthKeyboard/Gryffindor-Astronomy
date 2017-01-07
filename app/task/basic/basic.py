#!/usr/bin/python
# -*- coding: utf-8 -*-
from app.models.taskModel import Task
from app.core.tools import scheduler, add_log
import datetime
import pytz
from config import TASK_RUNNING, TASK_STOP

utc = pytz.UTC


def add_task():
    '''
        添加任务
    '''
    try:
        date = str(datetime.datetime.now().strftime("%Y-%m-%d"))
        taskList = Task.objects(beginDate__lte=date,
                                endDate__gte=date,
                                isRunning=TASK_STOP).all()
        if taskList:
            for each in taskList:
                exec (str(each.command))
                each.isRunning = TASK_RUNNING
                each.save()
                add_log('成功将任务 ' + each.jobId + ' 添加到任务队列中',
                        'system',
                        '')
    except Exception, e:
        add_log('add_task出现异常: ' + e.message,
                'system',
                '')


def delete_task():
    '''
        删除任务
    '''
    try:
        date = str(datetime.datetime.now().strftime("%Y-%m-%d"))
        taskList = Task.objects(endDate__lt=date,
                                isRunning=TASK_RUNNING).all()
        if taskList:
            for each in taskList:
                scheduler.delete_job(str(each['jobId']))
                each.isRunning = TASK_STOP
                each.save()
                add_log('成功将任务 ' + each.jobId + ' 从任务队列中踢出',
                        'system',
                        '')
    except Exception, e:
        add_log('delete_task出现异常: ' + e.message,
                'system',
                '')


def job3(a, b):
    answer = '>>>>>>>>>>job3带参数测试' + str(a) + ' ' + str(b) + '<<<<<<<<<<'
    print answer
    add_log('job3任务执行成功,输出: ' + answer,
            'system',
            '')
