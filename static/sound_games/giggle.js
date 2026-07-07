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
    let promptCount = parseInt(sessionStorage.getItem('giggle-generators-count') || '0');

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
                    sessionStorage.setItem('giggle-generators-count', String(promptCount));
                    checkPlayLimit();
                })
                .catch(() => {});
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

    function checkPlayLimit() {
        if (promptCount >= 7) {
            sessionStorage.setItem('giggle-generators-count', '0');
            showSuggestionOverlay('giggle_generators');
        }
    }

    function showSuggestionOverlay(currentModule) {
        const allGenres = [
            { name: 'Choice Chaos', module: 'choice_chaos', slug: 'choice-chaos' },
            { name: 'Mimic Mayhem', module: 'mimic_mayhem', slug: 'mimic-mayhem' },
            { name: 'Lip-Sync Legends', module: 'lip_sync_legends', slug: 'lip-sync-legends' },
            { name: 'Tale Twisters', module: 'tale_twisters', slug: 'tale-twisters' },
            { name: 'Funny Face Factory', module: 'funny_face_factory', slug: 'funny-face-factory' },
            { name: 'Doodle Dash', module: 'doodle_dash', slug: 'doodle-dash' },
            { name: 'Wild Roles', module: 'wild_roles', slug: 'wild-roles' },
            { name: 'Highway Hijinks', module: 'highway_hijinks', slug: 'highway-hijinks' },
        ];
        const lang = document.documentElement.lang || 'en';
        const others = allGenres.filter(g => g.module !== currentModule);
        const shuffled = others.sort(() => Math.random() - 0.5).slice(0, 3);
        const overlay = document.createElement('div');
        overlay.id = 'suggestion-overlay';
        overlay.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,0.6);display:flex;align-items:center;justify-content:center;z-index:9999;';
        overlay.innerHTML = `<div class="bg-white rounded-2xl shadow-2xl p-8 max-w-sm mx-4 text-center">
            <h2 class="text-xl font-bold text-gray-800 mb-2">🎉 ${document.documentElement.lang === 'fr' ? 'Bien joué!' : document.documentElement.lang === 'es' ? '¡Bien hecho!' : 'Well played!'}</h2>
            <p class="text-gray-500 mb-6">${document.documentElement.lang === 'fr' ? 'Tu as joué quelques parties! Tu veux essayer autre chose?' : document.documentElement.lang === 'es' ? '¡Has jugado unas cuantas veces! ¿Pruebas algo más?' : 'You have played a few rounds! Try something else?'}</p>
            <div class="space-y-3 mb-6">
                ${shuffled.map(g => `<a href="/${lang}/${g.slug}/" class="block w-full bg-purple-50 hover:bg-purple-100 border-2 border-purple-200 rounded-xl p-3 text-purple-700 font-medium transition-all">${g.name}</a>`).join('')}
            </div>
            <button onclick="sessionStorage.removeItem('giggle-generators-count');this.closest('#suggestion-overlay').remove()" class="text-gray-400 hover:text-gray-600 text-sm underline">${document.documentElement.lang === 'fr' ? 'Continuer à jouer' : document.documentElement.lang === 'es' ? 'Seguir jugando' : 'Keep playing'}</button>
            <br><br>
            <a href="/${lang}/" class="text-red-400 hover:text-red-600 text-sm underline">${document.documentElement.lang === 'fr' ? 'Arrêter' : document.documentElement.lang === 'es' ? 'Parar' : 'Stop playing'}</a>
        </div>`;
        document.body.appendChild(overlay);
    }
})();