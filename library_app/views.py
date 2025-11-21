import flask, flask_login, os
from .models import Quiz, Question
from project.settings import DATABASE
from werkzeug.utils import secure_filename
from sqlalchemy import func
def render_library():
    
    return flask.render_template(
        'library.html',
        username = flask_login.current_user.login,
        created_quizes = Quiz.query.filter(Quiz.author_id == flask_login.current_user.id).filter(Quiz.name != "draft").all(),
        )

def get_draft():
    next_id = DATABASE.session.query(func.max(Quiz.id)).scalar()
    next_id = (next_id or 0) + 1
    if flask.session.get('quizId'):
        return flask.redirect("/create-quiz/")
    flask.session['quizId'] = next_id
    print(flask.session.get('quizId'))
    return flask.redirect("/create-quiz/")

def get_redaction_quiz():
    id = flask.request.form["redact"]
    quiz = Quiz.query.get(id)
    if not quiz:
        return flask.redirect("/library/")
    if quiz.author_id != flask_login.current_user.id:
        return flask.redirect("/library/")
    flask.session['quizId'] = id
    return flask.redirect("/create-quiz/")


def render_create_quiz():
    questions = []
    question = None
    create_question = False
    print(flask.session.get('quizId'))
    if flask.request.method == 'POST':
        quiz = Quiz.query.get(flask.session.get('quizId'))
        if flask.request.form['button'] == 'one_answer':
            question = 'One answer'
            create_question = True
        elif flask.request.form['button'] == 'enter_answer':
            question = 'Enter answer'
            create_question = True
        elif flask.request.form['button'] == 'multiple_answers':
            question = 'multiple answers'
            create_question = True
        elif flask.request.form["button"] == 'save_quiz':
            if len(quiz.questions) != 0:
                quiz.name = flask.request.form['Name-Quiz']
                quiz.description = flask.request.form['Description-Quiz']
                quiz_image = flask.request.files['image']
                quiz.is_draft = False
                if quiz_image:
                    filename = secure_filename(quiz_image.filename)
                    name, ext = os.path.splitext(secure_filename(quiz_image.filename))
                    save_path = os.path.join(os.path.abspath(__file__), "..", "static", "images", "quizes", filename)
                    counter = 1
                    
                    while os.path.exists(save_path):
                        new_filename = f"{name}_{counter}{ext}"
                        save_path = os.path.join(os.path.abspath(__file__), "..", "static", "images", "quizes", new_filename)
                        counter += 1
                    
                    final_filename = os.path.basename(save_path)
                    print(os.path.abspath(save_path), final_filename, quiz_image)
                    quiz_image.save(os.path.abspath(save_path))
                    quiz.image = f"/images/quizes/{final_filename}"
                else:
                    quiz.image = f"/images/quizes/default.svg"

                print(flask.request.form['Name-Quiz'])
                DATABASE.session.commit()
                response = flask.make_response(flask.redirect("/library/"))
                flask.session.pop('quizId', None)
                return response

        else:
            type_question = flask.request.form['type_question']
            if type_question == 'one_answer':
                question = Question(
                    name = flask.request.form['question'],
                    type = 'one answer',
                    variant_1 = flask.request.form['answer1'],
                    variant_2 = flask.request.form['answer2'],
                    variant_3 = flask.request.form['answer3'],
                    variant_4 = flask.request.form['answer4'],

                    correct_answer = flask.request.form['correct answer'],

                    quiz_id = flask.session.get('quizId')   
                )
                q_image = flask.request.files['image']
                if q_image:
                    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
                    save_dir = os.path.join(BASE_DIR, "..", "library_app", "static", "images", "questions")
                    os.makedirs(save_dir, exist_ok=True)

                    filename = secure_filename(q_image.filename)
                    name, ext = os.path.splitext(filename)
                    save_path = os.path.join(save_dir, filename)
                    counter = 1

                    while os.path.exists(save_path):
                        new_filename = f"{name}_{counter}{ext}"
                        save_path = os.path.join(save_dir, new_filename)
                        counter += 1
                    final_filename = os.path.basename(save_path)
                    q_image.save(save_path)
                    print("✅ Saved:", save_path)

                    question.image = f"questions/{final_filename}"
                try:
                    DATABASE.session.add(question)
                    quiz.count_questions += 1
                    DATABASE.session.commit()
                    return flask.redirect(flask.url_for('/create-quiz/'))
                except:
                    print(Exception)
            elif type_question == 'enter_answer':
                question = Question(
                    name = flask.request.form['question'],
                    type = 'enter answer',
                    variant_1 = flask.request.form['answer1'],
                    correct_answer = flask.request.form['answer1'],
                    quiz_id = flask.session.get('quizId')
                )
                try:
                    DATABASE.session.add(question)
                    quiz.count_questions += 1
                    DATABASE.session.commit()
                    return flask.redirect(flask.url_for('/create-quiz/'))
                except:
                    print(Exception)
            elif type_question == 'multiple_answers':
                question = Question(
                    name = flask.request.form['question'],
                    type = 'multiple answers',
                    variant_1 = flask.request.form['answer1'],
                    variant_2 = flask.request.form['answer2'],
                    variant_3 = flask.request.form['answer3'],
                    variant_4 = flask.request.form['answer4'],
                    correct_answer = flask.request.form.getlist('correct answer'),
                    quiz_id = flask.session.get('quizId')
                )
                q_image = flask.request.files['image']
                if q_image:
                    filename = secure_filename(q_image.filename)
                    name, ext = os.path.splitext(secure_filename(q_image.filename))
                    save_path = os.path.join(os.path.abspath(__file__), "..", "static", "images", "questions", filename)
                    counter = 1
                    
                    while os.path.exists(save_path):
                        new_filename = f"{name}_{counter}{ext}"
                        save_path = os.path.join(os.path.abspath(__file__), "..", "static", "images", "questions", new_filename)
                        counter += 1
                    
                    final_filename = os.path.basename(save_path)
                    print(os.path.abspath(save_path), final_filename, q_image)
                    q_image.save(os.path.abspath(save_path))
                    question.image = f"questions/{final_filename}"
                try:
                    DATABASE.session.add(question)
                    quiz.count_questions += 1
                    DATABASE.session.commit()
                    return flask.redirect(flask.url_for('/create-quiz/'))
                except:
                    print(Exception)
    if flask.session.get('quizId'):
        quiz_id = flask.session.get('quizId')
        quiz = Quiz.query.get(quiz_id)
        if quiz:
            if quiz.questions != 0:
                print(quiz.questions)
                questions = quiz.questions
            else:
                questions = []
        else:
            quiz = Quiz(
                name = "draft",
                description = 'draft',
                count_questions = 0,
                author_id = flask_login.current_user.id,
                image = "/images/quizes/default.svg"
            )
            try:
                DATABASE.session.add(quiz)
                DATABASE.session.commit()
            except:
                print(Exception)
    

    return flask.render_template(
        'create_quiz.html',
        username = flask_login.current_user.login,
        quiz = Quiz.query.get(ident = 1),
        questions = questions,
        question = question,
        create_question = create_question
    )
            

def render_enter_answer():
    return flask.render_template(template_name_or_list='enter_answer.html')

def search_in_library():
    data = flask.request.get_json()
    search_text = data.get('search', '')

    quizes = Quiz.query

    quizes = quizes.filter(Quiz.author_id == flask_login.current_user.id)

    if search_text:
        quizes = quizes.filter(Quiz.name.ilike(f'%{search_text}%'))

    quizes = quizes.all()
    print(f"Search text: {search_text}, Found quizes: {[q.image for q in quizes]}")
    return flask.jsonify([q.to_dict() for q in quizes])