#!/usr/bin/env python3
"""Boceto funcional v3 (fase 8): genera v3/index.html desde assets/v3/media.json.
Texto: solo content/copy-v3.md. Rutas relativas desde /v3/.
Uso: python3 tools/boceto_v3.py
"""
import json, html, pathlib, re, hashlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
M = json.loads((ROOT / 'assets/v3/media.json').read_text())
IM, VI = M['images'], M['videos']
UP = '../'
E = html.escape


def srcset(files, kind):
    return ', '.join(f"{UP}{v['path']} {w}w" for w, v in sorted(files[kind].items(), key=lambda kv: int(kv[0])))


def pic(id_, crop='a', sizes='100vw', cls='', eager=False, alt=True, speed=None, extra=''):
    im = IM[id_]
    c = im['crops'][crop]
    w, h = c['width'], c['height']
    files = c['files']
    widths = sorted(int(x) for x in files['webp'])
    fb = next((x for x in widths if x >= 720), widths[-1])
    a_es = E(im['alt']['es']) if alt else ''
    a_en = E(im['alt']['en']) if alt else ''
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    sp = f' data-speed="{speed}"' if speed is not None else ''
    return (f'<figure class="m {cls}" style="--ar:{w}/{h};--c:{c["color"]};--lq:url({c["lqip"]})"{sp}{extra}>'
            f'<picture><source type="image/avif" srcset="{srcset(files, "avif")}" sizes="{sizes}">'
            f'<source type="image/webp" srcset="{srcset(files, "webp")}" sizes="{sizes}">'
            f'<img src="{UP}{files["webp"][str(fb)]["path"]}" width="{w}" height="{h}" alt="{a_es}"'
            + (f' data-alt-en="{a_en}"' if alt else '') +
            f' {load} decoding="async"></picture></figure>')


def vid(id_, cls='', hero=False, extra=''):
    v = VI[id_]
    w, h = v['width'], v['height']
    poster = UP + v['poster']['webp']['path']
    return (f'<figure class="m m--v {cls}" style="--ar:{w}/{h};--c:{v["color"]};--lq:url({v["lqip"]})"{extra}>'
            f'<video class="v" autoplay muted loop playsinline preload="none" width="{w}" height="{h}" data-poster="{poster}"'
            f' data-webm="{UP}{v["files"]["webm"]["path"]}" data-mp4="{UP}{v["files"]["mp4"]["path"]}"'
            + (' data-hero' if hero else '') +
            f' aria-label="{E(v["alt"]["es"])}" data-aria-en="{E(v["alt"]["en"])}"></video></figure>')


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
<meta property="og:url" content="{SITE}/v3/">
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
CARTA = 'carta/'

# ───────────────────────── secciones ─────────────────────────
rincones = [
    ('lugar-barra', 'a', 'Barra', 'The bar', 'Pucha que nos gusta nuestra barrita!', 'We really love our bar!'),
    ('lugar-terraza-techada', 'a', 'Terraza techada', 'Covered terrace', 'Techamos parte de la terraza', 'We roofed part of the terrace'),
    ('lugar-salon', 'm', None, None, None, None),
    ('lugar-sillones', 'a', 'Sillones', 'Lounge', None, None),
    ('lugar-terraza-abierta', 'a', 'Terraza', 'Terrace', 'Amamos los atardeceres desde nuestra terracita', 'We love the sunsets from our little terrace'),
    ('lugar-lampara-pinzas', 'a', 'Lámparas', 'The lamps', 'Nos gustan los brillitos, las luces', 'We love the sparkle, the lights'),
    ('lugar-ojo-piojo', 'm', 'Ojo Piojo', 'Ojo Piojo [Mural of eyes]', 'una mirada vale más que mil palabras', 'A look is worth a thousand words'),
]


def rincon_li(r, i):
    id_, crop, lab, lab_en, line, line_en = r
    cap = ''
    if lab:
        name = (f'<h3 class="rin__n">{E(lab)} {g("[" + lab_en.split(" [")[1], "gloss gloss--i")}</h3>'
                if '[' in lab_en else f'<h3 class="rin__n" data-en="{E(lab_en)}">{E(lab)}</h3>')
        cap = f'<figcaption class="rin__c">{name}' + (f'<p class="rin__l">{E(line)}{g(line_en)}</p>' if line else '') + '</figcaption>'
    return (f'<li class="rin" style="--i:{i}">' + pic(id_, crop, '(min-width:1024px) 60vh, (min-width:768px) 44vw, 76vw', 'rin__m') + cap + '</li>')


C_CASA = CARTA + '#casa'
C_MOC = CARTA + '#mocktails-sin-alcohol-mocktails-de-la-casa'
C_PIC = CARTA + '#comilona-picoteos'
C_GRE = CARTA + '#comilona-greditas'
C_PIZ = CARTA + '#comilona-pizzas-artesanales'


def item(id_, name, price, gl, cls='', sizes='(min-width:1024px) 22vw, 45vw', speed=None):
    return (f'<a class="it {cls}" href="{CARTA}"' + (f' data-speed="{speed}"' if speed is not None else '') + '>'
            + pic(id_, 'a', sizes, 'it__m reveal') +
            f'<span class="it__n">{E(name)}</span>{g(gl, "gloss gloss--s")}<span class="it__p">{E(price)}</span></a>')


eventos = [
    ('eventos-10-anos', 'Jul', 'Jul', 'Aniversario', 'Aniversario [Anniversary]', 7),
    ('eventos-fondita', 'Sep', 'Sep', 'Fondita', 'Fondita [Fiestas Patrias party]', 9),
    ('eventos-jaloguin', 'Oct', 'Oct', 'Jalogüín', 'Jalogüín [Halloween]', 10),
]

equipo = [('equipo-milagros', 'milagroosjm'), ('equipo-javier', 'javier.agmc'), ('equipo-eduardo', 'eduu.ardoo'),
          ('equipo-liz', 'lizzearellano'), ('equipo-pablete', 'pablete_bartender_')]

resenas = [
    ('fr', 'Super soirée à Castro ! Le service est sympa, super ambiance, avec musique très sympa!', 'Great night out in Castro! Friendly service, great atmosphere, really nice music!', 'Dorothee · Épinal, Francia · Tripadvisor', 'Dorothee · Épinal, France · Tripadvisor'),
    ('en', 'Really cute place. Good menu including lots of vegetarian options', None, 'Rachael · Takaka, Nueva Zelanda · Tripadvisor', 'Rachael · Takaka, New Zealand · Tripadvisor'),
    ('es', 'De los mejores bares que he visitado. Tienen una terraza maravillosa.', "One of the best bars I've been to. They have a wonderful terrace.", 'Oscar · Santiago, Chile · Tripadvisor', 'Oscar · Santiago, Chile · Tripadvisor'),
    ('fr', 'cela nous a fait bien plaisir de tomber sur un vrai bar', 'it made us very happy to come across a real bar', 'Emilie · París, Francia · Tripadvisor', 'Emilie · Paris, France · Tripadvisor'),
    ('en', 'Cool waiters, great food and comfy seats', None, 'Benjamín · Puerto Varas, Chile · Tripadvisor', 'Benjamín · Puerto Varas, Chile · Tripadvisor'),
    ('es', 'La atención es muy cálida y cercana.', 'The service is very warm and personal.', 'Dana · Castro, Chile · Tripadvisor', 'Dana · Castro, Chile · Tripadvisor'),
]

creditos = ['catarsis.fotografia', 'estudiouno.prod', 'isosur.prod', 'rober.patagonico']

ISO = svg_inline('almud-isotipo', 'iso').replace('<path ', '<path pathLength="1" ')

body = f'''
<a class="skip" href="#lugar" data-en="Skip to content">Saltar al contenido</a>
<header class="nav" data-nav>
  <a class="nav__logo" href="#top" aria-label="Almud Bar">{svg_inline('almud-nav-claro', 'nav__svg')}</a>
  <nav class="nav__r" aria-label="Principal" data-aria-en="Main">
    <a class="nav__a" href="{CARTA}" data-en="Menu">Carta</a>
    <button class="nav__a nav__lang" type="button" data-lang aria-label="English" data-aria-en="Español"><span data-en="ES">EN</span></button>
  </nav>
</header>

<main id="top">
<!-- 1 · PORTADA -->
<section class="hero" aria-label="Almud Bar">
  <div class="hero__win" data-win>
    {vid('portada-celular', 'hero__v hero__v--m', hero=True)}
    {vid('portada-escritorio', 'hero__v hero__v--d', hero=True)}
    <div class="hero__veil" aria-hidden="true"></div>
    <script>(function(d){{var L=matchMedia('(orientation: landscape) and (min-width:768px)').matches,v=d.querySelector(L?'.hero__v--d video':'.hero__v--m video');v.dataset.on='1';v.poster=v.dataset.poster;if(matchMedia('(prefers-reduced-motion: reduce)').matches){{v.removeAttribute('autoplay');return}}v.preload='auto';v.innerHTML='<source src="'+v.dataset.webm+'" type="video/webm"><source src="'+v.dataset.mp4+'" type="video/mp4">';v.load();var q=v.play();if(q&&q.catch)q.catch(function(){{}})}})(document)</script>
  </div>
  <div class="hero__iso" aria-hidden="true">{ISO}</div>
  <div class="hero__in">
    <h1 class="hero__logo"><span class="sr-only">Almud Bar</span>{svg_inline('almud-horizontal-claro', 'hero__svg')}</h1>
    <p class="hero__claim"><span class="hero__claim-t">Coctelería de autor, comida &amp; música bonita desde 2014</span>{g('Signature cocktails, food & lovely music since 2014')}</p>
    <div class="hero__btns">
      <a class="btn btn--rosa" href="{CARTA}" data-en="See the menu">Ver la carta</a>
    </div>
  </div>
</section>

<!-- 2 · EL LUGAR -->
<section class="lugar" id="lugar" aria-labelledby="h-lugar">
  <div class="lugar__head wrap">
    <div class="lugar__txt">{title('Somos inquietos y nos gusta el colorssss!', "We're restless and we love colour!", 'h-lugar')}</div>
    {vid('lugar-cintas', 'lugar__v reveal', extra=' data-speed="-0.12"')}
  </div>
  <div class="rincones" data-h>
    <div class="rincones__st">
      <ul class="rincones__tr" data-track>
        {''.join(rincon_li(r, i) for i, r in enumerate(rincones))}
      </ul>
    </div>
  </div>
</section>

<!-- 3 · TRAGOS -->
<section class="tragos" id="tragos" aria-labelledby="h-tragos">
  <div class="wrap tragos__g">
    <div class="tragos__head">{title('mucho amor, color y trabajo', 'A lot of love, colour and hard work', 'h-tragos')}</div>
    {pic('tragos-bartender', 'a', '(min-width:1024px) 46vw, 100vw', 'tragos__flag reveal')}
    <a class="it it--hero" href="{C_CASA}">
      {vid('tragos-humo', 'it__m reveal')}
      <span class="it__cap"><span class="it__n">Aquí te las traigo Peter</span>{g('[Pisco, elderflower, cranberry, smoke bubble]', 'gloss gloss--s')}<span class="it__p">$ 6.700</span></span>
    </a>
    <div class="tragos__pair">
      {pic('tragos-splash', 'a', '(min-width:1024px) 24vw, 45vw', 'it--a reveal', speed='-0.08')}
      {pic('tragos-sours', 'a', '(min-width:1024px) 24vw, 45vw', 'it--b reveal', speed='0.1')}
    </div>
    <ul class="menu menu--tragos">
      <li><a href="{C_CASA}"><span class="menu__n">Sagüer on Faia</span><i></i><span class="it__p">$ 7.900</span></a>{g('[Spiced sour with a little heat]', 'gloss gloss--s')}</li>
      <li><a href="{C_CASA}"><span class="menu__n">Sangría Foreva!</span><i></i><span class="it__p">$ 6.500</span></a>{g('[Carménère wine, aged pisco, cinnamon]', 'gloss gloss--s')}</li>
    </ul>
    <div class="moc">
      <h3 class="kick" data-en="Alcohol-free">Mocktails</h3>
      <p class="moc__l">no dejamos a nadie ajuera{g('We leave nobody out')}</p>
      <a class="moc__n" href="{C_MOC}"><span class="it__n">La moto chantá</span>{g('[Mango, passion fruit, cucumber]', 'gloss gloss--s')}<span class="it__p">$ 6.400</span></a>
    </div>
  </div>
</section>

<!-- 4 · COMIDA -->
<section class="comida" id="comida" aria-labelledby="h-comida">
  <div class="wrap comida__g">
    <div class="comida__head">{title('una cocina sencilla pero más que sabrosona!', 'A simple kitchen, but more than tasty!', 'h-comida')}</div>
    {pic('comida-pizza', 'a', '(min-width:1024px) 46vw, (min-width:768px) 64vw, 100vw', 'comida__v reveal')}
    {pic('carta-tukulito', 'a', '(min-width:1024px) 22vw, 45vw', 'comida__a reveal', speed='-0.1')}
    {vid('comida-cazuela', 'comida__b reveal', extra=' data-speed="0.08"')}
    <ul class="menu">
      <li><a href="{C_PIC}"><span class="menu__n">Tukulito Sakayama</span><i></i><span class="it__p">$ 15.900</span></a>{g('[Marinated tuna tataki]', 'gloss gloss--s')}</li>
      <li><a href="{C_GRE}"><span class="menu__n">Camarón que se duerme</span><i></i><span class="it__p">$ 15.900</span></a>{g('[Shrimp baked in a clay pot]', 'gloss gloss--s')}</li>
      <li><a href="{C_PIZ}"><span class="menu__n">Huerta sabrosa</span><i></i><span class="it__p">$ 13.900</span></a>{g('[Pizza: cherry tomato, mushrooms, greens]', 'gloss gloss--s')}</li>
    </ul>
  </div>
</section>

<!-- 5 · CON QUIÉN -->
<section class="quien" id="quien" aria-labelledby="h-quien">
  <div class="wrap">{title('no somos ná sin ustedes!', "We're nothing without you!", 'h-quien', 'ttl--xl')}</div>
  <div class="quien__g">
    <div class="col" data-speed="-0.06">{pic('con-quien-barra', 'a', '(min-width:1024px) 31vw, 47vw', 'reveal')}{pic('con-quien-amigos', 'a', '(min-width:1024px) 31vw, 47vw', 'reveal')}</div>
    <div class="col col--2" data-speed="0.1">{pic('con-quien-brindis', 'a', '(min-width:1024px) 31vw, 47vw', 'reveal')}{pic('con-quien-risa', 'a', '(min-width:1024px) 31vw, 47vw', 'reveal')}</div>
    <div class="col col--3" data-speed="-0.16">{pic('con-quien-solo', 'a', '(min-width:1024px) 31vw, 47vw', 'reveal')}</div>
  </div>
</section>

<!-- 6 · EVENTOS -->
<section class="eventos" id="eventos" aria-labelledby="h-eventos">
  <div class="wrap">
    {title('tirar la casa por la ventana!', 'Going all out!', 'h-eventos')}
    {pic('eventos-12-anos', 'a', '(min-width:1024px) 40vw, 100vw', 'ev__banner reveal')}
    <ol class="cal">
      {''.join('<li class="ev">' + pic(i, 'a', '(min-width:1024px) 22vw, 45vw', 'ev__m reveal') + f'<p class="ev__t"><span class="ev__mes" data-en="{me}">{mes}</span></p><h3 class="ev__n">{E(n)}</h3>' + (g("[" + ne.split(" [")[1] if "[" in ne else ne, "gloss gloss--s") if ne != n else '') + '</li>' for i, mes, me, n, ne, m in eventos)}
    </ol>
  </div>
</section>

<!-- 7 · EQUIPO -->
<section class="equipo" id="equipo" aria-labelledby="h-equipo">
  <div class="wrap">{title('Peazo de equipo que tenemos!', "What a team we've got!", 'h-equipo')}</div>
  <ul class="eq" data-swipe>
    {''.join(f'<li class="eq__p" style="--i:{k}">' + pic(i, 'a', '(min-width:1024px) 15vw, 62vw', 'reveal') + f'<a class="eq__at" href="{IG}{h}/" target="_blank" rel="noopener">@{h}</a></li>' for k, (i, h) in enumerate(equipo))}
  </ul>
  <p class="wrap own"><span class="own__k" data-en="The owners">Los dueños</span> <a href="{IG}cepaz/" target="_blank" rel="noopener">@cepaz</a> · <a href="{IG}rusio_mezclao/" target="_blank" rel="noopener">@rusio_mezclao</a></p>
</section>

<!-- 8 · RESEÑAS -->
<section class="resenas" id="resenas" aria-labelledby="h-resenas">
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
  {vid('donde-letrero', 'donde__v reveal')}
  <div class="donde__t">
    {title('Le esperamos desde las 18:00 hrs', "See you from 6 pm", 'h-donde')}
    <dl class="datos">
      <div><dt class="sr-only" data-en="Days">Días</dt><dd class="datos__big" data-en="Tue–Sat">Mar a Sáb</dd></div>
      <div><dt class="sr-only" data-en="Address">Dirección</dt><dd class="datos__big">Serrano 325, Castro</dd><dd class="datos__s" data-en="Opposite the Castro Cultural Centre">Al frente del Centro Cultural de Castro</dd></div>
    </dl>
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
    <p class="pie__f"><span class="ttl__t">USTÉ SE LO MERECE!</span>{g('You deserve it!')}</p>
    <div class="pie__logo">{svg_inline('almud-vertical-claro', 'pie__svg', label=True)}</div>
    <div class="pie__cr">
      <h2 class="kick" data-en="Images">Imágenes</h2>
      <ul>{''.join(f'<li><a href="{IG}{c}/" target="_blank" rel="noopener">@{c}</a></li>' for c in creditos)}</ul>
    </div>
  </div>
</footer>
'''

page = f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Almud Bar · Castro, Chiloé</title>
<meta name="description" content="Coctelería de autor, comida &amp; música bonita desde 2014. Serrano 325, Castro." data-en="Signature cocktails, food &amp; lovely music since 2014. Serrano 325, Castro.">
<meta name="theme-color" content="#160d0b">
<meta name="robots" content="noindex">
<link rel="icon" href="../brand/v3/favicon.svg" type="image/svg+xml">
<link rel="preload" href="../assets/fonts/big-shoulders-display-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="../assets/fonts/barlow-condensed-latin-500-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="../assets/fonts/barlow-condensed-latin-600-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="../css/v3/tokens.css?v={ver('css/v3/tokens.css')}">
<link rel="stylesheet" href="../css/v3/site.css?v={ver('css/v3/site.css')}">
<link rel="canonical" href="{SITE}/v3/">
{OG}
<script>(function(d){{var r=d.documentElement;r.classList.add('js');try{{if(localStorage.getItem('almud-idioma')==='en')r.lang='en'}}catch(e){{}}if(matchMedia('(prefers-reduced-motion: reduce)').matches)r.classList.add('rm');else r.classList.add('intro')}})(document)</script>
</head>
<body>
{body}
<script src="../vendor/gsap.min.js" defer></script>
<script src="../vendor/ScrollTrigger.min.js" defer></script>
<script src="../vendor/lenis.min.js" defer></script>
<script src="../js/v3/site.js?v={ver('js/v3/site.js')}" defer></script>
</body>
</html>
'''
out = ROOT / 'v3/index.html'
out.parent.mkdir(exist_ok=True)
out.write_text(page)
print('ok', out, len(page))
