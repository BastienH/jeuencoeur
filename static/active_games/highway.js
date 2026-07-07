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
    let promptCount = parseInt(sessionStorage.getItem('highway-hijinks-count') || '0');

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
            .catch(() => {});
        });
    }

    if (updateProgressBtn) {
        updateProgressBtn.addEventListener('click', () => {
            const val = parseInt(progressInput?.value);
            if (!isNaN(val) && tripId) {
                updateProgressUI(val);
                fetch(getBaseUrl() + '/update-progress/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrf() },
                    body: JSON.stringify({ trip_id: tripId, progress: val })
                }).catch(() => {});
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
                }).catch(() => {});
                tripId = null;
            }
            if (tripActive) tripActive.classList.add('hidden');
            if (tripSetup) tripSetup.classList.remove('hidden');
            updateProgressUI(0);
        });
    }

    if (boredomBusterBtn) {
        boredomBusterBtn.addEventListener('htmx:afterSwap', () => {
            promptCount++;
            sessionStorage.setItem('highway-hijinks-count', String(promptCount));
            checkPlayLimit('highway_hijinks');
        });
    }

    function checkPlayLimit(currentModule) {
        if (promptCount >= 7) {
            sessionStorage.setItem('highway-hijinks-count', '0');
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
            { name: 'Wild Roles', module: 'wild_roles', slug: 'wild-roles' },
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
            <button onclick="sessionStorage.removeItem('highway-hijinks-count');this.closest('#suggestion-overlay').remove()" class="text-gray-400 hover:text-gray-600 text-sm underline">${document.documentElement.lang === 'fr' ? 'Continuer à jouer' : document.documentElement.lang === 'es' ? 'Seguir jugando' : 'Keep playing'}</button>
            <br><br>
            <a href="/${lang}/" class="text-red-400 hover:text-red-600 text-sm underline">${document.documentElement.lang === 'fr' ? 'Arrêter' : document.documentElement.lang === 'es' ? 'Parar' : 'Stop playing'}</a>
        </div>`;
        document.body.appendChild(overlay);
    }
})();