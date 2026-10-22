"""Genera los SVG de marca v3 de Almud Bar (isotipo redibujado + logotipo desde fuentes).

Uso: python3 brand/v3/build_brand.py   (desde la raíz del proyecto)
- Isotipo: redibujo geométrico del almud del letrero (doble rombo, tres patas, V doble),
  a partir de los puntos extremos del trazado original brand/almud-isotipo.svg.
- Logotipo: ALMUD en Six Caps 400, BAR en Big Shoulders Display 800 (texto convertido a curvas).
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.varLib.instancer import instantiateVariableFont

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "brand" / "v3"
FONTS = ROOT / "assets" / "fonts"

NOCHE, PAPEL, CIELO, AZUL, BARRA = "#150b12", "#f6ecdc", "#36a3ff", "#2a2de8", "#ff3f6c"

# ---------------------------------------------------------------- isotipo
# Caja 620 x 900. Contornos como polígonos de línea central con trazo y unión a inglete.
ISO_W, ISO_H = 620, 900


def iso_paths(sw=26, legs=True, inner=True, chevron_ring=True):
    """Devuelve elementos SVG (sin color) del isotipo. sw = grosor del trazo."""
    h = sw / 2
    out = []
    # rombo exterior (tapa del almud)
    out.append(f'<path d="M289 {h+2}L{ISO_W-h-4} 215L266 {496-h-2}L{h+2} 181Z"/>')
    if inner:
        out.append('<path d="M287 76L512 217L271 409L87 192Z"/>')
    if legs:
        out.append('<path d="M60 318L101 606"/>')
        out.append('<path d="M549 290L446 650"/>')
        out.append('<path d="M285 545L282 760"/>')
    if chevron_ring:
        out.append(f'<path d="M62 600L{h+40} 676L285 {ISO_H-h-4}L480 712L476 652L285 806Z"/>')
    else:
        out.append(f'<path d="M50 640L285 {ISO_H-h-6}L478 680"/>')
    return out


def iso_group(color="currentColor", sw=26, **kw):
    body = "".join(iso_paths(sw, **kw))
    return (f'<g fill="none" stroke="{color}" stroke-width="{sw}" stroke-linejoin="miter" '
            f'stroke-miterlimit="10" stroke-linecap="butt">{body}</g>')


# ---------------------------------------------------------------- tipografía
def load(name, wght=None):
    f = TTFont(FONTS / name)
    if wght is not None:
        f = instantiateVariableFont(f, {"wght": wght})
    return f


def text_path(font, text, cap_px, x0, baseline, tracking=0.0):
    """Path SVG de `text` con altura de mayúscula cap_px, origen x0 y línea base `baseline`."""
    gs, cmap = font.getGlyphSet(), font.getBestCmap()
    # altura de mayúscula medida en la H
    b = BoundsPen(gs); gs[cmap[ord("H")]].draw(b)
    cap_units = b.bounds[3]
    s = cap_px / cap_units
    pen = SVGPathPen(gs)
    x = x0
    first = True
    xmin = None
    for ch in text:
        g = gs[cmap[ord(ch)]]
        bb = BoundsPen(gs); g.draw(bb)
        lsb = bb.bounds[0] if bb.bounds else 0
        if first:
            x -= lsb * s  # alinea el borde de tinta en x0
            first = False
        tp = TransformPen(pen, (s, 0, 0, -s, x, baseline))
        g.draw(tp)
        if xmin is None:
            xmin = x + lsb * s
        x_end_ink = x + (bb.bounds[2] if bb.bounds else g.width) * s
        x += g.width * s + tracking * cap_px
    return pen.getCommands(), x_end_ink


SIX = load("six-caps-latin-400-normal.woff2")
BIG = load("big-shoulders-display-latin-wght-normal.woff2", wght=800)


def svg(viewbox, body, label="Almud Bar"):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}" role="img" '
            f'aria-label="{label}"><title>{label}</title>{body}</svg>\n')


def write(name, content):
    (OUT / name).write_text(content)
    print("ok", name)


# ---------------------------------------------------------------- piezas
CAP = 600  # altura de mayúscula del logotipo (unidades)


def wordmark(x0, baseline, c_almud, c_bar, gap=0.10):
    d1, end1 = text_path(SIX, "ALMUD", CAP, x0, baseline, tracking=0.035)
    d2, end2 = text_path(BIG, "BAR", CAP, end1 + gap * CAP, baseline, tracking=0.02)
    body = f'<path fill="{c_almud}" d="{d1}"/><path fill="{c_bar}" d="{d2}"/>'
    return body, end2


def build():
    # 1) isotipo suelto
    pad = 20
    vb = f"{-pad} {-pad} {ISO_W+2*pad} {ISO_H+2*pad}"
    write("almud-isotipo.svg", svg(vb, iso_group("currentColor"), "Almud Bar isotipo"))
    write("almud-isotipo-claro.svg", svg(vb, iso_group(PAPEL), "Almud Bar isotipo"))
    write("almud-isotipo-oscuro.svg", svg(vb, iso_group(NOCHE), "Almud Bar isotipo"))

    # 2) logotipo ALMUD BAR
    for suf, ca, cb in [("", "currentColor", "currentColor"), ("-claro", PAPEL, CIELO),
                        ("-oscuro", NOCHE, AZUL)]:
        body, end = wordmark(0, CAP, ca, cb)
        write(f"almud-logotipo{suf}.svg", svg(f"-10 -10 {end+20:.0f} {CAP+20}", body))

    # 3) horizontal "letrero": ALMUD BAR + isotipo a la derecha (como el letrero real)
    iso_h = CAP * 1.32
    sc = iso_h / ISO_H
    for suf, ca, cb, ci in [("", "currentColor", "currentColor", "currentColor"),
                            ("-claro", PAPEL, CIELO, PAPEL), ("-oscuro", NOCHE, AZUL, NOCHE)]:
        top = (iso_h - CAP) / 2
        body, end = wordmark(0, top + CAP, ca, cb)
        ix = end + 0.22 * CAP
        g = f'<g transform="translate({ix:.1f} 0) scale({sc:.4f})">{iso_group(ci, sw=30)}</g>'
        W = ix + ISO_W * sc
        write(f"almud-horizontal{suf}.svg", svg(f"-10 -10 {W+20:.0f} {iso_h+20:.0f}", body + g))

    # 4) barra de navegación: isotipo a la izquierda + ALMUD BAR, compacto
    for suf, ca, cb, ci in [("", "currentColor", "currentColor", "currentColor"),
                            ("-claro", PAPEL, CIELO, PAPEL), ("-oscuro", NOCHE, AZUL, NOCHE)]:
        iso_h = CAP * 1.18
        sc = iso_h / ISO_H
        top = (iso_h - CAP) / 2
        g = f'<g transform="scale({sc:.4f})">{iso_group(ci, sw=38, legs=True)}</g>'
        x0 = ISO_W * sc + 0.24 * CAP
        body, end = wordmark(x0, top + CAP, ca, cb)
        write(f"almud-nav{suf}.svg", svg(f"-10 -10 {end+20:.0f} {iso_h+20:.0f}", g + body))

    # 5) vertical: isotipo arriba, ALMUD BAR abajo
    for suf, ca, cb, ci in [("", "currentColor", "currentColor", "currentColor"),
                            ("-claro", PAPEL, CIELO, PAPEL), ("-oscuro", NOCHE, AZUL, NOCHE)]:
        body, end = wordmark(0, 0, ca, cb)
        iso_h = CAP * 1.4
        sc = iso_h / ISO_H
        ix = (end - ISO_W * sc) / 2
        g = f'<g transform="translate({ix:.1f} 0) scale({sc:.4f})">{iso_group(ci, sw=30)}</g>'
        ty = iso_h + 0.28 * CAP + CAP
        body = f'<g transform="translate(0 {ty:.1f})">{body}</g>'
        write(f"almud-vertical{suf}.svg", svg(f"-10 -10 {end+20:.0f} {ty+20:.0f}", g + body))

    # 6) favicon: marca simplificada (rombo + V, trazo grueso) sobre baldosa noche
    # versión chica (16/32/48 e .ico y favicon.svg): sin patas ni rombo interior
    def fav(sw, inner, legs, ring, size_pad):
        # cuadrado centrado en el isotipo
        side = ISO_H + 2 * size_pad
        x = (ISO_W - side) / 2
        y = -size_pad
        rx = side * 0.22
        rect = f'<rect x="{x:.0f}" y="{y:.0f}" width="{side:.0f}" height="{side:.0f}" rx="{rx:.0f}" fill="{NOCHE}"/>'
        return svg(f"{x:.0f} {y:.0f} {side:.0f} {side:.0f}",
                   rect + iso_group(PAPEL, sw=sw, inner=inner, legs=legs, chevron_ring=ring),
                   "Almud Bar")
    # Chico: a 16 px las líneas finas desaparecen; se dibuja la tapa (rombo grueso) y el cuerpo
    # del almud como una sola silueta llena con la V recortada. Lee igual a 16 que a 512.
    pad = 40
    side = ISO_H + 2 * pad
    x, y = (ISO_W - side) / 2, -pad
    small = (f'<rect x="{x:.0f}" y="{y:.0f}" width="{side:.0f}" height="{side:.0f}" rx="{side*.22:.0f}" fill="{NOCHE}"/>'
             f'<path fill="none" stroke="{PAPEL}" stroke-width="78" stroke-linejoin="miter" d="M289 45L570 215L266 455L50 181Z"/>'
             f'<path fill="{PAPEL}" d="M50 300L120 330L150 600L285 720L420 600L500 300L575 270L520 650L285 870L40 660Z"/>')
    write("favicon.svg", svg(f"{x:.0f} {y:.0f} {side:.0f} {side:.0f}", small, "Almud Bar"))
    # Grande (180/192/512, ícono de inicio): el isotipo completo con trazo reforzado.
    write("favicon-detalle.svg", fav(sw=34, inner=True, legs=True, ring=True, size_pad=150))


if __name__ == "__main__":
    build()
