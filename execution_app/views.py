import flask, flask_login 
from library_app.models import RedeemCode, Quiz, Question, SessionAnswer, SessionParticipant, StudentReport, Room
from project.settings import DATABASE
from user_app.models import User
from flask import session, request, make_response

def render_enter_code():
    code = flask.request.args.get("code")
    print(code)
    print(flask.session)
    if code:
        quiz = Quiz.query.get(RedeemCode.query.filter_by(code_enter=code)[0].quiz)
        return flask.render_template(
            template_name_or_list= 'enter_nickname.html',
            quiz=quiz
        )
    return flask.render_template(
        template_name_or_list="enter_code.html"
    )

def report_view(hash_code):
    report = StudentReport.query.filter_by(hash_code=hash_code).first_or_404()
    participant = SessionParticipant.query.get(report.participant_id)
    print(report.participant_id)
    room = report.room

    host = User.query.get(room.host)
    name_teacher = f'{host.surname} {host.name}'
    print(name_teacher)
    answers = SessionAnswer.query.filter_by(room_id=room.id, participant_id=participant.id).all()

    gradef = int(report.percentage / 100 * 12 // 1)
    num = report.percentage / 100 * 12 - gradef
    if num >= 0.5:
        gradef += 1
    
    questions = []
    for a in answers:
        q = Question.query.get(a.question)
        questions.append({
            "id": q.id,
            "text": q.name,
            "type": q.type,
            "your_answer": a.get_answer(a.answer),
            "correct_answer": a.right_answers(),
            "is_correct": a.is_correct,
        })

    return flask.render_template("student_report.html", gradef= gradef, name_teacher=name_teacher, report=report, participant=participant, quiz=room.roomsQuiz, questions=questions)