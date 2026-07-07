(function() {
    const soundContainer = document.getElementById('sound-container');
    const playBtn = document.getElementById('play-sound-btn');
    const meterBar = document.getElementById('meter-bar');
    const meterPct = document.getElementById('meter-pct');
    const meterStatus = document.getElementById('meter-status');

    let audioContext = null;
    let analyser = null;
    let micStream = null;
    let animFrame = null;
    let promptCount = parseInt(sessionStorage.getItem('mimic-mayhem-count') || '0');

    function getSoundUrl() {
        const nameEl = soundContainer?.querySelector('.text-2xl');
        return nameEl?.textContent?.trim() || null;
    }

    function playSound() {
        const name = getSoundUrl();
        if (!name) return;
        if (playBtn) {
            playBtn.disabled = true;
            playBtn.textContent = document.documentElement.lang === 'fr' ? 'Lecture...' : document.documentElement.lang === 'es' ? 'Reproduciendo...' : 'Playing...';
        }
        const utterance = new SpeechSynthesisUtterance(name);
        utterance.lang = 'en';
        utterance.onend = () => {
            if (playBtn) {
                playBtn.disabled = false;
                playBtn.textContent = document.documentElement.lang === 'fr' ? 'Jouer le son' : document.documentElement.lang === 'es' ? 'Reproducir sonido' : 'Play Sound';
            }
        };
        speechSynthesis.speak(utterance);
    }

    async function startMeter() {
        if (audioContext) return;
        try {
            audioContext = new (window.AudioContext || window.webkitAudioContext)();
            analyser = audioContext.createAnalyser();
            analyser.fftSize = 256;
            micStream = await navigator.mediaDevices.getUserMedia({ audio: true });
            const source = audioContext.createMediaStreamSource(micStream);
            source.connect(analyser);
            tickMeter();
        } catch {
            if (meterStatus) meterStatus.textContent = document.documentElement.lang === 'fr' ? 'Micro indisponible' : document.documentElement.lang === 'es' ? 'Micro no disponible' : 'Mic unavailable';
        }
    }

    function tickMeter() {
        if (!analyser) return;
        const data = new Uint8Array(analyser.frequencyBinCount);
        analyser.getByteFrequencyData(data);
        const avg = data.reduce((a, b) => a + b, 0) / data.length;
        const pct = Math.min(100, Math.round(avg * 1.5));
        if (meterBar) meterBar.style.width = pct + '%';
        if (meterPct) meterPct.textContent = pct + '%';
        if (meterStatus) {
            meterStatus.textContent = pct < 10 ? (document.documentElement.lang === 'fr' ? 'Fais du bruit!' : document.documentElement.lang === 'es' ? '¡Haz ruido!' : 'Make some noise!')
                : pct < 40 ? (document.documentElement.lang === 'fr' ? 'Bien!' : document.documentElement.lang === 'es' ? '¡Bien!' : 'Good!')
                : pct < 70 ? (document.documentElement.lang === 'fr' ? 'Plus fort!' : document.documentElement.lang === 'es' ? '¡Más fuerte!' : 'Louder!')
                : document.documentElement.lang === 'fr' ? 'Incroyable!' : document.documentElement.lang === 'es' ? '¡Increíble!' : 'Amazing!';
        }
        animFrame = requestAnimationFrame(tickMeter);
    }

    function stopMeter() {
        if (animFrame) cancelAnimationFrame(animFrame);
        animFrame = null;
        if (micStream) micStream.getTracks().forEach(t => t.stop());
        micStream = null;
        if (audioContext) audioContext.close();
        audioContext = null;
        analyser = null;
    }

    if (playBtn) {
        playBtn.addEventListener('click', () => {
            playSound();
            startMeter();
        });
    }

    document.addEventListener('htmx:afterSwap', (e) => {
        if (e.detail.target === soundContainer) {
            stopMeter();
            promptCount++;
            sessionStorage.setItem('mimic-mayhem-count', String(promptCount));
            checkPlayLimit('mimic_mayhem');
        }
    });

    function checkPlayLimit(currentModule) {
        if (promptCount >= 7) {
            sessionStorage.setItem('mimic-mayhem-count', '0');
            showSuggestionOverlay(currentModule);
        }
    }

    function showSuggestionOverlay(currentModule) {
        const allGenres = [
            { name: 'Giggle Generators', module: 'giggle_generators', url: '/en/giggle-generators/' },
            { name: 'Choice Chaos', module: 'choice_chaos', url: '/en/choice-chaos/' },
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
            <button onclick="sessionStorage.removeItem('mimic-mayhem-count');this.closest('#suggestion-overlay').remove()" class="text-gray-400 hover:text-gray-600 text-sm underline">${document.documentElement.lang === 'fr' ? 'Continuer à jouer' : document.documentElement.lang === 'es' ? 'Seguir jugando' : 'Keep playing'}</button>
            <br><br>
            <a href="/en/" class="text-red-400 hover:text-red-600 text-sm underline">${document.documentElement.lang === 'fr' ? 'Arrêter' : document.documentElement.lang === 'es' ? 'Parar' : 'Stop playing'}</a>
        </div>`;
        document.body.appendChild(overlay);
    }
})();
