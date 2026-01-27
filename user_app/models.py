import uuid
import flask_login
from project.settings import DATABASE
from library_app.models import Quiz, RedeemCode

class User(DATABASE.Model, flask_login.UserMixin):
    id= DATABASE.Column(DATABASE.Integer, primary_key= True)
    
    login= DATABASE.Column(DATABASE.String(40), nullable= False)
    name= DATABASE.Column(DATABASE.String(30), nullable= False)
    surname= DATABASE.Column(DATABASE.String(30), nullable= False)
    email= DATABASE.Column(DATABASE.String(255), nullable= False)
    password= DATABASE.Column(DATABASE.String(30), nullable= False)
    created_quizes = DATABASE.relationship(Quiz, backref = 'user', lazy = True)
    hosted = DATABASE.relationship(RedeemCode, backref = 'hosted', lazy = True)
    passed_participations = DATABASE.relationship("SessionParticipant", backref="user")

class Student(DATABASE.Model, flask_login.UserMixin):
    id= DATABASE.Column(DATABASE.Integer, primary_key= True)

    login= DATABASE.Column(DATABASE.String(40), nullable= False)
    name= DATABASE.Column(DATABASE.String(30), nullable= False)
    surname= DATABASE.Column(DATABASE.String(30), nullable= False)
    password= DATABASE.Column(DATABASE.String(8), nullable= False, default=lambda: uuid.uuid4().hex)
    
    is_student = DATABASE.Column(DATABASE.Boolean, default=True)

    my_reports = DATABASE.relationship("StudentReport", backref='student', lazy=True)

class VerificationCode(DATABASE.Model):
    id= DATABASE.Column(DATABASE.Integer, primary_key= True)

    email = DATABASE.Column(DATABASE.String)
    code = DATABASE.Column(DATABASE.String)

    