#!/usr/bin/env python3
"""Boceto funcional v3 (fase 8): genera v3/index.html desde assets/v3/media.json.
Texto: solo content/copy-v3.md. Rutas relativas desde /v3/.
Uso: python3 tools/boceto_v3.py
"""
import json, html, pathlib, re, hashlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
M = json.loads((ROOT / 'assets/v3/media.json').read_text())
IM = dict(M['images'])
_NV2 = ROOT / 'assets/nv2/media-img.json'  # v4 fase 3: recortes nuevos de /nueva_v2/ (tools/media_nv2.py)
if _NV2.exists():
    IM.update(json.loads(_NV2.read_text())['images'])
VI = json.loads((ROOT / 'assets/v4/media-video.json').read_text())['videos']  # v4 fase 2: loops de 8–10 s hacia adelante con fundido
import os
RAIZ = True  # v4: se construye en /nueva/ con rutas absolutas   # fase 20: la v3 pasa a ser / (rutas absolutas)
UP = '/' if RAIZ else '../'
PATH = '/nueva_v8/'
E = html.escape


def srcset(files, kind):
    return ', '.join(f"{UP}{v['path']} {w}w" for w, v in sorted(files[kind].items(), key=lambda kv: int(kv[0])))


def pic(id_, crop='a', sizes='100vw', cls='', eager=False, alt=True, speed=None, extra='', art=None):
    """art = (recorte, media, sizes): dirección de arte (otro recorte desde ese ancho; v4 fase 3)."""
    im = IM[id_]
    c = im['crops'][crop]
    w, h = c['width'], c['height']
    files = c['files']
    widths = sorted(int(x) for x in files['webp'])
    fb = next((x for x in widths if x >= 720), widths[-1])
    a_es = E(im['alt']['es']) if alt else ''
    a_en = E(im['alt']['en']) if alt else ''
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    D = '' if eager else 'data-'  # v4 fase 2: las fotos no prioritarias se cargan por JS al acercarse (≤0,5 pantallas)
    sp = f' data-speed="{speed}"' if speed is not None else ''
    return (f'<figure class="m {cls}" style="--ar:{w}/{h};--c:{c["color"]};--lq:url({c["lqip"]})"{sp}{extra}>'
            f'<picture>'
            + (''.join(f'<source type="image/{k}" media="{art[1]}" {D}srcset="{srcset(im["crops"][art[0]]["files"], k)}" sizes="{art[2]}">' for k in ('avif', 'webp')) if art else '')
            + f'<source type="image/avif" {D}srcset="{srcset(files, "avif")}" sizes="{sizes}">'
            f'<source type="image/webp" {D}srcset="{srcset(files, "webp")}" sizes="{sizes}">'
            f'<img {D}src="{UP}{files["webp"][str(fb)]["path"]}" width="{w}" height="{h}" alt="{a_es}"'
            + (f' data-alt-en="{a_en}"' if alt else '') +
            f' {load} decoding="async"></picture>'
            + ('' if eager else f'<noscript><img src="{UP}{files["webp"][str(fb)]["path"]}" width="{w}" height="{h}" alt="{a_es}"></noscript>')
            + '</figure>')


def vid(id_, cls='', hero=False, extra=''):
    v = VI[id_]
    w, h = v['width'], v['height']
    poster = UP + v['poster']['webp']['path']
    return (f'<figure class="m m--v {cls}" style="--ar:{w}/{h};--c:{v["color"]};--lq:url({v["lqip"]})"{extra}>'
            f'<video class="v" autoplay muted loop playsinline preload="none" width="{w}" height="{h}" data-poster="{poster}"'
            f' data-webm="{UP}{v["files"]["webm"]["path"]}" data-mp4="{UP}{v["files"]["mp4"]["path"]}"'
            + (' data-hero' if hero else '') +
            f' aria-label="{E(v["alt"]["es"])}" data-aria-en="{E(v["alt"]["en"])}"></video>'
            f'<noscript><img class="v" src="{poster}" width="{w}" height="{h}" alt="{E(v["alt"]["es"])}"></noscript></figure>')


def ver(*paths):
    h = hashlib.md5()
    for q in paths:
        h.update((ROOT / q).read_bytes())
    return h.hexdigest()[:8]


SITE = 'https://almudbar.pages.dev'
OG = f'''<meta property="og:type" content="website">
<meta property="og:site_name" content="Almud Bar">
<meta property="og:title" content="Almud Bar · Castro, Chiloé">
<meta property="og:description" content="Coctelería de autor, comida &amp; música bonita desde 2014. Serrano 325, Castro.">
<meta property="og:url" content="{SITE}{PATH}">
<meta property="og:image" content="{SITE}/assets/v3/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Almud Bar, Castro">
<meta property="og:locale" content="es_CL">
<meta property="og:locale:alternate" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{SITE}/assets/v3/og.jpg">'''


def t(es, en, tag='span', cls='', attrs=''):
    """Etiqueta [UI]: se reemplaza por EN."""
    c = f' class="{cls}"' if cls else ''
    return f'<{tag}{c} data-en="{E(en)}"{attrs}>{E(es)}</{tag}>'


def g(en, cls='gloss'):
    """Glosa EN de un literal de Almud (solo visible en modo EN)."""
    return f'<span class="{cls}" lang="en">{E(en)}</span>'


def title(es, en, idn, cls=''):
    return (f'<h2 class="ttl {cls}" id="{idn}"><span class="ttl__t">{E(es)}</span></h2>'
            f'<p class="ttl-gloss">{g(en)}</p>')


SVG = {n: (ROOT / f'brand/v3/{n}.svg').read_text().strip() for n in
       ['almud-horizontal-claro', 'almud-nav-claro', 'almud-isotipo', 'almud-vertical-claro']}


def svg_inline(name, cls, label=None):
    s = (SVG[name].replace('fill="#36a3ff"', 'style="fill:var(--letrero-azul)"').replace('fill="#f6ecdc"', 'style="fill:var(--letrero-blanco)"')
             .replace('stroke="#f6ecdc"', 'style="stroke:var(--letrero-blanco)"'))
    s = re.sub(r'<title>.*?</title>', '', s)
    s = s.replace('<svg ', f'<svg class="{cls}" ' + ('aria-hidden="true" focusable="false" ' if not label else ''), 1)
    if not label:
        s = re.sub(r' role="img"| aria-label="[^"]*"', '', s)
    return s


IG = 'https://www.instagram.com/'
MAPS = 'https://www.google.com/maps/search/?api=1&query=Almud+Bar+Serrano+325+Castro+Chile'
DM = 'https://ig.me/m/almud_bar'
CARTA = '/nueva/carta/'

# ───────────────────────── secciones ─────────────────────────
rincones = [
    ('lugar-barra', 'a', 'Barra', 'The bar', 'Pucha que nos gusta nuestra barrita!', 'Gosh, we love our little bar!'),
    ('lugar-terraza-techada', 'a', 'Terraza techada', 'Covered terrace', 'Techamos parte de la terraza', 'Part of the terrace has a roof now'),
    ('lugar-sillones', 'a', 'Sillones', 'Lounge', None, None),
    ('lugar-terraza-abierta', 'a', 'Terraza', 'Terrace', 'Amamos los atardeceres desde nuestra terracita', 'We love a sunset from our little terrace'),
    ('lugar-lampara-pinzas', 'a', 'Lámparas', 'Lamps', 'Nos gustan los brillitos, las luces', 'We love a little sparkle and twinkly lights'),
    ('lugar-ojo-piojo', 'm', 'Ojo Piojo', 'Ojo Piojo [Heads up! · eye mural]', 'una mirada vale más que mil palabras', 'A look says more than a thousand words'),
]


def rincon_li(r, i):
    id_, crop, lab, lab_en, line, line_en = r
    cap = ''
    if lab:
        name = (f'<h3 class="rin__n">{E(lab)} {g("[" + lab_en.split(" [")[1], "gloss gloss--i")}</h3>'
                if '[' in lab_en else f'<h3 class="rin__n" data-en="{E(lab_en)}">{E(lab)}</h3>')
        cap = f'<figcaption class="rin__c">{name}' + (f'<p class="rin__l">{E(line)}{g(line_en)}</p>' if line else '') + '</figcaption>'
    return (f'<li class="rin" style="--i:{i}">' + pic(id_, crop, '(min-width:1024px) 30vw, (min-width:768px) 44vw, 76vw', 'rin__m') + cap + '</li>')


C_CASA = CARTA + '#casa'
_GL = json.loads((ROOT / 'content/carta-glosas-en-v3.json').read_text())
GL_CARNE = _GL.get('La carne es débil', '[Sautéed beef, mushrooms and cherry tomatoes]')
GL_QUESO = _GL.get('Una cosa poca', '[Baked cheese fondue with tomato, avocado and pesto]')
C_MOC = CARTA + '#mocktails-sin-alcohol-mocktails-de-la-casa'
C_PIC = CARTA + '#comilona-picoteos'
C_GRE = CARTA + '#comilona-greditas'
C_PIZ = CARTA + '#comilona-pizzas-artesanales'


def item(id_, name, price, gl, cls='', sizes='(min-width:1024px) 22vw, 45vw', speed=None):
    return (f'<a class="it {cls}" href="{C_CASA}"' + (f' data-speed="{speed}"' if speed is not None else '') + '>'
            + pic(id_, 'a', sizes, 'it__m reveal') +
            f'<span class="it__n">{E(name)}</span>{g(gl, "gloss gloss--s")}<span class="it__p">{E(price)}</span></a>')


def item2(id_, name, price, gl, href, cls='', sizes='(min-width:1024px) 22vw, 45vw', rv=''):
    """v4 fase 3: ítem de carta con nombre y precio literales de content/carta-v2.json y su ancla en la carta."""
    return (f'<a class="it {cls}" href="{href}">' + pic(id_, 'a', sizes, 'it__m ' + rv) +
            f'<span class="it__n">{E(name)}</span>{g(gl, "gloss gloss--s")}<span class="it__p">{E(price)}</span></a>')


C_SAN = CARTA + '#comilona-sanguches'
Q = '(min-width:1024px) 31vw, (min-width:768px) 31vw, 47vw'
# v4 fase 6 · Con quién: las 12 fotos de la baraja (mismo orden aprobado en la fase 3; los videos van aparte)
BARAJA = ['con-quien-barra', 'con-quien-amigos', 'quien-sillones-llenos', 'quien-carcajadas', 'con-quien-brindis', 'con-quien-amigas',
          'quien-grupo-peter', 'quien-copas-arriba', 'con-quien-risa', 'quien-grupo-flecos', 'con-quien-solo', 'quien-mesa-llena']
QB = '(min-width:1024px) 30vw, (min-width:768px) 60vw, 80vw'
Q_W = '(min-width:1024px) 31vw, (min-width:768px) 31vw, 92vw'

# v4 fase 7 · fiestas del slider: nombre y mes literales del calendario v3 (content/copy-v3.md), fotos propias de la fase 3.
# Negroni Week queda fuera (copy-v3: campaña internacional, sin foto propia); Bendita Primavera, también (una sola vez, en 2024,
# y su IG no dice el mes: sería inventarlo). Su foto aprobada sigue en la coda.
FIESTAS = [
    ('Aniversario', 'Jul', 'Jul', '[Anniversary]', [('p', 'eventos-12-anos'), ('p', 'eventos-cotillon-12'), ('p', 'eventos-baile-12')]),
    ('Fondita', 'Sep', 'Sep', "[Chile's Independence Day party]", [('p', 'eventos-fondita')]),
    ('Jalogüín', 'Oct', 'Oct', '[Halloween]', [('v', 'eventos-jaloguin'), ('p', 'eventos-jaloguin')]),
]


def fiesta_li(f, k):
    n, mes, mes_en, gl, fotos = f
    fs = ''.join(f'<div class="fs__f fs__f--{j + 1}">' + (vid(i, 'fs__m') if t == 'v' else pic(i, 'a', '(min-width:1024px) 22vw, 56vw', 'fs__m')) + '</div>' for j, (t, i) in enumerate(fotos))
    return (f'<li class="fs__s fs__s--{len(fotos)}" style="--len:{len(n)}" aria-label="{k + 1} / {len(FIESTAS)}">'
            f'<div class="fs__t"><p class="fs__mes" data-en="{mes_en}">{mes}</p><h3 class="fs__n">{E(n)}</h3>{g(gl, "gloss gloss--s")}</div>'
            f'<div class="fs__fotos">{fs}</div></li>')


eventos = [
    ('eventos-12-anos', 'Jul', 'Jul', 'Aniversario', 'Aniversario [Anniversary]', 7),
    ('eventos-fondita', 'Sep', 'Sep', 'Fondita', "Fondita [Chile's Independence Day party]", 9),
    ('eventos-jaloguin', 'Oct', 'Oct', 'Jalogüín', 'Jalogüín [Halloween]', 10),
]

equipo = [('equipo-milagros', 'milagroosjm'), ('equipo-javier', 'javier.agmc'), ('equipo-eduardo', 'eduu.ardoo'),
          ('equipo-liz', 'lizzearellano'), ('equipo-pablete', 'pablete_bartender_')]

resenas = [
    ('fr', 'Super soirée à Castro ! Le service est sympa, super ambiance, avec musique très sympa!', 'Great night out in Castro! Friendly service, great atmosphere, really nice music!', 'Dorothee · Épinal, Francia · Tripadvisor', 'Dorothee · Épinal, France · Tripadvisor'),
    ('en', 'Really cute place. Good menu including lots of vegetarian options', None, 'Rachael · Takaka, Nueva Zelanda · Tripadvisor', 'Rachael · Takaka, New Zealand · Tripadvisor'),
    ('es', 'De los mejores bares que he visitado. Tienen una terraza maravillosa.', "One of the best bars I've been to. They have a wonderful terrace.", 'Oscar · Santiago, Chile · Tripadvisor', 'Oscar · Santiago, Chile · Tripadvisor'),
    ('fr', 'cela nous a fait bien plaisir de tomber sur un vrai bar', 'we were so happy to stumble on a real bar', 'Emilie · París, Francia · Tripadvisor', 'Emilie · Paris, France · Tripadvisor'),
    ('en', 'Cool waiters, great food and comfy seats', None, 'Benjamín · Puerto Varas, Chile · Tripadvisor', 'Benjamín · Puerto Varas, Chile · Tripadvisor'),
    ('es', 'La atención es muy cálida y cercana.', 'The service is so warm and friendly.', 'Dana · Castro, Chile · Tripadvisor', 'Dana · Castro, Chile · Tripadvisor'),
]

# v4 fase 8 · Equipo: el dorso de cada tarjeta. Lugar y frase literales de su IG (si no hay frase, solo el @)
EQ_DORSO = {
    'equipo-javier': ('javier.agmc', 'Barra', 'Bar', 'mente creadora de muchos cócteles', 'the mastermind behind lots of our cocktails', 'IG-045'),
    'equipo-milagros': ('milagroosjm', 'Barra', 'Bar', 'la regia', 'our queen', 'IG-067'),
    'equipo-pablete': ('pablete_bartender_', 'Barra', 'Bar', 'haciéndole los copetitos a usté', 'making your drinks, yes, yours', 'IG-034'),
    'equipo-liz': ('lizzearellano', 'Salones', 'Floor', 'la amada', 'our beloved', 'IG-067'),
    'equipo-eduardo': ('eduu.ardoo', 'Salones', 'Floor', 'el ondero', 'the cool one', 'IG-067'),
}
# v4 fase 8 · Reseñas en dos cintas: solo las que dicen su país (10 de content/reviews.json); las 6 aprobadas en v3 con su extracto y glosa, las otras 4 textuales
FLAG = {
    'FR': '<svg class="flag" viewBox="0 0 24 16" width="24" height="16" role="img" aria-label="Francia" data-aria-en="France"><rect width="8" height="16" fill="#1f3c99"/><rect x="8" width="8" height="16" fill="#fff"/><rect x="16" width="8" height="16" fill="#e1262d"/></svg>',
    'CL': '<svg class="flag" viewBox="0 0 24 16" width="24" height="16" role="img" aria-label="Chile" data-aria-en="Chile"><rect width="24" height="16" fill="#fff"/><rect y="8" width="24" height="8" fill="#d52b1e"/><rect width="8" height="8" fill="#0039a6"/><path d="M4 1.6l.94 2.9h3.05L5.52 6.3l.94 2.9L4 7.4 1.54 9.2l.94-2.9L.01 4.5h3.05z" transform="translate(0 -.4) scale(1 .92)" fill="#fff"/></svg>',
    'NZ': '<svg class="flag" viewBox="0 0 24 16" width="24" height="16" role="img" aria-label="Nueva Zelanda" data-aria-en="New Zealand"><rect width="24" height="16" fill="#012169"/><path d="M0 0l12 8M12 0L0 8" stroke="#fff" stroke-width="1.6"/><path d="M0 0l12 8M12 0L0 8" stroke="#c8102e" stroke-width=".6"/><path d="M6 0v8M0 4h12" stroke="#fff" stroke-width="2.4"/><path d="M6 0v8M0 4h12" stroke="#c8102e" stroke-width="1.2"/><g fill="#c8102e" stroke="#fff" stroke-width=".4"><circle cx="18" cy="3.5" r=".9"/><circle cx="20.5" cy="7" r=".9"/><circle cx="16" cy="7.5" r=".9"/><circle cx="18" cy="12.5" r="1"/></g></svg>',
}
CINTAS = [
    [('FR', 'fr', 'Super soirée à Castro ! Le service est sympa, super ambiance, avec musique très sympa!', 'Great night out in Castro! Friendly service, great atmosphere, really nice music!', 'Dorothee · Épinal, Francia · Tripadvisor', 'Dorothee · Épinal, France · Tripadvisor'),
     ('CL', 'es', 'De los mejores bares que he visitado. Tienen una terraza maravillosa.', "One of the best bars I've been to. They have a wonderful terrace.", 'Oscar · Santiago, Chile · Tripadvisor', 'Oscar · Santiago, Chile · Tripadvisor'),
     ('NZ', 'en', 'Really cute place. Good menu including lots of vegetarian options', None, 'Rachael · Takaka, Nueva Zelanda · Tripadvisor', 'Rachael · Takaka, New Zealand · Tripadvisor'),
     ('CL', 'es', 'Haber... corta, Chiloé: palafitos, curanto y Almud. Bar original y cálido. Tomé bajo consejo del barman, sabia decisión.', None, 'Pablof · Santiago, Chile · Tripadvisor', 'Pablof · Santiago, Chile · Tripadvisor'),
     ('FR', 'fr', 'Des super cocktails bien fait, la nourriture est super aussi (je conseille le sandwich au poulet Pesto) le bar est décoré de façon originale et avec goût.', None, 'Pierre · Marsella, Francia · Tripadvisor', 'Pierre · Marseille, France · Tripadvisor')],
    [('FR', 'fr', 'cela nous a fait bien plaisir de tomber sur un vrai bar', 'we were so happy to stumble on a real bar', 'Emilie · París, Francia · Tripadvisor', 'Emilie · Paris, France · Tripadvisor'),
     ('CL', 'en', 'Cool waiters, great food and comfy seats', None, 'Benjamín · Puerto Varas, Chile · Tripadvisor', 'Benjamín · Puerto Varas, Chile · Tripadvisor'),
     ('CL', 'es', 'La atención es muy cálida y cercana.', 'The service is so warm and friendly.', 'Dana · Castro, Chile · Tripadvisor', 'Dana · Castro, Chile · Tripadvisor'),
     ('CL', 'es', 'La raja el bar, totalmente recomendable. Ondero, buena música, tragos buenísimos y una barra tipo NYC!', None, 'Andres · Santiago, Chile · Tripadvisor', 'Andres · Santiago, Chile · Tripadvisor'),
     ('CL', 'es', 'Estuve ahí cada día de mi estancia, porque es imposible no volver.', None, 'arqggodoy · Iquique, Chile · Tripadvisor', 'arqggodoy · Iquique, Chile · Tripadvisor')],
]


def flip(id_, sizes='(min-width:1024px) 22vw, 46vw'):
    h, rol, rol_en, fr, fr_en, _ = EQ_DORSO[id_]
    return (f'<div class="flip"><div class="flip__in"><div class="flip__front">' + pic(id_, 'a', sizes, 'reveal') + '</div>'
            f'<div class="flip__back"><p class="flip__rol" data-en="{rol_en}">{rol}</p><p class="flip__q">«{E(fr)}»{g(fr_en, "gloss gloss--s")}</p>'
            f'<a class="eq__at" href="{IG}{h}/" target="_blank" rel="noopener">@{h}</a></div></div></div>')


def flip_duo():
    return ('<div class="flip"><div class="flip__in"><div class="flip__front">' + pic('equipo-duo', 'a', '(min-width:1024px) 22vw, 46vw', 'reveal') + '</div>'
            f'<div class="flip__back"><p class="flip__q">«chicas super poderosas»{g("our powerpuff girls", "gloss gloss--s")}</p>'
            f'<a class="eq__at" href="{IG}milagroosjm/" target="_blank" rel="noopener">@milagroosjm</a><a class="eq__at" href="{IG}lizzearellano/" target="_blank" rel="noopener">@lizzearellano</a></div></div></div>')


def resena(r, dup=False):
    fl, l, q, gl, f, fen = r
    return (f'<li class="r"' + (' aria-hidden="true"' if dup else '') + f'><blockquote class="r__q" lang="{l}"><p>{E(q)}</p>' + (g(gl, 'gloss gloss--s') if gl else '') +
            f'</blockquote><p class="r__f">{FLAG[fl]}<span data-en="{E(fen)}">{E(f)}</span></p></li>')


creditos = ['catarsis.fotografia', 'estudiouno.prod', 'isosur.prod', 'rober.patagonico']

ISO = svg_inline('almud-isotipo', 'iso').replace('<path ', '<path pathLength="1" ')
ISO = ISO.replace('<g ', '<g class="iso__g" ', 1)


def _sub_bbox(sp):
    """Rango x de un subtrazado con comandos absolutos M/L/H/V/Q/Z."""
    toks = re.findall(r'[A-Za-z]|-?\d+(?:\.\d+)?(?:e-?\d+)?', sp)
    vals, cmd = [], None
    for t_ in toks:
        if t_.isalpha():
            cmd = t_
        else:
            vals.append((cmd, float(t_)))
    xs, k = [], 0
    while k < len(vals):
        c_, v_ = vals[k]
        if c_ == 'V':
            k += 1
        elif c_ == 'H':
            xs.append(v_); k += 1
        else:
            xs.append(v_); k += 2
    return min(xs), max(xs)


def letras(svg):
    """v4 fase 4: ALMUD y BAR pasan de 1 trazado a 1 trazado por letra (A L M U D · B A R), para que entren letra por letra."""
    def rep(m):
        attrs, d = m.group(1), m.group(2)
        grupos = []
        for sp in re.findall(r'M[^M]*', d):
            x0, x1 = _sub_bbox(sp)
            if grupos and x0 < grupos[-1][1]:
                grupos[-1][0].append(sp); grupos[-1][1] = max(grupos[-1][1], x1)
            else:
                grupos.append([[sp], x1])
        return ''.join(f'<path class="ltr"{attrs} d="{"".join(g_[0])}"/>' for g_ in grupos)
    return re.sub(r'<path( style="fill:var\(--letrero-(?:blanco|azul)\)") d="([^"]+)"/>', rep, svg)

body = f'''
<a class="skip" href="#lugar" data-en="Skip to content">Saltar al contenido</a>
<header class="nav" data-nav>
  <a class="nav__logo" href="#top" aria-label="Almud Bar">{svg_inline('almud-nav-claro', 'nav__svg')}</a>
  <nav class="nav__r" aria-label="Principal" data-aria-en="Main">
    <button class="nav__a nav__lang" type="button" data-lang aria-label="English" data-aria-en="Español"><span data-en="ES">EN</span></button>
    <a class="btn btn--rosa nav__carta" href="{CARTA}" data-en="Menu">Carta</a>
  </nav>
</header>

<main id="top">
<!-- 1 · PORTADA -->
<section class="hero" aria-label="Almud Bar">
  <div class="hero__win" data-win>
    {vid('portada-celular', 'hero__v hero__v--m', hero=True)}
    {vid('portada-escritorio', 'hero__v hero__v--d', hero=True)}
    <div class="hero__veil" aria-hidden="true"></div>
    <script>(function(d){{var L=matchMedia('(orientation: landscape) and (min-width:768px)').matches,v=d.querySelector(L?'.hero__v--d video':'.hero__v--m video');v.dataset.on='1';v.poster=v.dataset.poster;if(matchMedia('(prefers-reduced-motion: reduce)').matches){{v.removeAttribute('autoplay');return}}function go(){{if(v.dataset.src)return;v.dataset.src='1';v.preload='auto';v.innerHTML='<source src="'+v.dataset.webm+'" type="video/webm"><source src="'+v.dataset.mp4+'" type="video/mp4">';v.load();var q=v.play();if(q&&q.catch)q.catch(function(){{}})}}if(d.documentElement.classList.contains('intro')||d.readyState==='complete')go();else{{addEventListener('load',go);setTimeout(go,2500)}}}})(document)</script>
  </div>
  <div class="hero__iso" aria-hidden="true">{ISO}</div>
  <div class="hero__in">
    <h1 class="hero__logo"><span class="sr-only">Almud Bar</span>{letras(svg_inline('almud-horizontal-claro', 'hero__svg'))}</h1>
    <p class="hero__claim"><span class="hero__claim-t">Coctelería de autor, comida &amp; música bonita desde 2014</span>{g('Signature cocktails, food & good music since 2014')}</p>
    <div class="hero__btns">
      <a class="btn btn--rosa" href="{CARTA}" data-en="See the menu">Ver la carta</a>
    </div>
  </div>
</section>

<!-- 2 · EL LUGAR -->
<section class="lugar claro" id="lugar" aria-labelledby="h-lugar">
  <div class="lugar__head wrap">
    <div class="lugar__txt">{title('Somos inquietos y nos gusta el colorssss!', "Restless souls who love colorssss!", 'h-lugar')}</div>
    {vid('lugar-noche', 'lugar__v reveal')}
  </div>
  <div class="lleno wrap">
    {pic('lugar-techada-llena', 'a', '(min-width:1024px) 30vw, (min-width:768px) 30vw, 92vw', 'lleno__m lleno__m--1 clipin', extra=' data-par="-0.03"')}
    {pic('lugar-salon-lleno', 'a', '(min-width:1024px) 30vw, (min-width:768px) 30vw, 46vw', 'lleno__m lleno__m--2 clipin', extra=' data-par="0.06"')}
    {pic('lugar-terraza-repleta', 'a', '(min-width:1024px) 30vw, (min-width:768px) 30vw, 46vw', 'lleno__m lleno__m--3 clipin', extra=' data-par="-0.05"')}
  </div>
  <div class="rincones" data-h>
    <div class="rincones__st" data-ruleta aria-label="Rincones de Almud" data-aria-en="Corners of Almud">
      <ul class="rincones__tr" data-track>
        {''.join(rincon_li(r, i) for i, r in enumerate(rincones))}
      </ul>
    </div>
  </div>
</section>

<!-- 3 · TRAGOS -->
<section class="tragos claro" id="tragos" aria-labelledby="h-tragos">
  <div class="wrap tragos__g">
    <div class="tragos__head">{title('mucho amor, color y trabajo', 'Lots of love, color and hard work', 'h-tragos')}</div>
    <div class="tragos__band" aria-hidden="false">
      {pic('tragos-bartender', 'a', '(min-width:1024px) 46vw, 100vw', 'tragos__flag reveal')}
      {pic('tragos-splash', 'a', '(min-width:1024px) 24vw, 47vw', 'tragos__amb tragos__amb--1 pour', extra=' data-par="-0.03"')}
      {pic('tragos-sours', 'a', '(min-width:1024px) 24vw, 47vw', 'tragos__amb tragos__amb--2 pour', extra=' data-par="0.04"')}
      {vid('tragos-coctelera', 'tragos__amb tragos__amb--3 reveal')}
      {pic('tragos-copa-tallada', 'a', '(min-width:1024px) 24vw, 47vw', 'tragos__amb tragos__amb--4 pour')}
      {pic('tragos-old-fashioned', 'a', '(min-width:1024px) 31vw, 47vw', 'tragos__amb tragos__amb--5 pour')}
      {pic('eventos-negroni-week', 'a', '(min-width:1024px) 31vw, 47vw', 'tragos__amb tragos__amb--6 pour', extra=' data-par="-0.03"')}
      {pic('tragos-brindis-copas', 'a', '(min-width:1024px) 31vw, 47vw', 'tragos__amb tragos__amb--7 pour', extra=' data-par="0.04"')}
    </div>
    <!-- v4 fase 5: los destacados con nombre son un carrusel que se arrastra (dedo o mouse), con la lógica de la ruleta de rincones -->
    <div class="tragos__named carr" data-ruleta aria-label="Tragos de la casa" data-aria-en="House cocktails">
      <ul class="carr__tr" data-track>
        <li class="carr__c"><a class="it it--hero" href="{C_CASA}">
          {vid('tragos-humo', 'it__m')}
          <span class="it__cap"><span class="it__n">Aquí te las traigo Peter</span>{g('[Pisco, elderflower, cranberry, smoke bubble]', 'gloss gloss--s')}<span class="it__p">$ 6.700</span></span>
        </a></li>
        <li class="carr__c">{item2('carta-saguer', 'Sagüer on Faia', '$ 7.900', '[Spiced pisco sour with a little heat]', C_CASA, cls='it--a', sizes='(min-width:1024px) 26vw, 72vw')}</li>
        <li class="carr__c">{item2('carta-sangria', 'Sangría Foreva!', '$ 6.500', '[Carménère, aged pisco, cinnamon, fruit]', C_CASA, cls='it--b', sizes='(min-width:1024px) 26vw, 72vw')}</li>
        <li class="carr__c">{item2('carta-olvidar', 'Cómo te voy a olvidar', '$ 6.800', _GL.get('Cómo te voy a olvidar', '[Pear vodka, lemon, syrup, red wine float]'), C_CASA, cls='it--a', sizes='(min-width:1024px) 26vw, 72vw')}</li>
        <li class="carr__c">{item2('carta-coquette', 'A veces me pongo Coquette', '$ 7.100', _GL.get('A veces me pongo Coquette', '[Berry pisco, whisky cream liqueur, raspberry, orange, cinnamon]'), C_CASA, cls='it--b', sizes='(min-width:1024px) 26vw, 72vw')}</li>
        <li class="carr__c"><div class="moc2">
          <a class="moc2__m" href="{C_MOC}" tabindex="-1" aria-hidden="true">{pic('carta-moto', 'a', '(min-width:1024px) 26vw, 72vw', '')}</a>
          <div class="moc2__t">
            <h3 class="kick" data-en="Mocktails">Mocktails</h3>
            <p class="moc__l">no dejamos a nadie ajuera{g('Nobody gets left out!')}</p>
            <a class="moc__n" href="{C_MOC}"><span class="it__n">La moto chantá</span>{g('[Mango, passion fruit, cucumber]', 'gloss gloss--s')}<span class="it__p">$ 6.400</span></a>
          </div>
        </div></li>
      </ul>
    </div>
    <p class="ver-carta"><a class="btn btn--rosa" href="{C_CASA}" data-en="See the full menu">Ver la carta completa</a></p>
  </div>
</section>

<!-- 4 · COMIDA -->
<section class="comida claro" id="comida" aria-labelledby="h-comida">
  <div class="wrap comida__g">
    <div class="comida__head">{title('una cocina sencilla pero más que sabrosona!', 'Simple food, but seriously tasty!', 'h-comida')}</div>
    <a class="it co__big" href="{C_PIZ}">
      {pic('comida-pizza', 'a', '(min-width:1024px) 46vw, (min-width:768px) 64vw, 100vw', 'it__m plato')}
      <span class="it__n">Pizzas artesanales</span>{g('[Handmade pizzas]', 'gloss gloss--s')}
    </a>
    <a class="it co__a" href="{C_PIC}">
      {pic('carta-tukulito', 'a', '(min-width:1024px) 22vw, 45vw', 'it__m plato')}
      <span class="it__n">Tukulito Sakayama</span>{g('[Marinated tuna tataki]', 'gloss gloss--s')}<span class="it__p">$ 15.900</span>
    </a>
    <a class="it co__b" href="{C_PIC}">
      {vid('comida-carne', 'it__m plato')}
      <span class="it__n">La carne es débil</span>{g(GL_CARNE, 'gloss gloss--s')}<span class="it__p">$ 11.900</span>
    </a>
    <a class="it co__c" href="{C_PIC}">
      {vid('comida-queso', 'it__m plato')}
      <span class="it__n">Una cosa poca</span>{g(GL_QUESO, 'gloss gloss--s')}<span class="it__p">$ 11.900</span>
    </a>
    <!-- v4 fase 7 (6b): «el orden del desorden»: dos columnas independientes; la derecha parte más abajo y no se realinea -->
    <div class="co__more">
      <div class="co__col co__col--1">
        {item2('comida-ceviche', 'Todo que ver!', '$ 16.000', _GL.get('Todo que ver!'), C_PIC, cls='co__m1', sizes='(min-width:1024px) 23vw, 46vw', rv='plato')}
        {item2('carta-contuti', 'Con tuti si no pa qué!', '$ 19.900', _GL.get('Con tuti si no pa qué!'), C_PIC, cls='co__m3', sizes='(min-width:1024px) 23vw, 46vw', rv='plato')}
      </div>
      <div class="co__col co__col--2">
        {item2('comida-hamburguesa', 'Chambreao', '$ 10.900', _GL.get('Chambreao'), C_SAN, cls='co__m2', sizes='(min-width:1024px) 23vw, 46vw', rv='plato')}
        {item2('carta-camaron', 'Camarón que se duerme', '$ 15.900', _GL.get('Camarón que se duerme'), C_GRE, cls='co__m4', sizes='(min-width:1024px) 23vw, 46vw', rv='plato')}
      </div>
    </div>
    <p class="ver-carta"><a class="btn btn--rosa" href="{CARTA}#comilona" data-en="See the full menu">Ver la carta completa</a></p>
  </div>
</section>

<!-- 5 · CON QUIÉN · v4 fase 6: las fotos son una baraja que se lanza; los 3 videos de multitud quedan fijos fuera de ella -->
<section class="quien" id="quien" aria-labelledby="h-quien">
  <div class="wrap">{title('no somos ná sin ustedes!', "We're nothing without you!", 'h-quien', 'ttl--xl')}</div>
  <div class="qz wrap">
    {vid('quien-multitud-1', 'qz__v qz__v--1 reveal')}
    <div class="baraja" data-baraja aria-label="Fotos de la gente de Almud" data-aria-en="Photos of the Almud crowd">
      <ul class="baraja__p">
        {''.join('<li class="carta">' + pic(i, 'a', QB, 'carta__m') + '</li>' for i in BARAJA)}
      </ul>
      <p class="baraja__hint" aria-hidden="true"><svg class="baraja__mano" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M9 11V5.5a1.5 1.5 0 0 1 3 0V10m0-1.5a1.5 1.5 0 0 1 3 0V11m0-1a1.5 1.5 0 0 1 3 0v4.5a6 6 0 0 1-6 6h-1a6 6 0 0 1-4.8-2.4L3.6 14.8a1.6 1.6 0 0 1 2.5-2L9 15"/></svg><span data-en="Swipe">Desliza</span></p>
      <p class="sr-only baraja__live" aria-live="polite"></p>
    </div>
    <div class="qz__lado">
      {vid('quien-multitud-2', 'qz__v qz__v--2 reveal')}
      {vid('quien-multitud-3', 'qz__v qz__v--3 reveal')}
    </div>
  </div>
</section>

<!-- 6 · EVENTOS · v4 fase 7: el video grande de la fiesta, un slider de fiestas a pantalla completa y una coda de fotos -->
<section class="eventos claro" id="eventos" aria-labelledby="h-eventos">
  <div class="wrap ev7">
    <div class="ev7__head">{title('tirar la casa por la ventana!', 'Going all out!', 'h-eventos')}</div>
    {vid('eventos-fiesta', 'ev__banner ev__banner--v ev7__v reveal')}
    <div class="ev7__coda">
      <div class="ev7__col">{pic('eventos-terraza-12', 'a', '(min-width:1024px) 18vw, 46vw', 'reveal')}</div>
      <div class="ev7__col ev7__col--2">{pic('eventos-primavera', 'a', '(min-width:1024px) 18vw, 46vw', 'reveal')}</div>
    </div>
    <div class="fs" data-fiestas aria-label="Fiestas de Almud" data-aria-en="Almud parties">
      <ol class="fs__tr" data-track>
        {''.join(fiesta_li(f, k) for k, f in enumerate(FIESTAS))}
      </ol>
      <div class="fs__dots" hidden>{''.join(f'<button class="fs__dot" type="button" aria-label="{E(f[0])}"><span class="fs__bar"></span></button>' for f in FIESTAS)}</div>
    </div>
  </div>
</section>

<!-- 7 · EQUIPO · v4 fase 8: tarjetas que se dan vuelta (lugar, frase literal y @); el video de los dueños, fijo. Columnas con desfase -->
<section class="equipo" id="equipo" aria-labelledby="h-equipo">
  <div class="wrap">{title('Peazo de equipo que tenemos!', 'One heck of a team!', 'h-equipo')}</div>
  <div class="eqz wrap">
    <div class="eqz__m eqz__m--1">
      <div class="eqz__d eqz__d--1">{vid('equipo-duenos', 'eqz__v reveal')}</div>
      <div class="eqz__d eqz__d--2">{flip('equipo-javier')}{flip('equipo-milagros')}</div>
    </div>
    <div class="eqz__m eqz__m--2">
      <div class="eqz__d eqz__d--3">{flip('equipo-pablete')}{flip('equipo-liz')}</div>
      <div class="eqz__d eqz__d--4">{flip('equipo-eduardo')}{flip_duo()}</div>
    </div>
  </div>
  <p class="wrap own"><span class="own__k" data-en="The owners">Los dueños</span> <a href="{IG}cepaz/" target="_blank" rel="noopener">@cepaz</a> · <a href="{IG}rusio_mezclao/" target="_blank" rel="noopener">@rusio_mezclao</a></p>
</section>

<!-- 8 · RESEÑAS -->
<section class="resenas claro" id="resenas" aria-labelledby="h-resenas">
  <div class="wrap">
    <h2 class="ttl" id="h-resenas"><span class="ttl__t">Que no se lo cuenten</span></h2>
    <p class="ttl-gloss">{g("See for yourself")}</p>
  </div>
  <!-- v4 fase 8: dos cintas que pasan solas en sentidos contrarios y se arrastran; cada reseña en su idioma, con la bandera de su país -->
  <div class="cinta" data-cinta aria-label="Reseñas" data-aria-en="Reviews">
    {''.join(f'<ul class="cinta__row" data-dir="{d}">' + ''.join(resena(r) for r in fila) + '</ul>' for fila, d in zip(CINTAS, (-1, 1)))}
  </div>
</section>

<!-- 9 · CUÁNDO Y DÓNDE -->
<section class="donde" id="donde" aria-labelledby="h-donde">
  {vid('donde-terraza', 'donde__v reveal')}
  <div class="donde__t">
    {title('Le esperamos desde las 18:00 hrs', "Doors open at 6 pm — see you there!", 'h-donde')}
    <div class="donde__d">
    <dl class="datos">
      <div><dt class="sr-only" data-en="Open">Días</dt><dd class="datos__big" data-en="Tue–Sat">Mar a Sáb</dd></div>
      <div><dt class="sr-only" data-en="Address">Dirección</dt><dd class="datos__big">Serrano 325, Castro</dd><dd class="datos__s" data-en="Across from the Castro Cultural Center">Al frente del Centro Cultural de Castro</dd></div>
    </dl>
    {pic('donde-puerta', 'a', '(min-width:1024px) 14vw, 40vw', 'donde__p reveal')}
    </div>
    <div class="donde__btns">
      <a class="btn btn--rosa" href="{DM}" target="_blank" rel="noopener" data-en="Message us on Instagram">Escríbenos por DM</a>
      <a class="btn btn--ghost" href="{MAPS}" target="_blank" rel="noopener" data-en="Get directions">Cómo llegar</a>
    </div>
  </div>
</section>
</main>

<!-- 10 · PIE -->
<footer class="pie">
  <div class="wrap pie__g">
    <div class="pie__hero">
      <p class="pie__f"><span class="ttl__t">USTÉ SE LO MERECE!</span>{g("You've earned it, friend!")}</p>
    </div>
    <div class="pie__logo">{svg_inline('almud-vertical-claro', 'pie__svg', label=True)}</div>
    <div class="pie__cr">
      <h2 class="kick" data-en="Photos &amp; video">Imágenes</h2>
      <ul>{''.join(f'<li><a href="{IG}{c}/" target="_blank" rel="noopener">@{c}</a></li>' for c in creditos)}</ul>
    </div>
  </div>
</footer>
'''

IM_P = VI['portada-celular']['poster']['webp']['path']
IM_L = VI['portada-escritorio']['poster']['webp']['path']
page = f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Almud Bar · Castro, Chiloé</title>
<meta name="description" content="Coctelería de autor, comida &amp; música bonita desde 2014. Serrano 325, Castro." data-en="Signature cocktails, food &amp; good music since 2014. Serrano 325, Castro, Chiloé.">
<meta name="theme-color" content="#160d0b">
<meta name="robots" content="noindex">
<link rel="icon" href="{UP}brand/v3/favicon.svg" type="image/svg+xml">
<link rel="preload" href="{UP}assets/fonts/big-shoulders-display-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{UP}assets/fonts/barlow-condensed-latin-500-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{UP}assets/fonts/barlow-condensed-latin-600-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{UP}{IM_P}" as="image" type="image/webp" media="(orientation: portrait), (max-width: 767px)" fetchpriority="high">
<link rel="preload" href="{UP}{IM_L}" as="image" type="image/webp" media="(orientation: landscape) and (min-width: 768px)" fetchpriority="high">
<link rel="preload" href="{UP}vendor/gsap.min.js?v={ver('vendor/gsap.min.js')}" as="script">
<link rel="preload" href="{UP}vendor/ScrollTrigger.min.js?v={ver('vendor/ScrollTrigger.min.js')}" as="script">
<link rel="preload" href="{UP}js/nv8/site.js?v={ver('js/nv8/site.js')}" as="script">
<link rel="stylesheet" href="{UP}css/nv8/tokens.css?v={ver('css/nv8/tokens.css')}">
<link rel="stylesheet" href="{UP}css/nv8/site.css?v={ver('css/nv8/site.css')}">
<link rel="canonical" href="{SITE}{PATH}">
{OG}
<script>(function(d){{var r=d.documentElement;r.classList.add('js');try{{if(localStorage.getItem('almud-idioma')==='en')r.lang='en'}}catch(e){{}}if(matchMedia('(prefers-reduced-motion: reduce)').matches)r.classList.add('rm');else{{r.classList.add('intro');setTimeout(function(){{if(!window.__almudIntro)r.classList.remove('intro')}},1400)}}}})(document)</script>
</head>
<body>
{body}
<script src="{UP}vendor/gsap.min.js?v={ver('vendor/gsap.min.js')}" defer></script>
<script src="{UP}vendor/ScrollTrigger.min.js?v={ver('vendor/ScrollTrigger.min.js')}" defer></script>
<script src="{UP}vendor/lenis.min.js?v={ver('vendor/lenis.min.js')}" defer></script>
<script src="{UP}js/nv8/site.js?v={ver('js/nv8/site.js')}" defer></script>
</body>
</html>
'''
out = ROOT / 'nueva_v8/index.html'
out.parent.mkdir(exist_ok=True)
out.write_text(page)
print('ok', out, len(page))
