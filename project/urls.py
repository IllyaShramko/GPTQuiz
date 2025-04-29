from .settings import project
import home_app, user_app

home_app.home_app.add_url_rule(
    rule= '/',
    view_func= home_app.render_home_page
)
project.register_blueprint(blueprint= home_app.home_app)
# 
user_app.user_app.add_url_rule(
    rule= '/signup/',
    view_func= user_app.render_signup,
    methods= ["POST", "GET"]
)
user_app.user_app.add_url_rule(
    rule= '/login/',
    view_func= user_app.render_login,
    methods= ["POST", "GET"]
)
user_app.user_app.add_url_rule(
    rule = '/history/',
    view_func= user_app.render_history,
)
project.register_blueprint(blueprint= user_app.user_app)