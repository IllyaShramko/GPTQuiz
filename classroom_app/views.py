import flask, flask_login
from .models import GroupClass, Student
def render_classrooms():
    class_groups = GroupClass.query.filter_by(teacher_id = flask_login.current_user.id).all()
    return flask.render_template(
        "classrooms.html",
        username = flask_login.current_user.login,
        class_groups = class_groups,
    )