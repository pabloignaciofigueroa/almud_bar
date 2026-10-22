/* Almud Bar · v3
   Videos: autoplay muted loop playsinline. El JS SOLO les pone el póster y la fuente: la portada
   (por orientación) ya la conectó el script en línea del HTML; el resto se conecta una sola vez cuando
   está a ≤0,6 pantallas (IntersectionObserver SOLO para cargar). Una vez cargado, nunca se pausa ni se toca.
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
      { rootMargin: '10% 0px 60% 0px' });
    lazy.forEach(v => io.observe(v));
  } else lazy.forEach(attach);

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
    el.innerHTML = el.textContent.trim().split(/\s+/).map(w => '<span class="w"><span class="w__i">' + w + '</span></span>').join(' ');
  });
  const words = el => $$('.w__i', el);

  /* Momento memorable: el isotipo se abre al video */
  function intro() {
    const win = $('[data-win]'), iso = $('.hero__iso'), svg = $('svg', iso);
    const W = innerWidth, H = hero.offsetHeight;
    const r = svg.getBoundingClientRect();
    const P = (x, y) => [r.left + (x + 20) / 660 * r.width, r.top + (y + 20) / 940 * r.height];
    // boca del almud (rombo interior) con sus puntos medios: 8 vértices
    const T = P(287, 76), R = P(512, 217), B = P(271, 409), L = P(87, 192);
    const mid = (a, b) => [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2];
    const rh = [T, mid(T, R), R, mid(R, B), B, mid(B, L), L, mid(L, T)];
    const c = mid(T, B);
    const o = 24;
    const full = [[W / 2, -o], [W + o, -o], [W + o, H / 2], [W + o, H + o], [W / 2, H + o], [-o, H + o], [-o, H / 2], [-o, -o]];
    const st = { k: 0, e: 0 };
    const draw = () => {
      const pts = rh.map((p, i) => {
        const x0 = c[0] + (p[0] - c[0]) * st.k, y0 = c[1] + (p[1] - c[1]) * st.k;
        return (x0 + (full[i][0] - x0) * st.e).toFixed(1) + 'px ' + (y0 + (full[i][1] - y0) * st.e).toFixed(1) + 'px';
      });
      win.style.clipPath = 'polygon(' + pts.join(',') + ')';
    };
    draw();
    const inEls = $$('.hero__in > *');
    const tl = G.timeline({
      onComplete() { win.style.clipPath = ''; root.classList.remove('intro'); G.set([...inEls, iso, '.nav'], { clearProps: 'all' }); }
    });
    tl.to($$('path', iso), { strokeDashoffset: 0, duration: .75, ease: 'power3.inOut', stagger: .04 }, .05)
      .to(st, { k: 1, duration: .55, ease: EXPO, onUpdate: draw }, .5)
      .to(st, { e: 1, duration: 1.05, ease: 'expo.inOut', onUpdate: draw }, 1.0)
      .to(iso, { scale: 5.5, opacity: 0, duration: 1.05, ease: 'expo.in', transformOrigin: '50% 40%' }, 1.0)
      .fromTo('.hero__logo', { opacity: 1, clipPath: 'inset(0 100% 0 0)' }, { clipPath: 'inset(0 0% 0 0)', duration: 1.1, ease: EXPO }, 1.7)
      .fromTo('.hero__claim', { opacity: 0, y: 24 }, { y: 0, opacity: 1, duration: .9, ease: EXPO }, 1.85)
      .fromTo('.hero__btns', { opacity: 0, y: 24 }, { y: 0, opacity: 1, duration: .9, ease: EXPO }, 1.95)
      .fromTo('.nav', { opacity: 0 }, { opacity: 1, duration: .6 }, 2.0);
  }
  if (root.classList.contains('intro') && scrollY < 10) intro(); else root.classList.remove('intro');

  // Revelados de titulares
  $$('.ttl, .pie__f').forEach(t => {
    G.from(words(t), { yPercent: 110, duration: 1.05, ease: EXPO, stagger: .045,
      scrollTrigger: { trigger: t, start: 'top 88%', once: true },
      onComplete: () => $$('.w', t).forEach(w => { w.style.overflow = 'visible'; }) });
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
  // Galería horizontal sticky (escritorio, sin pin)
  mm.add('(min-width:1024px)', () => {
    const wrap = $('[data-h]'), tr = $('[data-track]');
    const dist = () => Math.max(0, tr.scrollWidth - innerWidth);
    const size = () => { wrap.style.height = (dist() + innerHeight) + 'px'; };
    size();
    const tw = G.to(tr, { x: () => -dist(), ease: 'none',
      scrollTrigger: { trigger: wrap, start: 'top top', end: 'bottom bottom', scrub: .6, invalidateOnRefresh: true, onRefreshInit: size } });
    return () => { wrap.style.height = ''; tw.kill(); };
  });
  addEventListener('load', () => ST.refresh());
})();
