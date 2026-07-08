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
    let promptCount = 0;
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
                    savePhotoLink.onclick = function(e) {
                        e.preventDefault();
                        var link = this;
                        resultCanvas.toBlob(function(blob) {
                            var url = URL.createObjectURL(blob);
                            var a = document.createElement('a');
                            a.href = url;
                            a.download = 'silly-face-' + Date.now() + '.png';
                            document.body.appendChild(a);
                            a.click();
                            setTimeout(function() { document.body.removeChild(a); URL.revokeObjectURL(url); }, 1000);
                        });
                    };
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
                    checkPlayLimit('funny_face_factory');
                })
                .catch(function() { showError(document.documentElement.lang === 'fr' ? 'Erreur de connexion' : document.documentElement.lang === 'es' ? 'Error de conexión' : 'Connection error'); });
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
