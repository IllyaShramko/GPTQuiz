const btns = document.getElementsByClassName("get-data-login")
const form = document.getElementById("form")
const blurr = document.getElementById("blur")
const closebtn = document.getElementById("close")
const modalInfo = document.getElementById("modalInfo")
btn.addEventListener("click", () => {
    form.classList.remove("hideform")
    blurr.classList.remove("hideform")
})

closebtn.addEventListener("click", () => {
    form.classList.add("hideform")
    blurr.classList.add("hideform")
})

blurr.addEventListener("click", () => {
    form.classList.add("hideform")
    blurr.classList.add("hideform")
})
