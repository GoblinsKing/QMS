from init_db import db,create_db
create_db()
from server import app, login_manager
from flask import request, render_template,session,redirect,url_for,flash
from flask_login import LoginManager,UserMixin,login_required,login_user,current_user,logout_user
from user import User
from question import *
from audit import *
#from datetime import datetime,timedelta

n = 1

part_num = 1
ques_num = 1
num = [3,2,1]
def next_ques():
    global part_num
    global ques_num
    if part_num == 3:
        return
    if ques_num == num[part_num-1]:
        ques_num = 1
        part_num += 1
    else:
        ques_num += 1

def check_password(username, password):
    if username == 'admin' and password == 'admin':
        user = User(username)
        login_user(user)
        return True
    return False

def get_user(user_id):
    """
    Your get user should get user details from the database
    """
    return User(user_id)

@login_manager.user_loader
def load_user(user_id):
    # get user information from db
    user = get_user(user_id)
    return user

@app.route('/', methods=['POST','GET'])
def login():
    if request.method== 'POST':
        form = request.form
        username=str(form['Username'])
        password=str(form['Password'])
        if check_password(username, password):
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password",'alart')
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
    part_num = 1
    ques_num = 1
    result = [0,0,0]
    while part_num <= len(num):
        ques_num = 1;
        while ques_num <= num[part_num-1]:
            result[part_num-1] += show_answer(part_num, ques_num)
            ques_num += 1
        part_num += 1

    return render_template('chart.html',Q1 = result[0]/3, Q2 = result[1]/2, Q3 = result[2]/1)

@app.route('/reset_audit')
def reset_audit():
    reset_answer()
    global n
    global part_num
    global ques_num
    n = 1
    part_num = 1
    ques_num = 1
    return redirect(url_for('dashboard'))

@app.route('/new_audit',methods=['POST','GET'])
@login_required
def new_audit():
    if request.method == 'POST':
        form = request.form
        choice=str(form['choice'])
        if choice == "1":
            return redirect(url_for('audit'))
    return render_template('new_audit.html')

@app.route('/audit',methods=['POST','GET'])
@login_required
def audit():
    global n
    global result

    #开始后再刷新会导致重新提交表单,导致前进
    
    answer = None
    if request.method == 'POST':
        n = n + 1
        form = request.form
        answer=str(form['result'])
        answer = get_answer(answer)
        comment = str(form['comment'])
        suggestion = str(form['comment'])
        save_answer(n, part_num, ques_num, answer, comment, suggestion)
        next_ques()
    question = get_question(part_num, ques_num)
    all_answers = all_answer()
    return render_template('audit.html',user=current_user, question=question, n = n, part_num = part_num, ques_num = ques_num, all_answer = all_answers)