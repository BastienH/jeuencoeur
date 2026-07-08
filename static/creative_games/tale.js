(function() {
    const storyPhase = document.getElementById('story-phase');
    const saveBtn = document.getElementById('save-btn');
    const clearBtn = document.getElementById('clear-btn');
    const phaseIndicator = document.getElementById('phase-indicator');

    let promptCount = 0;

    function countPrompt() {
        promptCount++;
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
            promptCount = 0;
            showSuggestionOverlay(currentModule);
        }
    }

    window.resetCurrentGameCounter = function() { promptCount = 0; };

    if (clearBtn) {
        clearBtn.addEventListener('click', () => {
            const key = 'tale_' + (document.documentElement.lang || 'en');
            sessionStorage.removeItem(key);
            loadState();
        });
    }

    var isAuthenticated = document.getElementById('auth-status')?.dataset?.authenticated === 'true';
    if (saveBtn) {
        saveBtn.addEventListener('click', () => {
            var title = window.prompt(document.documentElement.lang === 'fr' ? 'Titre de ton histoire:' : document.documentElement.lang === 'es' ? 'Título de tu historia:' : 'Title for your story:', '');
            if (title === null) return;
            if (!isAuthenticated) {
                if (!window.confirm(document.documentElement.lang === 'fr' ? 'Connecte-toi pour enregistrer ton histoire. Se connecter maintenant?' : document.documentElement.lang === 'es' ? 'Inicia sesión para guardar tu historia. ¿Iniciar sesión ahora?' : 'Log in to save your story. Log in now?')) {
                    return;
                }
            }
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
                } else if (data.status === 'login_required') {
                    window.location.href = data.login_url;
                }
            });
        });
    }

    loadState();
})();