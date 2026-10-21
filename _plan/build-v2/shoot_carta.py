#!/usr/bin/env python3
"""Fase 15 · capturas y pruebas de la carta (landing: destacados; carta/: pestañas y grupos).
Uso: python3 _plan/build-v2/shoot_carta.py [etiqueta] [--only 390,768,1440]
Sirve la raíz con http.server aparte (puerto 8765). Guarda en _plan/build-v2/shots-carta/ y escribe <etiqueta>-medidas.json:
errores de consola, CLS de carga y CLS de los cambios de pestaña (contando también los que siguen a una interacción),
teclado (flechas), atrás/adelante y ancho de página (sin scroll lateral)."""
import asyncio, json, os, sys
from pathlib import Path
from playwright.async_api import async_playwright
os.environ.setdefault('PLAYWRIGHT_BROWSERS_PATH', '/opt/pw-browsers')
OUT = Path(__file__).parent / 'shots-carta'
OUT.mkdir(exist_ok=True)
BASE = 'http://127.0.0.1:8765/'
CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
tag = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('--') else 'r'
only = sys.argv[sys.argv.index('--only') + 1].split(',') if '--only' in sys.argv else None
WIDTHS = [('390', 390, 844), ('768', 768, 1024), ('1440', 1440, 900)]
TABS = ['casa', 'mundo', 'espirituosos', 'vinos', 'sin-alcohol', 'comilona', 'promos']
INIT = """
window.__cls = 0; window.__clsAll = 0;
new PerformanceObserver((l) => { for (const e of l.getEntries()) { window.__clsAll += e.value; if (!e.hadRecentInput) window.__cls += e.value; } }).observe({ type: 'layout-shift', buffered: true });
"""


async def settle(pg, ms=450):
    await pg.wait_for_timeout(ms)
    await pg.evaluate("Promise.all([...document.images].filter(i => i.getBoundingClientRect().top < innerHeight*2 && i.getBoundingClientRect().bottom > -200).map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; setTimeout(r, 3000); })))")


async def run():
    res = {}
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=CHROME, args=['--no-sandbox'])
        for name, w, h in WIDTHS:
            if only and name not in only:
                continue
            for lang in ('es', 'en'):
                if lang == 'en' and name == '768':
                    continue
                key = f'{name}-{lang}'
                r = res[key] = {}
                ctx = await b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=1)
                if lang == 'en':
                    await ctx.add_init_script("try{localStorage.setItem('almud-lang','en')}catch(e){}")
                await ctx.add_init_script(INIT)
                pg = await ctx.new_page()
                errs = []
                pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
                pg.on('pageerror', lambda e: errs.append(str(e)))

                # ---- landing: los destacados de la carta
                await pg.goto(BASE + 'index.html', wait_until='networkidle')
                sec = pg.locator('#carta')
                await sec.scroll_into_view_if_needed()
                await pg.evaluate("document.querySelectorAll('#carta img').forEach(i => i.loading = 'eager')")
                await settle(pg, 900)
                await sec.screenshot(path=str(OUT / f'{tag}-landing-carta-{key}.jpg'), type='jpeg', quality=72)
                if lang == 'es':
                    for sid in ('tragos', 'sin-alcohol', 'comida'):
                        await pg.evaluate(f"document.querySelectorAll('#{sid} img').forEach(i => i.loading = 'eager')")
                        el = pg.locator('#' + sid)
                        await el.scroll_into_view_if_needed()
                        await settle(pg, 900)
                        await el.screenshot(path=str(OUT / f'{tag}-landing-{sid}-{key}.jpg'), type='jpeg', quality=60)
                r['landing_overflow'] = await pg.evaluate('document.documentElement.scrollWidth - innerWidth')

                # ---- carta/: carga
                await pg.goto(BASE + 'carta/', wait_until='networkidle')
                await settle(pg, 700)
                r['cls_carga'] = await pg.evaluate('window.__cls')
                await pg.screenshot(path=str(OUT / f'{tag}-carta-{key}-fold.jpg'), type='jpeg', quality=72)
                # cada pestaña, con el ratón, con la página ya bajada (la barra está fija)
                await pg.evaluate("scrollTo(0, document.querySelector('.tabs-sent').getBoundingClientRect().top + scrollY + 400)")
                await pg.wait_for_timeout(200)
                before = await pg.evaluate('window.__clsAll')
                r['tabs'] = {}
                for t in (TABS if lang == 'es' else ['casa', 'comilona']):
                    await pg.locator(f'.tab[data-tab="{t}"]').click()
                    await settle(pg, 350)
                    info = await pg.evaluate(f"""(() => {{ const p = document.getElementById('{t}'); const tb = document.querySelector('.tabs').getBoundingClientRect();
                        const vis = [...document.querySelectorAll('.cp')].filter(x => getComputedStyle(x).display !== 'none').map(x => x.id);
                        return {{hash: location.hash, sel: document.querySelector('.tab[aria-selected=true]').dataset.tab, visibles: vis,
                                 tabsTop: Math.round(tb.top), panelTop: Math.round(p.getBoundingClientRect().top), alto: Math.round(p.getBoundingClientRect().height),
                                 bg: getComputedStyle(p).backgroundColor}} }})()""")
                    r['tabs'][t] = info
                    await pg.screenshot(path=str(OUT / f'{tag}-carta-{key}-tab-{t}.jpg'), type='jpeg', quality=72)
                # un grupo filtrado (chips) en dos pestañas largas
                for t, sub in (('comilona', 'comilona-pizzas'), ('espirituosos', 'espirituosos-gin')):
                    if lang == 'en' and t == 'espirituosos':
                        continue
                    await pg.locator(f'.tab[data-tab="{t}"]').click()
                    await settle(pg, 300)
                    await pg.locator(f'.chip[data-sub="{sub}"]').click()
                    await settle(pg, 400)
                    r.setdefault('chips', {})[sub] = await pg.evaluate(f"""(() => {{ const v = [...document.querySelectorAll('#{t} .csub')].filter(x => getComputedStyle(x).display !== 'none').map(x => x.id);
                        return {{hash: location.hash, visibles: v, sel: document.querySelector('#{t} .chip[aria-selected=true]').dataset.sub}} }})()""")
                    await pg.screenshot(path=str(OUT / f'{tag}-carta-{key}-chip-{sub}.jpg'), type='jpeg', quality=72)
                r['cls_cambios_todo'] = round(await pg.evaluate('window.__clsAll') - before, 5)
                # atrás / adelante
                await pg.go_back(); await pg.wait_for_timeout(250)
                b1 = await pg.evaluate("[document.documentElement.dataset.tab, location.hash]")
                await pg.go_back(); await pg.wait_for_timeout(250)
                b2 = await pg.evaluate("[document.documentElement.dataset.tab, location.hash]")
                await pg.go_forward(); await pg.wait_for_timeout(250)
                f1 = await pg.evaluate("[document.documentElement.dataset.tab, location.hash]")
                r['historial'] = {'atras1': b1, 'atras2': b2, 'adelante': f1}
                # teclado: foco en la pestaña activa, flecha derecha, Fin, Inicio
                await pg.locator('.tab[aria-selected="true"]').focus()
                await pg.keyboard.press('ArrowRight')
                k1 = await pg.evaluate("[document.activeElement.dataset.tab, document.documentElement.dataset.tab, location.hash]")
                await pg.keyboard.press('End')
                k2 = await pg.evaluate("[document.activeElement.dataset.tab, document.documentElement.dataset.tab]")
                await pg.keyboard.press('Home')
                k3 = await pg.evaluate("[document.activeElement.dataset.tab, document.documentElement.dataset.tab]")
                r['teclado'] = {'flecha': k1, 'fin': k2, 'inicio': k3}
                r['overflow'] = await pg.evaluate('document.documentElement.scrollWidth - innerWidth')
                # enlace profundo
                await pg.goto(BASE + 'carta/#comilona-pizzas', wait_until='networkidle')
                await settle(pg, 500)
                r['deep'] = await pg.evaluate("[document.documentElement.dataset.tab, document.documentElement.getAttribute('data-sub-comilona'), Math.round(document.getElementById('comilona-pizzas').getBoundingClientRect().top)]")
                r['cls_deep'] = await pg.evaluate('window.__cls')
                await pg.screenshot(path=str(OUT / f'{tag}-carta-{key}-deep-pizzas.jpg'), type='jpeg', quality=72)
                r['errores'] = errs
                await ctx.close()
        # sin JS: todo apilado
        ctx = await b.new_context(viewport={'width': 390, 'height': 844}, java_script_enabled=False)
        pg = await ctx.new_page()
        await pg.goto(BASE + 'carta/', wait_until='networkidle')
        res['nojs'] = await pg.evaluate("[...document.querySelectorAll('.cp')].filter(x => getComputedStyle(x).display !== 'none').length")
        await pg.screenshot(path=str(OUT / f'{tag}-carta-390-nojs-fold.jpg'), type='jpeg', quality=60)
        await ctx.close()
        await b.close()
    (OUT / f'{tag}-medidas.json').write_text(json.dumps(res, ensure_ascii=False, indent=1))
    print(json.dumps(res, ensure_ascii=False, indent=1))


asyncio.run(run())
