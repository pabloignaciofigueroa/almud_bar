import asyncio
from playwright.async_api import async_playwright
OUT="/home/claude/almud_bar/_plan/v3/ronda1/voz"
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",args=["--no-sandbox"])
    pg=await (await b.new_context(viewport={"width":390,"height":844},has_touch=False)).new_page()
    await pg.goto("http://localhost:8841/v3/",wait_until="networkidle"); await pg.wait_for_timeout(2500)
    await pg.mouse.move(200,400)
    for i in range(30):
      await pg.mouse.wheel(0,60); await pg.wait_for_timeout(450)
      r=await pg.evaluate("""()=>{const a=document.querySelector('.hero__btns .btn').getBoundingClientRect();
        return {sy:scrollY|0,btn:[a.top|0,a.bottom|0], past:document.documentElement.classList.contains('is-past')}}""")
      print(i,r)
      if -10 < r['btn'][0] < 50: await pg.screenshot(path=f"{OUT}/home-m-es-overlap-w{i:02d}.jpg",type="jpeg",quality=70)
    await b.close()
asyncio.run(main())
