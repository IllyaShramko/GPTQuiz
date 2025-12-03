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
        username = None
        if flask_login.current_user.is_authenticated:
            username = flask_login.current_user.name + " " + flask_login.current_user.surname
        room = RedeemCode.query.filter_by(code_enter=code).first().room
        teacher = User.query.get(room.host)
        return flask.render_template(
            template_name_or_list= 'enter_nickname.html',
            quiz=quiz, username=username, teacher=teacher
        )
    return flask.render_template(
        template_name_or_list="enter_code.html"
    )

def report_view(hash_code):
    report = StudentReport.query.filter_by(hash_code=hash_code).first_or_404()
    participant = SessionParticipant.query.get(report.participant_id)
    print(report.participant_id)
    room = report.room
    questions = []
    if room:
        host = User.query.get(room.host)
        name_teacher = f'{host.surname} {host.name}'
        answers = SessionAnswer.query.filter_by(room_id=room.id, participant_id=participant.id).all()
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
        roomsquiz = room.roomsQuiz
    else:
        host = None
        name_teacher = f'Невідомо'
        answers = []
        roomsquiz = None
    
    print(name_teacher)

    gradef = int(report.percentage / 100 * 12 // 1)
    num = report.percentage / 100 * 12 - gradef
    if num >= 0.5:
        gradef += 1
    

    return flask.render_template("student_report.html", gradef= gradef, name_teacher=name_teacher, report=report, participant=participant, quiz=roomsquiz, questions=questions, is_auth=flask_login.current_user.is_authenticated)