from project.settings import DATABASE, socketio
from flask_socketio import join_room, emit
from library_app.models import RedeemCode, Result, Quiz, Room, Question
import json

from flask import request, session

@socketio.on("join_room")
def handle_join(data):
    username = data.get("username")
    code_enter = data.get("code")
    quiz_id = data.get("quizId")

    redeem = RedeemCode.query.filter_by(code_enter=code_enter).first()
    if not redeem:
        emit("join_error", {"message": "Код не найден"})
        return

    quiz = Quiz.query.get(quiz_id)

    result = Result(
        name=quiz.name,
        description=quiz.description,
        who_passed=username,
        what_passed=quiz_id,
        by_code=redeem.id,
        correct_answers=0,
        right_answers=0,
        all_answers=len(quiz.questions),
        name_teacher=redeem.hosted.name
    )

    try:
        DATABASE.session.add(result)
        DATABASE.session.commit()
        session['result_id'] = result.id
    except Exception as e:
        print("Error occurred while adding result:", e)

    room_id = str(redeem.room_id)
    join_room(room_id)

    room = Room.query.get(room_id)

    if not isinstance(room.students, list):
        room.students = []

    if username not in room.students:
        room.students.append(username)

    DATABASE.session.commit()

    emit("joined_success", {"quiz_name": redeem.name})
    emit("user_list_update", {"username": username}, room=room_id)

    if room.index_question is not None and room.index_question < len(quiz.questions):
        now_question = quiz.questions[room.index_question]

        emit("quiz_start_student", {
            "quiz_name": quiz.name,
            "name": now_question.name,
            "type": now_question.type,
            "variant_1": now_question.variant_1,
            "variant_2": now_question.variant_2,
            "variant_3": now_question.variant_3,
            "variant_4": now_question.variant_4,
            "correct_answer": now_question.correct_answer,
            "image": now_question.image,
            "id": now_question.id
        })

@socketio.on("host_join")
def handle_host_join(data):
    code_enter = data.get("room")
    print(code_enter)
    redeem = RedeemCode.query.filter_by(code_enter=code_enter).first()
    if not redeem:
        return

    room_id = str(redeem.room_id)
    join_room(room_id)

@socketio.on("quiz_start")
def handle_start(data):
    code_enter = data.get("code")
    redeem = RedeemCode.query.filter_by(code_enter=code_enter).first()
    room_id = str(redeem.room_id)
    room = Room.query.get(room_id)
    quiz = Quiz.query.get(room.quiz)
    room.index_question = 0
    DATABASE.session.commit()
    now_question = quiz.questions[0]
    print(now_question.id)
    emit("quiz_start_student", {
            "quiz_name": data.get("quiz_name"),
            "name": now_question.name,
            "type": now_question.type,
            "variant_1": now_question.variant_1,
            "variant_2": now_question.variant_2,
            "variant_3": now_question.variant_3,
            "variant_4": now_question.variant_4,
            "correct_answer": now_question.correct_answer,
            "image": now_question.image,
            "id": now_question.id
        }, room=room_id
    )
    emit("quiz_start_teacher", {
            "quiz_name": data.get("quiz_name"),
            "id": now_question.id,
            "name": now_question.name,
            "type": now_question.type,
            "variant_1": now_question.variant_1,
            "variant_2": now_question.variant_2,
            "variant_3": now_question.variant_3,
            "variant_4": now_question.variant_4,
            "correct_answer": now_question.correct_answer,
            "image": now_question.image
        }, room=room_id)


@socketio.on("answer")
def handle_answer(data):
    question_id = data.get("question_id")
    answer = data.get("answer")
    username = data.get("username")
    code_enter = data.get("code")

    if not question_id:
        print("question_id is None or missing in data")
        return

    question = Question.query.get(question_id)
    if not question:
        print(f"No question found with id: {question_id}")
        return

    if answer == question.correct_answer:
        result = Result.query.get(session['result_id'])
        result.correct_answers += 1
        result.right_answers += 1
        try:
            DATABASE.session.commit()
        except Exception as e:
            print("Error occurred while updating result:", e)

    redeem = RedeemCode.query.filter_by(code_enter=code_enter).first()
    if not redeem:
        return

    room = Room.query.get(redeem.room_id)
    room.answered_students = (room.answered_students or 0) + 1
    DATABASE.session.commit()

    quiz = Quiz.query.get(room.quiz)
    total_students = len(room.students or [])
    print(f"room.answered_students = {room.answered_students}")
    print(f"total_students = {total_students}")
    print(f"room.index_question = {room.index_question}")
    print(f"total_questions = {len(quiz.questions)}")

    if room.answered_students == total_students and room.index_question == len(quiz.questions) - 1:
        emit('show_finish_button', {}, room=str(room.id))

    emit('student_answer', {
        'username': username,
        'answer': answer,
        'question_id': question_id
    }, room=str(room.id), include_self=False)

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

    DATABASE.session.commit()

    if room.index_question < len(quiz.questions):
        now_question = quiz.questions[room.index_question]
        print(now_question.id)
        emit("quiz_start_student", {
                "quiz_name": quiz.name,
                "name": now_question.name,
                "type": now_question.type,
                "variant_1": now_question.variant_1,
                "variant_2": now_question.variant_2,
                "variant_3": now_question.variant_3,
                "variant_4": now_question.variant_4,
                "correct_answer": now_question.correct_answer,
                "image": now_question.image,
                "id": now_question.id
            }, room=room_id
        )
        emit("quiz_start_teacher", {
                "quiz_name": quiz.name,
                "id": now_question.id,
                "name": now_question.name,
                "type": now_question.type,
                "variant_1": now_question.variant_1,
                "variant_2": now_question.variant_2,
                "variant_3": now_question.variant_3,
                "variant_4": now_question.variant_4,
                "correct_answer": now_question.correct_answer,
                "image": now_question.image
            }, room=room_id)
    else:
        room.index_question = None
        room.answered_students = 0
        DATABASE.session.commit()

@socketio.on("quiz_end")
def handle_quiz_end(data):
    code_enter = data.get("code")
    redeem = RedeemCode.query.filter_by(code_enter=code_enter).first()
    if not redeem:
        return

    room = Room.query.get(redeem.room_id)

    
    emit("end_msg", {"msg": "Вікторину завершено."}, room=str(room.id))