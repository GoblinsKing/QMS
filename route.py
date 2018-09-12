from init_db import db,create_db
create_db()
from server import app, login_manager
from flask import request, render_template,session,redirect,url_for,flash
from flask_login import LoginManager,UserMixin,login_required,login_user,current_user,logout_user
from user import *
from question import *
from audit import *
#from datetime import datetime,timedelta

n = 1
series_num = 4
part_num = 1
ques_num = 0
num = [3,2,1]
Final = "False"
curr_audit = None

def next_ques():
    global series_num
    global part_num
    global ques_num
    if series_num == 10:
        return False
    while 1 != 0:
        if get_question(series_num,part_num,ques_num + 1) != None:
            ques_num += 1
            break
        elif get_question(series_num,part_num + 1,0) != None:
            part_num += 1
            ques_num = 0
            break
        elif get_question(series_num,part_num + 1,1) != None:
            part_num += 1
            ques_num = 1
            break
        else:
            series_num += 1
            part_num = 1
            ques_num = 0
            if get_question(series_num,part_num,ques_num) != None:
                break
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

@app.route('/reset_audit')
def reset_audit():
    #reset_answer()
    global part_num
    global ques_num
    global Final
    global curr_audit
    global series_num
    series_num = 4
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
    return render_template('new_audit.html', user=current_user)

@app.route('/audit',methods=['POST','GET'])
@login_required
def audit():
    global n
    global Final
    global curr_audit
    global part_num
    global ques_num
    global series_num
    #开始后再刷新会导致重新提交表单,导致前进
    #不重置评估直接开始会导致因为final值为TURE而尝试进result界面然后报错
    if Final == "True":
        result = calculate_result(curr_audit)
        return render_template('audit_result.html', result=result, title = curr_audit, user=current_user)
    answer = None
    if request.method == 'POST':
        n = n + 1
        form = request.form
        answer=str(form['result'])
        answer = get_answer(answer)
        comment = str(form['comment'])
        suggestion = str(form['comment'])
        save_answer(n, series_num, part_num, ques_num, answer, comment, suggestion, current_user.username, curr_audit)
        temp = next_ques()
        question = get_question(series_num, part_num, ques_num)
        if temp is False:
            Final = "True"
            result = calculate_result(curr_audit)
            return render_template('audit_result.html', result=result, title = curr_audit, user=current_user)
    question = get_question(series_num, part_num, ques_num)
    return render_template('audit.html',user=current_user, question=question, n = n, series_num = series_num, part_num = part_num, ques_num = ques_num)

@app.route('/AuditHistory',methods=['GET'])
@login_required
def AuditHistory():
    if current_user.role == "customer":
        history = check_audit(current_user.project)
    else:
        history = audit_history(current_user.username)
    return render_template('audit_history.html', audit_history=history, user=current_user)

@app.route('/update',methods=['GET'])
def update():
    return render_template('update.html', user=current_user)

@app.route('/AuditResult/<title>',methods=['GET'])
@login_required
def AuditResult(title):
    result = calculate_result(title)
    return render_template('audit_result.html', result=result, title = title, user=current_user)

@app.route('/AuditResult/<title>/chart',methods=['GET'])
@login_required
def chart(title):
    result = calculate_result(title)
    return render_template('chart.html',Q1 = result[0], Q2 = result[1], Q3 = result[2])