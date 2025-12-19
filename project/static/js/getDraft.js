const input = document.getElementsByClassName('quizCreate');
console.log(input);
fetch(`/get-draft/`)
    .then(res => res.json())
.then(data => {
    console.log(data.create_quiz_id);
    Array.from(input).forEach(element => {
        element.value = data.create_quiz_id;
    });
});