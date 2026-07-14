(function() {
    'use strict';

    if (!('serviceWorker' in navigator)) return;

    // --- Service Worker Registration ---

    navigator.serviceWorker.register('/static/sw.js', { scope: '/' })
        .then(function(reg) {
            reg.addEventListener('updatefound', function() {
                var newWorker = reg.installing;
                if (newWorker) {
                    newWorker.addEventListener('statechange', function() {
                        if (newWorker.state === 'activated') {
                            newWorker.postMessage({ type: 'skip-waiting' });
                        }
                    });
                }
            });
        })
        .catch(function(err) {
            console.warn('SW registration failed:', err);
        });

    // --- Platform Detection ---

    function detectPlatform() {
        var ua = navigator.userAgent || '';
        var isIOS = /iPhone|iPad|iPod/.test(ua) && !window.MSStream;
        var isAndroid = /android/i.test(ua);
        var isSafari = /Safari/.test(ua) && !/Chrome/.test(ua);
        var isChrome = /CriOS|Chrome/.test(ua) && !/SamsungBrowser/.test(ua) && !/Edg/.test(ua) && !window.opr;
        var isFirefox = /Firefox/.test(ua) || /FxiOS/.test(ua);
        var isSamsung = /SamsungBrowser/.test(ua);

        if (isIOS) return 'ios';
        if (isAndroid && isChrome) return 'android-chrome';
        if (isAndroid && isFirefox) return 'android-firefox';
        if (isAndroid && isSamsung) return 'android-samsung';
        if (isAndroid) return 'android-other';
        if (isChrome) return 'desktop-chrome';
        return 'other';
    }

    function isStandalone() {
        return window.navigator.standalone ||
               window.matchMedia('(display-mode: standalone)').matches ||
               window.matchMedia('(display: fullscreen)').matches;
    }

    // --- Install State ---

    var STORAGE_KEYS = {
        INSTALLED: 'pwa-installed',
        REJECTED: 'pwa-rejected',
        REJECTED_AT: 'pwa-rejected-at'
    };

    function getState() {
        if (localStorage.getItem(STORAGE_KEYS.INSTALLED)) return 'installed';
        var rejectedAt = localStorage.getItem(STORAGE_KEYS.REJECTED_AT);
        if (rejectedAt) {
            var oneWeek = 7 * 24 * 60 * 60 * 1000;
            if (Date.now() - parseInt(rejectedAt) < oneWeek) return 'rejected';
            localStorage.removeItem(STORAGE_KEYS.REJECTED);
            localStorage.removeItem(STORAGE_KEYS.REJECTED_AT);
        }
        return 'new';
    }

    function markInstalled() {
        localStorage.setItem(STORAGE_KEYS.INSTALLED, Date.now().toString());
    }

    function markRejected() {
        localStorage.setItem(STORAGE_KEYS.REJECTED, '1');
        localStorage.setItem(STORAGE_KEYS.REJECTED_AT, Date.now().toString());
    }

    // --- UI Creation ---

    function createInstallButton() {
        var btn = document.createElement('button');
        btn.id = 'pwa-install-btn';
        btn.setAttribute('aria-label', 'Install Jeu en Coeur');
        btn.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">' +
            '<path d="M12 3v12m0 0l-4-4m4 4l4-4"/>' +
            '<path d="M4 17v2a2 2 0 002 2h12a2 2 0 002-2v-2"/>' +
            '</svg> <span>Install</span>';
        btn.style.cssText = 'display:inline-flex;align-items:center;gap:4px;background:#26A69A;color:#fff;border:none;border-radius:9999px;padding:6px 14px;font-size:13px;font-weight:600;cursor:pointer;white-space:nowrap;transition:background 0.2s;';
        btn.addEventListener('mouseenter', function() { btn.style.background = '#00796B'; });
        btn.addEventListener('mouseleave', function() { btn.style.background = '#26A69A'; });
        return btn;
    }

    function createDialog(platform) {
        var overlay = document.createElement('div');
        overlay.id = 'pwa-install-overlay';
        overlay.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,0.5);display:flex;align-items:center;justify-content:center;z-index:9999;padding:1rem;';

        var dialog = document.createElement('div');
        dialog.style.cssText = 'background:#fff;border-radius:20px;padding:2rem;max-width:340px;width:100%;text-align:center;box-shadow:0 8px 32px rgba(0,0,0,0.12);';

        var title = '<h2 style="color:#00796B;font-size:1.25rem;font-weight:700;margin-bottom:0.5rem;">Add to Home Screen</h2>';
        var body = '';

        if (platform === 'ios') {
            body = '<p style="color:#666;font-size:0.9rem;line-height:1.6;margin-bottom:1.5rem;">' +
                'Tap the <strong>Share</strong> button in Safari, then choose <strong>"Add to Home Screen"</strong>.</p>' +
                '<div style="display:flex;align-items:center;justify-content:center;gap:12px;margin-bottom:1.5rem;">' +
                '<div style="text-align:center;">' +
                '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#26A69A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom:4px;">' +
                '<path d="M4 12v8a2 2 0 002 2h12a2 2 0 002-2v-8"/><polyline points="16 6 12 2 8 6"/><line x1="12" y1="2" x2="12" y2="15"/>' +
                '</svg><br><span style="font-size:0.75rem;color:#888;">Share</span></div>' +
                '<div style="text-align:center;">' +
                '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#26A69A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom:4px;">' +
                '<rect x="3" y="3" width="18" height="18" rx="3"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/>' +
                '</svg><br><span style="font-size:0.75rem;color:#888;">Add to Home</span></div>' +
                '</div>';
        } else {
            body = '<p style="color:#666;font-size:0.9rem;line-height:1.6;margin-bottom:1.5rem;">' +
                'Open your browser menu, then tap <strong>"Add to Home Screen"</strong>.</p>' +
                '<div style="text-align:center;margin-bottom:1.5rem;">' +
                '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#26A69A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
                '<circle cx="12" cy="5" r="1.5"/><circle cx="12" cy="12" r="1.5"/><circle cx="12" cy="19" r="1.5"/>' +
                '</svg><br><span style="font-size:0.75rem;color:#888;">Menu</span>' +
                '</div>';
        }

        var closeBtn = '<button id="pwa-install-close" style="background:#26A69A;color:#fff;border:none;border-radius:12px;padding:10px 28px;font-size:0.95rem;font-weight:600;cursor:pointer;transition:background 0.2s;">Got it</button>';
        var dismissBtn = '<button id="pwa-install-dismiss" style="background:none;border:none;color:#999;font-size:0.8rem;cursor:pointer;margin-top:12px;text-decoration:underline;">Don\'t show again</button>';

        dialog.innerHTML = title + body + closeBtn + dismissBtn;
        overlay.appendChild(dialog);
        document.body.appendChild(overlay);

        var closeBtnEl = document.getElementById('pwa-install-close');
        var dismissBtnEl = document.getElementById('pwa-install-dismiss');
        var overlayEl = document.getElementById('pwa-install-overlay');

        function close() { overlayEl.remove(); }

        closeBtnEl.addEventListener('click', close);
        dismissBtnEl.addEventListener('click', function() {
            markRejected();
            close();
        });
        overlayEl.addEventListener('click', function(e) {
            if (e.target === overlayEl) {
                markRejected();
                close();
            }
        });

        closeBtnEl.addEventListener('mouseenter', function() { closeBtnEl.style.background = '#00796B'; });
        closeBtnEl.addEventListener('mouseleave', function() { closeBtnEl.style.background = '#26A69A'; });
    }

    // --- Init ---

    function init() {
        if (isStandalone()) {
            markInstalled();
            return;
        }

        var platform = detectPlatform();
        var state = getState();

        if (state === 'installed') return;

        var headerNav = document.querySelector('header .flex.items-center');
        if (!headerNav) return;

        if (platform === 'android-chrome' || platform === 'desktop-chrome') {
            var deferredPrompt = null;
            var btn = createInstallButton();
            btn.style.display = 'none';
            headerNav.insertBefore(btn, headerNav.firstChild);

            window.addEventListener('beforeinstallprompt', function(e) {
                e.preventDefault();
                deferredPrompt = e;
                if (state === 'new') {
                    btn.style.display = 'inline-flex';
                } else if (state === 'rejected') {
                    btn.style.display = 'inline-flex';
                }
            });

            btn.addEventListener('click', function() {
                if (!deferredPrompt) return;
                deferredPrompt.prompt();
                deferredPrompt.userChoice.then(function(result) {
                    if (result.outcome === 'accepted') {
                        markInstalled();
                        btn.remove();
                    } else {
                        markRejected();
                    }
                    deferredPrompt = null;
                });
            });

            window.addEventListener('appinstalled', function() {
                markInstalled();
                btn.remove();
            });
        } else if (platform !== 'other' && state === 'new') {
            createDialog(platform);
        } else if (platform !== 'other' && state === 'rejected') {
            var retryBtn = createInstallButton();
            retryBtn.style.display = 'inline-flex';
            retryBtn.querySelector('span').textContent = 'Install';
            headerNav.insertBefore(retryBtn, headerNav.firstChild);
            retryBtn.addEventListener('click', function() {
                createDialog(platform);
            });
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
