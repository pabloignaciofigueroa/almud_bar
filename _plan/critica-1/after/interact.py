#!/usr/bin/env python3
"""Crítica 1 · pruebas de interacción: menú (abrir/cerrar/reabrir en ráfaga), Escape, mapa al tocar, carta por teclado."""
import asyncio, json, os
from playwright.async_api import async_playwright
CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
B = 'http://127.0.0.1:8765/'
OUT = os.path.dirname(os.path.abspath(__file__))
async def main():
    r = {}
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=CHROME, args=['--no-sandbox'])
        ctx = await b.new_context(viewport={'width': 390, 'height': 844}, has_touch=False)
        pg = await ctx.new_page(); third = []
        pg.on('request', lambda q: third.append(q.url) if not q.url.startswith(B) and not q.url.startswith('data:') else None)
        await pg.goto(B + 'index.html', wait_until='networkidle')
        state = lambda: pg.evaluate("({exp: document.querySelector('.menu-b').getAttribute('aria-expanded'), open: document.querySelector('#hoja').classList.contains('abierta'), vis: getComputedStyle(document.querySelector('#hoja')).visibility, lock: document.documentElement.classList.contains('hoja-on')})")
        fails = []
        import random
        for n in range(40):
            k = random.randint(1, 4)
            for _ in range(k):
                await pg.click('.menu-b'); await pg.wait_for_timeout(random.choice([0, 20, 60, 120, 200, 260]))
            await pg.wait_for_timeout(500)
            s = await state()
            ok = (s['exp'] == 'true') == s['open'] == s['lock'] and (s['vis'] == 'visible') == s['open']
            if not ok: fails.append(s)
        if (await state())['open']: await pg.click('.menu-b'); await pg.wait_for_timeout(400)
        await pg.click('.menu-b'); await pg.wait_for_timeout(500)
        await pg.screenshot(path=f'{OUT}/i-menu-390.jpg', type='jpeg', quality=70)
        await pg.keyboard.press('Escape'); await pg.wait_for_timeout(30)
        r['menu'] = {'bursts': 40, 'inconsistent': fails[:3], 'after_escape': await state()}
        n0 = len(third)
        await pg.evaluate("document.querySelector('.mapa').scrollIntoView()")
        await pg.wait_for_timeout(300)
        r['third_party_before_map_click'] = third[:n0 + 0]
        await pg.click('.mapa-b'); await pg.wait_for_timeout(2500)
        r['map_iframe'] = await pg.evaluate("!!document.querySelector('.mapa iframe')")
        r['third_party_after_click'] = len(third) > n0
        await pg.screenshot(path=f'{OUT}/i-mapa-390.jpg', type='jpeg', quality=70)
        r['next_event'] = await pg.evaluate("[...document.querySelectorAll('.cal li.es-prox')].map(l=>l.innerText.split('\\n').slice(0,3).join(' | '))")
        await ctx.close()
        # carta: teclado instantáneo
        ctx = await b.new_context(viewport={'width': 1440, 'height': 900})
        pg = await ctx.new_page()
        await pg.goto(B + 'carta/index.html', wait_until='networkidle')
        await pg.focus('#t-casa'); await pg.keyboard.press('ArrowRight')
        r['carta_key'] = await pg.evaluate("({tab: document.documentElement.dataset.tab, kb: document.documentElement.classList.contains('kb'), tr: getComputedStyle(document.querySelector('#t-mundo')).transitionDuration, bg: getComputedStyle(document.querySelector('#t-mundo')).backgroundColor})")
        r['carta_h_anim'] = await pg.evaluate("document.querySelector('.carta-h').classList.contains('h-arm')")
        await ctx.close(); await b.close()
    print(json.dumps(r, indent=1, ensure_ascii=False))
    open(f'{OUT}/interact.json', 'w').write(json.dumps(r, indent=1, ensure_ascii=False))
asyncio.run(main())
