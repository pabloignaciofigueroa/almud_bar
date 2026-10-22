"""Verifica el texto VISIBLE real (dom.json / dom-carta.json) contra copy-v3.md + carta-v2.json,
y aplica la lista PROHIB de tools/verify_copy_v3.py. No toca el sitio."""
import json, re, sys, unicodedata
from pathlib import Path
ROOT = Path("/home/claude/almud_bar"); OUT = ROOT / "_plan/v3/ronda1/voz"
sys.argv = ["x"]
src = (ROOT / "tools/verify_copy_v3.py").read_text()
ns = {}
exec(src.split("# ---------- documento ----------")[0], ns)  # norm, NSRC
norm, NSRC = ns["norm"], ns["NSRC"]
PROHIB = eval(re.search(r"PROHIB = (\[[\s\S]*?\n\])", src).group(1))
ALLOW = {"somos inquietos y nos gusta el colorssss!"}

doc = (ROOT / "content/copy-v3.md").read_text().split("<!-- CONTEO -->")[0]
approved = set()
for pat in (r"«([^»]+)»", r"‹([^›]+)›", r"“([^”]+)”"):
    for t in re.findall(pat, doc):
        approved.add(norm(t))
        for part in re.split(r"\s·\s", t): approved.add(norm(part))
        approved.add(norm(re.sub(r"\s*\[[^\]]*\]", "", t)))   # 'Ojo Piojo [mural of eyes]' -> partes
        for b in re.findall(r"\[[^\]]+\]", t): approved.add(norm(b))
# Decisiones posteriores de Carmen (08-juicio-carmen*.md) y carta
EXTRA_OK = {"sillones": "08-juicio-carmen §7", "lounge": "EN de Sillones (sin fuente en copy-v3)",
            "los dueños": "08-juicio-carmen-2 (línea aceptada; texto distinto al [DATO] pedido)",
            "the owners": "EN de Los dueños", "@cepaz": "08-juicio-carmen", "@rusio_mezclao": "08-juicio-carmen",
            "·": "separador", "nuevo": "tag carta (_iconos_a_tags)", "new": "tag carta EN",
            "saltar al contenido": "skip-link a11y", "skip to content": "skip-link a11y"}
carta = json.load(open(ROOT / "content/carta-v2.json"))
cstr = set(); cnames = set(); cdesc = set()
def walk(o, key=None):
    if isinstance(o, str):
        cstr.add(norm(o))
        if key == "nombre": cnames.add(norm(o))
        if key in ("desc", "nota", "intro"): cdesc.add(o)
    elif isinstance(o, dict):
        for k, v in o.items():
            if not k.startswith("_"): walk(v, k)
    elif isinstance(o, list):
        for v in o: walk(v, key)
walk(carta["secciones"])
revs = {norm(r["q"]) for r in json.load(open(ROOT / "content/reviews.json"))}

def runs(items):
    """une las palabras animadas (span.w__i) consecutivas en un solo titular"""
    res, buf = [], []
    for o in items:
        if o["sel"] == "span.w__i": buf.append(o["t"]); continue
        if buf: res.append({"sel": "TITULAR", "t": " ".join(buf), "lang": o["lang"]}); buf = []
        res.append(o)
    if buf: res.append({"sel": "TITULAR", "t": " ".join(buf), "lang": "?"})
    return res

def check(name, items, is_carta):
    unk, bad = [], []
    for o in runs(items):
        t = o["t"]; n = norm(t)
        ok = (n in approved or n in EXTRA_OK or n in cstr or any(n in r for r in revs)
              or (is_carta and any(n and n in c for c in cstr)))
        if not ok: unk.append((o["sel"], t))
        if o.get("lang") == "es" or o["sel"] == "TITULAR":
            if is_carta and (n in cnames): continue
            if n in ALLOW: continue
            for rx, nm in PROHIB:
                if re.search(rx, n): bad.append((nm, o["sel"], t[:120]))
    return unk, bad

dom = json.load(open(OUT / "dom.json")); domc = json.load(open(OUT / "dom-carta.json"))
report = []
for k, v in list(dom.items()) + list(domc.items()):
    if k.startswith("carta-") and k.count("-") == 2: continue  # vista inicial ya cubierta por pestañas
    unk, bad = check(k, v["out"], k.startswith("carta"))
    report.append((k, unk, bad))
seen = set()
for k, unk, bad in report:
    u = [x for x in unk if x not in seen]; b = [x for x in bad if x not in seen]
    seen.update(unk); seen.update(bad)
    if u or b:
        print("==", k)
        for x in u: print("  NO APROBADO", x)
        for x in b: print("  PROHIBIDO", x)
# conteo palabras visibles ES landing (regla copy-v3: fuera reseñas y carta destacada)
items = runs(dom["home-m-es"]["out"])
skip = {"p", "p.r__f", "span.it__n", "span.it__p", "span.menu__n", "a.skip", "span.gloss.gloss--on"}
wc = lambda t: sum(1 for tok in t.split() if re.search(r"[0-9A-Za-zÀ-ÿ&]", tok))
print("\nPalabras visibles ES landing (390):", sum(wc(o["t"]) for o in items if o["sel"] not in skip))
print("Literales (verify_copy_v3 en ROOT): ver salida aparte")
