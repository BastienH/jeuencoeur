(function() {
    const video = document.getElementById('camera-feed');
    const canvas = document.getElementById('face-canvas');
    const resultCanvas = document.getElementById('result-canvas');
    const resultContainer = document.getElementById('result-container');
    const snapBtn = document.getElementById('snap-btn');
    const retryBtn = document.getElementById('retry-btn');
    const nextPromptBtn = document.getElementById('next-prompt-btn');
    const savePhotoLink = document.getElementById('save-photo-link');
    const promptContainer = document.getElementById('prompt-container');

    let stream = null;
    let capturedDataUrl = null;
    let promptCount = parseInt(sessionStorage.getItem('funny-face-factory-count') || '0');

    async function startCamera() {
        try {
            stream = await navigator.mediaDevices.getUserMedia({
                video: { facingMode: 'user', width: { ideal: 640 }, height: { ideal: 480 } }
            });
            if (video) video.srcObject = stream;
        } catch {
            const frame = document.getElementById('face-frame');
            if (frame) frame.textContent = document.documentElement.lang === 'fr' ? 'Accès caméra refusé.' : document.documentElement.lang === 'es' ? 'Acceso a cámara denegado.' : 'Camera access denied.';
        }
    }

    function stopCamera() {
        if (stream) {
            stream.getTracks().forEach(t => t.stop());
            stream = null;
        }
    }

    function captureFrame() {
        if (!video || !canvas) return null;
        const w = video.videoWidth || 640;
        const h = video.videoHeight || 480;
        canvas.width = w;
        canvas.height = h;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0);
        return canvas.toDataURL('image/png');
    }

    if (snapBtn) {
        snapBtn.addEventListener('click', () => {
            capturedDataUrl = captureFrame();
            if (capturedDataUrl && resultCanvas) {
                const img = new Image();
                img.onload = () => {
                    resultCanvas.width = img.width;
                    resultCanvas.height = img.height;
                    resultCanvas.getContext('2d').drawImage(img, 0, 0);
                    if (savePhotoLink) {
                        savePhotoLink.href = capturedDataUrl;
                        savePhotoLink.download = 'silly-face-' + Date.now() + '.png';
                    }
                };
                img.src = capturedDataUrl;
                if (resultContainer) resultContainer.classList.remove('hidden');
                snapBtn.classList.add('hidden');
                if (retryBtn) retryBtn.classList.remove('hidden');
                stopCamera();
            }
        });
    }

    if (retryBtn) {
        retryBtn.addEventListener('click', () => {
            if (resultContainer) resultContainer.classList.add('hidden');
            snapBtn.classList.remove('hidden');
            retryBtn.classList.add('hidden');
            capturedDataUrl = null;
            startCamera();
        });
    }

    if (nextPromptBtn) {
        nextPromptBtn.addEventListener('click', () => {
            const base = window.location.pathname.replace(/\/+$/, '');
            fetch(base + '/next/', { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
                .then(r => r.text())
                .then(html => {
                    if (promptContainer) promptContainer.innerHTML = html;
                    if (resultContainer) resultContainer.classList.add('hidden');
                    snapBtn.classList.remove('hidden');
                    if (retryBtn) retryBtn.classList.add('hidden');
                    capturedDataUrl = null;
                    if (!stream) startCamera();
                    promptCount++;
                    sessionStorage.setItem('funny-face-factory-count', String(promptCount));
                    checkPlayLimit('funny_face_factory');
                })
                .catch(() => {});
        });
    }

    startCamera();

    function checkPlayLimit(currentModule) {
        if (promptCount >= 7) {
            sessionStorage.setItem('funny-face-factory-count', '0');
            showSuggestionOverlay(currentModule);
        }
    }

    function showSuggestionOverlay(currentModule) {
        const allGenres = [
            { name: 'Giggle Generators', module: 'giggle_generators', url: '/en/giggle-generators/' },
            { name: 'Choice Chaos', module: 'choice_chaos', url: '/en/choice-chaos/' },
            { name: 'Mimic Mayhem', module: 'mimic_mayhem', url: '/en/mimic-mayhem/' },
            { name: 'Lip-Sync Legends', module: 'lip_sync_legends', url: '/en/lip-sync-legends/' },
            { name: 'Tale Twisters', module: 'tale_twisters', url: '/en/tale-twisters/' },
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
            <button onclick="sessionStorage.removeItem('funny-face-factory-count');this.closest('#suggestion-overlay').remove()" class="text-gray-400 hover:text-gray-600 text-sm underline">${document.documentElement.lang === 'fr' ? 'Continuer à jouer' : document.documentElement.lang === 'es' ? 'Seguir jugando' : 'Keep playing'}</button>
            <br><br>
            <a href="/en/" class="text-red-400 hover:text-red-600 text-sm underline">${document.documentElement.lang === 'fr' ? 'Arrêter' : document.documentElement.lang === 'es' ? 'Parar' : 'Stop playing'}</a>
        </div>`;
        document.body.appendChild(overlay);
    }
})();