document.addEventListener("DOMContentLoaded", () => {
    const students = document.querySelectorAll(".student-card");
    const modal = document.getElementById("studentModal");
    const closeModal = document.getElementById("closeModal");
    const modalTitle = document.getElementById("modalTitle");
    const modalAnswers = document.getElementById("modalAnswers");

    function openModal() {
        modal.classList.add("show");
        modal.style.display = "block";
    }

    function hideModal() {
        modal.classList.remove("show");
        setTimeout(() => modal.style.display = "none", 400);
    }

    closeModal.addEventListener("click", hideModal);

    window.addEventListener("click", e => {
        if (e.target === modal) hideModal();
    });

    students.forEach(student => {
        student.addEventListener("click", () => {
            const studentId = student.dataset.studentId;

            fetch(`/report/student/${studentId}`)
                .then(res => res.json())
                .then(data => {
                    modalTitle.textContent = data.nickname;
                    modalAnswers.innerHTML = "";

                    data.answers.forEach((ans, index) => {
                        const el = document.createElement("p");
                        el.classList.add("modal-answer");

                        const userAnswer = Array.isArray(ans.answer) ? ans.answer.join(", ") : ans.answer;
                        const correctAnswer = Array.isArray(ans.correct_answer) ? ans.correct_answer.join(", ") : ans.correct_answer;

                        el.innerHTML = `
                            <b>Q${index + 1}:</b> ${ans.question_text}<br>
                            <b>Твоя відповідь:</b> ${userAnswer} ${ans.is_correct ? "✅" : "❌"}<br>
                            <b>Правильна:</b> ${correctAnswer}
                        `;
                        modalAnswers.appendChild(el);
                    });

                    openModal();
                });
        });
    });
});
