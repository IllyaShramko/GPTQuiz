import flask
from sqlalchemy import UniqueConstraint
from project.settings import DATABASE
import uuid
# from user_app.models import User

import uuid
from sqlalchemy.sql import func

class StudentReport(DATABASE.Model):
    __tablename__ = "student_report"

    id = DATABASE.Column(DATABASE.Integer, primary_key=True)

    participant_id = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey("session_participant.id"), nullable=False)
    room_id = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey("room.id"), nullable=False)

    total_questions = DATABASE.Column(DATABASE.Integer, nullable=False, default=0)
    correct_answers = DATABASE.Column(DATABASE.Integer, nullable=False, default=0)
    wrong_answers = DATABASE.Column(DATABASE.Integer, nullable=False, default=0)

    score = DATABASE.Column(DATABASE.Integer, nullable=False, default=0)       
    max_score = DATABASE.Column(DATABASE.Integer, nullable=False, default=0)   
    percentage = DATABASE.Column(DATABASE.Integer, nullable=False, default=0)  

    grade = DATABASE.Column(DATABASE.String(10), nullable=True)                

    hash_code = DATABASE.Column(DATABASE.String(64), unique=True, nullable=False, default=lambda: uuid.uuid4().hex)
    created_at = DATABASE.Column(DATABASE.DateTime, server_default=func.now())

    participant = DATABASE.relationship("SessionParticipant", backref="reports", lazy=True)
    room = DATABASE.relationship("Room", backref="student_reports", lazy=True)

    def calculate_from_answers(self, answers):
        self.total_questions = len(answers)
        self.correct_answers = sum(1 for a in answers if a.is_correct)
        self.wrong_answers = self.total_questions - self.correct_answers

        self.max_score = self.total_questions
        self.score = self.correct_answers
        self.percentage = round((self.correct_answers / self.total_questions) * 100) if self.total_questions else 0

        self.grade = str(round(self.percentage * 12 / 100))

    def to_dict(self):
        return {
            "participant": self.participant.nickname if self.participant else None,
            "room_id": self.room_id,
            "total_questions": self.total_questions,
            "correct_answers": self.correct_answers,
            "wrong_answers": self.wrong_answers,
            "score": self.score,
            "max_score": self.max_score,
            "percentage": self.percentage,
            "grade": self.grade,
            "hash_code": self.hash_code,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class Question(DATABASE.Model):
    __tablename__ = 'question'

    id = DATABASE.Column(DATABASE.Integer, primary_key=True)
    name = DATABASE.Column(DATABASE.String(100), nullable=False)
    type = DATABASE.Column(DATABASE.String(100), nullable=False)
    variant_1 = DATABASE.Column(DATABASE.String(100), nullable=False)
    variant_2 = DATABASE.Column(DATABASE.String(100), nullable=True)
    variant_3 = DATABASE.Column(DATABASE.String(100), nullable=True)
    variant_4 = DATABASE.Column(DATABASE.String(100), nullable=True)
    variant_5 = DATABASE.Column(DATABASE.String(100), nullable=True)
    correct_answer = DATABASE.Column(DATABASE.JSON)
    quiz_id = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey('quiz.id'), nullable=False)
    image = DATABASE.Column(DATABASE.String(255), nullable=True)

    answers = DATABASE.relationship("SessionAnswer", back_populates="question_obj", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "question_text": self.name,
            "type": self.type,
            "variants": [v for v in [self.variant_1, self.variant_2, self.variant_3, self.variant_4, self.variant_5] if v],
            "correct_answer": self.correct_answer,
            "quiz_id": self.quiz_id,
            "image": self.image,
            "answers": [a.to_dict() for a in self.answers] if self.answers else []
        }
    
    



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
    date = DATABASE.Column(DATABASE.DateTime, server_default=func.now())
    def get_report(self):
        from .models import SessionParticipant, SessionAnswer, Question

        participants = SessionParticipant.query.filter_by(room_id=self.id).all()
        report = []

        for p in participants:
            answers = SessionAnswer.query.filter_by(room_id=self.id, participant_id=p.id).all()
            total_questions = len(answers)
            correct = sum(1 for a in answers if a.is_correct)
            percent = (correct * 100 // total_questions) if total_questions else 0

            answers_data = []
            for a in answers:
                q = Question.query.get(a.question)
                answers_data.append({
                    "question_id": q.id,
                    "question_text": q.name,
                    "your_answer": a.answer,
                    "is_correct": a.is_correct
                })

            report.append({
                "participant_id": p.id,
                "nickname": p.nickname,
                "percent": percent,
                "answers": answers_data
            })

        return sorted(report, key=lambda x: x["percent"], reverse=True)



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
    session_id = DATABASE.Column(DATABASE.String(255), nullable=True)
    is_connected = DATABASE.Column(DATABASE.Boolean, default=True)
    __table_args_ = (UniqueConstraint("room_id", "nickname", "session_id", name="uq_partc_once"))

class SessionAnswer(DATABASE.Model):
    __tablename__ = "session_answer"

    id = DATABASE.Column(DATABASE.Integer, primary_key=True)
    room_id = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey("room.id"))
    question = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey("question.id"))
    participant_id = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey("session_participant.id"))
    answer = DATABASE.Column(DATABASE.JSON(), nullable=True)
    is_correct = DATABASE.Column(DATABASE.Boolean, default=False)

    question_obj = DATABASE.relationship("Question", back_populates="answers")
    __table_args__ = (UniqueConstraint('room_id', 'participant_id', 'question', name='uq_answer_once'),)

    def to_dict(self):
        question = self.question_obj
        return {
            "id": self.id,
            "participant_id": self.participant_id,
            "question": self.question,
            "question_text": question.name if question else "",
            "variants": [v for v in [
                question.variant_1,
                question.variant_2,
                question.variant_3,
                question.variant_4,
                question.variant_5
            ] if v] if question else [],
            "answer": self.answer,
            "is_correct": self.is_correct
        }
    def right_answers(self):
        question = self.question_obj
        if not question:
            return []
        if question.type == "one answer":
            if int(question.correct_answer) == 1:
                return [question.variant_1]
            elif int(question.correct_answer) == 2:
                return [question.variant_2]
            elif int(question.correct_answer) == 3:
                return [question.variant_3]
            elif int(question.correct_answer) == 4:
                return [question.variant_4]
            elif int(question.correct_answer) == 5:
                return [question.variant_5]
        elif question.type == "multiple answers":
            answers = []
            for ans in question.correct_answer:
                if ans == "1":
                    answers.append(question.variant_1)
                elif ans == "2":
                    answers.append(question.variant_2)
                elif ans == "3":
                    answers.append(question.variant_3)
                elif ans == "4":
                    answers.append(question.variant_4)
                elif ans == "5":
                    answers.append(question.variant_5)
            print(question.type, answers)
            return answers
        elif question.type == "enter answer":
            return question.correct_answer if question.correct_answer else []
        return []
    def get_answer(self, answersswer):
        question = self.question_obj
        if question.type == "one answer":
            print(answersswer, "Adlsldsldladl")
            if "Пропущений..." in [answersswer]:
                return ["Пропущений"]
            if int(answersswer) == 1:
                return [question.variant_1]
            elif int(answersswer) == 2:
                return [question.variant_2]
            elif int(answersswer) == 3:
                return [question.variant_3]
            elif int(answersswer) == 4:
                return [question.variant_4]
            elif int(answersswer) == 5:
                return [question.variant_5]
        elif question.type == "multiple answers":
            if isinstance(question.correct_answer, list):
                answers = []
                print(answersswer, type(answersswer))
                if not answersswer or "Пропущений..." in answersswer:
                    answers.append("Пропущений")
                    return answers
                for ans in answersswer:
                    if int(ans) == 1:
                        answers.append(question.variant_1)
                    elif int(ans) == 2:
                        answers.append(question.variant_2)
                    elif int(ans) == 3:
                        answers.append(question.variant_3)
                    elif int(ans) == 4:
                        answers.append(question.variant_4)
                    elif int(ans) == 5:
                        answers.append(question.variant_5)
                print(question.type, answers)
                return answers
        elif question.type == "enter answer":
            return answersswer

