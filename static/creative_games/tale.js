(function() {
    const storyPhase = document.getElementById('story-phase');
    const saveBtn = document.getElementById('save-btn');
    const clearBtn = document.getElementById('clear-btn');
    const phaseIndicator = document.getElementById('phase-indicator');

    function showError(msg) {
        var el = document.createElement('div');
        el.className = 'fixed bottom-4 left-1/2 -translate-x-1/2 bg-red-600 text-white px-6 py-3 rounded-xl shadow-lg z-50 text-sm font-medium';
        el.textContent = msg;
        document.body.appendChild(el);
        setTimeout(function() { el.remove(); }, 3000);
    }

    let promptCount = parseInt(sessionStorage.getItem('tale-twisters-count') || '0');

    function countPrompt() {
        promptCount++;
        sessionStorage.setItem('tale-twisters-count', String(promptCount));
        checkPlayLimit('tale_twisters');
    }

    function getCsrf() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
    }

    function baseUrl() {
        return window.location.pathname.replace(/\/+$/, '');
    }

    function updatePhaseIndicator(phase) {
        if (!phaseIndicator) return;
        phaseIndicator.querySelectorAll('[data-phase]').forEach((dot, i) => {
            const num = i + 1;
            dot.className = 'w-3 h-3 rounded-full ' + (num <= phase ? 'bg-purple-600' : 'bg-gray-300');
        });
    }

    function loadStartOptions() {
        fetch(baseUrl() + '/start/', { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
            .then(r => r.text())
            .then(html => {
                if (storyPhase) storyPhase.innerHTML = html;
                updatePhaseIndicator(0);
                attachListeners();
            })
            .catch(() => showError(document.documentElement.lang === 'fr' ? 'Erreur de connexion' : document.documentElement.lang === 'es' ? 'Error de conexión' : 'Connection error'));
    }

    function loadState() {
        fetch(baseUrl() + '/state/', { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
            .then(r => r.text())
            .then(html => {
                if (storyPhase) storyPhase.innerHTML = html;
                const phaseEl = storyPhase?.querySelector('[data-phase]');
                const phase = parseInt(phaseEl?.dataset?.phase || '0');
                updatePhaseIndicator(phase);
                if (saveBtn) saveBtn.disabled = phase < 3;
                if (phase === 0) {
                    loadStartOptions();
                } else {
                    attachListeners();
                }
            })
            .catch(() => showError(document.documentElement.lang === 'fr' ? 'Erreur de connexion' : document.documentElement.lang === 'es' ? 'Error de conexión' : 'Connection error'));
    }

    function attachListeners() {
        document.querySelectorAll('.seed-option').forEach(btn => {
            btn.addEventListener('click', () => {
                const seedId = btn.dataset.seedId;
                fetch(baseUrl() + '/start/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrf() },
                    body: JSON.stringify({ seed_id: seedId })
                })
                .then(r => r.json())
                .then(data => {
                    if (data.status === 'ok') { countPrompt(); loadTwistOptions(); }
                })
                .catch(() => showError(document.documentElement.lang === 'fr' ? 'Erreur de connexion' : document.documentElement.lang === 'es' ? 'Error de conexión' : 'Connection error'));
            });
        });

        document.querySelectorAll('.twist-option').forEach(btn => {
            btn.addEventListener('click', () => {
                const twistId = btn.dataset.twistId;
                fetch(baseUrl() + '/pick-twist/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrf() },
                    body: JSON.stringify({ twist_id: twistId })
                })
                .then(r => r.json())
                .then(data => {
                    if (data.status === 'ok') { countPrompt(); loadEndingOptions(); }
                })
                .catch(() => showError(document.documentElement.lang === 'fr' ? 'Erreur de connexion' : document.documentElement.lang === 'es' ? 'Error de conexión' : 'Connection error'));
            });
        });

        document.querySelectorAll('.ending-option').forEach(btn => {
            btn.addEventListener('click', () => {
                const endingId = btn.dataset.endingId;
                fetch(baseUrl() + '/pick-ending/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrf() },
                    body: JSON.stringify({ ending_id: endingId })
                })
                .then(r => r.json())
                .then(data => {
                    if (data.status === 'ok') { countPrompt(); loadState(); }
                })
                .catch(() => showError(document.documentElement.lang === 'fr' ? 'Erreur de connexion' : document.documentElement.lang === 'es' ? 'Error de conexión' : 'Connection error'));
            });
        });
    }

    function loadTwistOptions() {
        fetch(baseUrl() + '/pick-twist/', { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
            .then(r => r.text())
            .then(html => {
                if (storyPhase) storyPhase.innerHTML = html;
                updatePhaseIndicator(1);
                attachListeners();
            })
            .catch(() => showError(document.documentElement.lang === 'fr' ? 'Erreur de connexion' : document.documentElement.lang === 'es' ? 'Error de conexión' : 'Connection error'));
    }

    function loadEndingOptions() {
        fetch(baseUrl() + '/pick-ending/', { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
            .then(r => r.text())
            .then(html => {
                if (storyPhase) storyPhase.innerHTML = html;
                updatePhaseIndicator(2);
                attachListeners();
            })
            .catch(() => showError(document.documentElement.lang === 'fr' ? 'Erreur de connexion' : document.documentElement.lang === 'es' ? 'Error de conexión' : 'Connection error'));
    }

    function checkPlayLimit(currentModule) {
        if (promptCount >= 7) {
            sessionStorage.setItem('tale-twisters-count', '0');
            showSuggestionOverlay(currentModule);
        }
    }

    function showSuggestionOverlay(currentModule) {
        const allGenres = [
            { name: 'Giggle Generators', module: 'giggle_generators', slug: 'giggle-generators' },
            { name: 'Choice Chaos', module: 'choice_chaos', slug: 'choice-chaos' },
            { name: 'Mimic Mayhem', module: 'mimic_mayhem', slug: 'mimic-mayhem' },
            { name: 'Lip-Sync Legends', module: 'lip_sync_legends', slug: 'lip-sync-legends' },
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
            <button onclick="sessionStorage.removeItem('tale-twisters-count');this.closest('#suggestion-overlay').remove()" class="text-gray-400 hover:text-gray-600 text-sm underline">${document.documentElement.lang === 'fr' ? 'Continuer à jouer' : document.documentElement.lang === 'es' ? 'Seguir jugando' : 'Keep playing'}</button>
            <br><br>
            <a href="/${lang}/" class="text-red-400 hover:text-red-600 text-sm underline">${document.documentElement.lang === 'fr' ? 'Arrêter' : document.documentElement.lang === 'es' ? 'Parar' : 'Stop playing'}</a>
        </div>`;
        document.body.appendChild(overlay);
    }

    if (clearBtn) {
        clearBtn.addEventListener('click', () => {
            const key = 'tale_' + (document.documentElement.lang || 'en');
            sessionStorage.removeItem(key);
            loadState();
        });
    }

    if (saveBtn) {
        saveBtn.addEventListener('click', () => {
            var title = window.prompt(document.documentElement.lang === 'fr' ? 'Titre de ton histoire:' : document.documentElement.lang === 'es' ? 'Título de tu historia:' : 'Title for your story:', '');
            if (title === null) return;
            const contentEls = storyPhase?.querySelectorAll('.rounded-xl p');
            const content = contentEls ? Array.from(contentEls).map(p => p.textContent).join('\n\n') : '';
            saveBtn.disabled = true;
            saveBtn.textContent = document.documentElement.lang === 'fr' ? 'Enregistrement...' : document.documentElement.lang === 'es' ? 'Guardando...' : 'Saving...';
            fetch(baseUrl() + '/save/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrf() },
                body: JSON.stringify({ content, title: title || '' })
            })
            .then(r => r.json())
            .then(data => {
                if (data.status === 'ok') {
                    saveBtn.textContent = document.documentElement.lang === 'fr' ? 'Enregistré!' : document.documentElement.lang === 'es' ? '¡Guardado!' : 'Saved!';
                    setTimeout(() => {
                        saveBtn.textContent = document.documentElement.lang === 'fr' ? 'Enregistrer & Partager' : document.documentElement.lang === 'es' ? 'Guardar & Compartir' : 'Save & Share';
                        saveBtn.disabled = false;
                    }, 2000);
                }
            });
        });
    }

    loadState();
})();