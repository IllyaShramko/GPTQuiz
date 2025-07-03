import flask, flask_login 
from library_app.models import RedeemCode, Quiz, Question, Result
from project.settings import DATABASE

def render_execution_page(code):
    quiz = Quiz.query.get(RedeemCode.query.filter_by(code_enter=code)[0].quiz)
    if flask.request.method == "POST":
        nickname = flask.request.form.get("input-nickname")
        print(nickname)
        result = Result(
            who_passed= flask_login.current_user.id,
            what_passed= quiz.id,
            right_answers= 0
        )
        try:
            DATABASE.session.add(result)
            DATABASE.session.commit()
        except:
            print(Exception)
        return flask.redirect(f"/quiz/{quiz.id}/0/{result.id}")
    print(quiz.name)
    return flask.render_template(
        template_name_or_list= 'enter_nickname.html'
    )

def render_enter_code():
    if flask.request.method == "POST":
        code = flask.request.form["input-code"]
        redeem_code = RedeemCode.query.filter_by(code_enter = code)
        if redeem_code:
            return flask.redirect(f"/execution/{code}")

    return flask.render_template(
        template_name_or_list="enter_code.html"
    )
def passing_quiz(quiz_id, question_index, result_id):
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return "Quiz not found", 404
    
    result= Result.query.get(result_id)
    
    if not result:
        print(result)
        result = Result(
            who_passed= flask_login.current_user.id,
            what_passed= quiz_id,
            right_answers= 0
        )
        try:
            DATABASE.session.add(result)
            DATABASE.session.commit()
        except:
            print(Exception)

    questions = quiz.questions
    if question_index < 0 or question_index >= len(questions):
        return flask.redirect(f"/result/{result.id}")

    now_question = questions[question_index]

    if flask.request.method == "POST":

        if now_question.type == "one answer":
            user_answer = flask.request.form.get("answer")
            if user_answer == now_question.correct_answer:
                print("success")
                result.right_answers += 1
                DATABASE.session.commit()
            else:
                print("not success")
            return flask.redirect(f"/quiz/{quiz.id}/{question_index + 1}/{result.id}")
        elif now_question.type == "multiple answers":
            user_answer = flask.request.form.getlist("answer")
            if user_answer == now_question.correct_answer:
                print("success")
                result.right_answers += 1
                DATABASE.session.commit()
            else:
                print("not success")
            return flask.redirect(f"/quiz/{quiz.id}/{question_index + 1}/{result.id}")
        
        elif now_question.type == "enter answer":
            user_answer = flask.request.form.get("answer")
            if user_answer == now_question.correct_answer:
                print("success")
                result.right_answers += 1
                DATABASE.session.commit()
            else:
                print("not success")
            return flask.redirect(f"/quiz/{quiz.id}/{question_index + 1}/{result.id}")


    return flask.render_template("passing.html", question=now_question)

def render_results(result_id):
    result= Result.query.get(result_id)
    quiz= Quiz.query.get(result.what_passed)
    right= result.right_answers
    all_count= quiz.count_questions
    percent= f"{right*100//all_count}%"

    return flask.render_template('summary.html', right= right, all_count= all_count, percent= percent)
