import uuid
import flask_login
from project.settings import DATABASE
from datetime import datetime

room_history = DATABASE.Table('room_history',
    DATABASE.Column('student_id', DATABASE.Integer, DATABASE.ForeignKey('student.id'), primary_key=True),
    DATABASE.Column('room_id', DATABASE.Integer, DATABASE.ForeignKey('room.id'), primary_key=True)
)

class Student(DATABASE.Model, flask_login.UserMixin):
    id= DATABASE.Column(DATABASE.Integer, primary_key= True)

    login= DATABASE.Column(DATABASE.String(40), nullable= False)
    name= DATABASE.Column(DATABASE.String(30), nullable= False)
    surname= DATABASE.Column(DATABASE.String(30), nullable= False)
    password= DATABASE.Column(DATABASE.String(8), nullable= False, default=lambda: uuid.uuid4().hex)
    
    is_student = DATABASE.Column(DATABASE.Boolean, default=True)

    my_reports = DATABASE.relationship("StudentReport", backref='student', lazy=True)
    visited_rooms = DATABASE.relationship("Room", secondary=room_history, backref="participants")
    
    my_class_id = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey("group_class.id"))

class GroupClass(DATABASE.Model):
    id= DATABASE.Column(DATABASE.Integer, primary_key= True)

    number = DATABASE.Column(DATABASE.Integer,   nullable= False)
    char   = DATABASE.Column(DATABASE.String(1), nullable= False)

    teacher_id = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey("user.id"))
    students = DATABASE.relationship("Student", backref="classroom", lazy=True)
    rooms = DATABASE.relationship("Room", backref="classroom", lazy=True)