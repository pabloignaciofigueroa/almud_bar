#!/usr/bin/env python3
"""Almud Bar v2 · build: src-v2/index.html -> index.html (raíz) y src-v2/carta.html -> carta/index.html.

Inyecta:
  <x-img id crop sizes class [eager]/>   <picture> AVIF/WebP con srcset+sizes, width/height, LQIP, loading/fetchpriority
  <x-video id class sizes/>               <video> muted playsinline loop preload=none + póster + botón de pausa
  <x-preload id crop sizes/>              <link rel=preload as=image imagesrcset> de la portada
  <x-credit id [ui] [inline] [class]/>    "Foto @autor" con la fuente (post) de assets/v2/media.json
  <x-symbols/>                            símbolos SVG del logotipo (brand/)
  <x-handles>…</x-handles>                los @ como enlaces a Instagram (texto intacto)
  <x-hoy/> <x-resenas/>                   Hoy en Almud y reseñas, desde content/*.json
  <x-destacados/>                         landing: destacados de la carta (ítem con su foto real, nombre, descripción y precio)
  <x-carta-tabs/> <x-carta-estado/>       /carta/: pestañas por sección, grupos filtrables y el estado inicial (antes de pintar)
  {{precio:Nombre}}                       precio literal de content/carta-v2.json
  data-lines                              titular partido en líneas con máscara (<br> = corte)

Falla (código 1, sin escribir index.html) si:
  - falta un id de media, un recorte o un archivo;
  - falta el alt en español o en inglés (content/alts-v2.json);
  - hay un emoji visible;
  - un texto marcado data-src no es literal del guion (content/copy-v2.md) con esa fuente;
  - una glosa [EN]/[ES] o una etiqueta [UI] no está en el guion (salvo la lista UI_EXTRA, declarada);
  - queda texto visible sin marcar (sin fuente).

Uso: python3 tools/build_v2.py
"""
import html
import json
import re
import sys
import unicodedata
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import verify_copy as vc  # noqa: E402  (normalización y fuentes del guion)

SRC = ROOT / "src-v2" / "index.html"
OUT = ROOT / "index.html"
SRC_CARTA = ROOT / "src-v2" / "carta.html"
OUT_CARTA = ROOT / "carta" / "index.html"
SRC_404 = ROOT / "src-v2" / "404.html"   # pulido 3: Cloudflare Pages la sirve en cualquier ruta que no exista (rutas absolutas)
OUT_404 = ROOT / "404.html"
MEDIA = json.loads((ROOT / "assets/v2/media.json").read_text())
ALTS = json.loads((ROOT / "content/alts-v2.json").read_text())
CARTA = json.loads((ROOT / "content/carta-v2.json").read_text())
REVIEWS = json.loads((ROOT / "content/reviews.json").read_text())
HOY = json.loads((ROOT / "content/hoy-v2.json").read_text())
COPY_TEXT = (ROOT / "content/copy-v2.md").read_text()

MAPS = "https://www.google.com/maps/search/?api=1&amp;query=Almud%20Bar%2C%20Serrano%20325%2C%20Castro"  # fase 16: abre la ficha de Google, no un pin pelado
DM = "https://ig.me/m/almud_bar"

# Etiquetas de interfaz nuestras que el guion no lista (accesibilidad y controles). Se declaran en el informe.
UI_EXTRA = {
    "Saltar al contenido", "Skip to content", "Almud Bar", "Pausar video", "Pause video",
    "Reproducir video", "Play video",
    "Secciones de la carta", "Menu sections",
    # pulido 3 (fase 17): la página 404
    "Esta página no existe", "This page doesn't exist",
}

errors = []


def fail(msg):
    errors.append(msg)


# ------------------------------------------------------------------ guion: conjuntos válidos
def copy_sets():
    body = COPY_TEXT.split("<!-- VERIFICACION:INICIO -->")[0].split("## Correcciones mínimas")[0]
    body = re.sub(r"`[^`\n]*`", "", body)
    lits, en, es, ui = {}, set(), set(), set()
    for m in vc.LIT_RE.finditer(body):
        lits.setdefault(m.group(2).strip(), set()).add(key(m.group(1)))
    for m in re.finditer(r"“([^”]+)”\s*\[(EN|ES)\]", body):
        (en if m.group(2) == "EN" else es).add(key(m.group(1)))
    for m in re.finditer(r"‹([^›]+)›\s*\[UI\]", body):
        ui.add(key(m.group(1)))
    return lits, en, es, ui


def key(s):
    s = html.unescape(s).replace(" / ", " ")
    return vc.norm(s).strip()


LITS, EN_SET, ES_SET, UI_SET = copy_sets()
UI_OK = UI_SET | {key(x) for x in UI_EXTRA}
EN_OK = EN_SET | {key(x) for x in UI_EXTRA}


# ------------------------------------------------------------------ media
def media_entry(mid):
    if mid in MEDIA["images"]:
        e = MEDIA["images"][mid]
        if "alias" in e:
            return media_entry(e["alias"])[0], e["alias"]
        return e, mid
    fail(f"media: falta el id «{mid}»")
    return None, mid


def alt_for(mid, *alts_ids):
    for k in (mid, *alts_ids):
        a = ALTS.get(k)
        if a:
            if not a.get("es") or not a.get("en"):
                fail(f"alt: falta es/en para «{k}»")
            return a.get("es", ""), a.get("en", "")
    fail(f"alt: no hay alt para «{mid}»")
    return "", ""


def check_file(path):
    if not (ROOT / path).is_file():
        fail(f"media: falta el archivo {path}")


def srcset_of(c, fmt):
    parts = []
    for w in sorted(c["files"].get(fmt, {}), key=int):
        p = c["files"][fmt][w]["path"]
        check_file(p)
        parts.append(f"{p} {w}w")
    return ", ".join(parts)


def picture(mid, crop=None, sizes="100vw", cls="", eager=False, mcrop=None, msizes=None, media=None):
    e, real = media_entry(mid)
    if not e:
        return ""
    crops = e.get("crops", {})
    if crop is None:
        crop = "a" if "a" in crops else next(iter(crops))
    c = crops.get(crop)
    if not c or "files" not in c:
        fail(f"media: «{mid}» no tiene el recorte «{crop}»")
        return ""
    files = c["files"]
    srcsets = {}
    for fmt in ("avif", "webp"):
        parts = []
        for w in sorted(files.get(fmt, {}), key=int):
            p = files[fmt][w]["path"]
            check_file(p)
            parts.append(f"{p} {w}w")
        srcsets[fmt] = ", ".join(parts)
    if not srcsets["webp"]:
        fail(f"media: «{mid}» sin WebP")
    ws = sorted(files["webp"], key=int)
    fallback = next((w for w in ws if int(w) >= 960), ws[-1])
    alt_es, alt_en = alt_for(mid, real)
    fx, fy = c.get("focal", [50, 50])
    style = f"--pos:{fx}% {fy}%;--dom:{c.get('color', '#2a1a14')};--lqip:url({c['lqip']})" if c.get("lqip") else f"--pos:{fx}% {fy}%"
    load = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    msrc = ""
    if mcrop:  # fase 16: recorte propio para el teléfono (art direction), con su alto y ancho
        mc = crops.get(mcrop)
        if not mc:
            fail(f"media: «{mid}» no tiene el recorte «{mcrop}»")
            return ""
        msrc = "".join(f'<source media="{media}" type="image/{f}" srcset="{srcset_of(mc, f)}" sizes="{msizes}" width="{mc["width"]}" height="{mc["height"]}">'
                       for f in ("avif", "webp"))
    return (f'<picture class="ph {cls}">{msrc}'
            f'<source type="image/avif" srcset="{srcsets["avif"]}" sizes="{sizes}">'
            f'<source type="image/webp" srcset="{srcsets["webp"]}" sizes="{sizes}">'
            f'<img src="{files["webp"][fallback]["path"]}" width="{c["width"]}" height="{c["height"]}" '
            f'alt="{html.escape(alt_es)}" data-alt-en="{html.escape(alt_en)}" {load} decoding="async" style="{style}">'
            f'</picture>')


def preload(mid, crop, sizes, media=None, mcrop=None, msizes=None):
    e, _ = media_entry(mid)
    if not e:
        return ""
    def one(c, sz, med):
        files = e["crops"][c]["files"]["avif"]
        ss = ", ".join(f'{files[w]["path"]} {w}w' for w in sorted(files, key=int))
        m = f' media="{med}"' if med else ""
        return f'<link rel="preload" as="image" type="image/avif" imagesrcset="{ss}" imagesizes="{sz}"{m} fetchpriority="high">'
    if not mcrop:
        return one(crop, sizes, None)
    # fase 16: dos preloads excluyentes, igual que los <source media> de la portada
    return one(mcrop, msizes, media) + "\n" + one(crop, sizes, media.replace("max-width: 899px", "min-width: 900px"))


def video(mid, cls="", sizes=""):
    v = MEDIA["videos"].get(mid)
    if not v:
        fail(f"media: falta el video «{mid}»")
        return ""
    alt_es, alt_en = alt_for(mid)
    srcs = []
    if "webm" in v["files"]:
        check_file(v["files"]["webm"]["path"])
        srcs.append(f'<source src="{v["files"]["webm"]["path"]}" type=\'video/webm; codecs="av01.0.05M.08"\'>')
    check_file(v["files"]["mp4"]["path"])
    srcs.append(f'<source src="{v["files"]["mp4"]["path"]}" type="video/mp4">')
    poster = v["poster"]["webp"]["path"]
    check_file(poster)
    fx, fy = v.get("focal", [50, 50])
    return (f'<div class="vid {cls}" style="--pos:{fx}% {fy}%;--dom:{v.get("color", "#2a1a14")}">'
            f'<video muted playsinline loop preload="none" data-poster="{poster}" width="{v["width"]}" height="{v["height"]}" '
            f'aria-label="{html.escape(alt_es)}" data-aria-en="{html.escape(alt_en)}">{"".join(srcs)}</video>'
            f'<button type="button" class="vid-b" aria-pressed="false" data-ui data-en="Pause video" data-es-alt="Reproducir video" data-en-alt="Play video">Pausar video</button>'
            f'</div>')


def credit(mid, ui="Foto", inline=False, cls=""):
    e = MEDIA["images"].get(mid) or MEDIA["videos"].get(mid)
    if e and "alias" in e:
        e = MEDIA["images"].get(e["alias"])
    if not e:
        fail(f"crédito: falta el id «{mid}»")
        return ""
    who, post = e.get("credit"), e.get("post")
    if not who:
        fail(f"crédito: «{mid}» no tiene crédito en media.json")
        return ""
    ui_en = {"Foto": "Photo", "Video": "Video"}[ui]
    handle = who.lstrip("@")
    inner = (f'<span data-ui data-en="{ui_en}">{ui}</span> '
             f'<span data-src="{post}"><a href="https://www.instagram.com/{handle}/">{who}</a></span>')
    if inline:
        return inner
    return f'<p class="pie {cls}">{inner}</p>'


# ------------------------------------------------------------------ carta
def all_items():
    for s in CARTA["secciones"]:
        for g in s["grupos"]:
            for it in g["items"]:
                yield s, g, it


def precio_de(nombre):
    for _, _, it in all_items():
        if it["nombre"] == nombre and "precio" in it:
            return it["precio"]
    fail(f"carta: no hay precio para «{nombre}»")
    return ""


GROUP_EN = {
    "Tintelis": "Tintelis [reds]", "Blanquelis": "Blanquelis [whites]", "Whiscachos": "Whiscachos [whiskies]",
    "Ron poromponpon": "Ron poromponpon [rum]", "Vodkita": "Vodkita [vodka]", "Pa los chichichos": "Pa los chichichos [kids]",
    "Somos dulzones": "Somos dulzones [desserts]", "Picoteos": "Small plates", "Greditas": "Greditas [clay-pot dishes]",
    "Sanguches": "Sandwiches", "Pizzas artesanales": "Artisan pizzas", "Mocktails de la casa": "House mocktails",
    "Jugos & bebidas": "Juices & soft drinks", "Cervezas sin alcohol": "Alcohol-free beers", "Bebidas calientes": "Hot drinks",
}
TAG_EN = {"veggie": "veggie", "vegan": "vegan", "picante": "spicy", "nuevo": "new"}
TAG_SVG = {  # iconos dibujados, un solo trazo (1.5), sin emoji
    "veggie": '<path d="M3 13c0-6 4-10 10-10 0 6-4 10-10 10Zm0 0 6-6"/>',
    "vegan": '<path d="M2.5 4 8 13l5.5-9M8 13V8"/>',
    "picante": '<path d="M8 2c1 3 4 4 4 8a4 4 0 0 1-8 0c0-2 1-3 2-4 0 2 1 3 2 3 0-3-1-5 0-7Z"/>',
    "nuevo": '<path d="M8 1.5 9.8 6l4.7.3-3.6 3 1.2 4.6L8 11.4l-4.1 2.5 1.2-4.6-3.6-3L6.2 6Z"/>',
}

# ---- la carta en su página (/carta/): pestañas con las secciones de Almud, tinte suave por pestaña ----
TABS = [  # (ancla, secciones de carta-v2.json, glosa EN, tinte)
    ("casa", ["cocteleria-de-la-casa"], "House cocktails", "fucsia"),
    ("mundo", ["cocteles-del-mundo-mundial"], "Cocktails from all over the world [del mundo mundial]", "turquesa"),
    ("espirituosos", ["espirituosos"], "Spirits", "amarillo"),
    ("vinos", ["vinos-espumantes"], "Wines & sparkling", "coral"),
    ("sin-alcohol", ["mocktails-sin-alcohol", "jugos-bebidas", "cervezas-sin-alcohol", "bebidas-calientes"], "Alcohol-free mocktails & drinks", "verde"),
    ("comilona", ["comilona"], "Comilona [food]", "papel"),
    ("promos", ["nuestras-promos"], "Weekly deals", "coral"),
]
CHIPS = {"mundo", "espirituosos", "sin-alcohol", "comilona"}  # pestañas largas: un grupo a la vez
SUB_SLUG = {
    "Piscolein o combinadito": "piscolein", "Ron poromponpon": "ron", "Amamos el GIN!": "gin",
    "Tequilazos & mezcalazos": "tequilas", "Red Bull te da aaalas": "red-bull", "Mocktails de la casa": "mocktails",
    "Mocktails clásicos": "clasicos", "Jugos & bebidas": "jugos", "Cervezas sin alcohol": "cervezas",
    "Bebidas calientes": "calientes", "Pizzas artesanales": "pizzas", "Pa los chichichos": "chichichos",
    "Somos dulzones": "dulzones",
}
TAB_LAM = {  # láminas de pestaña: foto real del ambiente, sin nombre de ítem
    "casa": [("img", "carta-lamina-barra"), ("img", "tragos-copa-naranja")],  # fase 16: P109; el bartender del muro rosa (P184) queda solo en el landing  # + una copa tallada (P097), sin nombre de trago  # crítica 1: foto nítida del muro rosa donde se hacen (P184, IG-050) en vez del loop V021 borroso
    "mundo": [("img", "tragos-sours")],  # tres copas con espuma y flores (P086, IG-079): ambiente, sin nombre de trago
    "espirituosos": [("img", "carta-lamina-negroni")],
    "vinos": [("img", "carta-lamina-vino")],
    "comilona": [("img", "carta-lamina-tacos")],  # fase 16: la cazuela repetía el Camarón que se duerme  # crítica 1: foto nítida de una gredita (P091, IG-079) en vez del loop V052 movido; la columna no cambia de ancho entre grupos
}
GROUP_LAM = {  # láminas de grupo: se ven solo con su grupo
    "mundo-negroni": [("img", "carta-grupo-negroni")],
    "mundo-spritz": [("img", "carta-grupo-spritz")],
    "comilona-pizzas": [("img", "carta-grupo-pizzas")],
}
ITEM_IMG = {  # foto del ítem: solo cuando la foto es ese ítem (caption que lo nombra o carta.json › img)
    ("cocteleria-de-la-casa", "Aquí te las traigo Peter"): "carta-peter",
    ("cocteleria-de-la-casa", "Cómo te voy a olvidar"): "carta-olvidar",
    ("cocteleria-de-la-casa", "Sagüer on Faia"): "carta-saguer",
    ("cocteleria-de-la-casa", "Sangría Foreva!"): "carta-sangria",
    ("cocteleria-de-la-casa", "A veces me pongo Coquette"): "carta-coquette",
    ("mocktails-sin-alcohol", "La moto chantá"): "carta-moto",
    ("comilona", "Tukulito Sakayama"): "carta-tukulito",
    ("comilona", "Con tuti si no pa qué!"): "carta-contuti",
    ("comilona", "Camarón que se duerme"): "carta-camaron",
    ("comilona", "Topiturrón"): "carta-topiturron",
    ("comilona", "Pizza dulzona"): "carta-pizza-dulzona",
    # fase 16: las promos van sin foto (todas o ninguna: el sábado no tiene, y la del miércoles repetía a la garzona del Equipo)
}
DIA_TINTE = {0: "coral", 1: "coral", 2: "coral", 3: "turquesa", 4: "fucsia", 5: "amarillo", 6: "verde"}  # como Hoy en Almud
THUMB_SIZES = "(min-width: 1024px) 144px, 104px"
NOLAM = []


def esc(s):
    return html.escape(s, quote=False)


def slug(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def tag_html(t):
    if t not in TAG_SVG:
        fail(f"carta: tag desconocido «{t}»")
        return ""
    return (f'<span class="tag" data-dato><svg viewBox="0 0 16 16" aria-hidden="true">{TAG_SVG[t]}</svg>'
            f'<span data-en="{TAG_EN[t]}">{t}</span></span>')


def gloss(en_text, cls="gl"):
    if key(en_text) not in EN_OK:
        fail(f"glosa EN fuera del guion: «{en_text}»")
    return f'<p class="{cls}" lang="en">{esc(en_text)}</p>'


def item_html(it, cols, foto=None, extra_cls=""):
    name = esc(it["nombre"])
    if it.get("dia"):
        name = f'<span class="fdia">{esc(it["dia"])}</span> {name}<span class="hoy-m" data-ui data-en="Today">Hoy</span>'
    tags = "".join(tag_html(t) for t in it.get("tags", []))
    if cols:
        prices = "".join(
            f'<span class="fp"><span class="vh">{esc(c)}: </span>{esc(it["precios"].get(c, ""))}</span>' if it["precios"].get(c)
            else '<span class="fp fp-0" aria-hidden="true"></span>' for c in cols)
    else:
        prices = f'<span class="fp">{esc(it["precio"])}</span>'
    desc_bits = [it[k] for k in ("desc", "bodega", "nota") if it.get(k)]
    desc = f'<p class="fd">{esc(" · ".join(desc_bits))}</p>' if desc_bits else ""
    th, cls = "", "fila" + extra_cls
    if foto:
        th = f'<div class="fila-foto f r45" data-rv>{picture(foto, sizes=THUMB_SIZES)}</div>'
        cls += " con-foto"
    return f'<li class="{cls}">{th}<p class="fn">{name}{tags}</p><p class="fps num">{prices}</p>{desc}</li>'


def lamina_html(kind, mid, data_g=""):
    g = f' data-g="{data_g}"' if data_g else ""
    cls = "lamina lam-g" if data_g else "lamina"
    sizes = "(min-width: 1024px) 30vw, 45vw"
    if kind == "img":
        cred = credit(mid) if (MEDIA["images"].get(mid) or {}).get("credit") else ""
        return f'<figure class="{cls}"{g}><div class="f r45" data-rv>{picture(mid, sizes=sizes)}</div>{cred}</figure>'
    return f'<figure class="{cls}"{g}><div data-rv>{video(mid, "f r45")}</div></figure>'


def group_html(s, g, head_title=None, sub=False):
    cols = g.get("columnas")
    head = ""
    titulo = g.get("titulo") or head_title
    if titulo:
        h = "h4" if g.get("padre") else "h3"
        head += f'<{h} class="cg-h{" cg-sub" if g.get("padre") else ""}">{esc(titulo)}</{h}>'
        if titulo in GROUP_EN:
            head += gloss(GROUP_EN[titulo], "gl small")
    if g.get("nota"):
        head += "".join(f'<p class="cg-nota small">{esc(l)}</p>' for l in g["nota"].split("\n"))
    colrow = ""
    if cols:
        colrow = '<p class="cg-cols small" aria-hidden="true"><span></span>' + "".join(f"<span>{esc(c)}</span>" for c in cols) + "</p>"
    rows = []
    for it in g["items"]:
        foto = ITEM_IMG.get((s["id"], it["nombre"]))
        extra = f' promo promo-d{it["dia_n"]}' if it.get("dia_n") is not None else ""
        rows.append(item_html(it, cols, foto, extra))
    foot = f'<p class="cg-pie small">{esc(g["nota_pie"])}</p>' if g.get("nota_pie") else ""
    ncls = f" cg-m cg-m{len(cols)}" if cols else ""
    return f'<div class="cg{ncls}">{head}{colrow}<ul class="filas">{"".join(rows)}</ul>{foot}</div>'


def subunits(tab, secs):
    """Grupos de primer nivel de la pestaña (los hijos con «padre» van con su padre)."""
    units = []
    for i, s in enumerate(secs):
        for g in s["grupos"]:
            if g.get("padre") and units:
                units[-1]["grupos"].append((s, g, None))
                continue
            label = g.get("titulo") or s["titulo"]
            head = None if g.get("titulo") or i == 0 else s["titulo"]
            sid = f"{tab}-{SUB_SLUG.get(label, slug(label))}"
            units.append({"id": sid, "label": label, "grupos": [(s, g, head)]})
    return units


def tab_panel(tab, secs, en, tinte):
    main = secs[0]
    units = subunits(tab, secs)
    intro = f'<p class="cs-intro small">{esc(main["intro"])}</p>' if main.get("intro") else ""
    cab = (f'<div class="cp-cab g"><h2 class="head cp-h" id="{tab}-h" data-lines>{esc(main["titulo"])}</h2>'
           f'{gloss(en, "gl cp-gl")}{intro}</div>')
    chips = ""
    if tab in CHIPS:
        links = "".join(f'<a class="chip" href="#{u["id"]}" id="c-{u["id"]}" data-tab="{tab}" data-sub="{u["id"]}">{esc(u["label"])}</a>'
                        for u in units)
        chips = (f'<div class="chips-sent" aria-hidden="true"></div><div class="chips-w"><div class="chips" data-tab="{tab}" '
                 f'aria-label="{esc(main["titulo"])}">{links}</div></div>')
    lams = [lamina_html(k, m) for k, m in TAB_LAM.get(tab, [])]
    for u in units:
        lams += [lamina_html(k, m, u["id"]) for k, m in GROUP_LAM.get(u["id"], [])]
    lam_html = f'<div class="laminas">{"".join(lams)}</div>' if lams else ""
    body = []
    for u in units:
        inner = "".join(group_html(s, g, head) for s, g, head in u["grupos"])
        if tab in CHIPS:
            body.append(f'<div class="csub" id="{u["id"]}" data-tab="{tab}">{inner}</div>')
        else:
            body.append(inner)
    cls = "cp" + (" cp-lam" if lams else "")
    if lams and tab in CHIPS and tab not in TAB_LAM:  # grupos sin lámina en una pestaña con láminas de grupo: la lista ocupa todo
        NOLAM.extend((tab, u["id"]) for u in units if u["id"] not in GROUP_LAM)
    panel = (f'<section class="{cls}" id="{tab}" data-tinte="{tinte}" aria-labelledby="{tab}-h">{cab}{chips}'
             f'<div class="cp-cuerpo g">{lam_html}<div class="cp-grupos">{"".join(body)}</div></div></section>')
    return panel, [u["id"] for u in units] if tab in CHIPS else []


def carta_tabs_html():
    by_id = {s["id"]: s for s in CARTA["secciones"]}
    used = [sid for _, ss, _, _ in TABS for sid in ss]
    if sorted(used) != sorted(by_id):
        fail("carta: las secciones de carta-v2.json no calzan con TABS")
    n_items = sum(len(g["items"]) for s in CARTA["secciones"] for g in s["grupos"])
    tabs = "".join(f'<a class="tab" href="#{t}" id="t-{t}" data-tab="{t}">{esc(by_id[ss[0]]["titulo"])}</a>' for t, ss, _, _ in TABS)
    panels, state = [], {}
    for t, ss, en, tinte in TABS:
        p, subs = tab_panel(t, [by_id[x] for x in ss], en, tinte)
        panels.append(p)
        state[t] = subs
    nav = ('<div class="tabs-sent" aria-hidden="true"></div>'
           f'<nav class="tabs" id="secciones" aria-label="Secciones de la carta" data-aria-en="Menu sections"><div class="tabs-l">{tabs}</div></nav>')
    out = (f'<div class="carta-cuerpo" lang="es" data-carta data-items="{n_items}">{nav}'
           f'<div class="cps">{"".join(panels)}</div></div>')
    return out, n_items, state


def carta_estado(state):
    """Estado inicial antes de pintar: pestaña y grupo desde el hash, día de la promo. Sin JS no se aplica nada."""
    tabs = [t for t, *_ in TABS]
    subs = {s: t for t, ss in state.items() for s in ss}
    defs = {t: ss[0] for t, ss in state.items() if ss}
    conf = json.dumps({"t": tabs, "s": subs, "d": defs}, separators=(",", ":"))
    script = ("<script>(function(){var R=document.documentElement;"
              "try{if(localStorage.getItem('almud-lang')==='en'){R.lang='en';}}catch(e){}R.classList.add('js');"
              f"var C={conf},h='';try{{h=decodeURIComponent(location.hash.slice(1));}}catch(e){{}}"
              "var t=C.t[0];if(C.s[h]){t=C.s[h];}else if(C.t.indexOf(h)>-1){t=h;}R.setAttribute('data-tab',t);"
              "for(var k in C.d){R.setAttribute('data-sub-'+k,C.s[h]===k?h:C.d[k]);}"
              "var d=-1;try{var q=/[?&]dia=(\\d)/.exec(location.search);if(q){d=+q[1];}else{"
              "var w=new Intl.DateTimeFormat('en-US',{timeZone:'America/Santiago',weekday:'short'}).format(new Date());"
              "d=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'].indexOf(w);}}catch(e){}R.setAttribute('data-dia',d);})();"
              "window.__en=function(){if(document.documentElement.lang!=='en')return;var l=document.querySelectorAll('[data-en]:not([data-es])');"
              "for(var i=0;i<l.length;i++){l[i].setAttribute('data-es',l[i].textContent);l[i].textContent=l[i].getAttribute('data-en');}};</script>")
    on_p = ",".join(f'html[data-tab="{t}"] #{t}' for t in tabs)
    on_t = ",".join(f'html[data-tab="{t}"] .tab[data-tab="{t}"]' for t in tabs)
    on_s = ",".join(f'html[data-sub-{t}="{s}"] #{s}' + (f',html[data-sub-{t}="{s}"] .lam-g[data-g="{s}"]' if s in GROUP_LAM else "")
                    for t, ss in state.items() for s in ss)
    on_c = ",".join(f'html[data-sub-{t}="{s}"] .chip[data-sub="{s}"]' for t, ss in state.items() for s in ss)
    tint = "".join(f'html[data-dia="{d}"] #promos{{--tinte:var(--tinte-{c})}}'
                   for d, c in DIA_TINTE.items())
    css = ("<style>/* estado de la carta (generado por build_v2.py): sin JS no aplica y todo queda a la vista */"
           ".js .cp,.js .csub,.js .lam-g{display:none}"
           f"{on_p},{on_s}{{display:block}}"
           f"{on_t}{{background:var(--tab-on-bg);color:var(--tab-on-ink);text-decoration-color:transparent}}"
           f"{on_c}{{background:var(--chip-on-bg);color:var(--chip-on-ink)}}"
           + ",".join(f'html[data-dia="{d}"] .promo-d{d} .hoy-m' for d in range(2, 7)) + "{display:inline-flex}"
           f"{tint}"
           + (",".join(f'html[data-sub-{t}="{u}"] #{t} .laminas' for t, u in NOLAM) + "{display:none}" if NOLAM else "")
           + (",".join(f'html[data-sub-{t}="{u}"] #{t} .cp-grupos' for t, u in NOLAM) + "{grid-column:1/-1}" if NOLAM else "")
           + "</style>")
    return script + css


# ---- landing: destacados de la carta (los productos con su mejor foto) ----
DESTACADOS = [  # (sección, fuente, rótulo literal, glosa EN, ítems, ancla en /carta/)
    ("cocteleria-de-la-casa", "CARTA-2", "Coctelería de la casa", "House cocktails",
     ["Aquí te las traigo Peter", "Sagüer on Faia", "Sangría Foreva!"], "casa"),
    ("mocktails-sin-alcohol", "CARTA-5", "Mocktails de la casa", "House mocktails", ["La moto chantá"], "sin-alcohol-mocktails"),
    ("comilona", "CARTA-1", "Comilona", "Comilona [food]", ["Tukulito Sakayama", "Camarón que se duerme", "Pizza dulzona"], "comilona"),
]


def destacados_html():
    by_id = {s["id"]: s for s in CARTA["secciones"]}
    out = []
    for sid, src, rot, en, names, anchor in DESTACADOS:
        items = {it["nombre"]: it for g in by_id[sid]["grupos"] for it in g["items"]}
        cards = []
        for n in names:
            it = items.get(n)
            mid = ITEM_IMG.get((sid, n))
            if not it or not mid:
                fail(f"destacados: «{n}» no está en {sid} o no tiene foto")
                continue
            cards.append(
                f'<li class="dest"><div class="f r45">{picture(mid, sizes="(min-width: 1024px) 23vw, (min-width: 700px) 30vw, 38vw")}</div>'
                f'<div class="dest-t"><p class="dest-n"><span class="fn" data-src="{src}">{esc(it["nombre"])}</span> '
                f'<span class="fp num" data-carta>{esc(it["precio"])}</span></p>'
                f'<p class="fd" data-src="{src}">{esc(it["desc"])}</p></div></li>')
        out.append(f'<div class="dest-g dest-{slug(sid)}"><h3 class="dest-h"><a class="link" href="carta/#{anchor}">'
                   f'<span data-src="{src}">{esc(rot)}</span></a></h3>{gloss(en, "gl small")}<ul class="dest-l">{"".join(cards)}</ul></div>')
    return "".join(out)


# ------------------------------------------------------------------ hoy
def promo(dia_n):
    for s in CARTA["secciones"]:
        if s["id"] == "nuestras-promos":
            g = s["grupos"][0]
            for it in g["items"]:
                if it.get("dia_n") == dia_n:
                    return it, g
    fail(f"hoy: no hay promo para el día {dia_n}")
    return {}, {}


def lines_html(t):
    return "<br>".join(esc(x.strip()) for x in t.split(" / "))


def hoy_html():
    weeks = []
    promos_sec = next(s for s in CARTA["secciones"] if s["id"] == "nuestras-promos")
    pg = promos_sec["grupos"][0]
    variants = []
    for v in HOY["variantes"]:
        on = v.get("nojs", False)
        media = v["media"]
        if "video" in media:
            fig = f'<figure class="hoy-foto">{video(media["video"], "f r45")}</figure>'
        else:
            fig = f'<figure class="hoy-foto"><div class="f r45">{picture(media["img"], sizes="(min-width: 1024px) 40vw, (min-width: 700px) 60vw, 100vw")}</div></figure>'
        p = []
        if v.get("dato"):
            p.append(f'<p class="hoy-dato num dato-es" data-src="{v["dato_src"]}">{esc(v["dato"])}</p>{gloss(v["dato_en"], "gl hoy-dato num")}')
            p.append(f'<p class="hoy-rot" data-ui data-en="{v["rotulo_en"]}">{esc(v["rotulo"])}</p>')
        if v.get("promo_dia"):
            it, _ = promo(v["promo_dia"])
            name = it.get("texto") or it.get("nombre")
            p.append(f'<p class="que" data-src="CARTA-7">{esc(name)}</p>{gloss(v["item_en"])}')
            if not v.get("sin_precio"):
                p.append(f'<p class="precio num dato-es" data-src="CARTA-7">{esc(it["precio"])}</p>{gloss("CLP 4,500", "gl precio num")}')
            p.append(f'<p class="cuando num dato-es" data-src="CARTA-7">{esc(pg["nota"])}</p>{gloss("6 to 10 pm", "gl cuando num")}')
            p.append(f'<p class="small dato-es" data-src="CARTA-7">{esc(pg["nota_pie"])}</p>{gloss("* Always subject to stock! *", "gl small")}')
        else:
            p.append(f'<p class="que" data-src="{v["item_src"]}">{esc(v["item"])}</p>{gloss(v["item_en"])}')
        frase = ""
        if v.get("frase"):
            frase = f'<p class="body" data-src="{v["frase_src"]}">{esc(v["frase"])}</p>{gloss(v["frase_en"])}'
        # crítica 1: «siempre es un güen día…» deja de ser rótulo chico sobre la lista y cierra la frase, en body
        frase = (f'<div class="hoy-frase">{frase}<p class="body hoy-siempre" data-src="{HOY["semana_titulo_src"]}">{esc(HOY["semana_titulo"])}</p>'
                 f'{gloss(HOY["semana_titulo_en"])}</div>')
        # la semana, con el día de esta variante marcado
        rows = []
        vie = HOY["viernes_semana"]  # crítica 1: el viernes con su línea literal (IG-003), sin promo inventada
        semana_items = [dict(it, src="CARTA-7") for it in pg["items"] if it["dia_n"] < vie["dia_n"]]
        semana_items.append({"dia": vie["dia"], "dia_n": vie["dia_n"], "texto": vie["linea"], "src": vie["src"]})
        semana_items += [dict(it, src="CARTA-7") for it in pg["items"] if it["dia_n"] > vie["dia_n"]]
        for it in semana_items:
            today = it["dia_n"] in v["dias"]
            name = it.get("texto") or it.get("nombre")
            hoy_tag = '<span class="es-hoy-m" data-ui data-en="Today">Hoy</span>' if today else ""
            rows.append(f'<li{" class=\"es-hoy\" aria-current=\"date\"" if today else ""}>'
                        f'<b><span data-src="{it["src"]}">{esc(it["dia"])}</span>{hoy_tag}</b>'
                        f'<span class="gl" lang="en">{esc(HOY["dias_en"][it["dia"]])}</span>'
                        f'<span data-src="{it["src"]}">{esc(name)}</span></li>')
        semana = f'<div class="semana"><ol class="semana-l num">{"".join(rows)}</ol></div>'

        acc = (f'<p class="hoy-acc acc"><a class="btn" href="carta/#promos" data-ui data-en="See the menu">Ver la carta</a>'
               f'<a class="link" href="{MAPS}" data-ui data-en="Get directions">Cómo llegar</a></p>')
        variants.append(
            f'<div class="hoy-dia g" data-dias="{" ".join(map(str, v["dias"]))}" data-campo="{v["campo"]}"{"" if on else " hidden"}>'
            f'<h2 class="display hoy-h" data-src="{v["titular_src"]}" data-lines>{lines_html(v["titular"])}</h2>'
            f'{gloss(v["titular_en"], "gl gl-h hoy-glh")}'
            f'{fig}<div class="hoy-promo">{"".join(p)}</div>{frase}{acc}{semana}</div>')
    default = next(v for v in HOY["variantes"] if v.get("nojs"))
    script = ("<script>(function(){try{var q=/[?&]dia=(\\d)/.exec(location.search),d;"
              "if(q){d=+q[1];}else{var w=new Intl.DateTimeFormat('en-US',{timeZone:'America/Santiago',weekday:'short'}).format(new Date());"
              "d=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'].indexOf(w);}"
              "var s=document.getElementById('hoy'),v=s.querySelectorAll('.hoy-dia');"
              "for(var i=0;i<v.length;i++){var on=(' '+v[i].getAttribute('data-dias')+' ').indexOf(' '+d+' ')>-1;v[i].hidden=!on;"
              "if(on){s.setAttribute('data-campo',v[i].getAttribute('data-campo'));}}}catch(e){}})();</script>")
    return (f'<section class="sec hoy on-field" id="hoy" data-campo="{default["campo"]}" aria-label="Hoy en Almud" data-aria-en="Today at Almud">'
            + "".join(variants) + "</section>" + script)


# ------------------------------------------------------------------ reseñas
def resenas_html():
    sec = COPY_TEXT.split("## 9. Reseñas")[1].split("## 10.")[0]
    blocks = re.split(r"\n  (?=\d\. «)", sec)[1:]
    out = []
    for i, b in enumerate(blocks):
        m = re.match(r"\d\. «([^»]+)» \[RESEÑA:([^\]]+)\]", b)
        if not m:
            fail("reseñas: no pude leer un bloque de §9")
            continue
        q, who = m.group(1), m.group(2)
        lang = re.search(r'`lang="(\w+)"`', b)
        lang = lang.group(1) if lang else "es"
        rv = next((r for r in REVIEWS if r["who"] == who and key(q).lower() in key(r["q"]).lower()), None)
        if not rv:
            fail(f"reseñas: «{q[:40]}» no está en reviews.json ({who})")
            continue
        en = re.search(r"“([^”]+)” \[EN\]", b)
        es = re.search(r"“([^”]+)” \[ES\]", b)
        gls = ""
        if es:
            gls += f'<p class="gl-es" lang="es">{esc(es.group(1))}</p>'
        if en:
            gls += f'<p class="gl" lang="en">{esc(en.group(1))}</p>'
        frm = f", {rv['from'].split(',')[0]}" if rv.get("from") else ""
        out.append(f'<figure class="res res-{i + 1}">'
                   f'<blockquote lang="{lang}"><p class="res-q" data-src="RESEÑA:{who}">{esc(q)}</p></blockquote>{gls}'
                   f'<figcaption class="small num" data-dato>{esc(rv["who"] if who != "Visitante" else "Visitante")}{esc(frm)} · {esc(rv["src"])} · {esc(rv["date"])}</figcaption></figure>')
    if len(out) != 6:
        fail(f"reseñas: se esperaban 6, hay {len(out)}")
    more = ('<p class="res-mas"><button type="button" class="link res-mas-b" aria-expanded="false" data-ui data-en="More reviews">Ver más reseñas</button></p>')
    return f'<div class="g res-g">{"".join(out)}</div>{more}'


# ------------------------------------------------------------------ símbolos y @
def symbols():
    svg = (ROOT / "brand/almud-horizontal-claro.svg").read_text()
    vb = re.search(r'viewBox="([^"]+)"', svg).group(1)
    inner = re.sub(r"<title>.*?</title>", "", svg.split(">", 1)[1].rsplit("</svg>", 1)[0], flags=re.S)
    inner = re.sub(r'fill="#[0-9a-fA-F]{3,6}"', 'fill="currentColor"', inner)
    return f'<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><symbol id="logo-h" viewBox="{vb}">{inner}</symbol></svg>'


def handles(m):
    return re.sub(r"@([\w.]+[\w])", lambda h: f'<a href="https://www.instagram.com/{h.group(1)}/">@{h.group(1)}</a>', m.group(1))


# ------------------------------------------------------------------ expansión
def attrs_of(s):
    return dict((k, v if v is not None else True) for k, v in re.findall(r'([\w-]+)(?:="([^"]*)")?', s))


def expand(src):
    src = src.replace("<x-symbols/>", symbols())
    src = re.sub(r"<x-handles>(.*?)</x-handles>", handles, src, flags=re.S)
    src = re.sub(r"<x-preload\s([^>]*?)/>", lambda m: (lambda a: preload(a["id"], a["crop"], a["sizes"], a.get("media"), a.get("mcrop"), a.get("msizes")))(attrs_of(m.group(1))), src)
    src = re.sub(r"<x-img\s([^>]*?)/>", lambda m: (lambda a: picture(a["id"], a.get("crop"), a.get("sizes", "100vw"), a.get("class", ""), "eager" in a, a.get("mcrop"), a.get("msizes"), a.get("media")))(attrs_of(m.group(1))), src)
    src = re.sub(r"<x-video\s([^>]*?)/>", lambda m: (lambda a: video(a["id"], a.get("class", ""), a.get("sizes", "")))(attrs_of(m.group(1))), src)
    src = re.sub(r"<x-credit\s([^>]*?)/>", lambda m: (lambda a: credit(a["id"], a.get("ui", "Foto"), "inline" in a, a.get("class", "")))(attrs_of(m.group(1))), src)
    src = re.sub(r"\{\{precio:([^}]+)\}\}", lambda m: esc(precio_de(m.group(1))), src)
    if "<x-hoy/>" in src:
        src = src.replace("<x-hoy/>", hoy_html())
    if "<x-resenas/>" in src:
        src = src.replace("<x-resenas/>", resenas_html())
    if "<x-destacados/>" in src:
        src = src.replace("<x-destacados/>", destacados_html())
    n = 0
    if "<x-carta-tabs/>" in src:
        carta, n, state = carta_tabs_html()
        src = src.replace("<x-carta-tabs/>", carta)
        src = src.replace("<x-carta-estado/>", carta_estado(state))
    leftover = re.findall(r"<x-[\w-]+|\{\{", src)
    if leftover:
        fail(f"plantilla: quedan marcas sin expandir: {sorted(set(leftover))}")
    # titulares en líneas con máscara
    def split_lines(m):
        open_tag, inner, close = m.group(1), m.group(2), m.group(3)
        parts = re.split(r"<br\s*/?>", inner)
        spans = "<br>".join(f'<span class="ln"><span class="li" style="--i:{i}">{p.strip()}</span></span>' for i, p in enumerate(parts))
        return open_tag + spans + close
    src = re.sub(r"(<h[1-6][^>]*\bdata-lines\b[^>]*>)(.*?)(</h[1-6]>)", split_lines, src, flags=re.S)
    src = re.sub(r"(<p class=\"firma\"[^>]*\bdata-lines\b[^>]*>)(.*?)(</p>)", split_lines, src, flags=re.S)  # la firma del pie, con máscara de línea
    # el texto de Almud se queda en español también en modo EN: lang="es" en cada literal
    def add_lang(m):
        t = m.group(0)
        return t if re.search(r'\slang="', t) or 'data-src="RESEÑA' in t else t[:-1] + ' lang="es">'
    src = re.sub(r"<[a-z][a-z0-9]*\b[^>]*\bdata-src=\"[^\"]*\"[^>]*>", add_lang, src)
    return src, n


# ------------------------------------------------------------------ verificación del texto visible
EMOJI = re.compile("[\U0001F000-\U0001FAFF☀-➿️‍⭐⬆↔-⇿]")
SKIP_TAGS = {"script", "style", "title", "svg", "noscript", "head"}
VOID = {"br", "img", "source", "meta", "link", "input", "hr", "wbr", "area", "base", "col", "embed", "param", "track"}


class Checker(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []  # (tag, kind, collector_index or None)
        self.cols = []   # [kind, tag_src, text]
        self.checked = {"src": 0, "gl": 0, "ui": 0, "en-attr": 0}

    def ctx(self):
        for tag, kind, ci in reversed(self.stack):
            if kind:
                return kind, ci
        return None, None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in VOID:
            if tag == "br":
                k, ci = self.ctx()
                if ci is not None:
                    self.cols[ci][2] += " / "
            self.attr_checks(a)
            return
        kind, ci = None, None
        cls = (a.get("class") or "").split()
        parent_kind, _ = self.ctx()
        if tag in SKIP_TAGS or parent_kind == "skip":
            kind = "skip"
        elif "data-carta" in a or "data-dato" in a:
            kind = "skip-ok"
        elif "data-src" in a:
            kind = "src"
        elif "gl" in cls:
            kind = "gl"
        elif "gl-es" in cls:
            kind = "gl-es"
        elif "data-ui" in a:
            kind = "ui"
        if kind in ("src", "gl", "gl-es", "ui"):
            self.cols.append([kind, a.get("data-src"), ""])
            ci = len(self.cols) - 1
        self.stack.append((tag, kind, ci))
        self.attr_checks(a)

    def handle_startendtag(self, tag, attrs):
        self.attr_checks(dict(attrs))

    def attr_checks(self, a):
        if "data-en" in a:
            self.checked["en-attr"] += 1
            if key(a["data-en"]) not in EN_OK and key(a["data-en"]) not in {key(x) for x in TAG_EN.values()}:
                fail(f"data-en fuera del guion: «{a['data-en']}»")
        for k in ("data-es-alt", "data-en-alt"):
            if k in a and key(a[k]) not in UI_OK:
                fail(f"{k} fuera del guion: «{a[k]}»")

    def handle_endtag(self, tag):
        while self.stack:
            t, kind, ci = self.stack.pop()
            if ci is not None:
                self.finish(ci)
            if t == tag:
                break

    def finish(self, ci):
        kind, tag, text = self.cols[ci]
        t = key(text)
        if not t:
            return
        if EMOJI.search(text):
            fail(f"emoji visible: «{text[:60]}»")
        if kind == "src":
            self.checked["src"] += 1
            if t not in LITS.get(tag, set()):
                fail(f"literal [{tag}] no está en el guion: «{text[:90]}»")
        elif kind == "gl":
            self.checked["gl"] += 1
            if t not in EN_OK:
                fail(f"glosa EN fuera del guion: «{text[:90]}»")
        elif kind == "gl-es":
            self.checked["gl"] += 1
            if t not in ES_SET:
                fail(f"glosa ES fuera del guion: «{text[:90]}»")
        elif kind == "ui":
            self.checked["ui"] += 1
            if t not in UI_OK:
                fail(f"etiqueta [UI] fuera del guion: «{text[:90]}»")

    def handle_data(self, data):
        kind, ci = self.ctx()
        if kind == "skip":
            return
        if EMOJI.search(data) and kind != "skip":
            fail(f"emoji visible: «{data.strip()[:60]}»")
        if vc.FORBIDDEN.search(data) and kind != "skip":
            fail(f"palabra prohibida (fila/espera): «{data.strip()[:60]}»")
        if ci is not None:
            self.cols[ci][2] += data
        elif kind != "skip-ok" and re.search(r"[A-Za-zÀ-ÿ]", data):
            fail(f"texto visible sin fuente ni marca: «{data.strip()[:80]}»")


def rebase(src, prefix):
    """Rutas relativas a la raíz -> relativas a una página en subcarpeta (carta/index.html)."""
    return re.sub(r'(?<=[\s"\'(,])(assets|css|js|brand|vendor)/', prefix + r"\1/", src)


def versioned(out):
    """Pulido 3: css/v2 y js/v2 llevan ?v=<hash del contenido>; así public/_headers los puede marcar immutable por un año
    y un cambio de CSS o JS llega igual al instante (la URL cambia)."""
    import hashlib

    def rep(m):
        f = ROOT / re.sub(r"^(\.\./|/)+", "", m.group(2))
        if not f.is_file():
            fail(f"versión: falta {f.relative_to(ROOT)}")
            return m.group(0)
        return f'{m.group(1)}{m.group(2)}?v={hashlib.sha256(f.read_bytes()).hexdigest()[:10]}"'
    return re.sub(r'((?:href|src)=")((?:\.\./|/)?(?:css|js)/v2/[\w.-]+\.(?:css|js))"', rep, out)


def build(src_path, prefix=""):
    out, n_items = expand(src_path.read_text())
    if prefix:
        out = rebase(out, prefix)
    out = versioned(out)
    body = re.split(r"<body[^>]*>", out, maxsplit=1)[1]
    ch = Checker()
    ch.feed(body)
    for m in re.finditer(r"<img\b[^>]*>", out):
        tag = m.group(0)
        if 'alt="' not in tag or "data-alt-en=" not in tag:
            fail(f"img sin alt o sin data-alt-en: {tag[:120]}")
    return out, n_items, ch


def main():
    pages = [(SRC, OUT, ""), (SRC_CARTA, OUT_CARTA, "../"), (SRC_404, OUT_404, "/")]
    built = []
    for src, dst, prefix in pages:
        before = len(errors)
        out, n_items, ch = build(src, prefix)
        for i in range(before, len(errors)):
            errors[i] = f"{src.relative_to(ROOT)}: {errors[i]}"
        built.append((dst, out, n_items, ch))
    if errors:
        print(f"build_v2.py: ERROR ({len(errors)}), no se escribió ninguna página", file=sys.stderr)
        for e in errors:
            print("  - " + e, file=sys.stderr)
        sys.exit(1)
    for dst, out, n_items, ch in built:
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(out)
        imgs = len(re.findall(r"<picture", out))
        vids = len(re.findall(r"<video", out))
        print(f"{dst.relative_to(ROOT)}: {len(out) / 1024:.0f} KB · {imgs} imágenes · {vids} videos"
              + (f" · carta {n_items} ítems" if n_items else "")
              + f" · verificados: {ch.checked['src']} literales, {ch.checked['gl']} glosas, {ch.checked['ui']} [UI], {ch.checked['en-attr']} data-en")


if __name__ == "__main__":
    main()
