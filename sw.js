const CACHE = 'dojang-158bc04214';
const ARQUIVOS = ['./','./index.html','./manifest.webmanifest','./icon-192.png','./icon-512.png','./apple-touch-icon.png'];

self.addEventListener('install', e=>{
  e.waitUntil(caches.open(CACHE).then(c=>c.addAll(ARQUIVOS)).then(()=>self.skipWaiting()));
});
self.addEventListener('activate', e=>{
  e.waitUntil(caches.keys().then(ks=>Promise.all(
    ks.filter(k=>k!==CACHE).map(k=>caches.delete(k))
  )).then(()=>self.clients.claim()));
});
self.addEventListener('fetch', e=>{
  const r = e.request;
  if(r.method!=='GET') return;
  const url = new URL(r.url);
  if(url.origin!==location.origin) return;            // fontes e YouTube passam direto
  if(r.mode==='navigate'){                            // pagina: rede primeiro, cache se offline
    e.respondWith(fetch(r).then(res=>{
      const c = res.clone(); caches.open(CACHE).then(k=>k.put('./index.html', c)); return res;
    }).catch(()=>caches.match('./index.html')));
    return;
  }
  e.respondWith(caches.match(r).then(hit=>hit||fetch(r).then(res=>{
    if(res.ok){ const c=res.clone(); caches.open(CACHE).then(k=>k.put(r,c)); }
    return res;
  }).catch(()=>hit||new Response('',{status:504}))));
});
