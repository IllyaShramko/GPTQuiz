const deleteButton = document.getElementById("deleteReport")
const modal = document.getElementById("deleteModal")
const closeModalBtn = document.getElementById("cancel")
const blur = document.getElementById("blur")

deleteButton.addEventListener("click", () => {
    modal.style.display = "flex"
    blur.style.display = "block"
})
closeModalBtn.addEventListener("click", () => {
    modal.style.display = "none"
    blur.style.display = "none"
})
blur.addEventListener("click", () => {
    modal.style.display = "none"
    blur.style.display = "none"
})