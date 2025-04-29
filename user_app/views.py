import flask
from .models import User
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
            return flask.redirect('/')
        except:
            return "Не вдалося створити користувача"  
            
            
        
    return flask.render_template(template_name_or_list='signup.html')


def render_login():
    return flask.render_template(template_name_or_list= 'login.html')

def render_history():
    return flask.render_template(template_name_or_list= 'history.html')