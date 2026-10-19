// Offline shell. Bump CACHE whenever any asset changes.
const CACHE = 'midpoint-v1';
const ASSETS = [
  './', './index.html', './manifest.webmanifest',
  './icons/icon-192.png', './icons/icon-512.png',
  './icons/icon-maskable-512.png', './icons/apple-touch-icon.png',
];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(ASSETS)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim()),
  );
});

self.addEventListener('fetch', (e) => {
  const { request } = e;
  if (request.method !== 'GET' || new URL(request.url).origin !== self.location.origin) return;

  if (request.mode === 'navigate') {
    e.respondWith(
      fetch(request)
        .then((res) => { const c = res.clone(); caches.open(CACHE).then((k) => k.put('./index.html', c)); return res; })
        .catch(() => caches.match('./index.html', { ignoreSearch: true })),
    );
    return;
  }
  e.respondWith(
    caches.match(request, { ignoreSearch: true }).then((hit) =>
      hit || fetch(request).then((res) => {
        if (res && res.ok) { const c = res.clone(); caches.open(CACHE).then((k) => k.put(request, c)); }
        return res;
      }),
    ),
  );
});
