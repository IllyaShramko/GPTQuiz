const btn = document.getElementById("add")
const form = document.getElementById("form")
const blurr = document.getElementById("blur")
const closebtn = document.getElementById("close")
btn.addEventListener("click", () => {
    form.classList.remove("hideform")
    blurr.classList.remove("hideform")
})

closebtn.addEventListener("click", () => {
    form.classList.add("hideform")
    blurr.classList.add("hideform")
})

