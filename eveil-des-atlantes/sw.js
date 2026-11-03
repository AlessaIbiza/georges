const SHELL="eveil-des-atlantes-shell-v1",FILES=["./","index.html","cover.jpg","fond.jpg","icon-192.png","manifest.json","../fonts/grandcentral.woff"];
self.addEventListener("install",e=>{e.waitUntil(caches.open(SHELL).then(c=>c.addAll(FILES)).catch(()=>{}));self.skipWaiting()});
self.addEventListener("activate",e=>e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(n=>n.endsWith("-shell-v0")).map(n=>caches.delete(n)))).then(()=>self.clients.claim())));
self.addEventListener("fetch",e=>{const u=new URL(e.request.url);if(e.request.method!=="GET"||/\.(mp3|m4a|mp4)$/.test(u.pathname))return;
 e.respondWith(fetch(e.request).then(r=>{const c=r.clone();caches.open(SHELL).then(x=>x.put(e.request,c));return r}).catch(()=>caches.match(e.request)))});
