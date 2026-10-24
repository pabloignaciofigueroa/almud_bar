/* Almud Bar · v3 · carta.js: pestañas (una sección a la vez), subgrupos filtrables, idioma y el loop de Peter.
   El estado inicial (pestaña desde el hash) lo pone el script del <head> antes de pintar. Sin JS: todo apilado. */
(() => {
  'use strict';
  const d = document, R = d.documentElement;
  const $ = (s, c = d) => c.querySelector(s);
  const $$ = (s, c = d) => [...c.querySelectorAll(s)];

  /* video: póster y fuente cuando está a ≤1,5 pantallas (solo carga; nunca se pausa). Movimiento reducido: solo póster */
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  function attach(v) {
    if (v.dataset.on) return; v.dataset.on = '1';
    if (v.dataset.poster) v.poster = v.dataset.poster;
    if (reduce) { v.removeAttribute('autoplay'); return; }
    v.preload = 'auto';
    v.insertAdjacentHTML('beforeend', '<source src="' + v.dataset.webm + '" type="video/webm"><source src="' + v.dataset.mp4 + '" type="video/mp4">');
    v.load(); const p = v.play(); if (p && p.catch) p.catch(() => {});
  }
  const vids = $$('video.v');
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { io.unobserve(e.target); attach(e.target); } }), { rootMargin: '150% 0px' });
    vids.forEach(v => io.observe(v));
  } else vids.forEach(attach);

  /* idioma */
  const ATTR = [['data-alt-en', 'alt'], ['data-aria-en', 'aria-label']];
  function setLang(lang, save) {
    R.lang = lang;
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
  }
  if (R.lang === 'en') setLang('en', false);
  $('[data-lang]').addEventListener('click', () => { setLang(R.lang === 'en' ? 'es' : 'en', true); if (typeof paint === 'function') { tabsH(); paint(); } });

  /* pestañas */
  const tabs = $$('.tab'), list = $('.tabs__l');
  const ids = tabs.map(t => t.dataset.tab);
  list.setAttribute('role', 'tablist');
  tabs.forEach(t => { t.setAttribute('role', 'tab'); t.setAttribute('aria-controls', t.dataset.tab); });
  $$('.panel').forEach(p => p.setAttribute('role', 'tabpanel'));
  const sent = $('.tabs-sent');
  const nav = () => parseFloat(getComputedStyle(R).getPropertyValue('--nav')) || 60;

  function paint() {
    const cur = R.dataset.tab;
    const ch = $('#' + cur + ' .chips');
    R.style.setProperty('--chips-h', (ch ? ch.offsetHeight : 0) + 'px');
    tabs.forEach(t => { const on = t.dataset.tab === cur; t.setAttribute('aria-selected', on); t.tabIndex = on ? 0 : -1; if (on) reveal(t); });
    $$('.chips').forEach(cs => {
      const tid = cs.dataset.chips, chips = $$('.chip', cs);
      const s = R.getAttribute('data-sub-' + tid) || chips[0].dataset.sub;
      chips.forEach(c => { const on = c.dataset.sub === s; c.setAttribute('aria-current', on ? 'true' : 'false'); if (on && tid === cur) reveal(c); });
    });
  }
  function reveal(el) {
    const bar = el.parentElement;
    if (bar.scrollWidth <= bar.clientWidth) return;
    const l = el.offsetLeft - bar.offsetLeft, r = l + el.offsetWidth;
    if (l < bar.scrollLeft + 16) bar.scrollLeft = l - 16;
    else if (r > bar.scrollLeft + bar.clientWidth - 72) bar.scrollLeft = r - bar.clientWidth + 72;
  }
  const tabsBar = $('.tabs');
  const tabsH = () => R.style.setProperty('--tabs-h', tabsBar.offsetHeight + 'px');
  tabsH(); addEventListener('resize', tabsH);
  function top() {
    const y = sent.getBoundingClientRect().top + scrollY - nav();
    if (scrollY > y) scrollTo({ top: y, behavior: 'instant' });
  }
  function enter(el) {
    if (el.animate && !matchMedia('(prefers-reduced-motion: reduce)').matches)
      el.animate([{ opacity: 0, transform: 'translateY(10px)' }, { opacity: 1, transform: 'none' }], { duration: 380, easing: 'cubic-bezier(.16,1,.3,1)' });
  }
  function go(hash, how) {
    if (ids.includes(hash)) {
      if (R.dataset.tab === hash) return;
      R.dataset.tab = hash; paint(); filas.forEach(bordes); if (how) { top(); enter($('#' + hash)); }
      return true;
    }
    const sub = hash && $('.sub[data-sub="' + CSS.escape(hash) + '"]');
    if (sub) {
      const tid = sub.closest('.panel').id;
      R.dataset.tab = tid; R.setAttribute('data-sub-' + tid, hash); paint();
      if (how) { top(); enter(sub); } else requestAnimationFrame(() => sub.scrollIntoView());
      return true;
    }
  }
  tabs.forEach(t => t.addEventListener('click', e => { e.preventDefault(); if (go(t.dataset.tab, 'click')) history.replaceState(null, '', '#' + t.dataset.tab); }));
  $$('.chip').forEach(c => c.addEventListener('click', e => { e.preventDefault(); go(c.dataset.sub, 'click'); history.replaceState(null, '', '#' + c.dataset.sub); }));
  list.addEventListener('keydown', e => {
    const i = ids.indexOf(R.dataset.tab);
    const j = e.key === 'ArrowRight' ? i + 1 : e.key === 'ArrowLeft' ? i - 1 : e.key === 'Home' ? 0 : e.key === 'End' ? ids.length - 1 : -2;
    if (j === -2) return;
    e.preventDefault(); const k = (j + ids.length) % ids.length; go(ids[k]); tabs[k].focus();
  });
  /* v4 fase 9 · fundido solo donde queda fila por deslizar */
  const filas = [list, ...$$('.chips__in')];
  // v4 fase 10: oculta la pestaña (o chip) que queda a medias en cada borde; la flecha del contenedor dice que hay más
  function bordes(f) {
    const m = f.scrollWidth - f.clientWidth, L = f.scrollLeft > 2, D = m > 2 && f.scrollLeft < m - 2;
    f.classList.toggle('mas-i', L); f.classList.toggle('mas-d', D);
    const box = f.getBoundingClientRect(), its = [...f.children].map(c => c.getBoundingClientRect()).filter(r => r.width);
    const enteras = its.filter(r => r.left >= box.left - .5 && r.right <= box.right - (D ? 30 : 0) + .5);   // 30 px: lugar de la flecha
    const mi = L && enteras.length ? Math.max(0, enteras[0].left - box.left - 3) : 0;
    const md = D && enteras.length ? Math.max(0, box.right - enteras[enteras.length - 1].right - 3) : 0;
    f.style.setProperty('--mi', mi + 'px'); f.style.setProperty('--md', md + 'px');
    const c = f.closest('.tabs, .chips'); if (c) { c.classList.toggle('hay-d', D); c.classList.toggle('hay-i', L); }
  }
  filas.forEach(f => { f.addEventListener('scroll', () => bordes(f), { passive: true }); bordes(f); });
  addEventListener('resize', () => filas.forEach(bordes));
  if (d.fonts && d.fonts.ready) d.fonts.ready.then(() => filas.forEach(bordes));   // v4 fase 10: re-medir con la fuente real
  addEventListener('load', () => filas.forEach(bordes));
  // v4 fase 16: con #casa, #comilona… (enlaces de la home) se abre esa pestaña y la página queda ARRIBA, con «LA CARTA» entera
  // (el navegador saltaba al panel y dejaba el título cortado bajo la nav)
  if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
  const h0 = location.hash.slice(1);
  if (ids.includes(h0)) { const up = () => { if (scrollY > 0 && !tocado) scrollTo(0, 0); }; let tocado = false;
    ['wheel', 'touchstart', 'keydown'].forEach(ev => addEventListener(ev, () => { tocado = true; }, { once: true, passive: true }));
    requestAnimationFrame(up); addEventListener('load', () => { up(); setTimeout(up, 60); }); }
  addEventListener('hashchange', () => { const h = location.hash.slice(1); go(h);
    if (ids.includes(h)) { const y = Math.max(0, sent.getBoundingClientRect().top + scrollY - nav()); scrollTo({ top: Math.min(scrollY, y), behavior: 'instant' }); } });   // pestaña: la barra a la vista, sin saltar al panel
  go(location.hash.slice(1));
  paint();
  filas.forEach(bordes);
})();
