(function() {
    const questionContainer = document.getElementById('question-container');

    let promptCount = 0;

    function getCsrf() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
    }

    function spawnConfetti(btn) {
        const colors = ['#26A69A', '#E8836A', '#FFD54F', '#10b981', '#3b82f6', '#ef4444'];
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
        const base = window.location.pathname.replace(/\/+$/, '') + '/reroll/';
        const cat = document.getElementById('category-filter')?.value || '';
        const age = document.getElementById('age-filter')?.value || '';
        const params = new URLSearchParams();
        if (cat) params.set('category', cat);
        if (age) params.set('age_group', age);
        const url = base + (params.toString() ? '?' + params.toString() : '');
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
                checkPlayLimit('choice_chaos');
            })
            .catch(() => showError(document.documentElement.lang === 'fr' ? 'Erreur de connexion' : document.documentElement.lang === 'es' ? 'Error de conexión' : 'Connection error'));
    }

    document.addEventListener('htmx:afterSwap', (e) => {
        if (e.detail.target?.id === 'question-container') {
            promptCount++;
            checkPlayLimit('choice_chaos');
        }
    });

    document.addEventListener('click', (e) => {
        const btn = e.target.closest('.vote-btn');
        if (!btn) return;
        const vote = btn.dataset.vote;
        const questionId = btn.dataset.questionId;
        if (!vote) return;

        document.querySelectorAll('.vote-btn').forEach(b => {
            if (b === btn) {
                b.classList.add('ring-4', 'ring-primary', 'scale-[1.03]');
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
            body: JSON.stringify({ vote, question_id: questionId })
        }).catch(() => showError(document.documentElement.lang === 'fr' ? 'Erreur de connexion' : document.documentElement.lang === 'es' ? 'Error de conexión' : 'Connection error'));

        document.querySelectorAll('.vote-btn').forEach(b => b.style.pointerEvents = 'none');
        setTimeout(advanceQuestion, 2000);
    });

    function checkPlayLimit(currentModule) {
        if (promptCount >= 7) {
            promptCount = 0;
            showSuggestionOverlay(currentModule);
        }
    }

    window.resetCurrentGameCounter = function() { promptCount = 0; };
})();