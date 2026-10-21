#!/usr/bin/env python3
"""Jurado 2 (fase 16) · interacciones y mediciones. Sirve la raíz en :8765 (python3 -m http.server 8765 --bind 127.0.0.1).
Uso: python3 _plan/jurado-2/after/interact.py [hoy|menu|carta|targets|dpr|lcp|all]
Escribe interact.json y capturas i-*.jpg en esta carpeta."""
import asyncio, json, os, sys
from pathlib import Path
from playwright.async_api import async_playwright
os.environ.setdefault('PLAYWRIGHT_BROWSERS_PATH', '/opt/pw-browsers')
CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
OUT = Path(__file__).parent
BASE = 'http://127.0.0.1:8765/'
which = sys.argv[1] if len(sys.argv) > 1 else 'all'
R = {}

HOY_STATE = """() => { const s = document.getElementById('hoy'), v = s.querySelector('.hoy-dia:not([hidden])'), r = s.getBoundingClientRect();
  return { top: Math.round(r.top), arm: s.classList.contains('arm'), imprime: s.classList.contains('imprime'),
           clip: getComputedStyle(v).clipPath, bg: getComputedStyle(s).backgroundColor }; }"""


async def ctx(b, w, h, dpr=1, **kw):
    c = await b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=dpr, **kw)
    p = await c.new_page()
    errs = []
    p.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
    p.on('pageerror', lambda e: errs.append(str(e)))
    p._errs = errs
    return c, p


async def hoy(b):
    out = {}
    # 1) teléfono: menú → El lugar, luego subir hasta Hoy
    c, p = await ctx(b, 390, 844)
    await p.goto(BASE + 'index.html', wait_until='networkidle')
    await p.click('.menu-b'); await p.wait_for_timeout(500)
    await p.click('#hoja a[href="#lugar"]'); await p.wait_for_timeout(900)
    y = await p.evaluate("document.getElementById('hoy').offsetTop + 120")
    await p.evaluate(f'window.scrollTo(0,{y})'); await p.wait_for_timeout(1400)
    out['menu-lugar-subir-390'] = await p.evaluate(HOY_STATE)
    await p.screenshot(path=str(OUT / 'i-hoy-menu-subir-390.jpg'), type='jpeg', quality=70)
    await c.close()
    # 2) 1920: bajar exactamente una pantalla
    c, p = await ctx(b, 1920, 1080)
    await p.goto(BASE + 'index.html', wait_until='networkidle')
    await p.evaluate('window.scrollTo(0, innerHeight)'); await p.wait_for_timeout(1400)
    out['1920-una-pantalla'] = await p.evaluate(HOY_STATE)
    await p.screenshot(path=str(OUT / 'i-hoy-1920-una-pantalla.jpg'), type='jpeg', quality=70)
    await c.close()
    # 3) salto dentro de la sección en 4 anchos
    for w, h in [(390, 844), (1024, 768), (1440, 900), (1920, 1080)]:
        c, p = await ctx(b, w, h)
        await p.goto(BASE + 'index.html', wait_until='networkidle')
        await p.evaluate("window.scrollTo(0, document.getElementById('hoy').offsetTop + 50)"); await p.wait_for_timeout(1400)
        out[f'salto+50-{w}'] = await p.evaluate(HOY_STATE)
        await c.close()
    # 4) entrada directa con #lugar y subir
    c, p = await ctx(b, 1440, 900)
    await p.goto(BASE + 'index.html#lugar', wait_until='networkidle'); await p.wait_for_timeout(600)
    await p.evaluate("window.scrollTo(0, document.getElementById('hoy').offsetTop)"); await p.wait_for_timeout(1400)
    out['hash-lugar-subir-1440'] = await p.evaluate(HOY_STATE)
    await p.screenshot(path=str(OUT / 'i-hoy-hash-subir-1440.jpg'), type='jpeg', quality=70)
    out['errors'] = p._errs
    await c.close()
    out['ok'] = all(v.get('imprime') and 'inset(0px' in v.get('clip', '') and '100%' not in v.get('clip', '') for k, v in out.items() if isinstance(v, dict))
    R['hoy'] = out


async def menu(b):
    c, p = await ctx(b, 390, 844)
    await p.goto(BASE + 'index.html', wait_until='networkidle')
    await p.focus('.menu-b'); await p.keyboard.press('Enter'); await p.wait_for_timeout(300)
    st = await p.evaluate("() => ({ mainInert: document.querySelector('main').inert, footInert: document.querySelector('.pie-sitio').inert, ariaHidden: document.querySelector('main').getAttribute('aria-hidden'), active: document.activeElement.textContent.trim() })")
    seq = []
    for _ in range(14):
        await p.keyboard.press('Tab')
        seq.append(await p.evaluate("() => { const a = document.activeElement; return (a.closest('#hoja') ? 'hoja:' : a.classList.contains('menu-b') ? 'menu:' : 'FUERA:') + (a.textContent || '').trim().slice(0, 18); }"))
    for _ in range(3):
        await p.keyboard.press('Shift+Tab')
        seq.append(await p.evaluate("() => { const a = document.activeElement; return (a.closest('#hoja') ? 'hoja:' : a.classList.contains('menu-b') ? 'menu:' : 'FUERA:') + (a.textContent || '').trim().slice(0, 18); }"))
    await p.keyboard.press('Escape'); await p.wait_for_timeout(200)
    after = await p.evaluate("() => ({ mainInert: document.querySelector('main').inert, focus: document.activeElement.className })")
    R['menu'] = {'abierto': st, 'tabs': seq, 'escapa': any(s.startswith('FUERA') for s in seq), 'cerrado': after, 'errors': p._errs}
    await c.close()


TAB_PROBE = """() => { const l = document.querySelector('.tabs-l'), a = document.querySelector('.tab[aria-selected="true"]'), lr = l.getBoundingClientRect(), ar = a.getBoundingClientRect();
  const ch = [...document.querySelectorAll('.chip[aria-selected="true"]')].find((c) => c.offsetParent);
  const vis = (r, p) => r.left >= p.left - 1 && r.right <= p.right + 1;
  const tabs = [...document.querySelectorAll('.tab')].map((t) => Math.round(t.getBoundingClientRect().height));
  const rows = new Set([...document.querySelectorAll('.tab')].map((t) => Math.round(t.getBoundingClientRect().top))).size;
  let chipVis = null; if (ch && ch.offsetParent) { chipVis = vis(ch.getBoundingClientRect(), ch.parentElement.getBoundingClientRect()); }
  return { activo: a.textContent, activoVisible: vis(ar, lr), barH: Math.round(document.querySelector('.tabs').getBoundingClientRect().height), filas: rows, minTabH: Math.min(...tabs),
           mascara: l.className, chipVisible: chipVis, sw: document.documentElement.scrollWidth }; }"""


async def carta(b):
    out = {}
    for w, h in [(320, 568), (390, 844), (768, 1024), (1440, 900)]:
        for hsh in ['', '#promos', '#comilona-pizzas', '#sin-alcohol-cervezas']:
            c, p = await ctx(b, w, h)
            await p.goto(BASE + 'carta/index.html' + hsh, wait_until='networkidle'); await p.wait_for_timeout(500)
            out[f'{w}{hsh or "#casa"}'] = await p.evaluate(TAB_PROBE)
            if w in (390, 1440) and hsh:
                await p.screenshot(path=str(OUT / f'i-carta-{w}-{hsh[1:]}.jpg'), type='jpeg', quality=70)
            await c.close()
    R['carta'] = out


TARGETS = """() => { const bad = [];
  document.querySelectorAll('a, button').forEach((el) => {
    const r = el.getBoundingClientRect(), s = getComputedStyle(el);
    if (!r.width || !r.height || s.visibility === 'hidden' || el.closest('[hidden], .hoja:not(.abierta), .vh')) return;
    if (r.bottom < 0 && el.closest('.skip')) return;
    const inText = el.closest('.pie, .pie-creditos, .arrobas, .banda-pie .pie, .equipo-nombres, .res-g, blockquote');
    if ((r.height < 44 || r.width < 24) && !inText) bad.push((el.textContent || el.getAttribute('aria-label') || '').trim().slice(0, 26) + ' ' + Math.round(r.width) + '×' + Math.round(r.height));
  }); return bad; }"""


async def targets(b):
    out = {}
    for page in ['index.html', 'carta/index.html']:
        for w, h in [(390, 844), (1440, 900)]:
            c, p = await ctx(b, w, h)
            await p.goto(BASE + page, wait_until='networkidle')
            out[f'{page}-{w}'] = await p.evaluate(TARGETS)
            await c.close()
    R['targets'] = out


DPR = """(dpr) => { const r = [];
  document.querySelectorAll('picture img').forEach((i) => { const b = i.getBoundingClientRect(); if (!b.width || !i.currentSrc) return;
    const f = i.currentSrc.split('/').pop(), m = /-(\d+)\.(avif|webp|jpg)$/.exec(f); if (!m) return;
    const fw = +m[1], need = b.width * dpr; r.push([f, Math.round(b.width), fw, +(fw / need).toFixed(2), Math.round(i.naturalWidth)]); });
  return r; }"""


async def dpr(b):
    out = {}
    for w, h, d in [(390, 844, 3), (390, 844, 2), (1440, 900, 1), (1440, 900, 2), (1920, 1080, 1)]:
        for page in ['index.html', 'carta/index.html']:
            c, p = await ctx(b, w, h, d)
            await p.goto(BASE + page, wait_until='networkidle')
            H = await p.evaluate('document.documentElement.scrollHeight')
            for y in range(0, H, h):
                await p.evaluate(f'window.scrollTo(0,{y})'); await p.wait_for_timeout(120)
            await p.wait_for_timeout(800)
            rows = await p.evaluate(DPR, d)
            ratios = sorted(x[3] for x in rows)
            upscaled = [x for x in rows if x[2] < x[1] * 0.98]  # CSS px mayor que el archivo
            sizes_off = [x for x in rows if abs(x[4] - x[1]) > 0.1 * x[1]]  # sizes no calza con el ancho real
            out[f'{page}-{w}@{d}x'] = {'n': len(rows), 'mediana': ratios[len(ratios) // 2] if ratios else None, 'min': rows and min(rows, key=lambda x: x[3]),
                                       'max': rows and max(rows, key=lambda x: x[3]), 'css_mayor_que_archivo': upscaled, 'sizes_desajustado': sizes_off}
            await c.close()
    R['dpr'] = out


LCP_INIT = """window.__lcp = 0; window.__lcpEl = '';
new PerformanceObserver((l) => { for (const e of l.getEntries()) { window.__lcp = e.startTime; window.__lcpEl = (e.element && (e.element.currentSrc || e.element.tagName)) || e.url; } }).observe({ type: 'largest-contentful-paint', buffered: true });"""


async def lcp(b):
    out = {}
    for name, page, w, h, d in [('landing-390@3x', 'index.html', 390, 844, 3), ('landing-1440', 'index.html', 1440, 900, 1),
                                ('carta-390@3x', 'carta/index.html', 390, 844, 3)]:
        runs = []
        for _ in range(3):
            c = await b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=d, is_mobile=w < 900, has_touch=w < 900)
            await c.add_init_script(LCP_INIT)
            p = await c.new_page()
            cdp = await c.new_cdp_session(p)
            await cdp.send('Network.enable')
            await cdp.send('Network.setCacheDisabled', {'cacheDisabled': True})
            await cdp.send('Network.emulateNetworkConditions', {'offline': False, 'latency': 150, 'downloadThroughput': 1.6 * 1024 * 1024 / 8, 'uploadThroughput': 750 * 1024 / 8})
            await cdp.send('Emulation.setCPUThrottlingRate', {'rate': 4})
            bytes_ = []
            p.on('response', lambda r: bytes_.append(r.url))
            await p.goto(BASE + page, wait_until='load', timeout=120000)
            await p.wait_for_timeout(2500)
            v = await p.evaluate('[window.__lcp, window.__lcpEl]')
            runs.append([round(v[0]), str(v[1]).split('/')[-1]])
            await c.close()
        out[name] = {'runs': runs, 'mediana_ms': sorted(r[0] for r in runs)[1]}
    R['lcp'] = out


async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path=CHROME, args=['--no-sandbox'])
        for name, fn in [('hoy', hoy), ('menu', menu), ('carta', carta), ('targets', targets), ('dpr', dpr), ('lcp', lcp)]:
            if which in ('all', name):
                await fn(b)
                print(name, 'ok')
        await b.close()
    f = OUT / 'interact.json'
    old = json.loads(f.read_text()) if f.exists() else {}
    old.update(R)
    f.write_text(json.dumps(old, indent=1, ensure_ascii=False))

asyncio.run(main())
