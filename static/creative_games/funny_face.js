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
    const cameraContainer = document.getElementById('camera-container');
    const cameraStartOverlay = document.getElementById('camera-start-overlay');
    const fallbackInput = document.getElementById('camera-fallback-input');

    let stream = null;
    let capturedDataUrl = null;
    let promptCount = parseInt(sessionStorage.getItem('funny-face-factory-count') || '0');
    let cameraActive = false;
    let cameraSupported = !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia);

    function showOverlay() {
        if (cameraStartOverlay) cameraStartOverlay.classList.remove('hidden');
    }

    function hideOverlay() {
        if (cameraStartOverlay) cameraStartOverlay.classList.add('hidden');
    }

    function setCameraMessage(msg) {
        if (cameraStartOverlay) {
            const p = cameraStartOverlay.querySelector('p');
            if (p) p.textContent = msg;
        }
    }

    async function startCamera() {
        if (!cameraSupported) {
            fallbackInput.click();
            return;
        }
        try {
            stream = await navigator.mediaDevices.getUserMedia({
                video: { facingMode: 'user', width: { ideal: 640 }, height: { ideal: 480 } }
            });
            if (video) {
                video.srcObject = stream;
                video.play().catch(function(){});
            }
            cameraActive = true;
            hideOverlay();
        } catch {
            cameraSupported = false;
            setCameraMessage(document.documentElement.lang === 'fr' ? 'Appuyer pour prendre une photo' : document.documentElement.lang === 'es' ? 'Toca para tomar una foto' : 'Tap to take a photo');
            fallbackInput.click();
        }
    }

    function stopCamera() {
        if (stream) {
            stream.getTracks().forEach(function(t) { t.stop(); });
            stream = null;
        }
        cameraActive = false;
    }

    function processImage(dataUrl) {
        capturedDataUrl = dataUrl;
        if (capturedDataUrl && resultCanvas) {
            var img = new Image();
            img.onload = function() {
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
            hideOverlay();
        }
    }

    function captureFrame() {
        if (!video || !canvas || !cameraActive) return null;
        var w = video.videoWidth || 640;
        var h = video.videoHeight || 480;
        canvas.width = w;
        canvas.height = h;
        var ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0);
        return canvas.toDataURL('image/png');
    }

    if (cameraContainer) {
        cameraContainer.addEventListener('click', function() {
            if (!cameraActive) {
                if (cameraSupported) {
                    startCamera();
                } else {
                    fallbackInput.click();
                }
            }
        });
    }

    if (fallbackInput) {
        fallbackInput.addEventListener('change', function(e) {
            var file = e.target.files && e.target.files[0];
            if (!file) return;
            var reader = new FileReader();
            reader.onload = function(ev) {
                processImage(ev.target.result);
            };
            reader.readAsDataURL(file);
            fallbackInput.value = '';
        });
    }

    if (snapBtn) {
        snapBtn.addEventListener('click', function() {
            if (!cameraActive) {
                startCamera();
                return;
            }
            var dataUrl = captureFrame();
            if (dataUrl) processImage(dataUrl);
        });
    }

    if (retryBtn) {
        retryBtn.addEventListener('click', function() {
            if (resultContainer) resultContainer.classList.add('hidden');
            snapBtn.classList.remove('hidden');
            retryBtn.classList.add('hidden');
            capturedDataUrl = null;
            showOverlay();
            cameraActive = false;
        });
    }

    if (nextPromptBtn) {
        nextPromptBtn.addEventListener('click', function() {
            var base = window.location.pathname.replace(/\/+$/, '');
            fetch(base + '/next/', { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
                .then(function(r) { return r.text(); })
                .then(function(html) {
                    if (promptContainer) promptContainer.innerHTML = html;
                    if (resultContainer) resultContainer.classList.add('hidden');
                    snapBtn.classList.remove('hidden');
                    if (retryBtn) retryBtn.classList.add('hidden');
                    capturedDataUrl = null;
                    showOverlay();
                    cameraActive = false;
                    promptCount++;
                    sessionStorage.setItem('funny-face-factory-count', String(promptCount));
                    checkPlayLimit('funny_face_factory');
                })
                .catch(function() {});
        });
    }

    function checkPlayLimit(currentModule) {
        if (promptCount >= 7) {
            sessionStorage.setItem('funny-face-factory-count', '0');
            showSuggestionOverlay(currentModule);
        }
    }

    function showSuggestionOverlay(currentModule) {
        var allGenres = [
            { name: 'Giggle Generators', module: 'giggle_generators', slug: 'giggle-generators' },
            { name: 'Choice Chaos', module: 'choice_chaos', slug: 'choice-chaos' },
            { name: 'Mimic Mayhem', module: 'mimic_mayhem', slug: 'mimic-mayhem' },
            { name: 'Lip-Sync Legends', module: 'lip_sync_legends', slug: 'lip-sync-legends' },
            { name: 'Tale Twisters', module: 'tale_twisters', slug: 'tale-twisters' },
            { name: 'Doodle Dash', module: 'doodle_dash', slug: 'doodle-dash' },
            { name: 'Wild Roles', module: 'wild_roles', slug: 'wild-roles' },
            { name: 'Highway Hijinks', module: 'highway_hijinks', slug: 'highway-hijinks' },
        ];
        var lang = document.documentElement.lang || 'en';
        var others = allGenres.filter(function(g) { return g.module !== currentModule; });
        var shuffled = others.sort(function() { return Math.random() - 0.5; }).slice(0, 3);
        var overlay = document.createElement('div');
        overlay.id = 'suggestion-overlay';
        overlay.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,0.6);display:flex;align-items:center;justify-content:center;z-index:9999;';
        overlay.innerHTML = '<div class="bg-white rounded-2xl shadow-2xl p-8 max-w-sm mx-4 text-center">' +
            '<h2 class="text-xl font-bold text-gray-800 mb-2">🎉 ' + (document.documentElement.lang === 'fr' ? 'Bien joué!' : document.documentElement.lang === 'es' ? '¡Bien hecho!' : 'Well played!') + '</h2>' +
            '<p class="text-gray-500 mb-6">' + (document.documentElement.lang === 'fr' ? 'Tu as joué quelques parties! Tu veux essayer autre chose?' : document.documentElement.lang === 'es' ? '¡Has jugado unas cuantas veces! ¿Pruebas algo más?' : 'You have played a few rounds! Try something else?') + '</p>' +
            '<div class="space-y-3 mb-6">' +
            shuffled.map(function(g) { return '<a href="/' + lang + '/' + g.slug + '/" class="block w-full bg-purple-50 hover:bg-purple-100 border-2 border-purple-200 rounded-xl p-3 text-purple-700 font-medium transition-all">' + g.name + '</a>'; }).join('') +
            '</div>' +
            '<button onclick="sessionStorage.removeItem(\'funny-face-factory-count\');this.closest(\'#suggestion-overlay\').remove()" class="text-gray-400 hover:text-gray-600 text-sm underline">' + (document.documentElement.lang === 'fr' ? 'Continuer à jouer' : document.documentElement.lang === 'es' ? 'Seguir jugando' : 'Keep playing') + '</button>' +
            '<br><br>' +
            '<a href="/' + lang + '/" class="text-red-400 hover:text-red-600 text-sm underline">' + (document.documentElement.lang === 'fr' ? 'Arrêter' : document.documentElement.lang === 'es' ? 'Parar' : 'Stop playing') + '</a>' +
            '</div>';
        document.body.appendChild(overlay);
    }
})();
