#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_login import current_user
from app import app
from app.models.logModel import Log
from flask_login import login_required
import sys
import datetime

DEFAULT_PAGE_SIZE = 10

reload(sys)

sys.setdefaultencoding('utf8')


@app.route('/log/logShow',methods=['GET'])
@login_required
def log_show():
    args = request.args
    page = int(args.get('page', 1))
    paginate = Log.objects.paginate(page=page, per_page=10)
    return render_template('taskManage/log.html', paginate=paginate)

@app.route('/log/logShow/search',methods=['GET'])
@login_required
def log_show_search():
    try:
        args = request.args
        task = str(args.get('task',''))
        page = int(args.get('page', 1))
        paginate = Log.objects(fromTask__contains=task).paginate(page=page, per_page=10)
        return render_template('taskManage/log.html', paginate=paginate)
    except Exception,e:
        return e

@app.route('/log/delete/<string:id>',methods=['DELETE'])
@login_required
def log_delete(id):
    try:
        Log.objects(_id=id).delete()
        user = current_user
    except Exception,e:
        return jsonify(dict(success=False))
    return jsonify(dict(success=True))

@app.route('/log/getInfo/<string:id>',methods=['GET'])
@login_required
def log_getInfo(id):
    try:
        log = Log.objects(_id=id).first()
        return jsonify(dict(content=str(log.content)))
    except Exception,e:
        return jsonify(dict(success=False))

