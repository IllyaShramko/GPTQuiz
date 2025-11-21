import flask, flask_login
from library_app.models import SessionParticipant, StudentReport

def render_history():

    return flask.render_template(
        template_name_or_list = "history.html",
        username = flask_login.current_user.login,
        # results = results
    )