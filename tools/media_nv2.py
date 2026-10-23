#!/usr/bin/env python3
"""Fotos nuevas de /nueva_v2/ (v4 fase 3): recortes AVIF/WebP desde el material propio de Almud.

Lee tools/media_nv2.json y escribe assets/nv2/img/<id>-<crop>-<w>.{avif,webp} y assets/nv2/media-img.json
(mismo formato que assets/v3/media.json 'images'). Reutiliza las funciones de tools/media_v3.py (nunca amplía,
sRGB, unsharp suave solo al reducir, LQIP y color dominante). No toca assets/v3 ni assets/v4.
Uso: python3 tools/media_nv2.py [--force]
"""
import importlib.util, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location('media_v3', os.path.join(ROOT, 'tools/media_v3.py'))
mv3 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mv3)

MAN = os.path.join(ROOT, 'tools/media_nv2.json')
OUT_IMG = os.path.join(ROOT, 'assets/nv2/img')
OUT_JSON = os.path.join(ROOT, 'assets/nv2/media-img.json')
mv3.MAN, mv3.OUT_IMG = MAN, OUT_IMG  # do_image escribe en OUT_IMG y compara fechas con MAN
mv3.FORCE = '--force' in sys.argv


def main():
    M = json.load(open(MAN, encoding='utf-8'))
    os.makedirs(OUT_IMG, exist_ok=True)
    out = {'_doc': 'Generado por tools/media_nv2.py desde tools/media_nv2.json. Mismo formato que assets/v3/media.json images.', 'images': {}}
    for a in M['images']:
        e = mv3.do_image(a, M, M.get('credits', {}))
        out['images'][a['id']] = e
        c = e['crops']['a']
        print(f"{a['id']}: {c['crop_size'][0]}x{c['crop_size'][1]} -> {c['widths']}")
    json.dump(out, open(OUT_JSON, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('ok', mv3.rel(OUT_JSON), len(out['images']))


if __name__ == '__main__':
    main()
