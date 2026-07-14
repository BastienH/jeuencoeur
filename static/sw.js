const CACHE_VERSION = 'v1';
const CACHE_NAME = 'jeu-en-coeur-' + CACHE_VERSION;
const OFFLINE_URL = '/offline/';

const PRECACHE_URLS = [
    OFFLINE_URL,
    '/static/manifest.json',
    '/static/icons/icon.svg',
    '/static/icons/favicon.svg',
    '/static/icons/icon-192.png',
    '/static/icons/icon-512.png',
    '/static/icons/apple-touch-icon.png',
];

self.addEventListener('install', function(event) {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(function(cache) {
                return cache.addAll(PRECACHE_URLS);
            })
            .then(function() {
                return self.skipWaiting();
            })
    );
});

self.addEventListener('activate', function(event) {
    event.waitUntil(
        caches.keys().then(function(cacheNames) {
            return Promise.all(
                cacheNames
                    .filter(function(name) { return name !== CACHE_NAME; })
                    .map(function(name) { return caches.delete(name); })
            );
        }).then(function() {
            return self.clients.claim();
        })
    );
});

self.addEventListener('fetch', function(event) {
    var request = event.request;

    if (request.method !== 'GET') return;

    var url = new URL(request.url);

    if (url.pathname === OFFLINE_URL) return;

    if (request.mode === 'navigate') {
        event.respondWith(
            fetch(request)
                .then(function(response) {
                    var clone = response.clone();
                    caches.open(CACHE_NAME).then(function(cache) {
                        cache.put(request, clone);
                    });
                    return response;
                })
                .catch(function() {
                    return caches.match(request).then(function(cached) {
                        return cached || caches.match(OFFLINE_URL);
                    });
                })
        );
        return;
    }

    if (url.pathname.startsWith('/static/') || url.pathname.startsWith('/media/')) {
        event.respondWith(
            caches.match(request).then(function(cached) {
                if (cached) return cached;
                return fetch(request).then(function(response) {
                    if (response.ok) {
                        var clone = response.clone();
                        caches.open(CACHE_NAME).then(function(cache) {
                            cache.put(request, clone);
                        });
                    }
                    return response;
                });
            })
        );
        return;
    }
});
