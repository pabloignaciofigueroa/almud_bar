/* Almud Bar v2 · site.js
   Sin dependencias: el movimiento es CSS (transiciones con los tokens de tokens.css) disparado por IntersectionObserver.
   GSAP/ScrollTrigger no se cargan: no hay ninguna línea de tiempo atada al scroll (Emil: CSS/WAAPI primero).
   Sin JS (o si algo falla) todo queda visible: los estados ocultos solo los pone este archivo. */
(() => {
  'use strict';
  const d = document, root = d.documentElement;
  const $ = (s, c = d) => c.querySelector(s);
  const $$ = (s, c = d) => [...c.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)');
  const hasIO = 'IntersectionObserver' in window;
  const store = { get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }, set(k, v) { try { localStorage.setItem(k, v); } catch (e) { /* sin almacenamiento: no pasa nada */ } } };

  /* ───────── idioma: atributos data-en / data-alt-en / data-aria-en (lección de la v1) ───────── */
  const ATTRS = [['data-alt-en', 'alt'], ['data-aria-en', 'aria-label']];
  function setLang(lang, save) {
    root.lang = lang;
    $$('[data-en]').forEach((el) => {
      if (el.dataset.es === undefined) el.dataset.es = el.textContent;
      el.textContent = lang === 'en' ? el.dataset.en : el.dataset.es;
    });
    ATTRS.forEach(([src, attr]) => $$('[' + src + ']').forEach((el) => {
      const k = 'es' + attr.replace(/[^a-z]/gi, '');
      if (el.dataset[k] === undefined) el.dataset[k] = el.getAttribute(attr) || '';
      el.setAttribute(attr, lang === 'en' ? el.getAttribute(src) : el.dataset[k]);
    }));
    const md = $('meta[name="description"]');
    if (md) { if (!md.dataset.es) md.dataset.es = md.content; md.content = lang === 'en' ? md.dataset.metaEn : md.dataset.es; }
    $$('.lang-b').forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.lang === lang)));
    $$('.vid-b').forEach(paintVideoButton);
    if (save) store.set('almud-lang', lang);
  }
  $$('.lang-b').forEach((b) => b.addEventListener('click', () => setLang(b.dataset.lang, true)));

  /* ───────── videos: solo corren a la vista; en reduced motion quedan en su póster ───────── */
  function paintVideoButton(b) {
    const paused = b.getAttribute('aria-pressed') === 'true';
    const en = root.lang === 'en';
    b.textContent = paused ? (en ? b.dataset.enAlt : b.dataset.esAlt) : (en ? b.dataset.en : (b.dataset.es || 'Pausar video'));
  }
  const vids = $$('.vid');
  const vio = hasIO ? new IntersectionObserver((es) => es.forEach((e) => {
    const box = e.target, v = $('video', box);
    box._in = e.isIntersecting;
    if (e.isIntersecting && !box._paused && !reduce.matches) { v.preload = 'auto'; const p = v.play(); if (p) p.catch(() => {}); }
    else if (!v.paused) v.pause();
  }), { threshold: 0.25 }) : null;
  vids.forEach((box) => {
    const v = $('video', box), b = $('.vid-b', box);
    box._paused = reduce.matches;
    if (b) {
      b.dataset.es = b.textContent;
      b.setAttribute('aria-pressed', String(box._paused));
      paintVideoButton(b);
      b.addEventListener('click', () => {
        box._paused = !box._paused;
        b.setAttribute('aria-pressed', String(box._paused));
        paintVideoButton(b);
        if (box._paused) v.pause(); else { v.preload = 'auto'; const p = v.play(); if (p) p.catch(() => {}); }
      });
    }
    if (vio) vio.observe(box);
  });

  const saved = store.get('almud-lang');
  if (saved === 'en' || root.lang === 'en') setLang('en', false);

  /* ───────── menú del teléfono: clip-path 400 ms drawer, cierre 250 ms; Escape y teclado sin animación ───────── */
  const mb = $('.menu-b'), hoja = $('#hoja');
  let byKey = false;
  d.addEventListener('keydown', () => { byKey = true; }, true);
  d.addEventListener('pointerdown', () => { byKey = false; }, true);
  function openMenu() {
    hoja.hidden = false;
    hoja.classList.remove('cierra');
    if (!byKey && !reduce.matches) { hoja.classList.add('abre'); }
    mb.setAttribute('aria-expanded', 'true');
    root.classList.add('hoja-on');
    const first = $('a', hoja); if (first) first.focus({ preventScroll: true });
  }
  function closeMenu(instant) {
    mb.setAttribute('aria-expanded', 'false');
    root.classList.remove('hoja-on');
    hoja.classList.remove('abre');
    if (instant || byKey || reduce.matches) { hoja.hidden = true; return; }
    hoja.classList.add('cierra');
    hoja.addEventListener('animationend', () => { hoja.classList.remove('cierra'); hoja.hidden = true; }, { once: true });
  }
  if (mb && hoja) {
    mb.addEventListener('click', () => (mb.getAttribute('aria-expanded') === 'true' ? closeMenu(false) : openMenu()));
    $$('a', hoja).forEach((a) => a.addEventListener('click', () => closeMenu(true)));
    d.addEventListener('keydown', (e) => { if (e.key === 'Escape' && mb.getAttribute('aria-expanded') === 'true') { closeMenu(true); mb.focus(); } });
    matchMedia('(min-width: 1024px)').addEventListener('change', (e) => { if (e.matches) closeMenu(true); });
  }

  /* ───────── reseñas: en el teléfono, tres y "Ver más reseñas" ───────── */
  const rg = $('.res-g'), rb = $('.res-mas-b');
  if (rg && rb && matchMedia('(max-width: 699px)').matches) {
    rg.classList.add('res-pocas');
    rb.addEventListener('click', () => {
      rg.classList.remove('res-pocas');
      rb.setAttribute('aria-expanded', 'true');
      const r4 = $('.res-4', rg); if (r4) { r4.tabIndex = -1; r4.focus({ preventScroll: true }); }
    });
  }

  /* ───────── reveals: una sola vez, solo lo que aún está bajo el pliegue ───────── */
  if (!hasIO) return;
  /* una imagen lazy dentro de un marco recortado no "se ve" para el navegador: se pide al revelar */
  const eager = (el) => $$('img[loading="lazy"]', el).forEach((i) => { i.loading = 'eager'; });
  const below = (el) => el.getBoundingClientRect().top > innerHeight * 0.92;
  /* se observa el padre: un blanco recortado entero por clip-path no cuenta como visible para el observador */
  const armed = new Map();
  const io = new IntersectionObserver((es) => es.forEach((e) => {
    if (!e.isIntersecting) return;
    (armed.get(e.target) || [e.target]).forEach((el) => { eager(el); el.classList.add('rv-in'); });
    io.unobserve(e.target);
  }), { rootMargin: '0px 0px -12% 0px', threshold: 0 });
  $$('[data-rv]').forEach((el) => {
    if (el.closest('.hoy') || !below(el)) return;
    el.classList.add(el.dataset.rv === 'fade' ? 'fade-arm' : 'rv-arm');
    const host = el.parentElement;
    if (!armed.has(host)) { armed.set(host, []); io.observe(host); }
    armed.get(host).push(el);
  });
  $$('h2.display, h2.head').forEach((h) => {
    if (!$('.ln', h) || h.closest('.hoy') || !below(h)) return;
    h.classList.add('h-arm');
    armed.set(h, [h]);
    io.observe(h);
  });

  /* el momento autoral: "la franja se imprime", una vez, al entrar Hoy en Almud */
  const hoy = $('#hoy');
  if (hoy && below(hoy)) {
    hoy.classList.add('arm');
    const hio = new IntersectionObserver((es) => {
      if (!es[0].isIntersecting) return;
      eager(hoy.querySelector('.hoy-dia:not([hidden])') || hoy);
      hoy.classList.add('imprime');
      hio.disconnect();
    }, { rootMargin: '0px 0px -25% 0px' });
    hio.observe(hoy);
  }
})();
