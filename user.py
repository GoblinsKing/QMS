from flask_login import UserMixin
from init_db import db

class user(UserMixin, db.Model):
    __tablename__='user'
    id = db.Column('id',db.String,primary_key=True)
    name=db.Column('name',db.String)
    username = db.Column('username',db.String)
    password=db.Column('password',db.String)
    role = db.Column('role',db.String)
    __mapper_args__={
        'polymorphic_identity':'user',
        'polymorphic_on':role
    } 

class admin(user):
    __tablename__='admin'
    id = db.Column(db.String,db.ForeignKey('user.id'),primary_key=True)
    __mapper_args__={
        'polymorphic_identity':'admin',
    }

class customer(user):
    __tablename__='customer'
    id = db.Column(db.String,db.ForeignKey('user.id'),primary_key=True)
    __mapper_args__={
        'polymorphic_identity':'customer',
    }

def load_users():
    admin_1 = admin(id="999",name="admin",username="admin",password="admin")
    db.session.add(admin_1)
    customer_1 = customer(id="998",name="aaa",username="aaa",password="aaa")
    db.session.add(customer_1)
    db.session.commit()