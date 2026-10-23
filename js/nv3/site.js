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
  const land = matchMedia('(orientation: landscape) and (min-width:768px)');
  const heroVisible = () => $(land.matches ? '.hero__v--d video' : '.hero__v--m video');
  attach(heroVisible());
  land.addEventListener('change', () => attach(heroVisible()));
  const lazy = $$('video.v:not([data-hero])');
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { io.unobserve(e.target); attach(e.target); } }),
      { rootMargin: '0px 0px 15% 0px' });
    lazy.forEach(v => io.observe(v));
  } else lazy.forEach(attach);

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
  const ATTR = [['data-alt-en', 'alt'], ['data-aria-en', 'aria-label']];
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
  const navState = () => root.classList.toggle('is-past', scrollY > hero.offsetHeight - 170);
  addEventListener('scroll', navState, { passive: true }); navState();

  /* ───────── La ruleta de rincones (v4 fase 4) ─────────
     Se arrastra con el dedo o el mouse (pointer events propios), con inercia y encaje en cada foto.
     touch-action: pan-y → el scroll vertical sigue siendo del navegador: la ruleta nunca lo secuestra ni lo escucha.
     Cada foto se inclina según la velocidad y vuelve a su sitio. Solo transform. Con movimiento reducido: arrastre sin inclinación ni giro de entrada. */
  function ruleta() {
    const vp = $('[data-ruleta]'), tr = vp && $('[data-track]', vp);
    if (!vp || !tr || !window.PointerEvent) return;
    root.classList.add('rul');
    const items = $$('.rin', tr);
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
      drag = { id: e.pointerId, x0: e.clientX, y0: e.clientY, s0: x, t: e.timeStamp, lx: e.clientX, v: 0, on: e.pointerType === 'mouse' };
      if (drag.on) { vp.setPointerCapture(e.pointerId); vp.classList.add('is-drag'); }
      loadAll(); kick();
    });
    vp.addEventListener('pointermove', e => {
      if (!drag || e.pointerId !== drag.id) return;
      const dx = e.clientX - drag.x0;
      if (!drag.on) {               // en táctil: solo si el gesto es horizontal (si es vertical, el navegador ya hizo scroll y canceló)
        if (Math.abs(dx) < 6) return;
        drag.on = true; try { vp.setPointerCapture(e.pointerId); } catch (_) {}
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
    vp.addEventListener('lostpointercapture', end);
    vp.addEventListener('dragstart', e => e.preventDefault());
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
  ruleta();

  /* ───────── Movimiento ───────── */
  const G = window.gsap, ST = window.ScrollTrigger;
  if (!G || !ST || reduce) { root.classList.remove('intro'); return; }
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
  function intro() {
    const win = $('[data-win]'), iso = $('.hero__iso'), svg = $('svg', iso);
    const r = svg.getBoundingClientRect(), k = r.width / 660;
    // boca del almud (rombo interior del isotipo) en píxeles
    const cx = r.left + (299.5 + 20) * k, cy = r.top + (242.5 + 20) * k, a = 212 * k, b = 166 * k;
    const W = innerWidth, H = hero.offsetHeight;
    // el velo cubre justo la pantalla (+12 %): una capa chica que luego solo se escala en el compositor
    const u = (px, o) => ((px - o) / k).toFixed(0);
    const vx0 = u(-W * .12, r.left) - 20, vx1 = +u(W * 1.12, r.left) - 20, vy0 = u(-H * .12, r.top) - 20, vy1 = +u(H * 1.12, r.top) - 20;
    $('.iso__veil', iso).setAttribute('d', 'M' + vx0 + ' ' + vy0 + 'H' + vx1 + 'V' + vy1 + 'H' + vx0 + 'ZM287 76L87 192L271 409L512 217Z');
    const S = 1.3 * Math.max(...[[0, 0], [W, 0], [0, H], [W, H]].map(([px, py]) => Math.abs(px - cx) / a + Math.abs(py - cy) / b));
    const ox = ((299.5 + 20) / 660 * 100).toFixed(2) + '%', oy = ((242.5 + 20) / 940 * 100).toFixed(2) + '%';
    const ltrs = $$('.hero__svg .ltr');
    const chars = splitChars($('.hero__claim-t'));
    const gloss = $('.hero__claim .gloss');
    const btn = $('.hero__btns .btn');
    const logoIso = $('.hero__svg g g');   // el almudcito del logo: aterriza después de las letras
    const inEls = $$('.hero__in > *');
    const done = () => {
      root.classList.remove('intro');
      G.set([...inEls, iso, '.nav', win, ...ltrs, ...chars, btn, logoIso].filter(Boolean), { clearProps: 'transform,opacity' });
      ['wheel', 'touchstart', 'pointerdown', 'keydown'].forEach(ev => removeEventListener(ev, skip));
      removeEventListener('scroll', skip);
    };
    const tl = G.timeline({ onComplete: done });
    if (gloss) tl.from(gloss, { opacity: 0, duration: .4 }, 1.9);
    if (logoIso) tl.from(logoIso, { scale: 0, rotation: -28, opacity: 0, transformOrigin: '50% 50%', duration: .7, ease: 'back.out(2.6)' }, 1.55);
    G.set(iso, { xPercent: -50, yPercent: -50, x: 0, y: 0, transformOrigin: ox + ' ' + oy });
    tl.set(inEls, { opacity: 1 }, 0)
      .fromTo(window.__noWin ? {} : win, { scale: 1.14 }, { scale: 1, duration: 1.7, ease: 'expo.out' }, .3)
      .to($$('.iso__g path', iso), { strokeDashoffset: 0, duration: .62, ease: 'power2.inOut', stagger: .035 }, 0)
      .to(window.__noIso ? {} : iso, { scale: S, duration: .8, ease: 'power3.in' }, .72)
      .set(iso, { opacity: 0 }, 1.52)
      .from(ltrs, { y: 380, opacity: 0, rotation: i => (i % 2 ? 1 : -1) * (8 + i * 1.5), duration: .7, ease: 'back.out(2.4)', stagger: .055 }, 1.12)
      .from(window.__noCh ? {} : chars, { yPercent: 115, opacity: 0, rotation: i => (i % 3 - 1) * 14, duration: .42, ease: 'back.out(3)', stagger: .011 }, 1.34)
      .fromTo(btn, { scale: .35, opacity: 0, rotation: -7 }, { scale: 1, opacity: 1, rotation: 0, duration: .6, ease: 'elastic.out(1.1,.45)' }, 1.9)
      .fromTo('.nav', { opacity: 0 }, { opacity: 1, duration: .5 }, 1.6);
    function skip() { if (tl.progress() < 1) tl.progress(1); }
    ['wheel', 'touchstart', 'pointerdown', 'keydown'].forEach(ev => addEventListener(ev, skip, { passive: true }));
    // un scroll real (no el de la restauración de la página) también la salta
    setTimeout(() => addEventListener('scroll', skip, { passive: true }), 60);
    window.__almudIntroTL = tl;
  }
  // si el JS llega tarde (red lenta), no se hace esperar al turista: la portada aparece de inmediato
  if (root.classList.contains('intro') && scrollY < 10 && performance.now() < 1400) { window.__almudIntro = true; intro(); } else root.classList.remove('intro');

  // Revelados de titulares
  $$('.ttl, .pie__f').forEach(t => {
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
      const fs = parseFloat(getComputedStyle(t).fontSize) || 44, dx = fs * .075;
      const tl = G.timeline({ onComplete: () => { busy = false; G.set([...ss, bang].filter(Boolean), { clearProps: 'transform' }); } });
      tl
        .to(ss, { scaleY: 1.6, scaleX: .82, yPercent: -6, x: i => (i + 1) * dx, duration: .2, ease: 'power2.out', stagger: .045 })
        .to(ss, { scaleY: 1, scaleX: 1, yPercent: 0, x: 0, duration: 1.15, ease: 'elastic.out(1.15,.3)', stagger: .05 }, .3);
      if (bang) tl.to(bang, { x: (ss.length + 1) * dx, rotation: 14, duration: .22, ease: 'power2.out' }, .1)
        .to(bang, { x: 0, rotation: 0, duration: 1.1, ease: 'elastic.out(1.2,.3)' }, .45);
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
  $$('[data-par]').forEach(el => {   // parallax solo de fotos
    const s = parseFloat(el.dataset.par);
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
  $$('.rin__c, .it__n, .menu li, .ev__t, .ev__n, .eq__at, .r__q, .datos > div, .donde__btns, .moc__t, .pie__cr').forEach(el => {
    G.from(el, { y: 26, opacity: 0, duration: .9, ease: EXPO, scrollTrigger: { trigger: el, start: 'top 94%', once: true } });
  });

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
