import flask, flask_login
from library_app.models import Quiz, RedeemCode, Result

def render_reports_page():
    redeem_codes = flask_login.current_user.hosted 

    print(f"Redeem Codes: {redeem_codes}")

    for code in redeem_codes:
        print(f'results: {code.results}')

    return flask.render_template(
        template_name_or_list='reports.html',
        redeem_codes = redeem_codes
    )
