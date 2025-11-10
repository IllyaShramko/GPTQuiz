const deleteButton = document.getElementById("deleteReport")
const modal = document.getElementById("deleteModal")
const closeModalBtn = document.getElementById("cancel")
const blurrrr = document.getElementById("blurrrr")

deleteButton.addEventListener("click", () => {
    modal.style.display = "flex"
    blurrrr.style.display = "block"
})
closeModalBtn.addEventListener("click", () => {
    modal.style.display = "none"
    blurrrr.style.display = "none"
})
blurrrr.addEventListener("click", () => {
    modal.style.display = "none"
    blurrrr.style.display = "none"
})