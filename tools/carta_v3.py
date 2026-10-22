#!/usr/bin/env python3
"""Carta v3 (fase 14): genera v3/carta/index.html desde content/carta-v2.json.
Nombres, descripciones y precios literales. Rutas relativas desde /v3/carta/.
Uso: python3 tools/carta_v3.py"""
import json, html, pathlib, re, hashlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
C = json.loads((ROOT / 'content/carta-v2.json').read_text())
M = json.loads((ROOT / 'assets/v3/media.json').read_text())
E = html.escape
UP = '../../'
SITE = 'https://almudbar.pages.dev'
SEC = {s['id']: s for s in C['secciones']}


def ver(*ps):
    h = hashlib.md5()
    for q in ps:
        h.update((ROOT / q).read_bytes())
    return h.hexdigest()[:8]


def slug(t):
    t = t.lower()
    for a, b in zip('áéíóúüñ', 'aeiouun'):
        t = t.replace(a, b)
    return re.sub(r'[^a-z0-9]+', '-', t).strip('-')


# pestañas: (id, título ES literal, glosa EN, secciones que reúne, color de fondo)
TABS = [
    ('casa', 'Coctelería de la casa', 'House cocktails', ['cocteleria-de-la-casa'], 'muro'),
    ('mundo', 'Cócteles del mundo mundial', 'World classics', ['cocteles-del-mundo-mundial'], 'muro'),
    ('espirituosos', 'Espirituosos', 'Spirits', ['espirituosos'], 'papel'),
    ('vinos', 'Vinos & espumantes', 'Wines', ['vinos-espumantes'], 'muro'),
    ('sin', 'Mocktails sin alcohol', 'Alcohol-free', ['mocktails-sin-alcohol', 'jugos-bebidas', 'cervezas-sin-alcohol', 'bebidas-calientes'], 'papel'),
    ('comilona', 'Comilona', 'Food', ['comilona'], 'dorado'),
    ('promos', 'Nuestras promos', 'Deals', ['nuestras-promos'], 'dorado'),
]
GL = {'Tintelis': '[reds]', 'Blanquelis': '[whites]', 'Whiscachos': '[whiskies]', 'Ron poromponpon': '[rum]',
      'Vodkita': '[vodka]', 'Pa los chichichos': '[kids]', 'Somos dulzones': '[desserts]',
      'Jugos & bebidas': 'Juices & soft drinks', 'Cervezas sin alcohol': 'Alcohol-free beers', 'Bebidas calientes': 'Hot drinks'}
CHIP_EN = {'Clásicos': 'Classics', 'Vermú': 'Vermouth', 'Sagüer': 'Sours', 'Tintelis': 'Reds', 'Blanquelis': 'Whites',
           'Espumantes': 'Sparkling', 'Por copa': 'By the glass', 'Mocktails de la casa': 'House mocktails',
           'Mocktails clásicos': 'Classic mocktails', 'Jugos & bebidas': 'Juices & soft drinks', 'Cervezas sin alcohol': 'Alcohol-free beers',
           'Bebidas calientes': 'Hot drinks', 'Picoteos': 'Small plates', 'Greditas': 'Clay pots', 'Sanguches': 'Sandwiches',
           'Pizzas artesanales': 'Pizzas', 'Pa los chichichos': 'Kids', 'Somos dulzones': 'Desserts', 'Whiscachos': 'Whiskies',
           'Ron poromponpon': 'Rum', 'Vodkita': 'Vodka', 'Amamos el GIN!': 'Gin', 'Tequilazos & mezcalazos': 'Tequila & mezcal',
           'Piscolein o combinadito': 'Pisco & mixers'}
NOTA_EN = {'Precio del corto normal o XL\nNO INCLUYE BEBIDA': 'Single or XL pour · mixer not included',
           'Elija su medida 90 o 150 cc!': 'Choose 90 or 150 cc',
           'Los whiscachos no incluyen bebida pal que le guste tomarlo puritano': '[No mixer included]',
           'de 18:00 a 22:00 hrs': '6 to 10 pm · Always subject to stock!'}
DAY_EN = {'Martes': 'Tue', 'Miércoles': 'Wed', 'Jueves': 'Thu', 'Sábado': 'Sat', 'Viernes': 'Fri', 'Lunes': 'Mon'}
TAG = {'nuevo': ('Nuevo', 'New'), 'veggie': ('Veggie', 'Veggie'), 'vegan': ('Vegan', 'Vegan'), 'picante': ('Picante', 'Spicy')}

# fotos propias por ítem (media.json carta-*), y el loop de Peter
PHOTO = {}
for k, im in M['images'].items():
    if k.startswith('carta-'):
        PHOTO[im.get('item') or im.get('rincon') or ''] = k
NAMEMAP = {'carta-olvidar': 'Cómo te voy a olvidar', 'carta-saguer': 'Sagüer on Faia', 'carta-sangria': 'Sangría Foreva!',
           'carta-coquette': 'A veces me pongo Coquette', 'carta-moto': 'La moto chantá', 'carta-tukulito': 'Tukulito Sakayama',
           'carta-contuti': 'Con tuti si no pa qué!', 'carta-camaron': 'Camarón que se duerme'}
BYNAME = {v: k for k, v in NAMEMAP.items()}


def srcset(files, kind):
    return ', '.join(f"{UP}{v['path']} {w}w" for w, v in sorted(files[kind].items(), key=lambda kv: int(kv[0])))


def pic(id_):
    im = M['images'][id_]
    c = im['crops']['a']
    f = c['files']
    ws = sorted(int(x) for x in f['webp'])
    fb = next((x for x in ws if x >= 360), ws[-1])
    sz = '(min-width:1024px) 160px, 104px'
    return (f'<figure class="m pr__m" style="--ar:{c["width"]}/{c["height"]};--c:{c["color"]};--lq:url({c["lqip"]})">'
            f'<picture><source type="image/avif" srcset="{srcset(f, "avif")}" sizes="{sz}"><source type="image/webp" srcset="{srcset(f, "webp")}" sizes="{sz}">'
            f'<img src="{UP}{f["webp"][str(fb)]["path"]}" width="{c["width"]}" height="{c["height"]}" alt="{E(im["alt"]["es"])}" data-alt-en="{E(im["alt"]["en"])}" loading="lazy" decoding="async"></picture></figure>')


def peter():
    v = M['videos']['tragos-humo']
    return (f'<figure class="m m--v pr__m" style="--ar:{v["width"]}/{v["height"]};--c:{v["color"]};--lq:url({v["lqip"]})">'
            f'<video class="v" autoplay muted loop playsinline preload="none" width="{v["width"]}" height="{v["height"]}" data-poster="{UP}{v["poster"]["webp"]["path"]}"'
            f' data-webm="{UP}{v["files"]["webm"]["path"]}" data-mp4="{UP}{v["files"]["mp4"]["path"]}" aria-label="{E(v["alt"]["es"])}" data-aria-en="{E(v["alt"]["en"])}"></video>'
            f'<noscript><img class="v" src="{UP}{v["poster"]["webp"]["path"]}" width="{v["width"]}" height="{v["height"]}" alt="{E(v["alt"]["es"])}"></noscript></figure>')


def g(en, cls='gloss'):
    return f'<span class="{cls}" lang="en">{E(en)}</span>'


def nl(t):
    return '<br>'.join(E(x) for x in t.split('\n'))


# negritas de la carta impresa (tools/carta_negritas_v3.py): solo frases de ingredientes, sin precios ni cabeceras
GLOSA_EN = {k: v for k, v in json.loads((ROOT / 'content/carta-glosas-en-v3.json').read_text()).items() if not k.startswith('_')}
NEG_STOP = {'hasta', 'años', 'para menores'}
NEG_FIX = {'Especial pa': 'Especial pa compartir'}  # la línea siguiente del PDF ('compartir:') sigue en negrita
NEG = {k: sorted({NEG_FIX.get(x, x) for x in v if not re.search(r'\d', x) and x != x.upper() and x.lower() not in NEG_STOP}, key=len, reverse=True)
       for k, v in json.loads((ROOT / 'content/carta-negritas-v3.json').read_text()).items()}
CUR_SRC = ['']


def bold(desc):
    h = nl(desc)
    for ph in NEG.get(CUR_SRC[0], []):
        h = re.sub(r'(?<![\w>])(' + re.escape(E(ph)) + r')(?![\w<])', r'<b>\1</b>', h, count=1)
    return h


def item(it, cols):
    n = it['nombre']
    media = peter() if n == 'Aquí te las traigo Peter' else (pic(BYNAME[n]) if n in BYNAME else '')
    tags = ''.join(f'<span class="tag tag--{t}" data-en="{TAG[t][1]}">{TAG[t][0]}</span>' for t in it.get('tags', []))
    if 'precios' in it:
        pr = '<span class="pr__ps">' + ''.join(
            f'<span class="pr__p"><span class="pr__c">{E(c)}</span>{E(it["precios"].get(c, "–"))}</span>' for c in cols) + '</span>'
    else:
        pr = f'<span class="pr__p">{E(it.get("precio", ""))}</span>'
    extra = ''
    if it.get('dia'):
        extra += f'<span class="pr__dia" data-en="{DAY_EN.get(it["dia"], it["dia"])}">{E(it["dia"])}</span>'
    meta = ''
    if it.get('bodega') or it.get('nota'):
        meta = '<p class="pr__meta">' + ' · '.join(E(x) for x in [it.get('bodega'), it.get('nota')] if x) + '</p>'
    desc = f'<p class="pr__d">{bold(it["desc"])}</p>' if it.get('desc') else ''
    if n in GLOSA_EN:
        desc += g(GLOSA_EN[n], 'gloss gloss--s pr__g')
    return (f'<li class="pr{" pr--img" if media else ""}">{media}<div class="pr__t">{extra}'
            f'<h4 class="pr__n">{E(n)}{tags}</h4>{meta}{desc}</div>{pr}</li>')


def group(gr, sid, idx):
    t = gr.get('titulo')
    cols = gr.get('columnas', [])
    gid = f'{sid}-{slug(t)}' if t else f'{sid}-{idx}'
    head = ''
    if t:
        lvl = 'h4' if gr.get('padre') else 'h3'
        head = f'<{lvl} class="gr__t{" gr__t--sub" if gr.get("padre") else ""}">{E(t)}</{lvl}>' + (g(GL[t], 'gloss gloss--s') if t in GL else (g(CHIP_EN[t], 'gloss gloss--s') if t in CHIP_EN else ''))
    nota = (f'<p class="gr__nota">{nl(gr["nota"])}' + (g(NOTA_EN[gr["nota"]], 'gloss gloss--s') if gr["nota"] in NOTA_EN else '') + '</p>') if gr.get('nota') else ''
    pie = (f'<p class="gr__pie">{nl(gr["nota_pie"])}' + (g(NOTA_EN[gr["nota_pie"]], 'gloss gloss--s') if gr["nota_pie"] in NOTA_EN else '') + '</p>') if gr.get('nota_pie') else ''
    if cols:
        th = ''.join(f'<th scope="col" class="tbl__c">{E(c).replace(" [", "<br>[", 1)}</th>' for c in cols)
        rows = ''
        for it in gr['items']:
            d = f'<span class="pr__d">{bold(it["desc"])}</span>' if it.get('desc') else ''
            tags = ''.join(f'<span class="tag tag--{t}" data-en="{TAG[t][1]}">{TAG[t][0]}</span>' for t in it.get('tags', []))
            rows += (f'<tr><th scope="row"><span class="pr__n">{E(it["nombre"])}{tags}</span>{d}</th>'
                     + ''.join(f'<td class="tbl__p">{E(it.get("precios", {}).get(c, "–"))}</td>' for c in cols) + '</tr>')
        body = (f'<table class="tbl"><thead><tr><th scope="col"><span class="sr-only" data-en="Name">Nombre</span></th>{th}</tr></thead>'
                f'<tbody>{rows}</tbody></table>')
    else:
        body = '<ul class="prs">' + ''.join(item(i, cols) for i in gr['items']) + '</ul>'
    return gid, (f'<div class="gr" id="{gid}">{head}{nota}{body}{pie}</div>')


panels, chipcss = [], []
for tid, ttl, en, sids, col in TABS:
    chips = []      # (id, título)
    blocks = []     # (chip_id, html)
    cur = None
    for sid in sids:
        s = SEC[sid]
        CUR_SRC[0] = s.get('fuente', '')
        multi = len(sids) > 1
        for i, gr in enumerate(s['grupos']):
            gid, h = group(gr if (gr.get('titulo') or not multi) else {**gr, 'titulo': s['titulo']}, sid, i)
            if gr.get('padre') and cur:
                blocks[-1] = (cur, blocks[-1][1] + h)
                continue
            title = gr.get('titulo') or (s['titulo'] if multi else None)
            if title:
                chips.append((gid, title))
                cur = gid
            blocks.append((gid if title else None, h))
    if s.get('intro'):
        pass
    use_chips = len(chips) > 1
    chip_html = ''
    if use_chips:
        chip_html = (f'<div class="chips" data-chips="{tid}"><div class="chips__in">' + ''.join(
            f'<a class="chip" href="#{c}" data-sub="{c}" id="chip-{c}"' + (f' data-en="{E(CHIP_EN[t])}"' if t in CHIP_EN else '') + f'>{E(t)}</a>' for c, t in chips) + '</div></div>')
        for c, _ in chips[1:]:
            pass
        first = chips[0][0]
        chipcss.append(f'html.js:not([data-sub-{tid}]) #{tid} .sub:not([data-sub="{first}"]){{display:none}}')
        chipcss += [f'html.js[data-sub-{tid}="{c}"] #{tid} .sub:not([data-sub="{c}"]){{display:none}}' for c, _ in chips]

    body = ''.join(f'<div class="sub" data-sub="{c}">{h}</div>' if (use_chips and c) else h for c, h in blocks)
    panels.append(f'<section class="panel" id="{tid}" data-bg="{col}" aria-labelledby="tab-{tid}">'
                  f'<h2 class="panel__t">{E(ttl)}</h2>{chip_html}{body}</section>')

tabcss = [f'html.js[data-tab="{t[0]}"] .panel:not(#{t[0]}){{display:none}}' for t in TABS]
tabcss += [f'html.js[data-tab="{t[0]}"] #tab-{t[0]}{{color:var(--noche);background:var(--papel)}}' for t in TABS]
tabcss += [f'html.js[data-tab="{t[0]}"] .panels{{--hoja:var(--hoja-{t[4]})}}' for t in TABS]

tabs_html = ''.join(f'<a class="tab" id="tab-{t[0]}" href="#{t[0]}" data-tab="{t[0]}" data-en="{E(t[2])}">{E(t[1])}</a>' for t in TABS)
nav = (M and (ROOT / 'brand/v3/almud-nav-claro.svg').read_text().strip())
nav = re.sub(r'<title>.*?</title>', '', nav).replace('<svg ', '<svg class="nav__svg" aria-hidden="true" focusable="false" ', 1)
nav = re.sub(r' role="img"| aria-label="[^"]*"', '', nav)
nav = nav.replace('fill="#36a3ff"', 'style="fill:var(--letrero-azul)"').replace('fill="#f6ecdc"', 'style="fill:var(--letrero-blanco)"').replace('stroke="#f6ecdc"', 'style="stroke:var(--letrero-blanco)"')
ids = [t[0] for t in TABS]
subs_known = json.dumps({t[0]: True for t in TABS})

page = f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>La carta · Almud Bar, Castro</title>
<meta name="description" content="tenemos pa todos los gustos! Coctelería de la casa, cócteles del mundo mundial, espirituosos, vinos, mocktails y comilona." data-en="Something for every taste! House cocktails, classics, spirits, wines, alcohol-free and food.">
<meta name="theme-color" content="#160d0b">
<meta name="robots" content="noindex">
<link rel="canonical" href="{SITE}/v3/carta/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Almud Bar">
<meta property="og:title" content="La carta · Almud Bar">
<meta property="og:description" content="tenemos pa todos los gustos!">
<meta property="og:url" content="{SITE}/v3/carta/">
<meta property="og:image" content="{SITE}/assets/v3/og-carta.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="../../brand/v3/favicon.svg" type="image/svg+xml">
<link rel="preload" href="../../assets/fonts/big-shoulders-display-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="../../assets/fonts/barlow-condensed-latin-500-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="../../assets/fonts/barlow-condensed-latin-600-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="../../css/v3/tokens.css?v={ver('css/v3/tokens.css')}">
<link rel="stylesheet" href="../../css/v3/site.css?v={ver('css/v3/site.css')}">
<link rel="stylesheet" href="../../css/v3/carta.css?v={ver('css/v3/carta.css')}">
<style>{''.join(tabcss + chipcss)}</style>
<script>(function(d){{var r=d.documentElement,T={json.dumps(ids)},h=(location.hash||'').slice(1);r.classList.add('js');try{{if(localStorage.getItem('almud-idioma')==='en')r.lang='en'}}catch(e){{}}
var t=T.indexOf(h)>-1?h:null;if(!t&&h){{var el=null;try{{el=d.querySelector('[data-sub="'+h+'"]')}}catch(e){{}}}}
r.setAttribute('data-tab',t||'casa');if(h&&!t){{r.setAttribute('data-pending-sub',h)}}}})(document)</script>
</head>
<body>
<a class="skip" href="#carta" data-en="Skip to content">Saltar al contenido</a>
<header class="nav nav--carta">
  <a class="nav__logo" href="../" aria-label="Almud Bar · Inicio" data-aria-en="Almud Bar · Home">{nav}</a>
  <nav class="nav__r" aria-label="Carta" data-aria-en="Menu">
    <a class="nav__a nav__dm" href="https://ig.me/m/almud_bar" target="_blank" rel="noopener" data-en="Message us on Instagram">Escríbenos por DM</a>
    <button class="nav__a nav__lang" type="button" data-lang aria-label="English" data-aria-en="Español"><span data-en="ES">EN</span></button>
  </nav>
</header>
<main id="carta" class="carta">
  <div class="carta__head wrap">
    <h1 class="carta__t" data-en="The menu">La carta</h1>
    <p class="carta__b">tenemos pa todos los gustos!{g('something for every taste!')}</p>
  </div>
  <div class="tabs-sent" aria-hidden="true"></div>
  <nav class="tabs" aria-label="Secciones de la carta" data-aria-en="Menu sections"><div class="tabs__l">{tabs_html}</div></nav>
  <div class="panels"><div class="hoja">{''.join(panels)}</div></div>
  <footer class="carta__pie wrap">
    <a class="btn btn--ghost" href="https://uqr.to/ppvi" target="_blank" rel="noopener" data-en="Official menu (PDF)">Carta oficial (PDF)</a>
    <a class="btn btn--ghost" href="../" data-en="Home">Inicio</a>
  </footer>
</main>
<script>(function(d){{if(d.documentElement.lang!=='en')return;d.querySelectorAll('body [data-en]').forEach(function(e){{e.dataset.es=e.textContent;e.textContent=e.dataset.en}})}})(document)</script>
<script src="../../js/v3/carta.js?v={ver('js/v3/carta.js')}" defer></script>
</body>
</html>
'''
out = ROOT / 'v3/carta/index.html'
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(page)
print('ok', out, len(page))
