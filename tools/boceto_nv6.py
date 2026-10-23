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
PATH = '/nueva_v6/'
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

<!-- 6 · EVENTOS -->
<section class="eventos claro" id="eventos" aria-labelledby="h-eventos">
  <div class="wrap">
    {title('tirar la casa por la ventana!', 'Going all out!', 'h-eventos')}
    {vid('eventos-fiesta-12', 'ev__banner ev__banner--v reveal')}
    <div class="ev__mas">
      {pic('eventos-cotillon-12', 'a', '(min-width:1024px) 23vw, 46vw', 'reveal')}
      {pic('eventos-baile-12', 'a', '(min-width:1024px) 23vw, 46vw', 'reveal')}
      {pic('eventos-primavera', 'a', '(min-width:1024px) 23vw, 46vw', 'reveal')}
      {pic('eventos-terraza-12', 'a', '(min-width:1024px) 23vw, 46vw', 'reveal')}
    </div>
    <ol class="cal">
      {''.join('<li class="ev">' + (vid(i, 'ev__m reveal') if i in VI else pic(i, 'a', '(min-width:1024px) 22vw, 45vw', 'ev__m reveal')) + f'<p class="ev__t"><span class="ev__mes" data-en="{me}">{mes}</span></p><h3 class="ev__n">{E(n)}</h3>' + (g("[" + ne.split(" [")[1] if "[" in ne else ne, "gloss gloss--s") if ne != n else '') + '</li>' for i, mes, me, n, ne, m in eventos)}
    </ol>
  </div>
</section>

<!-- 7 · EQUIPO -->
<section class="equipo" id="equipo" aria-labelledby="h-equipo">
  <div class="wrap">{title('Peazo de equipo que tenemos!', 'One heck of a team!', 'h-equipo')}</div>
  <ul class="eq" data-swipe>
    <li class="eq__p eq__p--v" style="--i:0">{vid('equipo-duenos', 'reveal')}</li>
    {''.join(f'<li class="eq__p" style="--i:{k + 1}">' + pic(i, 'a', '(min-width:1024px) 15vw, 62vw', 'reveal') + f'<a class="eq__at" href="{IG}{h}/" target="_blank" rel="noopener">@{h}</a></li>' for k, (i, h) in enumerate(equipo))}
    <li class="eq__p eq__p--duo" style="--i:6">{pic('equipo-duo', 'a', '62vw', 'reveal', art=('d', '(min-width:1024px)', '46vw'))}</li>
  </ul>
  <p class="wrap own"><span class="own__k" data-en="The owners">Los dueños</span> <a href="{IG}cepaz/" target="_blank" rel="noopener">@cepaz</a> · <a href="{IG}rusio_mezclao/" target="_blank" rel="noopener">@rusio_mezclao</a></p>
</section>

<!-- 8 · RESEÑAS -->
<section class="resenas claro" id="resenas" aria-labelledby="h-resenas">
  <div class="wrap">
    <h2 class="ttl" id="h-resenas"><span class="ttl__t">Que no se lo cuenten</span></h2>
    <p class="ttl-gloss">{g("See for yourself")}</p>
  </div>
  <ul class="rs" data-swipe>
    {''.join(f'<li class="r"><blockquote class="r__q" lang="{l}"><p>{E(q)}</p>' + (g(gl, 'gloss gloss--s') if gl else '') + f'</blockquote><p class="r__f" data-en="{E(fen)}">{E(f)}</p></li>' for l, q, gl, f, fen in resenas)}
  </ul>
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
    <p class="pie__f"><span class="ttl__t">USTÉ SE LO MERECE!</span>{g("You've earned it, friend!")}</p>
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
<link rel="preload" href="{UP}js/nv6/site.js?v={ver('js/nv6/site.js')}" as="script">
<link rel="stylesheet" href="{UP}css/nv6/tokens.css?v={ver('css/nv6/tokens.css')}">
<link rel="stylesheet" href="{UP}css/nv6/site.css?v={ver('css/nv6/site.css')}">
<link rel="canonical" href="{SITE}{PATH}">
{OG}
<script>(function(d){{var r=d.documentElement;r.classList.add('js');try{{if(localStorage.getItem('almud-idioma')==='en')r.lang='en'}}catch(e){{}}if(matchMedia('(prefers-reduced-motion: reduce)').matches)r.classList.add('rm');else{{r.classList.add('intro');setTimeout(function(){{if(!window.__almudIntro)r.classList.remove('intro')}},1400)}}}})(document)</script>
</head>
<body>
{body}
<script src="{UP}vendor/gsap.min.js?v={ver('vendor/gsap.min.js')}" defer></script>
<script src="{UP}vendor/ScrollTrigger.min.js?v={ver('vendor/ScrollTrigger.min.js')}" defer></script>
<script src="{UP}vendor/lenis.min.js?v={ver('vendor/lenis.min.js')}" defer></script>
<script src="{UP}js/nv6/site.js?v={ver('js/nv6/site.js')}" defer></script>
</body>
</html>
'''
out = ROOT / 'nueva_v6/index.html'
out.parent.mkdir(exist_ok=True)
out.write_text(page)
print('ok', out, len(page))
