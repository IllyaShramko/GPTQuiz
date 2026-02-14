const graphicBtn = document.getElementById("graphic")
const generalBtn = document.getElementById("general")
const studentsInfo = document.querySelector(".judah")
const graphicInfo = document.querySelector(".chart-container")
let current_page = "general"
const roomId = document.getElementById('room_id').value;

graphicBtn.addEventListener("click", ()=>{
    if (current_page == "graphic") {
        return
    }
    graphicBtn.classList.remove("not")
    graphicBtn.classList.add('selected')
    graphicInfo.classList.remove("hide")
    generalBtn.classList.remove("selected")
    generalBtn.classList.add("not")
    studentsInfo.classList.add("hide")
    console.log(roomId)
    loadRoomStats(roomId);
    current_page = "graphic"
})
generalBtn.addEventListener("click", ()=>{
    if (current_page == "general") {
        return
    }
    generalBtn.classList.remove("not")
    generalBtn.classList.add('selected')
    studentsInfo.classList.remove("hide")
    graphicBtn.classList.remove("selected")
    graphicBtn.classList.add("not")
    graphicInfo.classList.add("hide")
    current_page = "general"
})
