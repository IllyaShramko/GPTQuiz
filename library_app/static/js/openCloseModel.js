const exitSaveBtn = document.getElementById('SaveAndExit')
const saveForm = document.getElementById('saveForm')
const blurW = document.getElementById('blur')
const inputImg = document.getElementById('imageQuiz')
const labelImg = document.getElementById('uploadLabel')


exitSaveBtn.addEventListener(
    'click',
    function (){
        saveForm.classList.add('showform')
        blurW.classList.add('showform')
    }
)

blurW.addEventListener('click', () => {
    saveForm.classList.remove('showform')
    blurW.classList.remove('showform')
})


inputImg.addEventListener('change', event => {
    const reader = new FileReader();
    reader.onload = function (event) {
        const imgElement = document.createElement('img');
        imgElement.src = event.target.result;
        labelImg.innerHTML = '';
        labelImg.appendChild(imgElement); 

    };
    reader.readAsDataURL(event.target.files[0]);
})

document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
        saveForm.classList.remove('showform')
        blurW.classList.remove('showform')
    }
});