from init_db import db
import time
class audit(db.Model):
    __tablename__='audit'
    id = db.Column('id',db.Integer,primary_key=True)
    part_num = db.Column('part_num',db.Integer)
    ques_num = db.Column('ques_num',db.Integer)
    answer = db.Column('answer',db.Integer)
    comment = db.Column('comment',db.String)
    suggestion = db.Column('suggestion',db.String)
    auditor = db.Column('auditor',db.String)
    name = db.Column('name',db.String)
    #datetime = db.Column('datetime',db.datetime.datetime)
    __mapper_args__={
        'polymorphic_identity':'audit',
    } 
    
def save_answer(n, part_num, ques_num, answer, comment, suggestion, auditor, name):
    #curr_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    new = audit(id = n, part_num = part_num, ques_num = ques_num, answer = answer, comment = comment, suggestion = suggestion, auditor = auditor, name = name)
    db.session.add(new)
    db.session.commit()

def show_answer(part_num, ques_num, curr_audit):
    temp = audit.query.filter_by(part_num = part_num, ques_num = ques_num, name = curr_audit).first()
    if temp is None:
        return None
    else:
        return temp.answer

def all_answer(curr_audit):
    temp = audit.query.filter_by(name = curr_audit).all()
    return temp

def calculate_result(curr_audit):
    part_num = 1
    ques_num = 1
    result = [0,0,0]
    num = [3,2,1]
    while part_num <= len(num):
        ques_num = 1;
        while ques_num <= num[part_num-1]:
            ans = show_answer(part_num, ques_num, curr_audit)
            if ans is None:
                return None
            result[part_num-1] += ans
            ques_num += 1
        part_num += 1
    result[0] = result[0]/3
    result[1] = result[1]/2
    result[2] = result[2]/1
    return result

def audit_history(auditor):
    temp = audit.query.filter_by(auditor = auditor).group_by(audit.name).all()
    return temp

def check_audit(name):
    temp = audit.query.filter_by(name = name).group_by(audit.name).all()
    return temp