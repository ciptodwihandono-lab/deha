// Peta Survei pindah ke /Peta-survey/. Service worker lama di /deha/peta/ diganti versi ini:
// tidak melayani apa pun, membersihkan entri cache lamanya, lalu melepas diri.
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', (e) => {
  e.waitUntil((async () => {
    const c = await caches.open('peta-survei');
    const scope = self.registration.scope;
    for (const req of await c.keys()) if (req.url.startsWith(scope)) await c.delete(req);
    await self.clients.claim();
    await self.registration.unregister();
    for (const client of await self.clients.matchAll({ type: 'window' })) client.navigate(client.url).catch(() => {});
  })());
});
