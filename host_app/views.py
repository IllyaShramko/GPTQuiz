from library_app.models import Quiz, RedeemCode, Room, Question
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
        if flask.request.form["btn"] == "host":
            redeem_code= generate_code()
            
            room = Room(quiz = quiz.id, host= flask_login.current_user.id)
            DATABASE.session.add(room)
            DATABASE.session.flush()
            
            code_db= RedeemCode(
                quiz= quiz,
                name = quiz.name,
                code_enter= redeem_code,
                hosted_by= flask_login.current_user.id,
                room_id= room.id
            )
            try:
                DATABASE.session.add(code_db)
                DATABASE.session.commit()
                code = redeem_code
                return flask.redirect(flask.url_for("host_app.render_hosting_quiz", code=code))
            except Exception as e:
                print(e)
        elif flask.request.form["btn"] == "delete":
            try:
                questions = Question.query.filter_by(quiz_id=quiz.id).all()
                for q in questions:
                    DATABASE.session.delete(q)
                DATABASE.session.delete(quiz)
                DATABASE.session.commit()
            except Exception as e:
                DATABASE.session.rollback()
                print("Error: ", e)
            return flask.redirect("/admin/")
            

        
            
        
    return flask.render_template(
        "previewQuiz.html", quiz = quiz, code= code,
        username = flask_login.current_user.login,
        user = flask_login.current_user
        )


def render_hosting_quiz(code):
    
    return flask.render_template("hosting.html", code=code)