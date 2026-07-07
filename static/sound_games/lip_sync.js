(function() {
    const actionBtn = document.getElementById('action-btn');
    const countdownDisplay = document.getElementById('countdown-display');
    const reverseToggle = document.getElementById('reverse-toggle');
    const reverseOptions = document.getElementById('reverse-options');
    const soundContainer = document.getElementById('sound-container');
    let promptCount = parseInt(sessionStorage.getItem('lip-sync-legends-count') || '0');

    if (actionBtn) {
        actionBtn.addEventListener('click', () => {
            if (!countdownDisplay) return;
            actionBtn.disabled = true;
            countdownDisplay.classList.remove('hidden');
            let count = 3;
            countdownDisplay.textContent = count;
            const interval = setInterval(() => {
                count--;
                if (count > 0) {
                    countdownDisplay.textContent = count;
                } else if (count === 0) {
                    countdownDisplay.textContent = 'GO!';
                } else {
                    clearInterval(interval);
                    countdownDisplay.classList.add('hidden');
                    actionBtn.disabled = false;
                }
            }, 1000);
        });
    }

    if (reverseToggle) {
        reverseToggle.addEventListener('click', () => {
            const isReverse = !reverseToggle.classList.contains('bg-purple-600');
            reverseToggle.classList.toggle('bg-purple-600');
            reverseToggle.classList.toggle('text-white');
            reverseToggle.classList.toggle('bg-gray-200');
            reverseToggle.classList.toggle('text-gray-700');
            reverseToggle.textContent = isReverse ? 'Reverse Mode: ON' : 'Reverse Mode: OFF';
            if (reverseOptions) reverseOptions.classList.toggle('hidden');

            if (isReverse && soundContainer) {
                const nameEl = soundContainer.querySelector('.text-2xl');
                const name = nameEl?.textContent?.trim() || '';
                const words = name.split(/\s+/).filter(Boolean);
                const options = reverseOptions?.querySelectorAll('.reverse-option');
                if (options && words.length >= 4) {
                    options.forEach((opt, i) => {
                        opt.textContent = words[i] || '???';
                    });
                }
            }
        });
    }

    document.querySelectorAll('.reverse-option').forEach(opt => {
        opt.addEventListener('click', () => {
            opt.classList.add('ring-4', 'ring-green-400');
        });
    });

    document.addEventListener('htmx:afterSwap', (e) => {
        if (e.detail.target === soundContainer) {
            promptCount++;
            sessionStorage.setItem('lip-sync-legends-count', String(promptCount));
            checkPlayLimit('lip_sync_legends');
        }
    });

    function checkPlayLimit(currentModule) {
        if (promptCount >= 7) {
            sessionStorage.setItem('lip-sync-legends-count', '0');
            showSuggestionOverlay(currentModule);
        }
    }

    function showSuggestionOverlay(currentModule) {
        const allGenres = [
            { name: 'Giggle Generators', module: 'giggle_generators', slug: 'giggle-generators' },
            { name: 'Choice Chaos', module: 'choice_chaos', slug: 'choice-chaos' },
            { name: 'Mimic Mayhem', module: 'mimic_mayhem', slug: 'mimic-mayhem' },
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
            <button onclick="sessionStorage.removeItem('lip-sync-legends-count');this.closest('#suggestion-overlay').remove()" class="text-gray-400 hover:text-gray-600 text-sm underline">${document.documentElement.lang === 'fr' ? 'Continuer à jouer' : document.documentElement.lang === 'es' ? 'Seguir jugando' : 'Keep playing'}</button>
            <br><br>
            <a href="/${lang}/" class="text-red-400 hover:text-red-600 text-sm underline">${document.documentElement.lang === 'fr' ? 'Arrêter' : document.documentElement.lang === 'es' ? 'Parar' : 'Stop playing'}</a>
        </div>`;
        document.body.appendChild(overlay);
    }
})();
