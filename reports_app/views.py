import flask, flask_login
from library_app.models import Quiz, RedeemCode, Result

def render_reports_page():
    redeem_codes = flask_login.current_user.hosted 
    quiz_ids = list({code.quiz for code in redeem_codes})  
    quizzes = Quiz.query.filter(Quiz.id.in_(quiz_ids)).all()
    results = Result.query.filter(Result.what_passed.in_(quiz_ids)).all()

    print(f"Quizzes: {quizzes}", f"Redeem Codes: {redeem_codes}", f"Results: {results}")
    
    return flask.render_template(
        template_name_or_list='reports.html',
        quizzes=quizzes,
        redeem_codes=redeem_codes,
        results=results
    )
