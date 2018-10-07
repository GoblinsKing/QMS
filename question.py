import csv

def get_answer(answer):
    if answer == "Excellent":
        return 5
    elif answer == "Good":
        return 4
    elif answer == "Fair":
        return 3
    elif answer == "Poor":
        return 2
    elif answer == "Terrible":
        return 1
    else:
        return 0

from init_db import db
class questions(db.Model):
    __tablename__='questions'
    id = db.Column('id',db.Integer,primary_key=True) ##id e.g. 0,1,2,3,4,5......
    series_num = db.Column('series_num',db.Integer)
    part_num = db.Column('part_num',db.Integer)
    ques_num = db.Column('ques_num',db.Integer)
    question = db.Column('question',db.String)
    __mapper_args__={
        'polymorphic_identity':'questions',
    } 

def load_ques():
    csvFile = open("questions.csv", "r")
    reader = csv.reader(csvFile)
    for row in reader:
        if reader.line_num == 1: # 忽略第一行
            continue
        question = questions(id=row[0],series_num=row[1],part_num=row[2],ques_num=row[3],question=row[4])
        db.session.add(question)
        db.session.commit()
    csvFile.close()

def get_question(series_num, part_num, ques_num):
    temp = questions.query.filter_by(series_num=series_num, part_num=part_num, ques_num=ques_num).first()
    if temp is None:
        return None
    else:
        return temp.question