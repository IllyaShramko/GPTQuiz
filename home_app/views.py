import flask, flask_login
from library_app.models import Quiz

def render_home_page():

    if flask_login.current_user.is_authenticated:
        return flask.redirect("/admin/")
    quizes= Quiz.query.all()[:4]
    print(quizes)
    return flask.render_template(
        template_name_or_list= 'home.html',
        quizes = quizes
    )