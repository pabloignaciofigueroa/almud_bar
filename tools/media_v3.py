#!/usr/bin/env python3
"""Medios v3 (fase 7): imágenes AVIF/WebP y loops MP4 (H.264) + WebM (VP9) desde el material propio de Almud.

Lee tools/media_v3.json y escribe:
  assets/v3/img/<id>-<crop>-<w>.{avif,webp}
  assets/v3/video/<id>-<w>.{mp4,webm} y <id>-poster.{avif,webp,jpg}   (póster = primer frame del loop)
  assets/v3/media.json                                                 (lo consume el build v3)
Con --qa escribe además la hoja de contacto _plan/v3/07-medios.jpg y la tabla _plan/v3/07-medios.md.

Reglas: nunca se amplía (solo anchos <= ancho real del recorte); sRGB; unsharp suave solo tras reducir; videos sin audio,
faststart, 720p máx. salvo fuente 1080p que lo valga; cada loop se codifica al mayor ancho que cumple su presupuesto con
CRF <= crf_max. No toca assets/img, assets/v2 ni el sitio.

Uso: python3 tools/media_v3.py [--force] [--only id1,id2] [--no-video] [--no-img] [--qa]
"""
import base64, csv, io, json, os, re, subprocess, sys
from PIL import Image, ImageCms, ImageFilter, ImageOps, ImageStat, ImageChops

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAN = os.path.join(ROOT, 'tools/media_v3.json')
OUT_IMG = os.path.join(ROOT, 'assets/v3/img')
OUT_VID = os.path.join(ROOT, 'assets/v3/video')
OUT_JSON = os.path.join(ROOT, 'assets/v3/media.json')
QA_JPG = os.path.join(ROOT, '_plan/v3/07-medios.jpg')
QA_MD = os.path.join(ROOT, '_plan/v3/07-medios.md')
SRGB = ImageCms.createProfile('sRGB')

ARGS = sys.argv[1:]
FORCE = '--force' in ARGS
ONLY = set(ARGS[ARGS.index('--only') + 1].split(',')) if '--only' in ARGS else None


def rel(p):
    return os.path.relpath(p, ROOT)


def fresh(out, *deps):
    if FORCE or not os.path.exists(out):
        return False
    m = os.path.getmtime(out)
    return all(os.path.getmtime(d) < m for d in deps)


# ---------- post y crédito ----------
POSTS = {p['code']: p for p in json.load(open(os.path.join(ROOT, 'content/ig_posts.json'), encoding='utf-8'))}


def post_of(src):
    m = re.match(r'(.+)_\d\d\.(jpg|mp4)$', os.path.basename(src))
    p = POSTS.get(m.group(1)) if m else None
    return (p['id'], p['code'], p['date']) if p else (None, None, None)


def credit_for(a, credits):
    pid, code, date = post_of(a['src'])
    pid = a.get('post_override', pid)
    c = {'post': pid, 'date': date, 'url': f'https://www.instagram.com/p/{code}/' if code else None, 'account': '@almud_bar'}
    photo = a.get('credit') or credits.get(pid)
    if photo:
        c['photo'] = photo
        c['text'] = f'Foto: {photo} para @almud_bar' if not a['src'].endswith('.mp4') else f'Video: {photo} para @almud_bar'
    else:
        c['text'] = '@almud_bar'
    if a.get('handle'):
        c['person'] = a['handle']
    return c


# ---------- imagen ----------
def load_srgb(path):
    im = Image.open(path)
    im = ImageOps.exif_transpose(im)
    icc = im.info.get('icc_profile')
    if icc:
        try:
            src = ImageCms.ImageCmsProfile(io.BytesIO(icc))
            if 'srgb' not in (ImageCms.getProfileDescription(src) or '').lower():
                im = ImageCms.profileToProfile(im.convert('RGB'), src, SRGB, renderingIntent=0, outputMode='RGB')
        except Exception as e:
            print('  icc ignorado', path, e)
    return im.convert('RGB')


def crop_box(W, H, ratio, focal):
    if ratio == 'orig':
        return (0, 0, W, H)
    rw, rh = (float(x) for x in ratio.split(':'))
    r = rw / rh
    if W / H > r:
        cw, ch = round(H * r), H
    else:
        cw, ch = W, round(W / r)
    fx, fy = focal[0] / 100 * W, focal[1] / 100 * H
    x0 = int(min(max(fx - cw / 2, 0), W - cw))
    y0 = int(min(max(fy - ch / 2, 0), H - ch))
    return (x0, y0, x0 + cw, y0 + ch)


def resize(im, w):
    if im.width <= w:
        return im  # nunca se amplía
    h = round(im.height * w / im.width)
    out = im.resize((w, h), Image.LANCZOS, reducing_gap=3.0)
    scale = w / im.width
    if scale < 0.95:
        out = out.filter(ImageFilter.UnsharpMask(radius=0.6 if scale > 0.5 else 0.8, percent=45, threshold=3))
    return out


def lqip(im):
    t = im.copy()
    t.thumbnail((24, 24), Image.LANCZOS)
    t = t.filter(ImageFilter.GaussianBlur(0.6))
    b = io.BytesIO()
    t.save(b, 'WEBP', quality=35, method=6)
    small = im.copy()
    small.thumbnail((64, 64))
    med = ImageStat.Stat(small).median
    return 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode(), '#%02x%02x%02x' % tuple(int(c) for c in med[:3])


def save(im, path, fmt, q):
    if fmt == 'avif':
        im.save(path, 'AVIF', quality=q['avif'], speed=4, subsampling='4:2:0')
    elif fmt == 'webp':
        im.save(path, 'WEBP', quality=q['webp'], method=6)
    elif fmt == 'jpg':
        im.save(path, 'JPEG', quality=q.get('jpg', 82), optimize=True, progressive=True, subsampling='4:2:0')


def common(a, credits):
    e = {'ref': a['ref'], 'src': a['src'], 'section': a['section'], 'alt': a['alt'], 'credit': credit_for(a, credits)}
    for k in ('rincon', 'evento', 'carta_item', 'handle', 'tag_src', 'status', 'optional', 'variant', 'note'):
        if a.get(k) is not None:
            e[k] = a[k]
    return e


def do_image(a, M, credits):
    q = dict(M['quality'], **a.get('quality', {}))
    src = os.path.join(ROOT, a['src'])
    im = load_srgb(src)
    W, H = im.size
    e = common(a, credits)
    e['source_size'] = [W, H]
    e['crops'] = {}
    for c in a['crops']:
        box = crop_box(W, H, c['ratio'], c.get('focal', [50, 50]))
        cr = im.crop(box)
        cw = cr.width
        cap = min(cw, c.get('max', 10 ** 6))
        if c.get('widths'):
            widths = [w for w in c['widths'] if w <= cap] or [cap]
        else:
            widths = [w for w in M['widths'] if w <= cap] or [cap]
        if cap - widths[-1] >= 64:  # ancho nativo del recorte si los estándar se quedan cortos
            widths.append(cap)
        widths = sorted(set(widths))
        files = {'avif': {}, 'webp': {}}
        for w in widths:
            out = None
            for f in ('avif', 'webp'):
                p = os.path.join(OUT_IMG, f"{a['id']}-{c['name']}-{w}.{f}")
                if not fresh(p, src, MAN):
                    out = out or resize(cr, w)
                    save(out, p, f, q)
                files[f][str(w)] = {'path': rel(p), 'bytes': os.path.getsize(p)}
        wmax = widths[-1]
        lq, dom = lqip(cr)
        e['crops'][c['name']] = {'ratio': c['ratio'] if c['ratio'] != 'orig' else f'{W}:{H}', 'focal': c.get('focal', [50, 50]),
                                 'box': list(box), 'crop_size': [cw, cr.height], 'width': wmax,
                                 'height': round(cr.height * wmax / cw), 'widths': widths, 'lqip': lq, 'color': dom,
                                 'files': files}
    return e


# ---------- video ----------
def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(' '.join(cmd) + '\n' + r.stderr[-2000:])
    return r


def ff(*a):
    run(['ffmpeg', '-v', 'error', '-y', *a])


def probe(path):
    o = run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height,r_frame_rate',
             '-of', 'json', path]).stdout
    s = json.loads(o)['streams'][0]
    return s['width'], s['height'], s['r_frame_rate']


def nframes(path):
    o = run(['ffprobe', '-v', 'error', '-count_frames', '-select_streams', 'v:0', '-show_entries', 'stream=nb_read_frames',
             '-of', 'csv=p=0', path]).stdout
    return int(o.strip())


COLOR = ['-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv']


def make_master(v, src, W, H, rate):
    """Concatena tramos, recorta y arma el loop en un máster sin pérdida a resolución de recorte. Devuelve (ruta, w, h)."""
    x0, y0, x1, y1 = crop_box(W, H, v['ratio'], v['focal'])
    cw, ch = (x1 - x0) // 2 * 2, (y1 - y0) // 2 * 2
    cropf = f'crop={cw}:{ch}:{x0}:{y0},' if (cw, ch) != (W, H) else ''
    segs = v['segments']
    parts, labels = [], []
    for i, (s, e) in enumerate(segs):
        sp = v.get('speed')  # cámara lenta opcional (p. ej. 0.8): frames intermedios por mezcla
        tempo = f'setpts=(PTS-STARTPTS)/{sp},framerate=fps={rate}' if sp else f'setpts=PTS-STARTPTS,fps={rate}'
        parts.append(f'[0:v]trim={s}:{e},{tempo},{cropf}format=yuv420p[s{i}]')
        labels.append(f'[s{i}]')
    if len(segs) > 1:
        parts.append(f"{''.join(labels)}concat=n={len(segs)}:v=1:a=0[c]")
    else:
        parts[-1] = parts[-1].replace('[s0]', '[c]')
    base = os.path.join(OUT_VID, v['id'])
    lin = base + '.lin.mkv'
    ff('-i', src, '-filter_complex', ';'.join(parts), '-map', '[c]', '-an', '-c:v', 'ffv1', lin)
    n = nframes(lin)
    num, den = (float(x) for x in rate.split('/'))
    fps = num / den
    mid = base + '.master.mkv'
    if v['loop'] == 'boomerang':
        # ida + vuelta sin repetir el primer ni el último frame (la costura no se congela)
        g = (f'[0:v]split[a][b];[b]reverse,trim=start_frame=1:end_frame={n - 1},setpts=PTS-STARTPTS[r];'
             f'[a][r]concat=n=2:v=1:a=0[out]')
    elif v['loop'] == 'crossfade':
        d = v['xfade']
        dn = round(d * fps)
        dur = n / fps
        g = (f'[0:v]split[a][b];[a]trim=start_frame={dn},setpts=PTS-STARTPTS[t];'
             f'[b]trim=end_frame={dn},setpts=PTS-STARTPTS[h];'
             f'[t][h]xfade=transition=fade:duration={dn / fps:.4f}:offset={dur - 2 * dn / fps:.4f}[out]')
    else:
        g = '[0:v]null[out]'
    ff('-i', lin, '-filter_complex', g, '-map', '[out]', '-an', '-c:v', 'ffv1', mid)
    os.remove(lin)
    return mid, cw, ch, fps


def seam_diff(mid):
    """Diferencia media (0–255) entre el último y el primer frame del loop: mide si la costura salta."""
    tmp = mid + '.%d.png'
    n = nframes(mid)
    ff('-i', mid, '-vf', f"select='eq(n\\,0)+eq(n\\,{n - 1})'", '-vsync', '0', tmp)
    a, b = Image.open(mid + '.1.png').convert('L'), Image.open(mid + '.2.png').convert('L')
    st = ImageStat.Stat(ImageChops.difference(a, b)).mean[0]
    # referencia: diferencia típica entre frames consecutivos al 25 % y al 75 % del loop
    refs = []
    for k in (n // 4, 3 * n // 4):
        ff('-i', mid, '-vf', f"select='eq(n\\,{k})+eq(n\\,{k + 1})'", '-vsync', '0', tmp)
        c, d = Image.open(mid + '.1.png').convert('L'), Image.open(mid + '.2.png').convert('L')
        refs.append(ImageStat.Stat(ImageChops.difference(c, d)).mean[0])
    ref = sum(refs) / len(refs)
    for i in (1, 2):
        os.remove(mid + f'.{i}.png')
    return round(st, 2), round(ref, 2), n


def enc_mp4(mid, out, tw, th, cw, crf):
    vf = f'scale={tw}:{th}:flags=lanczos,unsharp=5:5:0.3:5:5:0.0,format=yuv420p' if tw < cw else 'format=yuv420p'
    ff('-i', mid, '-an', '-vf', vf, '-c:v', 'libx264', '-preset', 'slower', '-crf', str(crf), '-profile:v', 'high',
       '-level', '4.1' if th > 1280 or tw > 1280 else '4.0', '-tune', 'film', '-x264-params', 'keyint=60:min-keyint=30',
       *COLOR, '-movflags', '+faststart', out)


def enc_webm(mid, out, tw, th, cw, crf):
    vf = f'scale={tw}:{th}:flags=lanczos,unsharp=5:5:0.3:5:5:0.0,format=yuv420p' if tw < cw else 'format=yuv420p'
    ff('-i', mid, '-an', '-vf', vf, '-c:v', 'libvpx-vp9', '-crf', str(crf), '-b:v', '0', '-deadline', 'good',
       '-cpu-used', '3', '-row-mt', '1', '-tile-columns', '1', '-g', '60', *COLOR, out)


def search(fn, mid, out, tw, th, cw, start, stop, budget):
    """Bisección: el CRF más bajo (mejor calidad) en [start, stop] que cabe en el presupuesto."""
    lo, hi, best, last = start, stop, None, None
    while lo <= hi:
        crf = (lo + hi) // 2
        fn(mid, out, tw, th, cw, crf)
        last = crf
        if os.path.getsize(out) <= budget:
            best, hi = crf, crf - 1
        else:
            lo = crf + 1
    if best is None:
        if last != stop:
            fn(mid, out, tw, th, cw, stop)
        return stop, False
    if last != best:
        fn(mid, out, tw, th, cw, best)  # el último intento no fue el elegido: reescribir
    return best, True


def do_video(v, credits):
    src = os.path.join(ROOT, v['src'])
    W, H, rate = probe(src)
    mid, cw, ch, fps = make_master(v, src, W, H, rate)
    seam, ref, n = seam_diff(mid)
    budget = v['budget_kb'] * 1024
    base = os.path.join(OUT_VID, v['id'])
    for f in os.listdir(OUT_VID):  # anchos de una corrida anterior
        if f.startswith(v['id'] + '-') and f.endswith(('.mp4', '.webm')):
            os.remove(os.path.join(OUT_VID, f))
    chosen = None
    for w in v['widths']:
        tw = min(w, cw) // 2 * 2
        th = round(ch * tw / cw) // 2 * 2
        mp4, webm = f'{base}-{tw}.mp4', f'{base}-{tw}.webm'
        c264, ok1 = search(enc_mp4, mid, mp4, tw, th, cw, v.get('crf_start', 21), v['crf_max'], budget)
        cvp9, ok2 = search(enc_webm, mid, webm, tw, th, cw, v.get('vp9_crf_start', 30), v['crf_max'] + 12, budget)
        print(f"  {v['id']} {tw}x{th}: mp4 crf{c264} {os.path.getsize(mp4) // 1024} KB, webm crf{cvp9} {os.path.getsize(webm) // 1024} KB",
              '' if ok1 and ok2 else '(no cumple; se prueba más chico)')
        chosen = (tw, th, mp4, webm, c264, cvp9, ok1 and ok2)
        if ok1 and ok2:
            break
        if w != v['widths'][-1]:
            os.remove(mp4); os.remove(webm)
    tw, th, mp4, webm, c264, cvp9, ok = chosen
    # póster = primer frame del loop (mismo encuadre y ancho que el video)
    png = base + '.poster.png'
    vf = f'scale={tw}:{th}:flags=lanczos' if tw < cw else 'null'
    ff('-i', mid, '-vf', f"select='eq(n\\,0)',{vf}", '-frames:v', '1', png)
    p = load_srgb(png)
    posters = {}
    for f, q in (('avif', {'avif': 50}), ('webp', {'webp': 74}), ('jpg', {'jpg': 80})):
        pp = f'{base}-poster.{f}'
        save(p, pp, f, q)
        posters[f] = {'path': rel(pp), 'bytes': os.path.getsize(pp)}
    lq, dom = lqip(p)
    os.remove(png)
    os.remove(mid)
    e = common(v, credits)
    e.update({'source_size': [W, H], 'width': tw, 'height': th, 'ratio': v['ratio'] if v['ratio'] != 'orig' else f'{W}:{H}',
              'segments': v['segments'], 'loop': v['loop'], 'frames': n, 'fps': round(fps, 3), 'duration': round(n / fps, 2),
              'muted': True, 'attrs': 'autoplay muted loop playsinline', 'budget_kb': v['budget_kb'], 'within_budget': ok,
              'seam': {'last_vs_first': seam, 'typical_step': ref},
              'files': {'webm': {'path': rel(webm), 'bytes': os.path.getsize(webm), 'type': 'video/webm; codecs="vp9"', 'crf': cvp9},
                        'mp4': {'path': rel(mp4), 'bytes': os.path.getsize(mp4), 'type': 'video/mp4; codecs="avc1.640028"', 'crf': c264}},
              'poster': posters, 'lqip': lq, 'color': dom})
    print(f"  -> {v['id']} {tw}x{th} {e['duration']} s, costura {seam} (paso típico {ref})")
    return e


def main():
    M = json.load(open(MAN, encoding='utf-8'))
    os.makedirs(OUT_IMG, exist_ok=True)
    os.makedirs(OUT_VID, exist_ok=True)
    old = json.load(open(OUT_JSON, encoding='utf-8')) if os.path.exists(OUT_JSON) else {}
    media = {'images': old.get('images', {}), 'videos': old.get('videos', {})}
    credits = M.get('credits', {})
    if '--no-img' not in ARGS:
        for a in M['images']:
            if ONLY and a['id'] not in ONLY:
                continue
            print('img', a['id'])
            media['images'][a['id']] = do_image(a, M, credits)
    if '--no-video' not in ARGS:
        for v in M['videos']:
            if ONLY and v['id'] not in ONLY:
                continue
            print('video', v['id'])
            media['videos'][v['id']] = do_video(v, credits)
    order_i = [a['id'] for a in M['images']]
    order_v = [v['id'] for v in M['videos']]
    out = {'_doc': ('Generado por tools/media_v3.py desde tools/media_v3.json. images[id].crops[name].files[avif|webp][ancho] = {path, bytes}; '
                    'width/height = intrínsecos del mayor ancho. videos[id].files: webm (VP9) primero, mp4 (H.264, faststart) de respaldo; '
                    'poster = primer frame del loop (avif/webp/jpg). alt.es/alt.en: solo Eventos nombra el evento. '
                    'status "por-confirmar" = Carmen debe aprobar antes de publicar.'),
           'images': {i: media['images'][i] for i in order_i if i in media['images']},
           'videos': {i: media['videos'][i] for i in order_v if i in media['videos']},
           'team_ig001': M.get('team_ig001'), 'rejected': M.get('rejected', [])}
    json.dump(out, open(OUT_JSON, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('ok', len(out['images']), 'imágenes,', len(out['videos']), 'videos ->', rel(OUT_JSON))


# ---------- QA: hoja de contacto + tabla ----------
SECTIONS = ['portada', 'lugar', 'tragos', 'comida', 'con-quien', 'eventos', 'equipo', 'donde', 'carta']
SEC_NAME = {'portada': '1 Portada', 'lugar': '2 El lugar', 'tragos': '3 Tragos', 'comida': '4 Comida', 'con-quien': '5 Con quién',
            'eventos': '6 Eventos', 'equipo': '7 Equipo', 'donde': '9 Dónde', 'carta': 'Carta destacada'}
K = lambda b: f"{b / 1024:,.0f}".replace(',', '.')


def pick(c, target):
    ws = c['widths']
    w = next((w for w in ws if w >= target), ws[-1])
    return w, c['files']['avif'][str(w)]['bytes']


def qa():
    from PIL import ImageDraw, ImageFont
    media = json.load(open(OUT_JSON, encoding='utf-8'))
    try:
        F = lambda s: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', s)
        FB = lambda s: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', s)
        font, small, big = F(15), F(13), FB(26)
    except OSError:
        font = small = big = ImageFont.load_default()
    by = {s: [] for s in SECTIONS}
    for i, e in media['videos'].items():
        by[e['section']].append(('v', i, e))
    for i, e in media['images'].items():
        by[e['section']].append(('i', i, e))
    CH, PAD, LAB, MAXW = 300, 14, 74, 2600
    blocks = []
    for s in SECTIONS:
        cells = []
        for kind, i, e in by[s]:
            if kind == 'v':
                im = Image.open(os.path.join(ROOT, e['poster']['jpg']['path'])).convert('RGB')
                l1 = f"▶ {i}" + (f" ({e.get('variant')})" if e.get('variant') else '')
                l2 = (f"{e['ref']} · {e['width']}x{e['height']} · {e['duration']} s {e['loop']}\n"
                      f"webm {K(e['files']['webm']['bytes'])} / mp4 {K(e['files']['mp4']['bytes'])} KB · póster {K(e['poster']['avif']['bytes'])} KB")
                cells.append((im, l1, l2, e.get('status'), True))
            else:
                for cn, c in e['crops'].items():
                    w = str(c['width'])
                    im = Image.open(os.path.join(ROOT, c['files']['webp'][w]['path'])).convert('RGB')
                    tag = e.get('evento') or e.get('handle') or e.get('rincon') or e.get('carta_item') or ''
                    l1 = f"{i} [{cn}]"
                    l2 = (f"{tag}\n" if tag else '') + f"{e['ref']} · {c['width']}x{c['height']} · avif {K(c['files']['avif'][w]['bytes'])} KB"
                    cells.append((im, l1, l2, e.get('status'), False))
        blocks.append((SEC_NAME[s], cells))
    # maquetar
    rows_layout, y = [], PAD
    for name, cells in blocks:
        rows_layout.append(('h', name, y)); y += 40
        x, row = PAD, []
        for c in cells:
            im = c[0].copy(); im.thumbnail((CH * 2, CH))
            w = max(im.width, 300)
            if x + w > MAXW - PAD and row:
                rows_layout.append(('r', row, y)); y += CH + LAB + PAD; x, row = PAD, []
            row.append((x, im) + c[1:]); x += w + PAD
        if row:
            rows_layout.append(('r', row, y)); y += CH + LAB + PAD
        y += 10
    sheet = Image.new('RGB', (MAXW, y + PAD), '#160d0b')
    d = ImageDraw.Draw(sheet)
    for kind, data, yy in rows_layout:
        if kind == 'h':
            d.text((PAD, yy + 4), data, fill='#f24350', font=big)
            continue
        for x, im, l1, l2, status, isv in data:
            sheet.paste(im, (x, yy))
            if isv:
                d.rectangle((x, yy, x + im.width - 1, yy + im.height - 1), outline='#2aa1f8', width=4)
            if status:
                d.rectangle((x, yy, x + 150, yy + 22), fill='#f24350'); d.text((x + 6, yy + 3), status.upper(), fill='#160d0b', font=small)
            cw = max(im.width, 300)
            fit = lambda t, f: t if d.textlength(t, font=f) <= cw else fit(t[:-2], f) if len(t) > 3 else t
            d.text((x, yy + CH + 6), fit(l1, font), fill='#f5e9db', font=font)
            for k, line in enumerate(l2.split('\n')):
                d.text((x, yy + CH + 28 + 17 * k), fit(line, small), fill='#c8af9c', font=small)
    sheet.save(QA_JPG, quality=80, optimize=True, progressive=True)
    print('hoja', rel(QA_JPG), sheet.size, os.path.getsize(QA_JPG) // 1024, 'KB')
    table(media)


def table(media):
    L = ['# Fase 7 · Medios v3 (imágenes y video)', '',
         'Generado por `python3 tools/media_v3.py --qa` desde `assets/v3/media.json` (manifiesto `tools/media_v3.json`). '
         'KB = 1024 bytes. Hoja de contacto: `_plan/v3/07-medios.jpg` (borde azul = póster de video; etiqueta rosa = por confirmar).', '',
         'Solo material propio de @almud_bar (fotógrafos encargados por el bar, acreditados). Sin terceros, sin exempleados, sin afiches ni texto encima; '
         'disfraces solo en Eventos. Ningún archivo se repite entre secciones. Nunca se amplía: el mayor ancho emitido es ≤ al recorte de la fuente.', '']
    # videos
    L += ['## Videos (loops)', '', '| id | sección | ref | tramo (s) | loop | salida | dur. | WebM VP9 | MP4 H.264 | póster AVIF/WebP/JPG | presupuesto | costura* |',
          '|---|---|---|---|---|---|---|---|---|---|---|---|']
    for i, v in media['videos'].items():
        segs = ' + '.join(f'{a}–{b}' for a, b in v['segments'])
        p = v['poster']
        L.append(f"| `{i}` | {SEC_NAME[v['section']]}{' · ' + v['variant'] if v.get('variant') else ''} | {v['ref']} | {segs} | {v['loop']} | "
                 f"{v['width']}x{v['height']} | {v['duration']} s | {K(v['files']['webm']['bytes'])} | {K(v['files']['mp4']['bytes'])} | "
                 f"{K(p['avif']['bytes'])} / {K(p['webp']['bytes'])} / {K(p['jpg']['bytes'])} | ≤{v['budget_kb']} {'pasa' if v['within_budget'] else 'NO PASA'} | "
                 f"{v['seam']['last_vs_first']} ({v['seam']['typical_step']}) |")
    L += ['', '*Costura: diferencia media de luminancia (0–255) entre el último y el primer frame del loop; entre paréntesis, la de dos frames '
          'consecutivos del mismo loop. Si la primera es del orden de la segunda, el salto no se nota.', '']
    # primer pantallazo
    pm = media['videos'].get('portada-celular')
    pd = media['videos'].get('portada-escritorio')
    if pm:
        worst = max(pm['files']['webm']['bytes'], pm['files']['mp4']['bytes'])
        tot = worst + pm['poster']['avif']['bytes'] + len(pm['lqip'])
        L += ['## Primer pantallazo', '', '| Pantalla | Qué carga | Peso | Tope |', '|---|---|---|---|',
              f"| Celular (<900 px) | póster AVIF {K(pm['poster']['avif']['bytes'])} + video {pm['width']}x{pm['height']} (el mayor de WebM/MP4: {K(worst)}) | "
              f"{K(tot)} KB | video ≤ 1.843 · pantallazo ≤ 1.536 KB: {'pasa' if tot <= 1.5 * 1024 * 1024 and worst <= 1.8 * 1024 * 1024 else 'NO PASA'} |"]
        if pd:
            worstd = max(pd['files']['webm']['bytes'], pd['files']['mp4']['bytes'])
            L.append(f"| Escritorio (≥900 px) | póster AVIF {K(pd['poster']['avif']['bytes'])} + video {pd['width']}x{pd['height']} ({K(worstd)}) | "
                     f"{K(worstd + pd['poster']['avif']['bytes'])} KB | video ≤ 2.560 KB: {'pasa' if worstd <= 2.5 * 1024 * 1024 else 'NO PASA'} |")
        L += ['', 'Fuentes, CSS, logo y JS van aparte (los cuenta el build). El `<video>` lleva `preload="auto"` solo en la variante que corresponde '
              'al ancho (`<source media>` no aplica a video en todos los navegadores: el build debe elegir la fuente por JS mínimo o servir dos `<video>` con '
              '`display:none` + `preload="none"` en el oculto).', '']
    # imágenes
    L += ['## Imágenes', '', '| id | sección | rincón / evento / @ / ítem | ref · post | fuente | recorte | anchos | celular AVIF¹ | mayor AVIF | mayor WebP | crédito | estado |',
          '|---|---|---|---|---|---|---|---|---|---|---|---|']
    nfiles = disk = 0
    for s in SECTIONS:
        for i, e in media['images'].items():
            if e['section'] != s:
                continue
            for cn, c in e['crops'].items():
                w = str(c['width'])
                pw, pb = pick(c, 720)
                disk += sum(f['bytes'] for fm in c['files'].values() for f in fm.values())
                nfiles += sum(len(fm) for fm in c['files'].values())
                tag = e.get('evento') or e.get('handle') or e.get('rincon') or e.get('carta_item') or ''
                cr = e['credit']
                L.append(f"| `{i}` [{cn}] | {SEC_NAME[s]} | {tag} | {e['ref']} · {cr.get('post') or '—'} | {e['source_size'][0]}x{e['source_size'][1]} | "
                         f"{c['ratio']} | {'/'.join(map(str, c['widths']))} | {pw}: {K(pb)} | {c['width']}: {K(c['files']['avif'][w]['bytes'])} | "
                         f"{K(c['files']['webp'][w]['bytes'])} | {cr.get('photo') or '@almud_bar'} | {e.get('status') or 'ok'}{' (opcional)' if e.get('optional') else ''} |")
    L += ['', f'¹ Celular = AVIF del menor ancho ≥ 720 px (tarjeta de ~360 css a DPR 2). Total: {nfiles} archivos de imagen, {K(disk)} KB en disco.', '']
    # alts
    L += ['## Alt (ES / EN)', '']
    for s in SECTIONS:
        L.append(f'**{SEC_NAME[s]}**')
        for coll in ('videos', 'images'):
            for i, e in media[coll].items():
                if e['section'] == s:
                    L.append(f"- `{i}`: {e['alt']['es']} / *{e['alt']['en']}*")
        L.append('')
    L += ['## Notas de selección', '']
    for coll in ('videos', 'images'):
        for i, e in media[coll].items():
            if e.get('note'):
                L.append(f"- `{i}`: {e['note']}")
    L += ['', '## Descartes', ''] + [f"- {r['ref']}: {r['reason']}" for r in media.get('rejected', [])] + ['']
    open(QA_MD, 'w', encoding='utf-8').write('\n'.join(L))
    print('tabla', rel(QA_MD))


if __name__ == '__main__':
    if '--qa' in ARGS and len([a for a in ARGS if a != '--qa']) == 0:
        qa()
    else:
        main()
        if '--qa' in ARGS:
            qa()
