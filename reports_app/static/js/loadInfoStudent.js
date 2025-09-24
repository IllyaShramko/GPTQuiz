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
                        el.innerHTML = `
                            <b>Q${index + 1}:</b> ${ans.question_text}<br>
                            <b>Твоя відповідь:</b> ${ans.answer} ${ans.is_correct ? "✅" : "❌"}<br>
                            <b>Правильна:</b> ${ans.correct_answer}
                        `;
                        modalAnswers.appendChild(el);
                    });

                    openModal();
                });
        });
    });
});
