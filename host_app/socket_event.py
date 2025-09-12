from project.settings import DATABASE, socketio
from flask_socketio import join_room, emit
from library_app.models import RedeemCode, Result, Quiz, Room
import json

from flask import request, session

@socketio.on("join_room")
def handle_join(data):
    username = data.get("username")
    code_enter = data.get("code")
    quiz_id = data.get("quizId")

    print(code_enter, quiz_id)
    redeem = RedeemCode.query.filter_by(code_enter=code_enter).first()
    if not redeem:
        emit("join_error", {"message": "Код не найден"})
        return
    quiz = Quiz.query.get(quiz_id)
    result = Result(
        name = quiz.name,
        description = quiz.description,
        who_passed = username,
        what_passed = quiz_id,
        by_code = redeem.id ,
        correct_answers = 0,
        right_answers = 0,
        all_answers = len(quiz.questions),
        name_teacher = redeem.hosted.name
    )
    try:
        DATABASE.session.add(result)
        DATABASE.session.commit()
        session['result_id'] = result.id
        print(session['result_id'])
        
    except Exception as e:
        print("Error occurred while adding result:", e)

    room_id = str(redeem.room_id)
    join_room(room_id)

    emit("joined_success", {"quiz_name": redeem.name})
    emit("user_list_update", {"username": username}, room=room_id)

    room = Room.query.get(room_id)

    if room.index_question != None and room.index_question < len(quiz.questions):
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
            "image": now_question.image
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
    emit("quiz_start_student", {
            "quiz_name": data.get("quiz_name"),
            "name": now_question.name,
            "type": now_question.type,
            "variant_1": now_question.variant_1,
            "variant_2": now_question.variant_2,
            "variant_3": now_question.variant_3,
            "variant_4": now_question.variant_4,
            "correct_answer": now_question.correct_answer,
            "image": now_question.image
        }, room=room_id
    )
    emit("quiz_start_teacher", {
            "quiz_name": data.get("quiz_name"),
            "name": now_question.name,
            "type": now_question.type,
            "variant_1": now_question.variant_1,
            "variant_2": now_question.variant_2,
            "variant_3": now_question.variant_3,
            "variant_4": now_question.variant_4,
            "correct_answer": now_question.correct_answer,
            "image": now_question.image
        }, room=room_id)
