// Georges : service worker minimal (rend Georges installable sur Android).
// Il ne met rien en cache : tout vient toujours du réseau, pour que les mises à jour arrivent tout de suite.
self.addEventListener('install',()=>self.skipWaiting());
self.addEventListener('activate',e=>e.waitUntil(self.clients.claim()));
self.addEventListener('fetch',()=>{});
