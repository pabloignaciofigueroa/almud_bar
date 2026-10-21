#!/usr/bin/env python3
"""Jurado 2 (fase 16) · capturas "después" viewport por viewport, con métricas.
Uso: python3 _plan/critica-1/after/shoot.py [landing|carta|both] [--only 390,1440-en] [--tag r1] [--dia 3]
Sirve la raíz aparte: python3 -m http.server 8794 --bind 127.0.0.1
Por captura: CLS (carga y tras recorrer), errores de consola, pedidos fallidos, pedidos a terceros, ancho de scroll,
imágenes duplicadas por id de medio (solo las visibles), objetivos táctiles < 24 px."""
import asyncio, json, os, sys
from pathlib import Path
from playwright.async_api import async_playwright
os.environ.setdefault('PLAYWRIGHT_BROWSERS_PATH', '/opt/pw-browsers')
CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
OUT = Path(__file__).parent / 'shots'
BASE = 'http://127.0.0.1:8794/'
args = sys.argv[1:]
which = args[0] if args and not args[0].startswith('--') else 'both'
only = args[args.index('--only') + 1].split(',') if '--only' in args else None
tag = args[args.index('--tag') + 1] if '--tag' in args else 'r'
dia = args[args.index('--dia') + 1] if '--dia' in args else None
CONFIGS = [  # nombre, ancho, alto, reduced, idioma
    ('320', 320, 568, False, 'es'), ('390', 390, 844, False, 'es'),
    ('768', 768, 1024, False, 'es'), ('1280', 1280, 720, False, 'es'),
    ('1440', 1440, 900, False, 'es'), ('1920', 1920, 1080, False, 'es'),
    ('390-en', 390, 844, False, 'en'), ('1440-en', 1440, 900, False, 'en'),
    ('390-rm', 390, 844, True, 'es'), ('1440-rm', 1440, 900, True, 'es'),

]
INIT = """
window.__cls = 0;
new PerformanceObserver((l) => { for (const e of l.getEntries()) if (!e.hadRecentInput) window.__cls += e.value; }).observe({ type: 'layout-shift', buffered: true });
"""
PROBE = """() => {
  const vis = (el) => { const r = el.getBoundingClientRect(); const s = getComputedStyle(el); return r.width > 0 && r.height > 0 && s.visibility !== 'hidden'; };
  const ids = {};
  document.querySelectorAll('picture img, video').forEach((el) => {
    if (!vis(el)) return;
    const src = (el.currentSrc || el.getAttribute('src') || el.getAttribute('poster') || '').split('/').pop().replace(/-(a|d|m|og)-\\d+\\.(avif|webp)$/, '').replace(/-poster\\.(avif|webp)$/, '').replace(/\\.(mp4|webm)$/, '');
    if (src) ids[src] = (ids[src] || 0) + 1;
  });
  const dup = Object.entries(ids).filter(([k, v]) => v > 1);
  const small = [];
  document.querySelectorAll('a, button').forEach((el) => {
    if (!vis(el)) return; const r = el.getBoundingClientRect();
    if (r.height < 24 && el.closest('p, li, dd, figcaption') === null) small.push((el.textContent || '').trim().slice(0, 30) + ' ' + Math.round(r.height));
  });
  return { dup, small: small.slice(0, 8), sw: document.documentElement.scrollWidth, H: document.documentElement.scrollHeight };
}"""

async def shoot(b, page, name, w, h, rm, lang):
    ctx = await b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=1, reduced_motion='reduce' if rm else 'no-preference')
    await ctx.add_init_script("try{localStorage.setItem('almud-lang','%s')}catch(e){}" % lang)
    await ctx.add_init_script(INIT)
    pg = await ctx.new_page()
    errs, failed, third = [], [], []
    pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.on('requestfailed', lambda r: failed.append(r.url.split('/')[-1] + ' ' + (r.failure or '')))
    pg.on('request', lambda r: third.append(r.url) if not r.url.startswith(BASE) and not r.url.startswith('data:') else None)
    url = BASE + ('index.html' if page == 'landing' else 'carta/index.html') + (f'?dia={dia}' if dia else '')
    await pg.goto(url, wait_until='networkidle')
    await pg.wait_for_timeout(600)
    cls_load = await pg.evaluate('window.__cls')
    H = await pg.evaluate('document.documentElement.scrollHeight')
    y, i = 0, 0
    while True:
        await pg.evaluate(f'window.scrollTo(0,{y})')
        await pg.wait_for_timeout(1100 if not rm else 400)
        await pg.screenshot(path=str(OUT / f'{tag}-{page}-{name}-v{i:02d}.jpg'), type='jpeg', quality=68)
        H = await pg.evaluate('document.documentElement.scrollHeight')
        if y + h >= H or i > 60:
            break
        y += h; i += 1
    probe = await pg.evaluate(PROBE)
    cls_after = await pg.evaluate('window.__cls')
    await ctx.close()
    return {'cls_load': round(cls_load, 4), 'cls_scroll': round(cls_after, 4), 'screens': i + 1, 'errors': errs[:5], 'failed': failed[:5],
            'third_party': third[:5], **probe}

async def main():
    res = {}
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=CHROME, args=['--no-sandbox'])
        for page in (['landing', 'carta'] if which == 'both' else [which]):
            for name, w, h, rm, lang in CONFIGS:
                if only and name not in only:
                    continue
                res[f'{page}-{name}'] = r = await shoot(b, page, name, w, h, rm, lang)
                print(page, name, json.dumps(r, ensure_ascii=False))
        await b.close()
    mf = OUT.parent / f'{tag}-metrics.json'
    old = json.loads(mf.read_text()) if mf.exists() else {}
    old.update(res)
    mf.write_text(json.dumps(old, indent=1, ensure_ascii=False))

asyncio.run(main())
