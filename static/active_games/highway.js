(function() {
    const startTripBtn = document.getElementById('start-trip-btn');
    const endTripBtn = document.getElementById('end-trip-btn');
    const updateProgressBtn = document.getElementById('update-progress-btn');
    const progressInput = document.getElementById('progress-input');
    const progressBar = document.getElementById('progress-bar');
    const progressPct = document.getElementById('progress-pct');
    const tripSetup = document.getElementById('trip-setup');
    const tripActive = document.getElementById('trip-active');
    const boredomBusterBtn = document.getElementById('boredom-buster-btn');

    let tripId = null;
    let promptCount = 0;

    function updateProgressUI(pct) {
        pct = Math.min(100, Math.max(0, pct));
        if (progressBar) progressBar.style.width = pct + '%';
        if (progressPct) progressPct.textContent = pct + '%';
    }

    function getBaseUrl() {
        return window.location.pathname.replace(/\/+$/, '');
    }

    function getCsrf() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
    }

    if (startTripBtn) {
        startTripBtn.addEventListener('click', () => {
            const distance = document.getElementById('distance-input')?.value || 100;
            fetch(getBaseUrl() + '/start-trip/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrf() },
                body: JSON.stringify({ distance: parseFloat(distance), lat: null, lon: null })
            })
            .then(r => r.json())
            .then(data => {
                if (data.status === 'ok') {
                    tripId = data.trip_id;
                    if (tripSetup) tripSetup.classList.add('hidden');
                    if (tripActive) tripActive.classList.remove('hidden');
                    updateProgressUI(0);
                    if (boredomBusterBtn) {
                        boredomBusterBtn.setAttribute('hx-vals', JSON.stringify({ trip_id: tripId }));
                        htmx.process(boredomBusterBtn);
                    }
                }
            })
            .catch(() => showError(document.documentElement.lang === 'fr' ? 'Erreur de connexion' : document.documentElement.lang === 'es' ? 'Error de conexión' : 'Connection error'));
        });
    }

    if (updateProgressBtn) {
        updateProgressBtn.addEventListener('click', () => {
            const val = parseInt(progressInput?.value);
            if (isNaN(val) || val < 0 || val > 100) {
                if (progressInput) {
                    progressInput.style.borderColor = '#ef4444';
                    setTimeout(() => { if (progressInput) progressInput.style.borderColor = ''; }, 2000);
                }
                showError(document.documentElement.lang === 'fr' ? 'Entrez un nombre entre 0 et 100' : document.documentElement.lang === 'es' ? 'Ingrese un número entre 0 y 100' : 'Enter a number between 0 and 100');
                return;
            }
            if (tripId) {
                updateProgressUI(val);
                fetch(getBaseUrl() + '/update-progress/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrf() },
                    body: JSON.stringify({ trip_id: tripId, progress: val })
                }).catch(() => showError(document.documentElement.lang === 'fr' ? 'Erreur de connexion' : document.documentElement.lang === 'es' ? 'Error de conexión' : 'Connection error'));
            }
        });
    }

    if (endTripBtn) {
        endTripBtn.addEventListener('click', () => {
            if (tripId) {
                fetch(getBaseUrl() + '/end-trip/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrf() },
                    body: JSON.stringify({ trip_id: tripId })
                }).catch(() => showError(document.documentElement.lang === 'fr' ? 'Erreur de connexion' : document.documentElement.lang === 'es' ? 'Error de conexión' : 'Connection error'));
                tripId = null;
            }
            if (tripActive) tripActive.classList.add('hidden');
            if (tripSetup) tripSetup.classList.remove('hidden');
            updateProgressUI(0);
        });
    }

    var ttsToggle = document.getElementById('tts-toggle');

    function speakGameContent() {
        if (ttsToggle && ttsToggle.checked) {
            var container = document.getElementById('game-content');
            if (!container) return;
            var nameEl = container.querySelector('h3');
            var instrEl = container.querySelector('p');
            var text = '';
            if (nameEl) text += nameEl.textContent + '. ';
            if (instrEl) text += instrEl.textContent;
            if (text) {
                var utterance = new SpeechSynthesisUtterance(text);
                utterance.lang = document.documentElement.lang || 'en';
                speechSynthesis.cancel();
                speechSynthesis.speak(utterance);
            }
        }
    }

    if (ttsToggle) {
        ttsToggle.addEventListener('change', function() {
            if (this.checked) {
                speakGameContent();
            } else {
                speechSynthesis.cancel();
            }
        });
    }

    if (boredomBusterBtn) {
        boredomBusterBtn.addEventListener('htmx:beforeRequest', function(e) {
            if (window.gameFilters) {
                var filters = window.gameFilters.getAll();
                var params = {};
                if (filters.age_group) params.age_group = filters.age_group;
                var qs = new URLSearchParams(params).toString();
                if (qs) {
                    var orig = e.detail.requestConfig;
                    orig.path = orig.path + (orig.path.includes('?') ? '&' : '?') + qs;
                }
            }
        });
        boredomBusterBtn.addEventListener('htmx:afterSwap', function() {
            promptCount++;
            checkPlayLimit('highway_hijinks');
            if (ttsToggle && ttsToggle.checked) speakGameContent();
        });
    }

    function checkPlayLimit(currentModule) {
        if (promptCount >= 7) {
            promptCount = 0;
            showSuggestionOverlay(currentModule);
        }
    }

    window.resetCurrentGameCounter = function() { promptCount = 0; };
})();
