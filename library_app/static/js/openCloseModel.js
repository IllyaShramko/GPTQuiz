const exitSaveBtn = document.getElementById('SaveAndExit')
const saveForm = document.getElementById('saveForm')


exitSaveBtn.addEventListener(
    'click',
    function (){
        saveForm.classList.add('showform')
    }
)