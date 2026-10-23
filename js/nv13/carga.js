(function (d) {
  /* v4 fase 13 · CARGA = DIBUJO DEL ALMUD. Sobre negro, el isotipo se dibuja de abajo hacia arriba según los bytes reales
     del video de portada (c-v en celular, c-h desde 768), el logo, los pósters de todos los videos y la primera foto de El lugar
     y de Tragos. Mínimo 3 s (el dibujo se suaviza), máximo 8 s (completa y entra; lo demás sigue en segundo plano).
     Las descargas quedan en la caché HTTP: el <video> y los <img> las reutilizan. Al 100 %: la boca se abre y el video
     parte desde 0 (antes, quieto en el cuadro 0: el letrero). Sin JS o con movimiento reducido: sin carga, video desde 0. */
  var r = d.documentElement, L = matchMedia('(min-width:768px)').matches;
  var v = d.querySelector(L ? '.hero__v--d video' : '.hero__v--m video');
  var rm = matchMedia('(prefers-reduced-motion: reduce)').matches;
  v.dataset.on = '1'; v.poster = v.dataset.poster; v.removeAttribute('autoplay'); v.autoplay = false;
  var webm = !!v.canPlayType && v.canPlayType('video/webm; codecs="vp9"') !== '';
  var url = webm ? v.dataset.webm : v.dataset.mp4;
  var H;
  function arranca() { try { v.currentTime = 0; } catch (e) {} var q = v.play(); if (q && q.catch) q.catch(function () {}); }
  function src() { if (v.dataset.src) return; v.dataset.src = '1'; v.preload = 'auto'; v.src = url; v.load(); if (H.quiere) arranca(); }
  // play desde 0; si el video aún no tiene fuente (red lenta: su descarga sigue), parte apenas llegue, también desde 0
  function play() { if (!v.dataset.src) { H.quiere = true; return; } arranca(); }
  H = window.__almudHero = { v: v, play: play, src: src, lista: false };
  if (rm || !r.classList.contains('intro')) { src(); play(); r.classList.remove('intro', 'carga'); return; }
  r.classList.add('carga');
  var man = {}; try { man = JSON.parse(d.getElementById('carga-man').textContent); } catch (e) {}
  var MIN = 3000, MAX = 8000, T0 = performance.now();
  var iso = null, pct = null;   // van después de este script en el HTML: se buscan en cada cuadro hasta encontrarlos
  var total = 0, loaded = 0, finished = false, shown = 0, videoOk = false, abre = false;
  var vb = (L ? man.h : man.v) || {}, vjob = { url: url, bytes: (webm ? vb.webm : vb.mp4) || 1, video: true };
  var otro = d.querySelector(L ? '.hero__v--m video' : '.hero__v--d video'), otroP = otro && otro.dataset.poster;
  var jobs = [vjob].concat((man.posters || []).filter(function (x) { return x.url !== otroP; }), man.logo ? [man.logo] : []);   // el póster de la otra portada no se baja
  var imgs = [d.querySelector('#lugar img[data-src]'), d.querySelector('#tragos .tragos__band img[data-src]')].filter(Boolean);
  jobs.forEach(function (j) { total += j.bytes; });
  var fb = man.fotos || []; imgs.forEach(function (i, k) { i._b = fb[k] || 60000; total += i._b; });
  function one(job) {
    var got = 0;
    function add(n) { var t = Math.max(0, Math.min(n, job.bytes - got)); got += t; loaded += t; }
    if (!window.fetch) { add(job.bytes); return Promise.resolve(); }
    return fetch(job.url, { cache: 'force-cache' }).then(function (res) {
      if (!res.ok) throw 0;
      if (!res.body || !res.body.getReader) return res.arrayBuffer().then(function () {});
      var rd = res.body.getReader();
      function pump() { return rd.read().then(function (x) { if (x.done) return; add(x.value.byteLength); return pump(); }); }
      return pump();
    }).then(function () { if (job.video) { videoOk = true; if (H.lista) src(); } }, function () { if (job.video && H.lista) src(); }).then(function () { add(job.bytes); });
  }
  function foto(img) {
    var b = img._b;
    return new Promise(function (res) {
      var ok = function () { loaded += b; res(); };
      [].forEach.call(img.parentElement.querySelectorAll('source[data-srcset]'), function (s) { s.srcset = s.dataset.srcset; s.removeAttribute('data-srcset'); });
      img.addEventListener('load', ok, { once: true }); img.addEventListener('error', ok, { once: true });
      img.src = img.dataset.src; img.removeAttribute('data-src');
    });
  }
  function worker(list) { var j = list.shift(); return j ? one(j).then(function () { return worker(list); }) : Promise.resolve(); }
  var cola = jobs.slice(1);
  Promise.all([one(vjob), worker(cola), worker(cola)].concat(imgs.map(foto))).then(function () { finished = true; });
  function fin() { finished = true; }
  setTimeout(fin, Math.max(0, MAX - performance.now()));   // tope contado desde que se pidió la página
  var MINe = Math.max(800, Math.min(MIN, MAX - T0 - 300));   // si el HTML llegó tarde, el recorrido mínimo se acorta para no pasar de 8 s
  H.saltar = fin;   // un scroll, un toque o una tecla durante la carga: completa el dibujo y entra
  ['wheel', 'touchmove', 'keydown'].forEach(function (ev) { addEventListener(ev, function f() { if (performance.now() - T0 > 400) { fin(); removeEventListener(ev, f); } }, { passive: true }); });
  function tick() {
    var now = performance.now();
    var target = finished ? 100 : (total ? Math.min(99, loaded / total * 100) : 0);
    target = Math.min(target, (now - T0) / MINe * 100);
    shown += (target - shown) * (finished ? .14 : .1);
    if (target - shown < .3) shown = target;
    if (!iso) iso = d.querySelector('.hero__iso'); if (!pct) pct = d.querySelector('[data-pct]');
    var n = Math.floor(shown);
    if (pct) pct.textContent = n;
    if (iso) iso.style.setProperty('--load', (shown / 100).toFixed(4));
    H.pct = n;
    if (shown >= 100 && finished) return listo();
    requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
  function listo() {
    var go = function () { if (abre) return; abre = true; H.lista = true; H.t100 = performance.now(); if (window.__almudOpen) window.__almudOpen(); else espera(0); };
    if (videoOk) { src(); if (v.readyState < 2) { v.addEventListener('loadeddata', go, { once: true }); setTimeout(go, 1200); } else go(); }
    else go();   // a los 8 s sin terminar: se entra con el cuadro 0 (póster = letrero); la descarga sigue y el video parte desde 0 al llegar, sin bajarse dos veces
  }
  function espera(k) {   // site.js todavía no llega: se espera un poco y, si no, la portada se abre sin animación
    if (window.__almudOpen) return window.__almudOpen();
    if (k > 15) { r.classList.remove('intro', 'carga'); play(); return; }
    setTimeout(function () { espera(k + 1); }, 100);
  }
})(document);
