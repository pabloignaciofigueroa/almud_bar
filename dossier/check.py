#!/usr/bin/env python3
"""Control del dossier: frases de 4 palabras repetidas entre láminas, tecnicismos y citas literales contra sus fuentes."""
import html, json, pathlib, re, collections
ROOT = pathlib.Path(__file__).resolve().parent.parent
t = (ROOT / 'dossier/almud-dossier-diseno.html').read_text()
t = re.sub(r'<style>.*?</style>', '', t, flags=re.S); t = re.sub(r'src="data:[^"]+"', '', t)
lams = [html.unescape(re.sub(r'<[^>]+>', ' ', x.split('>', 1)[1])) for x in t.split('<article')[1:]]
def grams(s):
    w = re.findall(r'\w+', s.lower()); return {' '.join(w[i:i + 4]) for i in range(len(w) - 3)}
cnt = collections.Counter(g for l in lams for g in grams(l))
print('4-gramas repetidos', [g for g, c in cnt.items() if c > 1])
todo = ' '.join(lams)
bad = re.findall(r'.{30}(?:\brem\b| px|\bMB\b|scroll|auditor|\.md|k-means|ghost|interfaz|píxel|algoritmo|\bCSS\b|\bHTML\b|\bSVG\b|vector|sticky|\bCLS\b|WCAG|favicon|escritorio|decidimos|lo que hicimos).{20}', todo)
print('tecnicismos', bad)
P = {p['id']: p['caption'] for p in json.loads((ROOT / 'content/ig_posts.json').read_text())}
R = ' '.join(r['q'] for r in json.loads((ROOT / 'content/reviews.json').read_text()))
CARTA = (ROOT / 'content/carta-v2.json').read_text()
n = lambda s: re.sub(r'\s+', ' ', re.sub(r'[^\w\s!?¿¡&:.,]', '', s.lower())).replace('!!', '!').strip()
src = (ROOT / 'dossier/build_dossier.py').read_text()
for m in re.finditer(r"Q\(['\"](.+?)['\"],\s*([^)]*\)?)", src):
    q, ids = m.group(1), re.findall(r'IG-\d+', m.group(2))
    base = n(P[ids[0]].replace('❤️', 'corazón')) if ids else n(R + CARTA)
    print('OK' if n(q) in base else 'XX', ids, q[:60])
