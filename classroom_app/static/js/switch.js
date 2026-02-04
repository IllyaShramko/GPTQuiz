const graphicBtn = document.getElementById("graphic")
const graphicInfo = document.querySelector(".chart-container")
const studentsBtn = document.getElementById("students")
const studentsInfo = document.querySelector(".students")
let current_page = "students"
const classroomId = document.getElementById('classroom_id').value;

graphicBtn.addEventListener("click", ()=>{
    if (current_page == "graphic") {
        return
    }
    graphicBtn.classList.remove("not")
    graphicBtn.classList.add('selected')
    graphicInfo.classList.remove("hide")
    studentsBtn.classList.remove("selected")
    studentsBtn.classList.add("not")
    studentsInfo.classList.add("hide")
    console.log(classroomId)
    updateCharts(classroomId);
    current_page = "graphic"
})
studentsBtn.addEventListener("click", ()=>{
    if (current_page == "students") {
        return
    }
    studentsBtn.classList.remove("not")
    studentsBtn.classList.add('selected')
    studentsInfo.classList.remove("hide")
    graphicBtn.classList.remove("selected")
    graphicBtn.classList.add("not")
    graphicInfo.classList.add("hide")
    current_page = "general"
})
