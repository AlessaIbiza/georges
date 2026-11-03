// Univers Lilith : garde la page en mémoire pour l'ouvrir sans réseau. Les épisodes « gardés » sont dans le cache lilith-audio-v1.
const SHELL="vivant-shell-v2",FILES=["cover.jpg","./","index.html","icon-192.png","manifest.json"];
self.addEventListener("install",e=>{e.waitUntil(caches.open(SHELL).then(c=>c.addAll(FILES)));self.skipWaiting();});
self.addEventListener("activate",e=>e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(n=>n.startsWith("vivant-shell")&&n!==SHELL).map(n=>caches.delete(n)))).then(()=>self.clients.claim())));
self.addEventListener("fetch",e=>{const u=new URL(e.request.url);if(e.request.method!=="GET"||u.pathname.endsWith(".mp3"))return;
  e.respondWith(fetch(e.request).then(r=>{const c=r.clone();caches.open(SHELL).then(x=>x.put(e.request,c));return r;}).catch(()=>caches.match(e.request)));});
