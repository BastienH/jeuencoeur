(function() {
    const canvas = document.getElementById('doodle-canvas');
    const clearBtn = document.getElementById('clear-canvas-btn');
    const saveBtn = document.getElementById('save-doodle-btn');
    const printBtn = document.getElementById('print-doodle-btn');
    const rerollBtn = document.getElementById('reroll-prompt-btn');
    let promptCount = 0;

    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let drawing = false;
    let brushSize = 4;
    let brushColor = '#000000';

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
            btn.style.borderColor = '#7c3aed';
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
            w.document.write(`<img src="${canvas.toDataURL()}" style="max-width:100%">`);
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


})();
