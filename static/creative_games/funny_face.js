(function() {
    var promptContainer = document.getElementById('prompt-container');
    var doneBtn = document.getElementById('done-btn');
    var anotherBtn = document.getElementById('another-btn');
    var resetCounterBtn = document.getElementById('reset-counter-btn');
    var faceCounter = document.getElementById('face-counter');

    var cameraToggleBtn = document.getElementById('camera-toggle-btn');
    var cameraSection = document.getElementById('camera-section');
    var cameraContainer = document.getElementById('camera-container');
    var video = document.getElementById('camera-feed');
    var canvas = document.getElementById('face-canvas');
    var resultCanvas = document.getElementById('result-canvas');
    var resultContainer = document.getElementById('result-container');
    var snapBtn = document.getElementById('snap-btn');
    var retryBtn = document.getElementById('retry-btn');
    var savePhotoLink = document.getElementById('save-photo-link');
    var fallbackInput = document.getElementById('camera-fallback-input');

    var promptCount = 0;
    var cameraStream = null;
    var cameraActive = false;
    var capturedDataUrl = null;
    var cameraSupported = !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia);

    function updateCounter() {
        if (faceCounter) faceCounter.textContent = promptCount;
    }

    function baseUrl() {
        return window.location.pathname.replace(/\/+$/, '');
    }

    function loadNextPrompt() {
        fetch(baseUrl() + '/next/', { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
            .then(function(r) { return r.text(); })
            .then(function(html) {
                var promptText = document.getElementById('prompt-text');
                if (promptText) promptText.innerHTML = html;
                if (resultContainer) resultContainer.classList.add('hidden');
            })
            .catch(function() { showError(getMsg('connection_error')); });
    }

    function getMsg(key) {
        var lang = document.documentElement.lang || 'en';
        var msgs = {
            connection_error: { en: 'Connection error', fr: 'Erreur de connexion', es: 'Error de conexión' },
        };
        return msgs[key]?.[lang] || msgs[key]?.en || key;
    }

    if (doneBtn) {
        doneBtn.addEventListener('click', function() {
            promptCount++;
            updateCounter();
            checkPlayLimit('funny_face_factory');
            loadNextPrompt();
        });
    }

    if (anotherBtn) {
        anotherBtn.addEventListener('click', function() {
            loadNextPrompt();
        });
    }

    if (resetCounterBtn) {
        resetCounterBtn.addEventListener('click', function() {
            promptCount = 0;
            updateCounter();
        });
    }

    function stopCamera() {
        if (cameraStream) {
            cameraStream.getTracks().forEach(function(t) { t.stop(); });
            cameraStream = null;
        }
        cameraActive = false;
        if (video) video.srcObject = null;
    }

    function startCamera() {
        if (!cameraSupported) {
            if (fallbackInput) fallbackInput.click();
            return;
        }
        if (cameraActive) return;
        navigator.mediaDevices.getUserMedia({ video: true, audio: false })
            .then(function(stream) {
                cameraStream = stream;
                if (video) {
                    video.srcObject = stream;
                    video.play().catch(function(){});
                }
                cameraActive = true;
            })
            .catch(function() {
                cameraSupported = false;
                if (fallbackInput) fallbackInput.click();
            });
    }

    if (cameraToggleBtn && cameraSection) {
        cameraToggleBtn.addEventListener('click', function() {
            var isHidden = cameraSection.classList.contains('hidden');
            cameraSection.classList.toggle('hidden');
            cameraToggleBtn.textContent = isHidden
                ? (document.documentElement.lang === 'fr' ? 'Fermer la caméra' : document.documentElement.lang === 'es' ? 'Cerrar cámara' : 'Close camera') + ' 📸'
                : (document.documentElement.lang === 'fr' ? 'Prendre une photo (optionnel)' : document.documentElement.lang === 'es' ? 'Tomar una foto (opcional)' : 'Take a photo (optional)') + ' 📸';
            if (isHidden) {
                setTimeout(startCamera, 300);
            } else {
                stopCamera();
                if (resultContainer) resultContainer.classList.add('hidden');
                if (snapBtn) snapBtn.classList.remove('hidden');
                if (retryBtn) retryBtn.classList.add('hidden');
                capturedDataUrl = null;
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

    function captureFrame() {
        if (!video || !canvas || !cameraActive) return null;
        var w = video.videoWidth || 640;
        var h = video.videoHeight || 480;
        canvas.width = w;
        canvas.height = h;
        var ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0, w, h);
        return canvas.toDataURL('image/png');
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
                    savePhotoLink.onclick = function(e) {
                        e.preventDefault();
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
            if (snapBtn) snapBtn.classList.add('hidden');
            if (retryBtn) retryBtn.classList.remove('hidden');
            stopCamera();
        }
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
            if (snapBtn) snapBtn.classList.remove('hidden');
            if (retryBtn) retryBtn.classList.add('hidden');
            capturedDataUrl = null;
            startCamera();
        });
    }

    function checkPlayLimit(currentModule) {
        if (promptCount >= 7) {
            promptCount = 0;
            updateCounter();
            showSuggestionOverlay(currentModule);
        }
    }

    window.resetCurrentGameCounter = function() {
        promptCount = 0;
        updateCounter();
    };

    updateCounter();
})();
