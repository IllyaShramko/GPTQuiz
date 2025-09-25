const input = document.getElementById('quizCreate');
fetch(`/get-draft/`)
    .then(res => res.json())
.then(data => {
    console.log(data.create_quiz_id);
    input.value = data.create_quiz_id;
});