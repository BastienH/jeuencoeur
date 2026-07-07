(function() {
    const canvas = document.getElementById('doodle-canvas');
    const clearBtn = document.getElementById('clear-canvas-btn');
    const saveBtn = document.getElementById('save-doodle-btn');
    const printBtn = document.getElementById('print-doodle-btn');
    const rerollBtn = document.getElementById('reroll-prompt-btn');
    let promptCount = parseInt(sessionStorage.getItem('doodle-dash-count') || '0');

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
            sessionStorage.setItem('doodle-dash-count', String(promptCount));
            checkPlayLimit('doodle_dash');
            if (promptCount < 7) window.location.reload();
        });
    }

    function checkPlayLimit(currentModule) {
        if (promptCount >= 7) {
            sessionStorage.setItem('doodle-dash-count', '0');
            showSuggestionOverlay(currentModule);
        }
    }

    function showSuggestionOverlay(currentModule) {
        const allGenres = [
            { name: 'Giggle Generators', module: 'giggle_generators', slug: 'giggle-generators' },
            { name: 'Choice Chaos', module: 'choice_chaos', slug: 'choice-chaos' },
            { name: 'Mimic Mayhem', module: 'mimic_mayhem', slug: 'mimic-mayhem' },
            { name: 'Lip-Sync Legends', module: 'lip_sync_legends', slug: 'lip-sync-legends' },
            { name: 'Tale Twisters', module: 'tale_twisters', slug: 'tale-twisters' },
            { name: 'Funny Face Factory', module: 'funny_face_factory', slug: 'funny-face-factory' },
            { name: 'Wild Roles', module: 'wild_roles', slug: 'wild-roles' },
            { name: 'Highway Hijinks', module: 'highway_hijinks', slug: 'highway-hijinks' },
        ];
        const lang = document.documentElement.lang || 'en';
        const others = allGenres.filter(g => g.module !== currentModule);
        const shuffled = others.sort(() => Math.random() - 0.5).slice(0, 3);
        const overlay = document.createElement('div');
        overlay.id = 'suggestion-overlay';
        overlay.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,0.6);display:flex;align-items:center;justify-content:center;z-index:9999;';
        overlay.innerHTML = `<div class="bg-white rounded-2xl shadow-2xl p-8 max-w-sm mx-4 text-center">
            <h2 class="text-xl font-bold text-gray-800 mb-2">🎉 ${document.documentElement.lang === 'fr' ? 'Bien joué!' : document.documentElement.lang === 'es' ? '¡Bien hecho!' : 'Well played!'}</h2>
            <p class="text-gray-500 mb-6">${document.documentElement.lang === 'fr' ? 'Tu as joué quelques parties! Tu veux essayer autre chose?' : document.documentElement.lang === 'es' ? '¡Has jugado unas cuantas veces! ¿Pruebas algo más?' : 'You have played a few rounds! Try something else?'}</p>
            <div class="space-y-3 mb-6">
                ${shuffled.map(g => `<a href="/${lang}/${g.slug}/" class="block w-full bg-purple-50 hover:bg-purple-100 border-2 border-purple-200 rounded-xl p-3 text-purple-700 font-medium transition-all">${g.name}</a>`).join('')}
            </div>
            <button onclick="sessionStorage.removeItem('doodle-dash-count');this.closest('#suggestion-overlay').remove()" class="text-gray-400 hover:text-gray-600 text-sm underline">${document.documentElement.lang === 'fr' ? 'Continuer à jouer' : document.documentElement.lang === 'es' ? 'Seguir jugando' : 'Keep playing'}</button>
            <br><br>
            <a href="/${lang}/" class="text-red-400 hover:text-red-600 text-sm underline">${document.documentElement.lang === 'fr' ? 'Arrêter' : document.documentElement.lang === 'es' ? 'Parar' : 'Stop playing'}</a>
        </div>`;
        document.body.appendChild(overlay);
    }
})();
