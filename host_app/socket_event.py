from project import DATABASE as db
from project.settings import DATABASE, socketio
from flask_socketio import join_room, emit
from library_app.models import RedeemCode, Quiz, Room, Question, SessionParticipant, SessionAnswer
import json, flask, time
from sqlalchemy import func
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
    if not quiz:
        emit("join_error", {"message": "Викторина не найдена"})
        return

    room = Room.query.get(redeem.room_id)
    if not room:
        emit("join_error", {"message": "Комната не найдена"})
        return
    
    session_id = session.sid if hasattr(session, 'sid') else request.sid
    participant = SessionParticipant(nickname=username, room_id=room.id, session_id=session_id)

    try:
        DATABASE.session.add(participant)
        DATABASE.session.commit()
        session['participant_id'] = participant.id
    except Exception as e:
        DATABASE.session.rollback()
        print("Ошибка при добавлении участника:", e)
        emit("join_error", {"message": "Не удалось добавить участника"})
        return

    # 👇 студент в 2 комнаты
    join_room(str(room.id))
    join_room(f"student_{participant.id}")

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
    redeem = RedeemCode.query.filter_by(code_enter=code_enter).first()
    if not redeem:
        return

    room = Room.query.get(redeem.room_id)
    if not room:
        return

    join_room(str(room.id))
    join_room(f"teacher_{room.host}")

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
        "image": now_question.image
    }

    emit("quiz_start_student", question_data, room=room_id)
    emit("quiz_start_teacher", question_data, room=room_id)

    duration = 30
    end_time = int(time.time() + duration)
    emit("question_timer", {"end_time": end_time, "duration": duration}, room=room_id)


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
        print(code_enter)
        print(flask.session)
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
        is_correct = str(answer).lower() == str(question.correct_answer).lower()

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

        emit('student_answer', {
            'username': username,
            'answer': answer,
            'question_id': question_id
        }, room=str(room.id), include_self=False)

        answers = SessionAnswer.query.filter_by(
            room_id=room.id,
            question=question.id
        ).all()

        if len(answers) == SessionParticipant.query.filter_by(room_id=room.id).count():
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
            "image": now_question.image
        }

        emit("quiz_start_student", question_data, room=room_id)
        emit("quiz_start_teacher", question_data, room=room_id)

        duration = 30
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

    all_participants = SessionParticipant.query.filter_by(room_id=room.id).all()

    for participant in all_participants:
        if participant.id not in answered_ids:
            skip_answer = SessionAnswer(
                room_id=room.id,
                question=current_question.id,
                participant_id=participant.id,
                answer="Пропущений...",  
                is_correct=False 
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
            "nickname": participant.nickname,
            "answer": user_answer_text,
            "is_correct": ans.is_correct,
            "correct_answer": correct_text
        })

    for res in results:
        socketio.emit(
            "student_result",
            {
                "your_answer": res["answer"],
                "is_correct": res["is_correct"],
                "correct_answer": res["correct_answer"]
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
