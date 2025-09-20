import flask, flask_login
from library_app.models import Quiz, RedeemCode
from project.settings import DATABASE

def render_reports_page():

    if flask.request.method == "POST":
        btn = flask.request.form.get("action")
        action = btn.split(";")[0]
        code_id = btn.split(";")[1]

        redeem_code = RedeemCode.query.get(code_id)
        if redeem_code:
            DATABASE.session.delete(redeem_code)
            DATABASE.session.commit()
            flask.flash("Redeem code deleted successfully.", "success")
        else:
            flask.flash("Redeem code not found.", "error")
            
    redeem_codes = flask_login.current_user.hosted 

    return flask.render_template(
        template_name_or_list='reports.html',
        redeem_codes = redeem_codes
    )
