const createBtns = document.getElementsByClassName('createQuiz');

function getCookie(name) {
    const cookies = document.cookie.split("; ").map(c => c.split("="));
    for (const [key, value] of cookies) {
        if (key === name) return decodeURIComponent(value);
    }
    return null;
}
console.log(createBtns);
Array.from(createBtns).forEach(element => {
    element.addEventListener('click', () => {
        const quizCreate = document.getElementById('quizCreate').value;
        const draft = getCookie("draft");
        if (draft) {
            window.location.href = "/create-quiz/";
        } else {
            document.cookie = `draft=${encodeURIComponent(quizCreate)}; path=/;`;
            window.location.href = "/create-quiz/";
        }
    })
});
