import flask, flask_login
from classroom_app import Student
from project import login_manager

def render_student_page():
    student= Student.query.get(flask_login.current_user.id)
    
    results = student.my_reports

    return flask.render_template(
        template_name_or_list= 'student_home.html',
        current_user = flask_login.current_user,
        results = results
    )
