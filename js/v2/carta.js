/* Almud Bar v2 · carta.js (fase 15): pestañas y grupos de la carta.
   El estado inicial (pestaña, grupo y día, desde el hash) ya lo puso el script del <head> antes de pintar,
   como atributos de <html>; el CSS generado muestra solo lo elegido. Este archivo agrega la semántica de pestañas
   (role tablist/tab/tabpanel, aria-selected, flechas, Inicio/Fin), el historial (atrás/adelante) y la entrada:
   ratón o toque = fundido de 200 ms con 8 px (Emil §6.14); teclado = instantáneo; reduced motion = solo opacidad.
   Sin JS: todas las secciones apiladas, y pestañas y chips son anclas. */
(() => {
  'use strict';
  const d = document, R = d.documentElement;
  const $ = (s, c = d) => c.querySelector(s);
  const $$ = (s, c = d) => [...c.querySelectorAll(s)];
  const tablist = $('.tabs-l');
  const tabs = $$('.tab');
  if (!tablist || !tabs.length) return;

  const reduce = matchMedia('(prefers-reduced-motion: reduce)');
  const css = getComputedStyle(R);
  const ms = (v) => { v = (v || '').trim(); return v.endsWith('ms') ? parseFloat(v) : parseFloat(v) * 1000; };
  const EASE = css.getPropertyValue('--ease-out').trim() || 'ease-out';
  const EASE_FADE = css.getPropertyValue('--ease-hover').trim() || 'ease';
  const D_TAB = ms(css.getPropertyValue('--d-tab')) || 200;
  const D_FADE = ms(css.getPropertyValue('--d-fade-reduced')) || 180;

  const panels = new Map(tabs.map((t) => [t.dataset.tab, d.getElementById(t.dataset.tab)]));
  const chipsOf = new Map($$('.chips').map((c) => [c.dataset.tab, $$('.chip', c)]));
  const tabOfSub = new Map();
  chipsOf.forEach((cs, t) => cs.forEach((c) => tabOfSub.set(c.dataset.sub, t)));
  const subOf = (t) => R.getAttribute('data-sub-' + t);

  /* ── semántica de pestañas (solo con JS: sin JS son anclas) ── */
  tablist.setAttribute('role', 'tablist');
  tabs.forEach((t) => {
    const p = panels.get(t.dataset.tab);
    t.setAttribute('role', 'tab');
    t.setAttribute('aria-controls', p.id);
    p.setAttribute('role', 'tabpanel');
    p.setAttribute('aria-labelledby', t.id);
    p.tabIndex = 0;
  });
  chipsOf.forEach((cs) => {
    cs[0].parentElement.setAttribute('role', 'tablist');
    cs.forEach((c) => {
      const s = d.getElementById(c.dataset.sub);
      c.setAttribute('role', 'tab');
      c.setAttribute('aria-controls', s.id);
      s.setAttribute('role', 'tabpanel');
      s.setAttribute('aria-labelledby', c.id);
      s.tabIndex = 0;
    });
  });

  function paint() {
    const cur = R.dataset.tab;
    tabs.forEach((t) => { const on = t.dataset.tab === cur; t.setAttribute('aria-selected', String(on)); t.tabIndex = on ? 0 : -1; });
    chipsOf.forEach((cs, t) => {
      const s = subOf(t);
      cs.forEach((c) => { const on = c.dataset.sub === s; c.setAttribute('aria-selected', String(on)); c.tabIndex = on ? 0 : -1; });
    });
  }

  /* la barra que se desliza de lado muestra siempre la pestaña o el chip activo (sin mover la página) */
  function reveal(el) {
    const bar = el.parentElement;
    const pad = parseFloat(getComputedStyle(bar).paddingLeft) || 0;
    const l = el.offsetLeft - bar.offsetLeft, r = l + el.offsetWidth;
    if (l < bar.scrollLeft + pad) bar.scrollLeft = l - pad;
    else if (r > bar.scrollLeft + bar.clientWidth - pad) bar.scrollLeft = r - bar.clientWidth + pad;
  }

  /* si ya se había bajado más allá de la barra, el contenido nuevo empieza justo bajo ella: nunca un recorrido largo */
  const docTop = (el) => el.getBoundingClientRect().top + scrollY;
  function align(sentinel, offset) {
    if (!sentinel) return;
    const y = Math.round(docTop(sentinel) - offset);
    if (scrollY > y) scrollTo({ top: y, behavior: 'instant' });
  }

  function enter(el) {
    if (!el.animate) return;
    if (reduce.matches) el.animate([{ opacity: 0 }, { opacity: 1 }], { duration: D_FADE, easing: EASE_FADE });
    else el.animate([{ opacity: 0, transform: 'translateY(8px)' }, { opacity: 1, transform: 'none' }], { duration: D_TAB, easing: EASE });
  }

  /* how: 'pointer' (fundido) · 'key' e 'history' (instantáneo) */
  function show(tab, sub, how) {
    if (!panels.has(tab)) return false;
    const sameTab = R.dataset.tab === tab;
    if (sameTab && (!sub || sub === subOf(tab))) return false;
    R.dataset.tab = tab;
    if (sub) R.setAttribute('data-sub-' + tab, sub);
    paint();
    measure();
    const panel = panels.get(tab);
    const el = sameTab && sub ? d.getElementById(sub) : panel;
    if (how !== 'history') {
      if (sameTab) align($('.chips-sent', panel), parseFloat(css.getPropertyValue('--tabs-h')) || 0);
      else align($('.tabs-sent'), 0);
    }
    if (how === 'pointer') enter(el);
    reveal(tabs.find((t) => t.dataset.tab === tab));
    const cs = chipsOf.get(tab);
    if (cs) reveal(cs.find((c) => c.dataset.sub === subOf(tab)) || cs[0]);
    return true;
  }

  function resolve(h) {
    if (panels.has(h)) return [h, null];
    if (tabOfSub.has(h)) return [tabOfSub.get(h), h];
    return null;
  }

  /* ratón, toque y Enter (un clic de teclado llega con detail 0) */
  function onClick(e) {
    const a = e.currentTarget;
    e.preventDefault();
    const how = e.detail === 0 ? 'key' : 'pointer';
    if (show(a.dataset.tab, a.dataset.sub || null, how)) history.pushState(null, '', '#' + (a.dataset.sub || a.dataset.tab));
  }
  /* flechas, Inicio y Fin: activación automática, sin animación */
  function onKey(list) {
    return (e) => {
      const i = list.indexOf(e.currentTarget);
      let j = -1;
      if (e.key === 'ArrowRight' || e.key === 'ArrowDown') j = (i + 1) % list.length;
      else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') j = (i - 1 + list.length) % list.length;
      else if (e.key === 'Home') j = 0;
      else if (e.key === 'End') j = list.length - 1;
      else if (e.key === ' ') { e.preventDefault(); e.currentTarget.click(); return; }
      if (j < 0) return;
      e.preventDefault();
      const n = list[j];
      n.focus({ preventScroll: true });
      if (show(n.dataset.tab, n.dataset.sub || null, 'key')) history.replaceState(null, '', '#' + (n.dataset.sub || n.dataset.tab));
    };
  }
  tabs.forEach((t) => { t.addEventListener('click', onClick); t.addEventListener('keydown', onKey(tabs)); });
  chipsOf.forEach((cs) => cs.forEach((c) => { c.addEventListener('click', onClick); c.addEventListener('keydown', onKey(cs)); }));

  /* atrás / adelante */
  addEventListener('popstate', () => {
    let h = '';
    try { h = decodeURIComponent(location.hash.slice(1)); } catch (e) { /* hash raro: se ignora */ }
    const r = h ? resolve(h) : [tabs[0].dataset.tab, null];
    if (r) show(r[0], r[1], 'history');
  });

  /* crítica 1: sin entrada al cargar (es la página que el local abre cada vez; el título no espera a ninguna animación) */

  /* el teclado nunca anima: mientras se navega con teclado, pestañas y chips cambian de color al instante */
  d.addEventListener('keydown', () => R.classList.add('kb'), true);
  d.addEventListener('pointerdown', () => R.classList.remove('kb'), true);

  /* bajo 1024 px la barra de pestañas va en varias filas: su alto real (y el de los chips) pasa a las variables
     que usan el sticky de los chips, los scroll-margin y align() */
  const bar = $('.tabs');
  function measure() {
    if (bar) R.style.setProperty('--tabs-h', bar.offsetHeight + 'px');
    const cw = $('.cp:not([hidden]) .chips-w') || [...$$('.chips-w')].find((c) => c.offsetHeight);
    if (cw && cw.offsetHeight) R.style.setProperty('--chips-h', cw.offsetHeight + 'px');
  }
  measure();
  if ('ResizeObserver' in window && bar) new ResizeObserver(measure).observe(bar);
  addEventListener('resize', measure);

  paint();
  reveal(tabs.find((t) => t.dataset.tab === R.dataset.tab) || tabs[0]);
  chipsOf.forEach((cs, t) => reveal(cs.find((c) => c.dataset.sub === subOf(t)) || cs[0]));
})();
