(function() {
    var csrf = document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
    var base = window.location.pathname.replace(/\/+$/, '').replace(/\/gallery\/?$/, '');
    var lang = document.documentElement.lang || 'en';

    function getCsrf() { return csrf; }

    function getMsg(key) {
        var msgs = {
            confirmDelete: { en: 'Delete this drawing?', fr: 'Supprimer ce dessin ?', es: '¿Eliminar este dibujo?' },
            saved: { en: 'Saved!', fr: 'Enregistré !', es: '¡Guardado!' },
            error: { en: 'Error', fr: 'Erreur', es: 'Error' },
        };
        return (msgs[key] && msgs[key][lang]) || msgs[key]?.en || key;
    }

    document.querySelectorAll('.delete-doodle-btn').forEach(function(btn) {
        btn.addEventListener('click', function() {
            if (!confirm(getMsg('confirmDelete'))) return;
            var card = btn.closest('.doodle-card');
            var id = card.dataset.id;
            fetch(base + '/delete/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrf() },
                body: JSON.stringify({ id: parseInt(id) })
            })
            .then(function(r) { return r.json(); })
            .then(function(data) {
                if (data.status === 'ok') {
                    card.remove();
                } else {
                    showError(getMsg('error'));
                }
            })
            .catch(function() { showError(getMsg('error')); });
        });
    });

    var saveAllBtn = document.getElementById('save-all-btn');
    if (saveAllBtn) {
        saveAllBtn.addEventListener('click', function() {
            var imgs = document.querySelectorAll('.doodle-card img');
            if (!imgs.length) return;
            saveAllBtn.disabled = true;
            var done = 0;
            imgs.forEach(function(img) {
                var canvas = document.createElement('canvas');
                canvas.width = img.naturalWidth;
                canvas.height = img.naturalHeight;
                canvas.getContext('2d').drawImage(img, 0, 0);
                canvas.toBlob(function(blob) {
                    var url = URL.createObjectURL(blob);
                    var a = document.createElement('a');
                    a.href = url;
                    var prompt = img.closest('.doodle-card')?.querySelector('p')?.textContent?.trim().replace(/\s+/g, '-').substring(0, 40) || 'doodle';
                    a.download = prompt + '-' + Date.now() + '.png';
                    document.body.appendChild(a);
                    a.click();
                    setTimeout(function() { document.body.removeChild(a); URL.revokeObjectURL(url); }, 1000);
                    done++;
                    if (done === imgs.length) {
                        saveAllBtn.disabled = false;
                    }
                });
            });
        });
    }
})();
