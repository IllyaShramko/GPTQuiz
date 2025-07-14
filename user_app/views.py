import flask
import flask_login
from .models import User
from project import login_manager
from project.settings import DATABASE


def render_signup():
    if flask.request.method == 'POST':
        user= User(
            login = flask.request.form['login'],
            name = flask.request.form['name'],
            surname = flask.request.form['surname'],
            email = flask.request.form['email'],
            password = flask.request.form['password']
        )
        try:
            DATABASE.session.add(user)
            DATABASE.session.commit()
            return flask.redirect('/login/')
        except:
            return "Не вдалося створити користувача"  
            
            
        
    return flask.render_template(template_name_or_list='signup.html')


def render_login():
    if flask.request.method == "POST":
        for user in User.query.filter_by(login = flask.request.form['login']):
            if user.password == flask.request.form['password']:
                flask_login.login_user(user)
                return flask.redirect('/admin/')
    return flask.render_template(template_name_or_list= 'login.html')

def render_profile():
    user = flask_login.current_user
    return flask.render_template(
        template_name_or_list="profile.html",
        user = user,
        username = flask_login.current_user.login
    )


def logout():
    flask_login.logout_user()
    return flask.redirect("/")
    