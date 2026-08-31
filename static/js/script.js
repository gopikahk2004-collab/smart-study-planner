let timerInterval = null;
let seconds = 25 * 60;

function updateTimer() {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    const el = document.getElementById("timer");
    if (el) el.textContent = `${String(mins).padStart(2,"0")}:${String(secs).padStart(2,"0")}`;
}

function startTimer() {
    if (timerInterval) return;
    timerInterval = setInterval(() => {
        if (seconds <= 0) {
            clearInterval(timerInterval);
            timerInterval = null;
            alert("🎉 Pomodoro complete! Take a 5-minute break.");
            return;
        }
        seconds--;
        updateTimer();
    }, 1000);
}

function resetTimer() {
    clearInterval(timerInterval);
    timerInterval = null;
    seconds = 25 * 60;
    updateTimer();
}

document.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("themeBtn");
    const saved = localStorage.getItem("theme");
    if (saved === "dark") document.body.classList.add("dark");
    if (btn) {
        btn.textContent = document.body.classList.contains("dark") ? "☀️" : "🌙";
        btn.addEventListener("click", () => {
            document.body.classList.toggle("dark");
            const dark = document.body.classList.contains("dark");
            localStorage.setItem("theme", dark ? "dark" : "light");
            btn.textContent = dark ? "☀️" : "🌙";
        });
    }
    updateTimer();
});
