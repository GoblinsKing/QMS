﻿from init_db import db,create_db
create_db()
from server import app, login_manager
from flask import request, render_template,session,redirect,url_for,flash
from flask_login import LoginManager,UserMixin,login_required,login_user,current_user,logout_user
from user import *
from question import *
from audit import *
#from datetime import datetime,timedelta

n = 1

part_num = 1
ques_num = 1
num = [3,2,1]
Final = "False"
curr_audit = None

def next_ques():
    global part_num
    global ques_num
    if part_num == 3:
        return False
    if ques_num == num[part_num-1]:
        ques_num = 1
        part_num += 1
    else:
        ques_num += 1
    return True

@login_manager.user_loader
def load_user(user_id):
    # get user information from db
    return get_user(user_id)

@app.route('/', methods=['POST','GET'])
def login():
    if request.method== 'POST':
        form = request.form
        username=str(form['Username'])
        password=str(form['Password'])
        if check_password(username, password):
            return redirect(url_for('dashboard'))
        else:
            flash("用户名或密码错误",'alart')
            return redirect(url_for('login'))

    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    else:
        return render_template('Login.html')

@app.route('/dashboard',methods=['POST','GET'])
@login_required
def dashboard():
    return render_template('Dashboard.html',user=current_user)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/chart',methods=['POST','GET'])
@login_required
def chart():
    result = calculate_result(curr_audit)
    return render_template('chart.html',Q1 = result[0], Q2 = result[1], Q3 = result[2])

@app.route('/reset_audit')
def reset_audit():
    #reset_answer()
    global part_num
    global ques_num
    global Final
    global curr_audit
    part_num = 1
    ques_num = 1
    Final = "False"
    curr_audit = None
    return redirect(url_for('dashboard'))

@app.route('/new_audit',methods=['POST','GET'])
@login_required
def new_audit():
    global curr_audit
    if request.method == 'POST':
        form = request.form
        choice=str(form['choice'])
        curr_audit=str(form['name'])
        if choice == "1":
            return redirect(url_for('audit'))
    return render_template('new_audit.html')

@app.route('/audit',methods=['POST','GET'])
@login_required
def audit():
    global n
    global result
    global Final
    global curr_audit
    #开始后再刷新会导致重新提交表单,导致前进
    if Final == "True":
        question = get_question(part_num, ques_num)
        result = calculate_result(curr_audit)
        return render_template('audit.html',user=current_user, question=question, n = n, part_num = part_num, ques_num = ques_num, Final = Final, result=result)
    answer = None
    if request.method == 'POST':
        n = n + 1
        form = request.form
        answer=str(form['result'])
        answer = get_answer(answer)
        comment = str(form['comment'])
        suggestion = str(form['comment'])
        save_answer(n, part_num, ques_num, answer, comment, suggestion, current_user.username, curr_audit)
        temp = next_ques()
        question = get_question(part_num, ques_num)
        if temp is False:
            Final = "True"
            result = calculate_result(curr_audit)
            return render_template('audit.html',user=current_user, question=question, n = n, part_num = part_num, ques_num = ques_num, Final = Final, result=result)
    question = get_question(part_num, ques_num)
    result = calculate_result(curr_audit)
    return render_template('audit.html',user=current_user, question=question, n = n, part_num = part_num, ques_num = ques_num, Final = Final, result=result)

@app.route('/AuditHistory',methods=['GET'])
@login_required
def AuditHistory():
    history = audit_history(current_user.username)
    return render_template('audit_history.html', audit_history=history)

@app.route('/update',methods=['GET'])
def update():
    return render_template('update.html')