import flask, flask_login 
from library_app.models import RedeemCode, Quiz, Question, Result
from project.settings import DATABASE
from user_app.models import User
from flask import session, request, make_response

def render_enter_code():
    code = flask.request.args.get("code")
    print(code)
    if code:
        quiz = Quiz.query.get(RedeemCode.query.filter_by(code_enter=code)[0].quiz)
        return flask.render_template(
            template_name_or_list= 'enter_nickname.html',
            quiz=quiz
        )
    return flask.render_template(
        template_name_or_list="enter_code.html"
    )
def passing_quiz(quiz_id, question_index, result_id):
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return "Quiz not found", 404
    
    result= Result.query.get(result_id)
    
    if not result:
        print(RedeemCode.query.filter_by(code_enter = session.get('code')).first().id)
        result = Result(
            name = quiz.name,
            description = quiz.description,
            who_passed= flask_login.current_user.id,
            what_passed= quiz_id,
            right_answers= 0,
            by_code= RedeemCode.query.filter_by(code_enter = session.get('code')).first().id,
            correct_answers= 0,
            all_answers= quiz.count_questions,
            name_teacher = "",
        )
        try:
            DATABASE.session.add(result)
            DATABASE.session.commit()
        except:
            print(Exception)

    questions = quiz.questions

    if question_index < 0 or question_index >= len(questions):

        passed_cookie = request.cookies.get("Passed", "")
        if passed_cookie:
            passed_ids = passed_cookie.split(",")
        else:
            passed_ids = []
        if str(result.id) not in passed_ids:
            passed_ids.append(str(result.id))

        response = make_response(flask.redirect(f"/result/{result.id}"))
        response.set_cookie("Passed", ",".join(passed_ids), max_age=60*60*24*30)

        return response

    now_question = questions[question_index]

    if flask.request.method == "POST":

        if now_question.type == "one answer":
            user_answer = flask.request.form.get("button").split(";")[1]
            if user_answer == now_question.correct_answer:
                print("success")
                result.right_answers += 1
                result.correct_answers += 1
                DATABASE.session.commit()
            else:
                print("not success")
            return flask.redirect(f"/quiz/{quiz.id}/{question_index + 1}/{result.id}")
        elif now_question.type == "multiple answers":
            user_answer = flask.request.form.getlist("answer")
            if user_answer == now_question.correct_answer:
                print("success")
                result.right_answers += 1
                result.correct_answers += 1
                DATABASE.session.commit()
            else:
                print("not success")
            return flask.redirect(f"/quiz/{quiz.id}/{question_index + 1}/{result.id}")
        
        elif now_question.type == "enter answer":
            user_answer = flask.request.form.get("answer")
            if user_answer == now_question.correct_answer:
                print("success")
                result.right_answers += 1
                result.correct_answers += 1
                DATABASE.session.commit()
            else:
                print("not success")
            return flask.redirect(f"/quiz/{quiz.id}/{question_index + 1}/{result.id}")


    return flask.render_template("passing.html", question=now_question)

def render_results(result_id):
    result= Result.query.get(result_id)
    quiz= Quiz.query.get(result.what_passed)
    right= result.right_answers
    incorrect = quiz.count_questions - right 
    all_count= quiz.count_questions
    percent= f"{right*100//all_count}"
    rating = f"{int(12 / all_count * right // 1)}"
    author = User.query.get(quiz.author_id)
    if author.name:
        name_author = f"{author.surname} {author.name}"
    else:
        name_author = author.login

    return flask.render_template('summary.html', right= right, incorrect= incorrect, all_count= all_count, percent= percent, rating= rating, name_author=name_author)
