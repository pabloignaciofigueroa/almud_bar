#!/usr/bin/env python3
"""Capturas y mediciones de la v2 (fase 14). Uso: python3 _plan/build-v2/shoot.py [etiqueta] [--only 390,1440]
Sirve la raíz con http.server aparte (puerto 8765). Recorre la página para disparar los reveals,
captura página completa y la corta en tramos para mirarla. Mide CLS, LCP y errores de consola."""
import asyncio, json, os, sys
from pathlib import Path
from playwright.async_api import async_playwright
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
os.environ.setdefault('PLAYWRIGHT_BROWSERS_PATH', '/opt/pw-browsers')
OUT = Path(__file__).parent / 'shots'
URL = 'http://127.0.0.1:8765/index.html'
tag = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('--') else 'r'
only = None
if '--only' in sys.argv:
    only = sys.argv[sys.argv.index('--only') + 1].split(',')
dia = None
if '--dia' in sys.argv:
    dia = sys.argv[sys.argv.index('--dia') + 1]
CONFIGS = [
    ('390', 390, 844, False, 'es'), ('768', 768, 1024, False, 'es'), ('1280', 1280, 720, False, 'es'),
    ('1440', 1440, 900, False, 'es'), ('1920', 1920, 1080, False, 'es'),
    ('390-rm', 390, 844, True, 'es'), ('1440-rm', 1440, 900, True, 'es'),
    ('390-en', 390, 844, False, 'en'), ('1440-en', 1440, 900, False, 'en'),
]
INIT = """
window.__cls = 0; window.__lcp = 0; window.__lcpEl = '';
new PerformanceObserver((l) => { for (const e of l.getEntries()) if (!e.hadRecentInput) window.__cls += e.value; }).observe({ type: 'layout-shift', buffered: true });
new PerformanceObserver((l) => { const es = l.getEntries(); const e = es[es.length - 1]; window.__lcp = e.startTime; window.__lcpEl = (e.element && (e.element.tagName + '.' + (e.element.className||'') + ' ' + (e.element.currentSrc||'').split('/').pop())) || ''; }).observe({ type: 'largest-contentful-paint', buffered: true });
"""
async def run():
    res = {}
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--no-sandbox'])
        for name, w, h, rm, lang in CONFIGS:
            if only and name not in only: continue
            ctx = await b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=1, reduced_motion='reduce' if rm else 'no-preference')
            if lang == 'en':
                await ctx.add_init_script("try{localStorage.setItem('almud-lang','en')}catch(e){}")
            await ctx.add_init_script(INIT)
            pg = await ctx.new_page()
            errs = []
            pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
            pg.on('pageerror', lambda e: errs.append(str(e)))
            url = URL + (f'?dia={dia}' if dia else '')
            await pg.goto(url, wait_until='networkidle')
            await pg.wait_for_timeout(800)
            first = await pg.evaluate('({cls: window.__cls, lcp: window.__lcp, el: window.__lcpEl})')
            await pg.screenshot(path=str(OUT / f'{tag}-{name}-fold.jpg'), type='jpeg', quality=70)
            H = await pg.evaluate('document.documentElement.scrollHeight')
            y = 0
            while y < H:
                y += int(h * 0.6)
                await pg.mouse.wheel(0, int(h * 0.6))
                await pg.wait_for_timeout(120)
                H = await pg.evaluate('document.documentElement.scrollHeight')
            await pg.wait_for_timeout(1200)
            cls_after = await pg.evaluate('window.__cls')
            await pg.evaluate('window.scrollTo(0,0)')
            await pg.wait_for_timeout(300)
            full = OUT / f'{tag}-{name}-full.png'
            await pg.screenshot(path=str(full), full_page=True)
            hx = await pg.evaluate('document.documentElement.scrollWidth')
            res[name] = {'cls_load': round(first['cls'], 4), 'cls_scroll': round(cls_after, 4), 'lcp_ms': round(first['lcp']), 'lcp_el': first['el'], 'height': H, 'scrollWidth': hx, 'errors': errs[:5]}
            # tramos para mirar
            im = Image.open(full).convert('RGB')
            seg = h * 3
            for i in range(0, im.height, seg):
                part = im.crop((0, i, im.width, min(im.height, i + seg)))
                scale = min(1, 900 / part.width) if w > 900 else 1
                if scale < 1: part = part.resize((int(part.width * scale), int(part.height * scale)))
                part.save(OUT / f'{tag}-{name}-s{i // seg:02d}.jpg', quality=72)
            full.unlink()
            await ctx.close()
        await b.close()
    print(json.dumps(res, indent=1))
    (OUT / f'{tag}-metrics.json').write_text(json.dumps(res, indent=1))
asyncio.run(run())
