# GPTQuiz

**GPTQuiz** — це вебсайт, створений на основі фреймворку **Flask**, призначений для розвитку освітнього процесу в середніх і вищих навчальних закладах.  
Його головна мета — **перевірка засвоєння знань протягом навчального року** з використанням можливостей **штучного інтелекту**.

![alt text](/library_app/static/images/quizes/default.svg)
---


## Навігація

- [Як користуватися](#як-користуватися)

- [Мета створення](#мета-створення)

- [Додатки](#додатки)

- [Склад команди](#склад-команди)

- [Висновок](#висновок)

---

### Додатки

- [USER APP](#1-user-app)

- [CLASSROOM APP](#2-classroom-app)

- [STUDENT APP](#3-student-app)

- [REPORTS APP](#4-reports-app)

- [HOST APP](#5-host-app)

- [EXECUTION APP](#6-execution-app)

- [LIBRARY APP](#7-library-app)
---

## Як користуватися

1. Перейдіть на сайт GPTQUIZ.com;
2. Якщо ви новий користувач та вперше на сайті - зареєструйтесь, а потім увійдіть в акаунт;
3. Натисніть зелену кнопку "Створити" та почніть робити квіз. У ньому можна: добавити картинки, зробити різні за типами питання(одні відповідь, декілька відповідей, ввести відповідь...), робити стільки питань, скільки забажається;
4. Після того, як ви зробили всі питання, опублікуйте цей квіз. Після публікації ви зможете отримати посилання на тест, кьюаркод або код;
5. Учні у свою чергу повинні зайти на платформу та ввести код, або перейти за посиланням.

6. _Якщо ви хочете створити клас та додати туди учнів, перейдіть на головну сторінку та створіть потрібний вам клас, наприклад: 2-А;  Щоб додати туди учнів вам потрібно зробити їм логін та пароль, за яким вони у майбутньому доєднаються до класу. Тоді ви зможете запускати квізи без ніяких проблем!_
---
## Мета створення

_Метою проекта було створити зручну онлайн-платформу для проведення квізів, перевірки знань у навчальному процесі, збереження історії результатів разом з графіками, використання штучного інтелекту для генерації тестів. На цьому сайті можна швидко зробити тест та провести його на уроці в школі, перевіривши знання ваших учнів._

## Склад команди

#### Шрамко Ілля (`TEAMLEAD`)
- **Роль:** Головний програміст, дизайнер
- **GitHub:** [Перейти](https://github.com/IllyaShramko)

#### Свистун Артем 
- **Роль:** Програміст, дизайнер, верстка  
- **GitHub:** [Перейти](https://github.com/asvistun5)

<!-- 
#### Гомельська Вікторія 
- **Роль:** Програміст, дизайнер, верстка  
- **GitHub:** [Перейти](https://github.com/Viktoria0228) -->

#### Потапенко Арина 
- **Роль:** Програміст, дизайнер, верстка  
- **GitHub:** [Перейти](https://github.com/PotapenkoArina)

#### Говоруха Поліна 
- **Роль:** Програміст, дизайнер, верстка  
- **GitHub:** [Перейти](https://github.com/HoworukhaPolina)

<!-- #### Михайло Міщенко  
- **Роль:** Програміст, дизайнер, верстка  
- **GitHub:** [Перейти](https://github.com/DeKlain4ik) -->



---

# Додатки

# 1. USER APP


Реєстрація, авторизація та профилі користувачів.

**Функціонал:** створення акаунтів, логін користувачів, підтвердження email, профіль користувача

**Структура:** models — моделі користувачів, views — логіка авторизації, templates — сторінки signup/login/profile

<details>
<summary><strong>VIEWS.PY</strong></summary>

```python
import flask
import flask_login

from classroom_app import Student
from .models import User, VerificationCode
from project.flask_config import api_instance
from project.settings import DATABASE
from brevo_python.models import SendSmtpEmail, SendSmtpEmailTo, SendSmtpEmailSender
import random, re, os, dotenv

dotenv.load_dotenv()

def validate_data():
    data = flask.request.get_json()

    login = data.get("login", "").strip()
    first_name = data.get("first_name", "").strip()
    surname = data.get("surname", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "")

    errors = {
        "success": True,
        "errors": []
    }

    if not all([login, first_name, surname, email, password]):
        errors["errors"].append({"success": False, "message": "Заповніть усі поля!", "type": "general"})
        errors["success"] = False

    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        errors["errors"].append({"success": False, "message": "Некоректна адреса електронної пошти.", "type": "email"})
        errors["success"] = False

    if len(password) < 6:
        errors["errors"].append({"success": False, "message": "Пароль має містити щонайменше 6 символів.", "type": "password"})
        errors["success"] = False

    existing_user_email = User.query.filter_by(email=email).first()
    if existing_user_email:
        errors["errors"].append({"success": False, "message": "Ця поштова скринька вже використовується", "type": "email"})
        errors["success"] = False
        
    existing_user_username = User.query.filter_by(login=login).first()
    if existing_user_username:
        errors["errors"].append({"success": False, "message": "Цей логін вже використовується", "type": "login"})
        errors["success"] = False
    print(errors)
    

    if not errors["success"]:
        return flask.jsonify(errors), 400
    
    return flask.jsonify({"success": True, "message": "Реєстрація успішна!"}), 200

def send_code():
    data = flask.request.get_json()
    email = data.get('email')
    if not email:
        return flask.jsonify({'error': 'Email required'}), 400

    code = str(random.randint(100000, 999999))
    codeDB = VerificationCode(
        email = email,
        code = code
    )
    try: 
        DATABASE.session.add(codeDB)
        DATABASE.session.commit()
    except Exception as e:
        print(e)
    flask.session['email_code'] = codeDB.id
    print(email)
    send_smtp_email = SendSmtpEmail(
        sender=SendSmtpEmailSender(email= os.getenv("MAIL_USERNAME"), name="GPTQuiz"),
        to=[SendSmtpEmailTo(email=email, name="Шановний Користувач")],
        subject="Ваш код підтвердження",
        html_content=f"<strong>Ваш код підтвердження: {code}</strong>"
    )
    try:
        response = api_instance.send_transac_email(send_smtp_email)
        print("ОК:", response)
    except Exception as e:
        print("Error sending email", e)
    return flask.jsonify({'message': f'Код відправленно на {email}'})

def validate_code():
    data = flask.request.get_json()

    login = data.get("login", "").strip()
    first_name = data.get("first_name", "").strip()
    surname = data.get("surname", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "")
    code = data.get("code", "").strip()
    
    if "email_code" not in flask.session:
        return flask.jsonify(success=False, message="Код підтвердження не знайдено у сессіі"), 400
    
    verify_code = VerificationCode.query.get(flask.session["email_code"])
    if not verify_code:
        return flask.jsonify(success = False, message = "Код не знайдено"), 500

    if code != verify_code.code:
        print(code, flask.session["email_code"])
        return flask.jsonify(success=False, message="Код підтвердження невірний."), 400
    user = User(
        login=login,
        name=first_name,
        surname=surname,
        email=email,
        password=password  
    )
    DATABASE.session.add(user)
    DATABASE.session.commit()
    flask.session.pop("email_code", None)
    return flask.jsonify(success=True, url="/login/"), 200

def render_signup():
    if flask.request.method == 'POST':
        user= User(
            login = flask.request.form['login'],
            name = flask.request.form['name'],
            surname = flask.request.form['surname'],
            email = flask.request.form['email'],
            password = flask.request.form['password']
        )
        try:
            DATABASE.session.add(user)
            DATABASE.session.commit()
            return flask.redirect('/login/')
        except:
            return "Не вдалося створити користувача"
    return flask.render_template(template_name_or_list='signup.html')


def render_login():
    error_msg = None
    selected = True
    if flask.request.method == "POST":
        if flask.request.form["button"] == "teacher":
            for user in User.query.filter_by(login = flask.request.form['login']):
                if user.password == flask.request.form['password']:
                    flask_login.login_user(user)
                    flask.session['user_role'] = 'teacher'
                    return flask.redirect('/admin/')
            error_msg = "Неправильний логін або пароль"
        elif flask.request.form["button"] == "student":
            for student in Student.query.filter_by(login = flask.request.form['login']):
                if student.password == flask.request.form['password']:
                    flask_login.login_user(student)
                    flask.session['user_role'] = 'student'
                    return flask.redirect('/student/')
            error_msg = "Неправильний логін або пароль"
            selected = False
    return flask.render_template(
        template_name_or_list= 'login.html',
        error_msg= error_msg,
        selected= selected
    )

def render_profile():
    user = flask_login.current_user
    return flask.render_template(
        template_name_or_list="profile.html",
        user = user,
        username = flask_login.current_user.login
    )

def create_admin():
    if flask.request.method == "POST":
        user= User(
            login = "admin",
            name = "name",
            surname = "surname",
            email = "",
            password = "admin"
        )
        try:
            DATABASE.session.add(user)
            DATABASE.session.commit()
            return flask.redirect('/login/')
        except:
            return "Не вдалося створити користувача"

def logout():
    flask_login.logout_user()
    return flask.redirect("/")
```

* >Цей код відповідає за реєстрацію та авторизацію. Перевіряє дані які користувач вводить при реєстрації(login, email, password), підтвердження email під час реєстрації; показує профіль користувача, вихід з акаунта. 

</details>


---



# 2. CLASSROOM APP

Створення класів учнів.

<details>
<summary><strong>VIEWS.PY</strong></summary>


```python
from datetime import datetime
import flask, flask_login
from library_app.models import Room, StudentReport
from project.settings import DATABASE
from .models import GroupClass, Student

def render_classrooms():
    errors = ""
    if flask.request.method == "POST":
        number = flask.request.form["number"]
        char   = flask.request.form["char"].upper()
        if GroupClass.query.filter_by(number=number, char=char, teacher_id = flask_login.current_user.id).first():
            errors = "У вас уже є такий клас"
        else:
            new_class = GroupClass(
                number= number,
                char= char,
                teacher_id = flask_login.current_user.id
            )
            try:
                DATABASE.session.add(new_class)
                DATABASE.session.commit()
            except:
                print("Error while creating new class", number, char)
    class_groups = GroupClass.query.filter_by(teacher_id = flask_login.current_user.id).all()
    return flask.render_template(
        "classrooms.html",
        username = flask_login.current_user.login,
        class_groups = class_groups,
        errors=errors
    )

def render_classroom(id):
    errors = ""
    classroom = GroupClass.query.get(id)
    if not classroom:
        return flask.redirect("/classrooms/")
    new_student = None
    if flask.request.method == "POST":
        student_login = flask.request.form["student_login"]
        student_name = flask.request.form["student_name"]
        student_surname = flask.request.form["student_surname"]
        if Student.query.filter_by(login=student_login).first():
            errors = "Учень з такім логіном вже існує"
        elif Student.query.filter_by(name=student_name, surname=student_surname,  my_class_id = id).first():
            errors = "У цьому класі вже є такий учень"
        else:
            new_student = Student(
                login= student_login,
                name= student_name,
                surname= student_surname,
                my_class_id = id
            )
            try:
                DATABASE.session.add(new_student)
                DATABASE.session.commit()
            except:
                print("Error while creating new student", student_login, student_name, student_surname)

    return flask.render_template(
        "class.html",
        username = flask_login.current_user.login,
        classroom= classroom,
        new_student= new_student,
        errors=errors
    )

def render_student_information(id):
    student = Student.query.get(id)
    if not student:
        return flask.redirect("/admin/", 404)
    if student.classroom.teacher_id != flask_login.current_user.id:
        return flask.redirect("/admin/", 403)
    
    return flask.render_template(
        "student.html",
        username = flask_login.current_user.login,
        student=student
    )

def get_data_login_student(id_student, id_classroom):
    response = {
        "status": 200,
        "login": "",
        "password": ""
    }
    student = Student.query.get(id_student)
    if flask.session.get("user_role") != "teacher":
        response["status"] = 403
        return response
    if not student:
        response["status"] = 404
        return response
    if student.classroom.id != id_classroom:
        response["status"] = 403
        return response
    classroom = GroupClass.query.get(id_classroom)
    if not classroom:
        response["status"] = 404
        return response
    if classroom.teacher_id != flask_login.current_user.id:
        response["status"] = 403
        return response
    response["login"] = student.login
    response["password"] = student.password
    return response

def get_class_stats(id):
    start_date_str = flask.request.args.get('start_date')
    end_date_str = flask.request.args.get('end_date')

    start_dt = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
    end_dt = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None

    classroom = GroupClass.query.get(id)
    if not classroom:
        return flask.jsonify({"labels": [], "success_rates": []})

    all_stats = []
    
    for room in classroom.rooms:
        room_date = room.date.date()

        if start_dt and room_date < start_dt: continue
        if end_dt and room_date > end_dt: continue

        percentages = [report.percentage for report in room.student_reports]
        
        if percentages:
            avg_room_success = round(sum(percentages) / len(percentages), 1)
            all_stats.append({
                "date": room_date.strftime('%Y-%m-%d'),
                "code": f"({room.redeem_codes[0].code_enter})", 
                "rate": avg_room_success 
            })

    all_stats.sort(key=lambda x: x['date'])

    labels = [[item['date'], f"{item['code']}"] for item in all_stats]
    rates = [item['rate'] for item in all_stats]

    return flask.jsonify({
        "labels": labels,
        "success_rates": rates
    })
```

* >Цей код відповідає за роботу вчителя з класами та студентами: керує класами, подає статистику успішності, рахує середній відсоток правильних відповідей для кожної кімнати, показує інформацію про конкретного студента.

</details>


---



# 3. STUDENT APP

---

Можливість студенту переглядати свої квізи, результати та статистику.

<details>
<summary><strong>VIEWS.PY</strong></summary>


```python
import flask, flask_login, datetime
from classroom_app import Student
from library_app.models import Question, SessionAnswer, SessionParticipant, StudentReport
from user_app.models import User

def render_student_page():

    return flask.render_template(
        template_name_or_list= 'student_home.html',
        current_user = flask_login.current_user,
        results = flask_login.current_user.my_reports
    )

def get_student_stats(student_id):
    start_date_str = flask.request.args.get('start_date')
    end_date_str = flask.request.args.get('end_date')

    query = StudentReport.query.filter_by(student_id=student_id)

    if start_date_str:
        start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
        query = query.filter(StudentReport.created_at >= start_date)

    if end_date_str:
        end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').replace(hour=23, minute=59, second=59)
        query = query.filter(StudentReport.created_at <= end_date)

    reports = query.order_by(StudentReport.created_at.asc()).all()

    data = {
        "dates": [r.created_at.strftime('%Y-%m-%d') for r in reports],
        "grades": [r.grade for r in reports],
        "hashes": [r.hash_code for r in reports],
        "pie_data": {}
    }

    for r in reports:
        g_label = f"Оцінка {r.grade}" if r.grade is not None else "Без оценки"
        data["pie_data"][g_label] = data["pie_data"].get(g_label, 0) + 1

    return flask.jsonify(data)

def report_view(hash_code):
    report = StudentReport.query.filter_by(hash_code=hash_code).first_or_404()
    participant = SessionParticipant.query.get(report.participant_id)
    room = report.room
    answers = SessionAnswer.query.filter_by(room_id=room.id, participant_id=participant.id).all()
    questions = []
    host = User.query.get(room.host)
    name_teacher = f'{host.surname} {host.name}'
    skipped = 0
    for a in answers:
        if a.answer == "Пропущений..." or a.answer == "Пропущений":
            skipped += 1
        q = Question.query.get(a.question)
        questions.append({
            "id": q.id,
            "text": q.name,
            "type": q.type,
            "your_answer": a.get_answer(a.answer),
            "correct_answer": a.right_answers(),
            "is_correct": a.is_correct,
        })
    roomsquiz = room.roomsQuiz
    
    print(name_teacher)

    

    return flask.render_template(
        "student_report.html",
        name_teacher=name_teacher,
        report=report,
        participant=participant,
        quiz=roomsquiz,
        questions=questions,
        ignore_links=True,
        answers=answers,
        skipped_answers= skipped
    )
```

* >Цей код відповідає за функціонал для студентів на сайті: формує дані для графіків і статистики; дати проходження квізів; показує детальний звіт по квізу: запитання та відповіді студента, кількість пропущених завдань...

</details>


---



# 4. REPORTS APP

---



Показ звітів та статистику квізів для вчителя.

<details>
<summary><strong>VIEWS.PY</strong></summary>


```python
import flask, flask_login
from library_app.models import Quiz, RedeemCode, StudentReport, Room, SessionParticipant, SessionAnswer
from project.settings import DATABASE

def render_reports_page():
    rooms = Room.query.filter_by(host=flask_login.current_user.id, archived = False).all()
    rooms.reverse()
    for room in rooms:
        reports = room.student_reports
        if reports and len(reports) > 0:
            
            room.success_rate = int(sum(r.percentage for r in reports) / len(reports))
        else:
            room.success_rate = 0
    return flask.render_template(
        template_name_or_list='reports.html',
        rooms=rooms,
        username = flask_login.current_user.login,
        archive = False
    )

def render_archived_reports():
    rooms = Room.query.filter_by(host=flask_login.current_user.id, archived = True).all()
    rooms.reverse()
    for room in rooms:
        reports = room.student_reports
        if reports and len(reports) > 0:
            
            room.success_rate = int(sum(r.percentage for r in reports) / len(reports))
        else:
            room.success_rate = 0
    return flask.render_template(
        template_name_or_list='reports.html',
        rooms=rooms,
        username = flask_login.current_user.login,
        archive = True
    )

def render_detail_report(room_id):
    room = Room.query.get_or_404(room_id)
    if room.host != flask_login.current_user.id:
        return {"error": "forbidden"}, 403
    report_data = room.get_report()
    return flask.render_template("detail_report.html", report=report_data, room=room, username = flask_login.current_user.login)

def get_student_report(student_id):
    student = SessionParticipant.query.get(student_id)
    if not student:
        return {"error": "not found"}, 404

    answers = SessionAnswer.query.filter_by(participant_id=student.id).all()

    return {
        "id": student.id,
        "nickname": f"{student.student_profile.surname} {student.student_profile.name}",
        "answers": [
            {
                "question_text": ans.question_obj.name if ans.question_obj else "",
                "type": ans.question_obj.type,
                "answer": ans.get_answer(ans.answer) if ans.question_obj else ans.answer,
                "is_correct": ans.is_correct,
                "correct_answer": ans.right_answers() if ans.question_obj else None
            }
            for ans in answers
        ]
    }

def get_report_answers(room_id):
    answers = SessionAnswer.query.filter_by(room_id=room_id).all()

    stats_map = {}

    for ans in answers:
        idx = ans.question_index
        if idx is None:
            continue
            
        if idx not in stats_map:
            stats_map[idx] = {'total': 0, 'correct': 0}
        
        stats_map[idx]['total'] += 1
        if ans.is_correct:
            stats_map[idx]['correct'] += 1

    result = []
    
    for idx in sorted(stats_map.keys()):
        total = stats_map[idx]['total']
        correct = stats_map[idx]['correct']
        
        percent = int((correct / total) * 100) if total > 0 else 0
        
        result.append({
            "question": f"Q{idx}",
            "succesfull": percent 
        })

    return flask.jsonify(result)
```

* >Цей код відповідає за звіти та статистику квізів для вчителя: показує детальний звіт по конкретній кімнаті квізу; повертає статистику відовідей по всіх студентах в кімнаті; обчислює середній відсоток успішності для кожної кімнати.

</details>

---

# 5. HOST APP

Відповідає за запуск квізів та управління кімнатами.

<details>
<summary><strong>VIEWS.PY</strong></summary>

```python
from library_app.models import Quiz, RedeemCode, Room, Question
import flask, random, flask_login

from project.settings import DATABASE

def generate_code():
    num1= random.randint(0,9)
    num2= random.randint(0,9)
    num3= random.randint(0,9)
    num4= random.randint(0,9)
    num5= random.randint(0,9)
    num6= random.randint(0,9)
    
    code= f"{num1}{num2}{num3}{num4}{num5}{num6}"
    return int(code)

def render_host_app(quizid):
    if not flask_login.current_user.is_authenticated:
        return flask.redirect(flask.url_for("user_app.render_login"))
    quiz = Quiz.query.get(ident=quizid)
    code = 000000
    if flask.request.method == "POST":
        if flask.request.form["btn"] == "host":
            redeem_code= generate_code()
            group_class = flask.request.form.get('group_class')
            room = Room(quiz = quiz.id, host= flask_login.current_user.id, group_class_id= group_class)
            DATABASE.session.add(room)
            DATABASE.session.flush()
            
            code_db= RedeemCode(
                quiz= quiz,
                name = quiz.name,
                code_enter= redeem_code,
                hosted_by= flask_login.current_user.id,
                room_id= room.id
            )
            try:
                DATABASE.session.add(code_db)
                DATABASE.session.commit()
                code = redeem_code
                return flask.redirect(flask.url_for("host_app.render_hosting_quiz", code=code))
            except Exception as e:
                print(e)
        elif flask.request.form["btn"] == "delete":
            try:
                questions = Question.query.filter_by(quiz_id=quiz.id).all()
                for q in questions:
                    DATABASE.session.delete(q)
                DATABASE.session.delete(quiz)
                DATABASE.session.commit()
            except Exception as e:
                DATABASE.session.rollback()
                print("Error: ", e)
            return flask.redirect("/admin/")
    return flask.render_template(
        "previewQuiz.html", quiz = quiz, code= code,
        username = flask_login.current_user.login,
        user = flask_login.current_user
        )


def render_hosting_quiz(code):
    
    return flask.render_template("hosting.html", code=code)
```
* >

</details>

---

# 6. EXECUTION APP

Логіка проходження квізу учасниками.

<details>
<summary><strong>VIEWS.PY</strong></summary>

```python
import flask, flask_login 
from library_app.models import RedeemCode, Quiz, Question, SessionAnswer, SessionParticipant, StudentReport, Room
from project.settings import DATABASE
from user_app.models import User
from classroom_app.models import Student

def render_login_student():
    if flask.request.method == "POST":
        for student in Student.query.filter_by(login = flask.request.form['login']):
            if student.password == flask.request.form['password']:
                flask_login.login_user(student)
                flask.session['user_role'] = 'student'
                redirect_url = flask.request.args.get("redirect_to")
                return flask.redirect(redirect_url)
    return flask.render_template(template_name_or_list= 'login_student.html')

def render_enter_code():
    code = flask.request.args.get("code")
    if not flask_login.current_user.is_authenticated:
        if not code:
            return flask.redirect("/login_student?redirect_to=/execution/")
        return flask.redirect(f"/login_student?redirect_to=/execution?code={code}")
    if flask.session.get("user_role") != "student":
        return flask.redirect(f"/login_student?redirect_to={code}")
    if code:
        quiz = RedeemCode.query.filter_by(code_enter= code).first_or_404().quiz
        room = RedeemCode.query.filter_by(code_enter=code).first().room
        teacher = User.query.get(room.host)
        username = flask_login.current_user.surname + " " + flask_login.current_user.name
        return flask.render_template(
            template_name_or_list= 'enter_nickname.html',
            quiz=quiz, teacher=teacher, username= username, student= flask_login.current_user
        )
    return flask.render_template(
        template_name_or_list="enter_code.html"
    )


```
</details>

---

# 7. LIBRARY APP

Бібліотека квізів та питань.

<details>
<summary><strong>VIEWS.PY</strong></summary>

```python
import flask, flask_login, os
from .models import Quiz, Question
from project.settings import DATABASE
from werkzeug.utils import secure_filename
from sqlalchemy import func
def render_library():
    
    return flask.render_template(
            'library.html',
            username = flask_login.current_user.login,
            created_quizes = Quiz.query.filter_by(author_id = flask_login.current_user.id, is_draft = False ).all(),
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
```

</details>

---


# Висновок

_Коли ми створювали цей веб-додаток ми здобули багато нового досвіду. Ми постаралися зробити зручний і функціональний сайт. Було реалізовано багато чого у цьому проєкті, наприклад: анімації при проходженні квізу, сторінки для студентів і вчителів, систему квізів, статистику результатів, розробка квізів та питань. Проєкт дав нам цінний досвід у створенні повноційного вебзастосунку. 
Ми прагнемо до того, щоб нашу онлайн-платформу почали використовувати у шкільних закладах тощо, тому будемо дуже раді цьому. Щіро дякуємо всією командою!_