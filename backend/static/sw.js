// sw.js

const CACHE_NAME = 'my-site-cache-v1';
const urlsToCache = [
    '/',
    '/static/css/style.css',
    '/static/js/app.js',
    // Add other static files to cache as needed
];

self.addEventListener('install', event => {
    // Perform installation steps
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                console.log('Opened cache');
                return cache.addAll(urlsToCache);
            })
    );
});

self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                // Cache hit - return response
                if (response) {
                    return response;
                }
                return fetch(event.request);
            })
    );
});
    