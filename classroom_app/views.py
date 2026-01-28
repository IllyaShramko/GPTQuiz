import flask, flask_login
from project.settings import DATABASE
from .models import GroupClass, Student

def render_classrooms():
    if flask.request.method == "POST":
        number = flask.request.form["number"]
        char   = flask.request.form["char"]
        new_class = GroupClass(
            number= number,
            char= char,
            teacher_id = flask_login.current_user.id
        )
        try:
            DATABASE.session.add(new_class)
            DATABASE.session.commit()
        except:
            print("Error while creating new class", number, char)
    class_groups = GroupClass.query.filter_by(teacher_id = flask_login.current_user.id).all()
    return flask.render_template(
        "classrooms.html",
        username = flask_login.current_user.login,
        class_groups = class_groups,
    )

def render_classroom(id):
    classroom = GroupClass.query.get(id)
    if not classroom:
        return flask.redirect("/classrooms/")
    new_student = None
    if flask.request.method == "POST":
        student_login = flask.request.form["student_login"]
        student_name = flask.request.form["student_name"]
        student_surname = flask.request.form["student_surname"]
        new_student = Student(
            login= student_login,
            name= student_name,
            surname= student_surname,
            my_class_id = id
        )
        try:
            DATABASE.session.add(new_student)
            DATABASE.session.commit()
        except:
            print("Error while creating new student", student_login, student_name, student_surname)

    return flask.render_template(
        "class.html",
        username = flask_login.current_user.login,
        classroom= classroom,
        new_student= new_student
    )