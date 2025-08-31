from library_app.models import Quiz, RedeemCode
import flask, random, flask_login
from project.settings import DATABASE

def generate_code():
    num1= random.randint(0,9)
    num2= random.randint(0,9)
    num3= random.randint(0,9)
    num4= random.randint(0,9)
    num5= random.randint(0,9)
    num6= random.randint(0,9)
    
    code= f"{num1}{num2}{num3}{num4}{num5}{num6}"
    return int(code)

def render_host_app(quizid):
    if not flask_login.current_user.is_authenticated:
        return flask.redirect(flask.url_for("user_app.render_login"))
    quiz = Quiz.query.get(ident=quizid)
    code = 000000
    if flask.request.method == "POST":
        redeem_code= generate_code()
        code_db= RedeemCode(
            quiz= quiz.id,
            name = quiz.name,
            code_enter= redeem_code,
            hosted_by= flask_login.current_user.id
            
        )
        try:
            DATABASE.session.add(code_db)
            DATABASE.session.commit()
            code = redeem_code
        except:
            print(Exception)

        
            
        
    return flask.render_template(
        "host.html", quiz = quiz, code= code,
        username = flask_login.current_user.login
        )