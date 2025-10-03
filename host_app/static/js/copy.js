const copyBtn = document.getElementById('copy-code');
const copyUrlBtn = document.getElementById('copy-url');
const linkTo = document.getElementById('linkToJoin');
const codeDisplay = document.getElementById('codeDisplay');

linkTo.href = `${window.location.origin}/execution?code=${codeDisplay.textContent.trim()}`


copyBtn.addEventListener('click', async () => {
    try {
        const text = codeDisplay.textContent.trim();
        await navigator.clipboard.writeText(text);
    } catch (err) {
        console.error('Помилка:', err);

    }
});

copyUrlBtn.addEventListener('click', async () => {
  try {
    const text = linkTo.href.trim();
    await navigator.clipboard.writeText(text);
  } catch (err) {
    console.error('Помилка:', err);
  }
});