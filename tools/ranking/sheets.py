import pandas as pd, os
from PIL import Image, ImageDraw, ImageFont
ROOT = '/home/claude/almud_bar/'
OUT = ROOT + '_plan/diag/top60/'
SP = '/tmp/claude-0/-home-claude/011b3bf8-fa11-50bd-ba3e-4cc567dfb832/scratchpad/'
FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf', 15)
FN = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed.ttf', 13)
FH = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf', 22)
RAT = {'4:5': .8, '16:9': 16/9, '1:1': 1, '3:4': .75, '9:16': 9/16}
top = pd.read_csv(SP + 'top.csv')

def path(f):
    return ROOT + ('assets/raw/' + f if not f.startswith('_plan') else f)

def crop(im, ratio, fx, fy):
    W, H = im.size; r = RAT[ratio]
    if W / H > r: h = H; w = int(H * r)
    else: w = W; h = int(W / r)
    cx, cy = W * fx / 100, H * fy / 100
    x = int(min(max(cx - w / 2, 0), W - w)); y = int(min(max(cy - h / 2, 0), H - h))
    return im.crop((x, y, x + w, y + h))

def tile(r, tw, th, lab_h, lines):
    im = Image.open(path(r['file'])).convert('RGB')
    c = crop(im, r['crop'], r['fx'], r['fy']); c.thumbnail((tw, th), Image.LANCZOS)
    t = Image.new('RGB', (tw, th + lab_h), (20, 14, 18))
    t.paste(c, ((tw - c.width) // 2, (th - c.height) // 2))
    d = ImageDraw.Draw(t)
    y = th + 4
    for i, ln in enumerate(lines):
        d.text((6, y), ln, font=FB if i == 0 else FN, fill=(245, 198, 88) if i == 0 else (235, 225, 215)); y += 17
    return t

def likes(r):
    return '—' if pd.isna(r['likes_norm']) else f"x{r['likes_norm']:.2f}"

def grid(rows, cols, tw, th, lab_h, fn, title, labeller):
    n = len(rows); R = (n + cols - 1) // cols
    sh = Image.new('RGB', (cols * tw + (cols + 1) * 6, 40 + R * (th + lab_h + 6)), (8, 6, 8))
    d = ImageDraw.Draw(sh); d.text((8, 8), title, font=FH, fill='white')
    for i, (_, r) in enumerate(rows.iterrows()):
        t = tile(r, tw, th, lab_h, labeller(r))
        sh.paste(t, (6 + (i % cols) * (tw + 6), 40 + (i // cols) * (th + lab_h + 6)))
    q = 75
    while True:
        sh.save(fn, quality=q, optimize=True)
        if os.path.getsize(fn) < 600_000: break
        sh = sh.resize((int(sh.width * .93), int(sh.height * .93)), Image.LANCZOS)
    print(fn, sh.size, os.path.getsize(fn) // 1024, 'KB q', q)

lab = lambda r: [f"#{r['rank']}  {r['ref']}  {r['score']:.1f}",
                 f"{r['file'].split('/')[-1][:30]}",
                 f"{r['bucket']} · ♥{likes(r)}",
                 f"{r['crop']} @{r['fx']},{r['fy']} · max {r['max_w']}px"]
grid(top[top['rank'] <= 30], 6, 300, 375, 74, OUT + 'ranking_1-30.jpg', 'Almud v2 · ranking 1–30 (recorte propuesto aplicado)', lab)
grid(top[top['rank'] > 30], 6, 300, 375, 74, OUT + 'ranking_31-60.jpg', 'Almud v2 · ranking 31–60 (recorte propuesto aplicado)', lab)

# coverage: best 2 per bucket among top60
order = ['barra', 'equipo/personal', 'patio techado', 'terraza descubierta', 'mesas interiores', 'sillones', 'cuadros/murales',
         'tragos', 'comida', 'fiestas/eventos', 'fachada/letrero', 'vista/Castro', 'dueños']
cov = pd.concat([top[top.bucket == b].sort_values('score', ascending=False).head(2) for b in order])
labc = lambda r: [f"{r['bucket'].upper()}", f"#{r['rank']} {r['ref']} · {r['score']:.1f}", f"{r['crop']} · max {r['max_w']}px"]
grid(cov, 6, 300, 375, 58, OUT + 'coverage.jpg', 'Almud v2 · cobertura: las 2 mejores por espacio', labc)

# heroes
H = [('V031-f01', '16:9', 55, 40, 'V031 loop 1,0–10,4 s · poster 0,9 s', 'DFWLrRxyvVB_00.mp4 · 1278×720 · max 1278'),
     ('V009-f01', '9:16', 50, 45, 'V009 loop 0–7,1 s (móvil)', 'C5WAi8PLHni_00.mp4 · 720×1280 · max 720'),
     ('P189', '16:9', 50, 38, 'P189 · techo de banderines', '1440×1919 · 16:9 → max 1440'),
     ('P362', '16:9', 50, 40, 'P362 · muro rojo + cartel ALMUD', '3072×4096 · 16:9 → max 3072 (único héroe real)'),
     ('P090', '16:9', 50, 40, 'P090 · faroles y flecos', '1440×1708 · 16:9 → max 1440'),
     ('P093', '16:9', 50, 55, 'P093 · barra curva', '1440×1701 · 16:9 → max 1440'),
     ('P124', '16:9', 45, 38, 'P124 · la botella en el aire', '1068×714 · 16:9 → max 1068'),
     ('P348', '16:9', 50, 45, 'P348 · 12 años desde arriba (violeta)', '3072×4096 · 16:9 → max 3072')]
allc = pd.concat([top, pd.read_csv(SP + 'rest.csv')]).drop_duplicates('ref').set_index('ref')
rows = []
for i, (ref, cr, fx, fy, a, b) in enumerate(H):
    r = allc.loc[ref].copy(); r['crop'] = cr; r['fx'] = fx; r['fy'] = fy; r['a'] = a; r['b'] = b; r['i'] = i + 1
    rows.append(r)
hr = pd.DataFrame(rows)
labh = lambda r: [f"H{r['i']}  {r['a']}", r['b']]
grid(hr, 2, 800, 450, 42, OUT + 'heroes.jpg', 'Almud v2 · 8 candidatas a portada (recorte de portada aplicado)', labh)
