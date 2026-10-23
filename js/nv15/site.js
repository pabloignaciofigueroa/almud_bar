/* Almud Bar · v3
   Videos: autoplay muted loop playsinline. El JS SOLO les pone el póster y la fuente: la portada
   (por orientación) ya la conectó el script en línea del HTML; el resto se conecta una sola vez cuando
   está a ≤0,15 pantallas (primer pantallazo ≤1,5 MB) (IntersectionObserver SOLO para cargar). Una vez cargado, nunca se pausa ni se toca.
   Con movimiento reducido: solo póster. */
(() => {
  'use strict';
  const d = document, root = d.documentElement;
  const $ = (s, c = d) => c.querySelector(s);
  const $$ = (s, c = d) => [...c.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ───────── Videos: solo poner póster y fuente ───────── */
  function attach(v) {
    if (!v || v.dataset.on) return;
    v.dataset.on = '1';
    if (v.dataset.poster) v.poster = v.dataset.poster;
    if (reduce) { v.removeAttribute('autoplay'); return; }
    v.preload = 'auto';
    v.insertAdjacentHTML('beforeend',
      '<source src="' + v.dataset.webm + '" type="video/webm"><source src="' + v.dataset.mp4 + '" type="video/mp4">');
    v.load();
    const p = v.play(); if (p && p.catch) p.catch(() => {});
  }
  window.__almudAttach = attach;
  const land = matchMedia('(min-width:768px)');
  const heroVisible = () => $(land.matches ? '.hero__v--d video' : '.hero__v--m video');
  attach(heroVisible());
  land.addEventListener('change', () => attach(heroVisible()));
  const lazy = $$('video.v:not([data-hero])');
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { io.unobserve(e.target); attach(e.target); } }),
      { rootMargin: '0px 0px 15% 0px' });
    lazy.forEach(v => io.observe(v));
  } else lazy.forEach(attach);
  /* v4 fase 13 · carga anticipada: con una sección a la vista, los videos de la SIGUIENTE se conectan en silencio
     (póster, fuente y play muteado), así al llegar ya están corriendo. Arranca cuando termina la carga del almud. */
  function anticipar() {
    if (!('IntersectionObserver' in window)) return;
    const secs = $$('main > section');
    const io3 = new IntersectionObserver(es => es.forEach(e => {
      if (!e.isIntersecting) return;
      io3.unobserve(e.target);
      const nx = secs[secs.indexOf(e.target) + 1];
      if (nx) $$('video.v:not([data-hero])', nx).forEach(attach);
    }), { threshold: 0.01 });
    secs.forEach(x => io3.observe(x));
  }
  if (root.classList.contains('carga')) window.__almudAnticipar = anticipar; else anticipar();

  /* ───────── Fotos diferidas (v4 fase 2): srcset/src en data-*; se asignan a ≤0,5 pantallas ───────── */
  function loadImg(img) {
    if (!img.dataset.src) return;
    $$('source[data-srcset]', img.parentElement).forEach(s => { s.srcset = s.dataset.srcset; s.removeAttribute('data-srcset'); });
    img.src = img.dataset.src; img.removeAttribute('data-src');
  }
  const lazyImgs = $$('img[data-src]');
  if ('IntersectionObserver' in window) {
    const io2 = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { io2.unobserve(e.target); loadImg(e.target); } }),
      { rootMargin: '0px 50% 50% 50%' });
    lazyImgs.forEach(i => io2.observe(i));
  } else lazyImgs.forEach(loadImg);

  /* ───────── Idioma (ES por defecto; EN solo si el usuario lo toca) ───────── */
  const ATTR = [['data-alt-en', 'alt'], ['data-aria-en', 'aria-label'], ['data-title-en', 'title']];   // v4 fase 9 (M2): el title del iframe del mapa también
  function setLang(lang, save) {
    root.lang = lang;
    $$('[data-en]').forEach(el => {
      if (el.tagName === 'META') { if (!el.dataset.es) el.dataset.es = el.content; el.content = lang === 'en' ? el.dataset.en : el.dataset.es; return; }
      if (el.dataset.es === undefined) el.dataset.es = el.textContent;
      el.textContent = lang === 'en' ? el.dataset.en : el.dataset.es;
    });
    ATTR.forEach(([src, a]) => $$('[' + src + ']').forEach(el => {
      const k = 'es' + a.replace('-', '');
      if (el.dataset[k] === undefined) el.dataset[k] = el.getAttribute(a) || '';
      el.setAttribute(a, lang === 'en' ? el.getAttribute(src) : el.dataset[k]);
    }));
    if (save) { try { localStorage.setItem('almud-idioma', lang); } catch (e) {} }
    if (window.ScrollTrigger) ScrollTrigger.refresh();
  }
  if (root.lang === 'en') setLang('en', false);
  $('[data-lang]').addEventListener('click', () => setLang(root.lang === 'en' ? 'es' : 'en', true));

  /* ───────── Nav: aparece al dejar la portada ───────── */
  const hero = $('.hero');
  const navLogo = $('.nav__logo');
  const navState = () => {
    const past = scrollY > hero.offsetHeight - 170;
    root.classList.toggle('is-past', past);
    // v4 fase 9 (I2): mientras el logo de la barra es invisible (en la portada) no recibe foco
    if (navLogo) { navLogo.tabIndex = past ? 0 : -1; navLogo.setAttribute('aria-hidden', past ? 'false' : 'true'); }
  };
  addEventListener('scroll', navState, { passive: true }); navState();

  /* ───────── La ruleta de rincones (v4 fase 4) ─────────
     Se arrastra con el dedo o el mouse (pointer events propios), con inercia y encaje en cada foto.
     touch-action: pan-y → el scroll vertical sigue siendo del navegador: la ruleta nunca lo secuestra ni lo escucha.
     Cada foto se inclina según la velocidad y vuelve a su sitio. Solo transform. Con movimiento reducido: arrastre sin inclinación ni giro de entrada. */
  function ruleta(vp) {   // v4 fase 5: la misma lógica sirve a la ruleta de rincones y al carrusel de tragos
    const tr = vp && $('[data-track]', vp);
    if (!vp || !tr || !window.PointerEvent) return;
    root.classList.add('rul');
    const items = [...tr.children];
    let moved = false;
    vp.setAttribute('role', 'region'); vp.tabIndex = 0;
    let x = 0, target = 0, min = 0, tilt = 0, vel = 0, raf = 0, drag = null, touched = false, last = 0;
    const gut = () => parseFloat(getComputedStyle(tr).paddingLeft) || 0;
    const stops = () => items.map(li => Math.max(min, -(li.offsetLeft - gut())));
    function measure() {
      const lastLi = items[items.length - 1];
      min = Math.min(0, vp.clientWidth - (lastLi.offsetLeft + lastLi.offsetWidth + gut()));
      target = Math.max(min, Math.min(0, target));
      kick();
    }
    const rubber = v => v > 0 ? v * .35 : v < min ? min + (v - min) * .35 : v;
    function snap(proj) {
      let best = 0, d = Infinity;
      stops().forEach(s => { const k = Math.abs(s - proj); if (k < d) { d = k; best = s; } });
      return best;
    }
    function frame(t) {
      const dt = Math.min(64, last ? t - last : 16.7); last = t;
      const prev = x;
      if (!drag) x += (target - x) * (1 - Math.pow(1 - .11, dt / 16.7));
      vel = (x - prev) / (dt / 16.7) * .6 + vel * .4;
      const tt = reduce ? 0 : Math.max(-9, Math.min(9, vel * .42));
      tilt += (tt - tilt) * (1 - Math.pow(1 - .16, dt / 16.7));
      tr.style.transform = 'translate3d(' + x.toFixed(2) + 'px,0,0)';
      items.forEach((li, i) => { li.style.transform = Math.abs(tilt) < .02 ? '' : 'rotate(' + (tilt * (1 + (i % 3) * .18)).toFixed(3) + 'deg)'; });
      if (drag || Math.abs(target - x) > .25 || Math.abs(tilt) > .02) raf = requestAnimationFrame(frame);
      else { x = target; tr.style.transform = 'translate3d(' + x + 'px,0,0)'; raf = 0; last = 0; }
    }
    function kick() { if (!raf) raf = requestAnimationFrame(frame); }
    // cargar sus fotos antes de que el visitante llegue (son 6: así no aparecen grises al arrastrar)
    const loadAll = () => $$('img[data-src]', tr).forEach(loadImg);
    vp.addEventListener('pointerdown', e => {
      if (e.button > 0) return;
      touched = true;
      moved = false;
      // la captura se toma recién al moverse 6 px: un clic quieto sigue abriendo el enlace de la tarjeta
      drag = { id: e.pointerId, x0: e.clientX, y0: e.clientY, s0: x, t: e.timeStamp, lx: e.clientX, v: 0, on: false };
      loadAll(); kick();
    });
    vp.addEventListener('pointermove', e => {
      if (!drag || e.pointerId !== drag.id) return;
      const dx = e.clientX - drag.x0;
      if (!drag.on) {               // en táctil: solo si el gesto es horizontal (si es vertical, el navegador ya hizo scroll y canceló)
        if (Math.abs(dx) < 6) return;
        drag.on = true; moved = true; try { vp.setPointerCapture(e.pointerId); } catch (_) {}
        vp.classList.add('is-drag');
      }
      const dtm = Math.max(1, e.timeStamp - drag.t);
      drag.v = (e.clientX - drag.lx) / dtm * .7 + drag.v * .3; drag.lx = e.clientX; drag.t = e.timeStamp;
      x = rubber(drag.s0 + dx); target = x; kick();
    });
    const end = e => {
      if (!drag || e.pointerId !== drag.id) return;
      const v = drag.on && e.type === 'pointerup' ? drag.v : 0;   // px/ms
      drag = null; vp.classList.remove('is-drag');
      target = snap(x + v * (reduce ? 120 : 340)); kick();
    };
    vp.addEventListener('pointerup', end); vp.addEventListener('pointercancel', end);
    vp.addEventListener('lostpointercapture', e => { if (e.target === vp) end(e); });   // la captura implícita del li (táctil) también burbujea: se ignora
    vp.addEventListener('dragstart', e => e.preventDefault());
    vp.addEventListener('click', e => { if (moved) { e.preventDefault(); e.stopPropagation(); moved = false; } }, true);   // un arrastre no es un clic
    vp.addEventListener('focusin', e => {   // con teclado (Tab) la tarjeta enfocada entra en pantalla
      const li = items.find(l => l.contains(e.target)); if (!li) return;
      vp.scrollLeft = 0; target = Math.max(min, Math.min(0, -(li.offsetLeft - gut()))); kick();
    });
    // trackpad con gesto horizontal: solo deltaX; el vertical nunca se toca
    let wheelT = 0;
    vp.addEventListener('wheel', e => {
      if (Math.abs(e.deltaX) <= Math.abs(e.deltaY) * 1.2) return;
      e.preventDefault(); touched = true; loadAll();
      x = Math.max(min - 60, Math.min(60, x - e.deltaX)); target = x; kick();
      clearTimeout(wheelT); wheelT = setTimeout(() => { target = snap(x); kick(); }, 140);
    }, { passive: false });
    vp.addEventListener('keydown', e => {
      if (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return;
      e.preventDefault(); touched = true; loadAll();
      const st = stops(); let i = st.indexOf(snap(target));
      i = Math.max(0, Math.min(st.length - 1, i + (e.key === 'ArrowRight' ? 1 : -1)));
      target = st[i]; kick();
    });
    addEventListener('resize', measure);
    measure();
    if ('IntersectionObserver' in window) {
      // al acercarse: se cargan sus fotos; al entrar, la ruleta gira sola una vez (un giro de entrada, no atado al scroll)
      const io = new IntersectionObserver(es => es.forEach(e => {
        if (!e.isIntersecting) return;
        if (e.intersectionRatio === 0 || e.boundingClientRect.top > innerHeight) { loadAll(); return; }
        io.disconnect(); loadAll();
        if (reduce || touched) return;
        x = Math.max(min, -vp.clientWidth * .9); target = 0; kick();
      }), { rootMargin: '0px 0px 60% 0px', threshold: [0, .35] });
      io.observe(vp);
    } else loadAll();
  }
  $$('[data-ruleta]').forEach(ruleta);

  /* ───────── Movimiento ───────── */
  const G = window.gsap, ST = window.ScrollTrigger;
  if (!G || !ST || reduce) {
    // sin GSAP: la carga del almud igual termina y la portada se abre sin animación (video desde 0)
    window.__almudOpen = () => { root.classList.remove('intro', 'carga'); if (window.__almudHero) window.__almudHero.play(); if (window.__almudAnticipar) window.__almudAnticipar(); };
    if (!root.classList.contains('carga')) root.classList.remove('intro'); else if (window.__almudHero && window.__almudHero.lista) window.__almudOpen();
    return;
  }
  G.registerPlugin(ST);
  root.classList.add('gs');
  const EXPO = 'expo.out';

  // Lenis (rueda/trackpad); en táctil, scroll nativo.
  if (window.Lenis && matchMedia('(hover:hover) and (pointer:fine)').matches) {
    const lenis = new Lenis({ duration: 1.05, easing: t => Math.min(1, 1.001 - Math.pow(2, -10 * t)) });
    lenis.on('scroll', ST.update);
    G.ticker.add(t => lenis.raf(t * 1000));
    G.ticker.lagSmoothing(0);
    window.__lenis = lenis;
    $$('a[href^="#"]').forEach(a => a.addEventListener('click', e => {
      const t = $(a.getAttribute('href')); if (!t) return; e.preventDefault(); lenis.scrollTo(t, { duration: 1.2 });
    }));
  }

  // Titulares: palabras con máscara
  $$('.ttl__t').forEach(el => {
    el.innerHTML = el.textContent.trim().split(/\s+/).map(w => {
      // v4 fase 4: su juego de palabras: «colorssss» (25 veces en sus captions, IG-111): cada s es suya
      const m = /^(.*?[^s])(s{3,})(\W*)$/i.exec(w);
      if (m) w = m[1] + [...m[2]].map(c => '<span class="ss">' + c + '</span>').join('') + (m[3] ? '<span class="ss ss--b">' + m[3] + '</span>' : '');
      return '<span class="w"><span class="w__i">' + w + '</span></span>';
    }).join(' ');
  });
  const words = el => $$('.w__i', el);

  /* Momento memorable (v4 fase 4): el almud se dibuja sobre el video (el póster ya se ve: no frena el LCP),
     crece por su boca hasta abrir la pantalla, y ALMUD BAR y la frase entran letra por letra; «Ver la carta» rebota.
     ≤2,5 s en total; un scroll, un toque o una tecla la terminan al tiro. */
  function splitChars(el) {
    const txt = el.textContent.trim();
    el.innerHTML = '<span class="sr-only">' + txt.replace(/&/g, '&amp;').replace(/</g, '&lt;') + '</span><span aria-hidden="true">' +
      txt.split(' ').map(w => '<span class="chw">' + [...w].map(c => '<span class="ch">' + c.replace('&', '&amp;') + '</span>').join('') + '</span>').join(' ') + '</span>';
    return $$('.ch', el);
  }
  // v4 fase 15: polígono convexo con cada lado corrido dd unidades hacia ADENTRO (vértice = cruce de los lados vecinos)
  function inset(p, dd) {
    const n = p.length, cx = p.reduce((t, q) => t + q[0], 0) / n, cy = p.reduce((t, q) => t + q[1], 0) / n;
    const Ls = p.map((a, i) => {
      const b = p[(i + 1) % n]; let nx = b[1] - a[1], ny = a[0] - b[0]; const l = Math.hypot(nx, ny); nx /= l; ny /= l;
      if (nx * (cx - a[0]) + ny * (cy - a[1]) < 0) { nx = -nx; ny = -ny; }
      return [nx, ny, nx * a[0] + ny * a[1] + dd];
    });
    return p.map((_, i) => {
      const [a1, b1, c1] = Ls[(i + n - 1) % n], [a2, b2, c2] = Ls[i], det = a1 * b2 - a2 * b1;
      return [(c1 * b2 - c2 * b1) / det, (a1 * c2 - a2 * c1) / det];
    });
  }
  function intro() {
    // corrección del cliente (fase 4): se entra en NEGRO; el almud se dibuja, su BOCA se abre y por ahí aparece el video
    // v4 fase 15 (revisión): la ventana del video ES la boca del isotipo, pegada a él: mismo centro, misma escala, mismo cuadro.
    // Antes (v14) la ventana se estiraba a pantalla completa por su cuenta (expo.inOut desde 0,6 s) mientras el isotipo
    // casi no crecía (expo.in, origen 50% 28%): a 0,85 s ya había video fuera de la boca y a 1,15 s cubría la pantalla
    // con el isotipo todavía en primer plano (escala 1,2, opacidad 0,95). Ahora el video solo se ve dentro del rombo de la boca,
    // que crece con el isotipo hasta pasar la cámara; recién cuando la boca contiene toda la pantalla el isotipo se apaga.
    const win = $('[data-win]'), iso = $('.hero__iso'), svg = $('svg', iso);
    G.set(iso, { xPercent: -50, yPercent: -50, x: 0, y: 0, scale: 1, opacity: 1 });
    const hr = hero.getBoundingClientRect(), r = svg.getBoundingClientRect(), ir = iso.getBoundingClientRect();
    const W = hero.offsetWidth, H = hero.offsetHeight;
    const P = q => [r.left - hr.left + (q[0] + 20) / 660 * r.width, r.top - hr.top + (q[1] + 20) / 940 * r.height];
    // boca: rombo interior del isotipo, en el borde INTERNO de su trazo (eje − 13 u. de las 26 del trazo; 1,5 u. queda bajo el trazo)
    const mouth = inset([[287, 76], [512, 217], [271, 409], [87, 192]], 11.5).map(P);
    const c = [mouth.reduce((t, q) => t + q[0], 0) / 4, mouth.reduce((t, q) => t + q[1], 0) / 4];   // centro de la boca
    // escala a la que la boca (escalada desde c) contiene toda la pantalla
    let cover = 1;
    mouth.forEach((a, i) => {
      const b = mouth[(i + 1) % 4]; let nx = b[1] - a[1], ny = a[0] - b[0]; const l = Math.hypot(nx, ny); nx /= l; ny /= l;
      let m = nx * (c[0] - a[0]) + ny * (c[1] - a[1]); if (m < 0) { nx = -nx; ny = -ny; m = -m; }
      [[-2, -2], [W + 2, -2], [W + 2, H + 2], [-2, H + 2]].forEach(X => {
        const dn = nx * (X[0] - c[0]) + ny * (X[1] - c[1]); if (dn < 0) cover = Math.max(cover, -dn / m);
      });
    });
    const S1 = cover * 1.25;   // escala final del isotipo: ya pasó la cámara
    // el isotipo escala desde el centro de su boca (su origen en px dentro de su propia caja)
    G.set(iso, { transformOrigin: (c[0] - (ir.left - hr.left)).toFixed(2) + 'px ' + (c[1] - (ir.top - hr.top)).toFixed(2) + 'px' });
    const st = { k: 0, p: 0 };
    const draw = () => {
      const s = Math.exp(st.p * Math.log(S1)), f = st.k * s;   // s: escala del isotipo (zoom a ritmo constante); f: de la boca
      win.style.clipPath = 'polygon(' + mouth.map(q => (c[0] + (q[0] - c[0]) * f).toFixed(1) + 'px ' + (c[1] + (q[1] - c[1]) * f).toFixed(1) + 'px').join(',') + ')';
      // el isotipo sigue opaco mientras la boca no contiene la pantalla; después (sus trazos ya fuera de cuadro) se apaga
      G.set(iso, { scale: s, opacity: s <= cover ? 1 : Math.max(0, 1 - (s - cover) / (S1 - cover)) });
    };
    draw();
    const ltrs = $$('.hero__svg .ltr');
    const chars = splitChars($('.hero__claim-t'));
    const gloss = $('.hero__claim .gloss');
    const btn = $('.hero__btns .btn');
    const logoIso = $('.hero__svg g g');   // el almudcito del logo: aterriza después de las letras
    const inEls = $$('.hero__in > *');
    const done = () => {
      win.style.clipPath = '';
      root.classList.remove('intro');
      G.set([...inEls, iso, '.nav', ...ltrs, ...chars, btn, logoIso].filter(Boolean), { clearProps: 'transform,opacity' });
      ['wheel', 'touchstart', 'pointerdown', 'keydown'].forEach(ev => removeEventListener(ev, skip));
      removeEventListener('scroll', skip);
      if (window.__almudAnticipar) window.__almudAnticipar();
    };
    // v4 fase 13: el almud ya lo dibujó la carga (de abajo hacia arriba, según los bytes); aquí parte en la BOCA.
    const tl = G.timeline({ paused: true, onComplete: done });
    G.set($$('.iso__g path', iso), { strokeDashoffset: 0 });
    // v4 fase 15: play desde 0 (cuadro 0 = el letrero) en el mismo instante en que la boca empieza a abrirse; antes de eso el
    // video está OCULTO (ventana de área cero y, durante la carga, visibility:hidden), no solo pausado.
    // La boca se abre (0,65 s) y luego el isotipo y su boca crecen juntos hasta pasar la cámara (0,6 → 1,55 s).
    const H0 = window.__almudHero, EXP = .6 + .95, D = .45;   // D: las letras y el botón entran un poco después (misma animación)
    tl.set(inEls, { opacity: 1 }, 0)
      .call(() => { root.classList.remove('carga'); root.classList.add('abre'); if (H0) { H0.tAbre = performance.now(); H0.ctAbre = H0.v.currentTime; H0.play(); } }, null, 0)
      .to(st, { k: 1, duration: .65, ease: 'power2.inOut', onUpdate: draw, onComplete: () => { if (H0) { H0.tRombo = performance.now(); H0.ctRombo = H0.v.currentTime; } } }, 0)   // la boca se abre
      .to(st, { p: 1, duration: .95, ease: 'power2.in', onUpdate: draw }, .6)              // isotipo y boca crecen juntos hasta pasar la cámara
      .call(() => { if (H0) { H0.tExp = performance.now(); H0.ctExp = H0.v.currentTime; } }, null, EXP)
      .from(ltrs, { y: 380, opacity: 0, rotation: i => (i % 2 ? 1 : -1) * (8 + i * 1.5), duration: .7, ease: 'back.out(2.4)', stagger: .055 }, 1.08 + D)
      .from(chars, { yPercent: 115, opacity: 0, rotation: i => (i % 3 - 1) * 14, duration: .42, ease: 'back.out(3)', stagger: .011 }, 1.28 + D)
      .fromTo(btn, { scale: .35, opacity: 0, rotation: -7 }, { scale: 1, opacity: 1, rotation: 0, duration: .6, ease: 'elastic.out(1.1,.45)' }, 1.83 + D)
      .fromTo('.nav', { opacity: 0 }, { opacity: 1, duration: .5 }, 1.53 + D);
    if (gloss) tl.from(gloss, { opacity: 0, duration: .4 }, 1.83 + D);
    if (logoIso) tl.from(logoIso, { scale: 0, rotation: -28, opacity: 0, transformOrigin: '50% 50%', duration: .7, ease: 'back.out(2.6)' }, 1.53 + D);
    function skip() { if (tl.progress() < 1) tl.progress(1); }
    window.__almudIntroTL = tl;
    window.__almudOpen = () => {
      if (tl.progress() > 0) return;
      tl.play(0);
      ['wheel', 'touchstart', 'pointerdown', 'keydown'].forEach(ev => addEventListener(ev, skip, { passive: true }));
      setTimeout(() => addEventListener('scroll', skip, { passive: true }), 60);   // un scroll real también la termina
    };
    if (window.__almudHero && window.__almudHero.lista) window.__almudOpen();
  }
  // v4 fase 13: la portada la abre la carga del almud (js en línea del hero) cuando llega al 100 %
  if (root.classList.contains('intro') && root.classList.contains('carga')) { window.__almudIntro = true; intro(); }
  else { root.classList.remove('intro'); }

  // Revelados de titulares
  $$('.ttl, .pie__f').filter(t => !t.closest('.quien') && !t.closest('.eventos')).forEach(t => {
    G.from(words(t), { yPercent: 110, duration: 1.05, ease: EXPO, stagger: .045,
      scrollTrigger: { trigger: t, start: 'top 88%', once: true },
      onComplete: () => { $$('.w', t).forEach(w => { w.style.overflow = 'visible'; }); if (t._in) t._in(); } });
  });

  /* «colorssss!»: las s se estiran y rebotan al entrar en pantalla y cada vez que pasa el dedo o el mouse */
  $$('.ttl').forEach(t => {
    const ss = $$('.ss:not(.ss--b)', t), bang = $('.ss--b', t);
    if (!ss.length) return;
    let busy = false, ready = false;
    const hiss = () => {
      if (busy || !ready) return; busy = true;
      // v4 fase 9: se estiran solo a lo ancho (sssssss…), nunca hacia arriba: ninguna letra pisa la línea de «GUSTA».
      // Se separan de derecha a izquierda y vuelven de izquierda a derecha, sin pasarse: nunca se montan entre ellas.
      const fs = parseFloat(getComputedStyle(t).fontSize) || 44, dx = fs * .2;
      const tl = G.timeline({ onComplete: () => { busy = false; G.set([...ss, bang].filter(Boolean), { clearProps: 'transform' }); } });
      G.set(ss, { transformOrigin: '50% 100%' });
      tl
        .to(ss, { scaleX: 1.4, scaleY: .94, x: i => (i + 1) * dx, duration: .24, ease: 'power2.out', stagger: { each: .04, from: 'end' } })
        .to(ss, { x: 0, duration: .75, ease: 'power3.out', stagger: .06 }, .42)
        .to(ss, { scaleX: 1, scaleY: 1, duration: .75, ease: 'back.out(2.5)', stagger: .06 }, .42);
      if (bang) tl.to(bang, { x: (ss.length + 1) * dx, rotation: 14, duration: .24, ease: 'power2.out' }, 0)
        .to(bang, { x: 0, rotation: 0, duration: .8, ease: 'power3.out' }, .42 + ss.length * .06);
    };
    t._in = () => { ready = true; hiss(); };
    ST.create({ trigger: t, start: 'top 85%', end: 'bottom 10%', onEnterBack: hiss, onEnter: () => { if (ready) hiss(); } });
    t.addEventListener('pointerenter', hiss);
    t.addEventListener('pointerdown', hiss);
  });

  /* El lugar: el local lleno se abre con la boca del almud (clip-path en rombo) y las fotos flotan a distinto ritmo */
  $$('.clipin').forEach((m, i) => {
    const img = $('img', m);
    G.timeline({ scrollTrigger: { trigger: m, start: 'top 90%', once: true } })
      .to(m, { clipPath: 'polygon(50% -62%,162% 50%,50% 162%,-62% 50%)', duration: 1.25, ease: 'expo.out', delay: (i % 2) * .08 })
      .to(img, { scale: 1, rotation: 0, duration: 1.6, ease: EXPO }, 0)
      .set(m, { clipPath: 'none' });
  });
  $$('[data-par]').forEach(el => {   // parallax solo de fotos (en celular, a la mitad: nunca pisa a la vecina)
    const s = parseFloat(el.dataset.par) * (innerWidth < 768 ? .3 : 1);
    G.fromTo(el, { y: () => -s * innerHeight * .5 }, { y: () => s * innerHeight * .5, ease: 'none',
      scrollTrigger: { trigger: el, start: 'top bottom', end: 'bottom top', scrub: .6, invalidateOnRefresh: true } });
  });
  // Revelados con máscara (medios)
  $$('.reveal').forEach(m => {
    const inner = $('img, video', m);
    const tl = G.timeline({ scrollTrigger: { trigger: m, start: 'top 92%', once: true } });
    tl.to(m, { clipPath: 'inset(0% 0 0 0)', duration: 1.15, ease: EXPO })
      .to(inner, { scale: 1, duration: 1.6, ease: EXPO }, 0)
      .set(m, { clipPath: 'none' });
  });
  // Bloques de texto
  $$('.rin__c, .it__n, .menu li, .ev__t, .ev__n, .eq__at, .r__q, .datos > div, .donde__btns, .moc__t, .pie__cr').filter(el => !el.closest('.carr') && !el.closest('.cinta')).forEach(el => {
    G.from(el, { y: 26, opacity: 0, duration: .9, ease: EXPO, scrollTrigger: { trigger: el, start: 'top 94%', once: true } });
  });

  /* ───────── v4 fase 5 · Tragos (rosa) ───────── */
  // Las fotos de la banda se «sirven» de arriba abajo (clip-path), como un trago que se llena
  $$('.pour').forEach((m, i) => {
    const img = $('img', m);
    G.timeline({ scrollTrigger: { trigger: m, start: 'top 90%', once: true } })
      .to(m, { clipPath: 'inset(0% 0 0% 0)', duration: 1.2, ease: 'expo.out', delay: (i % 2) * .1 })
      .to(img, { scale: 1, duration: 1.6, ease: EXPO }, 0)
      .set(m, { clipPath: 'none' });
  });
  // Carrusel: al entrar cada tarjeta (por scroll o arrastrándola), su foto se sirve y su nombre literal se arma letra por letra
  const cards = $$('.carr__c');
  if (cards.length && 'IntersectionObserver' in window) {
    const prep = li => {
      const m = $('.m', li), n = $('.it__n', li);
      const chars = n ? splitChars(n) : [];
      G.set(chars, { yPercent: 110, opacity: 0, rotation: i => (i % 3 - 1) * 16 });
      if (m) G.set(m, { clipPath: 'inset(0 0 100% 0)' });
      return () => {
        const tl = G.timeline();
        if (m) tl.to(m, { clipPath: 'inset(0% 0 0% 0)', duration: 1, ease: 'expo.out' }).set(m, { clipPath: 'none' });
        tl.to(chars, { yPercent: 0, opacity: 1, rotation: 0, duration: .5, ease: 'back.out(2.6)', stagger: .028 }, .18);
      };
    };
    const go = new Map(cards.map(li => [li, prep(li)]));
    const io3 = new IntersectionObserver(es => es.forEach(e => {
      if (!e.isIntersecting) return;
      io3.unobserve(e.target); go.get(e.target)();
    }), { threshold: .12 });
    cards.forEach(li => io3.observe(li));
  }

  // v4 fase 9 · el Peter: su nombre literal se arma letra por letra sobre el video y el precio cae en su sitio
  const pe = $('.peter');
  if (pe) {
    const ch = splitChars($('.peter__n', pe)), pr = $('.peter__p', pe);
    G.timeline({ scrollTrigger: { trigger: pe, start: 'top 60%', once: true } })
      .from(ch, { yPercent: 120, opacity: 0, rotation: i => (i % 3 - 1) * 18, duration: .6, ease: 'back.out(2.6)', stagger: .045 })
      .from(pr, { y: 40, opacity: 0, rotation: -8, duration: .8, ease: 'elastic.out(1.1,.45)', clearProps: 'transform,opacity' }, '-=.25');
  }

  /* ───────── v4 fase 5 · Comida (naranja) ───────── */
  // Los platos llegan a la mesa: entran girando un poco (como cuando se sirven) y la foto se abre en redondo, como un plato
  $$('.plato').forEach((m, i) => {
    const card = m.closest('.it') || m, inner = $('img, video', m);
    const rot = [-7, 5, -4, 8][i % 4];
    G.timeline({ scrollTrigger: { trigger: card, start: 'top 90%', once: true }, delay: (i % 3) * .09 })
      .from(card, { rotation: rot, y: 46, opacity: 0, duration: 1.1, ease: 'back.out(1.5)', transformOrigin: '50% 60%', clearProps: 'transform,opacity' })
      .to(m, { clipPath: 'circle(76% at 50% 55%)', duration: 1.1, ease: 'expo.out' }, 0)
      .to(inner, { scale: 1, duration: 1.5, ease: EXPO }, 0)
      .set(m, { clipPath: 'none' });
  });
  // «más que sabrosona!» late: un doble latido cada pocos segundos mientras el título está en pantalla (y al pasar el dedo o el mouse)
  const ct = $('.comida .ttl');
  if (ct) {
    const ws = words(ct).slice(-3);
    ws.forEach(w => w.classList.add('sabro'));
    let ready = false, on = false;
    const beat = G.timeline({ paused: true, repeat: -1, repeatDelay: 2.4 })
      // v4 fase 9: late hacia abajo (origen arriba) y sin giro: «SABROSONA!» nunca sube sobre «PERO MÁS»
      .to(ws, { keyframes: [
        { scaleY: 1.08, scaleX: 1.025, duration: .14, ease: 'power2.out' },
        { scaleY: .98, scaleX: 1, duration: .13, ease: 'power1.in' },
        { scaleY: 1.045, scaleX: 1.012, duration: .12, ease: 'power2.out' },
        { scaleY: 1, scaleX: 1, duration: .5, ease: 'power2.out' }], stagger: .08 });
    G.set(ws, { transformOrigin: '50% 0%' });
    const sync = () => { if (ready && on) beat.play(); else beat.pause(0); };
    ct._in = () => { ready = true; sync(); };
    ST.create({ trigger: ct, start: 'top 85%', end: 'bottom 10%', onToggle: self => { on = self.isActive; sync(); } });
    const again = () => { if (ready) beat.play(0); };
    ct.addEventListener('pointerenter', again); ct.addEventListener('pointerdown', again);
  }
  // «Ver la carta completa»: un micro rebote al aparecer
  $$('.tragos .ver-carta .btn, .comida .ver-carta .btn').forEach(b => {
    G.from(b, { scale: .55, rotation: -5, opacity: 0, duration: .95, ease: 'elastic.out(1.1,.42)', transformOrigin: '100% 50%',
      clearProps: 'transform,opacity', scrollTrigger: { trigger: b, start: 'top 95%', once: true } });
  });

  /* ───────── v4 fase 6 · Con quién (verde) ───────── */
  // El título entra como un brindis: «no somos ná» desde la izquierda y «sin ustedes!» desde la derecha; chocan, rebotan y vibran
  const qt = $('.quien .ttl');
  if (qt) {
    const ws = $$('.w', qt);
    ws.forEach(w => { w.style.overflow = 'visible'; });
    const mid = Math.ceil(ws.length / 2), izq = ws.slice(0, mid), der = ws.slice(mid);
    G.timeline({ scrollTrigger: { trigger: qt, start: 'top 86%', once: true } })
      .from(izq, { x: () => -innerWidth * .7, rotation: -10, opacity: 0, duration: .62, ease: 'power3.in', stagger: { each: .05, from: 'end' } }, 0)
      .from(der, { x: () => innerWidth * .7, rotation: 10, opacity: 0, duration: .62, ease: 'power3.in', stagger: .05 }, 0)
      .to(izq, { x: -16, rotation: -3, duration: .08, ease: 'power2.out' }, .72)                 // ¡chin chin! el choque
      .to(der, { x: 16, rotation: 3, duration: .08, ease: 'power2.out' }, .72)
      .to(ws, { x: 0, rotation: 0, duration: .9, ease: 'elastic.out(1.3,.3)' }, .8)
      .fromTo(qt, { scale: 1 }, { keyframes: [{ scale: 1.05, duration: .07, ease: 'power2.out' }, { scale: 1, duration: .6, ease: 'elastic.out(1,.35)' }], transformOrigin: '30% 60%' }, .72)
      .set([...ws, qt], { clearProps: 'transform,opacity' });
  }

  // La baraja: al entrar se baraja (se parte en dos y se intercala) y se reparte en una pila con rotaciones leves.
  // La foto de arriba se toma con el dedo o el mouse y se lanza con inercia; aparece la siguiente; al acabarse, la pila se arma sola.
  // Clic o toque sin arrastre, Enter o flechas: pasa la foto. touch-action: pan-y → un deslizamiento vertical mueve la página.
  const dk = $('[data-baraja]');
  if (dk && window.PointerEvent) {
    root.classList.add('bj');
    const cards = $$('.carta', dk), n = cards.length, live = $('.baraja__live', dk), hint = $('.baraja__hint', dk);
    dk.tabIndex = 0; dk.setAttribute('role', 'group');
    const R = G.utils.random;
    let pila = [], busy = true, dealt = false, drag = null, k = 1;
    const pose = c => ({ x: c._px, y: c._py, rotation: c._pr });
    const say = () => {
      live.textContent = root.lang === 'en' ? 'Photo ' + k + ' of ' + n : 'Foto ' + k + ' de ' + n;
    };
    const top = () => pila[pila.length - 1];
    const mark = () => { cards.forEach(c => c.classList.remove('is-top')); if (top()) top().classList.add('is-top'); };
    G.set(cards, { opacity: 0 });
    function deal() {
      busy = true;
      pila = G.utils.shuffle(cards.slice());
      pila.forEach((c, i) => { c.style.zIndex = i + 1; c.style.visibility = ''; c._px = R(-16, 16); c._py = R(-12, 12); c._pr = R(-7, 7); });
      const W = dk.clientWidth;
      dk.classList.add('is-dealing');
      G.timeline({ onComplete: () => { busy = false; dk.classList.remove('is-dealing'); mark(); say(); } })
        .fromTo(pila, { x: 0, y: -40, rotation: 0, scale: .9, opacity: 0 }, { y: 0, scale: 1, opacity: 1, duration: .32, ease: 'power2.out', stagger: .012 })
        // barajar: dos mitades que se abren…
        .to(pila, { x: i => (i % 2 ? 1 : -1) * Math.min(W * .3, 170), rotation: i => (i % 2 ? 10 : -10), y: i => -i * 1.5, duration: .36, ease: 'power2.inOut' })
        // …y se intercalan, repartiéndose una a una sobre la pila
        .to(pila, { x: (i, c) => c._px, y: (i, c) => c._py, rotation: (i, c) => c._pr, duration: .55, ease: 'back.out(1.7)', stagger: .045 });
    }
    // v4 fase 7 (6b) · baraja infinita: la foto lanzada sale volando hacia el lado del gesto, frena, gira y vuelve deslizándose
    // POR DEBAJO de la pila hasta quedar última, con la rotación leve de las demás. La pila nunca se vacía ni se rearma de golpe.
    const restack = () => pila.forEach((x, i) => { x.style.zIndex = i + 1; });
    function lanzar(dir, vx = 0, vy = 0) {
      const c = top(); if (!c || busy) return;
      pila.pop(); pila.unshift(c); mark();
      G.killTweensOf(c);
      c.classList.add('is-vuela');
      const out = dir * (c.offsetWidth * 1.18 + 24) + G.utils.clamp(-120, 120, vx * 90);
      c._px = R(-16, 16); c._py = R(-12, 12); c._pr = R(-7, 7);
      G.timeline({ onComplete: () => c.classList.remove('is-vuela') })
        .to(c, { x: out, y: '+=' + G.utils.clamp(-60, 60, vy * 90 + R(-24, 16)), rotation: dir * R(18, 28), duration: .36, ease: 'power3.out' })   // vuela y frena
        .add(restack)                                                                                                                         // ya fuera: pasa al fondo del mazo
        .to(c, { x: c._px, y: c._py, rotation: c._pr, scale: .96, duration: .58, ease: 'power3.inOut' })                                     // gira y vuelve por debajo
        .to(c, { scale: 1, duration: .25, ease: 'power2.out' });
      const nx = top();
      if (nx && nx !== c && !G.isTweening(nx)) G.fromTo(nx, { scale: .97 }, { scale: 1, duration: .5, ease: 'back.out(3)' });
      if (hint) hint.classList.add('is-used');
      k = k % n + 1; say();
    }
    dk.addEventListener('pointerdown', e => {
      if (e.button > 0 || busy || !top()) return;
      const c = top();
      drag = { id: e.pointerId, x0: e.clientX, y0: e.clientY, lx: e.clientX, ly: e.clientY, t: e.timeStamp, vx: 0, vy: 0, on: false, c, p: pose(c), mouse: e.pointerType === 'mouse' };
    });
    dk.addEventListener('pointermove', e => {
      if (!drag || e.pointerId !== drag.id) return;
      const dx = e.clientX - drag.x0, dy = e.clientY - drag.y0;
      if (!drag.on) {
        if (Math.hypot(dx, dy) < 6) return;
        if (!drag.mouse && Math.abs(dy) > Math.abs(dx)) { drag = null; return; }   // gesto vertical: es scroll, no se toca
        drag.on = true; try { dk.setPointerCapture(e.pointerId); } catch (_) {}
        dk.classList.add('is-drag');
      }
      const dt = Math.max(1, e.timeStamp - drag.t);
      drag.vx = (e.clientX - drag.lx) / dt * .7 + drag.vx * .3; drag.vy = (e.clientY - drag.ly) / dt * .7 + drag.vy * .3;
      drag.lx = e.clientX; drag.ly = e.clientY; drag.t = e.timeStamp;
      G.set(drag.c, { x: drag.p.x + dx, y: drag.p.y + dy * (drag.mouse ? 1 : .35), rotation: drag.p.rotation + dx * .06 });
    });
    const soltar = e => {
      if (!drag || e.pointerId !== drag.id) return;
      const d = drag; drag = null; dk.classList.remove('is-drag');
      if (!d.on) { if (e.type === 'pointerup') lanzar(1); return; }   // clic o toque: pasa la foto
      const dx = e.clientX - d.x0;
      if (e.type === 'pointerup' && (Math.abs(dx) > dk.clientWidth * .22 || Math.abs(d.vx) > .45)) lanzar(Math.sign(Math.abs(d.vx) > .45 ? d.vx : dx), d.vx, d.vy);
      else G.to(d.c, { ...d.p, duration: .7, ease: 'elastic.out(1,.45)' });
    };
    dk.addEventListener('pointerup', soltar); dk.addEventListener('pointercancel', soltar);
    dk.addEventListener('lostpointercapture', e => { if (e.target === dk) soltar(e); });
    dk.addEventListener('dragstart', e => e.preventDefault());
    dk.addEventListener('keydown', e => {
      if (e.key === 'Enter' || e.key === 'ArrowRight') { e.preventDefault(); lanzar(1); }
      else if (e.key === 'ArrowLeft') { e.preventDefault(); lanzar(-1); }
    });
    // sus fotos se piden 2 pantallas antes (nunca en el primer pantallazo) y se decodifican fuera del hilo principal: el reparto no se traba
    let listas = null;
    const preparar = () => {
      if (listas) return listas;
      $$('img[data-src]', dk).forEach(loadImg);
      listas = Promise.all($$('img', dk).map(im => (im.complete ? Promise.resolve() : new Promise(ok => { im.addEventListener('load', ok, { once: true }); im.addEventListener('error', ok, { once: true }); }))
        .then(() => (im.decode ? im.decode().catch(() => {}) : null))));
      return listas;
    };
    ST.create({ trigger: dk, start: 'top 300%', once: true, onEnter: preparar });   // sus fotos se piden 1 pantalla antes, nunca en el primer pantallazo
    ST.create({ trigger: dk, start: 'top 78%', once: true, onEnter: () => {
      if (dealt) return; dealt = true;
      Promise.race([preparar(), new Promise(ok => setTimeout(ok, 700))]).then(deal);   // espera las fotos listas, como máximo 0,7 s
    } });
  }

  /* ───────── v4 fase 7 · Eventos (lila) ───────── */
  // «tirar la casa por la ventana!»: las palabras caen desde arriba, como lanzadas por una ventana, y rebotan al llegar
  const et = $('.eventos .ttl');
  if (et) {
    const ws = $$('.w', et);
    ws.forEach(w => { w.style.overflow = 'visible'; });
    // y: desde el borde superior de la sección (overflow: clip)
    G.from(ws, { y: () => -(et.getBoundingClientRect().top - et.closest('.eventos').getBoundingClientRect().top + et.offsetHeight + 40),
      rotation: i => [-18, 12, -8, 16, -12][i % 5], opacity: 0, duration: 1.25, ease: 'bounce.out',
      stagger: .11, clearProps: 'transform,opacity', scrollTrigger: { trigger: et, start: 'top 82%', once: true } });
  }

  // Slider de fiestas: a pantalla completa, avanza solo cada 5 s (con una barra de progreso en su indicador), se pausa mientras
  // se arrastra o mientras no está en pantalla, y se mueve con el dedo, el mouse, las flechas o los indicadores.
  // touch-action: pan-y → un deslizamiento vertical mueve la página. Cada fiesta entra con su nombre letra por letra y sus fotos repartiéndose.
  const fsEl = $('[data-fiestas]');
  if (fsEl && window.PointerEvent) {
    const tr = $('[data-track]', fsEl), slides = [...tr.children], n = slides.length, dots = $$('.fs__dot', fsEl), bars = $$('.fs__bar', fsEl);
    fsEl.classList.add('is-on'); $('.fs__dots', fsEl).hidden = false;
    fsEl.tabIndex = 0; fsEl.setAttribute('role', 'region');
    fsEl.setAttribute('aria-roledescription', 'carrusel');
    slides.forEach(sl => sl.setAttribute('role', 'group'));
    const names = slides.map(sl => { const h = $('.fs__n', sl); return h ? splitChars(h) : []; });
    let i = 0, W = fsEl.clientWidth, drag = null, onScreen = false, prog = null, entered = new Set();
    const listo = () => { $$('img[data-src]', fsEl).forEach(loadImg); $$('video', fsEl).forEach(v => window.__almudAttach && window.__almudAttach(v)); };
    function enter(k) {
      const sl = slides[k], fotos = $$('.fs__f', sl);
      G.fromTo(names[k], { yPercent: 105, opacity: 0, rotation: j => (j % 3 - 1) * 12 }, { yPercent: 0, opacity: 1, rotation: 0, duration: .55, ease: 'back.out(2.4)', stagger: .035, overwrite: true });
      G.fromTo(fotos, { y: () => innerHeight * .35, x: 0, rotation: j => (j % 2 ? 18 : -18), scale: .8, opacity: 0 },   // suben desde abajo: nunca se salen por los lados
        { y: 0, x: 0, rotation: (j, f) => parseFloat(getComputedStyle(f).getPropertyValue('--rot')) || 0, scale: 1, opacity: 1, duration: .9, ease: 'back.out(1.5)', stagger: .12, delay: .15, overwrite: true });   // cada foto queda con su giro leve (--rot)
      entered.add(k);
    }
    function play() {
      if (prog) prog.kill();
      bars.forEach((b, j) => b.style.setProperty('--p', j === i ? 0 : 0));
      const st = { p: 0 };
      prog = G.to(st, { p: 1, duration: 5, ease: 'none', paused: !onScreen || !!drag, onUpdate: () => bars[i].style.setProperty('--p', st.p.toFixed(3)), onComplete: () => go(i + 1) });
    }
    function go(k, dur = .95) {
      i = (k + n) % n;
      G.to(tr, { x: -i * W, duration: dur, ease: 'expo.out', overwrite: true });
      dots.forEach((d, j) => d.setAttribute('aria-current', j === i ? 'true' : 'false'));
      slides.forEach((sl, j) => sl.setAttribute('aria-hidden', j === i ? 'false' : 'true'));
      enter(i); play();
    }
    dots.forEach((d, j) => d.addEventListener('click', () => go(j)));
    fsEl.addEventListener('keydown', e => {
      if (e.key === 'ArrowRight') { e.preventDefault(); go(i + 1); } else if (e.key === 'ArrowLeft') { e.preventDefault(); go(i - 1); }
    });
    fsEl.addEventListener('pointerdown', e => {
      if (e.button > 0 || e.target.closest('.fs__dot')) return;
      drag = { id: e.pointerId, x0: e.clientX, y0: e.clientY, lx: e.clientX, t: e.timeStamp, v: 0, on: false, s0: -i * W };
    });
    fsEl.addEventListener('pointermove', e => {
      if (!drag || e.pointerId !== drag.id) return;
      const dx = e.clientX - drag.x0, dy = e.clientY - drag.y0;
      if (!drag.on) {
        if (Math.hypot(dx, dy) < 6) return;
        if (e.pointerType !== 'mouse' && Math.abs(dy) > Math.abs(dx)) { drag = null; return; }   // vertical: es scroll
        drag.on = true; try { fsEl.setPointerCapture(e.pointerId); } catch (_) {}
        fsEl.classList.add('is-drag'); if (prog) prog.pause(); G.killTweensOf(tr);
      }
      const dt = Math.max(1, e.timeStamp - drag.t); drag.v = (e.clientX - drag.lx) / dt * .7 + drag.v * .3; drag.lx = e.clientX; drag.t = e.timeStamp;
      let x = drag.s0 + dx; const min = -(n - 1) * W;
      if (x > 0) x *= .35; else if (x < min) x = min + (x - min) * .35;
      G.set(tr, { x });
    });
    const soltar = e => {
      if (!drag || e.pointerId !== drag.id) return;
      const d = drag; drag = null; fsEl.classList.remove('is-drag');
      if (!d.on) return;
      const dx = e.clientX - d.x0;
      if (e.type === 'pointerup' && (Math.abs(dx) > W * .18 || Math.abs(d.v) > .4)) go(i - Math.sign(Math.abs(d.v) > .4 ? d.v : dx));
      else go(i);
    };
    fsEl.addEventListener('pointerup', soltar); fsEl.addEventListener('pointercancel', soltar);
    fsEl.addEventListener('lostpointercapture', e => { if (e.target === fsEl) soltar(e); });
    fsEl.addEventListener('dragstart', e => e.preventDefault());
    addEventListener('resize', () => { W = fsEl.clientWidth; G.set(tr, { x: -i * W }); });
    document.addEventListener('visibilitychange', () => { if (!prog) return; if (document.hidden) prog.pause(); else if (onScreen && !drag) prog.resume(); });
    // fotos y video de las fichas: se piden al acercarse (nunca en el primer pantallazo); el video de Jalogüín queda en play desde ahí
    ST.create({ trigger: fsEl, start: 'top 250%', once: true, onEnter: listo });
    names.forEach(ch => G.set(ch, { yPercent: 105, opacity: 0 }));
    G.set($$('.fs__f', fsEl), { opacity: 0 });
    ST.create({ trigger: fsEl, start: 'top 75%', end: 'bottom 25%',
      onToggle: self => {
        onScreen = self.isActive;
        if (!prog) { if (onScreen) go(0, 0); return; }
        if (onScreen && !drag && !document.hidden) prog.resume(); else prog.pause();
      } });
  }

  /* ───────── v4 fase 8 · Equipo (rojo): tarjetas que se dan vuelta ───────── */
  const flips = $$('.flip');
  if (flips.length) {
    root.classList.add('fl');
    flips.forEach((f, k) => {
      f.style.setProperty('--k', k % 3);
      // v4 fase 11: el giro depende SOLO de .is-on (antes :focus-within y :hover también giraban: al quedar con foco tras el clic,
      // la tarjeta no volvía nunca). Clic, tap o Enter/Espacio alternan; hover solo la inclina un poco.
      const flipT = () => { const on = f.classList.toggle('is-on'); f.setAttribute('aria-pressed', on); };
      f.tabIndex = 0; f.setAttribute('role', 'button'); f.setAttribute('aria-pressed', 'false');
      f.addEventListener('click', e => { if (!e.target.closest('a')) flipT(); });
      f.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); flipT(); } });
      f.addEventListener('animationend', () => f.classList.remove('peek'));
    });
    ST.create({ trigger: '.eqz', start: 'top 70%', once: true, onEnter: () => flips.forEach(f => f.classList.add('peek')) });
  }

  /* ───────── Reseñas (crema): dos cintas de tarjetas que se leen enteras ───────── */
  // v4 fase 9: cada cinta avanza una tarjeta y se detiene 2,4 s con las tarjetas enteras en pantalla (alineadas al margen);
  // las dos van en sentidos contrarios, se pausan con hover o foco y se arrastran con el dedo o el mouse (al soltar, encaja en una tarjeta).
  const cinta = $('[data-cinta]');
  if (cinta && window.PointerEvent) {
    root.classList.add('cn');
    cinta.setAttribute('role', 'region'); cinta.tabIndex = 0;
    const rows = $$('.cinta__row', cinta).map(row => {
      [...row.children].forEach(li => { const c = li.cloneNode(true); c.setAttribute('aria-hidden', 'true'); c.querySelectorAll('[aria-label]').forEach(x => x.removeAttribute('aria-label')); row.appendChild(c); });
      return { row, dir: +row.dataset.dir, x: 0, step: 0, half: 0, base: 0, tw: null };
    });
    const set = r => { r.row.style.transform = 'translate3d(' + r.x.toFixed(2) + 'px,0,0)'; };
    const norm = r => { while (r.x <= r.base - r.half) r.x += r.half; while (r.x > r.base) r.x -= r.half; };
    const snapX = r => r.base + Math.round((r.x - r.base) / r.step) * r.step;
    const measure = () => rows.forEach(r => {
      const li = r.row.children; r.step = li[1].offsetLeft - li[0].offsetLeft; r.half = r.step * (li.length / 2);
      r.base = 0;   // la cinta ya va dentro de los márgenes: la tarjeta queda alineada a su borde
      r.x = snapX(r); norm(r); set(r);
    });
    measure(); addEventListener('resize', measure);
    let on = false, hold = false, drag = null;
    // v4 fase 11: más ágil: pausa de 1 s y paso de 0,8 s; la segunda cinta va desfasada medio ciclo, así siempre hay una moviéndose
    const PAUSA = 1, PASO = .8;
    const next = (r, d = PAUSA) => {
      if (r.tw) r.tw.kill();
      r.tw = G.delayedCall(d, () => {
        if (!on || hold || drag) { next(r); return; }
        const st = { x: r.x };
        r.tw = G.to(st, { x: r.x + r.dir * r.step, duration: PASO, ease: 'power2.inOut', onUpdate: () => { r.x = st.x; set(r); },
          onComplete: () => { norm(r); set(r); next(r); } });
      });
    };
    ST.create({ trigger: cinta, start: 'top bottom', end: 'bottom top', onToggle: self => { on = self.isActive; if (on) rows.forEach((r, i) => { if (!r.tw) next(r, PAUSA + i * (PAUSA + PASO) / 2); }); } });
    cinta.addEventListener('pointerenter', e => { if (e.pointerType === 'mouse') hold = true; });
    cinta.addEventListener('pointerleave', e => { if (e.pointerType === 'mouse') hold = false; });
    cinta.addEventListener('focusin', () => { hold = true; }); cinta.addEventListener('focusout', () => { hold = false; });
    cinta.addEventListener('pointerdown', e => {
      const row = e.target.closest('.cinta__row'); if (!row || e.button > 0) return;
      const r = rows.find(q => q.row === row);
      drag = { id: e.pointerId, r, x0: e.clientX, y0: e.clientY, lx: e.clientX, t: e.timeStamp, v: 0, on: false, s: r.x };
    });
    cinta.addEventListener('pointermove', e => {
      if (!drag || e.pointerId !== drag.id) return;
      const dx = e.clientX - drag.x0, dy = e.clientY - drag.y0;
      if (!drag.on) {
        if (Math.hypot(dx, dy) < 6) return;
        if (e.pointerType !== 'mouse' && Math.abs(dy) > Math.abs(dx)) { drag = null; return; }   // vertical: es scroll
        drag.on = true; if (drag.r.tw) drag.r.tw.kill(); try { cinta.setPointerCapture(e.pointerId); } catch (_) {} cinta.classList.add('is-drag');
      }
      const dt = Math.max(1, e.timeStamp - drag.t); drag.v = (e.clientX - drag.lx) / dt * .7 + drag.v * .3; drag.lx = e.clientX; drag.t = e.timeStamp;
      const r = drag.r; r.x = drag.s + dx; norm(r); set(r);
    });
    const soltar = e => {
      if (!drag || e.pointerId !== drag.id) return;
      const d = drag; drag = null; cinta.classList.remove('is-drag');
      if (!d.on) return;
      const r = d.r, st = { x: r.x }, to = r.base + Math.round((r.x + d.v * 180 - r.base) / r.step) * r.step;   // inercia y encaje en una tarjeta
      r.tw = G.to(st, { x: to, duration: .7, ease: 'power3.out', onUpdate: () => { r.x = st.x; set(r); }, onComplete: () => { norm(r); set(r); next(r); } });
    };
    cinta.addEventListener('pointerup', soltar); cinta.addEventListener('pointercancel', soltar);
    cinta.addEventListener('lostpointercapture', e => { if (e.target === cinta) soltar(e); });
    cinta.addEventListener('dragstart', e => e.preventDefault());
  }

  /* ───────── Cierre (negro): «Le esperamos desde las 18:00 hrs» se escribe en vivo ───────── */
  const dt_ = $('.donde__sub'), dtt = dt_ && $('.donde__sub-t', dt_);   // 8c: ahora es el subtítulo del cierre
  if (dtt) {
    const chars = splitChars(dtt);
    G.set(chars, { opacity: 0 });
    const cur = document.createElement('span'); cur.className = 'tw-c'; cur.setAttribute('aria-hidden', 'true'); dt_.appendChild(cur);
    const place = k => {   // el cursor va justo después de la última letra escrita (solo transform: no mueve nada)
      const base = dt_.getBoundingClientRect(), c = chars[Math.max(0, k)].getBoundingClientRect();
      cur.style.transform = 'translate(' + (k < 0 ? c.left - base.left : c.right - base.left + 2).toFixed(1) + 'px,' + (c.top - base.top + c.height * .08).toFixed(1) + 'px)';
    };
    place(-1);
    ST.create({ trigger: dt_, start: 'top 80%', once: true, onEnter: () => {
      let k = 0;
      const typeOne = () => {
        if (k >= chars.length) return;
        chars[k].style.opacity = 1; place(k);
        const ch = chars[k].textContent; k++;
        G.delayedCall(ch === ' ' ? .02 : (/[,:]/.test(ch) ? .26 : .055 + Math.random() * .05), typeOne);   // ritmo de máquina, con pausa en «:»
      };
      typeOne();
    } });
    addEventListener('resize', () => place(chars.findIndex(c => c.style.opacity !== '1') - 1));
  }

  const mm = G.matchMedia();
  // Parallax sutil: masas a distinta velocidad (≥768 px)
  mm.add('(min-width:768px)', () => {
    $$('[data-speed]').forEach(el => {
      const s = parseFloat(el.dataset.speed);
      G.fromTo(el, { y: () => -s * innerHeight * .5 }, { y: () => s * innerHeight * .5, ease: 'none',
        scrollTrigger: { trigger: el, start: 'top bottom', end: 'bottom top', scrub: true, invalidateOnRefresh: true } });
    });
  });
  addEventListener('load', () => ST.refresh());
})();
