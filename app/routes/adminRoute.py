#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import redirect,url_for,render_template,request,jsonify
from flask_login import logout_user, current_user, login_user, login_required
from app.models.adminModel import User
from app.extension.tools import get_md5
from app import app


@app.route('/admin', methods=['GET'])
def admin():
    if current_user.is_active:
        return redirect(url_for('task_show'))
    return redirect(url_for('admin_login'))

@app.route('/admin/login', methods=['POST', 'GET'])
def admin_login():
    if request.method == 'POST':
        account = request.form.get('account',None)
        password = request.form.get('password',None)
        user = User.objects(account=account).first()
        a = get_md5(password)
        if user and user.password == get_md5(password):
            login_user(user)
            return redirect(url_for('task_show'))
    return render_template('taskManage/login.html')

#管理员修改密码
@app.route('/admin/changePassword',methods=['PUT'])
@login_required
def admin_change_password():
    user = current_user
    password = request.form.get('password',None)
    oldPwd = request.form.get('oldPwd',None)
    oldPwd = get_md5(oldPwd)
    userAdmin = User.objects(myid=user.myid).first()
    if userAdmin:
        userOldPwd = userAdmin.password
        if (password is not None) and (oldPwd == userOldPwd):
            userAdmin.password = get_md5(password)
            userAdmin.save()
            return jsonify(dict(message=0))
        else:
            if oldPwd != userOldPwd:
                return jsonify(dict(message=1))
    return jsonify(dict(message=2))

@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('admin_login'))