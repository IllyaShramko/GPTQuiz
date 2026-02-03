import flask_login
from project import DATABASE as db
from project.settings import DATABASE, socketio
from flask_socketio import join_room, emit
from library_app.models import RedeemCode, Quiz, Room, Question, SessionParticipant, SessionAnswer, StudentReport
from classroom_app import Student
import json, flask, time
from flask import request, session

def create_student_report(participant_id, room_id):
    answers = SessionAnswer.query.filter_by(room_id=room_id, participant_id=participant_id).all()

    total = len(answers)
    correct = sum(1 for a in answers if a.is_correct)
    wrong = total - correct

    max_score = total
    score = correct
    percentage = round((correct / total) * 100) if total else 0

    grade = percentage / 100 * 12 // 1

    report = StudentReport(
        participant_id=participant_id,
        room_id=room_id,
        total_questions=total,
        correct_answers=correct,
        wrong_answers=wrong,
        score=score,
        max_score=max_score,
        percentage=percentage,
        grade=grade,
        student_id=flask_login.current_user.id
    )

    DATABASE.session.add(report)
    DATABASE.session.commit()

    return report.hash_code

@socketio.on("join_room")
def handle_join(data):
    code_enter = data.get("code")
    quiz_id = data.get("quizId")
    student_id = data.get("student_id")

    redeem = RedeemCode.query.filter_by(code_enter=code_enter).first()
    if not redeem:
        emit("join_error", {"message": "Код не найден"})
        return

    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        emit("join_error", {"message": "Викторина не найдена"})
        return

    room = Room.query.get(redeem.room_id)
    if not room:
        emit("join_error", {"message": "Комната не найдена"})
        return
    
    participants = SessionParticipant.query.filter_by(room_id=room.id).filter_by(is_connected = True).all()
    username = flask_login.current_user.surname + " " + flask_login.current_user.name
    students = [[f"{p.student_profile.surname} {p.student_profile.name}", p.reconnect_hash] for p in participants]
    existing_participiant = SessionParticipant.query.filter_by(student_id=student_id, room_id=room.id).first()
    if not existing_participiant:
        print("Участника нет в комнате, добавление...")
        existing_participiant = SessionParticipant(
            room_id=room.id, 
            is_connected=True,
            student_id=flask_login.current_user.id
        )
        try:
            DATABASE.session.add(existing_participiant)
            DATABASE.session.commit()
            students.append([username, existing_participiant.reconnect_hash])    
            room.students = students
            DATABASE.session.commit()
            print(f"Участник (id: {existing_participiant.id}, student_id: {student_id}) успешно добавлен")
        except Exception as e:
            DATABASE.session.rollback()
            print("Ошибка при добавлении участника:", e)
            emit("join_error", {"message": "Не удалось добавить участника"})
            return
    elif existing_participiant.is_connected == False:
        existing_participiant.is_connected = True
        
        students.append([username, existing_participiant.reconnect_hash])    
        room.students = students
        DATABASE.session.commit()
    else:
        print("Участник есть в комнате")
    session['participant_id'] = existing_participiant.id
    join_room(str(room.id))
    join_room(f"student_{existing_participiant.id}")


    emit("joined_success", {"quiz_name": redeem.name, "hash": existing_participiant.reconnect_hash})
    print("students:", students)
    emit("user_list_update", {"students": students}, room=str(room.id))

    if room.index_question is not None and 0 <= room.index_question <= len(quiz.questions):
        current_question = quiz.questions[room.index_question]
        emit("quiz_start_student", {
            "quiz_name": quiz.name,
            "name": current_question.name,
            "type": current_question.type,
            "variant_1": current_question.variant_1,
            "variant_2": current_question.variant_2,
            "variant_3": current_question.variant_3,
            "variant_4": current_question.variant_4,
            "correct_answer": current_question.correct_answer,
            "image": current_question.image,
            "id": current_question.id,
            "current_question": room.index_question
        })
        answers = SessionAnswer.query.filter_by(room_id = room.id, question= current_question.id).count()
        answer_status = SessionAnswer.query.filter_by(participant_id=existing_participiant.id, question=current_question.id).first()
        if answers != len(students):
            print("ANSWERSERWRE STATUS:", answer_status)
            if answer_status:
                emit(
                    "current_question_info",
                    {
                        "question": current_question.type,
                        "is_correct": "wait",
                        "answer_id": None,
                    }
                )
            return
        
        if answer_status:
            emit(
                "current_question_info",
                {
                    "question": current_question.type,
                    "is_correct": answer_status.is_correct,
                    "answer_id": answer_status.get_answer(answer_status.answer),
                }
            )
        else:
            emit(
                "current_question_info",
                {
                    "question": current_question.type,
                    "is_correct": "skipped",
                    "answer_id": None,
                }
            )
        return

@socketio.on("remove_student")
def handle_remove_student(data):
    code_enter = data.get("code")
    student = data.get("student")
    print("Видалено:", student)
    redeem = RedeemCode.query.filter_by(code_enter=code_enter).first()
    if not redeem:
        return
    room = Room.query.get(redeem.room_id)
    if not room:
        return
    participant = SessionParticipant.query.filter_by(room_id=room.id, reconnect_hash= student[1]).first()
    if not participant:
        return
    participant.is_connected = False
    DATABASE.session.commit()
    emit("remove_student_client", {"hash": student[1]}, room=str(room.id))

@socketio.on("host_join")
def handle_host_join(data):
    code_enter = data.get("room")
    redeem = RedeemCode.query.filter_by(code_enter=code_enter).first()
    if not redeem:
        return

    room = Room.query.get(redeem.room_id)
    if not room:
        return

    join_room(str(room.id))
    join_room(f"teacher_{room.host}")

    participants = SessionParticipant.query.filter_by(room_id=room.id, is_connected=True).all()
    students = [[f"{p.student_profile.surname} {p.student_profile.name}", p.reconnect_hash] for p in participants]

    emit("user_list_update", {"students": students}, room=str(room.id))

    if not flask_login.current_user.is_authenticated or flask_login.current_user.id != room.host:
        if flask.session.get("user_role") != "teacher":
            return

    quiz = Quiz.query.get(room.quiz) if room and room.quiz else None

    if room.index_question is not None and quiz and 0 <= room.index_question < len(quiz.questions):
        current_question = quiz.questions[room.index_question]

        question_data = {
            "id": current_question.id,
            "name": current_question.name,
            "type": current_question.type,
            "variant_1": current_question.variant_1,
            "variant_2": current_question.variant_2,
            "variant_3": current_question.variant_3,
            "variant_4": current_question.variant_4,
            "correct_answer": current_question.correct_answer,
            "image": current_question.image
        }

        socketio.emit("quiz_start_teacher", question_data, room=f"teacher_{room.host}")

        try:
            duration = 45
            end_time = int(time.time() + duration)
            socketio.emit("question_timer", {"end_time": end_time, "duration": duration}, room=f"teacher_{room.host}")
        except Exception as e:
            print("Error emitting reconnect timer to teacher:", e)

        answers = SessionAnswer.query.filter_by(room_id=room.id, question=current_question.id).all()
        if answers:
            print("AAAAAAAAAAAAAAAAAAA", answers)
            if len(answers) == len(participants):
                results = []
                for ans in answers:
                    participant = SessionParticipant.query.get(ans.participant_id)
                    correct_text = ans.right_answers()
                    if isinstance(correct_text, list):
                        correct_text = correct_text if len(correct_text) > 1 else correct_text[0]

                    user_answer_text = ans.get_answer(ans.answer)
                    user_answer_text = user_answer_text if len(user_answer_text) > 1 else user_answer_text[0]

                    results.append({
                        "student_id": ans.participant_id,
                        "nickname": participant.student_profile.surname + " " + participant.student_profile.name,
                        "answer": user_answer_text,
                        "is_correct": ans.is_correct,
                        "correct_answer": correct_text,
                        "answer_id": ans.answer,
                        "correct_answer_id": current_question.correct_answer,
                        "type": current_question.type
                    })

                socketio.emit(
                    "teacher_results",
                    {
                        "results": results,
                        "index_question": room.index_question,
                        "total_questions": len(quiz.questions)
                    },
                    room=f"teacher_{room.host}"
                )
            else:
                for ans in answers:
                    participant = SessionParticipant.query.get(ans.participant_id)
                    socketio.emit(
                        'student_answer',
                        {
                            'username': participant.nickname,
                            'answer': ans.get_answer(ans.answer) if ans.answer else ans.answer,
                            'question_id': current_question.id
                        },
                        room=f"teacher_{room.host}"
                    )
    return

@socketio.on("quiz_start")
def handle_start(data):
    code_enter = data.get("code")
    redeem = RedeemCode.query.filter_by(code_enter=code_enter).first()
    if not redeem:
        return

    room_id = str(redeem.room_id)
    room = Room.query.get(room_id)
    quiz = Quiz.query.get(room.quiz)

    room.index_question = 0
    DATABASE.session.commit()
    now_question = quiz.questions[0]
    print(now_question.id)

    question_data = {
        "id": now_question.id,
        "name": now_question.name,
        "type": now_question.type,
        "variant_1": now_question.variant_1,
        "variant_2": now_question.variant_2,
        "variant_3": now_question.variant_3,
        "variant_4": now_question.variant_4,
        "correct_answer": now_question.correct_answer,
        "image": now_question.image,
        "current_question": room.index_question
    }

    emit("quiz_start_student", question_data, room=room_id)
    emit("quiz_start_teacher", question_data, room=room_id)

    duration = 45
    end_time = int(time.time() + duration)
    emit("question_timer", {"end_time": end_time, "duration": duration}, room=room_id)

@socketio.on("answer")
def handle_answer(data):
    question_id = data.get("question_id")
    answer = data.get("answer")   
    username = data.get("username")
    code_enter = data.get("code")
    my_hash = data.get("my_hash")   
    print(my_hash)
    if not question_id:
        print("question_id is None or missing in data")
        return

    question = Question.query.get(question_id)
    if not question:
        print(f"No question found with id: {question_id}")
        return
    print(session.get("participant_id"))
    participiant = SessionParticipant.query.get(session.get("participant_id"))
    redeem = RedeemCode.query.filter_by(code_enter=code_enter).first()
    room = Room.query.get(redeem.room_id)

    is_correct = False

    if question.type == "multiple answers":
        if isinstance(answer, str):
            try:
                answer = json.loads(answer)
            except:
                answer = [int(x) for x in answer.split(",")]

        if isinstance(question.correct_answer, str):
            try:
                correct = json.loads(question.correct_answer)
            except:
                correct = [int(x) for x in question.correct_answer.split(",")]
        else:
            correct = question.correct_answer

        is_correct = set(map(int, answer)) == set(map(int, correct))

    else:
        is_correct = str(answer).lower() == str(question.correct_answer).lower()

    session_answer = SessionAnswer(
        room_id = room.id,
        question = question.id,
        participant_id = participiant.id,
        answer = answer,
        is_correct = is_correct,
        question_index = room.index_question + 1
    )

    try:
        db.session.add(session_answer)
        db.session.commit()
        print("Result updated successfully.")
    except Exception as e:
        db.session.rollback()
        print("Error occurred while updating result:", e)

    if redeem and room:
        room.answered_students = (room.answered_students or 0) + 1
        db.session.commit()

        quiz = Quiz.query.get(room.quiz)
        total_students = len(room.students or [])
        print(f"Answered: {room.answered_students}, Total: {total_students}, Question Index: {room.index_question}, Total Questions: {len(quiz.questions)}")

        emit('student_answer', {
            'username': username,
            "hash": my_hash,
            'answer': answer,
            'question_id': question_id
        }, room=str(room.id), include_self=False)

        answers = SessionAnswer.query.filter_by(
            room_id=room.id,
            question=question.id
        ).all()

        if len(answers) == SessionParticipant.query.filter_by(room_id=room.id).filter_by(is_connected = True).count():
            handle_end_question({"code": code_enter})

@socketio.on("next_question")
def handle_next(data):
    code_enter = data.get("code")
    redeem = RedeemCode.query.filter_by(code_enter=code_enter).first()
    if not redeem:
        return

    room_id = str(redeem.room_id)
    room = Room.query.get(room_id)
    quiz = Quiz.query.get(room.quiz)

    if room.index_question is None:
        room.index_question = 0
    else:
        room.index_question += 1
    room.answered_students = 0
    DATABASE.session.commit()

    if room.index_question < len(quiz.questions):
        now_question = quiz.questions[room.index_question]
        print(now_question.id)

        question_data = {
            "id": now_question.id,
            "name": now_question.name,
            "type": now_question.type,
            "variant_1": now_question.variant_1,
            "variant_2": now_question.variant_2,
            "variant_3": now_question.variant_3,
            "variant_4": now_question.variant_4,
            "correct_answer": now_question.correct_answer,
            "image": now_question.image,
            "current_question": room.index_question
        }

        emit("quiz_start_student", question_data, room=room_id)
        emit("quiz_start_teacher", question_data, room=room_id)

        duration = 45
        end_time = int(time.time() + duration)
        emit("question_timer", {"end_time": end_time, "duration": duration}, room=room_id)
    else:
        room.index_question = None
        DATABASE.session.commit()

@socketio.on("quiz_end_msg")
def handle_quiz_end_msg(data):
    code_enter = data.get("code")
    redeem = RedeemCode.query.filter_by(code_enter=code_enter).first()
    if not redeem:
        return
    room = Room.query.get(redeem.room_id)
    emit("end_msg", {}, room=str(room.id))

@socketio.on("end_quiz")
def handle_quiz_end(data):
    code_enter = data.get("code")
    redeem = RedeemCode.query.filter_by(code_enter=code_enter).first()
    if not redeem:
        return

    room = Room.query.get(redeem.room_id)

    report = create_student_report(participant_id= session['participant_id'], room_id=room.id)
    emit("end_quiz", {'hash_code': report}, room= f"student_{session['participant_id']}")

@socketio.on("show_quiz_results")
def handle_show_quiz_results(data):
    code_enter = data.get("code")
    redeem = RedeemCode.query.filter_by(code_enter=code_enter).first()
    if not redeem:
        return

    room = Room.query.get(redeem.room_id)
    if not room:
        return
    emit("quiz_results", {"url": f"/report/{room.id}"})

@socketio.on("end_question")
def handle_end_question(data):
    room = Room.query.get(RedeemCode.query.filter_by(code_enter=data.get("code")).first().room_id)
    if not room:
        return

    quiz = Quiz.query.get(room.quiz)
    current_question = quiz.questions[room.index_question]

    answered_ids = {
        ans.participant_id
        for ans in SessionAnswer.query.filter_by(room_id=room.id, question=current_question.id).all()
    }

    all_participants = SessionParticipant.query.filter_by(room_id=room.id).filter_by(is_connected = True).all()

    for participant in all_participants:
        if participant.id not in answered_ids:
            skip_answer = SessionAnswer(
                room_id=room.id,
                question=current_question.id,
                participant_id=participant.id,
                answer="Пропущений...",  
                is_correct=False,
                question_index = room.index_question
            )
            db.session.add(skip_answer)

    db.session.commit()

    answers = SessionAnswer.query.filter_by(room_id=room.id, question=current_question.id).all()
    results = []
    for ans in answers:
        participant = SessionParticipant.query.get(ans.participant_id)
        correct_text = ans.right_answers() 
        if isinstance(correct_text, list):
            correct_text = correct_text if len(correct_text) > 1 else correct_text[0]

        user_answer_text = ans.get_answer(ans.answer) 
        user_answer_text = user_answer_text if len(user_answer_text) > 1 else user_answer_text[0]

        results.append({
            "student_id": ans.participant_id,
            "nickname": participant.student_profile.surname + " " + participant.student_profile.name,
            "answer": user_answer_text,
            "is_correct": ans.is_correct,
            "correct_answer": correct_text,
            "answer_id": ans.answer,
            "correct_answer_id": current_question.correct_answer,
            "type": current_question.type
        })

    for res in results:
        print(res)
        socketio.emit(
            "student_result",
            {
                "your_answer": res["answer"],
                "is_correct": res["is_correct"],
                "correct_answer": res["correct_answer"],
                "answer_id": res["answer_id"],
                "type": res["type"],
                "correct_answer_id": res["correct_answer_id"]
            },
            room=f"student_{res['student_id']}"
        )

    socketio.emit(
        "teacher_results",
        {
            "results": results,
            "index_question": room.index_question,
            "total_questions": len(quiz.questions)
        },
        room=f"teacher_{room.host}"
    )

@socketio.on("add_15_sec")
def handle_add_time(data):
    code_enter = data.get("code")
    redeem = RedeemCode.query.filter_by(code_enter=code_enter).first()
    if not redeem:
        return

    room = Room.query.get(redeem.room_id)
    if not room:
        return
    socketio.emit("add_time", room=str(room.id))