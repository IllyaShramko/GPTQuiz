const quizesContainer = document.querySelector('.quizes > div')
const leftBtn = document.querySelector('.scroll-left-btn')
const rightBtn = document.querySelector('.scroll-right-btn')

leftBtn.onclick = () => {
    quizesContainer.scrollBy({ left: -238, behavior: 'smooth' })
}
rightBtn.onclick = () => {
    quizesContainer.scrollBy({ left: 238, behavior: 'smooth' })
}

let scrollAmount = 0
let isScrolling = false

quizesContainer.addEventListener('wheel', e => {
    e.preventDefault()
    scrollAmount += e.deltaY
    if (!isScrolling) smoothScroll()
})

function smoothScroll() {
    isScrolling = true
    const step = scrollAmount * 0.1
    quizesContainer.scrollLeft += step
    scrollAmount -= step
    if (Math.abs(scrollAmount) > 0.5) {
        requestAnimationFrame(smoothScroll)
    } else {
        isScrolling = false
        scrollAmount = 0
    }
}