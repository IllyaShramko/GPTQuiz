import flask, flask_login
from library_app.models import Result, RedeemCode

def render_reports_page():

    redeem_codes = flask_login.current_user.hosted

    results = []

    print(redeem_codes)

    for code in redeem_codes:
        result = Result.query.filter_by(what_passed=code.quiz)
        print(result.all())
        if result:
            results.extend(result)

    print(results)

    return flask.render_template(
        template_name_or_list= 'reports.html'
    )