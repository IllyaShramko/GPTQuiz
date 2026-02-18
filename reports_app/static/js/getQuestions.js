function renderQuestions(questions) {
    const container = document.querySelector(".questions-container");
    container.innerHTML = "";

    questions.forEach((q, index) => {
        const block = document.createElement("div");

        let variantsHTML = "";

        q.variants.forEach(variant => {
            variantsHTML += `<div class="question-block">
                <p>${variant}</p>
            </div>`;
        });

        block.innerHTML = `
            <h3>${index + 1}. ${q.question_text}</h3>
            <p>Варіанти відповіді:</p>
            <div class="questions-block">
                ${variantsHTML}
            </div>
        `;

        container.appendChild(block);
    });
}


function loadQuestions() {
    fetch(`/reports/${roomId}/questions`)
        .then(response => {
            if (!response.ok) {
                throw new Error("Ошибка загрузки");
            }
            return response.json();
        })
        .then(data => {
            renderQuestions(data);
        })
        .catch(error => {
            console.error("Fetch error:", error);
        });
}
