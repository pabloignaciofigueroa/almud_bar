#!/usr/bin/env python3
"""Dossier-brochure de decisiones de diseño · Almud Bar (sitio final, almudbar.pages.dev).
Formato de la skill dossier-brochure-web-regalo (caso de referencia: chiloe_magico_tours/dossier).
Genera dossier/almud-dossier-diseno.html (autocontenido). PDF y PNG con dossier/render.js.
Uso: python3 dossier/build_dossier.py
"""
import base64, html, io, json, pathlib, random, re, subprocess, tempfile
from PIL import Image, ImageFilter, ImageOps

ROOT = pathlib.Path(__file__).resolve().parent.parent
D = ROOT / 'dossier'
SH = D / 'shots'
E = html.escape

# ───────── datos (desde los archivos, nunca de memoria) ─────────
IM = dict(json.loads((ROOT / 'assets/v3/media.json').read_text())['images'])
IM.update(json.loads((ROOT / 'assets/nv2/media-img.json').read_text())['images'])
IM.update(json.loads((ROOT / 'assets/nv9/media-img.json').read_text())['images'])
VI = json.loads((ROOT / 'assets/v4/media-video.json').read_text())['videos']
POSTS_L = json.loads((ROOT / 'content/ig_posts.json').read_text())
POSTS = {p['id']: p for p in POSTS_L}
N_POSTS = len(POSTS_L)
CARTA = json.loads((ROOT / 'content/carta-v2.json').read_text())['secciones']
N_SECC = len(CARTA)
N_ITEMS = sum(len(g.get('items', [])) for s in CARTA for g in s.get('grupos', [s]))
REV = json.loads((ROOT / 'content/reviews.json').read_text())
N_REV = len(REV)
BIO = (ROOT / 'content/bio.txt').read_text()
N_PUB = int(re.search(r'(\d+) publicaciones', BIO).group(1))

# Lo que usa la página principal (tools/boceto_raiz.py genera index.html)
RAIZ = (ROOT / 'tools/boceto_raiz.py').read_text()
_body = RAIZ[RAIZ.index("body = f'''"):]
_pre = RAIZ[RAIZ.index('rincones = ['):RAIZ.index("body = f'''")]
_pre = _pre[:_pre.index('def flip_duo')] + _pre[_pre.index('def resena'):]  # la tarjeta del dúo ya no está en la página
_ids = set(re.findall(r"(?:pic|vid|item2?|flip)\('([a-z0-9\-]+)'", _body)) | set(re.findall(r"'((?:con-quien|quien|lugar|eventos|equipo)-[a-z0-9\-]+)'", _pre))
_ids = {i for i in _ids if i in IM or i in VI}
N_FOTOS = sum(i in IM for i in _ids)   # «eventos-jaloguin» es foto y video a la vez: cuenta en ambos
N_VIDEOS = len({VI[i]['ref'] if i.startswith('portada') else i for i in _ids if i in VI})  # tramos de video; el montaje de portada va en dos formatos y cuenta una vez
N_POSTS_USADOS = len({d[i]['credit']['post'] for d in (IM, VI) for i in _ids if i in d})
CINTAS = re.findall(r"\('(FR|CL|NZ)', '(?:fr|es|en)'", RAIZ[RAIZ.index('CINTAS = ['):RAIZ.index('def flip(')])
N_RES_SITIO = len(CINTAS)
PAISES = {'FR': 'Francia', 'CL': 'Chile', 'NZ': 'Nueva Zelanda'}
N_PAIS = {k: CINTAS.count(k) for k in ('CL', 'FR', 'NZ')}

MES = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic']


def IG(pid):
    y, m, d = POSTS[pid]['date'].split('-')
    return f'Instagram · {int(d)} {MES[int(m) - 1]} {y}'


def FECHA(pid):
    return IG(pid).split(' · ')[1]


# ───────── imágenes ─────────
def b64img(img, w, q=80):
    img = img.convert('RGB')
    if img.width > w:
        img = img.resize((w, round(img.height * w / img.width)), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, 'JPEG', quality=q, optimize=True, progressive=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()


def shot(name, w=1500, crop=None):
    im = Image.open(SH / f'{name}.jpg')
    if crop:  # fracción del alto que se conserva, desde arriba
        im = im.crop((0, 0, im.width, round(im.height * crop)))
    return b64img(im, w)


def med(key, w=1400, crop='a', q=80):
    """La foto tal como la publica el sitio (recorte más grande) o el póster del video."""
    if key in VI:
        p = ROOT / VI[key]['poster']['webp']['path']
    else:
        c = IM[key]['crops']
        f = (c.get(crop) or next(iter(c.values())))['files']['webp']
        p = ROOT / f[str(max(int(x) for x in f))]['path']
    return b64img(ImageOps.exif_transpose(Image.open(p)), w, q)


def frame(video, t, w=2600):
    """Un cuadro del video de portada, a su resolución completa."""
    with tempfile.TemporaryDirectory() as td:
        out = pathlib.Path(td) / 'f.png'
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', str(t), '-i', str(ROOT / video), '-frames:v', '1', str(out)], check=True)
        im = Image.open(out).convert('RGB')
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.6, 60, 2))
        return b64img(im, w, 86)


def png(rel, w=900):
    im = Image.open(ROOT / rel).convert('RGBA')
    if im.width > w:
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, 'PNG', optimize=True)
    return 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()


def font(name):
    return 'data:font/woff2;base64,' + base64.b64encode((ROOT / 'assets/fonts' / f'{name}.woff2').read_bytes()).decode()


# ───────── paleta del sitio (css/nv18/tokens.css) ─────────
C = dict(amarillo='#f5c518', rosa='#f24350', naranja='#f27a12', verde='#0b6e4b', lila='#a58ac9', rojo='#c2202a',
         crema='#f5e9db', negro='#0e0c0b', azul='#2aa1f8', tinta='#c41e34', gris='#6d6159')
AM, RO, NA, VE, LI, RJ, CR, NE, AZ, TN, GR = (C[k] for k in ('amarillo', 'rosa', 'naranja', 'verde', 'lila', 'rojo', 'crema', 'negro', 'azul', 'tinta', 'gris'))

# ───────── piezas de layout (en pulgadas) ─────────
L, N = [], [0]


def nx():
    N[0] += 1
    return N[0]


def lam(bg, inner, nc='rgba(14,12,11,.45)'):
    k = nx()
    L.append(f'<article class="lam" style="background:{bg}">{inner}<span class="no" style="color:{nc}">{k:02d}</span></article>')


def box(x, y, w, inner, cls='', st=''):
    return f'<div class="tx {cls}" style="left:{x}in;top:{y}in;width:{w}in;{st}">{inner}</div>'


def fr(name, x, y, w, rot=0, z=2, crop=None, lt=False):
    return f'<div class="fr{' lt' if lt else ''}" style="left:{x}in;top:{y}in;width:{w}in;transform:rotate({rot}deg);z-index:{z}"><img src="{shot(name, 1400, crop)}" alt=""></div>'


def ph(name, x, y, w, rot=0, z=3):
    return f'<div class="ph" style="left:{x}in;top:{y}in;width:{w}in;transform:rotate({rot}deg);z-index:{z}"><img src="{shot(name, 560)}" alt=""></div>'


def photo(key, x, y, w, h, r=.24, pos='50% 50%', z=1, rot=0):
    return f'<div class="pic" style="left:{x}in;top:{y}in;width:{w}in;height:{h}in;border-radius:{r}in;transform:rotate({rot}deg);z-index:{z}"><img src="{med(key, 1500)}" style="object-position:{pos}" alt=""></div>'


def pill(t, bg, fg='#fff'):
    return f'<span class="pill" style="background:{bg};color:{fg}">{E(t)}</span>'


def plato(key, x, y, d, nombre, precio, rot=0):
    """Plato en redondo, como se abre su foto en el sitio, con su nombre y precio en una cápsula."""
    return (f'<div class="plato" style="left:{x}in;top:{y}in;width:{d}in;height:{d}in;transform:rotate({rot}deg)"><img src="{med(key, 700)}" alt=""></div>'
            f'<div class="tx tag" style="left:{x - .35}in;top:{y + d - .2}in;width:{d + .7}in">{pill(nombre + " · " + precio, NE, CR)}</div>')


def rombo(x, y, d, bg, fg, inner, fs=12, z=5):
    """Medallón con la forma de la boca del almud (un rombo)."""
    return (f'<div class="rb" style="left:{x}in;top:{y}in;width:{d}in;height:{d}in;z-index:{z}">'
            f'<span class="rb-bg" style="background:{bg}"></span><div style="color:{fg};font-size:{fs}pt">{inner}</div></div>')


def pol(key, x, y, w, rot, z=2):
    return f'<div class="pol" style="left:{x}in;top:{y}in;width:{w}in;transform:rotate({rot}deg);z-index:{z}"><img src="{med(key, 620, q=78)}" alt=""></div>'


def Q(text, source, cls=''):
    return f'<blockquote class="q2 {cls}"><p>«{text}»</p><cite>{E(source)}</cite></blockquote>'


def cintas(x0, x1, top=0, n=46, hmax=1.0, seed=7):
    """Las cintas de su techo colgando del borde superior: sus colores, largos dispares."""
    r = random.Random(seed)
    cols = [AM, RO, NA, VE, LI, RJ, AZ]
    w = (x1 - x0) / n
    return ''.join(f'<span class="cinta" style="left:{x0 + i * w:.3f}in;top:{top}in;width:{w * .78:.3f}in;height:{hmax * r.uniform(.35, 1):.2f}in;background:{r.choice(cols)}"></span>' for i in range(n))


def seal(x, y, d, rot=-8):
    ring = 'PARA ALMUD BAR ★ HECHO EN CASTRO ★ OCTUBRE 2026 ★ '
    return f'''<svg class="seal" viewBox="0 0 200 200" style="left:{x}in;top:{y}in;width:{d}in;height:{d}in;transform:rotate({rot}deg)">
  <defs><path id="sr" d="M100,100 m-74,0 a74,74 0 1,1 148,0 a74,74 0 1,1 -148,0"/></defs>
  <circle cx="100" cy="100" r="98" fill="{RJ}"/>
  <circle cx="100" cy="100" r="91" fill="none" stroke="#fff" stroke-width="2"/>
  <circle cx="100" cy="100" r="58" fill="none" stroke="#fff" stroke-width="1.5"/>
  <text font-family="BC" font-weight="600" font-size="12.5" fill="#fff"><textPath href="#sr" textLength="462" lengthAdjust="spacing">{ring}</textPath></text>
  <text x="100" y="98" text-anchor="middle" font-family="BSD" font-weight="800" font-size="34" fill="#fff">UN</text>
  <text x="100" y="131" text-anchor="middle" font-family="BSD" font-weight="800" font-size="34" fill="#fff">REGALO</text>
</svg>'''


LOGO_O = png('brand/v3/png/almud-horizontal-oscuro.png', 900)
ISO_O = png('brand/v3/png/almud-isotipo-oscuro.png', 300)

# ═════════════════════════ 01 · PORTADA ═════════════════════════
# La misma imagen con que se abre el sitio: el primer cuadro de su video de portada (el letrero), dentro de la boca del almud.
nx()
L.append(f'''<article class="lam" style="background:{NE}">
  <img class="bleed" src="{frame('assets/v4/video/portada-c-h-1280.mp4', 0.0)}" style="object-position:50% 45%" alt="">
  <div class="spread-tab"><img class="spread-logo" src="{LOGO_O}" alt="Almud Bar"></div>
</article>''')

# ═════════════════════════ 02 · CARTA ═════════════════════════
lam(CR,
    photo('lugar-techada-llena', .45, .45, 5.55, 7.6, pos='50% 40%', z=2) +
    seal(8.65, 5.75, 2.3) +
    box(6.55, .6, 6.0, f'''<p class="k" style="color:{TN}">Antes de empezar</p>
  <h2 class="t">Un sitio hecho <em style="color:{RO}">con</em> lo que ustedes ya dijeron</h2>
  <div class="letter">
  <p>Carmen Paz, Sylvain:</p>
  <p>Todo lo que van a ver ya era suyo. Cada título sale de sus posts, de su bio, de su carta o de lo que sus clientes escribieron en Tripadvisor; el sitio solo lo ordena, le da aire y lo pone en movimiento.</p>
  <p>Las imágenes también: las {N_FOTOS} fotos y los {N_VIDEOS} videos salen de su Instagram, sin fotos de banco. La letra, los colores y el logo vienen de su letrero, de sus afiches y de las cintas de su techo.</p>
  <p>Este documento cuenta, sección por sección, de dónde viene cada cosa. Es un regalo. Ojalá lo disfruten tanto como nosotros disfrutamos haciéndolo.</p>
  <p class="sign">Pablo Figueroa G.</p></div>'''))

# ═════════════════════════ 03 · DE DÓNDE VIENE TODO ═════════════════════════
pols = [('tragos-bartender', .55, .7, -8), ('lugar-barra', 2.55, .45, 5), ('quien-grupo-peter', 4.4, .85, -3),
        ('comida-pizza', .75, 3.1, 4), ('lugar-ojo-piojo', 2.8, 2.95, -6), ('eventos-fondita', 4.6, 3.3, 7),
        ('lugar-sillones', 1.0, 5.5, -4), ('carta-sangria', 3.15, 5.35, 3)]


def big(nm, cap):
    return f'<div class="bign"><b>{nm}</b><span>{cap}</span></div>'


lam(RJ, ''.join(pol(k, x, y, 1.85, r) for k, x, y, r in pols) +
    box(6.85, .6, 5.7, f'''<p class="k" style="color:rgba(255,255,255,.85)">De dónde viene todo</p>
  <h2 class="t" style="color:#fff">Todo esto <em style="color:{AM}">ya</em> era suyo</h2>
  <div class="bigs">{big(N_POSTS, f"publicaciones de su Instagram leídas completas, de las {N_PUB} de su perfil")}{big(N_ITEMS, f"tragos, platos y bebidas de sus {N_SECC} secciones de carta, al pie de la letra")}{big(N_REV, f"reseñas de sus clientes en Tripadvisor y Google; en el sitio, las {N_RES_SITIO} que dicen su país")}{big(N_FOTOS, f"fotos suyas y {N_VIDEOS} videos, de {N_POSTS_USADOS} publicaciones")}</div>
  <p class="p" style="color:#fff">Cada texto del sitio tiene su origen identificado: qué post, qué línea de la bio, qué carta o qué reseña. Lo único que no sale de sus publicaciones son las indicaciones de uso, como «Ver la carta» o «Escríbenos por DM», las ayudas en inglés para el turista y la referencia «Al frente del Centro Cultural de Castro», que es como los ubican las guías de viaje.</p>'''),
    nc='rgba(255,255,255,.7)')

# ═════════════════════════ 04 · LA MARCA ═════════════════════════
stripes = [('amarillo', 'Amarillo cinta', NE), ('rosa', 'Rosa muro', NE), ('naranja', 'Naranja cinta', NE), ('verde', 'Verde cinta', CR),
           ('lila', 'Lila cinta', NE), ('rojo', 'Rojo cinta', CR), ('crema', 'Crema', NE), ('negro', 'Negro', CR), ('azul', 'Azul letrero', NE)]
sth = ''.join(f'<div class="stripe" style="background:{C[k]};color:{fg}"><span class="sn">{nm}</span><span class="sh">{C[k]}</span></div>' for k, nm, fg in stripes)
lam(CR, f'<div class="stripes">{sth}</div>' +
    f'<img class="abs" src="{LOGO_O}" style="left:.55in;top:.5in;width:2.3in" alt="">' +
    box(.55, 1.35, 6.9, f'''<p class="k" style="color:{TN}">La marca · voz, letra y color</p>
  <p class="spa">Somos inquietos</p><p class="spb">y nos gusta el</p><p class="spa" style="color:{RO}">colorssss!</p>
  <p class="cap2">Así lo dicen ustedes · {IG("IG-111")}</p>''') +
    box(.55, 4.7, 6.9, f'''<div class="cols3">
  <div><h4 style="color:{TN}">Voz</h4><p>Viene de cómo escriben en Instagram: de usté, invitando, con juegos de palabras. Las cascadas como «ito ito», los «Besi» y las frases de carrete se quedan en Instagram, donde todos los conocen; la única que entra es la frase de Elymar, escrita así por ustedes.</p></div>
  <div><h4 style="color:{VE}">Letra</h4><p>Viene de su letrero y sus afiches: Big Shoulders Display, alta, angosta y gruesa como el «BAR», para gritar; Barlow Condensed, igual de angosta, para leer.</p></div>
  <div><h4 style="color:{TN}">Color</h4><p>Viene del techo de cintas, del muro rosa y del letrero azul. Cada sección tiene su cinta, y el texto se lee con holgura sobre cada una.</p></div></div>'''))

# ═════════════════════════ 05 · RECORRIDO ═════════════════════════
actos = [('d-apertura', 'Entrar', 'Su almud se dibuja, abre la boca y deja ver su letrero, con la frase con que abre su bio y «Ver la carta».', -3),
         ('d-tragos-peter', 'Pedir', 'Sus seis rincones; el Peter con su humo; tragos y platos con el nombre y el precio de su carta.', 2),
         ('d-quien-b', 'Celebrar', 'La baraja de su gente, sus fiestas de cada temporada y el equipo con sus frases.', -2),
         ('d-cierre-a', 'Volver', 'Reseñas en su idioma y su firma de cierre, con el día, la hora, el mapa y el DM.', 3)]
ah = ''
for i, (s_, t_, p_, r_) in enumerate(actos):
    x = .5 + i * 3.1
    ah += fr(s_, x, 3.2, 2.85, r_) + rombo(x + 2.0, 2.5, 1.1, AM, NE, f'<b class="rbn">{i + 1}</b>', z=5)
    ah += box(x, 5.45, 2.8, f'<h3 class="t3" style="color:#fff">{t_}</h3><p class="p" style="color:rgba(255,255,255,.9)">{p_}</p>')
lam(VE, box(.5, .6, 10, f'''<p class="k" style="color:rgba(255,255,255,.8)">El recorrido</p>
  <h2 class="t" style="color:#fff">Un viernes en Almud, <em style="color:{AM}">en</em> cuatro actos</h2>''') + ah,
    nc='rgba(255,255,255,.7)')

# ═════════════════════════ 06 · LA ESPERA Y LA PORTADA ═════════════════════════
lam(NE, fr('d-carga-2', .55, 2.3, 3.6, -3, lt=True) + fr('d-apertura', 3.0, 3.95, 4.7, 2, z=3, lt=True) + ph('m-hero', 8.05, 2.85, 1.75, -4, z=4) +
    rombo(3.55, 1.65, 1.15, RO, NE, '<span class="rbs">Al cien<br>por ciento</span>', fs=11, z=6) +
    box(.55, .55, 7.2, f'''<p class="k" style="color:{RO}">La espera y la portada</p>
  <h2 class="t" style="color:{CR}">El almud se abre <em style="color:{AZ}">y</em> aparece el bar</h2>''') +
    box(10.15, .6, 2.45, f'''<p class="p" style="color:{CR}">Su nombre es una medida chilota y su logo la dibuja, con la boca en rombo. Mientras carga la página, ese almud se traza sobre negro al ritmo de lo que va llegando, con el porcentaje debajo.</p>
  <p class="p" style="color:{CR}">Al completarse, la boca se abre y adentro ya corre su propio video: el letrero, la puerta, las cintas, los ojos, las lámparas y la terraza llena. Es el mismo en el celular y en el computador.</p>''') +
    box(10.15, 5.05, 2.45, Q('Hicimos este video pa contar un poquito de nuestro Almudcito!', IG('IG-061'), 'light') +
        f'<p class="p" style="color:{CR}">Encima, solo el logo, su presentación de Instagram y un botón: «Ver la carta».</p>'),
    nc='rgba(245,233,219,.55)')

# ═════════════════════════ 07 · EL LUGAR ═════════════════════════
rinc = ''.join(pill(n_, c_, f_) for n_, c_, f_ in [('Barra', NE, CR), ('Terraza techada', RO, NE), ('Sillones', VE, CR), ('Terraza', NA, NE), ('Lámparas', LI, NE), ('Ojo Piojo', RJ, CR)])
lam(AM, fr('d-lugar-c', 5.35, .6, 7.2, 1.5) + fr('d-lugar-b', 6.2, 4.6, 4.3, -2.5, z=3) + ph('m-lugar-c', 10.9, 3.9, 1.6, 4, z=4) +
    box(.55, .55, 4.6, f'''<p class="k" style="color:{TN}">El lugar</p>
  <h2 class="t">Seis rincones, <em style="color:{TN}">una</em> frase cada uno</h2>
  <div class="pills">{rinc}</div>''') +
    box(.55, 3.3, 4.55, Q('Pucha que nos gusta nuestra barrita!', 'Barra · ' + IG('IG-087')) + Q('Felices, con el corazón llenifer!', 'Sillones · ' + IG('IG-009')) +
        Q('una mirada vale más que mil palabras', 'Ojo Piojo · ' + IG('IG-118')) +
        '''<p class="p">Su feed recorre el local de rincón en rincón, y cada rincón ya tenía su frase. Aquí se pasan con el dedo, como sus carruseles, y cada foto se balancea como las cintas del techo. Arriba, tres fotos de las salas repletas.</p>
  <p class="p sm">En Barra queda un solo signo de exclamación; en Sillones, «corazón» reemplaza al emoji del original.</p>'''))

# ═════════════════════════ 08 · TRAGOS ═════════════════════════
tragos = ''.join(pill(f'{n_} · {p_}', c_, f_) for n_, p_, c_, f_ in [
    ('Sagüer on Faia', '$ 7.900', NE, CR), ('Sangría Foreva!', '$ 6.500', CR, NE), ('Cómo te voy a olvidar', '$ 6.800', NE, CR),
    ('A veces me pongo Coquette', '$ 7.100', CR, NE), ('La moto chantá', '$ 6.400', AM, NE)])
lam(RO, fr('d-tragos-peter', .5, .55, 7.6, -1.5) + ph('m-tragos-c', 7.25, 4.1, 1.6, 5, z=4) +
    rombo(6.6, .15, 1.25, AM, NE, '<span class="rbs">$ 6.700</span>', fs=15, z=6) +
    box(8.75, .6, 3.85, f'''<p class="k" style="color:{TN}">La barra</p>
  <h2 class="t">El Peter <em style="color:{RO}">abre</em> la barra</h2>
  {Q("Aquí te las traigo Peter!", IG("IG-044"))}
  <p class="p">Su post lo presentó con un grito, y así entra: grande, con su burbuja de humo en movimiento y el nombre armándose letra por letra. Al lado, la barra en columnas que parten a distinta altura, como su feed de collage.</p>''', 'card', f'background:{CR};') +
    box(.55, 6.45, 6.4, f'<p class="k" style="color:{NE}">Y cinco más de su carta: cuatro de la casa y un mocktail</p><div class="pills">{tragos}</div>'),
    nc='rgba(14,12,11,.55)')

# ═════════════════════════ 09 · COMIDA ═════════════════════════
lam(NA, plato('carta-tukulito', .75, 2.95, 1.8, 'Tukulito Sakayama', '$ 15.900', -6) + plato('comida-ceviche', 2.85, 2.7, 1.8, 'Todo que ver!', '$ 16.000', 5) +
    plato('comida-hamburguesa', 4.95, 3.05, 1.8, 'Chambreao', '$ 10.900', -3) + plato('carta-contuti', 1.8, 5.45, 1.8, 'Con tuti si no pa qué!', '$ 19.900', 7) +
    plato('carta-camaron', 3.95, 5.5, 1.8, 'Camarón que se duerme', '$ 15.900', -5) +
    fr('d-comida-a', 7.2, .6, 5.35, 2) + ph('m-comida-b', 10.9, 3.95, 1.6, -4, z=4) +
    box(.55, .55, 6.3, f'''<p class="k" style="color:{NE}">La cocina</p>
  <h2 class="t">Platos que llegan <em style="color:{CR}">a la</em> mesa</h2>
  <p class="p">Como cuando se sirven, los platos entran girando un poco y su foto se abre en redondo. Cada video muestra el plato que nombra: el sartén es «La carne es débil» y el queso que se estira, «Una cosa poca».</p>''') +
    box(7.2, 4.4, 3.4, Q('Las masas de nuestras pizzas son hechas por nosotros!', 'Su carta · Comilona') +
        '<p class="p">Siete platos de su carta con nombre y precio literales, más sus pizzas. Los cuatro de abajo van en dos columnas que no se realinean: el orden del desorden.</p>'),
    nc='rgba(14,12,11,.55)')

# ═════════════════════════ 10 · LA GENTE Y SUS FIESTAS ═════════════════════════
baraja = [('con-quien-brindis', .6, 2.4, -9), ('quien-carcajadas', .8, 2.3, 6), ('quien-mesa-llena', .65, 2.35, -3), ('quien-grupo-peter', .75, 2.25, 4)]
fiestas = ''.join(pill(t_, c_, f_) for t_, c_, f_ in [('Aniversario · julio', AM, NE), ('Fondita · septiembre', RO, NE), ('Jalogüín · octubre', NA, NE)])
lam(VE, ''.join(pol(k, x, y, 3.2, r, z=2 + i) for i, (k, x, y, r) in enumerate(baraja)) +
    rombo(3.35, 5.75, 1.15, AM, NE, '<span class="rbs">Nunca<br>se acaba</span>', fs=11, z=7) +
    fr('d-eventos-a', 7.0, .6, 5.55, -2) + ph('m-eventos-b', 6.2, 3.45, 1.5, 4, z=4) +
    box(.55, .55, 6.2, f'''<p class="k" style="color:{AM}">Con quién y cuándo</p>
  <h2 class="t" style="color:#fff">Siempre lleno, <em style="color:{AM}">todo</em> el año</h2>''') +
    box(4.25, 1.85, 1.85, Q('Ya saben que no somos ná sin ustedes!', IG('IG-026'), 'light') +
        '<p class="p" style="color:#fff">«Faltan muuuchas más, pero no se pueden subir más de 20…», dice el mismo post. Sus carruseles de gente son aquí una baraja que se lanza con el dedo; la foto vuelve por debajo y la pila no se vacía. Al lado, tres videos de mesas llenas.</p>') +
    box(8.0, 4.75, 4.55, f'''<div class="pills">{fiestas}</div>
  <p class="p" style="color:#fff;margin-top:.12in">Las fiestas que vuelven cada año pasan solas, con su nombre enorme. Las de una sola vez y las campañas ajenas quedan fuera: nada que ustedes no hayan anunciado.</p>
  {Q("Se comió, se tomó, se bailó, quedamos con dolor de guata de tanto reír", IG("IG-072"), "light")}'''),
    nc='rgba(255,255,255,.7)')

# ═════════════════════════ 11 · EQUIPO ═════════════════════════
apodos = [('Barra', 'mente creadora de muchos cócteles'), ('Barra', 'la regia'), ('Barra', 'haciéndole los copetitos a usté'),
          ('Liz · Salones', 'la amada'), ('Salones', 'el ondero'), ('Elymar · Barra y salón', 'le pone una sonrisota con cada cóctecito ito ito')]
aph = ''.join(f'<div class="apodo"><span>{E(a)}</span><b>«{E(b)}»</b></div>' for a, b in apodos)
lam(RJ, fr('d-equipo-flip', .5, .6, 6.9, -1.5) + ph('m-equipo-flip', 6.0, 3.55, 1.6, 4, z=4) +
    box(.55, 5.3, 5.2, f'''<p class="qbig">«los papis del almud: el franchuto y la disharashera»</p>
  <p class="k" style="color:rgba(255,255,255,.75);margin-top:.08in">Así nombran a los dueños · {IG("IG-067")}</p>''') +
    box(8.05, .55, 4.5, f'''<p class="k" style="color:{AM}">El equipo</p>
  <h2 class="t" style="color:#fff">Cada uno <em style="color:{AM}">en</em> su lugar</h2>
  <p class="p" style="color:#fff">Ustedes presentan al equipo con cariño y por su lugar en el bar: «en esa barra…», «por los salones…». Cada tarjeta se da vuelta al tocarla y muestra justo eso, con la frase que ustedes le dedicaron.</p>
  <div class="apodos">{aph}</div>
  <p class="p" style="color:#fff">El sitio habla por el local: no enlaza perfiles personales, ni del equipo ni de ustedes. El video con ustedes dos vive aquí, para que la portada sea del bar.</p>
  <p class="p sm" style="color:rgba(255,255,255,.8)">Frases publicadas el {FECHA("IG-045")}, {FECHA("IG-067")}, {FECHA("IG-034")} y {FECHA("IG-001")}. La de Elymar va en singular; el original dice «le ponen». Del post de los dueños se omiten sus cuentas. Elymar aparece etiquetada en el post del {FECHA("IG-001")}.</p>'''),
    nc='rgba(255,255,255,.7)')

# ═════════════════════════ 12 · RESEÑAS Y DESPEDIDA ═════════════════════════
paises = ''.join(pill(f'{PAISES[k]} · {v}', c_, f_) for (k, v), c_, f_ in zip(N_PAIS.items(), (VE, AZ, LI), (CR, NE, NE)))
lam(CR, cintas(0, 13, 0, 60, .5) + '<p class="qq" style="left:.35in;top:.5in">“</p>' +
    box(.6, 1.7, 5.9, f'''<p class="qbig" style="color:{NE}">Estuve ahí cada día de mi estancia, porque es imposible no volver.</p>
  <p class="k" style="color:{TN};margin-top:.1in">arqggodoy · Iquique, Chile · Tripadvisor</p>
  <h2 class="t" style="margin-top:.28in">Diez voces <em style="color:{RO}">y</em> una despedida</h2>
  <div class="pills">{paises}</div>
  <p class="p" style="margin-top:.14in">Sus clientes hablan de la terraza, de la atención, de la música y de encontrar «un vrai bar». En el sitio van las reseñas que dicen de dónde venía quien escribió, cada una en su idioma, en dos cintas que pasan solas.</p>
  <p class="p">Al final, su despedida de siempre en grande. Al lado, «Le esperamos desde las 18:00 hrs» se escribe en vivo, con los días y la dirección de su bio, el mapa y un solo botón: escribirles por DM, porque así conversan ustedes. No hay «Reservar».</p>''') +
    fr('d-resenas', 7.0, 1.0, 5.55, 2) + fr('d-cierre-b', 7.25, 4.75, 5.3, -2, z=3, crop=.56) +
    rombo(11.55, 3.6, 1.25, RO, NE, '<span class="rbs">Usté se lo<br>merece!</span>', fs=10.5, z=6))

# ═════════════════════════ 13 · DETALLES ═════════════════════════
dcol = [RO, AM, VE, LI, AZ]
phs = ''.join(ph(k, .65 + i * 2.45, .5 + (0, .3, 0, .3, 0)[i], 2.05, (-4, 3, -2, 4, -3)[i]) for i, k in enumerate(['m-carta', 'm-en-lugar', 'm-tragos-c', 'm-equipo-b', 'm-resenas']))
dots = ''.join(f'<div class="dot" style="left:{.45 + i * 2.45}in;top:{1.4 + (0, .3, 0, .3, 0)[i]}in;background:{c_}"></div>' for i, c_ in enumerate(dcol))
det = [('La carta, aparte', f'Sus {N_ITEMS} ítems, tal como en su carta impresa, en una página propia. Las siete pestañas se ven siempre completas, cada una con el color de una cinta, y cada trago o plato del inicio abre su sección de la carta.', RO),
       ('Español e inglés', 'Un botón «EN» arriba. Sus frases y los nombres de la carta no se traducen: llevan debajo una ayuda para el turista, con el mismo humor.', AM),
       ('Videos que no paran', 'Corren solos desde que se ven y siguen corriendo al bajar por la página. Los de la sección siguiente ya están listos al llegar.', VE),
       ('Con el dedo', 'Rincones, tragos, baraja, tarjetas y reseñas se mueven con el dedo, y deslizar hacia abajo siempre mueve la página. Con el movimiento reducido, todo queda quieto y completo.', LI)]
deth = ''.join(box(.55 + i * 3.1, 5.75, 2.85, f'<div class="bar" style="background:{c_}"></div><h3 class="t4" style="color:{CR}">{t_}</h3><p class="p" style="color:rgba(245,233,219,.88)">{p_}</p>') for i, (t_, p_, c_) in enumerate(det))
lam(NE, dots + phs + deth, nc='rgba(245,233,219,.55)')

# ═════════════════════════ 14 · CIERRE ═════════════════════════
k14 = nx()
L.append(f'''<article class="lam" style="background:{NE}"><img class="bleed" src="{med("lugar-terraza-repleta", 1950, q=82)}" style="object-position:50% 50%" alt="">''' +
         box(6.75, .5, 5.75, f'''<img class="mk" src="{ISO_O}" alt="">
  <p class="k" style="color:{TN}">Lo que sigue</p><h2 class="t">Hacerlo <em style="color:{RO}">suyo</em></h2>
  <p class="p">Este sitio se hizo solo con lo que ya estaba publicado. Con un par de conversaciones podría ir mucho más lejos:</p>
  <ul class="next"><li>Fotografía propia de cada rincón, como los sillones llenos de gente, y de ustedes dos</li>
    <li>Sus videos originales en alta, horizontales y verticales, para una portada aún más nítida</li>
    <li>Dominio propio .cl y alojamiento a nombre de Almud</li>
    <li>La carta y las fiestas del año al día, actualizadas desde el mismo sitio</li></ul>
  <p class="invite">Cuando quieran, lo conversamos.</p>
  <p class="who">Pablo Figueroa G.</p><p class="role">Director de estudio</p>
  <p class="contact"><a href="mailto:pablo@bergerac.cl">pablo@bergerac.cl</a> · <a href="tel:+56975892096">+56 9 7589 2096</a></p>
  <p class="link"><a href="https://bergerac.cl">Bergerac.cl</a></p>''', 'card', f'background:{CR};padding:.45in .5in;') +
         f'<span class="no" style="color:rgba(255,255,255,.75)">{k14:02d}</span></article>')

# ═════════════════════════ CSS ═════════════════════════
CSS = f'''
@font-face{{font-family:"BSD";src:url({font("big-shoulders-display-latin-wght-normal")}) format("woff2");font-weight:100 900}}
@font-face{{font-family:"BC";font-weight:400;src:url({font("barlow-condensed-latin-400-normal")}) format("woff2")}}
@font-face{{font-family:"BC";font-weight:500;src:url({font("barlow-condensed-latin-500-normal")}) format("woff2")}}
@font-face{{font-family:"BC";font-weight:600;src:url({font("barlow-condensed-latin-600-normal")}) format("woff2")}}
@page{{size:13in 8.5in;margin:0}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{background:#3a3532}}
body{{font-family:"BC","Arial Narrow",sans-serif;font-weight:500;color:{NE};-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.lam{{width:13in;height:8.5in;overflow:hidden;margin:0 auto .3in;position:relative;page-break-after:always;break-after:page}}
@media print{{html,body{{background:none}}.lam{{margin:0}}}}
.bleed{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}}
.abs{{position:absolute;display:block;z-index:4}}
.spread-tab{{position:absolute;left:0;top:.45in;background:#fff;opacity:.75;padding:.2in .36in .2in .5in;border-radius:0 .18in .18in 0}}
.spread-logo{{width:1.9in;display:block}}
.no{{position:absolute;right:.4in;bottom:.28in;font-weight:600;font-size:7.5pt;letter-spacing:.2em;z-index:20}}
.tx{{position:absolute;z-index:4}}
.tx.tag{{text-align:center;z-index:5}}
.card{{border-radius:.22in;padding:.3in .34in;box-shadow:0 10pt 30pt rgba(0,0,0,.2)}}
.k{{font-weight:600;font-size:8pt;letter-spacing:.24em;text-transform:uppercase;margin-bottom:.1in}}
.t{{font-family:"BSD";font-weight:800;font-size:40pt;line-height:.95;text-transform:uppercase;margin-bottom:.18in}}
.t em{{font-style:normal}}
.t3{{font-family:"BSD";font-weight:800;font-size:26pt;text-transform:uppercase;margin-bottom:.05in}}
.t4{{font-family:"BSD";font-weight:800;font-size:19pt;text-transform:uppercase;margin:.1in 0 .05in}}
.p{{font-size:10.6pt;line-height:1.42;margin-bottom:.08in}}
.p.sm{{font-size:9pt;color:{GR}}}
.q2{{margin:.04in 0 .1in}}
.q2 p{{font-family:"BSD";font-weight:700;font-size:13.5pt;line-height:1.08;text-transform:uppercase;margin-bottom:3pt}}
.q2 cite{{font-style:normal;font-weight:600;font-size:7.4pt;letter-spacing:.16em;text-transform:uppercase;color:{TN}}}
.q2.light p{{color:#fff}}.q2.light cite{{color:rgba(255,255,255,.8)}}
.letter p{{font-size:13.2pt;line-height:1.45;margin-bottom:.12in}}
.sign{{font-family:"BSD";font-weight:800;font-size:16pt;text-transform:uppercase;letter-spacing:.04em}}
.seal{{position:absolute;z-index:6;filter:drop-shadow(0 8pt 18pt rgba(0,0,0,.25))}}
.pic{{position:absolute;overflow:hidden;box-shadow:0 12pt 34pt rgba(0,0,0,.22)}}
.pic img{{width:100%;height:100%;object-fit:cover;display:block}}
.fr{{position:absolute;border-radius:8pt;overflow:hidden;box-shadow:0 14pt 34pt rgba(0,0,0,.32);background:#111}}
.fr img{{width:100%;display:block}}
.fr.lt{{outline:2.5pt solid rgba(245,233,219,.45);outline-offset:-2.5pt}}
.ph{{position:absolute;border-radius:16pt;overflow:hidden;border:4pt solid #111;box-shadow:0 14pt 30pt rgba(0,0,0,.35);background:#111}}
.ph img{{width:100%;display:block;border-radius:12pt}}
.rb{{position:absolute;display:flex;align-items:center;justify-content:center;text-align:center}}
.rb-bg{{position:absolute;inset:14%;transform:rotate(45deg);border-radius:6pt;box-shadow:0 8pt 20pt rgba(0,0,0,.25)}}
.rb>div{{position:relative;font-family:"BSD";font-weight:800;text-transform:uppercase;line-height:.98}}
.rbn{{font-size:30pt;font-weight:800}}
.rbs{{display:block}}
.pol{{position:absolute;background:#fff;padding:.08in .08in .3in;box-shadow:0 10pt 24pt rgba(0,0,0,.32)}}
.pol img{{width:100%;aspect-ratio:1;object-fit:cover;display:block}}
.plato{{position:absolute;border-radius:50%;overflow:hidden;border:5pt solid {CR};box-shadow:0 12pt 26pt rgba(0,0,0,.3);z-index:2}}
.plato img{{width:100%;height:100%;object-fit:cover;display:block}}
.bigs{{display:grid;grid-template-columns:1fr 1fr;gap:.14in .3in;margin:.04in 0 .2in}}
.bign b{{display:block;font-family:"BSD";font-weight:800;font-size:58pt;line-height:.95;color:{AM}}}
.bign span{{display:block;font-size:10pt;line-height:1.3;color:#fff;margin-top:.03in}}
.stripes{{position:absolute;right:0;top:0;bottom:0;width:5.1in;display:flex}}
.stripe{{flex:1;position:relative}}
.stripe .sn{{position:absolute;left:50%;top:.55in;transform:translateX(-50%) rotate(180deg);writing-mode:vertical-rl;font-weight:600;font-size:9pt;letter-spacing:.2em;text-transform:uppercase;white-space:nowrap}}
.stripe .sh{{position:absolute;left:0;right:0;bottom:.55in;font-weight:600;font-size:7pt;letter-spacing:.06em;writing-mode:vertical-rl;transform:rotate(180deg);display:flex;align-items:center;width:100%}}
.spa{{font-family:"BSD";font-weight:800;font-size:66pt;line-height:.92;text-transform:uppercase}}
.spb{{font-family:"BSD";font-weight:800;font-size:34pt;line-height:1;text-transform:uppercase;color:{TN};margin:.02in 0}}
.cap2{{font-weight:600;font-size:8pt;letter-spacing:.18em;text-transform:uppercase;color:{GR};margin-top:.16in}}
.cols3{{display:grid;grid-template-columns:repeat(3,1fr);gap:.28in}}
.cols3 h4{{font-family:"BSD";font-weight:800;font-size:19pt;text-transform:uppercase;margin-bottom:.05in}}
.cols3 p{{font-size:10pt;line-height:1.42}}
.pills{{display:flex;flex-wrap:wrap;gap:6pt}}
.pill{{display:inline-block;padding:5pt 11pt;border-radius:999px;font-family:"BSD";font-weight:700;font-size:10.5pt;letter-spacing:.02em;text-transform:uppercase;box-shadow:0 3pt 8pt rgba(0,0,0,.12)}}
.apodos{{display:grid;grid-template-columns:1fr 1fr;gap:6pt;margin:.06in 0 .14in}}
.apodo{{background:{NE};color:{CR};border-radius:6pt;padding:6pt 9pt}}
.apodo span{{display:block;font-weight:600;font-size:7.4pt;letter-spacing:.18em;text-transform:uppercase;color:{AM}}}
.apodo b{{display:block;font-family:"BSD";font-weight:700;font-size:11pt;line-height:1.05;text-transform:uppercase}}
.qq{{position:absolute;font-family:"BSD";font-weight:800;font-size:170pt;line-height:1;color:{RO};z-index:1}}
.qbig{{font-family:"BSD";font-weight:800;font-size:26pt;line-height:1.02;text-transform:uppercase;color:#fff}}
.cinta{{position:absolute;display:block;border-radius:0 0 2pt 2pt;z-index:1}}
.dot{{position:absolute;width:2.6in;height:2.6in;border-radius:50%;opacity:.95;z-index:1}}
.bar{{width:.6in;height:4pt;border-radius:2pt}}
.mk{{width:.5in;display:block;margin-bottom:.14in}}
.next{{list-style:none;margin:.04in 0 .18in}}
.next li{{font-size:10.6pt;line-height:1.4;padding:5pt 0;border-bottom:.5pt solid rgba(14,12,11,.2)}}
.invite{{font-size:14pt;font-style:italic;margin-bottom:.06in}}
.who{{font-family:"BSD";font-weight:800;font-size:12pt;letter-spacing:.16em;text-transform:uppercase}}
.role{{font-size:10pt}}
.contact{{font-size:9pt;color:{GR}}}
.card a{{color:inherit;text-decoration:none}}
.link{{font-family:"BSD";font-weight:800;font-size:20pt;letter-spacing:.12em;text-transform:uppercase;color:{RO};margin-top:.1in}}
'''

DOC = f'''<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Almud Bar · Decisiones de diseño del sitio web</title><style>{CSS}</style></head>
<body>{''.join(L)}</body></html>'''
out = D / 'almud-dossier-diseno.html'
out.write_text(DOC, encoding='utf-8')
print('ok', len(L), 'láminas', round(len(DOC) / 1e6, 1), 'MB',
      dict(fotos=N_FOTOS, videos=N_VIDEOS, posts_usados=N_POSTS_USADOS, posts=N_POSTS, items=N_ITEMS, rev=N_REV, rev_sitio=N_RES_SITIO, paises=N_PAIS))
