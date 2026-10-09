/* Almud Bar · main.js */
(() => {
  'use strict';
  const d = document, root = d.documentElement;
  root.classList.add('js');
  if (typeof window.gsap !== 'undefined' && typeof window.ScrollTrigger !== 'undefined') root.classList.add('has-gsap');
  const $ = (s, c = d) => c.querySelector(s);
  const $$ = (s, c = d) => [...c.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)');
  const fine = matchMedia('(hover: hover) and (pointer: fine)');
  const mobileQ = matchMedia('(max-width: 760px)');
  const hasGsap = () => typeof window.gsap !== 'undefined' && typeof window.ScrollTrigger !== 'undefined';

  /* ───────── Idioma ───────── */
  const I18N_ATTRS = [['data-alt-en', 'alt'], ['data-aria-en', 'aria-label'], ['data-title-en', 'title']];
  function setLang(lang, save) {
    root.lang = lang;
    $$('[data-en]').forEach(el => {
      if (el.dataset.es === undefined) el.dataset.es = el.textContent;
      el.textContent = lang === 'en' ? el.dataset.en : el.dataset.es;
    });
    I18N_ATTRS.forEach(([src, attr]) => $$('[' + src + ']').forEach(el => {
      const k = 'es' + attr.replace(/[^a-z]/gi, '');
      if (el.dataset[k] === undefined) el.dataset[k] = el.getAttribute(attr) || '';
      el.setAttribute(attr, lang === 'en' ? el.getAttribute(src) : el.dataset[k]);
    }));
    const md = $('meta[name="description"]');
    if (md) { if (!md.dataset.es) md.dataset.es = md.content; md.content = lang === 'en' ? md.dataset.metaEn : md.dataset.es; }
    if (save) { try { localStorage.setItem('almud-lang', lang); } catch (e) {} }
    if (window.__swiper && window.__swiper.a11y) {
      $$('.reviews__swiper .swiper-slide').forEach((s, i, a) => s.setAttribute('aria-label', (i + 1) + ' / ' + a.length));
    }
    d.dispatchEvent(new CustomEvent('almud:lang'));
  }
  let saved = 'es'; try { saved = localStorage.getItem('almud-lang') || 'es'; } catch (e) {}
  if (saved === 'en') setLang('en', false);
  $('.lang').addEventListener('click', () => { setLang(root.lang === 'en' ? 'es' : 'en', true); if (hasGsap()) ScrollTrigger.refresh(); });

  /* ───────── Videos ───────── */
  function setVideo(v, base, poster) {
    if (v.dataset.loaded === base) return;
    v.dataset.loaded = base;
    if (poster) v.poster = poster;
    v.innerHTML = '<source src="' + base + '.webm" type="video/webm"><source src="' + base + '.mp4" type="video/mp4">';
    v.load();
  }
  const heroV = $('.hero__video');
  function heroSource() {
    const m = mobileQ.matches;
    setVideo(heroV, m ? heroV.dataset.srcMobile : heroV.dataset.srcDesktop, m ? heroV.dataset.posterMobile : 'assets/video/hero-poster.jpg');
  }
  heroSource();
  const lazyVideos = $$('video[data-src]:not(.story__video)');
  const vio = new IntersectionObserver(es => es.forEach(e => {
    const v = e.target;
    if (e.isIntersecting) {
      setVideo(v, v.dataset.src, v.dataset.poster);
      if (!reduce.matches) v.play().catch(() => {});
    } else if (!v.paused) v.pause();
  }), { rootMargin: '25% 0px' });
  lazyVideos.forEach(v => vio.observe(v));
  /* la historia: poster cerca, video al entrar (o sin GSAP, al verse) */
  new IntersectionObserver((es, o) => { if (es[0].isIntersecting) { storyVid().poster = storyVid().dataset.poster; if (!root.classList.contains('has-gsap')) setVideo(storyVid(), storyVid().dataset.src, storyVid().dataset.poster); o.disconnect(); } }, { rootMargin: '25% 0px' }).observe($('.story__video'));
  const heroIO = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting && !reduce.matches && root.classList.contains('is-ready')) heroV.play().catch(() => {});
    else if (!e.isIntersecting) heroV.pause();
  }));
  heroIO.observe(heroV);

  /* Sonido de la historia */
  const storyV = $('.story__video'), soundBtn = $('.sound');
  function storyVid() { return storyV; }
  soundBtn.addEventListener('click', () => {
    const on = soundBtn.getAttribute('aria-pressed') !== 'true';
    setVideo(storyV, storyV.dataset.src, storyV.dataset.poster);
    storyV.muted = !on;
    if (on) { storyV.currentTime = 0; storyV.loop = false; storyV.play().catch(() => {}); }
    else storyV.loop = true;
    soundBtn.setAttribute('aria-pressed', String(on));
  });
  storyV.addEventListener('ended', () => { storyV.muted = true; storyV.loop = true; soundBtn.setAttribute('aria-pressed', 'false'); storyV.play().catch(() => {}); });

  /* ───────── Carta ───────── */
  const tabs = $$('.tab');
  function selectTab(t, focus) {
    tabs.forEach(x => { const on = x === t; x.setAttribute('aria-selected', on); x.tabIndex = on ? 0 : -1; $('#' + x.getAttribute('aria-controls')).hidden = !on; });
    if (focus) t.focus();
    const panel = $('#' + t.getAttribute('aria-controls'));
    const act = $('.dish.is-active', panel) || $('.dish', panel);
    if (act) activate(act, false);
    if (hasGsap()) { ScrollTrigger.refresh(); gsap.fromTo(panel, { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: .7, ease: 'expo.out' }); }
  }
  tabs.forEach((t, i) => {
    t.addEventListener('click', () => selectTab(t));
    t.addEventListener('keydown', e => {
      const k = e.key; let j = null;
      if (k === 'ArrowRight') j = (i + 1) % tabs.length; else if (k === 'ArrowLeft') j = (i - 1 + tabs.length) % tabs.length;
      else if (k === 'Home') j = 0; else if (k === 'End') j = tabs.length - 1;
      if (j !== null) { e.preventDefault(); selectTab(tabs[j], true); }
    });
  });
  function activate(li, anim = true) {
    const list = li.closest('.carta');
    $$('.dish', list).forEach(x => { const on = x === li; x.classList.toggle('is-active', on); $('.dish__btn', x).setAttribute('aria-expanded', on); });
    const show = $('.carta__show', list); if (!show) return;
    const media = $('.dish__media', li).cloneNode(true);
    $$('img', media).forEach(im => { im.loading = 'eager'; im.removeAttribute('data-img'); });
    const name = $('.dish__n', li).textContent, desc = $('.dish__d', li), price = $('.dish__p', li).textContent;
    show.innerHTML = '';
    const wrap = d.createElement('div'); wrap.className = 'show';
    const m = d.createElement('div'); m.className = 'show__media'; [...media.childNodes].forEach(n => m.appendChild(n));
    const h = d.createElement('p'); h.className = 'show__n'; h.textContent = name; h.lang = 'es';
    const p = d.createElement('p'); p.className = 'show__p'; p.textContent = price;
    wrap.append(m, h); if (desc) { const dd = desc.cloneNode(true); dd.className = 'show__d'; wrap.append(dd); } wrap.append(p);
    show.append(wrap);
    if (anim && hasGsap() && !reduce.matches) {
      gsap.fromTo(m, { clipPath: 'inset(100% 0 0 0)' }, { clipPath: 'inset(0% 0 0 0)', duration: .9, ease: 'expo.out' });
      gsap.fromTo([h, p, wrap.querySelector('.show__d')].filter(Boolean), { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: .8, stagger: .05, ease: 'expo.out' });
    }
  }
  $$('.dish').forEach(li => $('.dish__btn', li).addEventListener('click', () => {
    if (li.classList.contains('is-active') && mobileQ.matches) { li.classList.remove('is-active'); $('.dish__btn', li).setAttribute('aria-expanded', 'false'); }
    else activate(li);
    if (hasGsap()) setTimeout(() => ScrollTrigger.refresh(), 600);
  }));
  $$('.carta').forEach(c => { const f = $('.dish', c); if (f) activate(f, false); });
  /* promo de hoy */
  const today = new Date().getDay();
  $$('.promo').forEach(p => p.classList.toggle('is-today', +p.dataset.day === today));

  /* vistazo de foto al pasar por un plato */
  const peek = $('.peek'), peekImg = $('img', peek);
  if (fine.matches) {
    $$('.dish.has-img .dish__btn').forEach(b => {
      b.addEventListener('pointerenter', () => {
        const im = $('img', b.parentElement); if (!im || !hasGsap() || b.parentElement.classList.contains('is-active')) return;
        peekImg.src = im.currentSrc || im.src;
        gsap.to(peek, { opacity: 1, scale: 1, duration: .5, ease: 'expo.out' });
      });
      b.addEventListener('pointerleave', () => hasGsap() && gsap.to(peek, { opacity: 0, scale: .6, duration: .4, ease: 'expo.out' }));
    });
  }

  /* ───────── Mapa diferido ───────── */
  $('.map__btn').addEventListener('click', e => {
    const m = e.currentTarget.closest('.map');
    const f = d.createElement('iframe');
    f.src = m.dataset.map; f.title = root.lang === 'en' ? 'Map: Almud Bar, Serrano 325, Castro' : 'Mapa: Almud Bar, Serrano 325, Castro';
    f.loading = 'lazy'; f.referrerPolicy = 'no-referrer-when-downgrade';
    m.appendChild(f); m.classList.add('is-live'); f.focus();
  });

  /* ───────── Menú ───────── */
  const menu = $('#menu'), burger = $('.burger'), menuClose = $('.menu__close');
  const outside = [$('main'), $('.top'), $('.foot')];
  let lastFocus = null;
  function openMenu() {
    lastFocus = d.activeElement;
    menu.hidden = false; burger.setAttribute('aria-expanded', 'true');
    outside.forEach(el => el.inert = true);
    if (window.__lenis) window.__lenis.stop();
    if (hasGsap()) {
      gsap.killTweensOf([menu, '.menu__nav a']);
      gsap.fromTo(menu, { clipPath: 'inset(0 0 100% 0)' }, { clipPath: 'inset(0 0 0% 0)', duration: reduce.matches ? 0 : .9, ease: 'expo.inOut' });
      gsap.fromTo('.menu__nav a', { yPercent: 110 }, { yPercent: 0, duration: reduce.matches ? 0 : 1, ease: 'expo.out', stagger: .05, delay: .25 });
    } else menu.style.clipPath = 'none';
    menuClose.focus();
    showMenuImg('historia');
  }
  function closeMenu(cb) {
    burger.setAttribute('aria-expanded', 'false');
    outside.forEach(el => el.inert = false);
    const done = () => { menu.hidden = true; if (window.__lenis) window.__lenis.start(); if (cb) cb(); else if (lastFocus) lastFocus.focus(); };
    if (hasGsap() && !reduce.matches) { gsap.killTweensOf([menu, '.menu__nav a']); gsap.to(menu, { clipPath: 'inset(100% 0 0 0)', duration: .7, ease: 'expo.inOut', onComplete: done }); }
    else done();
  }
  function showMenuImg(k) { $$('.menu__media img').forEach(i => i.classList.toggle('is-on', i.dataset.menu === k)); }
  burger.addEventListener('click', openMenu);
  menuClose.addEventListener('click', () => closeMenu());
  d.addEventListener('keydown', e => { if (e.key === 'Escape' && !menu.hidden && burger.getAttribute('aria-expanded') === 'true') { e.preventDefault(); closeMenu(); } });
  menu.addEventListener('keydown', e => {
    if (e.key === 'Tab') {
      const f = $$('button, a[href]', menu).filter(x => x.offsetParent !== null);
      const first = f[0], last = f[f.length - 1];
      if (e.shiftKey && d.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && d.activeElement === last) { e.preventDefault(); first.focus(); }
    }
  });
  $$('.menu__nav a').forEach(a => {
    a.addEventListener('pointerenter', () => showMenuImg(a.dataset.k));
    a.addEventListener('focus', () => showMenuImg(a.dataset.k));
    a.addEventListener('click', e => {
      e.preventDefault(); const target = $(a.getAttribute('href'));
      closeMenu(() => goTo(target));
    });
  });
  function goTo(target) {
    if (!target) return;
    if (window.__lenis) window.__lenis.scrollTo(target, { duration: 1.4 }); else target.scrollIntoView({ behavior: reduce.matches ? 'auto' : 'smooth' });
    target.setAttribute('tabindex', '-1'); target.focus({ preventScroll: true });
  }
  $$('a[href^="#"]').forEach(a => { if (a.closest('.menu')) return; a.addEventListener('click', e => { const t = $(a.getAttribute('href')); if (t) { e.preventDefault(); goTo(t); } }); });
  $('.skip').addEventListener('click', e => { e.preventDefault(); const m = $('#contenido'); m.focus(); goTo(m); });

  /* ───────── Arrastrar (tendedero) ───────── */
  const line = $('.clothesline__items');
  let dragging = false, sx = 0, sl = 0, moved = 0;
  line.addEventListener('pointerdown', e => { if (e.pointerType !== 'mouse') return; dragging = true; moved = 0; sx = e.clientX; sl = line.scrollLeft; line.setPointerCapture(e.pointerId); line.style.cursor = 'grabbing'; });
  line.addEventListener('pointermove', e => { if (!dragging) return; const dx = e.clientX - sx; moved = Math.abs(dx); line.scrollLeft = sl - dx; });
  const endDrag = () => { dragging = false; line.style.cursor = ''; };
  line.addEventListener('pointerup', endDrag); line.addEventListener('pointercancel', endDrag);

  /* ───────── Reseñas: Swiper diferido ───────── */
  const revs = $('.reviews__swiper');
  const loadCSS = href => new Promise(r => { const l = d.createElement('link'); l.rel = 'stylesheet'; l.href = href; l.onload = r; l.onerror = r; d.head.appendChild(l); });
  const loadJS = src => new Promise((r, j) => { const s = d.createElement('script'); s.src = src; s.onload = r; s.onerror = j; d.body.appendChild(s); });
  const rio = new IntersectionObserver(async es => {
    if (!es.some(e => e.isIntersecting)) return; rio.disconnect();
    try {
      await Promise.all([loadCSS('vendor/swiper-bundle.min.css'), loadJS('vendor/swiper-bundle.min.js')]);
      window.__swiper = new Swiper(revs, {
        slidesPerView: 'auto', spaceBetween: 20, grabCursor: true, speed: 800, keyboard: { enabled: true },
        navigation: { prevEl: '.rnav--prev', nextEl: '.rnav--next' },
        a11y: { enabled: true, prevSlideMessage: root.lang === 'en' ? 'Previous review' : 'Reseña anterior', nextSlideMessage: root.lang === 'en' ? 'Next review' : 'Reseña siguiente', slideLabelMessage: '{{index}} / {{slidesLength}}' }
      });
    } catch (e) { revs.style.overflowX = 'auto'; }
  }, { rootMargin: '80% 0px' });
  rio.observe(revs);
  d.addEventListener('almud:lang', () => {
    const s = window.__swiper; if (!s || !s.params.a11y) return;
    s.params.a11y.prevSlideMessage = root.lang === 'en' ? 'Previous review' : 'Reseña anterior';
    s.params.a11y.nextSlideMessage = root.lang === 'en' ? 'Next review' : 'Reseña siguiente';
    $('.rnav--prev').setAttribute('aria-label', s.params.a11y.prevSlideMessage);
    $('.rnav--next').setAttribute('aria-label', s.params.a11y.nextSlideMessage);
  });
  d.addEventListener('almud:lang', () => { const b = $('.reviews__big'); b.textContent = root.lang === 'en' ? b.textContent.replace(',', '.') : b.textContent.replace('.', ','); });

  /* ───────── Cursor "Arrastrar" ───────── */
  const cursor = $('.cursor');
  function cursorFor(el) {
    if (!fine.matches) return;
    el.addEventListener('pointerenter', () => hasGsap() && gsap.to(cursor, { scale: 1, opacity: 1, duration: .5, ease: 'expo.out' }));
    el.addEventListener('pointerleave', () => hasGsap() && gsap.to(cursor, { scale: 0, opacity: 0, duration: .4, ease: 'expo.out' }));
  }
  cursorFor(revs); cursorFor(line);

  /* ───────── Arranque con fuentes ───────── */
  const fontsReady = Promise.race([
    Promise.allSettled(['400 1em "Six Caps"', '100 1em "Big Shoulders"', '300 1em Oswald', '400 1em Oswald', '600 1em Caveat'].map(f => d.fonts.load(f))),
    new Promise(r => setTimeout(r, 2500))
  ]);
  const libsReady = new Promise(r => { if (d.readyState === 'complete' || hasGsap()) r(); else window.addEventListener('DOMContentLoaded', r); });

  Promise.all([fontsReady, libsReady]).then(() => {
    if (!hasGsap()) { finish(); return; }
    start();
  });

  function finish() {
    root.classList.add('is-ready'); d.body.classList.remove('is-loading');
    const l = $('.loader'); if (l) l.remove();
    if (!reduce.matches) heroV.play().catch(() => {});
  }

  function start() {
    gsap.registerPlugin(ScrollTrigger);
    gsap.defaults({ ease: 'expo.out', duration: 1 });

    /* Lenis */
    if (!reduce.matches && typeof window.Lenis !== 'undefined') {
      const lenis = new Lenis({ duration: 1.1, easing: t => Math.min(1, 1.001 - Math.pow(2, -10 * t)), smoothWheel: true });
      window.__lenis = lenis;
      lenis.on('scroll', ScrollTrigger.update);
      gsap.ticker.add(t => lenis.raf(t * 1000));
      gsap.ticker.lagSmoothing(0);
    }
    const vel = () => (window.__lenis ? window.__lenis.velocity : 0) || 0;

    /* cabecera que se esconde */
    let lastY = 0, savedAnchor = null; const top = $('.top');
    const secsA = $$('main > section, main > div, .foot');
    const saveAnchor = () => { const c = secsA.find(x => x.getBoundingClientRect().bottom > innerHeight * .3); if (c) { const r = c.getBoundingClientRect(); savedAnchor = { el: c, f: -r.top / Math.max(1, r.height) }; } };
    ScrollTrigger.create({ start: 0, end: 'max', onUpdate: s => { const y = s.scroll(); top.classList.toggle('is-hidden', y > lastY && y > 400); lastY = y; saveAnchor(); } });

    ['.menu-sec'].forEach(sel => ScrollTrigger.create({ trigger: sel, start: 'top 40px', end: 'bottom 40px', toggleClass: { targets: top, className: 'on-light' } }));

    /* Cargador + entrada del hero */
    const intro = gsap.timeline({ onComplete: finish });
    let seen = false; try { seen = sessionStorage.getItem('almud-seen') === '1'; sessionStorage.setItem('almud-seen', '1'); } catch (e) {}
    if (!reduce.matches) {
      intro.to('.lw', { opacity: 1, y: 0, duration: seen ? .25 : .45, stagger: seen ? .06 : .14, ease: 'back.out(2)' })
        .to('.loader', { clipPath: 'inset(0 0 100% 0)', duration: .8, ease: 'expo.inOut' }, seen ? '+=.05' : '+=.15')
        .from('.hero__almud .ch>span, .hero__bar .ch>span', { yPercent: 105, duration: 1.2, stagger: .05 }, '-=.45')
        .from('.hero__iso', { rotate: -25, scale: .4, opacity: 0, duration: 1.3, ease: 'elastic.out(1,.6)' }, '-=1')
        .from('.hero__copy .line>span', { yPercent: 110, duration: 1, stagger: .08 }, '-=1.05')
        .from('.hero__ctas .btn', { y: 30, opacity: 0, stagger: .08 }, '-=.8');
      // los nodos de .ch necesitan un hijo para el revelado: se anima el propio span dentro del overflow
    } else intro.set({}, {});

    const mm = gsap.matchMedia();
    mm.add({ desk: '(min-width: 760.02px)', mob: '(max-width: 760px)', motion: '(prefers-reduced-motion: no-preference)' }, ctx => {
      const { desk, motion } = ctx.conditions;
      if (!motion) return;

      /* hero parallax */
      gsap.to('.hero__media', { yPercent: 10, ease: 'none', scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true } });
      gsap.to('.hero__inner', { yPercent: -18, opacity: .2, ease: 'none', scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true } });

      /* léxico: marquesina con impulso del scroll */
      const track = $('.lexicon__track'), list = $('.lexicon__list');
      if (!track.dataset.cloned) { const c = list.cloneNode(true); c.setAttribute('aria-hidden', 'true'); track.appendChild(c); const c2 = list.cloneNode(true); c2.setAttribute('aria-hidden', 'true'); track.appendChild(c2); track.dataset.cloned = '1'; }
      let x = 0; const tick = () => { const w = list.offsetWidth || 1; x -= .5 + Math.min(Math.abs(vel()) * .12, 12); if (x <= -w) x += w; track.style.transform = 'translate3d(' + x + 'px,0,0)'; };
      gsap.ticker.add(tick);

      /* revelados de líneas */
      $$('.h-display .line>span, .foot__besi .line>span').forEach(s => {
        gsap.from(s, { yPercent: 108, duration: 1.2, scrollTrigger: { trigger: s.closest('.line'), start: 'top 88%', once: true } });
      });

      /* flecos que se mecen */
      $$('.fringe').forEach(f => {
        const q = gsap.quickTo(f, 'skewX', { duration: .8, ease: 'power3.out' });
        const t2 = () => q(gsap.utils.clamp(-14, 14, -vel() * .35));
        gsap.ticker.add(t2); ctx.add(() => () => gsap.ticker.remove(t2));
      });

      /* HISTORIA: el almud se abre */
      const stage = $('.story__stage'), win = $('.story__window'), iso = $('.story__iso');
      const lines = $$('.story__lines li');
      const P = [[288, 0], [614, 215], [266, 496], [0, 180]];
      const R = [[0, 0], [100, 0], [100, 100], [0, 100]];
      let rhombus = [[50, 18], [74, 39], [50, 60], [26, 39]];
      const measure = () => {
        const sr = stage.getBoundingClientRect(), ir = iso.getBoundingClientRect();
        rhombus = P.map(([px, py]) => [((ir.left - sr.left) + px / 614 * ir.width) / sr.width * 100, ((ir.top - sr.top) + py / 897 * ir.height) / sr.height * 100]);
      };
      const o = { t: 0 };
      const draw = () => { const t = o.t; win.style.clipPath = 'polygon(' + rhombus.map((p, i) => (p[0] + (R[i][0] - p[0]) * t).toFixed(2) + '% ' + (p[1] + (R[i][1] - p[1]) * t).toFixed(2) + '%').join(',') + ')'; };
      const tl = gsap.timeline({ scrollTrigger: { trigger: '.story', start: 'top top', end: 'bottom bottom', scrub: .6, invalidateOnRefresh: true, onRefreshInit: measure, onRefresh: () => { measure(); draw(); },
        onEnter: () => { setVideo(storyV, storyV.dataset.src, storyV.dataset.poster); storyV.play().catch(() => {}); },
        onEnterBack: () => storyV.play().catch(() => {}), onLeave: () => storyV.pause(), onLeaveBack: () => storyV.pause() } });
      measure(); draw();
      tl.to('.story__note', { opacity: 0, y: 20, duration: .05 }, 0)
        .to(o, { t: 1, duration: .22, ease: 'power2.inOut', onUpdate: draw }, .02)
        .to(iso, { scale: 3.2, opacity: 0, duration: .2, ease: 'power2.in' }, .02)
        .fromTo('.story__video', { scale: 1.25 }, { scale: 1, duration: .3, ease: 'none' }, .02)
        .to('.story__veil', { opacity: 1, duration: .1 }, .18)
        .to('.story__ui', { opacity: 1, duration: .05 }, .2)
        .to('.story__progress i', { scaleX: 1, ease: 'none', duration: .98 }, 0);
      const seg = .76 / lines.length;
      lines.forEach((li, i) => {
        const t0 = .22 + i * seg;
        tl.fromTo(li, { opacity: 0, yPercent: 30 }, { opacity: 1, yPercent: 0, duration: seg * .35, ease: 'power3.out' }, t0);
        if (i < lines.length - 1) tl.to(li, { opacity: 0, yPercent: -30, duration: seg * .3, ease: 'power2.in' }, t0 + seg * .7);
      });
      ctx.add(() => () => { win.style.clipPath = ''; });

      /* MANIFIESTO palabra por palabra */
      const mt = $('.manifesto__text');
      if (!mt.dataset.split) {
        const cols = ['var(--barra)', 'var(--pisco)', 'var(--cinta)', 'var(--cielo)', 'var(--violeta)', 'var(--brasa)'];
        mt.innerHTML = mt.textContent.split(' ').map((w, i) => '<span class="w"' + (i % 3 === 1 ? ' style="color:' + cols[(i / 3 | 0) % cols.length] + '"' : '') + '>' + w + '</span>').join(' ');
        mt.dataset.split = '1';
      }
      gsap.to('.manifesto__text .w', { opacity: 1, stagger: .1, ease: 'none', scrollTrigger: { trigger: '.manifesto', start: 'top 75%', end: 'bottom 70%', scrub: true } });
      gsap.from('.manifesto__sign', { rotate: -12, opacity: 0, scale: .7, duration: 1.2, ease: 'elastic.out(1,.6)', scrollTrigger: { trigger: '.manifesto__sign', start: 'top 90%', once: true } });

      /* RINCONES: galería horizontal (sticky, sin pin) */
      if (desk) {
        const sec = $('.nooks'), trk = $('.nooks__track');
        const dist = () => Math.max(0, trk.scrollWidth - innerWidth);
        const setH = () => { sec.style.height = (dist() + innerHeight) + 'px'; };
        setH();
        ScrollTrigger.addEventListener('refreshInit', setH);
        gsap.to(trk, { x: () => -dist(), ease: 'none', scrollTrigger: { trigger: sec, start: 'top top', end: 'bottom bottom', scrub: .5, invalidateOnRefresh: true } });
        gsap.to('.nooks__bar i', { scaleX: 1, ease: 'none', scrollTrigger: { trigger: sec, start: 'top top', end: 'bottom bottom', scrub: true } });
        $$('.nook__media img, .nook__media video').forEach(m => gsap.fromTo(m, { xPercent: -3 }, { xPercent: 3, ease: 'none', scrollTrigger: { trigger: sec, start: 'top top', end: 'bottom bottom', scrub: true } }));
        ctx.add(() => () => { ScrollTrigger.removeEventListener('refreshInit', setH); sec.style.height = ''; });
      }

      /* masas a distinta velocidad */
      $$('[data-speed]').forEach(el => {
        const s = parseFloat(el.dataset.speed);
        gsap.fromTo(el, { y: () => -s * innerHeight * .6 }, { y: () => s * innerHeight * .6, ease: 'none', scrollTrigger: { trigger: el.closest('section'), start: 'top bottom', end: 'bottom top', scrub: true, invalidateOnRefresh: true } });
      });
      gsap.from('.food__copy', { scale: .85, opacity: 0, duration: 1.4, scrollTrigger: { trigger: '.food', start: 'top 60%', once: true } });

      /* tablero: alfileres caen */
      $$('.pin').forEach((p, i) => gsap.from(p, { scale: .8, opacity: 0, duration: 1.2, scrollTrigger: { trigger: p, start: 'top 92%', once: true } }));

      /* tendedero: balanceo con la velocidad */
      const pols = $$('.polaroid');
      const swing = () => { const v = gsap.utils.clamp(-10, 10, vel() * .25); pols.forEach((p, i) => gsap.to(p, { '--sw': (v * (i % 2 ? 1 : -1)).toFixed(2) + 'deg', duration: .9, ease: 'power3.out', overwrite: 'auto' })); };
      let lastV = 0; const swingTick = () => { const v = Math.round(vel()); if (v !== lastV) { lastV = v; swing(); } };
      gsap.ticker.add(swingTick);
      gsap.from('.polaroid', { y: -60, opacity: 0, stagger: .08, duration: 1.2, ease: 'back.out(1.6)', scrollTrigger: { trigger: '.clothesline', start: 'top 85%', once: true } });

      /* reseñas: número que sube */
      const big = $('.reviews__big');
      ScrollTrigger.create({ trigger: '.reviews', start: 'top 70%', once: true, onEnter: () => { const n = { v: 0 }; gsap.to(n, { v: 4.6, duration: 1.6, ease: 'expo.out', onUpdate: () => { big.textContent = n.v.toFixed(1).replace('.', root.lang === 'en' ? '.' : ','); } }); } });

      /* pie */
      gsap.from('.foot__logo', { yPercent: 40, opacity: 0, duration: 1.4, scrollTrigger: { trigger: '.foot__logo', start: 'top 95%', once: true } });

      return () => { gsap.ticker.remove(tick); gsap.ticker.remove(swingTick); track.style.transform = ''; };
    });

    /* botones magnéticos */
    if (fine.matches && !reduce.matches) {
      $$('.magnetic').forEach(b => {
        const qx = gsap.quickTo(b, 'x', { duration: .6, ease: 'expo.out' }), qy = gsap.quickTo(b, 'y', { duration: .6, ease: 'expo.out' });
        b.addEventListener('pointermove', e => { const r = b.getBoundingClientRect(); qx((e.clientX - r.left - r.width / 2) * .3); qy((e.clientY - r.top - r.height / 2) * .35); });
        b.addEventListener('pointerleave', () => { qx(0); qy(0); });
      });
      const cx = gsap.quickTo(cursor, 'x', { duration: .45, ease: 'expo.out' }), cy = gsap.quickTo(cursor, 'y', { duration: .45, ease: 'expo.out' });
      const px = gsap.quickTo(peek, 'x', { duration: .6, ease: 'expo.out' }), py = gsap.quickTo(peek, 'y', { duration: .6, ease: 'expo.out' });
      window.addEventListener('pointermove', e => { cx(e.clientX); cy(e.clientY); px(e.clientX + 40); py(e.clientY - 60); }, { passive: true });
    }

    /* conservar la posición al cruzar el quiebre móvil/escritorio */
    let anchor = null;
    mobileQ.addEventListener('change', () => {
      anchor = savedAnchor;
      heroSource();
      requestAnimationFrame(() => requestAnimationFrame(() => {
        ScrollTrigger.refresh();
        if (anchor) { const y = anchor.el.getBoundingClientRect().top + scrollY + anchor.f * anchor.el.offsetHeight; if (window.__lenis) window.__lenis.scrollTo(y, { immediate: true }); else scrollTo(0, y); anchor = null; }
      }));
    });

    window.addEventListener('load', () => ScrollTrigger.refresh());
  }
})();
