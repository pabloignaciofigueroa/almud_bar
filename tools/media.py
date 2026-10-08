#!/usr/bin/env python3
"""Genera assets/img (WebP 800/1800 + LQIP) y assets/video desde assets/raw.
Uso: python3 tools/media.py [--videos]"""
import json, os, sys, base64, io, subprocess
from PIL import Image, ImageOps
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, 'assets/raw/ig')
P = {p['id']: p for p in json.load(open(os.path.join(ROOT, 'content/ig_posts.json')))}

def f(pid, k=0, ext='jpg'):
    return os.path.join(RAW, f"{P[pid]['code']}_{k:02d}.{ext}")

# nombre -> (archivo fuente, recorte opcional (x0,y0,x1,y1) en fracciones)
IMAGES = {
 # rincones
 'barra-botellas': (f('IG-108'), None), 'barra-equipo': (f('IG-091'), None),
 'lamparas': (f('IG-103'), None), 'salon': (f('IG-173'), None),
 'terraza-techada': (f('IG-004', 1), None), 'terraza-techada-noche': (f('IG-004', 3), None),
 'fogon': (f('IG-004', 4), None), 'terraza-luces': (f('IG-109'), None), 'terraza-mesas': (f('IG-160'), None),
 'vista': (f('IG-163'), None), 'cintas': (f('IG-174'), None), 'cintas-salon': (f('IG-175'), None),
 'ojo-piojo': (f('IG-118'), None), 'flecos': (f('IG-090'), None), 'flecos-2': (f('IG-111'), None),
 # carta
 'c-peter': (f('IG-044'), None), 'c-olvidar': (f('IG-002'), None), 'c-saguer': (f('IG-063'), None),
 'c-sangria': (f('IG-039'), None), 'c-coquette': (f('IG-096'), None), 'c-moto': (f('IG-011'), None),
 'c-tukulito': (f('IG-139'), None), 'c-contuti': (f('IG-066'), None), 'c-gredita': (f('IG-077'), None),
 'c-topiturron': (f('IG-040'), None), 'c-negroni': (f('IG-042'), None), 'c-piscolein': (f('IG-019'), None),
 # comilona (masas)
 'm-pizza': (f('IG-154'), None), 'm-pizza-2': (f('IG-141'), None), 'm-tabla': (f('IG-066'), None),
 'm-gredita': (f('IG-150'), None), 'm-tacos': (f('IG-105'), None), 'm-bowl': (f('IG-022', 1), None),
 'm-trago-sol': (f('IG-064', 2), None), 'm-brindis': (f('IG-069'), None), 'm-trago-flor': (f('IG-046'), None),
 # eventos
 'e-12': (f('IG-009', 0), None), 'e-12b': (f('IG-008', 9), None), 'e-12c': (f('IG-010'), None),
 'e-jaloguin': (f('IG-038', 4), None), 'e-jaloguin-2': (f('IG-070', 8), None),
 'e-fondita': (f('IG-079', 4), None), 'e-negroni': (f('IG-005', 0), None), 'e-tiki': (f('IG-053', 0), None),
 'e-rucalaf': (f('IG-025', 14), None), 'e-desfile': (f('IG-057'), None), 'e-amor': (f('IG-116'), None),
 'e-primavera': (f('IG-075', 4), None), 'e-islenos': (f('IG-029'), None), 'e-10': (f('IG-100'), None),
 'e-fiesta': (f('IG-008', 4), None), 'e-fiesta-2': (f('IG-009', 15), None),
 # equipo
 't-milagros': (f('IG-083'), None), 't-liz': (f('IG-088'), None), 't-pablete': (f('IG-034'), None),
 't-javier': (f('IG-012'), None), 't-eduardo': (f('IG-085'), None), 't-grupo': (f('IG-091'), None),
 't-chicas': (f('IG-014'), None), 't-bartender-1': (f('IG-001', 1), None), 't-bartender-2': (f('IG-001', 2), None),
 'team-pasto': (f('IG-179', 1), None),
 # hero / otros
 'puerta': (f('IG-177'), None), 'posavaso': (f('IG-086'), None),
}
VIDEOS = {
 # nombre: (fuente, inicio, duración, ancho, audio?)
 'hero': (f('IG-061', 0, 'mp4'), 1.0, 7.2, 1280, False),
 'hero-movil': (f('IG-090', 0, 'mp4'), 0, 10, 720, False),
 'historia': (f('IG-061', 0, 'mp4'), 0, None, 1278, True, 'crop=1278:520:0:8'),
 'cintas': (f('IG-111', 0, 'mp4'), 0, None, 720, False),
}

def lqip(im):
    t = im.copy(); t.thumbnail((24, 24)); b = io.BytesIO(); t.save(b, 'WEBP', quality=40)
    return 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()

def main():
    out = os.path.join(ROOT, 'assets/img'); os.makedirs(out, exist_ok=True)
    meta = {}
    if os.path.exists(os.path.join(out, 'meta.json')):
        meta = json.load(open(os.path.join(out, 'meta.json')))
    for name, (src, crop) in IMAGES.items():
        if not os.path.exists(src):
            src = src.replace('.jpg', '.jpg')
        im = ImageOps.exif_transpose(Image.open(src)).convert('RGB')
        if crop:
            W, H = im.size; im = im.crop((int(crop[0]*W), int(crop[1]*H), int(crop[2]*W), int(crop[3]*H)))
        W, H = im.size
        for w in (800, 1800):
            p = os.path.join(out, f'{name}-{w}.webp')
            if not os.path.exists(p) or os.path.getmtime(p) < os.path.getmtime(src):
                t = im.copy(); t.thumbnail((w, w * 3)); t.save(p, 'WEBP', quality=78 if w == 1800 else 74, method=5)
        r = min(1, 1800 / W)
        meta[name] = {'w': round(W * r), 'h': round(H * r), 'lqip': lqip(im), 'src': os.path.basename(src)}
    json.dump(meta, open(os.path.join(out, 'meta.json'), 'w'), indent=0)
    print('img', len(meta))
    if '--videos' in sys.argv:
        vout = os.path.join(ROOT, 'assets/video'); os.makedirs(vout, exist_ok=True)
        only = [a for a in sys.argv[2:] if not a.startswith('--')]
        for name, (src, ss, dur, w, audio, *extra) in VIDEOS.items():
            if only and name not in only: continue
            base = os.path.join(vout, name)
            cut = ['-ss', str(ss)] + (['-t', str(dur)] if dur else [])
            vf = (extra[0] + ',' if extra else '') + f"scale='min({w},iw)':-2"
            a = ['-c:a', 'aac', '-b:a', '96k'] if audio else ['-an']
            subprocess.run(['ffmpeg', '-v', 'error', '-y', *cut, '-i', src, '-vf', vf, '-c:v', 'libx264', '-preset', 'slow', '-crf', '27', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', *a, base + '.mp4'], check=True)
            a2 = ['-c:a', 'libopus', '-b:a', '80k'] if audio else ['-an']
            subprocess.run(['ffmpeg', '-v', 'error', '-y', *cut, '-i', src, '-vf', vf, '-c:v', 'libvpx-vp9', '-b:v', '0', '-crf', '38', '-row-mt', '1', '-deadline', 'good', '-cpu-used', '4', *a2, base + '.webm'], check=True)
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(ss + 0.5), '-i', src, '-frames:v', '1', '-vf', vf, '-q:v', '4', base + '-poster.jpg'], check=True)
            print('video', name, os.path.getsize(base + '.mp4') // 1024, 'KB')

if __name__ == '__main__':
    main()
