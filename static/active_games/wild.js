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
    let promptCount = parseInt(sessionStorage.getItem('wild-roles-count') || '0');

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
                sessionStorage.setItem('wild-roles-count', String(promptCount));
                checkPlayLimit('wild_roles');
            })
            .catch(() => {});
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
                    sessionStorage.setItem('wild-roles-count', String(promptCount));
                    checkPlayLimit('wild_roles');
                    attachRerollListeners();
                })
                .catch(() => {
                    spinBtn.disabled = false;
                    spinBtn.textContent = document.documentElement.lang === 'fr' ? 'Tourner!' : document.documentElement.lang === 'es' ? '¡Girar!' : 'Spin!';
                });
        });
    }

    if (switchBtn) {
        switchBtn.addEventListener('click', () => {
            if (spinBtn) spinBtn.click();
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
            }).catch(() => {});
        });
    });

    function checkPlayLimit(currentModule) {
        if (promptCount >= 7) {
            sessionStorage.setItem('wild-roles-count', '0');
            showSuggestionOverlay(currentModule);
        }
    }

    function showSuggestionOverlay(currentModule) {
        const allGenres = [
            { name: 'Giggle Generators', module: 'giggle_generators', slug: 'giggle-generators' },
            { name: 'Choice Chaos', module: 'choice_chaos', slug: 'choice-chaos' },
            { name: 'Mimic Mayhem', module: 'mimic_mayhem', slug: 'mimic-mayhem' },
            { name: 'Lip-Sync Legends', module: 'lip_sync_legends', slug: 'lip-sync-legends' },
            { name: 'Tale Twisters', module: 'tale_twisters', slug: 'tale-twisters' },
            { name: 'Funny Face Factory', module: 'funny_face_factory', slug: 'funny-face-factory' },
            { name: 'Doodle Dash', module: 'doodle_dash', slug: 'doodle-dash' },
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
            <button onclick="sessionStorage.removeItem('wild-roles-count');this.closest('#suggestion-overlay').remove()" class="text-gray-400 hover:text-gray-600 text-sm underline">${document.documentElement.lang === 'fr' ? 'Continuer à jouer' : document.documentElement.lang === 'es' ? 'Seguir jugando' : 'Keep playing'}</button>
            <br><br>
            <a href="/${lang}/" class="text-red-400 hover:text-red-600 text-sm underline">${document.documentElement.lang === 'fr' ? 'Arrêter' : document.documentElement.lang === 'es' ? 'Parar' : 'Stop playing'}</a>
        </div>`;
        document.body.appendChild(overlay);
    }
})();