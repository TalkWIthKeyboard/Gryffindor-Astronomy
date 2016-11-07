#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import render_template, request, jsonify, redirect, url_for
from config import TASK_STOP,TASK_RUNNING,TASK_HANG,SYSTEM_RUNNING,SYSTEM_STOP
from flask_login import login_required
import app.core.tools as tools
from app.models.taskModel import Task
from app.models.logModel import Log
from flask_login import current_user
from app import app
import datetime
import time
import sys

DEFAULT_PAGE_SIZE = 10

reload(sys)

sys.setdefaultencoding('utf8')

@app.route('/',methods=['GET'])
def init():
    return redirect(url_for('admin'))

@app.route('/taskManage/taskShow',methods=['GET'])
@login_required
def task_show():
    args = request.args
    page = int(args.get('page', 1))
    paginate = Task.objects.paginate(page=page, per_page=10)
    return render_template('taskManage/taskManage.html', paginate=paginate,systemState=tools.systemState)

@app.route('/taskManage/create',methods=['POST'])
@login_required
def task_create():
    if request.method == 'POST':
        try:
            task = Task(pushTime=request.form['pushTime'],
                        beginDate=request.form['beginDate'],
                        endDate=request.form['endDate'],
                        jobId=request.form['jobId'],
                        command=request.form['command'],
                        description=request.form['description'],
                        updateTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        isRunning=TASK_STOP)
            task.save()
            user = current_user
            log = Log(content='创建编号为 ' + str(task.jobId) + ' 的任务',
                      fromTask=user.userName,
                      parameter='',
                      createTime=datetime.datetime.now())
            log.save()
        except Exception,e:
            return jsonify(dict(success=False))
        return jsonify(dict(success=True))

@app.route('/taskManage/update/<string:id>',methods=['PUT'])
@login_required
def task_update(id):
    if request.method == 'PUT':
        try:
            task = Task.objects(_id=id).first()
            task.pushTime = request.form['pushTime']
            task.beginDate = request.form['beginDate']
            task.endDate = request.form['endDate']
            task.jobId = request.form['jobId']
            task.command = request.form['command']
            task.description = request.form['description']
            task.updateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            task.save()
            user = current_user
            log = Log(content='修改任务 ' + str(task.jobId) + ' 的信息',
                      fromTask=user.userName,
                      parameter='',
                      createTime=datetime.datetime.now())
            log.save()
        except Exception,e:
            return jsonify(dict(success=False))
        return jsonify(dict(success=True))

@app.route('/taskManage/getInfo/<string:id>',methods=['GET'])
@login_required
def task_getInfo(id):
    try:
        task = Task.objects(_id=id).first()
        taskDict = task.to_dict()
        taskDict["_id"] = str(taskDict["_id"])
        return jsonify(taskDict)
    except Exception,e:
        return jsonify(dict(success=False))

@app.route('/taskManage/delete/<string:id>',methods=['DELETE'])
@login_required
def task_delete(id):
    try:
        task = Task.objects(_id=id).first()
        user = current_user
        log = Log(content='删除编号为 ' + str(task.jobId) + ' 的任务',
                  fromTask=user.userName,
                  parameter='',
                  createTime=datetime.datetime.now())
        log.save()
        if task.isRunning == TASK_RUNNING:
            tools.scheduler.delete_job(str(task['jobId']))
        Task.objects(_id=id).delete()
    except Exception,e:
        return jsonify(dict(success=False))
    return jsonify(dict(success=True))

@app.route('/taskManage/taskShow/search',methods=['GET'])
@login_required
def task_show_search():
    try:
        args = request.args
        jobId = args.get('jobId','')
        page = int(args.get('page', 1))
        paginate = Task.objects(jobId__contains=jobId).paginate(page=page, per_page=10)
        return render_template('taskManage/taskManage.html', paginate=paginate,systemState=tools.systemState)
    except Exception,e:
        return e

@app.route('/taskManage/startTask/<string:id>',methods=['GET'])
@login_required
def task_start(id):
    try:
        task = Task.objects(_id=id).first()
        tools.scheduler.resume_job(str(task['jobId']))
        task.isRunning = TASK_RUNNING
        task.save()
        user = current_user
        log = Log(content='启动编号为 ' + str(task.jobId) + ' 的任务',
                  fromTask=user.userName,
                  parameter='',
                  createTime=datetime.datetime.now())
        log.save()
    except Exception,e:
        return jsonify(dict(success=False))
    return jsonify(dict(sucess=True))

@app.route('/taskManage/stopTask/<string:id>',methods=['GET'])
@login_required
def task_stop(id):
    try:
        task = Task.objects(_id=id).first()
        tools.scheduler.pause_job(str(task['jobId']))
        task.isRunning = TASK_HANG
        task.save()
        user = current_user
        log = Log(content='暂停编号为 ' + str(task.jobId) + ' 的任务',
                  fromTask=user.userName,
                  parameter='',
                  createTime=datetime.datetime.now())
        log.save()
    except Exception,e:
        return jsonify(dict(success=False))
    return jsonify(dict(sucess=True))

@app.route('/taskManage/startSystem',methods=['GET'])
@login_required
def system_start():
    try:
        if tools.scheduler.running != True:
            tools.scheduler.init_app(app)
            tools.scheduler.start()
        else:
            tasks = Task.objects(isRunning=TASK_HANG).all()
            for each in tasks:
                tools.scheduler.resume_job(str(each['jobId']))
                log = Log(content='成功将任务 ' + each.jobId + ' 重新启动',
                          fromTask='system',
                          parameter='',
                          createTime=datetime.datetime.now())
                log.save()
                each.isRunning = TASK_RUNNING
                each.save()
        tools.systemState = SYSTEM_RUNNING
        user = current_user
        log = Log(content='成功启动系统',
                  fromTask=user.userName,
                  parameter='',
                  createTime=datetime.datetime.now())
        log.save()
    except Exception,e:
        print e
    time.sleep(1)
    return redirect(url_for("task_show"))

@app.route('/taskManage/stopSystem',methods=['GET'])
@login_required
def system_stop():
    try:
        tasks = Task.objects(isRunning=TASK_RUNNING).all()
        for each in tasks:
            tools.scheduler.pause_job(str(each['jobId']))
            log = Log(content='成功将任务 ' + each.jobId + ' 在队列中挂起',
                      fromTask='system',
                      parameter='',
                      createTime=datetime.datetime.now())
            log.save()
            each.isRunning = TASK_HANG
            each.save()
        tools.systemState = SYSTEM_STOP
        user = current_user
        log = Log(content='成功关闭系统',
                  fromTask=user.userName,
                  parameter='',
                  createTime=datetime.datetime.now())
        log.save()
    except Exception,e:
        print e
    time.sleep(1)
    return redirect(url_for("task_show"))



