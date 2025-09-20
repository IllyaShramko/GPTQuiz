import flask
from project.settings import DATABASE
# from user_app.models import User

class Question(DATABASE.Model):
    __tablename__ = 'question'
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
    answers = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey("session_answer.id"), nullable = True)



class RedeemCode(DATABASE.Model):
    id = DATABASE.Column(DATABASE.Integer, primary_key = True)
    name = DATABASE.Column(DATABASE.String(100), nullable = False)
    quiz = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey("quiz.id"))
    code_enter = DATABASE.Column(DATABASE.Integer)
    hosted_by = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey("user.id"))
    room_id = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey("room.id"))

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
    participants = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey("session_participant.id"), nullable=True)



class Quiz(DATABASE.Model):
    id = DATABASE.Column(DATABASE.Integer, primary_key = True)
    name = DATABASE.Column(DATABASE.String(100), nullable = False)
    description = DATABASE.Column(DATABASE.String, nullable = False)
    count_questions = DATABASE.Column(DATABASE.Integer, nullable = False)
    author_id = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey('user.id'))
    image = DATABASE.Column(DATABASE.String(100), nullable = False)
    questions = DATABASE.relationship(Question, backref = 'quiz', lazy = True)
    codes = DATABASE.relationship(RedeemCode, backref = 'quiz1', lazy = True)
    rooms = DATABASE.relationship(Room, backref="roomsQuiz", lazy=True)


class SessionParticipant(DATABASE.Model):
    id = DATABASE.Column(DATABASE.Integer, primary_key = True)
    room_id = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey('room.id'))
    nickname = DATABASE.Column(DATABASE.String(100), nullable = False)
    

class SessionAnswer(DATABASE.Model):
    id = DATABASE.Column(DATABASE.Integer, primary_key = True)
    room_id = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey('room.id'))
    question = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey('question.id'))
    participant_id = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey('session_participant.id'))
    answer = DATABASE.Column(DATABASE.String(100), nullable = False)
    is_correct = DATABASE.Column(DATABASE.Boolean, default = False)
    
