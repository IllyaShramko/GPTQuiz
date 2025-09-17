import flask
from project.settings import DATABASE
# from user_app.models import User

class Question(DATABASE.Model):
    id = DATABASE.Column(DATABASE.Integer, primary_key = True)

    name = DATABASE.Column(DATABASE.String(100), nullable = False)
    type = DATABASE.Column(DATABASE.String(100), nullable = False)
    variant_1 = DATABASE.Column(DATABASE.String(100), nullable = False)
    variant_2 = DATABASE.Column(DATABASE.String(100), nullable = True)
    variant_3 = DATABASE.Column(DATABASE.String(100), nullable = True)
    variant_4 = DATABASE.Column(DATABASE.String(100), nullable = True)
    variant_5 = DATABASE.Column(DATABASE.String(100), nullable = True)

    correct_answer = DATABASE.Column(DATABASE.JSON())

    quiz_id = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey('quiz.id'))
    image = DATABASE.Column(DATABASE.String(100), nullable = True)

class Result(DATABASE.Model):
    id = DATABASE.Column(DATABASE.Integer, primary_key = True)
    name = DATABASE.Column(DATABASE.String(100))
    description = DATABASE.Column(DATABASE.String(100))
    who_passed = DATABASE.Column(DATABASE.String(50))
    what_passed = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey('quiz.id'))
    by_code = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey('redeem_code.id'))
    right_answers = DATABASE.Column(DATABASE.Integer)
    correct_answers = DATABASE.Column(DATABASE.Integer)
    all_answers = DATABASE.Column(DATABASE.Integer)
    name_teacher = DATABASE.Column(DATABASE.String(100))
    

class RedeemCode(DATABASE.Model):
    id = DATABASE.Column(DATABASE.Integer, primary_key = True)
    name = DATABASE.Column(DATABASE.String(100), nullable = False)
    quiz = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey("quiz.id"))
    code_enter = DATABASE.Column(DATABASE.Integer)
    hosted_by = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey("user.id"))
    room_id = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey("room.id"))
    results = DATABASE.relationship(Result, backref = 'redeemcode', lazy = True)

class Room(DATABASE.Model):
    __tablename__ = 'room'
    id = DATABASE.Column(DATABASE.Integer, primary_key=True)
    students = DATABASE.Column(DATABASE.JSON())
    index_question = DATABASE.Column(DATABASE.Integer)
    quiz = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey("quiz.id"))
    host = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey("user.id"))
    status = DATABASE.Column(DATABASE.String, default= "waiting")
    answered_students = DATABASE.Column(DATABASE.Integer, default=0)
    redeem_codes = DATABASE.relationship("RedeemCode", backref="room", lazy=True)



class Quiz(DATABASE.Model):
    id = DATABASE.Column(DATABASE.Integer, primary_key = True)
    name = DATABASE.Column(DATABASE.String(100), nullable = False)
    description = DATABASE.Column(DATABASE.String, nullable = False)
    count_questions = DATABASE.Column(DATABASE.Integer, nullable = False)
    author_id = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey('user.id'))
    image = DATABASE.Column(DATABASE.String(100), nullable = False)
    questions = DATABASE.relationship(Question, backref = 'quiz', lazy = True)
    codes = DATABASE.relationship(RedeemCode, backref = 'quiz1', lazy = True)
    results = DATABASE.relationship(Result, backref = 'quiz2', lazy=True)
    rooms = DATABASE.relationship(Room, backref="roomsQuiz", lazy=True)
