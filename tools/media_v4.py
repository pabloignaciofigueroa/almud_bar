#!/usr/bin/env python3
"""Medios v4 · fase 2 (solo video): loops MP4 (H.264) + WebM (VP9) de 8–10 s, siempre hacia adelante, con fundido
final→inicio (loop "crossfade"), desde los reels propios de Almud. Copia de tools/media_v3.py (que no se toca).

Lee tools/media_v4.json (sección "videos") y escribe:
  assets/v4/video/<id>-<w>.{mp4,webm} y <id>-poster.{avif,webp,jpg}   (póster = primer frame del loop)
  assets/v4/media-video.json                                           (mismo formato que videos de assets/v3/media.json)
Presupuestos por formato: budget_kb (WebM) y budget_mp4_kb (MP4; por defecto = budget_kb).

Reglas: nunca se amplía (solo anchos <= ancho real del recorte); sRGB; unsharp suave solo tras reducir; videos sin audio,
faststart, 720p máx. salvo fuente 1080p que lo valga; cada loop se codifica al mayor ancho que cumple su presupuesto con
CRF <= crf_max. No toca assets/img, assets/v2 ni el sitio.

Uso: python3 tools/media_v3.py [--force] [--only id1,id2] [--no-video] [--no-img] [--qa]
"""
import base64, csv, io, json, os, re, subprocess, sys
from PIL import Image, ImageCms, ImageFilter, ImageOps, ImageStat, ImageChops

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAN = os.path.join(ROOT, 'tools/media_v4.json')
OUT_VID = os.path.join(ROOT, 'assets/v4/video')
OUT_JSON = os.path.join(ROOT, 'assets/v4/media-video.json')
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
    if v.get('parts'):
        return make_master_parts(v, rate)
    if v.get('crop'):  # v4: recorte manual [x, y, ancho, alto] en px de la fuente (p. ej. llevar la comida al centro); nunca se amplía
        x0, y0, cw0, ch0 = v['crop']
        x1, y1 = x0 + cw0, y0 + ch0
    else:
        x0, y0, x1, y1 = crop_box(W, H, v['ratio'], v['focal'])
    cw, ch = (x1 - x0) // 2 * 2, (y1 - y0) // 2 * 2
    cropf = f'crop={cw}:{ch}:{x0}:{y0},' if (cw, ch) != (W, H) else ''
    segs = v['segments']
    parts, labels = [], []
    for i, (s, e) in enumerate(segs):
        sp = v.get('speed')  # cámara lenta opcional (p. ej. 0.8)
        tempo = f'setpts=(PTS-STARTPTS)/{sp},fps={rate}' if sp else f'setpts=PTS-STARTPTS,fps={rate}'  # cámara lenta por repetición de cuadros: sin mezcla, sin desenfoque
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


def make_master_parts(v, rate):
    """v4 fase 10: montaje de tramos de reels distintos, cada uno con su recorte [x, y, w, h] y escalado a v['out'] = [W, H],
    unidos con un fundido de v['join_xfade'] s y cerrados con el fundido de loop de siempre (v['xfade'])."""
    OW, OH = v['out']
    num, den = (float(x) for x in rate.split('/'))
    fps = num / den
    base = os.path.join(OUT_VID, v['id'])
    ins, chains, durs = [], [], []
    for k, prt in enumerate(v['parts']):
        s0, e0 = prt['seg']
        ins += ['-i', os.path.join(ROOT, prt['src'])]
        cr = prt.get('crop')
        cropf = f'crop={cr[2]}:{cr[3]}:{cr[0]}:{cr[1]},' if cr else ''
        chains.append(f'[{k}:v]trim={s0}:{e0},setpts=PTS-STARTPTS,fps={rate},{cropf}scale={OW}:{OH}:flags=lanczos,setsar=1,format=yuv420p[p{k}]')
        durs.append(round((e0 - s0) * fps) / fps)
    jd = round(v['join_xfade'] * fps) / fps
    last, acc = '[p0]', durs[0]
    for k in range(1, len(durs)):
        out = f'[j{k}]'
        chains.append(f'{last}[p{k}]xfade=transition=fade:duration={jd:.4f}:offset={acc - jd:.4f}{out}')
        last, acc = out, acc + durs[k] - jd
    lin = base + '.lin.mkv'
    ff(*ins, '-filter_complex', ';'.join(chains), '-map', last, '-an', '-c:v', 'ffv1', lin)
    n = nframes(lin)
    dn = round(v['xfade'] * fps)
    dur = n / fps
    g = (f'[0:v]split[a][b];[a]trim=start_frame={dn},setpts=PTS-STARTPTS[t];'
         f'[b]trim=end_frame={dn},setpts=PTS-STARTPTS[h];'
         f'[t][h]xfade=transition=fade:duration={dn / fps:.4f}:offset={dur - 2 * dn / fps:.4f}[out]')
    mid = base + '.master.mkv'
    ff('-i', lin, '-filter_complex', g, '-map', '[out]', '-an', '-c:v', 'ffv1', mid)
    os.remove(lin)
    return mid, OW, OH, fps


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
    budget_mp4 = v.get('budget_mp4_kb', v['budget_kb']) * 1024
    base = os.path.join(OUT_VID, v['id'])
    for f in os.listdir(OUT_VID):  # anchos de una corrida anterior
        if re.fullmatch(re.escape(v['id']) + r'-\d+\.(mp4|webm)', f):  # solo los anchos de ESTE id (no 'eventos-fiesta-12-…' al codificar 'eventos-fiesta')
            os.remove(os.path.join(OUT_VID, f))
    chosen = None
    for w in v['widths']:
        tw = min(w, cw) // 2 * 2
        th = round(ch * tw / cw) // 2 * 2
        mp4, webm = f'{base}-{tw}.mp4', f'{base}-{tw}.webm'
        c264, ok1 = search(enc_mp4, mid, mp4, tw, th, cw, v.get('crf_start', 21), v['crf_max'], budget_mp4)
        cvp9, ok2 = search(enc_webm, mid, webm, tw, th, cw, v.get('vp9_crf_start', 30), v.get('vp9_crf_max', v['crf_max'] + 12), budget)
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
    pq = v.get('poster_q', {})
    for f, q in (('avif', {'avif': pq.get('avif', 50)}), ('webp', {'webp': pq.get('webp', 74)}), ('jpg', {'jpg': pq.get('jpg', 80)})):
        pp = f'{base}-poster.{f}'
        save(p, pp, f, q)
        posters[f] = {'path': rel(pp), 'bytes': os.path.getsize(pp)}
    lq, dom = lqip(p)
    os.remove(png)
    os.remove(mid)
    e = common(v, credits)
    e.update({'source_size': [W, H], 'width': tw, 'height': th, 'ratio': v['ratio'] if v['ratio'] != 'orig' else f'{W}:{H}',
              'segments': v['segments'], 'loop': v['loop'], 'frames': n, 'fps': round(fps, 3), 'duration': round(n / fps, 2),
              'muted': True, 'attrs': 'autoplay muted loop playsinline', 'budget_kb': v['budget_kb'], 'budget_mp4_kb': v.get('budget_mp4_kb', v['budget_kb']), 'within_budget': ok,
              'xfade': v.get('xfade'), 'tramo_s': round(sum(e - s for s, e in v['segments']), 2),
              'seam': {'last_vs_first': seam, 'typical_step': ref},
              'files': {'webm': {'path': rel(webm), 'bytes': os.path.getsize(webm), 'type': 'video/webm; codecs="vp9"', 'crf': cvp9},
                        'mp4': {'path': rel(mp4), 'bytes': os.path.getsize(mp4), 'type': 'video/mp4; codecs="avc1.640028"', 'crf': c264}},
              'poster': posters, 'lqip': lq, 'color': dom})
    print(f"  -> {v['id']} {tw}x{th} {e['duration']} s, costura {seam} (paso típico {ref})")
    return e


def main():
    M = json.load(open(MAN, encoding='utf-8'))
    os.makedirs(OUT_VID, exist_ok=True)
    old = json.load(open(OUT_JSON, encoding='utf-8')) if os.path.exists(OUT_JSON) else {}
    videos = old.get('videos', {})
    credits = M.get('credits', {})
    for v in M['videos']:
        if ONLY and v['id'] not in ONLY:
            continue
        assert v['loop'] == 'crossfade', f"{v['id']}: en v4 solo se permite loop crossfade (nunca boomerang)"
        assert not v.get('speed'), f"{v['id']}: v4 va a velocidad real"
        print('video', v['id'])
        videos[v['id']] = do_video(v, credits)
    order_v = [v['id'] for v in M['videos']]
    out = {'_doc': ('Generado por tools/media_v4.py desde tools/media_v4.json (fase 2 v4). videos[id].files: webm (VP9) primero, '
                    'mp4 (H.264, faststart) de respaldo; poster = primer frame del loop (avif/webp/jpg). Cada loop dura 8–10 s, '
                    'avanza siempre (sin boomerang ni reverse) y cierra con un fundido final→inicio de xfade s.'),
           'videos': {i: videos[i] for i in order_v if i in videos}}
    json.dump(out, open(OUT_JSON, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('ok', len(out['videos']), 'videos ->', rel(OUT_JSON))


if __name__ == '__main__':
    main()
