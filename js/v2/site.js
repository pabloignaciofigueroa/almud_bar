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
    if (save) store.set('almud-idioma', lang);
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
  /* fase 16: el póster se pide recién cuando el video está a una pantalla (no compite con la portada) */
  const pio = hasIO ? new IntersectionObserver((es) => es.forEach((e) => {
    if (!e.isIntersecting) return; const v = $('video', e.target); if (v.dataset.poster) { v.poster = v.dataset.poster; delete v.dataset.poster; } pio.unobserve(e.target);
  }), { rootMargin: '100% 0px' }) : null;
  vids.forEach((box) => {
    const v = $('video', box), b = $('.vid-b', box);
    if (pio) pio.observe(box); else if (v.dataset.poster) v.poster = v.dataset.poster;
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

  /* el color dominante y el LQIP solo hacen falta mientras la foto carga */
  const done = (i) => { i.style.background = 'none'; };
  $$('.f img, .cover-img img').forEach((i) => { if (i.complete && i.naturalWidth) done(i); else i.addEventListener('load', () => done(i), { once: true }); });

  const saved = store.get('almud-idioma');
  if (saved === 'en' || root.lang === 'en') setLang('en', false);

  /* ───────── menú del teléfono (crítica 1, P0) ─────────
     El estado vive en una clase (.abierta) y el CSS hace una transición de clip-path: 400 ms drawer al abrir, 250 ms al cerrar,
     interrumpible desde el valor actual. No hay animationend ni temporizadores: abrir, cerrar y reabrir rápido no deja
     manejadores pendientes que oculten la hoja. Teclado, Escape y enlaces de la hoja: instantáneo (.al-instante). */
  const mb = $('.menu-b'), hoja = $('#hoja');
  let byKey = false;
  d.addEventListener('keydown', () => { byKey = true; }, true);
  d.addEventListener('pointerdown', () => { byKey = false; }, true);
  /* fase 16: con la hoja abierta, lo de atrás queda inerte (ni foco ni lector de pantalla): el foco no se escapa de la hoja */
  const behind = () => [$('main'), $('.pie-sitio'), $('.skip'), $('.nav-logo'), $('.nav-links'), $('.nav .btn')].filter(Boolean);
  function setMenu(open, instant) {
    if (!mb || !hoja) return;
    const now = instant || byKey;
    behind().forEach((el) => { el.inert = open; if (open) el.setAttribute('aria-hidden', 'true'); else el.removeAttribute('aria-hidden'); });
    if (now) hoja.classList.add('al-instante');
    hoja.classList.toggle('abierta', open);
    mb.setAttribute('aria-expanded', String(open));
    root.classList.toggle('hoja-on', open);
    if (now) { void hoja.offsetWidth; hoja.classList.remove('al-instante'); }
    if (open) { const first = $('a', hoja); if (first) first.focus({ preventScroll: true }); }
  }
  if (mb && hoja) {
    hoja.hidden = false;  /* sin JS la hoja queda oculta con [hidden]; con JS la ocultan visibility y clip-path */
    mb.addEventListener('click', () => setMenu(mb.getAttribute('aria-expanded') !== 'true', false));
    $$('a', hoja).forEach((a) => a.addEventListener('click', () => setMenu(false, true)));
    /* Tab desde el último control de la hoja vuelve al botón Menú (y Mayús+Tab desde Menú, al último): el foco da la vuelta adentro */
    hoja.addEventListener('keydown', (e) => {
      if (e.key !== 'Tab' || e.shiftKey) return;
      const f = $$('a, button', hoja); if (d.activeElement === f[f.length - 1]) { e.preventDefault(); mb.focus(); }
    });
    mb.addEventListener('keydown', (e) => {
      if (e.key !== 'Tab' || !e.shiftKey || mb.getAttribute('aria-expanded') !== 'true') return;
      const f = $$('a, button', hoja); e.preventDefault(); f[f.length - 1].focus();
    });
    d.addEventListener('keydown', (e) => { if (e.key === 'Escape' && mb.getAttribute('aria-expanded') === 'true') { setMenu(false, true); mb.focus(); } });
    matchMedia('(min-width: 1024px)').addEventListener('change', (e) => { if (e.matches) setMenu(false, true); });
  }

  /* ───────── mapa: el iframe de Google Maps se crea solo al tocar "Ver mapa" (ningún pedido a terceros antes) ───────── */
  const mapa = $('.mapa');
  if (mapa) {
    const a = $('.mapa-b', mapa);
    a.addEventListener('click', (e) => {
      e.preventDefault();
      const f = d.createElement('iframe');
      f.src = mapa.dataset.mapa;
      f.title = root.lang === 'en' ? mapa.dataset.titleEn : mapa.dataset.titleEs;
      f.loading = 'eager';
      f.referrerPolicy = 'no-referrer-when-downgrade';
      f.setAttribute('allowfullscreen', '');
      mapa.classList.add('cargado');
      a.replaceWith(f);
      f.focus({ preventScroll: true });
    });
  }

  /* ───────── eventos: el próximo mes con evento, según la fecha en America/Santiago ─────────
     Mismo mecanismo que Hoy en Almud. Sin JS (o si Intl falla) no se marca nada y el calendario queda completo. */
  const cal = $$('.cal li[data-mes]');
  if (cal.length) {
    try {
      const m = +new Intl.DateTimeFormat('en-US', { timeZone: 'America/Santiago', month: 'numeric' }).format(new Date());
      const months = [...new Set(cal.map((li) => +li.dataset.mes))].sort((x, y) => x - y);
      const next = months.find((x) => x >= m) || months[0];
      cal.filter((li) => +li.dataset.mes === next).forEach((li) => {
        li.classList.add('es-prox');
        const tag = $(next === m ? '.ev-este' : '.ev-prox', li);
        if (tag) tag.hidden = false;
      });
    } catch (e) { /* sin Intl con zona horaria: el calendario queda sin marca */ }
  }

  /* ───────── nav de escritorio: la sección a la vista lleva aria-current (y su subrayado) ───────── */
  const navl = $$('.nav-links a[href^="#"]');
  if (navl.length && hasIO) {
    const byId = new Map(navl.map((a) => [a.getAttribute('href').slice(1), a]));
    const nio = new IntersectionObserver((es) => es.forEach((e) => {
      const a = byId.get(e.target.id);
      if (!a) return;
      if (e.isIntersecting) { navl.forEach((x) => x.removeAttribute('aria-current')); a.setAttribute('aria-current', 'true'); }
      else if (a.getAttribute('aria-current')) a.removeAttribute('aria-current');
    }), { rootMargin: '-45% 0px -50% 0px' });
    byId.forEach((a, id) => { const sec = d.getElementById(id); if (sec) nio.observe(sec); });
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
  /* fase 16: también se revela lo que ya quedó arriba (un salto de ancla o un scroll rápido no deja nada escondido) */
  const io = new IntersectionObserver((es) => es.forEach((e) => {
    if (!e.isIntersecting && e.boundingClientRect.top > 0) return;
    (armed.get(e.target) || [e.target]).forEach((el) => { eager(el); el.classList.add('rv-in'); });
    io.unobserve(e.target);
  }), { rootMargin: '0px 0px -12% 0px', threshold: 0 });
  $$('[data-rv]').forEach((el) => {
    if (el.closest('.hoy') || !below(el)) return;
    el.classList.add('rv-arm');
    const host = el.parentElement;
    if (!armed.has(host)) { armed.set(host, []); io.observe(host); }
    armed.get(host).push(el);
  });
  $$('h2.display, h2.head, .firma').forEach((h) => {
    if (!$('.ln', h) || h.closest('.hoy') || !below(h)) return;
    h.classList.add('h-arm');
    armed.set(h, [h]);
    io.observe(h);
  });

  /* el momento autoral: "la franja se imprime", una vez, al entrar Hoy en Almud.
     Fase 16: el recorte vive en el hijo (.hoy-dia), no en la sección observada, así que la sección siempre "se ve" para el
     observador; y se imprime apenas cualquier parte asoma o si ya quedó arriba (menú → El lugar y luego subir; 1920 bajando
     exactamente una pantalla). Nunca queda en blanco. */
  const hoy = $('#hoy');
  if (hoy && below(hoy)) {
    hoy.classList.add('arm');
    const imprime = () => {
      if (hoy.classList.contains('imprime')) return;
      eager(hoy.querySelector('.hoy-dia:not([hidden])') || hoy);
      hoy.classList.add('imprime');
      hio.disconnect();
    };
    const hio = new IntersectionObserver((es) => {
      const r = es[0].boundingClientRect;
      if (es[0].isIntersecting || r.top < innerHeight * 0.75) imprime();
    }, { rootMargin: '0px 0px -25% 0px', threshold: 0 });
    hio.observe(hoy);
  }
})();
