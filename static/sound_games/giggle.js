(function() {
    const triggerBtn = document.getElementById('trigger-btn');
    const skipBtn = document.getElementById('skip-btn');
    const timerText = document.getElementById('timer-text');
    const timerRing = document.getElementById('timer-ring');
    const challengeContainer = document.getElementById('challenge-container');
    const ttsToggle = document.getElementById('tts-toggle');
    const shakeToggle = document.getElementById('shake-toggle');

    const CIRCUMFERENCE = 263.89;
    const DURATION = 10;
    let interval = null;
    let timeLeft = 0;
    let running = false;
    let promptCount = 0;

    function hideSkip() { if (skipBtn) skipBtn.classList.add('hidden'); }
    function showSkip() { if (skipBtn) skipBtn.classList.remove('hidden'); }

    function advancePrompt() {
        hideSkip();
        if (challengeContainer) {
            fetch(challengeContainer.dataset.nextUrl || window.location.pathname.replace(/\/+$/, '') + '/next/')
                .then(r => r.text())
                .then(html => {
                    challengeContainer.innerHTML = html;
                    promptCount++;
                    checkPlayLimit('giggle_generators');
                })
                .catch(() => showError(document.documentElement.lang === 'fr' ? 'Erreur de connexion' : document.documentElement.lang === 'es' ? 'Error de conexión' : 'Connection error'));
        }
    }

    function startCountdown() {
        if (running) return;
        running = true;
        timeLeft = DURATION;
        updateDisplay();
        if (triggerBtn) triggerBtn.disabled = true;
        showSkip();
        if (ttsToggle && ttsToggle.checked) {
            const txt = challengeContainer?.querySelector('#challenge-text')?.textContent;
            if (txt) {
                const utterance = new SpeechSynthesisUtterance(txt);
                utterance.lang = document.documentElement.lang || 'en';
                speechSynthesis.speak(utterance);
            }
        }
        interval = setInterval(() => {
            timeLeft--;
            updateDisplay();
            if (timeLeft <= 0) {
                clearInterval(interval);
                interval = null;
                running = false;
                if (triggerBtn) triggerBtn.disabled = false;
                hideSkip();
                if (timerRing) timerRing.style.strokeDashoffset = '0';
                promptCount++;
                checkPlayLimit('giggle_generators');
            }
        }, 1000);
    }

    function updateDisplay() {
        if (timerText) timerText.textContent = Math.max(0, timeLeft);
        if (timerRing) {
            const offset = CIRCUMFERENCE * (1 - Math.max(0, timeLeft) / DURATION);
            timerRing.style.strokeDashoffset = offset;
        }
    }

    if (triggerBtn) triggerBtn.addEventListener('click', startCountdown);
    if (skipBtn) skipBtn.addEventListener('click', () => {
        if (interval) { clearInterval(interval); interval = null; }
        running = false;
        timeLeft = 0;
        updateDisplay();
        if (triggerBtn) triggerBtn.disabled = false;
        hideSkip();
        advancePrompt();
    });

    if (shakeToggle && window.DeviceMotionEvent) {
        let lastShake = 0;
        window.addEventListener('devicemotion', (e) => {
            if (!shakeToggle.checked) return;
            const acc = e.accelerationIncludingGravity;
            const total = Math.abs(acc.x) + Math.abs(acc.y) + Math.abs(acc.z);
            const now = Date.now();
            if (total > 35 && now - lastShake > 2000) {
                lastShake = now;
                window.location.reload();
            }
        });
    }

    function checkPlayLimit(currentModule) {
        if (promptCount >= 7) {
            promptCount = 0;
            window.showSuggestionOverlay(currentModule);
        }
    }

    window.resetCurrentGameCounter = function() { promptCount = 0; };
})();