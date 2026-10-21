#!/usr/bin/env python3
"""Validate content/carta-v2.json.

Checks
  - structure: secciones[].grupos[].items[] with required keys
  - every item has a non-empty "nombre" and a "precio" or non-empty "precios"
  - no empty strings anywhere in the document
  - every price parses as a CLP integer ("$ 8.800" -> 8800)
  - multi-price items use exactly the labels declared in the group's "columnas"
  - (optional, if pdftotext is installed) every price of a section appears in its
    source PDF the same number of times it appears in the JSON
Prints counts per section/group. Exit code 1 on any error.

Usage: python3 tools/validate_carta.py [path/to/carta-v2.json]
"""
import json, re, sys, shutil, subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PATH = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'content' / 'carta-v2.json'
PDFS = {
    'CARTA-1': 'carta_1_Comilona.pdf',
    'CARTA-2': 'carta_2_Cocteleria_De_La_Casa.pdf',
    'CARTA-3': 'carta_3_Cocteles_Del_Mundo_Mundial.pdf',
    'CARTA-4': 'carta_4_Espirituosos.pdf',
    'CARTA-5': 'carta_5_Mocktails_Sin_alcohol.pdf',
    'CARTA-6': 'carta_6_Vinos_Espumantes.pdf',
    'CARTA-7': 'carta_7_Nuestras_Promos.pdf',
}
PRICE_RE = re.compile(r'^\$ ?(\d{1,3}(?:\.\d{3})*)$')

errors = []
def err(msg): errors.append(msg)

def clp(s):
    m = PRICE_RE.match(s) if isinstance(s, str) else None
    return int(m.group(1).replace('.', '')) if m else None

def walk_empty(node, path='$'):
    if isinstance(node, str):
        if not node.strip():
            err(f'empty string at {path}')
    elif isinstance(node, dict):
        for k, v in node.items():
            walk_empty(v, f'{path}.{k}')
    elif isinstance(node, list):
        if not node:
            err(f'empty list at {path}')
        for i, v in enumerate(node):
            walk_empty(v, f'{path}[{i}]')

def main():
    data = json.loads(PATH.read_text(encoding='utf-8'))
    walk_empty(data)
    secs = data.get('secciones') or []
    if not secs:
        err('no secciones')
    ids = Counter(s.get('id') for s in secs)
    for k, n in ids.items():
        if n > 1: err(f'duplicate section id {k}')

    total = 0
    prices_by_src = {}
    print(f'{PATH.relative_to(ROOT) if PATH.is_relative_to(ROOT) else PATH}\n')
    for s in secs:
        for key in ('id', 'titulo', 'fuente', 'grupos'):
            if key not in s: err(f'section {s.get("id")} missing {key}')
        n_sec = sum(len(g.get('items', [])) for g in s.get('grupos', []))
        total += n_sec
        print(f'{s.get("fuente")}  {s.get("titulo")}  [{s.get("id")}]  -> {n_sec} items')
        for g in s.get('grupos', []):
            cols = g.get('columnas')
            items = g.get('items') or []
            label = g.get('titulo') or '(sin título)'
            if g.get('padre'): label = f'{g["padre"]} › {label}'
            print(f'    {len(items):3d}  {label}' + (f'   columnas={cols}' if cols else ''))
            for i, it in enumerate(items):
                where = f'{s.get("id")} / {label} / #{i+1} {it.get("nombre")!r}'
                if not isinstance(it.get('nombre'), str) or not it['nombre'].strip():
                    err(f'{where}: missing nombre')
                has_p, has_ps = 'precio' in it, 'precios' in it
                if has_p == has_ps:
                    err(f'{where}: needs exactly one of precio / precios')
                plist = []
                if has_p:
                    plist.append(it['precio'])
                if has_ps:
                    if not isinstance(it['precios'], dict) or not it['precios']:
                        err(f'{where}: precios must be a non-empty object')
                    else:
                        plist += list(it['precios'].values())
                        if cols and list(it['precios'].keys()) != cols:
                            err(f'{where}: precios labels {list(it["precios"])} != columnas {cols}')
                        if not cols:
                            err(f'{where}: precios used but group has no columnas')
                for p in plist:
                    v = clp(p)
                    if v is None:
                        err(f'{where}: price {p!r} does not parse as CLP')
                    elif v <= 0 or v % 100:
                        err(f'{where}: suspicious price {p!r} -> {v}')
                    else:
                        prices_by_src.setdefault(s.get('fuente'), Counter())[v] += 1
                if 'tags' in it and not (isinstance(it['tags'], list) and all(isinstance(t, str) for t in it['tags'])):
                    err(f'{where}: tags must be a list of strings')
    print(f'\nTOTAL: {len(secs)} secciones, {sum(len(s.get("grupos", [])) for s in secs)} grupos, {total} items')

    # optional cross-check with the source PDFs
    pdfdir = ROOT / 'assets' / 'raw' / 'carta'
    if shutil.which('pdftotext') and pdfdir.is_dir():
        print('\nPDF price cross-check:')
        for src, counter in sorted(prices_by_src.items()):
            f = pdfdir / PDFS.get(src, '')
            if not f.is_file():
                print(f'  {src}: pdf not found, skipped'); continue
            txt = subprocess.run(['pdftotext', '-layout', str(f), '-'], capture_output=True, text=True).stdout
            txt = re.sub(r'\$\s*1 0\.000', '$ 10.000', txt)  # documented OCR break (Tullamore XL)
            found = Counter(int(m.replace('.', '')) for m in re.findall(r'\$\s*(\d{1,3}(?:\.\d{3})+)', txt))
            # inline prices inside notes (e.g. "POR $3.700") are not items
            if src == 'CARTA-3': found[3700] -= 1
            if found == counter:
                print(f'  {src}: OK ({sum(counter.values())} prices)')
            else:
                diff = {k: (counter[k], found[k]) for k in set(counter) | set(found) if counter[k] != found[k]}
                err(f'{src}: price multiset differs from PDF (json, pdf): {diff}')
                print(f'  {src}: MISMATCH {diff}')

    if errors:
        print(f'\n{len(errors)} ERROR(S):')
        for e in errors: print('  -', e)
        sys.exit(1)
    print('\nOK: all checks passed')

if __name__ == '__main__':
    main()
