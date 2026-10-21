#!/usr/bin/env python3
"""Verifica el guion v2 (content/copy-v2.md) contra las fuentes literales de Almud.

Cada texto marcado «…» [FUENTE] debe aparecer literal en su fuente, tras normalizar:
  - NFC; glifos emoji, selectores de variante y ZWJ fuera;
  - saltos de línea (y " / " del titular) como un espacio; espacios colapsados;
  - sin espacio antes de , . ! ? : ; )
Un literal con "…" que no aparece entero se verifica trozo a trozo, en orden.
CARTA-n se compara sin distinguir mayúsculas (los PDF imprimen en caja alta) y,
para títulos de grupo, contra el nombre del PDF sin tildes.

Además: aritmética de titulares {display}/{head} (Six Caps k=0,22), aviso de
bloques > 25 palabras y búsqueda de palabras prohibidas (filas y esperas de mesa).

Uso:  python3 tools/verify_copy.py [--write]   (--write vuelca la tabla en copy-v2.md)
Sale con código 1 si algún literal o titular falla.
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COPY = ROOT / "content" / "copy-v2.md"

# ---------- normalización con mapa de índices ----------
DROP = {0xFE0E, 0xFE0F, 0x200D, 0x20E3}


def is_emoji(c):
    o = ord(c)
    if o in DROP:
        return True
    if 0x1F3FB <= o <= 0x1F3FF or 0x1F000 <= o <= 0x1FAFF or 0x2600 <= o <= 0x27BF:
        return True
    if 0x1F1E6 <= o <= 0x1F1FF:  # banderas
        return True
    return unicodedata.category(c) == "So" and c not in "°"


def norm_map(text):
    """Devuelve (normalizado, índices en el original, emoji_quitados_por_posición)."""
    text = unicodedata.normalize("NFC", text)
    out, idx = [], []
    for i, c in enumerate(text):
        if is_emoji(c):
            continue
        if c.isspace():
            c = " "
        if c == " " and (not out or out[-1] == " "):
            continue
        if c in ",.!?:;)" and out and out[-1] == " ":
            out.pop(); idx.pop()
        out.append(c); idx.append(i)
    while out and out[-1] == " ":
        out.pop(); idx.pop()
    return "".join(out), idx, text


def norm(text):
    return norm_map(text)[0]


def fold(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").lower()


# ---------- fuentes ----------
def load_sources():
    src = {}
    for p in json.loads((ROOT / "content/ig_posts.json").read_text()):
        src[p["id"]] = p["caption"]
    src["BIO"] = (ROOT / "content/bio.txt").read_text()
    src["DATO"] = (ROOT / "content/research_web.md").read_text() + "\n" + src["BIO"]
    # VID-061: transcripción de subtítulos quemados (bloque §2 de content/copy.md, v1)
    v1 = (ROOT / "content/copy.md").read_text()
    m = re.search(r"\[VID-061\]:(.*?)- Crédito", v1, re.S)
    src["VID-061"] = re.sub(r'^\s*\d+\.\s*"|"\s*$', "", m.group(1), flags=re.M) if m else ""
    # CARTA-n: sección del PDF en carta_raw + strings de carta.json + nombre del PDF
    raw = (ROOT / "content/carta_raw.txt").read_text()
    parts = re.split(r"=== (carta_(\d)_[^\n]+)", raw)  # el PDF trae \f antes de "==="
    carta_json = json.loads((ROOT / "content/carta.json").read_text())
    # cada PDF solo contra su propia parte de carta.json
    json_keys = {"1": ["comilona"], "2": ["coctel"], "5": ["mocktail"],
                 "7": ["promos", "promo_precio", "promo_hora", "promo_nota"]}
    strings = []

    def walk(x):
        if isinstance(x, str):
            strings.append(x)
        elif isinstance(x, dict):
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
    for k in range(1, len(parts), 3):
        fname, n, body = parts[k], parts[k + 1], parts[k + 2]
        title = re.sub(r"^carta_\d_|\.pdf$", "", fname).replace("_", " ")
        strings.clear()
        for key in json_keys.get(n, []):
            walk(carta_json[key])
        src[f"CARTA-{n}"] = body + "\n" + "\n".join(strings)
        src[f"CARTA-{n}#file"] = title
    reviews = json.loads((ROOT / "content/reviews.json").read_text())
    for r in reviews:
        src.setdefault(f"RESEÑA:{r['who']}", "")
        src[f"RESEÑA:{r['who']}"] += r["q"] + "\n"
    return src


def find_in(lit, source, ci=False):
    """Busca el literal normalizado en la fuente; devuelve (ok, modo, emoji_quitado)."""
    ns, idx, orig = norm_map(source)
    nl = norm(lit.replace(" / ", " "))
    hay, needle = (ns.lower(), nl.lower()) if ci else (ns, nl)
    pos = hay.find(needle)
    if pos >= 0:
        span = orig[idx[pos]: idx[pos + len(needle) - 1] + 1]
        return True, "exacto" + (" (sin mayúsc.)" if ci else ""), any(is_emoji(c) for c in span)
    if "…" in nl:
        frags = [f.strip(" ") for f in nl.split("…") if f.strip(" ")]
        start, emo = 0, False
        for f in frags:
            f2 = f.lower() if ci else f
            p = hay.find(f2, start)
            if p < 0:
                return False, "recorte: falta «%s»" % f, False
            span = orig[idx[p]: idx[p + len(f2) - 1] + 1]
            emo = emo or any(is_emoji(c) for c in span)
            start = p + len(f2)
        return True, "recorte en orden (%d trozos)" % len(frags), emo
    return False, "no encontrado", False


# ---------- aritmética de titulares ----------
K = 0.22
SIZES = {"display": {390: (358, 96), 1440: (790, 210)}, "head": {390: (358, 56), 1440: (790, 98)}}
BUDGET = {"display": 30, "head": 32}


def capacity(kind, w, strict=False):
    """Caracteres por línea: nominal = redondeo (sistema.md: ≈17); estricta = piso."""
    col, size = SIZES[kind][w]
    x = col / (K * size)
    return int(x) if strict else int(round(x))


def check_headline(lit, kind):
    lines = [l.strip() for l in lit.split(" / ")]
    total = len(" ".join(lines))
    res, ok = [], True
    for w in (390, 1440):
        cap = capacity(kind, w)
        if len(lines) == 1 and len(lines[0]) > cap:
            # sin corte: el navegador parte; estimar líneas
            nlines = -(-len(lines[0]) // cap)
        else:
            nlines = len(lines)
        over = [len(l) for l in lines if len(l) > cap]
        if over or nlines > 2:
            ok = False
        res.append(f"{w}: {'+'.join(str(len(l)) for l in lines)}/{cap}")
    just = any(len(l) > min(capacity(kind, w, strict=True) for w in (390, 1440)) for l in lines)
    note = "justo" if just else ""
    if total > BUDGET[kind]:
        note = (note + " " if note else "") + f"total {total} > {BUDGET[kind]}"
    return ok, " · ".join(res), note, total


# ---------- prohibidas ----------
FORBIDDEN = re.compile(r"\bfilas?\b|hacer fila|esperar (una |la )?mesa|desocup|lista de espera|\bqueue|wait(ing)? for a table|line up|\bwaitlist", re.I)

LIT_RE = re.compile(r"«([^»]+)»\s*\[([^\]]+)\](?:\s*\{(display|head)[^}]*\})?")
ANY_RE = re.compile(r"[«‹“]([^»›”]+)[»›”]\s*\[([^\]]+)\]")


def main():
    text = COPY.read_text()
    text_scan = re.sub(r"`[^`\n]*`", "", text)  # lo que va entre comillas de código es ejemplo
    body = text_scan.split("<!-- VERIFICACION:INICIO -->")[0]
    # no verificar la sección "Correcciones mínimas" (cita ejemplos sin fuente)
    scan = body.split("## Correcciones mínimas")[0]
    src = load_sources()
    rows, fails, heads, warns = [], 0, [], []
    seen = set()
    for m in LIT_RE.finditer(scan):
        lit, tag, kind = m.group(1), m.group(2).strip(), m.group(3)
        key = (lit, tag)
        if key in seen:
            continue
        seen.add(key)
        if tag not in src and not tag.startswith("CARTA-"):
            rows.append((lit, tag, "FALLA", "fuente desconocida", ""))
            fails += 1
            continue
        ci = tag.startswith("CARTA-")
        ok, mode, emo = find_in(lit, src.get(tag, ""), ci=ci)
        if not ok and ci:
            fname = src.get(tag + "#file", "")
            if fold(norm(lit)) in fold(fname) or fold(fname) == fold(norm(lit)):
                ok, mode = True, "nombre del PDF (sin tildes ni mayúsc.)"
        if not ok and tag == "DATO":
            nums = re.findall(r"\d[\d.,]*", lit)
            if nums and all(n in src["DATO"] for n in nums):
                ok, mode = True, "cifras presentes"
        rows.append((lit, tag, "pasa" if ok else "FALLA", mode, "sí" if emo else ""))
        if not ok:
            fails += 1
        if kind:
            hok, hres, hnote, _ = check_headline(lit, kind)
            heads.append((lit, tag, kind, hres, "pasa" if hok else "FALLA", hnote))
            if not hok:
                fails += 1
        else:
            nw = len(norm(lit).split())
            if nw > 25:
                warns.append(f"{tag}: {nw} palabras «{lit[:50]}…»")
    # prohibidas en todo texto visible (literales, UI, EN, ES)
    for m in ANY_RE.finditer(scan):
        if FORBIDDEN.search(m.group(1)):
            warns.append(f"PROHIBIDA: «{m.group(1)}» [{m.group(2)}]")
            fails += 1

    out = []
    out.append(f"Resultado: **{len(rows) - sum(r[2] == 'FALLA' for r in rows)}/{len(rows)} literales pasan**; "
               f"**{sum(h[4] == 'pasa' for h in heads)}/{len(heads)} titulares caben en 2 líneas**; "
               f"palabras prohibidas: {sum('PROHIBIDA' in w for w in warns)}. Generado por `tools/verify_copy.py`.")
    out.append("")
    out.append("### Literales")
    out.append("")
    out.append("| # | Texto literal | Fuente | Verificación | Modo | Emoji quitado |")
    out.append("|---|---|---|---|---|---|")
    for i, (lit, tag, st, mode, emo) in enumerate(rows, 1):
        out.append(f"| {i} | {lit.replace('|', '¦')} | {tag} | {st} | {mode} | {emo} |")
    out.append("")
    out.append("### Titulares (Six Caps, k = 0,22; car. por línea / capacidad)")
    out.append("")
    out.append("| Titular | Fuente | Paso | 390 · 1440 | Cabe | Nota |")
    out.append("|---|---|---|---|---|---|")
    for lit, tag, kind, hres, st, note in heads:
        out.append(f"| {lit} | {tag} | {kind} | {hres} | {st} | {note} |")
    if warns:
        out.append("")
        out.append("### Avisos")
        out.append("")
        for w in warns:
            out.append(f"- {w}")
    table = "\n".join(out)
    print(table)
    if "--write" in sys.argv:
        new = re.sub(r"<!-- VERIFICACION:INICIO -->.*<!-- VERIFICACION:FIN -->",
                     "<!-- VERIFICACION:INICIO -->\n" + table.replace("\\", "\\\\") + "\n<!-- VERIFICACION:FIN -->",
                     text, flags=re.S)
        COPY.write_text(new)
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
