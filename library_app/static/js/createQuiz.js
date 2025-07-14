const createBtn = document.getElementById('createQuiz');

console.log(document.cookie.split("; ")[1])
createBtn.addEventListener('click', () => {
    const quizCreate = document.getElementById('quizCreate').value
    if (document.cookie.split("; ")[1]){
        
    }
    else {
        document.cookie =  `draft=${quizCreate}; path=/;`;
    }
});


