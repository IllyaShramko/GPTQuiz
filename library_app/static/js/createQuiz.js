const createBtn = document.getElementById('createQuiz');

function getCookie(name) {
    const cookies = document.cookie.split("; ").map(c => c.split("="));
    for (const [key, value] of cookies) {
        if (key === name) return decodeURIComponent(value);
    }
    return null;
}

createBtn.addEventListener('click', () => {
    const quizCreate = document.getElementById('quizCreate').value;
    const draft = getCookie("draft");

    if (draft) {

    } else {
        document.cookie = `draft=${encodeURIComponent(quizCreate)}; path=/;`;

    }
});
