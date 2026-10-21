#!/usr/bin/env python3
"""Almud Bar v2 · build: src-v2/index.html -> index.html (raíz).

Inyecta:
  <x-img id crop sizes class [eager]/>   <picture> AVIF/WebP con srcset+sizes, width/height, LQIP, loading/fetchpriority
  <x-video id class sizes/>               <video> muted playsinline loop preload=none + póster + botón de pausa
  <x-preload id crop sizes/>              <link rel=preload as=image imagesrcset> de la portada
  <x-credit id [ui] [inline] [class]/>    "Foto @autor" con la fuente (post) de assets/v2/media.json
  <x-symbols/>                            símbolos SVG del logotipo (brand/)
  <x-handles>…</x-handles>                los @ como enlaces a Instagram (texto intacto)
  <x-hoy/> <x-resenas/> <x-carta/>        Hoy en Almud, reseñas y la carta, desde content/*.json
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
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import verify_copy as vc  # noqa: E402  (normalización y fuentes del guion)

SRC = ROOT / "src-v2" / "index.html"
OUT = ROOT / "index.html"
MEDIA = json.loads((ROOT / "assets/v2/media.json").read_text())
ALTS = json.loads((ROOT / "content/alts-v2.json").read_text())
CARTA = json.loads((ROOT / "content/carta-v2.json").read_text())
REVIEWS = json.loads((ROOT / "content/reviews.json").read_text())
HOY = json.loads((ROOT / "content/hoy-v2.json").read_text())
COPY_TEXT = (ROOT / "content/copy-v2.md").read_text()

MAPS = "https://www.google.com/maps/search/?api=1&amp;query=-42.4825681,-73.7617619"
DM = "https://ig.me/m/almud_bar"

# Etiquetas de interfaz nuestras que el guion no lista (accesibilidad y controles). Se declaran en el informe.
UI_EXTRA = {
    "Saltar al contenido", "Skip to content", "Almud Bar", "Pausar video", "Pause video",
    "Reproducir video", "Play video",
    "Índice de la carta", "Menu index",
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


def picture(mid, crop=None, sizes="100vw", cls="", eager=False):
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
    return (f'<picture class="ph {cls}">'
            f'<source type="image/avif" srcset="{srcsets["avif"]}" sizes="{sizes}">'
            f'<source type="image/webp" srcset="{srcsets["webp"]}" sizes="{sizes}">'
            f'<img src="{files["webp"][fallback]["path"]}" width="{c["width"]}" height="{c["height"]}" '
            f'alt="{html.escape(alt_es)}" data-alt-en="{html.escape(alt_en)}" {load} decoding="async" style="{style}">'
            f'</picture>')


def preload(mid, crop, sizes):
    e, _ = media_entry(mid)
    if not e:
        return ""
    files = e["crops"][crop]["files"]["avif"]
    ss = ", ".join(f'{files[w]["path"]} {w}w' for w in sorted(files, key=int))
    return f'<link rel="preload" as="image" type="image/avif" imagesrcset="{ss}" imagesizes="{sizes}" fetchpriority="high">'


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
            f'<video muted playsinline loop preload="none" poster="{poster}" width="{v["width"]}" height="{v["height"]}" '
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


CARTA_ORDER = [  # orden del guion (tragos, sin alcohol, bebidas, comilona, promos) y su ancla
    ("cocteleria-de-la-casa", "carta-casa", "House cocktails"),
    ("cocteles-del-mundo-mundial", "carta-mundo", "Cocktails from all over the world [del mundo mundial]"),
    ("espirituosos", "carta-espirituosos", "Spirits"),
    ("mocktails-sin-alcohol", "carta-sin-alcohol", "House mocktails"),
    ("jugos-bebidas", "carta-jugos", "Juices & soft drinks"),
    ("cervezas-sin-alcohol", "carta-cervezas", "Alcohol-free beers"),
    ("bebidas-calientes", "carta-calientes", "Hot drinks"),
    ("vinos-espumantes", "carta-vinos", "Wines & sparkling"),
    ("comilona", "carta-comilona", "Comilona [food]"),
    ("nuestras-promos", "carta-promos", "Weekly deals"),
]
GROUP_EN = {
    "Tintelis": "Tintelis [reds]", "Blanquelis": "Blanquelis [whites]", "Whiscachos": "Whiscachos [whiskies]",
    "Ron poromponpon": "Ron poromponpon [rum]", "Vodkita": "Vodkita [vodka]", "Pa los chichichos": "Pa los chichichos [kids]",
    "Somos dulzones": "Somos dulzones [desserts]", "Picoteos": "Small plates", "Greditas": "Greditas [clay-pot dishes]",
    "Sanguches": "Sandwiches", "Pizzas artesanales": "Artisan pizzas", "Mocktails de la casa": "House mocktails",
}
LAMINAS = {  # una lámina (foto real o loop) por sección de la carta, donde existe
    "cocteleria-de-la-casa": [("img", "carta-peter")],
    "cocteles-del-mundo-mundial": [("video", "carta-muro-rosa")],
    "espirituosos": [("img", "carta-lamina-negroni")],
    "mocktails-sin-alcohol": [("img", "carta-moto")],
    "comilona": [("img", "carta-contuti"), ("video", "carta-cazuela")],
}
TRIO = {"jugos-bebidas", "cervezas-sin-alcohol", "bebidas-calientes"}
TAG_EN = {"veggie": "veggie", "vegan": "vegan", "picante": "spicy", "nuevo": "new"}
TAG_SVG = {  # iconos dibujados, un solo trazo (1.5), sin emoji
    "veggie": '<path d="M3 13c0-6 4-10 10-10 0 6-4 10-10 10Zm0 0 6-6"/>',
    "vegan": '<path d="M2.5 4 8 13l5.5-9M8 13V8"/>',
    "picante": '<path d="M8 2c1 3 4 4 4 8a4 4 0 0 1-8 0c0-2 1-3 2-4 0 2 1 3 2 3 0-3-1-5 0-7Z"/>',
    "nuevo": '<path d="M8 1.5 9.8 6l4.7.3-3.6 3 1.2 4.6L8 11.4l-4.1 2.5 1.2-4.6-3.6-3L6.2 6Z"/>',
}


def esc(s):
    return html.escape(s, quote=False)


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


def item_html(it, cols):
    name = esc(it["nombre"])
    if it.get("dia"):
        name = f'<span class="fdia">{esc(it["dia"])}</span> {name}'
    tags = "".join(tag_html(t) for t in it.get("tags", []))
    if cols:
        prices = "".join(
            f'<span class="fp"><span class="vh">{esc(c)}: </span>{esc(it["precios"].get(c, ""))}</span>' if it["precios"].get(c)
            else '<span class="fp fp-0" aria-hidden="true"></span>' for c in cols)
    else:
        prices = f'<span class="fp">{esc(it["precio"])}</span>'
    desc_bits = [it[k] for k in ("desc", "bodega", "nota") if it.get(k)]
    desc = f'<p class="fd">{esc(" · ".join(desc_bits))}</p>' if desc_bits else ""
    return f'<li class="fila"><p class="fn">{name}{tags}</p><p class="fps num">{prices}</p>{desc}</li>'


def lamina_html(kind, mid):
    if kind == "img":
        cred = credit(mid) if (MEDIA["images"].get(mid) or {}).get("credit") else ""
        return f'<figure class="lamina"><div class="f r45" data-rv>{picture(mid, sizes="(min-width: 1024px) 30vw, (min-width: 700px) 45vw, 90vw")}</div>{cred}</figure>'
    return f'<figure class="lamina">{video(mid, "f r45")}</figure>'


def section_html(s, anchor, en):
    grupos = []
    for g in s["grupos"]:
        cols = g.get("columnas")
        head = ""
        if g.get("titulo"):
            sub = " cg-sub" if g.get("padre") else ""
            head += f'<h4 class="cg-h{sub}">{esc(g["titulo"])}</h4>'
            if g["titulo"] in GROUP_EN:
                head += gloss(GROUP_EN[g["titulo"]], "gl small")
        if g.get("nota"):
            head += "".join(f'<p class="cg-nota small">{esc(l)}</p>' for l in g["nota"].split("\n"))
        colrow = ""
        if cols:
            colrow = '<p class="cg-cols small" aria-hidden="true"><span></span>' + "".join(f"<span>{esc(c)}</span>" for c in cols) + "</p>"
        rows = "".join(item_html(it, cols) for it in g["items"])
        foot = f'<p class="cg-pie small">{esc(g["nota_pie"])}</p>' if g.get("nota_pie") else ""
        ncls = f" cg-m cg-m{len(cols)}" if cols else ""
        grupos.append(f'<div class="cg{ncls}">{head}{colrow}<ul class="filas">{rows}</ul>{foot}</div>')
    intro = f'<p class="cs-intro small">{esc(s["intro"])}</p>' if s.get("intro") else ""
    lams = LAMINAS.get(s["id"], [])
    lam_html = f'<div class="laminas">{"".join(lamina_html(k, m) for k, m in lams)}</div>' if lams else ""
    cls = "cs" + (" cs-lam" if lams else "") + (" cs-trio-i" if s["id"] in TRIO else "")
    return (f'<section class="{cls}" id="{anchor}" aria-labelledby="{anchor}-h">'
            f'<div class="cs-cab"><h3 class="head cs-h" id="{anchor}-h">{esc(s["titulo"])}</h3>{gloss(en)}{intro}</div>'
            f'{lam_html}<div class="cs-grupos">{"".join(grupos)}</div></section>')


def carta_html():
    by_id = {s["id"]: s for s in CARTA["secciones"]}
    if set(by_id) != {k for k, _, _ in CARTA_ORDER}:
        fail("carta: las secciones de carta-v2.json no calzan con CARTA_ORDER")
    n_items = sum(len(g["items"]) for s in CARTA["secciones"] for g in s["grupos"])
    idx = "".join(f'<li><a class="link" href="#{a}">{esc(by_id[k]["titulo"])}</a></li>' for k, a, _ in CARTA_ORDER)
    out = [f'<nav class="carta-indice g" aria-label="Índice de la carta" data-aria-en="Menu index"><ul>{idx}</ul></nav>',
           '<div class="carta-secs">']
    trio = []
    for k, a, en in CARTA_ORDER:
        h = section_html(by_id[k], a, en)
        if k in TRIO:
            trio.append(h)
            if len(trio) == 3:
                out.append(f'<div class="cs-trio">{"".join(trio)}</div>')
            continue
        out.append(h)
    out.append("</div>")
    return f'<div class="carta-cuerpo" lang="es" data-carta data-items="{n_items}">' + "".join(out) + "</div>", n_items


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
            p.append(f'<p class="hoy-dato num" data-src="{v["dato_src"]}">{esc(v["dato"])}</p>{gloss(v["dato_en"])}')
            p.append(f'<p class="hoy-rot" data-ui data-en="{v["rotulo_en"]}">{esc(v["rotulo"])}</p>')
        if v.get("promo_dia"):
            it, _ = promo(v["promo_dia"])
            name = it.get("texto") or it.get("nombre")
            p.append(f'<p class="que" data-src="CARTA-7">{esc(name)}</p>{gloss(v["item_en"])}')
            if not v.get("sin_precio"):
                p.append(f'<p class="precio num" data-src="CARTA-7">{esc(it["precio"])}</p>{gloss("CLP 4,500")}')
            p.append(f'<p class="cuando num" data-src="CARTA-7">{esc(pg["nota"])}</p>{gloss("6 to 10 pm")}')
            p.append(f'<p class="small" data-src="CARTA-7">{esc(pg["nota_pie"])}</p>{gloss("* Always subject to stock! *", "gl small")}')
        else:
            p.append(f'<p class="que" data-src="{v["item_src"]}">{esc(v["item"])}</p>{gloss(v["item_en"])}')
        frase = ""
        if v.get("frase"):
            frase = f'<div class="hoy-frase"><p class="body" data-src="{v["frase_src"]}">{esc(v["frase"])}</p>{gloss(v["frase_en"])}</div>'
        # la semana, con el día de esta variante marcado
        rows = []
        for it in pg["items"]:
            today = it["dia_n"] in v["dias"]
            name = it.get("texto") or it.get("nombre")
            hoy_tag = '<span class="es-hoy-m" data-ui data-en="Today">Hoy</span>' if today else ""
            rows.append(f'<li{" class=\"es-hoy\" aria-current=\"date\"" if today else ""}>'
                        f'<b><span data-src="CARTA-7">{esc(it["dia"])}</span>{hoy_tag}</b>'
                        f'<span class="gl" lang="en">{esc(HOY["dias_en"][it["dia"]])}</span>'
                        f'<span data-src="CARTA-7">{esc(name)}</span></li>')
        semana = (f'<div class="semana"><p class="small" data-src="{HOY["semana_titulo_src"]}">{esc(HOY["semana_titulo"])}</p>'
                  f'{gloss(HOY["semana_titulo_en"], "gl small")}<ol class="semana-l num">{"".join(rows)}</ol></div>')
        acc = (f'<p class="hoy-acc acc"><a class="btn" href="#carta-promos" data-ui data-en="See the menu">Ver la carta</a>'
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
        out.append(f'<figure class="res res-{i + 1}" data-rv="fade">'
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
    src = re.sub(r"<x-preload\s([^>]*?)/>", lambda m: (lambda a: preload(a["id"], a["crop"], a["sizes"]))(attrs_of(m.group(1))), src)
    src = re.sub(r"<x-img\s([^>]*?)/>", lambda m: (lambda a: picture(a["id"], a.get("crop"), a.get("sizes", "100vw"), a.get("class", ""), "eager" in a))(attrs_of(m.group(1))), src)
    src = re.sub(r"<x-video\s([^>]*?)/>", lambda m: (lambda a: video(a["id"], a.get("class", ""), a.get("sizes", "")))(attrs_of(m.group(1))), src)
    src = re.sub(r"<x-credit\s([^>]*?)/>", lambda m: (lambda a: credit(a["id"], a.get("ui", "Foto"), "inline" in a, a.get("class", "")))(attrs_of(m.group(1))), src)
    src = re.sub(r"\{\{precio:([^}]+)\}\}", lambda m: esc(precio_de(m.group(1))), src)
    src = src.replace("<x-hoy/>", hoy_html())
    src = src.replace("<x-resenas/>", resenas_html())
    carta, n = carta_html()
    src = src.replace("<x-carta/>", carta)
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


def main():
    src = SRC.read_text()
    out, n_items = expand(src)
    body = out.split("<body>", 1)[1]
    ch = Checker()
    ch.feed(body)
    # alt-en en cada imagen
    for m in re.finditer(r"<img\b[^>]*>", out):
        tag = m.group(0)
        if 'alt="' not in tag or "data-alt-en=" not in tag:
            fail(f"img sin alt o sin data-alt-en: {tag[:120]}")
    if errors:
        print(f"build_v2.py: ERROR ({len(errors)}), index.html no se escribió", file=sys.stderr)
        for e in errors:
            print("  - " + e, file=sys.stderr)
        sys.exit(1)
    OUT.write_text(out)
    imgs = len(re.findall(r"<picture", out))
    vids = len(re.findall(r"<video", out))
    print(f"index.html: {len(out) / 1024:.0f} KB · {imgs} imágenes · {vids} videos · carta {n_items} ítems · "
          f"verificados: {ch.checked['src']} literales, {ch.checked['gl']} glosas, {ch.checked['ui']} [UI], {ch.checked['en-attr']} data-en")


if __name__ == "__main__":
    main()
