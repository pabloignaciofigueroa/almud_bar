#!/usr/bin/env python3
"""Verifica content/copy-v3.md (adaptado de tools/verify_voice_v3.py).
- cada «…» [FUENTE] existe literal en su fuente (normalización igual a verify_voice_v3)
- fuentes nuevas: TAG-001 (usertags IG-001), DATO (research_web.md), RESEÑA:autor (reviews.json)
- prohibidos de brand-voice-v3 §4 en el texto ES visible de la landing (salvo nombres de carta)
- conteo de palabras visibles (columna Cuenta = sí)
"""
import json, re, sys, unicodedata
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "/home/claude/almud_bar")
DOC = ROOT / "content/copy-v3.md"
THIRD = {"IG-007", "IG-028", "IG-029", "IG-056"}

def is_emoji(c):
    o = ord(c); cat = unicodedata.category(c)
    return (cat in ("So", "Cs") or o in (0xFE0F, 0xFE0E, 0x200D, 0x20E3)
            or 0x1F3FB <= o <= 0x1F3FF or 0x1F000 <= o <= 0x1FAFF or 0xE0020 <= o <= 0xE007F)

def norm(t):
    t = unicodedata.normalize("NFC", t)
    t = "".join(c for c in t if not is_emoji(c)).lower()
    t = re.sub(r"\s+", " ", t)
    t = re.sub(r" ([.,!?;:)…])", r"\1", t)
    return t.strip()

# ---------- fuentes ----------
src = {}
for p in json.load(open(ROOT / "content/ig_posts.json")):
    src[p["id"]] = p["caption"]
src["BIO"] = (ROOT / "content/bio.txt").read_text()
carta = json.load(open(ROOT / "content/carta-v2.json"))
def strings(o):
    if isinstance(o, str): yield o
    elif isinstance(o, dict):
        for v in o.values(): yield from strings(v)
    elif isinstance(o, list):
        for v in o: yield from strings(v)
for sec in carta["secciones"]:
    src.setdefault(sec["fuente"], "")
    src[sec["fuente"]] += "\n" + "\n".join(strings(sec))
src["DATO"] = (ROOT / "content/research_web.md").read_text()
tags = []
for p in json.load(open(ROOT / "assets/raw/ig/posts_new.json")):
    if p.get("code") == "DeNQ8A2lDgg":
        for cm in p.get("carousel_media") or []:
            for t in ((cm.get("usertags") or {}).get("in") or []):
                tags.append("@" + t["user"]["username"])
src["TAG-001"] = "\n".join(tags)
for r in json.load(open(ROOT / "content/reviews.json")):
    src["RESEÑA:" + r["who"]] = src.get("RESEÑA:" + r["who"], "") + "\n" + r["q"]
NSRC = {k: norm(v) for k, v in src.items()}

# ---------- documento ----------
doc = DOC.read_text().split("<!-- CONTEO -->")[0]
lit_pat = re.compile(r"«([^»]+)»")
ui_pat = re.compile(r"‹([^›]+)›")
src_pat = re.compile(r"\[((?:IG|CARTA|TAG)-\d+|BIO|DATO|VID-061|UI|RESEÑA:[^\]]+)\]")

PROHIB = [
    (r"\b(ito|ita|ucho|ona)s? (ito|ita|ucho|ona)s?\b", "cascada"), (r"eichon", "-eichon"),
    (r"(?!s)([a-záéíóúñ])\1\1", "letra triple"), (r"[!?]{2,}", "signos en serie"),
    (r"almudcito", "Almudcito"), (r"\bfilas?\b", "fila"), (r"\bespera(r|s|n)?\b", "espera"),
    (r"\breserv", "reserva"), (r"tempran", "temprano"), (r"\bdj\b", "DJ"), (r"en vivo", "en vivo"),
    (r"experiencia", "experiencia"), (r"\w@", "forma con @"), (r"\bbesi", "Besi"), (r"\bmuac", "Muac"),
    (r"se llena", "se llena"), (r"pucho", "pucho"), (r"mejor los tomamos", "veto IG-046"),
    (r"bigoteli", "veto IG-139"), (r"pr[oó]ximamente|se vienen|todos los (viernes|s[aá]bados)", "promesa"),
]
ALLOW = {"somos inquietos y nos gusta el colorssss!"}

section = None; ok = fail = 0; out = []; warns = []; counts = {}; seen = set()
def wc(t):
    return sum(1 for tok in t.split() if re.search(r"[0-9A-Za-zÀ-ÿ&]", tok))

for line in doc.splitlines():
    m = re.match(r"## (Nav|\d+\.|C\.)\s*(.*)", line)
    if m:
        section = m.group(1).rstrip("."); counts.setdefault(section, 0)
    if not line.startswith("| ") or line.startswith("|---") or section is None:
        # literales sueltos fuera de tablas (listas de grupos, notas)
        pass
    cells = [c.strip() for c in line.strip().strip("|").split("|")] if line.startswith("| ") else None
    # --- literales: en toda línea, emparejar «…» con la fuente que la sigue
    for mm in re.finditer(r"«([^»]+)»(?:\s*·\s*«[^»]+»)*\s*(?:\|\s*)?\[((?:IG|CARTA|TAG)-\d+|BIO|DATO|VID-061|RESEÑA:[^\]]+)\]", line):
        s = mm.group(2)
        for lit in lit_pat.findall(mm.group(0)):
            n = norm(lit)
            if s not in NSRC: res = "FUENTE DESCONOCIDA"; fail += 1
            elif n in NSRC[s]: res = "OK"; ok += 1
            else: res = "NO ENCONTRADA"; fail += 1
            if s in THIRD: res += " · TERCERO"; fail += 1
            key = (lit, s)
            if key not in seen or res != "OK":
                out.append(f"{res:<13} §{section} [{s}] «{lit}»")
            seen.add(key)
    # --- tablas de la landing: prohibidos + conteo
    if cells and len(cells) >= 5 and section not in ("C",) and cells[0] not in ("Elemento",):
        es, fuente, cuenta = cells[1], cells[2], cells[4]
        texts = lit_pat.findall(es) + ui_pat.findall(es)
        is_carta = cuenta.startswith("no·carta")
        if not is_carta and not cuenta.startswith("no·reseña"):
            for t in texts:
                nt = norm(t)
                if nt in ALLOW: continue
                for rx, name in PROHIB:
                    if re.search(rx, nt):
                        warns.append(f"PROHIBIDO({name}) §{section} «{t}»"); fail += 1
        if cuenta == "sí":
            counts[section] += sum(wc(t) for t in texts)

print(f"Literales: {ok + fail} revisados ({len(seen)} únicos) · OK {ok} · fallas {fail}")
print("\n".join(out))
print("\nProhibidos (landing, texto ES visible):", "\n".join(warns) if warns else "ninguno")
names = {"Nav": "Nav", "1": "1 Portada", "2": "2 El lugar", "3": "3 Tragos", "4": "4 Comida", "5": "5 Con quién",
         "6": "6 Eventos", "7": "7 Equipo", "8": "8 Reseñas (solo titular)", "9": "9 Cuándo y dónde", "10": "10 Pie"}
print("\n| Sección | Palabras |\n|---|---|")
tot = 0
for k, v in names.items():
    print(f"| {v} | {counts.get(k, 0)} |"); tot += counts.get(k, 0)
print(f"| **Total landing (ES)** | **{tot}** |")
print("META ≤150:", "CUMPLE" if tot <= 150 else "NO CUMPLE")
sys.exit(1 if fail or tot > 150 else 0)
