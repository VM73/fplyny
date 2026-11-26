// F-plyny – service worker: soubory appky ze sítě, při výpadku z cache. Supabase se necachuje.
const CACHE = 'fplyny-13';
const SOUBORY = ['./', 'index.html', 'manifest.webmanifest', 'apple-touch-icon.png', 'icon-192.png', 'icon-512.png', 'favicon-32.png'];
self.addEventListener('install', e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(SOUBORY)).then(() => self.skipWaiting())); });
self.addEventListener('activate', e => { e.waitUntil(caches.keys().then(k => Promise.all(k.filter(x => x !== CACHE).map(x => caches.delete(x)))).then(() => self.clients.claim())); });
self.addEventListener('fetch', e => {
  const u = new URL(e.request.url);
  if (e.request.method !== 'GET' || u.origin !== location.origin) return;
  const fresh = !/\.(webp|png)$/.test(u.pathname); // stránka a skripty vždy ověřit na serveru (obejde 10min cache GitHub Pages)
  e.respondWith(fetch(e.request, fresh ? {cache: 'no-cache'} : {}).then(r => { const k = r.clone(); caches.open(CACHE).then(c => c.put(e.request, k)); return r; })
    .catch(() => caches.match(e.request).then(r => r || caches.match('index.html'))));
});
