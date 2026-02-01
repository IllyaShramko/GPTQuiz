import flask, flask_login, datetime
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

def get_student_stats(student_id):
    start_date_str = flask.request.args.get('start_date')
    end_date_str = flask.request.args.get('end_date')

    query = StudentReport.query.filter_by(student_id=student_id)

    if start_date_str:
        start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
        query = query.filter(StudentReport.created_at >= start_date)

    if end_date_str:
        end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').replace(hour=23, minute=59, second=59)
        query = query.filter(StudentReport.created_at <= end_date)

    reports = query.order_by(StudentReport.created_at.asc()).all()

    data = {
        "dates": [r.created_at.strftime('%Y-%m-%d') for r in reports],
        "grades": [r.grade for r in reports],
        "hashes": [r.hash_code for r in reports],
        "pie_data": {}
    }

    for r in reports:
        g_label = f"Оцінка {r.grade}" if r.grade is not None else "Без оценки"
        data["pie_data"][g_label] = data["pie_data"].get(g_label, 0) + 1

    return flask.jsonify(data)

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