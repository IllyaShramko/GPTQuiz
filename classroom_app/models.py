import uuid
import flask_login
from project.settings import DATABASE
from datetime import datetime


class Student(DATABASE.Model, flask_login.UserMixin):
    id= DATABASE.Column(DATABASE.Integer, primary_key= True)

    login= DATABASE.Column(DATABASE.String(40), nullable= False)
    name= DATABASE.Column(DATABASE.String(30), nullable= False)
    surname= DATABASE.Column(DATABASE.String(30), nullable= False)
    password= DATABASE.Column(DATABASE.String(5), nullable= False, default=lambda: uuid.uuid4().hex[:5])

    my_reports = DATABASE.relationship("StudentReport", backref='student', lazy=True)
    sessions = DATABASE.relationship("SessionParticipant", backref="student_profile", lazy=True)
    my_class_id = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey("group_class.id"))

class GroupClass(DATABASE.Model):
    id= DATABASE.Column(DATABASE.Integer, primary_key= True)

    number = DATABASE.Column(DATABASE.Integer,   nullable= False)
    char   = DATABASE.Column(DATABASE.String(1), nullable= False)

    teacher_id = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey("user.id"))
    students = DATABASE.relationship("Student", backref="classroom", lazy=True)
    rooms = DATABASE.relationship("Room", backref="classroom", lazy=True)