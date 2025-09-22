import flask, flask_login
from library_app.models import Quiz, RedeemCode, Room
from project.settings import DATABASE

def render_reports_page():
            
    rooms = Room.query.filter_by(host= flask_login.current_user.id)

    return flask.render_template(
        template_name_or_list='reports.html',
        rooms = rooms
    )

def render_detail_report(room_id):
    room = Room.query.get_or_404(room_id)
    report_data = room.get_report()
    return flask.render_template("detail_report.html", report=report_data, room=room)
