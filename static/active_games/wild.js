(function() {
    const spinBtn = document.getElementById('spin-btn');
    const switchBtn = document.getElementById('switch-btn');
    const reactions = document.getElementById('reactions');
    const resultContainer = document.getElementById('result-container');
    const timerContainer = document.getElementById('timer-container');
    const timerText = document.getElementById('wild-timer-text');
    const timerRing = document.getElementById('wild-timer-ring');
    const spinUrl = window.location.pathname.replace(/\/+$/, '') + '/spin/';
    const basePath = window.location.pathname.replace(/\/+$/, '');
    const CIRCUMFERENCE = 263.89;

    let timerInterval = null;
    let timeLeft = 0;
    let promptCount = 0;

    function startTimer(seconds) {
        if (timerInterval) clearInterval(timerInterval);
        timeLeft = seconds;
        if (timerContainer) timerContainer.classList.remove('hidden');
        updateTimerDisplay();
        timerInterval = setInterval(() => {
            timeLeft--;
            updateTimerDisplay();
            if (timeLeft <= 0) {
                clearInterval(timerInterval);
                timerInterval = null;
                if (timerContainer) timerContainer.classList.add('hidden');
                if (spinBtn && !spinBtn.disabled) spinBtn.click();
            }
        }, 1000);
    }

    function updateTimerDisplay() {
        if (timerText) timerText.textContent = Math.max(0, timeLeft);
        if (timerRing) {
            const offset = CIRCUMFERENCE * (1 - Math.max(0, timeLeft) / 30);
            timerRing.style.strokeDashoffset = offset;
        }
    }

    function fetchPartial(url, targetId) {
        fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
            .then(r => r.text())
            .then(html => {
                const target = document.getElementById(targetId);
                if (target) {
                    const wrapper = document.createElement('div');
                    wrapper.innerHTML = html;
                    const newContent = wrapper.firstElementChild;
                    if (newContent) {
                        target.replaceWith(newContent);
                    } else {
                        target.innerHTML = html;
                    }
                }
                promptCount++;
                checkPlayLimit('wild_roles');
            })
            .catch(() => showError(document.documentElement.lang === 'fr' ? 'Erreur de connexion' : document.documentElement.lang === 'es' ? 'Error de conexión' : 'Connection error'));
    }

    if (spinBtn) {
        spinBtn.addEventListener('click', () => {
            spinBtn.disabled = true;
            spinBtn.textContent = document.documentElement.lang === 'fr' ? 'Rotation...' : document.documentElement.lang === 'es' ? 'Girando...' : 'Spinning...';
            fetch(spinUrl, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
                .then(r => r.text())
                .then(html => {
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(html, 'text/html');
                    const newResults = doc.querySelector('#result-container');
                    if (newResults && resultContainer) {
                        resultContainer.innerHTML = newResults.innerHTML;
                    }
                    spinBtn.disabled = false;
                    spinBtn.textContent = document.documentElement.lang === 'fr' ? 'Tourner!' : document.documentElement.lang === 'es' ? '¡Girar!' : 'Spin!';
                    if (reactions) reactions.classList.remove('hidden');
                    if (switchBtn) switchBtn.classList.remove('hidden');
                    startTimer(30);
                    promptCount++;
                    checkPlayLimit('wild_roles');
                    attachRerollListeners();
                })
                .catch(() => {
                    spinBtn.disabled = false;
                    spinBtn.textContent = document.documentElement.lang === 'fr' ? 'Tourner!' : document.documentElement.lang === 'es' ? '¡Girar!' : 'Spin!';
                    showError(document.documentElement.lang === 'fr' ? 'Erreur de connexion' : document.documentElement.lang === 'es' ? 'Error de conexión' : 'Connection error');
                });
        });
    }

    if (switchBtn) {
        switchBtn.addEventListener('click', () => {
            fetch(spinUrl, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
                .then(r => r.text())
                .then(html => {
                    var parser = new DOMParser();
                    var doc = parser.parseFromString(html, 'text/html');
                    var newResults = doc.querySelector('#result-container');
                    if (newResults && resultContainer) {
                        resultContainer.innerHTML = newResults.innerHTML;
                    }
                    if (timerContainer) timerContainer.classList.remove('hidden');
                    startTimer(30);
                    if (reactions) reactions.classList.remove('hidden');
                    promptCount++;
                    checkPlayLimit('wild_roles');
                    attachRerollListeners();
                })
                .catch(function() { showError(document.documentElement.lang === 'fr' ? 'Erreur de connexion' : document.documentElement.lang === 'es' ? 'Error de conexión' : 'Connection error'); });
        });
    }

    function attachRerollListeners() {
        document.querySelectorAll('.reroll-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const target = btn.dataset.target;
                let url;
                if (target === 'character') url = basePath + '/spin-character/';
                else if (target === 'setting') url = basePath + '/spin-setting/';
                else if (target === 'activity') url = basePath + '/spin-activity/';
                if (url) fetchPartial(url, 'wild-' + target);
            });
        });
    }

    attachRerollListeners();

    document.querySelectorAll('.reaction-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const reaction = btn.dataset.reaction;
            fetch(basePath + '/react/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.value || '' },
                body: JSON.stringify({ reaction })
            }).catch(() => showError(document.documentElement.lang === 'fr' ? 'Erreur de connexion' : document.documentElement.lang === 'es' ? 'Error de conexión' : 'Connection error'));
        });
    });

    function checkPlayLimit(currentModule) {
        if (promptCount >= 7) {
            promptCount = 0;
            showSuggestionOverlay(currentModule);
        }
    }

    window.resetCurrentGameCounter = function() { promptCount = 0; };
})();
