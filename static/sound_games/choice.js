(function() {
    const questionContainer = document.getElementById('question-container');
    let promptCount = parseInt(sessionStorage.getItem('choice-chaos-count') || '0');

    function getCsrf() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
    }

    function spawnConfetti(btn) {
        const colors = ['#7c3aed', '#ec4899', '#f59e0b', '#10b981', '#3b82f6', '#ef4444'];
        for (let i = 0; i < 25; i++) {
            const piece = document.createElement('div');
            piece.className = 'confetti-piece';
            piece.style.left = Math.random() * 100 + '%';
            piece.style.top = Math.random() * 50 + '%';
            piece.style.background = colors[Math.floor(Math.random() * colors.length)];
            piece.style.width = (4 + Math.random() * 6) + 'px';
            piece.style.height = (4 + Math.random() * 6) + 'px';
            piece.style.animationDuration = (1 + Math.random()) + 's';
            piece.style.animationDelay = Math.random() * 0.3 + 's';
            btn.appendChild(piece);
            setTimeout(() => piece.remove(), 2000);
        }
    }

    function advanceQuestion() {
        const url = window.location.pathname.replace(/\/+$/, '') + '/reroll/';
        fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
            .then(r => r.text())
            .then(html => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                const newContent = doc.querySelector('[class*="bg-white rounded-2xl shadow-lg"]') ||
                                   doc.querySelector('#question-container') || doc.body;
                if (questionContainer) {
                    questionContainer.innerHTML = newContent.innerHTML || html;
                }
                promptCount++;
                sessionStorage.setItem('choice-chaos-count', String(promptCount));
                checkPlayLimit('choice_chaos');
            })
            .catch(() => {});
    }

    document.addEventListener('htmx:afterSwap', (e) => {
        if (e.detail.target?.id === 'question-container') {
            promptCount++;
            sessionStorage.setItem('choice-chaos-count', String(promptCount));
            checkPlayLimit('choice_chaos');
        }
    });

    document.addEventListener('click', (e) => {
        const btn = e.target.closest('.vote-btn');
        if (!btn) return;
        const vote = btn.dataset.vote;
        if (!vote) return;

        document.querySelectorAll('.vote-btn').forEach(b => {
            if (b === btn) {
                b.classList.add('ring-4', 'ring-purple-400', 'scale-[1.03]');
                spawnConfetti(b);
            } else {
                b.classList.add('opacity-40', 'pointer-events-none');
            }
        });

        const voteResult = document.getElementById('vote-result');
        if (voteResult) {
            voteResult.textContent = (document.documentElement.lang === 'fr' ? 'Tu as choisi ' : document.documentElement.lang === 'es' ? 'Elegiste ' : 'You chose ') + (vote === 'a' ? 'Option A' : (document.documentElement.lang === 'fr' ? 'Option B' : document.documentElement.lang === 'es' ? 'Opción B' : 'Option B')) + '!';
        }

        fetch(window.location.pathname.replace(/\/+$/, '') + '/vote/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrf(),
            },
            body: JSON.stringify({ vote })
        }).catch(() => {});

        document.querySelectorAll('.vote-btn').forEach(b => b.style.pointerEvents = 'none');
        setTimeout(advanceQuestion, 2800);
    });

    function checkPlayLimit(currentModule) {
        if (promptCount >= 7) {
            sessionStorage.setItem('choice-chaos-count', '0');
            showSuggestionOverlay(currentModule);
        }
    }

    function showSuggestionOverlay(currentModule) {
        const allGenres = [
            { name: 'Giggle Generators', module: 'giggle_generators', url: '/en/giggle-generators/' },
            { name: 'Mimic Mayhem', module: 'mimic_mayhem', url: '/en/mimic-mayhem/' },
            { name: 'Lip-Sync Legends', module: 'lip_sync_legends', url: '/en/lip-sync-legends/' },
            { name: 'Tale Twisters', module: 'tale_twisters', url: '/en/tale-twisters/' },
            { name: 'Funny Face Factory', module: 'funny_face_factory', url: '/en/funny-face-factory/' },
            { name: 'Doodle Dash', module: 'doodle_dash', url: '/en/doodle-dash/' },
            { name: 'Wild Roles', module: 'wild_roles', url: '/en/wild-roles/' },
            { name: 'Highway Hijinks', module: 'highway_hijinks', url: '/en/highway-hijinks/' },
        ];
        const others = allGenres.filter(g => g.module !== currentModule);
        const shuffled = others.sort(() => Math.random() - 0.5).slice(0, 3);
        const overlay = document.createElement('div');
        overlay.id = 'suggestion-overlay';
        overlay.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,0.6);display:flex;align-items:center;justify-content:center;z-index:9999;';
        overlay.innerHTML = `<div class="bg-white rounded-2xl shadow-2xl p-8 max-w-sm mx-4 text-center">
            <h2 class="text-xl font-bold text-gray-800 mb-2">🎉 ${document.documentElement.lang === 'fr' ? 'Bien joué!' : document.documentElement.lang === 'es' ? '¡Bien hecho!' : 'Well played!'}</h2>
            <p class="text-gray-500 mb-6">${document.documentElement.lang === 'fr' ? 'Tu as joué quelques parties! Tu veux essayer autre chose?' : document.documentElement.lang === 'es' ? '¡Has jugado unas cuantas veces! ¿Pruebas algo más?' : 'You have played a few rounds! Try something else?'}</p>
            <div class="space-y-3 mb-6">
                ${shuffled.map(g => `<a href="${g.url}" class="block w-full bg-purple-50 hover:bg-purple-100 border-2 border-purple-200 rounded-xl p-3 text-purple-700 font-medium transition-all">${g.name}</a>`).join('')}
            </div>
            <button onclick="sessionStorage.removeItem('choice-chaos-count');this.closest('#suggestion-overlay').remove()" class="text-gray-400 hover:text-gray-600 text-sm underline">${document.documentElement.lang === 'fr' ? 'Continuer à jouer' : document.documentElement.lang === 'es' ? 'Seguir jugando' : 'Keep playing'}</button>
            <br><br>
            <a href="/en/" class="text-red-400 hover:text-red-600 text-sm underline">${document.documentElement.lang === 'fr' ? 'Arrêter' : document.documentElement.lang === 'es' ? 'Parar' : 'Stop playing'}</a>
        </div>`;
        document.body.appendChild(overlay);
    }
})();