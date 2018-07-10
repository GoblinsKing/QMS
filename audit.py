from init_db import db
class audit(db.Model):
    __tablename__='audit'
    id = db.Column('id',db.Integer,primary_key=True)
    part_num = db.Column('part_num',db.Integer)
    ques_num = db.Column('ques_num',db.Integer)
    answer = db.Column('answer',db.Integer)
    __mapper_args__={
        'polymorphic_identity':'audit',
    } 
    
def save_answer(n, part_num, ques_num, answer):
    new = audit(id = n, part_num = part_num, ques_num = ques_num, answer = answer)
    db.session.add(new)
    db.session.commit()

def show_answer(part_num, ques_num):
    temp = audit.query.filter_by(part_num = part_num, ques_num = ques_num).first()
    if temp is None:
        return None
    else:
        return temp.answer