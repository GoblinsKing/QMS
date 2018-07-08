#import csv

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
    id = db.Column('id',db.Integer,primary_key=True) ##id e.g. "1.1"
    part_num = db.Column('part_num',db.Integer)
    ques_num = db.Column('ques_num',db.Integer)
    question = db.Column('question',db.String)
    __mapper_args__={
        'polymorphic_identity':'questions',
    } 

def load_ques():
    question_1_1 = questions(id= 1,part_num=1,ques_num=1,question="something for 1.1")
    db.session.add(question_1_1)
    question_1_2 = questions(id= 2,part_num=1,ques_num=2,question="something for 1.2")
    db.session.add(question_1_2)
    question_1_3 = questions(id= 3,part_num=1,ques_num=3,question="something for 1.3")
    db.session.add(question_1_3)
    question_2_1 = questions(id= 4,part_num=2,ques_num=1,question="something for 2.1")
    db.session.add(question_2_1)
    question_2_2 = questions(id= 5,part_num=2,ques_num=2,question="something for 2.2")
    db.session.add(question_2_2)
    question_3_1 = questions(id= 6,part_num=3,ques_num=1,question="something for 3.1")
    db.session.add(question_3_1)
    db.session.commit()
    #with open('user.csv') as f:
    #    f_csv = csv.reader(f)
    #    headers = next(f_csv)
    #    for row in f_csv:
    #        if row[4] == "trainer":
    #            Trainer = trainer(name=row[0],zid=row[1],id=row[2],password=row[3])
    #            db.session.add(Trainer)
    #        else:
    #            Trainee = trainee(name=row[0],zid=row[1],id=row[2],password=row[3])
    #           db.session.add(Trainee)
    #    db.session.commit()