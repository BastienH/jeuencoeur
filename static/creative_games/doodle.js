(function() {
    const canvas = document.getElementById('doodle-canvas');
    const clearBtn = document.getElementById('clear-canvas-btn');
    const saveBtn = document.getElementById('save-doodle-btn');
    const printBtn = document.getElementById('print-doodle-btn');
    const rerollBtn = document.getElementById('reroll-prompt-btn');
    const modeGuided = document.getElementById('mode-guided');
    const modeFree = document.getElementById('mode-free');
    const guidedContent = document.getElementById('guided-content');
    const timerToggle = document.getElementById('timer-toggle');
    const timerDuration = document.getElementById('timer-duration');
    const timerBadge = document.getElementById('doodle-timer-badge');
    const timerText = document.getElementById('doodle-timer-text');
    let promptCount = 0;

    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let drawing = false;
    let brushSize = 4;
    let brushColor = '#000000';
    let isGuided = true;
    let timerInterval = null;
    let timeLeft = 0;

    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    function getPos(e) {
        const rect = canvas.getBoundingClientRect();
        const sx = canvas.width / rect.width;
        const sy = canvas.height / rect.height;
        if (e.touches) {
            return { x: (e.touches[0].clientX - rect.left) * sx, y: (e.touches[0].clientY - rect.top) * sy };
        }
        return { x: (e.clientX - rect.left) * sx, y: (e.clientY - rect.top) * sy };
    }

    function startDraw(e) {
        e.preventDefault();
        drawing = true;
        const pos = getPos(e);
        ctx.beginPath();
        ctx.moveTo(pos.x, pos.y);
    }

    function draw(e) {
        e.preventDefault();
        if (!drawing) return;
        const pos = getPos(e);
        ctx.lineWidth = brushSize;
        ctx.strokeStyle = brushColor;
        ctx.lineTo(pos.x, pos.y);
        ctx.stroke();
    }

    function stopDraw(e) {
        e.preventDefault();
        if (drawing) { drawing = false; ctx.closePath(); }
    }

    canvas.addEventListener('mousedown', startDraw);
    canvas.addEventListener('mousemove', draw);
    canvas.addEventListener('mouseup', stopDraw);
    canvas.addEventListener('mouseleave', stopDraw);
    canvas.addEventListener('touchstart', startDraw, { passive: false });
    canvas.addEventListener('touchmove', draw, { passive: false });
    canvas.addEventListener('touchend', stopDraw, { passive: false });

    document.querySelectorAll('.brush-size-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            brushSize = parseInt(btn.dataset.size);
            document.querySelectorAll('.brush-size-btn').forEach(b => b.style.borderColor = 'transparent');
            btn.style.borderColor = '#26A69A';
        });
    });

    document.querySelectorAll('.color-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            brushColor = btn.dataset.color;
            document.querySelectorAll('.color-btn').forEach(b => b.style.borderColor = 'transparent');
            btn.style.borderColor = '#9ca3af';
        });
    });

    document.querySelector('.brush-size-btn')?.click();
    document.querySelector('.color-btn')?.click();

    function setMode(guided) {
        isGuided = guided;
        if (guidedContent) guidedContent.classList.toggle('hidden', !guided);
        if (modeGuided) {
            modeGuided.className = 'mode-btn px-5 py-2 rounded-lg font-semibold text-sm ' + (guided ? 'bg-primary text-white' : 'bg-gray-200 text-gray-500');
        }
        if (modeFree) {
            modeFree.className = 'mode-btn px-5 py-2 rounded-lg font-semibold text-sm ' + (guided ? 'bg-gray-200 text-gray-500' : 'bg-primary text-white');
        }
    }

    if (modeGuided) modeGuided.addEventListener('click', () => setMode(true));
    if (modeFree) modeFree.addEventListener('click', () => setMode(false));

    function stopTimer() {
        if (timerInterval) {
            clearInterval(timerInterval);
            timerInterval = null;
        }
        if (timerBadge) timerBadge.classList.add('hidden');
    }

    function startTimer(seconds) {
        stopTimer();
        timeLeft = seconds;
        if (timerText) timerText.textContent = timeLeft;
        if (timerBadge) {
            timerBadge.classList.remove('hidden');
            timerBadge.className = 'absolute top-3 right-3 z-10 bg-white/90 backdrop-blur rounded-lg px-3 py-1.5 shadow text-sm font-bold text-red-500 border border-red-200';
        }
        timerInterval = setInterval(() => {
            timeLeft--;
            if (timerText) timerText.textContent = Math.max(0, timeLeft);
            if (timeLeft <= 3 && timeLeft > 0 && timerBadge) {
                timerBadge.className = 'absolute top-3 right-3 z-10 bg-red-500/90 backdrop-blur rounded-lg px-3 py-1.5 shadow text-sm font-bold text-white border border-red-300 animate-pulse';
            }
            if (timeLeft <= 0) {
                stopTimer();
                if (saveBtn) saveBtn.click();
            }
        }, 1000);
    }

    function resetTimer() {
        if (timerToggle && timerToggle.checked) {
            var sec = parseInt(timerDuration?.value) || 20;
            if (sec < 5) sec = 5;
            startTimer(sec);
        } else {
            stopTimer();
        }
    }

    if (timerToggle) {
        timerToggle.addEventListener('change', resetTimer);
    }
    if (timerDuration) {
        timerDuration.addEventListener('input', function() {
            if (timerToggle && timerToggle.checked) {
                var sec = parseInt(this.value) || 20;
                if (sec < 5) sec = 5;
                startTimer(sec);
            }
        });
    }

    if (clearBtn) {
        clearBtn.addEventListener('click', () => {
            ctx.fillStyle = '#ffffff';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
        });
    }

    function getCsrf() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
    }

    function getData(attr) {
        const el = document.querySelector('[data-' + attr + ']');
        return el?.dataset?.[attr] || '';
    }

    if (saveBtn) {
        saveBtn.addEventListener('click', () => {
            const dataUrl = canvas.toDataURL('image/png');
            saveBtn.disabled = true;
            saveBtn.textContent = document.documentElement.lang === 'fr' ? 'Enregistrement...' : document.documentElement.lang === 'es' ? 'Guardando...' : 'Saving...';
            const base = window.location.pathname.replace(/\/+$/, '');
            fetch(base + '/save/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrf(),
                },
                body: JSON.stringify({ image: dataUrl, subject: getData('subject'), emotion: getData('emotion'), accessory: getData('accessory') })
            })
            .then(r => r.json())
            .then(data => {
                if (data.status === 'ok') {
                    if (data.anonymous_id) {
                        document.cookie = 'doodle_anon_id=' + data.anonymous_id + ';path=/;max-age=31536000';
                    }
                    saveBtn.textContent = document.documentElement.lang === 'fr' ? 'Enregistré!' : document.documentElement.lang === 'es' ? '¡Guardado!' : 'Saved!';
                    setTimeout(() => { saveBtn.textContent = document.documentElement.lang === 'fr' ? 'Enregistrer le dessin' : document.documentElement.lang === 'es' ? 'Guardar dibujo' : 'Save Drawing'; saveBtn.disabled = false; }, 2000);
                }
            });
        });
    }

    if (printBtn) {
        printBtn.addEventListener('click', () => {
            const w = window.open('', '_blank');
            if (!w) return;
            w.document.write('<img src="' + canvas.toDataURL() + '" style="max-width:100%">');
            w.document.close();
            w.focus();
            w.print();
        });
    }

    if (rerollBtn) {
        rerollBtn.addEventListener('click', () => {
            promptCount++;
            checkPlayLimit('doodle_dash');
            if (promptCount < 7) {
                fetch(window.location.pathname.replace(/\/+$/, '') + '/next/', { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
                    .then(r => r.text())
                    .then(html => {
                        var parser = new DOMParser();
                        var doc = parser.parseFromString(html, 'text/html');
                        var newPrompt = doc.querySelector('.bg-white.rounded-2xl');
                        if (newPrompt) {
                            var oldPrompt = document.querySelector('.bg-white.rounded-2xl.shadow-lg.p-6');
                            if (oldPrompt && oldPrompt.id !== 'result-container') oldPrompt.replaceWith(newPrompt);
                        }
                        ctx.fillStyle = '#ffffff';
                        ctx.fillRect(0, 0, canvas.width, canvas.height);
                        resetTimer();
                    })
                    .catch(function() { showError(document.documentElement.lang === 'fr' ? 'Erreur de connexion' : document.documentElement.lang === 'es' ? 'Error de conexión' : 'Connection error'); });
            }
        });
    }

    function checkPlayLimit(currentModule) {
        if (promptCount >= 7) {
            promptCount = 0;
            showSuggestionOverlay(currentModule);
        }
    }

    window.resetCurrentGameCounter = function() { promptCount = 0; };

    resetTimer();

})();
