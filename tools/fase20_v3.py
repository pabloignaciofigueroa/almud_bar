#!/usr/bin/env python3
"""Fase 20 · la v3 pasa a ser la portada (/ y /carta/). PREPARADO, NO APLICADO hasta el OK del director.

Sin argumentos (ensayo, no toca el repo):
  1. arma un public/ de prueba en _plan/v3/fase20/ensayo/public con la v3 en / y /carta/ (rutas absolutas,
     canonical y og:url en la raíz), sitemap nuevo, _redirects (/v3/ → /, /v3/carta/ → /carta/) y _headers;
  2. corre los chequeos de publish.py (referencias internas, tamaños) y lista lo que --aplicar cambiaría.
  Para probarlo: python3 -m http.server -d _plan/v3/fase20/ensayo/public 8780

Con --aplicar (solo con el OK):
  - archiva la v1b (index.html) y la carta v2 (carta/index.html) en _plan/archivo/ (quedan además en git);
  - genera index.html y carta/index.html en modo raíz (ALMUD_RAIZ=1);
  - actualiza sitemap.xml y tools/publish.py (sale la v1b y las páginas /v3/, entra _redirects, caché de assets/v3 y vendor);
  - después: python3 tools/publish.py, commit y push a main (Cloudflare Pages publica).
"""
import os, sys, shutil, subprocess, pathlib, datetime, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
HOY = datetime.date.today().isoformat()
SITEMAP = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://almudbar.pages.dev/</loc><lastmod>{HOY}</lastmod></url>
  <url><loc>https://almudbar.pages.dev/carta/</loc><lastmod>{HOY}</lastmod></url>
</urlset>
"""
REDIRECTS = """/v3/ / 301
/v3 / 301
/v3/carta/ /carta/ 301
/v3/carta /carta/ 301
/v3/avance/ / 301
"""
HEADERS_EXTRA = """
/assets/v3/*
  Cache-Control: public, max-age=604800, stale-while-revalidate=86400

/vendor/*
  Cache-Control: public, max-age=31536000, immutable
"""


def gen(out_dir):
    env = dict(os.environ, ALMUD_RAIZ='1', ALMUD_OUT=str(out_dir))
    for t in ('tools/boceto_v3.py', 'tools/carta_v3.py'):
        subprocess.run([sys.executable, t], cwd=ROOT, env=env, check=True)


def patch_publish(text):
    text = text.replace("INCLUDE_FILES = ['index.html', 'carta/index.html', 'css/main.css', 'js/main.js', 'assets/og.jpg', 'v3/avance/index.html', 'v3/index.html', 'v3/carta/index.html',  # v1b: la v1 vuelve como portada",
                        "INCLUDE_FILES = ['index.html', 'carta/index.html', 'assets/og.jpg',  # fase 20: la v3 es la portada (/ y /carta/); /v3/ redirige")
    text = text.replace("ALL_DIRS = ['assets/img', 'assets/video', 'v3/avance/img']", "ALL_DIRS = []")
    text = text.replace("""/site.webmanifest
  Content-Type: application/manifest+json
  Cache-Control: public, max-age=86400
\"\"\"""", """/site.webmanifest
  Content-Type: application/manifest+json
  Cache-Control: public, max-age=86400
""" + HEADERS_EXTRA + '"""\nREDIRECTS = """' + REDIRECTS + '"""')
    text = text.replace("    (stage / '_headers').write_text(HEADERS)", "    (stage / '_headers').write_text(HEADERS)\n    (stage / '_redirects').write_text(REDIRECTS)")
    text = text.replace("if part.startswith('_') and s != '_headers':", "if part.startswith('_') and s not in ('_headers', '_redirects'):")
    return text


def ensayo():
    base = ROOT / '_plan/v3/fase20/ensayo'
    if base.exists():
        shutil.rmtree(base)
    repo = base / 'repo'
    # copia mínima del repo para el ensayo (enlaces duros para los medios: no ocupa espacio)
    for d in ['assets/v3', 'assets/fonts', 'assets/v2', 'brand', 'css', 'js', 'vendor', 'content', 'tools']:
        # medios por enlace duro (solo lectura); el código y el texto se copian, porque el ensayo los modifica
        link = d.startswith('assets') or d in ('brand', 'vendor')
        shutil.copytree(ROOT / d, repo / d, copy_function=os.link if link else shutil.copy2, ignore=shutil.ignore_patterns('__pycache__'))
    for f in ['404.html', 'robots.txt', 'site.webmanifest', 'assets/og.jpg']:
        (repo / f).parent.mkdir(parents=True, exist_ok=True); shutil.copy2(ROOT / f, repo / f)
    (repo / 'carta').mkdir(exist_ok=True)
    gen(repo)
    (repo / 'sitemap.xml').write_text(SITEMAP)
    pub = repo / 'tools/publish.py'
    pub.write_text(patch_publish(pub.read_text()))
    subprocess.run([sys.executable, 'tools/publish.py'], cwd=repo, check=True)
    shutil.move(str(repo / 'public'), str(base / 'public'))
    shutil.rmtree(repo)
    idx = (base / 'public/index.html').read_text()
    print('canonical:', re.search(r'rel="canonical" href="([^"]+)"', idx).group(1),
          '· og:url:', re.search(r'og:url" content="([^"]+)"', idx).group(1),
          '· rutas absolutas:', idx.count('href="/') + idx.count('src="/'), '· rutas ../:', idx.count('"../'))
    print('ensayo listo en', base / 'public')
    print('--aplicar cambiaría: index.html (v1b → v3), carta/index.html (v2 → v3), sitemap.xml, tools/publish.py; '
          'archiva la v1b y la carta v2 en _plan/archivo/.')


def aplicar():
    arch = ROOT / '_plan/archivo'; arch.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / 'index.html', arch / 'v1b-index.html')
    shutil.copy2(ROOT / 'carta/index.html', arch / 'carta-v2-index.html')
    gen(ROOT)
    (ROOT / 'sitemap.xml').write_text(SITEMAP)
    p = ROOT / 'tools/publish.py'; p.write_text(patch_publish(p.read_text()))
    print('aplicado. Sigue: python3 tools/publish.py, revisar, commit y push.')


if __name__ == '__main__':
    aplicar() if '--aplicar' in sys.argv else ensayo()
