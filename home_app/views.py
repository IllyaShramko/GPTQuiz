import flask, flask_login

def render_home_page():

    if flask_login.current_user.is_authenticated:
        return flask.redirect("/admin/")
    
    return flask.render_template(
        template_name_or_list= 'home.html'
    )