import flask, flask_login
from library_app.models import Quiz

def render_home_page():

    if flask_login.current_user.is_authenticated:
        role = flask.session.get('user_role') 
        if role == 'teacher':
            return flask.redirect("/admin/")
        if role == 'student':
            return flask.redirect("/student/")
    quizes= Quiz.query.filter_by(is_draft = False).all()
    print(quizes)
    return flask.render_template(
        template_name_or_list= 'home.html',
        quizes = quizes
    )