import flask, flask_login

def render_history():
    cookie = flask.request.cookies.get("Passed", "Not Found")
    results = []
    if cookie != "Not Found":
        # result_ids = cookie.split(",")

        # result_ids = [int(x) for x in cookie.split(",") if x.isdigit()]

        # results = SessionParticipant.query.filter(SessionParticipant.id.in_(result_ids)).all()

        print(results)

    return flask.render_template(
        template_name_or_list = "history.html",
        username = flask_login.current_user.login,
        results = results
    )