// Service worker de /app/: hace que la web se pueda instalar como app
// (iPhone, PC; en Android el manifest prefiere la app de Play) y que abra
// aunque no haya conexion.
//
// A proposito no guarda casi nada: la pagina va siempre primero a la red (asi
// cada deploy se ve al instante) y la copia guardada solo se usa sin
// conexion. La API esta en otro dominio y no pasa por aca.
const CACHE = 'playloggr-app-v1';
const SHELL = ['/app/', '/app/manifest.webmanifest', '/app/icons/icon-192.png', '/favicon.svg'];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;

  // La app en si (/app/ con cualquier query o #): red primero, copia de respaldo.
  const isApp = req.mode === 'navigate' && (url.pathname === '/app/' || url.pathname === '/app/index.html');
  if (isApp) {
    e.respondWith(
      fetch(req)
        .then((res) => {
          if (res.ok) {
            const copy = res.clone();
            caches.open(CACHE).then((c) => c.put('/app/', copy));
          }
          return res;
        })
        .catch(() => caches.match('/app/'))
    );
    return;
  }

  // Lo que esta en SHELL: red primero y, sin conexion, la copia.
  if (SHELL.includes(url.pathname)) {
    e.respondWith(fetch(req).catch(() => caches.match(url.pathname)));
  }
});
