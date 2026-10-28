#!/usr/bin/env python3
"""Dossier de decisiones de diseño · Almud Bar (sitio final, almudbar.pages.dev).
Genera dossier/almud-dossier-diseno.html (autocontenido). PDF con dossier/render.js.
Uso: python3 dossier/build_dossier.py
"""
import base64, html, io, json, pathlib
from PIL import Image, ImageOps

ROOT = pathlib.Path(__file__).resolve().parent.parent
D = ROOT / 'dossier'
SH = D / 'shots'
E = html.escape

# ───────── medios del sitio (los mismos archivos que usa la página principal) ─────────
IM = dict(json.loads((ROOT / 'assets/v3/media.json').read_text())['images'])
IM.update(json.loads((ROOT / 'assets/nv2/media-img.json').read_text())['images'])
IM.update(json.loads((ROOT / 'assets/nv9/media-img.json').read_text())['images'])
VI = json.loads((ROOT / 'assets/v4/media-video.json').read_text())['videos']
POSTS = {p['id']: p for p in json.loads((ROOT / 'content/ig_posts.json').read_text())}
MES = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic']


def fecha(iso):
    y, m, d = iso.split('-')
    return f'{int(d)} {MES[int(m) - 1]} {y}'


def ig(pid):
    return 'Instagram · ' + fecha(POSTS[pid]['date'])


def b64img(img, w, q=80):
    img = img.convert('RGB')
    if img.width > w:
        img = img.resize((w, round(img.height * w / img.width)), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, 'JPEG', quality=q, optimize=True, progressive=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()


def shot(name, w=1500):
    p = SH / f'{name}.jpg'
    return b64img(Image.open(p), w) if p.exists() else ''


def _best(files):
    ws = sorted(int(x) for x in files['webp'])
    return ROOT / files['webp'][str(ws[-1])]['path']


def med(id_, w=480, crop='a'):
    """Imagen del sitio (foto o póster del video), tal como está publicada."""
    if id_ in VI:
        p = ROOT / VI[id_]['poster']['webp']['path']
    else:
        c = IM[id_]['crops']
        p = _best((c.get(crop) or next(iter(c.values())))['files'])
    return b64img(ImageOps.exif_transpose(Image.open(p)), w, 78)


def origen(id_):
    d = IM.get(id_) or VI.get(id_)
    return ig(d['credit']['post'])


def plan(name, w=700):
    return b64img(Image.open(ROOT / '_plan/v4' / f'{name}.jpg'), w, 80)


def png(rel, w=900):
    im = Image.open(ROOT / rel).convert('RGBA')
    if im.width > w:
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, 'PNG', optimize=True)
    return 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()


def font(name):
    return 'data:font/woff2;base64,' + base64.b64encode((ROOT / 'assets/fonts' / f'{name}.woff2').read_bytes()).decode()


# ───────── piezas ─────────
COL = {'amarillo': '#f5c518', 'rosa': '#f24350', 'naranja': '#f27a12', 'verde': '#0b6e4b', 'lila': '#a58ac9',
       'rojo': '#c2202a', 'crema': '#f5e9db', 'negro': '#0e0c0b', 'azul': '#2aa1f8'}
OSCUROS = {'verde', 'rojo', 'negro'}  # texto crema encima
RECORRIDO = ['La espera', 'Portada', 'El lugar', 'Tragos', 'Comida', 'Con quién', 'Eventos', 'Equipo', 'Reseñas', 'Usté se lo merece']
LOGO_C = png('brand/v3/png/almud-horizontal-claro.png', 900)
LOGO_O = png('brand/v3/png/almud-horizontal-oscuro.png', 900)


def quote(text, source, big=False):
    return f'<blockquote class="q{" big" if big else ""}"><p>{text}</p><cite>{E(source)}</cite></blockquote>'


def thumbs(items, cls=''):
    out = ''.join(f'<figure class="th"><img src="{med(i)}" alt=""><figcaption>{cap}<b>{E(origen(i))}</b></figcaption></figure>'
                  for i, cap in items)
    return f'<div class="ths {cls}">{out}</div>'


def block(title, body, cls=''):
    return f'<section class="bk {cls}"><h4>{title}</h4>{body}</section>'


def recorrido(cur):
    li = ''.join(f'<li class="{"on" if r == cur else ""}">{E(r)}</li>' for r in RECORRIDO)
    return f'<div class="recw"><p class="lab">Lugar en el recorrido</p><ol class="rec">{li}</ol></div>'


def PIE(n):
    return f'<footer class="pf"><span>ALMUD BAR · Decisiones de diseño del sitio</span><span>{n:02d}</span></footer>'


L, N = [], [0]


def nx():
    N[0] += 1
    return N[0]


def lamina(left, right, lc='negro', rc='crema'):
    n = nx()
    L.append(f'<article class="lam"><div class="L c-{lc}{" dk" if lc in OSCUROS else ""}">{left}</div>'
             f'<div class="R c-{rc}{" dk" if rc in OSCUROS else ""}">{right}{PIE(n)}</div></article>')


def fig(name, cap, cls='', w=1500):
    return f'<figure class="sh {cls}"><img src="{shot(name, w)}" alt=""><figcaption>{cap}</figcaption></figure>'


def figc(name, cap, frac, cls='', w=1500):
    """Captura recortada desde arriba (frac = fracción del alto que se conserva)."""
    p = SH / f'{name}.jpg'
    im = Image.open(p)
    im = im.crop((0, 0, im.width, round(im.height * frac)))
    return f'<figure class="sh {cls}"><img src="{b64img(im, w)}" alt=""><figcaption>{cap}</figcaption></figure>'


def seccion(nombre, kick, titulo, fuente, lead, left, bloques, lc):
    right = (f'<p class="kick">{kick}</p><h2>{titulo}</h2><p class="src">{E(fuente)}</p>'
             f'<p class="lead">{lead}</p><div class="grid">{"".join(bloques)}</div>')
    lamina(f'<p class="lab">El sitio</p>{left}{recorrido(nombre)}', right, lc)


def precios(rows):
    return '<table class="pt">' + ''.join(f'<tr><td class="n">{E(a)}</td><td>{E(b)}</td></tr>' for a, b in rows) + '</table>'


# ═════════════════════════ 01 · PORTADA ═════════════════════════
lamina(
    f'<img class="bleed" src="{med("tragos-bartender", 1400)}" alt="" style="object-position:50% 40%">',
    f'''<div class="cover">
  <img class="cv-logo" src="{LOGO_C}" alt="Almud Bar">
  <p class="cv-sub">Decisiones de diseño del sitio web</p>
  <h1>De su Instagram<br><span>a su sitio</span></h1>
  <p class="cv-for">Preparado para Carmen Paz y Sylvain</p>
  <p class="cv-meta">Serrano 325 · Castro, Chiloé · octubre 2026</p>
  <p class="cv-meta">almudbar.pages.dev</p>
</div>''', 'negro', 'negro')

# ═════════════════════════ 02 · CARTA ═════════════════════════
lamina(
    f'<img class="bleed" src="{med("lugar-techada-llena", 1400)}" alt="" style="object-position:50% 40%">',
    f'''<p class="kick">Antes de empezar</p><h2>Un sitio hecho con lo que ustedes ya dijeron</h2>
<div class="letter">
<p>Carmen Paz, Sylvain:</p>
<p>Este sitio nació de mirar con atención lo que Almud ya publica. No hay frases inventadas ni promesas de agencia: cada título sale de sus posts de Instagram, de su bio, de su carta o de lo que sus clientes escribieron en Tripadvisor. Lo que hicimos fue ordenarlo, darle aire y ponerlo en movimiento.</p>
<p>Tampoco hay fotos de banco de imágenes. Todas las fotos y los videos son de Almud, y los colores salen de su propio local: las cintas del techo, el muro rosa de la barra y el letrero.</p>
<p>Este documento explica, sección por sección, qué se decidió y por qué. En cada lámina, a la izquierda está la sección tal como se ve en el sitio, en computador y en celular. A la derecha, de dónde salió cada texto e imagen, qué letra y qué color se usó, cómo se mueve y por qué va en ese lugar del recorrido.</p>
<p>Es un regalo. Ojalá lo disfruten tanto como nosotros disfrutamos haciéndolo.</p>
<p class="sign">Pablo Figueroa G.<br><span>Director de estudio</span></p>
</div>''', 'rosa', 'crema')

# ═════════════════════════ 03 · DE DÓNDE VIENE TODO ═════════════════════════
grid15 = ['lugar-barra', 'tragos-bartender', 'lugar-terraza-techada', 'con-quien-brindis', 'comida-pizza',
          'eventos-12-anos', 'tragos-splash', 'quien-grupo-peter', 'lugar-ojo-piojo', 'carta-sangria',
          'lugar-sillones', 'lugar-terraza-abierta', 'eventos-fondita', 'comida-ceviche', 'donde-puerta']
lamina(
    f'''<p class="lab">Algunas de sus fotos · Instagram @almud_bar</p>
<div class="igrid">{"".join(f'<img src="{med(i, 360)}" alt="">' for i in grid15)}</div>
<p class="lab" style="margin-top:.18in">Su carta, en su propia página del sitio</p>
<div class="pair2"><img src="{shot("m-carta", 700)}" alt=""><img src="{shot("m-carta2", 700)}" alt=""></div>''',
    f'''<p class="kick">Materia prima</p><h2>De dónde viene todo</h2>
<p class="lead">Antes de diseñar, reunimos lo que Almud ya había publicado y lo ordenamos: el local, la barra, la cocina, la gente, las fiestas, el equipo y la carta.</p>
<div class="grid">
{block("Instagram @almud_bar", "<p>Su perfil tiene <b>759 publicaciones</b>. Leímos completas las <b>180 más recientes</b>, de diciembre de 2022 a octubre de 2026, con sus textos y <b>57 videos</b>. De ahí salen los títulos y todas las imágenes del sitio: <b>52 fotos y 13 videos</b>, de 38 publicaciones distintas.</p>")}
{block("La carta", "<p>Las <b>7 cartas oficiales</b> del enlace de su bio: <b>10 secciones y 256 tragos, platos y bebidas</b>. Los nombres, las descripciones y los precios del sitio están al pie de la letra.</p>")}
{block("Lo que dicen de ustedes", "<p><b>18 reseñas</b> citables de Tripadvisor y Google, en español, inglés y francés. En el sitio van las <b>10</b> que dicen de dónde venía quien la escribió.</p>")}
{block("Quién hizo las imágenes", "<p>Al pie van las productoras que ustedes mismos acreditan en sus posts: @catarsis.fotografia, @estudiouno.prod e @isosur.prod.</p>")}
{block("La regla", "<p>Cada texto del sitio tiene su origen identificado: qué post, qué línea de la bio, qué carta o qué reseña. Lo único escrito por nosotros son las indicaciones de uso: «Carta», «Ver la carta», «Escríbenos por DM», «Abrir en Google Maps», los nombres de los rincones y las ayudas en inglés para el turista.</p>", "wide")}
</div>''', 'negro', 'crema')

# ═════════════════════════ 04 · VOZ ═════════════════════════
lamina(
    f'''<p class="lab">El sitio</p>
{fig("d-lugar-a", "Su frase, como título de El lugar · en el computador")}
<div class="row2 r4">{fig("m-en-lugar", "La misma sección en inglés", "mob")}
<div class="lnote"><p>En inglés, sus frases no se traducen: quedan en español y llevan debajo una ayuda corta para el turista, con el mismo humor: «Restless souls who love colorssss!».</p></div></div>''',
    f'''<p class="kick">Sistema · voz</p><h2>Escribir como Almud</h2>
<p class="lead">El sitio no agrega adjetivos ni promesas: habla como habla Almud, de usté, con cariño y con juego de palabras. Y elige, de todo lo que publican, lo que mejor recibe a alguien que llega por primera vez.</p>
{quote("Somos inquietos y nos gusta el colorssss!", ig("IG-111"), True)}
<div class="grid">
{block("De usté, invitando", quote("Le esperamos desde las 18:00 hrs", ig("IG-155")) + quote("USTÉ SE LO MERECE!", ig("IG-087")) + "<p>Las invitaciones con que cierran sus posts cierran también el sitio.</p>")}
{block("El oficio, con humildad", quote("mucho amor, color y trabajo", ig("IG-045")) + "<p>Nunca dicen «mixología»: hablan de amor y de horas de trabajo. Así se presentan los tragos.</p>")}
{block("Nadie queda afuera", quote("no dejamos a nadie ajuera", ig("IG-011")) + "<p>La frase acompaña a los tragos sin alcohol, en su propio rincón del carrusel.</p>")}
{block("Lo que se quedó en Instagram", "<p>Las cascadas («Almudcito ito ito»), las palabras en «-eichon», los «Besi» y las frases de carrete funcionan en sus posts, donde todos los conocen. En una vitrina para alguien que llega por primera vez, restan. La única excepción es la frase de Elymar, en Equipo, que ustedes escribieron así.</p>")}
</div>''', 'amarillo', 'crema')

# ═════════════════════════ 05 · TIPOGRAFÍA ═════════════════════════
lamina(
    f'''<p class="lab">El sitio</p>
{fig("d-tragos-c", "Los nombres de sus tragos, en la letra de los títulos · en el computador")}
<div class="spec">
  <p class="sp1">Aquí te las traigo Peter</p><p class="cap">Big Shoulders Display · títulos y nombres</p>
  <p class="sp2">Pisco, elderflower, cranberry y burbuja de humo. $ 6.700</p><p class="cap">Barlow Condensed · textos, precios y botones</p>
</div>''',
    f'''<p class="kick">Sistema · tipografía</p><h2>Letras angostas, como su letrero</h2>
<p class="lead">El letrero de Almud y su logotipo son letras altas y angostas, y sus afiches gritan los títulos en mayúsculas gruesas. El sitio usa dos letras de esa misma familia: una para gritar y otra para leer.</p>
<div class="grid">
{block("Big Shoulders Display · títulos", "<p>Condensada y gruesa, en mayúsculas, como el «BAR» de su logotipo y los títulos de sus afiches. Va en los títulos de cada sección y en los nombres de los rincones, de los tragos, de los platos y de las fiestas.</p>")}
{block("Barlow Condensed · lectura", "<p>De la misma familia angosta, pero tranquila. Va en los textos, los precios, los botones y las ayudas en inglés. Se lee cómoda en el celular, incluso de noche y con poca luz.</p>")}
{block("El logo no se escribe", "<p>La letra del «ALMUD» del letrero es preciosa pero se lee mal a tamaño de texto. Por eso no se usa para escribir: el logotipo va siempre dibujado, tal como es.</p>")}
{block("Primero, que se lea", "<p>Ningún texto es chico, los títulos no pasan de tres líneas y los precios van en el mismo color del texto, sin competir con el nombre. Las letras viajan con el sitio, así que nunca cambian de forma mientras se lee.</p>")}
</div>''', 'rosa', 'crema')

# ═════════════════════════ 06 · PALETA ═════════════════════════
SW = [('Amarillo cinta', 'amarillo', 'El lugar'), ('Rosa muro', 'rosa', 'Tragos'), ('Naranja cinta', 'naranja', 'Comida'),
      ('Verde cinta', 'verde', 'Con quién'), ('Lila cinta', 'lila', 'Eventos'), ('Rojo cinta', 'rojo', 'Equipo'),
      ('Crema', 'crema', 'Reseñas'), ('Negro', 'negro', 'Portada y cierre'), ('Azul letrero', 'azul', 'el «BAR»')]
sw_html = ''.join(f'<span class="sw c-{k}{" dk" if k in OSCUROS else ""}"><b>{E(n)}</b><i>{COL[k]}</i><em>{E(s)}</em></span>' for n, k, s in SW)
lamina(
    f'''<p class="lab">El sitio</p>
<div class="mrow3">{fig("m-lugar-a", "El lugar", "mob")}{fig("m-tragos-a", "Tragos", "mob")}{fig("m-quien-a", "Con quién", "mob")}</div>
<p class="lnote" style="margin-top:.1in">Amarillo, rosa muro y verde cinta · en el celular. Cada sala tiene su color.</p>''',
    f'''<p class="kick">Sistema · color</p><h2>La paleta está colgando del techo</h2>
<p class="lead">Almud es color puro: el techo de miles de cintas, el muro rosa de botellas, los banderines y el letrero azul. En vez de inventar colores, se tomaron de ahí, uno por sección.</p>
<div class="sws">{sw_html}</div>
<p class="lab dkl">De estas fotos de su Instagram salen los colores</p>
<div class="srcp">
 <figure><img src="{plan("cintas")}" alt=""><figcaption>Techo de cintas<b>{ig("IG-050")}</b></figcaption></figure>
 <figure><img src="{plan("muro")}" alt=""><figcaption>Muro rosa<b>{ig("IG-008")}</b></figcaption></figure>
 <figure><img src="{plan("barra")}" alt=""><figcaption>Barra y banderines<b>{ig("IG-079")}</b></figcaption></figure>
</div>
<div class="grid">
{block("Un color por sala", "<p>Pasar de una sección a otra es como pasar de la barra a la terraza: cambia la luz. La carta usa los mismos colores, uno por pestaña.</p>")}
{block("Un solo negro y un azul", "<p>El negro es el de sus videos y afiches. El azul es el del letrero y solo pinta el «BAR» del logo.</p>")}
{block("Contraste", "<p>El rojo y el verde quedaron un poco más hondos que en las cintas, para que el texto crema se lea con holgura. Sobre los colores claros, el texto va en negro. Se revisó texto por texto, en el inicio y en la carta.</p>", "wide")}
</div>''', 'negro', 'crema')

# ═════════════════════════ 07 · LOGO ═════════════════════════
lamina(
    f'''<div class="logos">
  <div class="lg dark wide"><img src="{LOGO_C}" alt=""></div>
  <div class="lg cream wide"><img src="{LOGO_O}" alt=""></div>
  <div class="lg dark"><img src="{png("brand/v3/png/almud-vertical-claro.png", 600)}" alt=""></div>
  <div class="lg yel"><img src="{png("brand/v3/png/almud-isotipo-oscuro.png", 400)}" alt=""></div>
</div>''',
    f'''<p class="kick">Sistema · logo</p><h2>El almud del letrero</h2>
<p class="lead">El logotipo ALMUD BAR y su isotipo, el almud, se redibujaron siguiendo los trazos de su carta y su letrero, para que se vean nítidos a cualquier tamaño: desde el ícono de la pestaña del navegador hasta un letrero.</p>
<div class="grid">
{block("Trazos respetados", "<p>ALMUD alto y fino en blanco, BAR grueso en azul letrero, y el almud con su boca de rombo. Nada se estiró ni se simplificó.</p>")}
{block("Variantes", "<p>Horizontal y vertical, en claro para la noche y en oscuro para el crema de la carta, más el almud solo para el ícono y para la imagen que aparece al compartir el enlace por WhatsApp.</p>")}
{block("Letra por letra", "<p>El logotipo se separó en sus ocho letras para que en la portada entren una a una, con rebote, como cuando ustedes escriben «V I E R N E S».</p>" + quote("V I E R N E S", ig("IG-107")))}
{block("Dónde aparece", "<p>El almud se dibuja trazo a trazo mientras carga la página y luego abre la portada. El logotipo vive en la barra de arriba, encabeza la portada a gran escala y cierra el pie en su versión vertical.</p>")}
</div>''', 'negro', 'crema')

# ═════════════════════════ 08 · RECORRIDO ═════════════════════════
strip = [('d-carga-2', '1 · La espera'), ('d-hero', '2 · Portada'), ('d-lugar-b', '3 · El lugar'),
         ('d-tragos-b', '4 · Tragos'), ('d-comida-a', '5 · Comida'), ('d-quien-a', '6 · Con quién'),
         ('d-eventos-a', '7 · Eventos'), ('d-equipo-a', '8 · Equipo'), ('d-resenas', '9 · Reseñas')]
lamina(
    '<p class="lab">El sitio</p><div class="strip">' + ''.join(f'<figure><img src="{shot(s, 640)}" alt=""><figcaption>{c}</figcaption></figure>' for s, c in strip)
    + '</div><p class="lnote">El recorrido de arriba hacia abajo · en el computador. Lo cierra «Usté se lo merece!» (10).</p>',
    f'''<p class="kick">Sistema · recorrido</p><h2>Entrar a Almud un viernes</h2>
<p class="lead">El orden de la página no es una lista de servicios: es la visita de un cliente. Se abre la puerta, se ve el local lleno, se pide en la barra, se come, se brinda con la gente y al final se sabe cómo volver.</p>
<div class="grid acts">
{block("<em>1</em> Entrar", "<p>La espera, con el almud que se dibuja y abre la boca, y la portada: el local en movimiento, el logo y su bio. Un solo botón: «Ver la carta».</p>")}
{block("<em>2</em> Pedir", "<p>El lugar y sus seis rincones; después la barra, con el Peter y cinco tragos más de la carta, y la cocina, con ocho platos.</p>")}
{block("<em>3</em> Celebrar", "<p>La gente, las fiestas del año y el equipo que atiende. Es la parte más larga, porque Almud es su gente.</p>")}
{block("<em>4</em> Volver", "<p>Lo que dicen sus clientes de otros países y, al final, «Usté se lo merece!» con el día, la hora, la dirección, el mapa y cómo escribirles.</p>")}
{block("Ritmo", "<p>Cada sección cambia de color y de forma: una ruleta que se arrastra, columnas desordenadas a propósito, una baraja de fotos, un carrusel de fiestas, tarjetas que se dan vuelta, cintas de reseñas. Ninguna composición se repite dos veces seguidas.</p>", "wide")}
</div>''', 'crema', 'crema')

# ═════════════════════════ 09 · LA ESPERA ═════════════════════════
seccion('La espera', '01 · La espera antes de entrar', 'Almud Bar · Serrano 325', 'Su isotipo y su logotipo',
        'Mientras la página carga, la pantalla está en negro y el almud se dibuja de abajo hacia arriba. Al completarse, su boca se abre y por ahí aparece el bar.',
        f'<div class="two">{fig("d-carga-2", "El almud se dibuja según lo que ya cargó, con el porcentaje debajo", w=1100)}{fig("d-apertura", "Al 100 %, la boca se abre y adentro ya corre el video", w=1100)}</div>',
        [block("Qué se ve", "<p>Sobre negro, el almud se dibuja trazo a trazo, al ritmo de lo que de verdad va bajando: el video de la portada, el logo y las primeras fotos. Debajo, solo el porcentaje. Al llegar al cien, la boca de rombo se abre hasta llenar la pantalla y el video parte desde el comienzo.</p>"),
         block("Tiempos", "<p>Dura al menos tres segundos, para que el dibujo se alcance a ver, y nunca más de ocho: si la conexión es lenta, el almud se completa igual y lo demás sigue cargando por detrás. Quien tenga el movimiento reducido en su equipo entra directo a la portada.</p>"),
         block("Por qué así", "<p>El almud es la medida chilota que le da nombre al bar, y su boca abierta es justamente «lo que se llena». En vez de una pantalla vacía, la espera es su logo dibujándose; al terminar, el almud se abre y deja ver el bar lleno.</p>", 'wide')],
        'negro')

# ═════════════════════════ 10 · PORTADA ═════════════════════════
seccion('Portada', '02 · Portada', 'Coctelería de autor, comida &amp; música bonita desde 2014', 'Bio de Instagram',
        'El local a pantalla completa, en movimiento. Encima, solo el logotipo, la frase de su bio y un botón.',
        f'<div class="row2">{fig("d-hero", "En el computador")}{fig("m-hero", "En el celular", "mob")}</div>',
        [block("Textos", "<p>La única frase es la primera línea de su bio, tal cual. El botón es uno solo: «Ver la carta». La dirección y el horario quedaron para el final, donde se buscan.</p>"),
         block("Imágenes", thumbs([("portada-c-h-l", "Su video institucional, hecho por @estudiouno.prod · "), ("lugar-techada-llena", "La terraza techada llena · ")])),
         block("Movimiento", "<p>Un solo montaje, igual en el computador, la tablet y el celular: los flecos y el letrero de su video institucional, y después la cámara caminando por la terraza techada llena, bajo las cintas. El video avanza siempre y se funde del final al comienzo, sin cortes.</p>"),
         block("Por qué así", "<p>La mejor manera de presentar un bar es mostrarlo lleno. La portada es el bar, no una persona: el barman y ustedes tienen su lugar en Equipo. Y parte igual en cualquier pantalla, para que todos entren por la misma puerta.</p>")],
        'negro')

# ═════════════════════════ 11 · EL LUGAR ═════════════════════════
seccion('El lugar', '03 · El lugar', 'Somos inquietos y nos gusta el colorssss!', ig('IG-111'),
        'Sobre amarillo cinta: el local lleno de noche, tres fotos de las salas repletas y una ruleta con sus seis rincones.',
        f'<div class="two">{fig("d-lugar-b", "El local lleno, en tres fotos", w=1100)}{fig("d-lugar-c", "La ruleta de rincones", w=1100)}</div>',
        [block("Textos · un rincón, una frase suya",
               quote("Pucha que nos gusta nuestra barrita!", 'Barra · ' + ig('IG-087')) + quote("Techamos parte de la terraza", 'Terraza techada · ' + ig('IG-004'))
               + quote("Felices, con el corazón llenifer!", 'Sillones · ' + ig('IG-009') + ' · «corazón» en lugar del emoji')
               + quote("Amamos los atardeceres desde nuestra terracita", 'Terraza · ' + ig('IG-163')) + quote("Nos gustan los brillitos, las luces", 'Lámparas · ' + ig('IG-147'))
               + quote("una mirada vale más que mil palabras", 'Ojo Piojo · ' + ig('IG-118'))),
         block("Imágenes", thumbs([("lugar-barra", "Barra · "), ("lugar-sillones", "Sillones · @estudiouno.prod · "), ("lugar-lampara-pinzas", "Lámparas · "), ("lugar-ojo-piojo", "Ojo Piojo · ")])),
         block("Movimiento", "<p>Cada «s» de «colorssss!» se estira y rebota, al entrar y al pasar el dedo. Las fotos del local lleno se abren en rombo, como la boca del almud. La ruleta se arrastra con el dedo o el mouse y cada foto se balancea, como colgada del techo. Las seis fotos ya están listas antes de llegar: ninguna aparece vacía.</p>"),
         block("Por qué así", "<p>«colorssss» es su juego de palabras más reconocible y su frase es el manifiesto del lugar. Los rincones muestran el espacio, y la franja de fotos repletas muestra que siempre está lleno.</p>")],
        'amarillo')

# ═════════════════════════ 12 · TRAGOS ═════════════════════════
seccion('Tragos', '04 · Tragos', 'mucho amor, color y trabajo', ig('IG-045'),
        'Sobre rosa muro: el Peter con su burbuja de humo, grande y en movimiento; a su lado, la barra en columnas desordenadas, y debajo un carrusel con cinco tragos más de la carta.',
        f'<div class="two">{fig("d-tragos-peter", "El Peter, con su nombre armándose sobre el humo", w=1100)}{fig("d-tragos-c", "El carrusel de tragos con nombre y precio", w=1100)}</div>',
        [block("Los seis de la carta", precios([("Aquí te las traigo Peter", "$ 6.700"), ("Sagüer on Faia", "$ 7.900"), ("Sangría Foreva!", "$ 6.500"),
                                                 ("Cómo te voy a olvidar", "$ 6.800"), ("A veces me pongo Coquette", "$ 7.100"), ("La moto chantá", "$ 6.400")])
               + '<p class="small">Nombres y precios de su Coctelería de la casa y de sus mocktails, al pie de la letra.</p>'),
         block("Imágenes", thumbs([("tragos-humo", "El Peter · "), ("tragos-bartender", "Frente al muro · "), ("carta-saguer", "Sagüer · "), ("carta-moto", "Moto chantá · ")])),
         block("Movimiento", "<p>«Aquí te las traigo Peter» se arma letra por letra sobre el video del humo. Las fotos se «sirven» de arriba abajo, como un vaso que se llena. En el carrusel, cada nombre también se arma al entrar; se arrastra con el dedo o el mouse, y un toque abre ese trago en la carta.</p>"),
         block("Por qué así", "<p>El Peter es su trago más llamativo y su nombre ya es un grito, así que abre la sección.</p>" + quote("Aquí te las traigo Peter!", ig('IG-044')) + "<p>Un trago lleva nombre solo si la foto es ese trago y el nombre sigue en la carta.</p>")],
        'rosa')

# ═════════════════════════ 13 · COMIDA ═════════════════════════
seccion('Comida', '05 · Comida', 'una cocina sencilla pero más que sabrosona!', ig('IG-022'),
        'Sobre naranja cinta: la pizza recién salida, dos platos en video y cuatro más en dos columnas, cada uno con su nombre y precio.',
        f'<div class="two">{fig("d-comida-a", "La pizza y los platos en video", w=1100)}{fig("d-comida-b", "El orden del desorden", w=1100)}</div>',
        [block("De su carta", precios([("Tukulito Sakayama", "$ 15.900"), ("La carne es débil", "$ 11.900"), ("Una cosa poca", "$ 11.900"), ("Todo que ver!", "$ 16.000"),
                                        ("Con tuti si no pa qué!", "$ 19.900"), ("Chambreao", "$ 10.900"), ("Camarón que se duerme", "$ 15.900")])
               + '<p class="small">Más sus Pizzas artesanales, que abren la sección.</p>'),
         block("Imágenes", thumbs([("comida-pizza", "Pizza · @catarsis.fotografia · "), ("comida-ceviche", "Todo que ver! · "), ("comida-hamburguesa", "Chambreao · "), ("carta-contuti", "Con tuti · ")])),
         block("Movimiento", "<p>Los platos llegan girando un poco, como cuando se sirven en la mesa, y su foto se abre en redondo, como un plato. «más que sabrosona!» late cada pocos segundos.</p>"),
         block("Por qué así", "<p>Cada video muestra el plato que nombra: el sartén es «La carne es débil» y el queso que se estira es «Una cosa poca». Las columnas parten a distinta altura y no se realinean: un orden del desorden.</p>")],
        'naranja')

# ═════════════════════════ 14 · CON QUIÉN ═════════════════════════
seccion('Con quién', '06 · Con quién', 'no somos ná sin ustedes!', ig('IG-026'),
        'Sobre verde cinta: tres videos de mesas llenas y, al centro, una baraja de doce fotos de su gente que se lanza con el dedo.',
        f'<div class="row2">{fig("d-quien-b", "La baraja entre los videos · en el computador")}{fig("m-quien-b", "En el celular", "mob")}</div>',
        [block("Textos", quote("Ya saben que no somos ná sin ustedes! Faltan muuuchas más, pero no se pueden subir más de 20", ig('IG-026'))
               + "<p>El título es la única frase. Las fotos dicen el resto.</p>"),
         block("Imágenes", thumbs([("quien-grupo-peter", "Polera Peter · "), ("con-quien-brindis", "Brindis · @estudiouno.prod · "), ("quien-carcajadas", "Carcajadas · "), ("quien-mesa-llena", "Mesa llena · ")])),
         block("Movimiento", "<p>El título entra como un brindis: «no somos ná» llega por la izquierda, «sin ustedes!» por la derecha, y chocan. La foto de arriba se lanza, sale volando y vuelve por debajo de la pila: la baraja nunca se acaba. Los videos siguen corriendo al lado.</p>" + quote("Venga a hacer chin chin que esta vida es una sola!", ig('IG-157'))),
         block("Por qué así", "<p>Sus posts de gente son carruseles de hasta veinte fotos que se pasan con el dedo; la baraja convierte ese gesto en juego. La sección es de la gente, en plural: los videos son de mesas llenas, grupos y baile, y se dejó fuera un plano que la fiesta no necesitaba.</p>")],
        'verde')

# ═════════════════════════ 15 · EVENTOS ═════════════════════════
seccion('Eventos', '07 · Eventos', 'tirar la casa por la ventana!', ig('IG-010'),
        'Sobre lila cinta: la fiesta de aniversario en video, una frase suya sobre cómo se vive una fiesta en Almud y un carrusel con las tres fiestas que se repiten cada año.',
        f'<div class="two">{fig("d-eventos-a", "El título, la bajada y el Aniversario", w=1100)}{fig("d-eventos-b", "La Fondita, en el carrusel de fiestas", w=1100)}</div>',
        [block("Textos", quote("Se comió, se tomó, se bailó, quedamos con dolor de guata de tanto reír", ig('IG-072'))
               + precios([("Aniversario", "julio"), ("Fondita", "septiembre"), ("Jalogüín", "octubre")])
               + '<p class="small">Solo el mes y el nombre, sin fechas ni promesas: nada que ustedes no hayan anunciado.</p>'),
         block("Imágenes", thumbs([("eventos-12-anos", "12 años · @isosur.prod · "), ("eventos-baile-12", "El baile · @isosur.prod · "), ("eventos-fondita", "La fondita · "), ("eventos-jaloguin", "Jalogüín · ")])),
         block("Movimiento", "<p>Cada palabra del título cae desde arriba con un giro y rebota, como lanzada por la ventana. Las fiestas pasan solas cada pocos segundos: el nombre se arma letra por letra, enorme, y las fotos se reparten con un giro leve. Se pueden pasar con el dedo, el mouse o las flechas. Jalogüín va en video, con disfraces y la barra llena.</p>"),
         block("Por qué así", "<p>Almud acaba de cumplir 12 años y el título es su propia frase sobre esa fiesta. La bajada la eligieron entre sus frases porque resume la fiesta mejor que cualquier frase nuestra. Quedaron fuera las fiestas de una sola vez y las campañas que no son suyas: el carrusel muestra lo que vuelve cada año.</p>")],
        'lila')

# ═════════════════════════ 16 · EQUIPO ═════════════════════════
seccion('Equipo', '08 · Equipo', 'Peazo de equipo que tenemos!', ig('IG-048'),
        'Sobre rojo cinta: el video del cumpleaños número 10 con ustedes dos y seis tarjetas del equipo que se dan vuelta al tocarlas.',
        f'<div class="row2">{fig("d-equipo-flip", "Dos tarjetas dadas vuelta · en el computador")}{fig("m-equipo-flip", "En el celular", "mob")}</div>',
        [block("Al dar vuelta la tarjeta", precios([("Barra", "«mente creadora de muchos cócteles»"), ("Barra", "«la regia»"), ("Barra", "«haciéndole los copetitos a usté»"),
                                                     ("Liz · Salones", "«la amada»"), ("Salones", "«el ondero»"), ("Elymar · Barra y salón", "«le pone una sonrisota con cada cóctecito ito ito»")])
               + '<p class="small">Frases de sus posts (' + ig('IG-045') + ', ' + ig('IG-067') + ', ' + ig('IG-034') + ' y ' + ig('IG-001') + '). La de Elymar pasa al singular, porque aquí habla de ella sola (el original dice «le ponen»).</p>', 'wide'),
         block("Los dueños", quote("los papis del almud: el franchuto y la disharashera", ig('IG-067')) + "<p>Al pie de la sección, con sus propias palabras.</p><p class='small'>El post nombra también sus cuentas de Instagram; en el sitio se omiten.</p>"),
         block("Por qué así", "<p>El sitio habla por el local, no expone a su gente: no hay cuentas personales de Instagram, ni del equipo ni de ustedes. Cada uno aparece con su lugar en el bar y el apodo cariñoso que ustedes le dieron. El video con ustedes dos está aquí y no en la portada, para que la portada sea del local.</p>")],
        'rojo')

# ═════════════════════════ 17 · RESEÑAS ═════════════════════════
seccion('Reseñas', '09 · Reseñas', 'Que no se lo cuenten', ig('IG-024'),
        'Sobre crema, como el papel de la carta: diez reseñas de clientes en dos cintas que pasan solas en sentidos contrarios, cada una en su idioma y con la bandera de su país.',
        f'{fig("d-resenas", "Diez voces, tres idiomas · en el computador")}',
        [block("Lo que dicen", quote("Super soirée à Castro ! Le service est sympa, super ambiance, avec musique très sympa!", 'Dorothee · Épinal, Francia · Tripadvisor')
               + quote("La raja el bar, totalmente recomendable. Ondero, buena música, tragos buenísimos y una barra tipo NYC!", 'Andres · Santiago, Chile · Tripadvisor')
               + quote("Estuve ahí cada día de mi estancia, porque es imposible no volver.", 'arqggodoy · Iquique, Chile · Tripadvisor'), 'wide'),
         block("Cómo se mueven", "<p>Las dos cintas avanzan de a una tarjeta y se detienen un momento para leer, desfasadas: siempre hay una quieta. Se pueden arrastrar con el dedo o el mouse, y se detienen al pasar el cursor encima.</p>"),
         block("Por qué así", "<p>Van solo las reseñas que dicen de dónde venía quien las escribió: Francia, Nueva Zelanda y varias ciudades de Chile. Cada una en su idioma y con su ortografía («Castro !»). Repiten lo que más elogian sus clientes: la terraza, la atención, la música y la sorpresa de encontrar «un vrai bar». Ninguna habla de esperas.</p>")],
        'crema')

# ═════════════════════════ 18 · CIERRE ═════════════════════════
seccion('Usté se lo merece', '10 · Cierre', 'USTÉ SE LO MERECE!', ig('IG-087'),
        'Una sola sección de noche para cerrar: la terraza de tarde, su firma en grande y, al lado, cuándo y dónde, con el mapa y el botón para escribirles. Al pie, el logo y los créditos.',
        f'<div class="row2">{figc("d-cierre-b", "Cierre · en el computador", 0.66)}{fig("m-cierre-a", "En el celular", "mob")}</div>',
        [block("Datos", quote("Le esperamos desde las 18:00 hrs", ig('IG-155')) + "<p><b>Mar a Sáb · Serrano 325, Castro.</b> Son los de su bio. Debajo, la referencia que usan todos: «Al frente del Centro Cultural de Castro».</p>"),
         block("Imágenes", thumbs([("donde-terraza", "La terraza de tarde · "), ("donde-puerta", "La puerta · @estudiouno.prod · ")])),
         block("Movimiento", "<p>«Le esperamos desde las 18:00 hrs» se escribe en vivo, letra por letra, con un cursor rosa que la sigue. El video de la terraza va entero, sin recortes. El mapa de Google está en la misma página, en el punto exacto, con un enlace para abrirlo en el celular.</p>"),
         block("Por qué así", "<p>Lo práctico llega cuando ya se decidió. No hay «Reservar»: Almud conversa por mensaje directo, así que el botón lleva ahí. Y el cierre es su firma de siempre, con su ortografía: usté se lo merece.</p>")],
        'negro')

# ═════════════════════════ 19 · DETALLES ═════════════════════════
lamina(
    f'''<p class="lab">El sitio</p>
{fig("d-carta", "La carta, en su propia página · en el computador")}
<div class="mrow3">{fig("m-carta", "La carta en el celular", "mob")}{fig("m-en-lugar", "Modo inglés", "mob")}{fig("m-comida-b", "Comida", "mob")}</div>''',
    f'''<p class="kick">Detalles en todo el sitio</p><h2>Lo que no se ve, pero se siente</h2>
<p class="lead">Pequeñas decisiones que no se notan una por una, pero que hacen que el sitio se sienta cuidado de principio a fin.</p>
<div class="grid">
{block("La carta, perfecta", "<p>Una página aparte con sus 256 ítems al pie de la letra. Las siete pestañas se ven siempre completas, en cualquier pantalla, cada una con un color de las cintas. Cada trago y plato del inicio abre su lugar exacto en ella.</p>")}
{block("Dos idiomas", "<p>Un botón «EN» arriba. Sus frases y los nombres de la carta no se traducen: llevan debajo una ayuda en inglés. La elección queda recordada para la próxima visita.</p>")}
{block("Los videos nunca se detienen", "<p>Corren solos desde que se ven y siguen corriendo al bajar. Los de la sección siguiente se preparan antes de llegar, así que ninguno se ve quieto.</p>")}
{block("Pensado para el celular", "<p>Ruletas, carruseles, la baraja, las tarjetas y las reseñas se manejan con el dedo, y un deslizamiento vertical siempre mueve la página.</p>")}
{block("Solo cuentas de Almud", "<p>No hay perfiles personales en ninguna parte del sitio. Solo enlazan Almud y las productoras que hicieron las fotos y los videos.</p>")}
{block("Al compartir", "<p>Al mandar el enlace por WhatsApp aparece una imagen con el logo y la frase de la bio, no un cuadro vacío. Quien tenga el movimiento reducido ve el sitio completo y quieto.</p>")}
</div>''', 'naranja', 'crema')

# ═════════════════════════ 20 · CIERRE ═════════════════════════
lamina(
    f'<img class="bleed" src="{med("lugar-terraza-repleta", 1400)}" alt="" style="object-position:50% 50%">',
    f'''<div class="close">
  <img class="cl-logo" src="{LOGO_C}" alt="">
  <p class="kick">Lo que sigue</p><h2>Hacerlo suyo</h2>
  <p class="lead">Este sitio se hizo solo con lo que ya estaba publicado. Con un par de conversaciones podría ir mucho más lejos:</p>
  <ul class="next"><li>Fotografía propia de cada rincón, como los sillones llenos de gente, y de ustedes dos</li>
    <li>Sus videos originales en alta, horizontales y verticales, para una portada aún más nítida</li>
    <li>Dominio propio .cl y alojamiento a nombre de Almud</li>
    <li>La carta y las fiestas del año al día, actualizadas desde el mismo sitio</li></ul>
  <p class="invite">Cuando quieran, lo conversamos.</p>
  <p class="who">Pablo Figueroa G.</p>
  <p class="role">Director de estudio</p>
  <p class="contact"><a href="mailto:pablo@bergerac.cl">pablo@bergerac.cl</a> · <a href="tel:+56975892096">+56 9 7589 2096</a></p>
  <p class="link"><a href="https://bergerac.cl">Bergerac.cl</a></p>
</div>''', 'negro', 'negro')

# ═════════════════════════ CSS ═════════════════════════
CSS = f'''
@font-face{{font-family:"BSD";src:url({font("big-shoulders-display-latin-wght-normal")}) format("woff2");font-weight:100 900}}
@font-face{{font-family:"BC";font-weight:400;src:url({font("barlow-condensed-latin-400-normal")}) format("woff2")}}
@font-face{{font-family:"BC";font-weight:500;src:url({font("barlow-condensed-latin-500-normal")}) format("woff2")}}
@font-face{{font-family:"BC";font-weight:600;src:url({font("barlow-condensed-latin-600-normal")}) format("woff2")}}
@page{{size:13in 8.5in;margin:0}}
:root{{--neg:#0e0c0b;--cre:#f5e9db;--rosa:#f24350;--tinta:#c41e34;--gris:#6d6159}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{background:#3a3532}}
body{{font-family:"BC",Arial Narrow,sans-serif;font-weight:500;color:var(--neg);-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.lam{{width:13in;height:8.5in;display:grid;grid-template-columns:6.5in 6.5in;overflow:hidden;margin:0 auto .3in;page-break-after:always;break-after:page;position:relative}}
@media print{{html,body{{background:none}}.lam{{margin:0}}}}
{"".join(f".c-{k}{{background:{v}}}" for k, v in COL.items())}
.L{{padding:.42in .4in .36in;display:flex;flex-direction:column;gap:.13in;overflow:hidden;color:var(--neg);position:relative}}
.L.dk{{color:var(--cre)}}
.L:has(.bleed){{padding:0}}
.bleed{{width:100%;height:100%;object-fit:cover;display:block}}
.R{{position:relative;padding:.46in .52in .66in;display:flex;flex-direction:column;overflow:hidden;color:var(--neg)}}
.R.dk{{color:var(--cre)}}
.lab{{font-family:"BC";font-weight:600;font-size:7pt;letter-spacing:.22em;text-transform:uppercase}}
.sh{{display:flex;flex-direction:column;gap:3pt;min-width:0}}
.sh img{{width:100%;display:block;border-radius:3pt;box-shadow:0 6pt 18pt rgba(0,0,0,.28)}}
.sh figcaption{{font-size:7.6pt;font-weight:500;opacity:.85}}
.two{{display:flex;flex-direction:column;gap:.14in}}
.two .sh{{align-items:center}}
.two .sh img{{width:auto;max-width:100%;max-height:2.42in}}
.two .sh figcaption{{align-self:stretch}}
.row2{{display:flex;gap:.2in;align-items:flex-start}}
.row2>.sh:first-child{{flex:1}}
.sh.mob{{width:1.55in;flex:none}}
.r4 .sh.mob{{width:1.25in}}
.r4 .sh.mob img{{max-height:2.45in;object-fit:cover;object-position:top}}
.mrow3 .sh.mob img{{max-height:3.3in;object-fit:cover;object-position:top}}
.mrow3{{display:flex;gap:.16in;justify-content:center}}
.mrow3 .sh.mob{{width:1.7in}}
.lnote{{font-size:9pt;line-height:1.4;flex:1;align-self:center;opacity:.9}}
.recw{{margin-top:auto}}
.rec{{list-style:none;columns:2;column-gap:.2in;font-size:8.4pt;font-weight:600;letter-spacing:.06em;text-transform:uppercase;line-height:1.7;margin-top:4pt}}
.rec li{{opacity:.45;break-inside:avoid}}
.rec li.on{{opacity:1}}
.rec li.on::before{{content:"";display:inline-block;width:6pt;height:6pt;background:currentColor;margin-right:5pt;transform:rotate(45deg);vertical-align:1pt}}
.kick{{font-weight:600;font-size:7.6pt;letter-spacing:.26em;text-transform:uppercase;color:var(--tinta);margin-bottom:.08in}}
.R.dk .kick{{color:var(--rosa)}}
h1,h2{{font-family:"BSD";font-weight:800;text-transform:uppercase;line-height:.95;letter-spacing:.005em}}
h2{{font-size:30pt;margin-bottom:.06in}}
.src{{font-weight:600;font-size:7.4pt;letter-spacing:.2em;text-transform:uppercase;color:var(--tinta);margin-bottom:.1in}}
.lead{{font-size:12pt;line-height:1.35;margin:.04in 0 .17in;max-width:5.4in}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:.16in .28in;align-content:start}}
.bk h4{{font-weight:600;font-size:7.4pt;letter-spacing:.2em;text-transform:uppercase;padding-bottom:3pt;border-bottom:1pt solid currentColor;margin-bottom:5pt}}
.bk h4 em{{font-family:"BSD";font-weight:800;font-style:normal;font-size:20pt;letter-spacing:0;color:var(--tinta);margin-right:4pt;vertical-align:-3pt}}
.bk p{{font-size:9.6pt;line-height:1.4;margin-bottom:4pt}}
.bk p.small{{font-size:7.6pt;color:var(--gris)}}
.bk.wide{{grid-column:1/-1}}
.q{{margin:0 0 5pt}}
.q p{{font-family:"BSD";font-weight:700;font-size:12pt;line-height:1.08;text-transform:uppercase;margin-bottom:1pt}}
.q p::before{{content:"«"}}.q p::after{{content:"»"}}
.q.big p{{font-size:24pt;font-weight:800}}
.q.big{{margin:.02in 0 .16in}}
.q cite{{display:block;font-style:normal;font-weight:600;font-size:6.8pt;letter-spacing:.16em;text-transform:uppercase;color:var(--tinta)}}
.R.dk .q cite{{color:var(--rosa)}}
.bk .q p{{font-size:10.4pt}}
.ths{{display:grid;grid-template-columns:repeat(4,1fr);gap:5pt}}
.bk .ths:has(.th:nth-child(2):last-child){{grid-template-columns:repeat(2,1fr)}}
.th img{{width:100%;height:.82in;object-fit:cover;display:block;border-radius:2pt}}
.th figcaption{{font-size:6.6pt;line-height:1.2;margin-top:2pt;color:var(--gris)}}
.th figcaption b{{display:block;font-weight:600;color:var(--tinta)}}
.pt{{width:100%;border-collapse:collapse;margin-bottom:3pt}}
.pt td{{font-size:9.2pt;padding:2.2pt 0;border-bottom:.5pt solid rgba(14,12,11,.25)}}
.pt td.n{{font-family:"BSD";font-weight:700;text-transform:uppercase;font-size:9.6pt}}
.pt td:last-child{{text-align:right;font-weight:600}}
.pf{{position:absolute;left:.52in;right:.52in;bottom:.28in;display:flex;justify-content:space-between;font-weight:600;font-size:6.6pt;letter-spacing:.22em;text-transform:uppercase;opacity:.65;border-top:.5pt solid currentColor;padding-top:5pt}}
/* portada */
.cover{{display:flex;flex-direction:column;justify-content:center;height:100%;gap:.12in}}
.cv-logo{{width:3.1in;margin-bottom:.2in}}
.cv-sub{{font-weight:600;font-size:9pt;letter-spacing:.3em;text-transform:uppercase;color:#f5c518}}
.cover h1{{font-size:56pt}}
.cover h1 span{{color:var(--rosa)}}
.cv-for{{font-family:"BSD";font-weight:700;font-size:17pt;text-transform:uppercase;margin-top:.2in;color:#2aa1f8}}
.cv-meta{{font-size:10.5pt;opacity:.8}}
/* carta */
.letter p{{font-size:10.6pt;line-height:1.5;margin-bottom:7pt;max-width:5.3in}}
.letter .sign{{font-family:"BSD";font-weight:800;font-size:15pt;text-transform:uppercase;margin-top:8pt;line-height:1.1}}
.letter .sign span{{font-family:"BC";font-weight:500;font-size:9.4pt;text-transform:none}}
/* materia prima */
.igrid{{display:grid;grid-template-columns:repeat(5,1fr);gap:4pt}}
.igrid img{{width:100%;aspect-ratio:1;object-fit:cover;display:block;border-radius:2pt}}
.pair2{{display:flex;gap:.14in}}
.pair2 img{{width:1.7in;height:2.6in;object-fit:cover;object-position:top;border-radius:3pt}}
/* tipografía */
.spec{{background:var(--cre);color:var(--neg);padding:.18in .22in;border-radius:3pt;margin-top:.1in}}
.sp1{{font-family:"BSD";font-weight:800;font-size:30pt;text-transform:uppercase;line-height:.95;color:#1d5fae}}
.sp2{{font-size:14pt;line-height:1.3;margin-top:.12in}}
.spec .cap{{font-weight:600;font-size:6.6pt;letter-spacing:.18em;text-transform:uppercase;color:var(--gris);margin-top:3pt}}
/* paleta */
.sws{{display:grid;grid-template-columns:repeat(9,1fr);gap:3pt;margin-bottom:.12in}}
.sw{{height:1.02in;padding:4pt;display:flex;flex-direction:column;justify-content:flex-end;gap:1pt;color:var(--neg);border-radius:2pt;outline:.5pt solid rgba(14,12,11,.2)}}
.sw.dk{{color:var(--cre)}}
.sw b{{font-family:"BSD";font-weight:800;text-transform:uppercase;font-size:7.4pt;line-height:1}}
.sw i{{font-style:normal;font-size:6.4pt}}
.sw em{{font-style:normal;font-size:6.2pt;opacity:.85}}
.srcp{{display:grid;grid-template-columns:repeat(3,1fr);gap:5pt;margin:4pt 0 .12in}}
.srcp img{{width:100%;height:.95in;object-fit:cover;display:block;border-radius:2pt}}
.srcp figcaption{{font-size:7pt;margin-top:2pt}}
.srcp figcaption b{{display:block;font-weight:600;color:var(--tinta);font-size:6.6pt}}
.dkl{{color:var(--tinta);margin-bottom:2pt}}
/* logos */
.logos{{display:grid;grid-template-columns:1fr 1fr;gap:6pt;padding:.42in .4in;height:100%;align-content:center}}
.lg{{display:grid;place-items:center;height:1.9in;padding:.25in;border-radius:3pt}}
.lg.dark{{background:#000;outline:.5pt solid #333}}.lg.cream{{background:var(--cre)}}.lg.yel{{background:#f5c518}}
.lg.wide{{grid-column:1/-1;height:1.45in}}
.lg img{{max-width:100%;max-height:1.35in;width:auto;height:auto;display:block}}
.lg.wide img{{max-height:.8in}}
/* recorrido */
.strip{{display:grid;grid-template-columns:repeat(3,1fr);gap:7pt}}
.strip img{{width:100%;aspect-ratio:16/10;object-fit:cover;display:block;border-radius:2pt}}
.strip figcaption{{font-weight:600;font-size:7.4pt;letter-spacing:.08em;text-transform:uppercase;margin-top:3pt}}
/* cierre */
.close{{display:flex;flex-direction:column;justify-content:center;height:100%;gap:.07in}}
.cl-logo{{width:2.2in;margin-bottom:.22in}}
.next{{list-style:none;margin:.02in 0 .2in}}
.next li{{font-size:12pt;line-height:1.4;padding:5pt 0;border-bottom:.5pt solid rgba(245,233,219,.35)}}
.close a{{color:inherit;text-decoration:none}}
.invite{{font-family:"BSD";font-weight:700;font-size:18pt;text-transform:uppercase;color:#f5c518;margin-bottom:.06in}}
.who{{font-weight:600;font-size:10pt;letter-spacing:.24em;text-transform:uppercase}}
.role{{font-size:10pt;margin-top:-3pt}}
.contact{{font-size:9pt;opacity:.7}}
.link{{font-family:"BSD";font-weight:800;font-size:20pt;letter-spacing:.06em;text-transform:uppercase;color:var(--rosa);margin-top:.1in}}
'''

DOC = f'''<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Almud Bar · Decisiones de diseño del sitio web</title><style>{CSS}</style></head>
<body>{"".join(L)}</body></html>'''
out = D / 'almud-dossier-diseno.html'
out.write_text(DOC, encoding='utf-8')
print('ok', out, len(L), 'láminas', round(len(DOC) / 1e6, 1), 'MB')
