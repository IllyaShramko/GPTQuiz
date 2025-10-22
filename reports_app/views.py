import flask, flask_login
from library_app.models import Quiz, RedeemCode, StudentReport, Room, SessionParticipant, SessionAnswer
from project.settings import DATABASE

def render_reports_page():
    rooms = Room.query.filter_by(host=flask_login.current_user.id).all() 
    for room in rooms:
        reports = room.student_reports
        if reports and len(reports) > 0:
            
            room.success_rate = int(sum(r.percentage for r in reports) / len(reports))
            print(len(reports))
        else:
            room.success_rate = 0
            print(0)
    return flask.render_template(
        template_name_or_list='reports.html',
        rooms=rooms,
        username = flask_login.current_user.login
    )

def render_detail_report(room_id):
    room = Room.query.get_or_404(room_id)
    if room.host != flask_login.current_user.id:
        return {"error": "forbidden"}, 403
    if flask.request.method == "POST":
        try:
            DATABASE.session.delete(room)
            DATABASE.session.commit()
        except Exception as e:
            print(e)
            DATABASE.session.rollback()
            return {"error": "internal server error"}, 500
        return flask.redirect("/reports/")
    report_data = room.get_report()
    return flask.render_template("detail_report.html", report=report_data, room=room, username = flask_login.current_user.login)

def get_student_report(student_id):
    student = SessionParticipant.query.get(student_id)
    if not student:
        return {"error": "not found"}, 404

    answers = SessionAnswer.query.filter_by(participant_id=student.id).all()

    return {
        "id": student.id,
        "nickname": student.nickname,
        "answers": [
            {
                "question_text": ans.question_obj.name if ans.question_obj else "",
                "type": ans.question_obj.type,
                "answer": ans.get_answer(ans.answer) if ans.question_obj else ans.answer,
                "is_correct": ans.is_correct,
                "correct_answer": ans.right_answers() if ans.question_obj else None
            }
            for ans in answers
        ]
    }
