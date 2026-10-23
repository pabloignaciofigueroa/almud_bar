(function (d) {
  /* v4 fase 13 · CARGA = DIBUJO DEL ALMUD. Sobre negro, el isotipo se dibuja de abajo hacia arriba según lo que hace falta
     para ARRANCAR: los primeros ~3 s del video de portada (c-v en celular, c-h-l desde 768) o su canplaythrough, el logo,
     los pósters de los videos y la primera foto de El lugar y de Tragos. El video se baja solo (una sola descarga, la del
     <video>), primero que todo; lo demás espera a que el video tenga sus 3 s. Mínimo 3 s (dibujo suavizado), tope 8 s desde que
     se pidió la página. Al 100 %: la boca se abre y el video parte desde 0 (v15: antes de eso, oculto; se ve solo por la boca); si aún
     no puede arrancar, la boca espera abierta y parte en cuanto pueda. Sin JS o con movimiento reducido: sin carga, video desde 0. */
  var r = d.documentElement, L = matchMedia('(min-width:768px)').matches;
  var v = d.querySelector(L ? '.hero__v--d video' : '.hero__v--m video');
  var rm = matchMedia('(prefers-reduced-motion: reduce)').matches;
  v.dataset.on = '1'; v.poster = v.dataset.poster; v.removeAttribute('autoplay'); v.autoplay = false;
  var webm = !!v.canPlayType && v.canPlayType('video/webm; codecs="vp9"') !== '';
  var url = webm ? v.dataset.webm : v.dataset.mp4;
  var H, ARR = 3;   // segundos de video que bastan para arrancar
  function src() { if (v.dataset.src) return; v.dataset.src = '1'; v.preload = 'auto'; v.src = url; v.load(); }
  function arranca() { try { v.currentTime = 0; } catch (e) {} var q = v.play(); if (q && q.catch) q.catch(function () {}); }
  // play desde 0 apenas el video pueda arrancar (readyState ≥ 3); si todavía no, en su primer canplay
  function play() {
    src();
    if (v.readyState >= 3) return arranca();
    H.quiere = true;
    var f = function () { if (!H.quiere) return; H.quiere = false; arranca(); };
    v.addEventListener('canplay', f, { once: true });
  }
  H = window.__almudHero = { v: v, play: play, src: src, lista: false };
  if (rm || !r.classList.contains('intro')) { src(); play(); r.classList.remove('intro', 'carga'); return; }
  r.classList.add('carga');
  src();   // el video parte primero; su descarga es la misma que va a reproducir
  var man = {}; try { man = JSON.parse(d.getElementById('carga-man').textContent); } catch (e) {}
  var MIN = 3000, MAX = 7600, T0 = performance.now();   // 7,6 s + salto final de ≤0,35 s: el 100 % llega antes de los 8 s
  var iso = null, pct = null;   // van después de este script en el HTML: se buscan en cada cuadro hasta encontrarlos
  var finished = false, shown = 0, abre = false, extrasOn = false;
  var vb = (L ? man.h : man.v) || {}, vbytes = (webm ? vb.webm : vb.mp4) || 1e6, vdur = vb.dur || 17;
  var VW = Math.max(150000, vbytes * ARR / vdur);   // peso de «lo que hace falta para arrancar»
  var otro = d.querySelector(L ? '.hero__v--m video' : '.hero__v--d video'), otroP = otro && otro.dataset.poster;
  var jobs = (man.posters || []).filter(function (x) { return x.url !== otroP && x.url !== v.dataset.poster; }).concat(man.logo ? [man.logo] : []);   // el póster de la otra portada no se baja
  var imgs = [d.querySelector('#lugar img[data-src]'), d.querySelector('#tragos .tragos__band img[data-src]')].filter(Boolean);
  var fb = man.fotos || [], total = VW, loaded = 0;
  jobs.forEach(function (j) { total += j.bytes; });
  imgs.forEach(function (i, k) { i._b = fb[k] || 60000; total += i._b; });
  function vfrac() {   // cuánto de «arrancar» tiene el video: búfer desde 0 hasta 3 s, o canplaythrough
    if (v.readyState >= 4) return 1;
    var e = 0; try { if (v.buffered.length && v.buffered.start(0) < .2) e = v.buffered.end(0); } catch (x) {}
    return Math.min(1, e / ARR);
  }
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
    }).catch(function () {}).then(function () { add(job.bytes); });
  }
  function foto(img) {
    return new Promise(function (res) {
      var ok = function () { loaded += img._b; res(); };
      [].forEach.call(img.parentElement.querySelectorAll('source[data-srcset]'), function (s) { s.srcset = s.dataset.srcset; s.removeAttribute('data-srcset'); });
      img.addEventListener('load', ok, { once: true }); img.addEventListener('error', ok, { once: true });
      img.src = img.dataset.src; img.removeAttribute('data-src');
    });
  }
  function worker(list) { var j = list.shift(); return j ? one(j).then(function () { return worker(list); }) : Promise.resolve(); }
  var extrasDone = false;
  function extras() {   // pósters, logo y fotos: después de que el video tiene con qué arrancar (o a los 2,5 s, para no quedar en cero)
    if (extrasOn) return; extrasOn = true;
    var cola = jobs.slice();
    Promise.all([worker(cola), worker(cola)].concat(imgs.map(foto))).then(function () { extrasDone = true; });
  }
  setTimeout(extras, 2500);
  var tFin = 0, sFin = 0;
  function fin() { if (finished) return; finished = true; tFin = performance.now(); sFin = shown; }
  setTimeout(fin, Math.max(0, MAX - performance.now()));   // tope contado desde que se pidió la página
  var MINe = Math.max(800, Math.min(MIN, MAX - T0 - 300));   // si el HTML llegó tarde, el recorrido mínimo se acorta
  H.saltar = fin;   // un scroll o una tecla durante la carga: completa el dibujo y entra
  ['wheel', 'touchmove', 'keydown'].forEach(function (ev) { addEventListener(ev, function f() { if (performance.now() - T0 > 400) { fin(); removeEventListener(ev, f); } }, { passive: true }); });
  function tick() {
    var now = performance.now(), vf = vfrac();
    if (vf >= 1) extras();
    if (vf >= 1 && extrasDone) fin();
    if (finished) {   // v4 fase 14: al terminar (o al tope) el % sube a 100 en ≤0,35 s, por tiempo: nunca queda asintótico
      var k = Math.min(1, (now - tFin) / 350, (now - T0) / MINe);
      shown = Math.max(shown, sFin + (100 - sFin) * (1 - Math.pow(1 - k, 2)));
      if (k >= 1) shown = 100;
    } else {
      var target = Math.min(99, (vf * VW + loaded) / total * 100, (now - T0) / MINe * 100);
      shown += (target - shown) * .1;
      if (target - shown < .3) shown = target;
    }
    if (!iso) iso = d.querySelector('.hero__iso'); if (!pct) pct = d.querySelector('[data-pct]');
    var n = Math.floor(shown);
    if (pct) pct.textContent = n;
    if (iso) iso.style.setProperty('--load', (shown / 100).toFixed(4));
    H.pct = n;
    last = now;
    if (shown >= 100 && finished) { clearInterval(iv); return listo(); }
    if (!raf) { raf = true; requestAnimationFrame(function () { raf = false; tick(); }); }
  }
  // v4 fase 14: el dibujo va con rAF, pero un reloj real (setInterval) lo sigue moviendo si rAF se frena,
  // y un setTimeout fuerza el 100 % y la apertura a los 8 s pase lo que pase
  var last = 0, raf = false;
  var iv = setInterval(function () { if (performance.now() - last > 80) tick(); }, 50);
  setTimeout(function () { fin(); shown = 100; tick(); listo(); }, Math.max(0, 8000 - performance.now()));
  tick();
  function listo() {
    clearInterval(iv);
    if (abre) return; abre = true; H.lista = true; H.t100 = performance.now();
    if (window.__almudOpen) window.__almudOpen(); else espera(0);
  }
  function espera(k) {   // site.js todavía no llega: se espera un poco y, si no, la portada se abre sin animación
    if (window.__almudOpen) return window.__almudOpen();
    if (k > 15) { r.classList.remove('intro', 'carga'); play(); return; }
    setTimeout(function () { espera(k + 1); }, 100);
  }
})(document);
