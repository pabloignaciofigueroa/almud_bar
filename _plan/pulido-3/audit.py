#!/usr/bin/env python3
"""Pulido 3 (fase 17) · sondas de auditoría técnica (Impeccable audit + Emil break-ui).
Sirve la raíz aparte: python3 -m http.server 8794 --bind 127.0.0.1
Uso: python3 _plan/pulido-3/audit.py [tag]   → escribe audit-<tag>.json y capturas b-<tag>-*.jpg en shots/
Sondas: axe-core (wcag2a/aa + best-practice), esquema de titulares, imágenes (alt, width/height, decoding, loading,
fetchpriority), recorrido con Tab (anillo visible en cada parada), sin JS, sin imágenes (red lenta), 200 % de zoom
(1280 → 640 CSS px a DPR 2), letra por defecto grande (24 px), 320 px EN, reduced motion, consola y pedidos fallidos."""
import asyncio, json, os, sys
from pathlib import Path
from playwright.async_api import async_playwright
os.environ.setdefault('PLAYWRIGHT_BROWSERS_PATH', '/opt/pw-browsers')
CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
OUT = Path(__file__).parent / 'shots'
BASE = 'http://127.0.0.1:8794/'
AXE = Path('/home/claude/.npm/_npx/68d4b0c02cc20704/node_modules/axe-core/axe.min.js').read_text()
tag = sys.argv[1] if len(sys.argv) > 1 else 'antes'
PAGES = {'landing': 'index.html', 'carta': 'carta/index.html'}
R = {}

STATIC = """() => {
  const hs = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].map(h => h.tagName + ' ' + h.textContent.trim().replace(/\\s+/g,' ').slice(0,40));
  const imgs = [...document.querySelectorAll('img')].map(i => ({ src: (i.getAttribute('src')||'').split('/').pop(), alt: i.hasAttribute('alt'),
    wh: i.hasAttribute('width') && i.hasAttribute('height'), dec: i.getAttribute('decoding'), load: i.getAttribute('loading'), fp: i.getAttribute('fetchpriority') }));
  const ids = {}; document.querySelectorAll('[id]').forEach(e => ids[e.id] = (ids[e.id]||0)+1);
  const head = { favicon: !!document.querySelector('link[rel=icon]'), manifest: !!document.querySelector('link[rel=manifest]'),
    theme: !!document.querySelector('meta[name=theme-color]'), ld: [...document.querySelectorAll('script[type="application/ld+json"]')].length,
    preload: [...document.querySelectorAll('link[rel=preload]')].map(l => (l.getAttribute('href')||l.getAttribute('imagesrcset')||'').split('/').pop().slice(0,40)),
    hreflang: [...document.querySelectorAll('link[hreflang]')].length };
  const landmarks = { main: document.querySelectorAll('main').length, nav: document.querySelectorAll('nav,[role=navigation]').length, footer: document.querySelectorAll('footer').length, header: document.querySelectorAll('header').length };
  return { hs, imgs_total: imgs.length, img_noalt: imgs.filter(i=>!i.alt).length, img_nowh: imgs.filter(i=>!i.wh).map(i=>i.src),
    img_nodecoding: imgs.filter(i=>!i.dec).length, img_lazy: imgs.filter(i=>i.load==='lazy').length, img_fp_high: imgs.filter(i=>i.fp==='high').map(i=>i.src),
    dup_ids: Object.entries(ids).filter(([k,v])=>v>1), head, landmarks };
}"""

FOCUS = """() => { const a = document.activeElement; if (!a || a === document.body) return null;
  const s = getComputedStyle(a); const r = a.getBoundingClientRect();
  return { t: (a.getAttribute('aria-label') || a.textContent || a.tagName).trim().replace(/\\s+/g,' ').slice(0,28), tag: a.tagName,
    ring: s.outlineStyle !== 'none' && parseFloat(s.outlineWidth) >= 2, oc: s.outlineColor, inview: r.bottom > 0 && r.top < innerHeight, w: Math.round(r.width), h: Math.round(r.height) }; }"""


async def newpage(b, w, h, dpr=1, js=True, rm=False, lang='es'):
    c = await b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=dpr, java_script_enabled=js,
                            reduced_motion='reduce' if rm else 'no-preference')
    await c.add_init_script("try{localStorage.setItem('almud-lang','%s')}catch(e){}" % lang)
    p = await c.new_page()
    p._errs, p._failed = [], []
    p.on('console', lambda m: p._errs.append(m.text) if m.type == 'error' else None)
    p.on('pageerror', lambda e: p._errs.append(str(e)))
    p.on('requestfailed', lambda r: p._failed.append(r.url.split('/')[-1] + ' ' + (r.failure or '')))
    p.on('response', lambda r: p._failed.append(f'{r.status} ' + r.url.split('/')[-1]) if r.status >= 400 else None)
    return c, p


async def walk(p):
    H = await p.evaluate('document.documentElement.scrollHeight'); y = 0
    while y < H:
        await p.evaluate(f'window.scrollTo(0,{y})'); await p.wait_for_timeout(250); y += 600
        H = await p.evaluate('document.documentElement.scrollHeight')
    await p.evaluate('window.scrollTo(0,0)'); await p.wait_for_timeout(300)


async def axe(p):
    await p.add_script_tag(content=AXE)
    res = await p.evaluate("""async () => { const r = await axe.run(document, { runOnly: ['wcag2a','wcag2aa','wcag21aa','wcag22aa','best-practice'] });
      return r.violations.map(v => ({ id: v.id, impact: v.impact, n: v.nodes.length, ex: v.nodes.slice(0,3).map(n => n.target.join(' ') + ' :: ' + (n.failureSummary||'').split('\\n').slice(1,2).join('')) })); }""")
    return res


async def page_audit(b, name, path):
    out = {}
    for w, h in [(390, 844), (1440, 900)]:
        c, p = await newpage(b, w, h)
        await p.goto(BASE + path, wait_until='networkidle'); await walk(p)
        out[f'axe-{w}'] = await axe(p)
        if w == 1440: out['static'] = await p.evaluate(STATIC)
        # teclado: 40 Tab desde arriba
        await p.evaluate('window.scrollTo(0,0)'); stops = []
        for i in range(40):
            await p.keyboard.press('Tab'); await p.wait_for_timeout(60)
            stops.append(await p.evaluate(FOCUS))
        out[f'kb-{w}'] = {'stops': len([s for s in stops if s]), 'sin_anillo': [s for s in stops if s and not s['ring']],
                          'fuera_de_vista': [s['t'] for s in stops if s and not s['inview']], 'primeros': [s['t'] for s in stops[:12] if s]}
        out[f'console-{w}'] = p._errs[:5]; out[f'failed-{w}'] = p._failed[:5]
        await c.close()
    # sin JS
    c, p = await newpage(b, 390, 844, js=False)
    await p.goto(BASE + path, wait_until='networkidle'); await p.wait_for_timeout(300)
    out['nojs'] = await p.evaluate("""() => { const hidden = [...document.querySelectorAll('main section, main h2, main img')].filter(e => { const s = getComputedStyle(e); return s.display === 'none' || s.visibility === 'hidden' || parseFloat(s.opacity) === 0; }).length;
      return { H: document.documentElement.scrollHeight, sw: document.documentElement.scrollWidth, ocultos: hidden, h2: document.querySelectorAll('h2').length }; }""")
    await p.screenshot(path=str(OUT / f'b-{tag}-{name}-nojs-390.jpg'), type='jpeg', quality=60)
    await c.close()
    # sin imágenes (red lenta: las fotos nunca llegan)
    c, p = await newpage(b, 390, 844)
    await p.route('**/*.{avif,webp,jpg,png,mp4}', lambda r: r.abort())
    await p.goto(BASE + path, wait_until='domcontentloaded'); await p.wait_for_timeout(1200)
    out['sin-img'] = await p.evaluate("() => ({ sw: document.documentElement.scrollWidth, broken: [...document.querySelectorAll('img')].filter(i => i.complete && !i.naturalWidth && i.getBoundingClientRect().height < 4).length })")
    await p.screenshot(path=str(OUT / f'b-{tag}-{name}-sin-img-390.jpg'), type='jpeg', quality=60)
    await p.evaluate('window.scrollTo(0, innerHeight * 2)'); await p.wait_for_timeout(500)
    await p.screenshot(path=str(OUT / f'b-{tag}-{name}-sin-img-390-b.jpg'), type='jpeg', quality=60)
    await c.close()
    # 200 % de zoom en 1280 × 720 = 640 × 360 CSS px a DPR 2
    c, p = await newpage(b, 640, 360, dpr=2)
    await p.goto(BASE + path, wait_until='networkidle'); await p.wait_for_timeout(400)
    out['zoom200'] = await p.evaluate("() => ({ sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth })")
    await p.screenshot(path=str(OUT / f'b-{tag}-{name}-zoom200.jpg'), type='jpeg', quality=60)
    await p.evaluate('window.scrollTo(0, innerHeight * 3)'); await p.wait_for_timeout(500)
    await p.screenshot(path=str(OUT / f'b-{tag}-{name}-zoom200-b.jpg'), type='jpeg', quality=60)
    await c.close()
    # letra grande: el usuario pide 24 px por defecto (ajuste del navegador)
    c, p = await newpage(b, 390, 844)
    cdp = await c.new_cdp_session(p)
    await cdp.send('Page.enable')
    await cdp.send('Page.setFontSizes', {'fontSizes': {'standard': 24, 'fixed': 20}})
    await p.goto(BASE + path, wait_until='networkidle'); await p.wait_for_timeout(400)
    out['letra24'] = await p.evaluate("() => ({ body: getComputedStyle(document.body).fontSize, small: getComputedStyle(document.querySelector('.small, .pie, .tab') || document.body).fontSize, sw: document.documentElement.scrollWidth })")
    await p.screenshot(path=str(OUT / f'b-{tag}-{name}-letra24-390.jpg'), type='jpeg', quality=60)
    await c.close()
    # 320 EN
    c, p = await newpage(b, 320, 568, lang='en')
    await p.goto(BASE + path, wait_until='networkidle'); await walk(p)
    out['320-en'] = await p.evaluate("""() => { const over = [...document.querySelectorAll('main *, nav *, header *')].filter(e => { const r = e.getBoundingClientRect(); return r.width && (r.right > innerWidth + 1 || r.left < -1) && getComputedStyle(e).position !== 'fixed' && !e.closest('.tabs-l,.chips,.cover-img,.vh') ; }).slice(0,6).map(e => e.className + ' ' + Math.round(e.getBoundingClientRect().right));
      return { sw: document.documentElement.scrollWidth, desbordes: over }; }""")
    await p.screenshot(path=str(OUT / f'b-{tag}-{name}-320-en.jpg'), type='jpeg', quality=60)
    await c.close()
    return out


async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path=CHROME, args=['--no-sandbox'])
        for n, path in PAGES.items():
            R[n] = await page_audit(b, n, path)
            print(n, json.dumps(R[n], ensure_ascii=False)[:3000])
        # 404
        c, p = await newpage(b, 390, 844)
        r = await p.goto(BASE + 'no-existe/', wait_until='load')
        R['404'] = {'status': r.status if r else None}
        await c.close()
        await b.close()
    (OUT.parent / f'audit-{tag}.json').write_text(json.dumps(R, indent=1, ensure_ascii=False))

asyncio.run(main())
