const graphicBtn = document.getElementById("graphic");
const generalBtn = document.getElementById("general");
const studentsInfo = document.querySelector(".judah");
const graphicInfo = document.querySelector(".chart-container");
let current_page = "general";
const roomId = document.getElementById('room_id').value;
const questionsBtn = document.getElementById('questions');


function switchTab(tab) {
    if (current_page === tab) return;

    if (tab === "graphic") {
        graphicBtn.classList.remove("not");
        graphicBtn.classList.add('selected');
        graphicInfo.classList.remove("hide");

        generalBtn.classList.remove("selected");
        generalBtn.classList.add("not");
        studentsInfo.classList.add("hide");

        loadRoomStats(roomId);
    } else if (tab === "general") {
        generalBtn.classList.remove("not");
        generalBtn.classList.add('selected');
        studentsInfo.classList.remove("hide");

        graphicBtn.classList.remove("selected");
        graphicBtn.classList.add("not");
        graphicInfo.classList.add("hide");
    } else if (tab === "questions") {
        
    }

    current_page = tab;
}

graphicBtn.addEventListener("click", () => switchTab("graphic"));
generalBtn.addEventListener("click", () => switchTab("general"));
questionsBtn.addEventListener("click", () => switchTab("questions"));