from server import app, login_manager
from flask import request, render_template,session,redirect,url_for,flash
from flask_login import LoginManager,UserMixin,login_required,login_user,current_user,logout_user
from user import User
from question import *
#from isoi import *
#from datetime import datetime,timedelta

#app.config['SECRET_KEY']='GoblinsKing'
#login_manager = LoginManager()
#login_manager.init_app(app)
#isoi = ISOI()


n = 0
result = [0,0,0]
CurrQues = 1
QuesNum = [3,2,1]

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

@app.route('/', methods=['POST', 'GET'])
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
    global n
    global result
    global CurrQues
    
    #question1=["Q1.1","Q1.2","Q1.3"]
    #question2=["Q2.1","Q2.2"]
    #question3=["Q3.1"]
    question = ["Q1.1 xxx","Q1.2 xxx","Q1.3 xxx","Q2.1 xxx","Q2.2 xxx","Q3.1 xxx"]
    n = n + 1
    answer = None
    if request.method== 'POST':
        form = request.form
        answer=str(form['result'])
    if n == 1:
        answer = None
    answer = get_answer(answer)
    if n <= 4:
        result[CurrQues-1] = result[CurrQues-1] + answer
    elif n <= 6:
        result[1] = result[1] + answer
    elif n <= 7:
        result[2] = result[2] + answer
    return render_template('Dashboard.html',user=current_user,question=question,n=n,answer=answer,result=result)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/chart',methods=['POST','GET'])
@login_required
def chart():
    return render_template('chart.html',Q1 = result[0]/3,Q2 = result[1]/2,Q3 = result[2]/1)