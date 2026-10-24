// Aplikasi dibuka dari cache (cepat, juga tanpa sinyal) lalu diperiksa ke server di latar belakang.
// Potongan peta (tile) yang pernah tampil disimpan di cache terpisah agar peta tetap tampil tanpa sinyal.
const CACHE = 'peta-survei';
const TILES = 'peta-tiles';
const TILE_MAX = 6000;   // batas jumlah tile tersimpan (± 100–150 MB)
const FILES = ['./index.html', './manifest.webmanifest', './icon.svg', './icon-192.png', './icon-512.png', './icon-maskable-512.png', './apple-touch-icon.png', './vendor/leaflet.js', './vendor/leaflet.css', './vendor/sql-wasm.js', './vendor/sql-wasm.wasm'];
const SCOPE = self.registration.scope;
const INDEX = new URL('./index.html', SCOPE).href;
const OWN = new Set(FILES.map((f) => new URL(f, SCOPE).href));
const TILE_HOSTS = ['server.arcgisonline.com', 'tile.openstreetmap.org'];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(FILES.map((f) => new Request(f, { cache: 'reload' })))).then(() => self.skipWaiting()));
});
self.addEventListener('activate', (e) => {
  e.waitUntil(caches.keys().then((keys) => Promise.all(keys.filter((k) => k !== CACHE && k !== TILES).map((k) => caches.delete(k)))).then(() => self.clients.claim()));
});

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
  const changed = (await Promise.all([...OWN].map((k) => refresh(k).catch(() => false)))).some(Boolean);
  if (changed) (await self.clients.matchAll({ type: 'window' })).forEach((c) => c.postMessage({ type: 'updated' }));
}
let trimming = false;
async function trimTiles() {
  if (trimming) return; trimming = true;
  try { const c = await caches.open(TILES); const keys = await c.keys(); for (let i = 0; i < keys.length - TILE_MAX; i++) await c.delete(keys[i]); } finally { trimming = false; }
}
async function tile(req) {
  const c = await caches.open(TILES);
  const hit = await c.match(req.url);
  if (hit) return hit;
  const res = await fetch(req);
  if (res.ok && res.type !== 'opaque') { c.put(req.url, res.clone()).then(() => { if (Math.random() < 0.05) trimTiles(); }); }
  return res;
}

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const u = new URL(req.url);
  if (TILE_HOSTS.includes(u.hostname)) { e.respondWith(tile(req)); return; }
  if (u.origin !== self.location.origin) return;
  const clean = u.origin + u.pathname;
  const isApp = req.mode === 'navigate' ? (clean === SCOPE || clean === INDEX) : OWN.has(clean);
  if (!isApp) return;
  const key = req.mode === 'navigate' || clean === SCOPE ? INDEX : clean;
  e.respondWith(caches.match(key).then((hit) => hit || fetch(req).then((res) => {
    if (res.ok) { const copy = res.clone(); caches.open(CACHE).then((c) => c.put(key, copy)); }
    return res;
  })).catch(() => caches.match(INDEX)));
  if (key === INDEX) e.waitUntil(checkAll().catch(() => {}));
});
self.addEventListener('message', (e) => { if (e.data && e.data.type === 'check') e.waitUntil(checkAll().catch(() => {})); });
