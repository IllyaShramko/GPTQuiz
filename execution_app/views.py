import flask, flask_login 
from library_app.models import RedeemCode, Quiz, Question, SessionAnswer, SessionParticipant, StudentReport, Room
from project.settings import DATABASE
from user_app.models import User
from classroom_app.models import Student

def render_login_student():
    if flask.request.method == "POST":
        for student in Student.query.filter_by(login = flask.request.form['login']):
            if student.password == flask.request.form['password']:
                flask_login.login_user(student)
                flask.session['user_role'] = 'student'
                return flask.redirect('/execution/')
    return flask.render_template(template_name_or_list= 'login_student.html')

def render_enter_code():
    if not flask_login.current_user.is_authenticated:
        return flask.redirect("/login_student/")
    if flask.session.get("user_role") != "student":
        return flask.redirect("/login_student/")
    
    code = flask.request.args.get("code")
    if code:
        quiz = RedeemCode.query.filter_by(code_enter= code).first_or_404().quiz
        room = RedeemCode.query.filter_by(code_enter=code).first().room
        teacher = User.query.get(room.host)
        username = flask_login.current_user.surname + " " + flask_login.current_user.name
        return flask.render_template(
            template_name_or_list= 'enter_nickname.html',
            quiz=quiz, teacher=teacher, username= username, student= flask_login.current_user
        )
    return flask.render_template(
        template_name_or_list="enter_code.html"
    )

