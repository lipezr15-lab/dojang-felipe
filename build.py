"""Gera o site estatico (index.html + service worker) a partir de src/app.html.

src/app.html e a fonte unica. Ele e escrito no formato do Artifact do Claude
(sem doctype/html/head/body — o visualizador embrulha isso), entao aqui o
documento completo e montado em volta dele.

    python build.py

Depois: git add -A && git commit && git push  (o GitHub Pages publica sozinho)
"""
import hashlib
import io
import os

RAIZ = os.path.dirname(os.path.abspath(__file__))

CABECA = '''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="Treino de Taekwondo ATA Songahm do Felipe: formas, sparring, armas, chutes e diario.">
<meta name="theme-color" content="#EFF3F9" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0A101B" media="(prefers-color-scheme: dark)">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="Dojang">
<link rel="manifest" href="./manifest.webmanifest">
<link rel="apple-touch-icon" href="./apple-touch-icon.png">
<link rel="icon" href="./icon-192.png">
<style>
  :root{color-scheme:light dark}
  html,body{margin:0}
  img{max-width:100%}
  [hidden]{display:none!important}
</style>
'''

REGISTRO = '''
<script>
if('serviceWorker' in navigator){
  addEventListener('load', ()=>{ navigator.serviceWorker.register('./sw.js').catch(()=>{}); });
}
</script>
'''

SW = '''const CACHE = 'dojang-%s';
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
'''


def main():
    fonte = io.open(os.path.join(RAIZ, 'src', 'app.html'), encoding='utf-8').read()
    corte = fonte.index('</style>') + len('</style>')
    doc = CABECA + fonte[:corte] + '\n</head>\n<body>\n' + fonte[corte:] + REGISTRO + '\n</body>\n</html>\n'

    io.open(os.path.join(RAIZ, 'index.html'), 'w', encoding='utf-8').write(doc)
    versao = hashlib.sha1(doc.encode('utf-8')).hexdigest()[:10]
    io.open(os.path.join(RAIZ, 'sw.js'), 'w', encoding='utf-8').write(SW % versao)
    print('index.html %d bytes | cache dojang-%s' % (len(doc), versao))


if __name__ == '__main__':
    main()
