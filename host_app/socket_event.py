from project import DATABASE as db
from project.settings import DATABASE, socketio
from flask_socketio import join_room, emit
from library_app.models import RedeemCode, Quiz, Room, Question, SessionParticipant, SessionAnswer
import json, flask
from sqlalchemy import func
from flask import request, session

@socketio.on("join_room")
def handle_join(data):
    username = data.get("username")
    code_enter = data.get("code")
    quiz_id = data.get("quizId")

    # Проверяем код
    redeem = RedeemCode.query.filter_by(code_enter=code_enter).first()
    if not redeem:
        emit("join_error", {"message": "Код не найден"})
        return

    # Проверяем викторину
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        emit("join_error", {"message": "Викторина не найдена"})
        return

    # Проверяем комнату
    room = Room.query.get(redeem.room_id)
    if not room:
        emit("join_error", {"message": "Комната не найдена"})
        return

    # Добавляем участника
    participant = SessionParticipant(
        nickname=username,
        room_id=room.id
    )
    try:
        DATABASE.session.add(participant)
        DATABASE.session.commit()
        session['participant_id'] = participant.id
    except Exception as e:
        DATABASE.session.rollback()
        print("Ошибка при добавлении участника:", e)
        emit("join_error", {"message": "Не удалось добавить участника"})
        return

    join_room(str(room.id))

    participants = SessionParticipant.query.filter_by(room_id=room.id).all()
    students = [p.nickname for p in participants]
    room.students = students
    DATABASE.session.commit()


    emit("joined_success", {"quiz_name": redeem.name})
    emit("user_list_update", {"students": students}, room=str(room.id))

    if room.index_question is not None and 0 <= room.index_question < len(quiz.questions):
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

@socketio.on("disconnect")
def handle_disconnect():
    participant_id = session.get("participant_id")
    if not participant_id:
        return  

    participant = SessionParticipant.query.get(participant_id)
    if not participant:
        return

    room_id = participant.room_id

    try:
        DATABASE.session.delete(participant)
        DATABASE.session.commit()
    except Exception as e:
        DATABASE.session.rollback()
        print("Ошибка при удалении участника:", e)
        return

    participants = SessionParticipant.query.filter_by(room_id=room_id).all()
    students = [p.nickname for p in participants]
    room = Room.query.get(room_id)
    if room:
        room.students = students
        DATABASE.session.commit()

    emit("user_list_update", {"students": students}, room=str(room_id))


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

    participant = SessionParticipant.query.get(session['participant_id'])
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
        is_correct = str(answer) == str(question.correct_answer)

    session_answer = SessionAnswer(
        room_id = room.id if room else None,
        question = question.id,
        participant_id = participant.id,
        answer = answer,
        is_correct = is_correct
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
        print(f"{room.students}, {room}")
        print(f"Answered: {room.answered_students}, Total: {total_students}, Question Index: {room.index_question}, Total Questions: {len(quiz.questions)}")
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
    room.answered_students = 0

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

    quiz = Quiz.query.get(redeem.quiz)
    room = Room.query.get(redeem.room_id)

    participant = SessionParticipant.query.get(session['participant_id'])
    participant_answers = SessionAnswer.query.filter_by(
        participant_id=participant.id,
        room_id=room.id
    ).all()

    correct_answers = sum(1 for ans in participant_answers if ans.is_correct)
    notcorrect_answers = len(participant_answers) - correct_answers
    percent_successful = f"{correct_answers * 100 // len(quiz.questions)}" if quiz.questions else "0"

    # сериализуем ответы через to_dict()
    jsonlist = [ans.to_dict() for ans in participant_answers]

    emit(
        "end_quiz",
        {
            "correct_answers": correct_answers,
            "participant_answers": jsonlist,
            "percent": percent_successful,
            "notcorrect_answers": notcorrect_answers
        },
        room=str(room.id)
    )

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
    # participants = SessionParticipant.query.filter_by(room_id=room.id).all()
    # results = []

    # for p in participants:
    #     answers = SessionAnswer.query.filter_by(room_id=room.id, participant_id=p.id).all()
    #     total = len(answers)
    #     correct = sum(1 for a in answers if a.is_correct)
    #     percent = (correct * 100 // total) if total else 0

    #     answers_info = [
    #         {
    #             "question_text": a.question_obj.name if a.question_obj else "",
    #             "is_correct": a.is_correct
    #         } 
    #         for a in answers
    #     ]

    #     results.append({
    #         "nickname": p.nickname,
    #         "percent": percent,
    #         "answers": answers_info
    #     })

    # results.sort(key=lambda x: x["percent"], reverse=True)
    # emit(
    #     "quiz_results",
    #     {"results": results},
    #     room=str(room.id) 
    # )