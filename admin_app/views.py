import flask, flask_login
from library_app.models import Quiz
from project import login_manager

def render_admin_page():
    quizes= Quiz.query.filter(Quiz.is_draft == False)

    return flask.render_template(
        template_name_or_list= 'admin.html',
        username = flask_login.current_user.login,
        quizes = quizes
    )

def search():
    data = flask.request.get_json()
    search_text = data.get('search', '')

    quizes = Quiz.query.filter(Quiz.is_draft == False)

    if search_text:
        quizes = quizes.filter(Quiz.name.ilike(f'%{search_text}%'))

    quizes = quizes.all()
    print(f"Search text: {search_text}, Found quizes: {[q.image for q in quizes]}")
    return flask.jsonify([q.to_dict() for q in quizes])