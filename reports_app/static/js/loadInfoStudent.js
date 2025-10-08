document.addEventListener("DOMContentLoaded", () => {
    const students = document.querySelectorAll(".student-card");
    const modal = document.getElementById("studentModal");
    const closeModal = document.getElementById("closeModal");
    const modalTitle = document.getElementById("nicknameStudent");
    const modalAnswers = document.getElementById("modalAnswers");
    const modalBlur = document.getElementById("blur")

    function openModal() {
        modal.classList.add("show");
        modalBlur.style.display = "block"
        modal.style.display = "flex";
    }

    function hideModal() {
        modal.classList.remove("show");
        modalBlur.style.display = "none"
        modal.style.display = "none"
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
                        const el = document.createElement("div");
                        el.classList.add("question");
                        if (!ans.is_correct) {
                            el.classList.add('wrongQ')
                        }
                        else{
                            el.classList.add("correctQ")
                        }
                        const userAnswer = Array.isArray(ans.answer) ? ans.answer.join(", ") : ans.answer;
                        const correctAnswer = Array.isArray(ans.correct_answer) ? ans.correct_answer.join(", ") : ans.correct_answer;

                        el.innerHTML = `
                            <h3>Запитання №${index + 1}</h3>
                            <h4>${ans.question_text}</h4>
                            <div class="answers">
                                <p>Твоя відповідь: ${userAnswer}</p>
                                <p>Правильна: ${correctAnswer}</p>
                            </div>
                            <p class="points">${Number(ans.is_correct)}/1</p>
                        `;
                        modalAnswers.appendChild(el);
                    });

                    openModal();
                });
        });
    });
});
