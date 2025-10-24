import flask, flask_login, os
from .models import Quiz, Question
from project.settings import DATABASE
from werkzeug.utils import secure_filename

def render_library():
    
    
    print(flask_login.current_user.created_quizes)
    return flask.render_template(
        'library.html',
        username = flask_login.current_user.login,
        create_quiz_id = len(Quiz.query.all()) + 1,
        created_quizes = flask_login.current_user.created_quizes
        )

def get_draft():
    create_quiz_id = len(Quiz.query.all()) + 1
    return {"create_quiz_id": create_quiz_id}

def render_create_quiz():
    questions = []
    question = None
    create_question = False
    if flask.request.method == 'POST':
        quiz = Quiz.query.get(flask.request.cookies.get('draft'))
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
                response.delete_cookie('draft')
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

                    quiz_id = int(flask.request.cookies.get("draft"))
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
                    try:
                        os.makedirs(os.path.dirname(save_path), exist_ok=True)
                    except Exception as e:
                        print(f"92 Directory already exists: {e}")
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
            elif type_question == 'enter_answer':
                question = Question(
                    name = flask.request.form['question'],
                    type = 'enter answer',
                    variant_1 = flask.request.form['answer1'],
                    correct_answer = flask.request.form['answer1'],
                    quiz_id = int(flask.request.cookies.get('draft'))
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
                    quiz_id = int(flask.request.cookies.get('draft'))
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
    if flask.request.cookies.get("draft"):
        cookies = int(flask.request.cookies.get("draft"))
        quiz = Quiz.query.get(cookies)
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