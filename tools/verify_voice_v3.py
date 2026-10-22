#!/usr/bin/env python3
"""Verifica brand-voice-v3.md: cada «…» [FUENTE] existe literal en su fuente
(ignorando emoji, mayúsculas y saltos de línea) + reglas de voz premium."""
import json, re, sys, unicodedata
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "/home/claude/almud_bar")
DOC = ROOT / "content/brand-voice-v3.md"
THIRD = {"IG-007", "IG-028", "IG-029", "IG-056"}

def is_emoji(c):
    o = ord(c)
    cat = unicodedata.category(c)
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
vid = []
for line in (ROOT / "content/copy.md").read_text().splitlines()[18:32]:
    m = re.match(r'\s+\d+\.\s+"(.*)"\s*$', line)
    if m: vid.append(m.group(1))
src["VID-061"] = "\n".join(vid)
NSRC = {k: norm(v) for k, v in src.items()}

# ---------- documento ----------
doc = DOC.read_text().split("<!-- RESULTADO -->")[0]
section = None; sub = None
pat = re.compile(r"«([^»]+)»\s*(?:\|\s*)?\[([A-Z]+(?:-\d+)?)\]")
rows, stars = [], {}
for line in doc.splitlines():
    m = re.match(r"## (\d+)\.", line)
    if m: section = int(m.group(1)); sub = None
    m = re.match(r"### (.+)", line)
    if m: sub = m.group(1).strip()
    if section == 5 and sub and sub != "Resumen de favoritos":
        stars.setdefault(sub, 0)
        if line.startswith("| ★ |"): stars[sub] += 1
    for lit, s in pat.findall(line):
        kind = "titular" if (section == 5 and line.startswith("| ") and sub != "Resumen de favoritos"
                             and re.match(r"\| (★ )?\| «", line)) else ""
        if s == "FUENTE": continue
        if section == 2 and not line.startswith("| "): kind = "nota"
        rows.append((section, sub, lit, s, kind))

PROHIB = [
    (r"\b(ito|ita|ucho|ona)s? (ito|ita|ucho|ona)s?\b", "cascada de diminutivo"),
    (r"eichon", "-eichon"),
    (r"(?!s)([a-záéíóúñ])\1\1", "letra triple"),
    (r"[!?]{2,}", "signos en serie"),
    (r"almudcito", "Almudcito"),
    (r"\bfilas?\b", "fila"), (r"\bespera(r|s|n)?\b", "espera"), (r"\breserv", "reserva"),
    (r"tempran", "temprano"), (r"\bdj\b", "DJ"), (r"en vivo", "en vivo"),
    (r"experiencia", "experiencia"), (r"\w@", "forma con @"), (r"\bbesi", "Besi"),
    (r"\bmuac", "Muac"), (r"se llena", "se llena"), (r"pucho", "pucho"),
]
ALLOW = {"somos inquietos y nos gusta el colorssss!"}

ok = fail = 0; out = []; warns = []
seen = set()
for section, sub, lit, s, kind in rows:
    key = (lit, s)
    n = norm(lit)
    if s == "PIEZA":
        res = "SIN FUENTE EN REPO (confirmar a ojo en el afiche)"
    elif s not in NSRC:
        res = "FUENTE DESCONOCIDA"; fail += 1
    elif n in NSRC[s]:
        res = "OK"; ok += 1
    else:
        res = "NO ENCONTRADA"; fail += 1
    if s in THIRD:
        res += " · TERCERO"; fail += 1
    if key not in seen or res != "OK":
        out.append(f"{res:<14} §{section} [{s}] «{lit}»")
    seen.add(key)
    if section in (2, 5) and kind != "nota":
        nl = norm(lit)
        if nl not in ALLOW:
            for rx, name in PROHIB:
                if re.search(rx, nl):
                    warns.append(f"PROHIBIDO({name}) §{section} {sub or ''} «{lit}»")
        w = len(lit.split())
        if section == 2 and w > 8:
            warns.append(f"LARGO {w} palabras (>8) §2 «{lit}»")
        if kind == "titular" and w > 6:
            warns.append(f"LARGO {w} palabras (>6) titular {sub} «{lit}»")

print(f"Literales revisados: {len(rows)} ({len(seen)} únicos) · OK {ok} · fallas {fail}")
print("\n".join(sorted(set(out))))
print("\nReglas (secciones 2 y 5):")
print("\n".join(warns) if warns else "sin avisos")
print("\nFavoritos por sección:", ", ".join(f"{k}={v}" for k, v in stars.items()))
bad = [k for k, v in stars.items() if v != 1]
print("Secciones sin un único ★:", bad or "ninguna")
sys.exit(1 if fail else 0)
