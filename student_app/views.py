import flask, flask_login
from classroom_app import Student
from library_app.models import Question, SessionAnswer, SessionParticipant, StudentReport
from user_app.models import User

def render_student_page():
    student= Student.query.get(flask_login.current_user.id)
    
    results = student.my_reports
    print(results)

    return flask.render_template(
        template_name_or_list= 'student_home.html',
        current_user = flask_login.current_user,
        results = results
    )

def get_data_from_student():
    student= Student.query.get(flask_login.current_user.id)
    results = student.my_reports

    

def report_view(hash_code):
    report = StudentReport.query.filter_by(hash_code=hash_code).first_or_404()
    participant = SessionParticipant.query.get(report.participant_id)
    room = report.room
    answers = SessionAnswer.query.filter_by(room_id=room.id, participant_id=participant.id).all()
    questions = []
    host = User.query.get(room.host)
    name_teacher = f'{host.surname} {host.name}'
    skipped = 0
    for a in answers:
        if a.answer == "Пропущений..." or a.answer == "Пропущений":
            skipped += 1
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
    
    print(name_teacher)

    gradef = int(report.percentage / 100 * 12 // 1)
    num = report.percentage / 100 * 12 - gradef
    if num >= 0.5:
        gradef += 1
    

    return flask.render_template(
        "student_report.html",
        gradef= gradef,
        name_teacher=name_teacher,
        report=report,
        participant=participant,
        quiz=roomsquiz,
        questions=questions,
        ignore_links=True,
        answers=answers,
        skipped_answers= skipped
    )