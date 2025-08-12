const descs = document.querySelectorAll('.quiz-description');

descs.forEach(desc => {
    if (text.length > 110) {
        desc.textContent = text.slice(0, 110) + '...';
    }
});