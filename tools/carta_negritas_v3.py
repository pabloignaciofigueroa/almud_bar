#!/usr/bin/env python3
"""Negritas de la carta impresa (ronda 2b). Los PDF no marcan la negrita en la fuente (todo es Oswald-Regular
con trazo), así que se mide la tinta de cada palabra en una página renderizada: las palabras en negrita tienen
≥ 0,285 de píxeles oscuros y las normales ≤ 0,26. Las palabras en negrita consecutivas (en orden de columna)
forman una frase. Salida: content/carta-negritas-v3.json = {"CARTA-n": [frases]}.
Uso: python3 tools/carta_negritas_v3.py"""
import json, pathlib, re
import pdfplumber, pypdfium2 as P, numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
S, TH = 4, 0.285
out = {}
for pdf_path in sorted((ROOT / 'assets/raw/carta').glob('carta_*.pdf')):
    n = re.match(r'carta_(\d+)_', pdf_path.name).group(1)
    doc = P.PdfDocument(str(pdf_path))
    phrases = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        for i, pg in enumerate(pdf.pages):
            im = np.asarray(doc[i].render(scale=S).to_pil().convert('L'))
            ws = [w for w in pg.extract_words(extra_attrs=['size']) if 12.5 <= w['size'] <= 15.5]
            mid = pg.width / 2
            for col in (0, 1):
                cw = sorted([w for w in ws if (w['x0'] >= mid) == bool(col)], key=lambda w: (round(w['top']), w['x0']))
                run = []
                for w in cw + [None]:
                    bold = False
                    if w:
                        a = im[int(w['top'] * S):int(w['bottom'] * S), int(w['x0'] * S):int(w['x1'] * S)]
                        bold = a.size and (a < 128).mean() >= TH
                    if bold and re.search(r'[\d$]', w['text']):
                        bold = False  # los precios en negrita cortan la frase
                    if bold:
                        run.append(w['text'])
                    elif run:
                        ph = re.sub(r'^[\W_]+|[\s,.:;!?)\]]+$', '', ' '.join(run))
                        if len(ph) >= 3:
                            phrases.append(ph)
                        run = []
    out[f'CARTA-{n}'] = sorted(set(phrases), key=len, reverse=True)
    print(pdf_path.name, len(out[f'CARTA-{n}']))
(ROOT / 'content/carta-negritas-v3.json').write_text(json.dumps(out, ensure_ascii=False, indent=1))
