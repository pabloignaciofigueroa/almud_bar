import json, sys, asyncio
from playwright.async_api import async_playwright

OUT = "/home/claude/almud_bar/_plan/v3/ronda1/voz"
CH = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
PAGES = [("home", "http://localhost:8841/v3/"), ("carta", "http://localhost:8841/v3/carta/")]
VPS = [("m", 390, 844), ("d", 1440, 900)]

EXTRACT = r"""
() => {
  const vw = innerWidth, out = [], issues = [];
  const vis = el => { const s = getComputedStyle(el); if (s.display==='none'||s.visibility==='hidden'||+s.opacity===0) return false;
    let p = el; while (p) { const cs = getComputedStyle(p); if (cs.display==='none'||cs.visibility==='hidden') return false; p = p.parentElement; } return true; };
  const sel = el => { let s = el.tagName.toLowerCase(); if (el.className && typeof el.className==='string') s += '.' + el.className.trim().split(/\s+/).join('.'); return s; };
  const seen = new Set();
  const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let n;
  while ((n = w.nextNode())) {
    const t = n.textContent.replace(/\s+/g, ' ').trim(); if (!t) continue;
    const el = n.parentElement; if (!el || ['SCRIPT','STYLE','NOSCRIPT'].includes(el.tagName)) continue;
    if (!vis(el)) continue;
    if (el.closest('.sr-only')) continue;
    const r = el.getBoundingClientRect(); if (r.width < 1 || r.height < 1) continue;
    const cs = getComputedStyle(el);
    out.push({sel: sel(el), t, tt: cs.textTransform, fs: cs.fontSize, lang: el.closest('[lang]')?.getAttribute('lang')});
    if (!seen.has(el)) { seen.add(el);
      if (el.scrollWidth > el.clientWidth + 1 && cs.overflow !== 'visible') issues.push({k:'overflow-clip', sel: sel(el), t, sw: el.scrollWidth, cw: el.clientWidth});
      if (cs.textOverflow === 'ellipsis' || cs.webkitLineClamp !== 'none') issues.push({k:'ellipsis/clamp', sel: sel(el), t});
      // horizontal: outside viewport and not in a horizontal track/carousel
      const inTrack = el.closest('[data-track],[data-swipe],.rincones,.eq,.rs');
      if (!inTrack && (r.right > vw + 1 || r.left < -1)) issues.push({k:'offscreen-x', sel: sel(el), t, l: Math.round(r.left), r: Math.round(r.right)});
      // word broken mid-word? range rects per word
      const rg = document.createRange(); const words = [...n.textContent.matchAll(/\S+/g)];
      for (const m of words) { rg.setStart(n, m.index); rg.setEnd(n, m.index + m[0].length); const rs = rg.getClientRects();
        if (rs.length > 1) { const tops = new Set([...rs].map(x => Math.round(x.top))); if (tops.size > 1) issues.push({k:'word-split', sel: sel(el), w: m[0]}); } }
    }
  }
  return {out, issues, sw: document.documentElement.scrollWidth, vw};
}
"""

async def run():
    res = {}
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=CH, args=["--no-sandbox", "--autoplay-policy=no-user-gesture-required"])
        for vk, W, H in VPS:
            for lang in ("es", "en"):
                for pk, url in PAGES:
                    ctx = await b.new_context(viewport={"width": W, "height": H}, device_scale_factor=1)
                    pg = await ctx.new_page()
                    await pg.goto(url, wait_until="networkidle")
                    await pg.wait_for_timeout(2500)
                    if lang == "en":
                        btn = pg.locator("[data-lang]")
                        if await btn.count():
                            try:
                                await btn.first.click(timeout=3000)
                            except Exception:
                                await pg.evaluate("document.querySelector('[data-lang]').click()")
                            await pg.wait_for_timeout(800)
                    total = await pg.evaluate("document.documentElement.scrollHeight")
                    y, i = 0, 0
                    while y < total and i < 60:
                        await pg.evaluate(f"window.scrollTo(0,{y})")
                        await pg.mouse.wheel(0, 1); await pg.wait_for_timeout(1100)
                        await pg.screenshot(path=f"{OUT}/{pk}-{vk}-{lang}-{i:02d}.jpg", quality=60, type="jpeg")
                        i += 1; y += int(H * 0.9)
                        total = await pg.evaluate("document.documentElement.scrollHeight")
                    # final extraction at bottom then at top (reveals done)
                    await pg.evaluate("window.scrollTo(0,0)"); await pg.wait_for_timeout(600)
                    data = await pg.evaluate(EXTRACT)
                    data["shots"] = i; data["lang"] = await pg.evaluate("document.documentElement.lang")
                    res[f"{pk}-{vk}-{lang}"] = data
                    await ctx.close()
        await b.close()
    json.dump(res, open(f"{OUT}/dom.json", "w"), ensure_ascii=False, indent=1)
    for k, v in res.items():
        print(k, "shots", v["shots"], "lang", v["lang"], "sw", v["sw"], "vw", v["vw"], "issues", len(v["issues"]))

asyncio.run(run())
