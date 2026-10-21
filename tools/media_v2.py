#!/usr/bin/env python3
"""Medios v2 (fase 10): imágenes AVIF/WebP (+JPEG solo og) y reels H.264/AV1 desde los crudos de Almud.

Lee tools/media_v2.json y escribe:
  assets/v2/img/<id>-<crop>-<w>.{avif,webp}   (og: <id>.jpg)
  assets/v2/video/<id>.mp4 (+ .webm AV1 si es más liviano) y <id>-poster.{avif,webp}
  assets/v2/media.json                         (lo consume el build)
Reglas: nunca se amplía (solo anchos <= ancho real del recorte), sRGB, unsharp suave solo tras reducir,
sin denoise. No toca assets/img ni assets/video (v1, tools/media.py).

Uso: python3 tools/media_v2.py [--force] [--only id1,id2] [--no-video] [--no-img]
"""
import base64, csv, io, json, os, subprocess, sys
from PIL import Image, ImageCms, ImageFilter, ImageOps, ImageStat

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAN = os.path.join(ROOT, 'tools/media_v2.json')
OUT_IMG = os.path.join(ROOT, 'assets/v2/img')
OUT_VID = os.path.join(ROOT, 'assets/v2/video')
OUT_JSON = os.path.join(ROOT, 'assets/v2/media.json')
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


# ---------- catálogo (alt placeholder) ----------
CAT = {}
for r in csv.DictReader(open(os.path.join(ROOT, '_plan/diag/catalogo.csv'), encoding='utf-8')):
    CAT.setdefault(r['ref'], r)


def alt_for(a):
    if a.get('alt'):
        return a['alt']
    r = CAT.get(a.get('catalog_ref') or a['ref'])
    d = (r or {}).get('descripcion', '')
    return d.split(': ', 1)[1] if d.startswith('Portada (frame)') and ': ' in d else d


def post_for(a):
    r = CAT.get(a.get('catalog_ref') or a['ref'])
    return a.get('post') or (r or {}).get('post_id')


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
        except Exception as e:  # perfil roto: se asume sRGB
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


def resize(im, w, h=None):
    if im.width <= w and (h is None or im.height <= h):
        return im  # nunca se amplía
    h = h or round(im.height * w / im.width)
    out = im.resize((w, h), Image.LANCZOS, reducing_gap=3.0)
    scale = w / im.width
    if scale < 0.95:  # unsharp suave solo tras reducir; sin denoise
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
    mean = ImageStat.Stat(small).median
    return 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode(), '#%02x%02x%02x' % tuple(int(c) for c in mean[:3])


def save(im, path, fmt, q):
    if fmt == 'avif':
        im.save(path, 'AVIF', quality=q['avif'], speed=4, subsampling='4:2:0')
    elif fmt == 'webp':
        im.save(path, 'WEBP', quality=q['webp'], method=6)
    elif fmt == 'jpg':
        im.save(path, 'JPEG', quality=q['jpg'], optimize=True, progressive=True, subsampling='4:2:0')


def do_image(a, M, credits):
    q = dict(M['quality'], **a.get('quality', {}))
    src = os.path.join(ROOT, a['src'])
    im = load_srgb(src)
    W, H = im.size
    fmts = a.get('formats', ['avif', 'webp'])
    entry = {'ref': a['ref'], 'src': a['src'], 'section': a['section'], 'source_size': [W, H],
             'alt_placeholder': alt_for(a), 'post': post_for(a), 'crops': {}}
    post = entry['post']
    entry['credit'] = credits.get(post) if post else None
    for k in ('note', 'credit_note', 'fallback'):
        if a.get(k):
            entry[k] = a[k]
    for c in a['crops']:
        box = crop_box(W, H, c['ratio'], c.get('focal', [50, 50])) if 'size' not in c else None
        if 'size' in c:  # tamaño fijo (og)
            tw, th = c['size']
            box = crop_box(W, H, f'{tw}:{th}', c['focal'])
            cr = im.crop(box)
            out = resize(cr, tw, th) if cr.width > tw else cr
            p = os.path.join(OUT_IMG, f"{a['id']}.jpg")
            save(out, p, 'jpg', q)
            entry['crops'][c['name']] = {'ratio': c['ratio'], 'focal': c['focal'], 'box': box, 'width': out.width,
                                         'height': out.height, 'files': {'jpg': {str(out.width): {'path': rel(p), 'bytes': os.path.getsize(p)}}}}
            continue
        cr = im.crop(box)
        cw = cr.width
        cap = min(cw, a.get('cap', 10 ** 6), c.get('max', 10 ** 6))
        if c.get('widths'):  # fase 16: anchos propios del recorte (p. ej. la portada del teléfono)
            widths = [w for w in c['widths'] if w <= cw] or [cw]
        else:
            widths = [w for w in M['widths'] if w <= cap] or [cw]
            if cap - widths[-1] >= 64:  # fase 16: el ancho nativo del recorte, si los estándar se quedan cortos (nunca se amplía)
                widths.append(cap)
        widths = sorted(set(widths) | {w for w in a.get('extra_widths', []) if w < widths[0]})
        qc = dict(q, **c.get('quality', {}))
        files = {f: {} for f in fmts}
        for w in widths:
            out = None
            for f in fmts:
                p = os.path.join(OUT_IMG, f"{a['id']}-{c['name']}-{w}.{f}")
                if not fresh(p, src, MAN):
                    out = out or resize(cr, w)
                    save(out, p, f, qc)
                files[f][str(w)] = {'path': rel(p), 'bytes': os.path.getsize(p)}
        wmax = widths[-1]
        hmax = round(cr.height * wmax / cw)
        lq, dom = lqip(cr)
        entry['crops'][c['name']] = {'ratio': c['ratio'], 'focal': c.get('focal', [50, 50]), 'box': list(box),
                                     'crop_size': [cw, cr.height], 'width': wmax, 'height': hmax,
                                     'widths': widths, 'lqip': lq, 'color': dom, 'files': files}
    return entry


# ---------- video ----------
def ff(*a):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *a], check=True)


def probe(path):
    o = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height,r_frame_rate',
                        '-of', 'json', path], capture_output=True, text=True, check=True)
    s = json.loads(o.stdout)['streams'][0]
    n, d = s['r_frame_rate'].split('/')
    return s['width'], s['height'], float(n) / float(d)


def vfilter(v, W, H):
    """Recorte + escala (sin ampliar) + unsharp suave si se reduce. Devuelve (filtro, w, h)."""
    x0, y0, x1, y1 = crop_box(W, H, v['ratio'], v['focal'])
    cw, ch = x1 - x0, y1 - y0
    tw = min(v['width'], cw)
    tw -= tw % 2
    th = round(ch * tw / cw)
    th -= th % 2
    f = []
    if (cw, ch) != (W, H):
        f.append(f'crop={cw}:{ch}:{x0}:{y0}')
    if tw < cw:
        f.append(f'scale={tw}:{th}:flags=lanczos')
        f.append('unsharp=5:5:0.35:5:5:0.0')
    elif (cw, ch) != (tw, th):
        f.append(f'scale={tw}:{th}:flags=lanczos')
    f.append('format=yuv420p')
    return ','.join(f), tw, th


def build_graph(v, W, H):
    base, tw, th = vfilter(v, W, H)
    s, e = v['start'], v['end']
    if v['loop'] == 'boomerang':
        g = (f"[0:v]trim={s}:{e},setpts=PTS-STARTPTS,{base},split[a][b];"
             f"[b]reverse,trim=start_frame=1,setpts=PTS-STARTPTS[r];[a][r]concat=n=2:v=1:a=0[out]")
        dur = 2 * (e - s)
    elif v['loop'] == 'crossfade':
        d = v['xfade']
        g = (f"[0:v]trim={s + d}:{e},setpts=PTS-STARTPTS,{base}[a];"
             f"[0:v]trim={s}:{s + d},setpts=PTS-STARTPTS,{base}[b];"
             f"[a][b]xfade=transition=fade:duration={d}:offset={e - s - 2 * d:.3f}[out]")
        dur = e - s - d
    else:
        g = f"[0:v]trim={s}:{e},setpts=PTS-STARTPTS,{base}[out]"
        dur = e - s
    return g, tw, th, dur


COLOR = ['-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv']


def do_video(v):
    src = os.path.join(ROOT, v['src'])
    W, H, fps = probe(src)
    g, tw, th, dur = build_graph(v, W, H)
    base = os.path.join(OUT_VID, v['id'])
    mid = base + '.master.mkv'
    # máster intermedio sin pérdida para codificar varias veces
    ff('-i', src, '-filter_complex', g, '-map', '[out]', '-an', '-c:v', 'libx264', '-qp', '0', '-preset', 'ultrafast', *COLOR, mid)
    budget = v['budget_kb'] * 1024
    mp4 = base + '.mp4'
    crf_used = None
    for crf in range(v.get('crf_start', 22), 36):
        ff('-i', mid, '-an', '-c:v', 'libx264', '-preset', 'veryslow', '-crf', str(crf), '-profile:v', 'high', '-level', '4.0',
           '-pix_fmt', 'yuv420p', '-tune', 'film', '-x264-params', 'keyint=60:min-keyint=30', *COLOR, '-movflags', '+faststart', mp4)
        crf_used = crf
        if os.path.getsize(mp4) <= budget:
            break
    # AV1 (WebM) a calidad comparable; se queda solo si es más liviano
    webm = base + '.webm'
    av1_crf = crf_used + 14
    ff('-i', mid, '-an', '-c:v', 'libsvtav1', '-preset', '5', '-crf', str(av1_crf), '-g', '60', '-pix_fmt', 'yuv420p', *COLOR, webm)
    keep_webm = os.path.getsize(webm) < os.path.getsize(mp4) * 0.9
    if not keep_webm:
        os.remove(webm)
    # póster desde el máster (mismo encuadre)
    t = v.get('poster_t', 0.5)
    png = base + '.poster.png'
    ff('-ss', str(t), '-i', mid, '-frames:v', '1', png)
    p = load_srgb(png)
    posters = {}
    for f, q in (('avif', {'avif': 55}), ('webp', {'webp': 78})):
        pp = f'{base}-poster.{f}'
        save(p, pp, f, q)
        posters[f] = {'path': rel(pp), 'bytes': os.path.getsize(pp)}
    lq, dom = lqip(p)
    os.remove(png)
    os.remove(mid)
    out = {'ref': v['ref'], 'src': v['src'], 'section': v['section'], 'source_size': [W, H], 'width': tw, 'height': th,
           'ratio': v['ratio'], 'focal': v['focal'], 'start': v['start'], 'end': v['end'], 'loop': v['loop'],
           'duration': round(dur, 2), 'fps': round(fps, 2), 'muted': True, 'crf_h264': crf_used,
           'files': {'mp4': {'path': rel(mp4), 'bytes': os.path.getsize(mp4), 'codec': 'avc1.640028'}},
           'poster': posters, 'lqip': lq, 'color': dom, 'budget_kb': v['budget_kb'],
           'alt_placeholder': alt_for(v), 'post': post_for(v)}
    if keep_webm:
        out['files']['webm'] = {'path': rel(webm), 'bytes': os.path.getsize(webm), 'codec': 'av01', 'crf': av1_crf}
    for k in ('credit', 'credit_src', 'note'):
        if v.get(k):
            out[k] = v[k]
    print(f"  video {v['id']}: {tw}x{th} {dur:.1f}s crf{crf_used} mp4 {os.path.getsize(mp4) // 1024} KB"
          + (f" webm {out['files']['webm']['bytes'] // 1024} KB" if keep_webm else ' (AV1 no compensa)'))
    return out


def main():
    M = json.load(open(MAN, encoding='utf-8'))
    os.makedirs(OUT_IMG, exist_ok=True)
    os.makedirs(OUT_VID, exist_ok=True)
    media = json.load(open(OUT_JSON, encoding='utf-8')) if os.path.exists(OUT_JSON) else {}
    media.setdefault('images', {})
    media.setdefault('videos', {})
    credits = M.get('credits', {})
    done = {'images': set(), 'videos': set()}
    if '--no-img' not in ARGS:
        for a in M['images']:
            if ONLY and a['id'] not in ONLY:
                continue
            if 'alias' in a:
                done['images'].add(a['id'])
                media['images'][a['id']] = {'alias': a['alias'], 'ref': a['ref'], 'section': a['section'], 'note': a.get('note', '')}
                continue
            print('img', a['id'])
            media['images'][a['id']] = do_image(a, M, credits)
            done['images'].add(a['id'])
    if '--no-video' not in ARGS:
        for v in M['videos']:
            if ONLY and v['id'] not in ONLY:
                continue
            print('video', v['id'])
            media['videos'][v['id']] = do_video(v)
            done['videos'].add(v['id'])
    # fusión al escribir: otra corrida (p. ej. --no-img) puede haber escrito mientras tanto
    disk = json.load(open(OUT_JSON, encoding='utf-8')) if os.path.exists(OUT_JSON) else {}
    for k in ('images', 'videos'):
        merged = disk.get(k, {})
        merged.update({i: e for i, e in media[k].items() if i in done[k]})
        for i, e in media[k].items():
            merged.setdefault(i, e)
        media[k] = merged
    ids = {a['id'] for a in M['images']}, {v['id'] for v in M['videos']}
    media['images'] = {i: e for i, e in media['images'].items() if i in ids[0]}
    media['videos'] = {i: e for i, e in media['videos'].items() if i in ids[1]}
    media['_doc'] = ('Generado por tools/media_v2.py desde tools/media_v2.json. images[id].crops[name].files[fmt][width] '
                     '= {path, bytes}; width/height = intrínsecos del mayor ancho emitido. alias -> otro id.')
    media['rejected'] = M.get('rejected', [])
    json.dump(media, open(OUT_JSON, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('ok', len(media['images']), 'imágenes,', len(media['videos']), 'videos ->', rel(OUT_JSON))


if __name__ == '__main__' and '--qa' not in sys.argv:
    main()


# ---------- QA: hoja de contacto + tabla de pesos ----------
def qa():
    from PIL import ImageDraw, ImageFont
    media = json.load(open(OUT_JSON, encoding='utf-8'))
    qdir = os.path.join(ROOT, '_plan/media-v2')
    os.makedirs(qdir, exist_ok=True)
    try:
        font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
    except OSError:
        font = ImageFont.load_default()
    cells = []
    for i, e in media['images'].items():
        if 'alias' in e:
            continue
        for cn, c in e['crops'].items():
            if 'jpg' in c['files']:
                f = next(iter(c['files']['jpg'].values()))
                cells.append((f"{i} [{cn}]", f['path'], f"{c['width']}x{c['height']} jpg", f['bytes'], e['ref']))
            else:
                w = str(c['width'])
                f = c['files']['avif'][w]
                cells.append((f"{i} [{cn} {c['ratio']}]", f['path'], f"{c['width']}x{c['height']}", f['bytes'], e['ref']))
    for i, v in media['videos'].items():
        mp4 = v['files']['mp4']
        cells.append((f"{i} [video {v['loop']}]", v['poster']['avif']['path'],
                      f"{v['width']}x{v['height']} {v['duration']}s", mp4['bytes'], v['ref']))
    CH, PAD, LAB = 300, 8, 34
    rows, row, x = [], [], 0
    MAXW = 2400
    prepared = []
    for lab, p, dim, b, ref in cells:
        im = Image.open(os.path.join(ROOT, p)).convert('RGB')
        im.thumbnail((10 ** 5, CH))
        im.thumbnail((CH * 2, CH))
        prepared.append((lab, im, dim, b, ref))
    for it in prepared:
        w = max(it[1].width, 210)
        if x + w + PAD > MAXW and row:
            rows.append(row); row, x = [], 0
        row.append(it); x += w + PAD
    rows.append(row)
    sheet = Image.new('RGB', (MAXW, len(rows) * (CH + LAB + PAD) + PAD), '#170e0b')
    d = ImageDraw.Draw(sheet)
    y = PAD
    for r in rows:
        x = PAD
        for lab, im, dim, b, ref in r:
            sheet.paste(im, (x, y))
            d.text((x, y + CH + 3), lab, fill='#f6ecdc', font=font)
            d.text((x, y + CH + 18), f"{ref} · {dim} · {b / 1024:.0f} KB", fill='#cbb9a5', font=font)
            x += max(im.width, 210) + PAD
        y += CH + LAB + PAD
    sheet.save(os.path.join(qdir, 'qa.jpg'), quality=82, optimize=True)
    print('qa.jpg', sheet.size)
    pesos(media, qdir)


def pick(c, target, fmt='avif'):
    ws = c['widths']
    w = next((w for w in ws if w >= target), ws[-1])
    return w, c['files'][fmt][str(w)]['bytes']


def pesos(media, qdir):
    K = lambda b: f"{b / 1024:,.0f}".replace(',', '.')
    L = ['# Fase 10 · Pesos de medios v2', '',
         'Generado por `python3 tools/media_v2.py --qa` desde `assets/v2/media.json`. KB = 1024 bytes.',
         '"Teléfono" = AVIF del menor ancho ≥ 1170 px (390 css × DPR 3) o el mayor disponible si la fuente no llega; '
         '"escritorio" = AVIF del mayor ancho emitido. WebP es el respaldo (no se suma: el navegador baja uno).', '',
         '## Imágenes', '', '| id | ref | recorte | anchos | teléfono AVIF | escritorio AVIF | mayor WebP | en disco (todas) |',
         '|---|---|---|---|---|---|---|---|']
    tot = {'phone': 0, 'desk': 0, 'disk': 0, 'n': 0}
    for i, e in media['images'].items():
        if 'alias' in e:
            L.append(f"| {i} | {e['ref']} | → `{e['alias']}` | — | 0 | 0 | 0 | 0 |")
            continue
        for cn, c in e['crops'].items():
            disk = sum(f['bytes'] for fm in c['files'].values() for f in fm.values())
            tot['disk'] += disk
            tot['n'] += sum(len(fm) for fm in c['files'].values())
            if 'jpg' in c['files']:
                L.append(f"| {i} | {e['ref']} | {cn} {c['ratio']} | {c['width']} jpg | — | — | — | {K(disk)} |")
                continue
            pw, pb = pick(c, 1170)
            dw = c['widths'][-1]
            db = c['files']['avif'][str(dw)]['bytes']
            wb = c['files']['webp'][str(dw)]['bytes']
            tot['phone'] += pb; tot['desk'] += db
            L.append(f"| {i} | {e['ref']} | {cn} {c['ratio']} | {'/'.join(map(str, c['widths']))} | {pw}: {K(pb)} | {dw}: {K(db)} | {K(wb)} | {K(disk)} |")
    L += ['', f"**Total imágenes:** {tot['n']} archivos, {K(tot['disk'])} KB en disco. "
          f"Si un teléfono bajara todos los recortes: {K(tot['phone'])} KB AVIF; escritorio al mayor ancho: {K(tot['desk'])} KB AVIF "
          '(cota superior: cada página usa un recorte por foto y lazy-load).', '',
          '## Video', '', '| id | ref | salida | loop | CRF H.264 | MP4 | AV1 WebM | póster AVIF | presupuesto |', '|---|---|---|---|---|---|---|---|---|']
    vt = vb = vp = 0
    for i, v in media['videos'].items():
        mp4 = v['files']['mp4']['bytes']; web = v['files'].get('webm', {}).get('bytes')
        po = v['poster']['avif']['bytes']
        vt += mp4; vb += min(mp4, web or mp4); vp += po
        ok = 'pasa' if mp4 <= v['budget_kb'] * 1024 else 'NO PASA'
        L.append(f"| {i} | {v['ref']} | {v['width']}x{v['height']} {v['duration']} s | {v['loop']} | {v['crf_h264']} | {K(mp4)} | "
                 f"{K(web) if web else '—'} | {K(po)} | ≤{v['budget_kb']} ({ok}) |")
    L += ['', f"**Total video (MP4, peor caso):** {K(vt)} KB de ≤ 7.168 KB (7 MB): {'pasa' if vt <= 7 * 1024 * 1024 else 'NO PASA'}. "
          f"Con AV1 donde existe: {K(vb)} KB. Pósters: {K(vp)} KB.", '']
    por = media['images']['portada-terraza']['crops']['a']
    pw, pb = pick(por, 1170)
    dw = por['widths'][-1]; db = por['files']['avif'][str(dw)]['bytes']
    L += ['## Primer viewport', '',
          'La portada v2 es la foto P189 (no hay video arriba del pliegue: el loop V021 bajó a la carta). '
          'Se cuentan solo los medios; fuentes, CSS y JS van aparte.', '',
          '| Pantalla | Qué carga | Peso | Presupuesto |', '|---|---|---|---|',
          f"| Teléfono 390×844, DPR 3 | P189 AVIF {pw} (+ LQIP inline) | {K(pb)} KB | ≤ 1.434 KB (1,4 MB): {'pasa' if pb <= 1.4 * 1024 * 1024 else 'NO PASA'} |",
          f"| Escritorio 1440×900, DPR 1–2 | P189 AVIF {dw} (tope nativo; en DPR 2 se ve a media resolución, decisión abierta del contrato) | {K(db)} KB | ≤ 2.355 KB (2,3 MB): {'pasa' if db <= 2.3 * 1024 * 1024 else 'NO PASA'} |",
          f"| Respaldo WebP (teléfono / escritorio) | P189 WebP | {K(por['files']['webp'][str(pw)]['bytes'])} / {K(por['files']['webp'][str(dw)]['bytes'])} KB | — |",
          '', 'La banda "Hoy en Almud" queda justo bajo el pliegue: su foto o póster se pide con `loading="lazy"` y prioridad normal.', '']
    open(os.path.join(qdir, 'pesos.md'), 'w', encoding='utf-8').write('\n'.join(L))
    print('pesos.md')


if '--qa' in sys.argv and __name__ == '__main__':
    qa()
