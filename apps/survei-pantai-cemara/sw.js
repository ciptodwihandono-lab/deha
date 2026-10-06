// Aplikasi dibuka dari cache di HP (cepat, juga tanpa sinyal), lalu diperiksa
// diam-diam ke server. Bila ada file yang berubah, cache diperbarui dan
// halaman diberi tahu agar memuat versi baru. Tidak perlu menaikkan versi
// manual: perubahan apa pun di index.html terdeteksi dengan membandingkan isi.
const CACHE = 'survei-cemara';
const FILES = ['./index.html', './manifest.webmanifest', './icon.svg', './icon-192.png', './icon-512.png', './icon-maskable-512.png', './apple-touch-icon.png'];
const INDEX = new URL('./index.html', self.registration.scope).href;

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE)
      .then((c) => c.addAll(FILES.map((f) => new Request(f, { cache: 'reload' }))))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

function keyFor(req) {
  // Halaman aplikasi (./ atau ./index.html, dengan atau tanpa ?query) disimpan di satu kunci.
  if (req.mode === 'navigate') return INDEX;
  const u = new URL(req.url);
  if (u.href.split('?')[0] === self.registration.scope) return INDEX;
  return u.origin + u.pathname;
}

async function refresh(key) {
  const cache = await caches.open(CACHE);
  const res = await fetch(key, { cache: 'no-store' });
  if (!res.ok) return false;
  const old = await cache.match(key);
  const [a, b] = await Promise.all([res.clone().arrayBuffer(), old ? old.arrayBuffer() : Promise.resolve(null)]);
  await cache.put(key, res);
  if (!b || a.byteLength !== b.byteLength) return !!b;
  const x = new Uint8Array(a), y = new Uint8Array(b);
  for (let i = 0; i < x.length; i++) if (x[i] !== y[i]) return true;
  return false;
}

async function checkAll() {
  const keys = FILES.map((f) => new URL(f, self.registration.scope).href);
  const changed = (await Promise.all(keys.map((k) => refresh(k).catch(() => false)))).some(Boolean);
  if (changed) {
    const clients = await self.clients.matchAll({ type: 'window' });
    clients.forEach((c) => c.postMessage({ type: 'updated' }));
  }
  return changed;
}

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET' || new URL(req.url).origin !== self.location.origin) return;
  const key = keyFor(req);
  e.respondWith(
    caches.match(key).then((hit) => hit || fetch(req).then((res) => {
      if (res.ok) { const copy = res.clone(); caches.open(CACHE).then((c) => c.put(key, copy)); }
      return res;
    }).catch(() => caches.match(INDEX)))
  );
  if (key === INDEX) e.waitUntil(checkAll().catch(() => {}));
});

self.addEventListener('message', (e) => {
  if (e.data && e.data.type === 'check') e.waitUntil(checkAll().catch(() => {}));
});
