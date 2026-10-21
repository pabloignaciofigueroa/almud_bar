"""Render del style tile a 1440 y 390 (página completa) -> JPEG q78, partido si es muy alto."""
import sys, os
from playwright.sync_api import sync_playwright
from PIL import Image
D = os.path.dirname(os.path.abspath(__file__))
def run(w, h, name):
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args=['--no-sandbox', '--allow-file-access-from-files'])
        pg = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=1)
        pg.goto('file://' + D + '/index.html'); pg.wait_for_load_state('networkidle'); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(800)
        png = '/tmp/claude-0/-home-claude/011b3bf8-fa11-50bd-ba3e-4cc567dfb832/scratchpad/' + name + '.png'
        pg.screenshot(path=png, full_page=True); b.close()
    im = Image.open(png).convert('RGB'); W, H = im.size
    parts = 1 if H <= 5200 else 2
    for i in range(parts):
        y0 = H * i // parts; y1 = H * (i + 1) // parts
        out = os.path.join(D, name + ('' if parts == 1 else f'-{i+1}') + '.jpg')
        im.crop((0, y0, W, y1)).save(out, 'JPEG', quality=78, optimize=True, progressive=True)
        print(out, W, y1 - y0, os.path.getsize(out) // 1024, 'KB')
for a in sys.argv[1:] or ['1440', '390']:
    run(int(a), 900 if a == '1440' else 844, 'tile-' + a)
