#!/usr/bin/env python3
"""Genera index.html desde src/index.html: imágenes (srcset, width/height, LQIP),
carta y reseñas desde content/*.json, símbolos del logo. Falla si falta un alt en inglés."""
import json, os, re, sys, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
J = lambda p: json.load(open(os.path.join(ROOT, p)))
meta = J('assets/img/meta.json')
carta = J('content/carta.json')
reviews = J('content/reviews.json')
E = html.escape
IMG_FOR = {'IG-044': 'c-peter', 'IG-002': 'c-olvidar', 'IG-063': 'c-saguer', 'IG-039': 'c-sangria', 'IG-096': 'c-coquette',
           'IG-011': 'c-moto', 'IG-139': 'c-tukulito', 'IG-066': 'c-contuti', 'IG-077': 'c-gredita', 'IG-040': 'c-topiturron',
           'IG-016': 'c-negroni', 'IG-019': 'c-piscolein'}
EN_ALT = {'c-peter': 'Red cocktail topped with a smoke-filled bubble', 'c-olvidar': 'Clear cocktail tinted red by a float of red wine',
          'c-saguer': 'Spiced sour being torched at the bar', 'c-sangria': 'Glass of house sangria with fruit and flowers',
          'c-coquette': 'Pink creamy cocktail being handed over', 'c-moto': 'Orange mango mocktail with a salt rim',
          'c-tukulito': 'Seared tuna tataki with house bread', 'c-contuti': 'Sharing board with cheeses, olives, fruit and ham',
          'c-gredita': 'Clay pot of shrimp and mushrooms', 'c-topiturron': 'Chocolate nougat dessert with sorbet',
          'c-negroni': 'Negroni being stirred at the bar', 'c-piscolein': 'Bartender serving a round of piscolas'}
ES_ALT = {'c-peter': 'Cóctel rojo coronado con una burbuja de humo', 'c-olvidar': 'Cóctel transparente teñido de rojo por el vino tinto',
          'c-saguer': 'Sour especiado flameado en la barra', 'c-sangria': 'Copa de sangría de la casa con fruta y flores',
          'c-coquette': 'Cóctel rosado y cremoso pasando de mano en mano', 'c-moto': 'Mocktail naranjo de mango con borde de sal',
          'c-tukulito': 'Tataki de atún sellado con pan de la casa', 'c-contuti': 'Tabla para compartir con quesos, aceitunas, fruta y jamón',
          'c-gredita': 'Gredita de camarones y champiñones', 'c-topiturron': 'Postre de turrón de chocolate con sorbete',
          'c-negroni': 'Negroni mezclándose en la barra', 'c-piscolein': 'Bartender sirviendo una ronda de piscolas'}

def img_tag(name, sizes, alt='', alt_en='', extra=''):
    a = f' alt="{E(alt)}"' + (f' data-alt-en="{E(alt_en)}"' if alt_en else '')
    return f'<img data-img="{name}" sizes="{sizes}"{a}{extra}>'

def item_html(it, kind, i):
    name = it['n']; img = IMG_FOR.get(it.get('img', ''))
    pic = img_tag(img, '(max-width: 900px) 80vw, 34vw', ES_ALT[img], EN_ALT[img]) if img else ''
    plate = '' if img else f'<div class="plate plate--{i % 6}" aria-hidden="true"><span>{E(name)}</span></div>'
    desc = f'<p class="dish__d" lang="es">{E(it["d"])}</p>' if it.get('d') else ''
    return (f'<li class="dish{" has-img" if img else ""}" data-img="{img or ""}">'
            f'<button class="dish__btn" type="button" aria-expanded="{"true" if i == 0 else "false"}">'
            f'<span class="dish__n" lang="es">{E(name)}</span><span class="dish__p">${E(it["p"])}</span></button>'
            f'<div class="dish__more"><div class="dish__media">{pic}{plate}</div>{desc}</div></li>')

def panel(kind, items, active):
    out = [f'<div class="carta" role="tabpanel" id="panel-{kind}" aria-labelledby="tab-{kind}"{"" if active else " hidden"}>',
           '<div class="carta__grid"><div class="carta__lists">']
    group = object(); n = 0
    for it in items:
        g = it.get('g')
        if g != group:
            if n: out.append('</ul>')
            if g: out.append(f'<h3 class="carta__g" lang="es">{E(g)}</h3>')
            out.append('<ul class="carta__list">'); group = g
        out.append(item_html(it, kind, n)); n += 1
    out.append('</ul></div><aside class="carta__show" aria-hidden="true"></aside></div></div>')
    return '\n'.join(out)

def promos():
    cards = []
    for i, p in enumerate(carta['promos']):
        img = IMG_FOR.get(p.get('img', ''))
        pic = img_tag(img, '(max-width: 760px) 80vw, 22vw') if img else '<div class="plate plate--4" aria-hidden="true"><span>Ramón</span></div>'
        cards.append(f'<li class="promo c{i}" data-day="{p["dia"]}"><div class="promo__media">{pic}</div>'
                     f'<p class="promo__d" lang="es">{E(p["d"])}</p><p class="promo__t" lang="es">{E(p["t"])}</p>'
                     f'<p class="promo__today" data-en="Today!">¡Hoy!</p></li>')
    return (f'<div class="carta" role="tabpanel" id="panel-promos" aria-labelledby="tab-promos" hidden>'
            f'<p class="promos__head" lang="es"><span class="promos__price">{E(carta["promo_precio"])}</span> {E(carta["promo_hora"])}</p>'
            f'<ul class="promos">{"".join(cards)}</ul><p class="promos__note" lang="es">{E(carta["promo_nota"])}</p></div>')

def resenas():
    out = []
    flag = {'es': 'ES', 'en': 'EN', 'fr': 'FR'}
    for r in reviews:
        who = r['who'] if r['who'] != 'Visitante' else 'Visitante de Google Maps'
        frm = f'<span class="rev__from">{E(r["from"])}</span>' if r['from'] else ''
        out.append(f'<div class="swiper-slide"><figure class="rev rev--{r["lang"]}"><span class="rev__lang">{flag[r["lang"]]}</span>'
                   f'<blockquote lang="{r["lang"]}"><p>{E(r["q"])}</p></blockquote>'
                   f'<figcaption><b>{E(who)}</b>{frm}<span class="rev__src">{E(r["src"])} · {r["date"][:4]}</span></figcaption></figure></div>')
    return '\n'.join(out)

def logo_defs():
    d = re.search(r' d="([^"]+)"', open(os.path.join(ROOT, 'brand/almud-horizontal.svg')).read()).group(1)
    di = re.search(r' d="([^"]+)"', open(os.path.join(ROOT, 'brand/almud-isotipo.svg')).read()).group(1)
    return (f'<symbol id="logo-h" viewBox="0 0 1957 897"><path fill="currentColor" fill-rule="evenodd" d="{d}"/></symbol>\n'
            f'<symbol id="iso" viewBox="1343 0 614 897"><path fill="currentColor" fill-rule="evenodd" d="{di}"/></symbol>')

def expand_imgs(s):
    missing = []
    def rep(m):
        tag = m.group(0); name = re.search(r'data-img="([^"]+)"', tag).group(1)
        if name not in meta: missing.append('meta:' + name); return tag
        mm = meta[name]
        alt = re.search(r' alt="([^"]*)"', tag)
        if alt is None: missing.append('alt:' + name)
        elif alt.group(1) and 'data-alt-en=' not in tag: missing.append('alt-en:' + name)
        eager = 'data-eager' in tag
        add = (f' src="assets/img/{name}-800.webp" srcset="assets/img/{name}-800.webp 800w, assets/img/{name}-1800.webp 1800w"'
               f' width="{mm["w"]}" height="{mm["h"]}" decoding="async"' + ('' if eager else ' loading="lazy"') +
               f' style="background-image:url({mm["lqip"]})"')
        if 'sizes=' not in tag: add += ' sizes="100vw"'
        return tag[:-1] + add + '>'
    s = re.sub(r'<img [^>]*data-img="[^"]+"[^>]*>', rep, s)
    return s, missing

def main():
    s = open(os.path.join(ROOT, 'src/index.html')).read()
    c = (panel('coctel', carta['coctel'], True) + panel('mocktail', carta['mocktail'], False) +
         panel('comilona', carta['comilona'], False) + promos())
    s = s.replace('<!--CARTA-->', c).replace('<!--RESENAS-->', resenas()).replace('<!--LOGO_DEFS-->', logo_defs())
    s, missing = expand_imgs(s)
    if missing:
        print('ERROR imágenes:', missing); sys.exit(1)
    open(os.path.join(ROOT, 'index.html'), 'w').write(s)
    print('index.html', len(s) // 1024, 'KB')

if __name__ == '__main__':
    main()
