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
    let promptCount = 0;

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
            stopMeter();
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
            checkPlayLimit('mimic_mayhem');
        }
    });

    function checkPlayLimit(currentModule) {
        if (promptCount >= 7) {
            promptCount = 0;
            showSuggestionOverlay(currentModule);
        }
    }

    window.resetCurrentGameCounter = function() { promptCount = 0; };
})();
