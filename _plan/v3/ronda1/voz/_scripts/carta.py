import json, asyncio, sys
sys.path.insert(0, "/tmp/claude-0/-home-claude/011b3bf8-fa11-50bd-ba3e-4cc567dfb832/scratchpad")
from playwright.async_api import async_playwright

OUT = "/home/claude/almud_bar/_plan/v3/ronda1/voz"
CH = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
EXTRACT = open("/tmp/claude-0/-home-claude/011b3bf8-fa11-50bd-ba3e-4cc567dfb832/scratchpad/extract.js").read()

async def run():
    res = {}
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=CH, args=["--no-sandbox", "--autoplay-policy=no-user-gesture-required"])
        for vk, W, H in (("m", 390, 844), ("d", 1440, 900)):
            for lang in ("es", "en"):
                ctx = await b.new_context(viewport={"width": W, "height": H})
                pg = await ctx.new_page()
                await pg.goto("http://localhost:8841/v3/carta/", wait_until="networkidle")
                await pg.wait_for_timeout(1500)
                if lang == "en":
                    await pg.locator("[data-lang]").first.click(); await pg.wait_for_timeout(600)
                ids = await pg.evaluate("[...document.querySelectorAll('.tab')].map(t=>t.dataset.tab)")
                for ti, tid in enumerate(ids):
                    await pg.locator(f'.tab[data-tab="{tid}"]').click(); await pg.wait_for_timeout(900)
                    # sub-tabs inside panel?
                    subs = await pg.evaluate(f"[...document.querySelectorAll('#{tid} .sub')].length")
                    total = await pg.evaluate("document.documentElement.scrollHeight")
                    y, i = await pg.evaluate("scrollY"), 0
                    start = y
                    while y < total and i < 12:
                        await pg.evaluate(f"window.scrollTo(0,{y})"); await pg.wait_for_timeout(500)
                        if vk == "m" or i < 3:
                            await pg.screenshot(path=f"{OUT}/carta-{vk}-{lang}-t{ti}-{i:02d}.jpg", quality=60, type="jpeg")
                        i += 1; y += int(H * 0.9)
                    await pg.evaluate("window.scrollTo(0,0)"); await pg.wait_for_timeout(300)
                    data = await pg.evaluate(EXTRACT)
                    res[f"carta-{vk}-{lang}-{tid}"] = dict(data, subs=subs, shots=i)
                await ctx.close()
        await b.close()
    json.dump(res, open(f"{OUT}/dom-carta.json", "w"), ensure_ascii=False, indent=1)
    for k, v in res.items():
        print(k, "shots", v["shots"], "subs", v["subs"], "issues", [x for x in v["issues"] if not (x['k']=='offscreen-x' and 'tab' in x['sel'])])

asyncio.run(run())
