#!/usr/bin/env python3
"""Regenera public/: la carpeta que se publica en Cloudflare Pages.

Copia solo lo que el sitio v2 usa de verdad (fase 16: se siguen las referencias desde las páginas; index.html, carta/index.html, css/v2, js/v2, vendor, assets/v2, assets/fonts, brand),
deja fuera todo lo interno y escribe public/_headers con la política de caché.

Falla (código 1, sin dejar un public/ a medias) si:
  - se cuela algo interno (.md, .py, .csv, .json, assets/raw, nombres con "_"),
  - falta un archivo que index.html, css o js referencian,
  - algún archivo pesa más de 25 MB (límite por archivo de Cloudflare Pages).

Uso: python3 tools/publish.py
"""
import pathlib, re, shutil, sys, tempfile
from urllib.parse import unquote

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / 'public'

INCLUDE_FILES = ['index.html', 'carta/index.html', 'v3/index.html', 'v3/carta/index.html', 'nueva/index.html', 'nueva/carta/index.html', 'nueva_v2/index.html', 'nueva_v3/index.html', 'nueva_v4/index.html', 'nueva_v5/index.html', 'nueva_v6/index.html', 'nueva_v7/index.html', 'nueva_v8/index.html', 'nueva_v9/index.html', 'nueva_v9/carta/index.html', 'nueva_v10/index.html', 'nueva_v10/carta/index.html', 'nueva_v11/index.html', 'nueva_v11/carta/index.html', 'nueva_v12/index.html', 'nueva_v12/carta/index.html', 'nueva_v13/index.html', 'nueva_v13/carta/index.html', 'assets/og.jpg',  # fase 20: la v3 es la portada (/ y /carta/); /v3/ redirige
                  # fase 15: la carta en su propia página
                 '404.html', 'robots.txt', 'sitemap.xml', 'site.webmanifest']  # pulido 3: 404 de Pages, rastreo e íconos
# v2: solo lo que el sitio nuevo usa. La v1 (css/main.css, js/main.js, assets/img, assets/video) queda en el repo por historia, fuera de public/.
INCLUDE_DIRS = ['css/v2', 'js/v2', 'vendor', 'assets/v2', 'assets/fonts', 'brand', 'css/v3', 'js/v3', 'assets/v3', 'css/v4', 'js/v4', 'assets/v4', 'css/nv2', 'js/nv2', 'css/nv3', 'js/nv3', 'css/nv4', 'js/nv4', 'css/nv5', 'js/nv5', 'css/nv6', 'js/nv6', 'css/nv7', 'js/nv7', 'css/nv8', 'js/nv8', 'css/nv9', 'js/nv9', 'css/nv10', 'js/nv10', 'css/nv11', 'js/nv11', 'css/nv12', 'js/nv12', 'css/nv13', 'js/nv13', 'assets/nv2', 'assets/nv9']

ALL_DIRS = []

BLOCKED_EXT = {'.md', '.py', '.csv', '.json', '.pyc', '.sh', '.ipynb'}
BLOCKED_DIRS = {'assets/raw'}
BLOCKED_NAMES = {'.DS_Store', 'Thumbs.db', '__pycache__', 'node_modules', '.git'}
MAX_BYTES = 25 * 1024 * 1024

# Caché (antes en vercel.json). Cloudflare Pages lee public/_headers.
# Pulido 3: css/v2 y js/v2 se piden con ?v=<hash del contenido> (build_v2.py), así que son immutable por un año: un cambio
# cambia la URL. Las fuentes no cambian nunca de contenido con el mismo nombre. Las fotos (assets/v2) se nombran por id y ancho,
# no por contenido: una semana + revalidación. Las páginas siempre se revalidan.
HEADERS = """\
/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin

/
  Cache-Control: public, max-age=0, must-revalidate

/carta/
  Cache-Control: public, max-age=0, must-revalidate

/css/*
  Cache-Control: public, max-age=31536000, immutable

/js/*
  Cache-Control: public, max-age=31536000, immutable

/assets/fonts/*
  Cache-Control: public, max-age=31536000, immutable

/assets/v2/*
  Cache-Control: public, max-age=604800, stale-while-revalidate=86400

/brand/*
  Cache-Control: public, max-age=604800, stale-while-revalidate=86400

/site.webmanifest
  Content-Type: application/manifest+json
  Cache-Control: public, max-age=86400

/assets/v3/*
  Cache-Control: public, max-age=604800, stale-while-revalidate=86400

/assets/v4/*
  Cache-Control: public, max-age=604800, stale-while-revalidate=86400

/vendor/*
  Cache-Control: public, max-age=31536000, immutable
"""
# v4 fase 10 pub: la v11 es la portada (/ y /carta/); la v3 queda archivada en /v3/ y /v3/carta/ (noindex), así que ya no se redirige
REDIRECTS = """/v3/avance/ / 301
"""


def is_internal(rel: pathlib.PurePosixPath) -> str | None:
    """Devuelve el motivo si la ruta es interna; None si es publicable."""
    s = rel.as_posix()
    if any(s == d or s.startswith(d + '/') for d in BLOCKED_DIRS):
        return 'carpeta interna'
    for part in rel.parts:
        if part in BLOCKED_NAMES:
            return f'nombre bloqueado ({part})'
        if part.startswith('_') and s not in ('_headers', '_redirects'):
            return f'nombre interno ({part})'
        if part.startswith('.'):
            return f'archivo oculto ({part})'
    if rel.suffix.lower() in BLOCKED_EXT:
        return f'extensión interna ({rel.suffix})'
    return None


SITE = 'https://almudbar.pages.dev/'


def used_files() -> set[str]:
    """Fase 16: lo que las páginas usan de verdad (HTML → CSS/JS → fuentes e imágenes), siguiendo las referencias.
    Lo que no se referencia no se publica (videos e imágenes viejas, vendor/ que la v2 no carga, brand/ de trabajo)."""
    seen, todo = set(), list(INCLUDE_FILES)
    while todo:
        f = todo.pop()
        if f in seen or not (ROOT / f).is_file():
            continue
        seen.add(f)
        if pathlib.PurePosixPath(f).suffix not in ('.html', '.css', '.js', '.webmanifest'):
            continue
        text = (ROOT / f).read_text(errors='ignore').replace(SITE, '/')
        base = pathlib.PurePosixPath('.') if f.endswith('.js') else pathlib.PurePosixPath(f).parent
        todo += [r for r in references(text, base) if r not in seen]
    return seen


def copy_tree(stage: pathlib.Path) -> list[str]:
    skipped = []
    used = used_files()
    for f in INCLUDE_FILES:
        src = ROOT / f
        if not src.is_file():
            sys.exit(f'ERROR: falta {f}')
        (stage / f).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, stage / f)
    for d in INCLUDE_DIRS:
        base = ROOT / d
        if not base.is_dir():
            sys.exit(f'ERROR: falta la carpeta {d}/')
        for src in sorted(base.rglob('*')):
            if not src.is_file():
                continue
            rel = pathlib.PurePosixPath(src.relative_to(ROOT).as_posix())
            if is_internal(rel):
                skipped.append(rel.as_posix())
                continue
            if rel.as_posix() not in used:
                skipped.append(rel.as_posix() + ' (sin uso)')
                continue
            dst = stage / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    for d in ALL_DIRS:  # v1b: medios de la v1 (sus rutas se arman en JS, el rastreo no las ve)
        for src in sorted((ROOT / d).rglob('*')):
            rel = pathlib.PurePosixPath(src.relative_to(ROOT).as_posix())
            if src.is_file() and not is_internal(rel):
                (stage / rel).parent.mkdir(parents=True, exist_ok=True); shutil.copy2(src, stage / rel)
    (stage / '_headers').write_text(HEADERS)
    (stage / '_redirects').write_text(REDIRECTS)
    return skipped


REF_PATTERNS = [
    re.compile(r'''(?:src|href|poster|data-[\w-]+)\s*=\s*["']([^"']+)["']'''),
    re.compile(r'''srcset\s*=\s*["']([^"']+)["']'''),
    re.compile(r'''url\(\s*["']?([^"')]+)["']?\s*\)'''),
    re.compile(r'''["'`]((?:\.{0,2}/)?(?:assets|brand|css|js|vendor)/[^"'`\s]+?)["'`]'''),
]


def references(text: str, base: pathlib.PurePosixPath) -> set[str]:
    refs = set()
    for pat in REF_PATTERNS:
        for m in pat.finditer(text):
            for piece in m.group(1).split(','):
                url = piece.strip().split(' ')[0].split('#')[0].split('?')[0]
                if not url or url.startswith('@') or re.match(r'^([a-z]+:|//|#|\{|\$)', url, re.I) or '${' in url:
                    continue
                if not re.search(r'\.[a-z][a-z0-9]{1,4}$', url, re.I):
                    continue
                p = (base / unquote(url)).as_posix() if not url.startswith('/') else url.lstrip('/')
                parts = []
                for seg in p.split('/'):
                    if seg in ('', '.'):
                        continue
                    if seg == '..':
                        if parts:
                            parts.pop()
                        continue
                    parts.append(seg)
                refs.add('/'.join(parts))
    return refs


def check(stage: pathlib.Path) -> list[str]:
    errors = []
    files = [p for p in stage.rglob('*') if p.is_file()]
    for p in files:
        rel = pathlib.PurePosixPath(p.relative_to(stage).as_posix())
        why = is_internal(rel)
        if why:
            errors.append(f'interno: {rel} ({why})')
        if p.stat().st_size > MAX_BYTES:
            errors.append(f'pesa más de 25 MB: {rel} ({p.stat().st_size / 1048576:.1f} MB)')
    sources = [stage / f for f in INCLUDE_FILES] + list((stage / 'css').rglob('*.css')) + list((stage / 'js').rglob('*.js'))
    missing = set()
    for src in sources:
        rel_dir = pathlib.PurePosixPath(src.relative_to(stage).as_posix()).parent
        # en JS las rutas son relativas al documento, no al archivo .js
        base = pathlib.PurePosixPath('.') if src.suffix == '.js' else rel_dir
        for ref in references(src.read_text(errors='ignore').replace(SITE, '/'), base):
            if not (stage / ref).is_file():
                missing.add(f'falta: {ref} (referenciado en {src.relative_to(stage)})')
    return errors + sorted(missing)


def main():
    with tempfile.TemporaryDirectory(dir=ROOT) as tmp:
        stage = pathlib.Path(tmp) / 'public'
        stage.mkdir()
        skipped = copy_tree(stage)
        errors = check(stage)
        if errors:
            print('publish.py: ERROR, public/ no se modificó', file=sys.stderr)
            for e in errors:
                print('  ' + e, file=sys.stderr)
            sys.exit(1)
        if OUT.exists():
            shutil.rmtree(OUT)
        shutil.move(str(stage), OUT)
    files = [p for p in OUT.rglob('*') if p.is_file()]
    total = sum(p.stat().st_size for p in files)
    big = max(files, key=lambda p: p.stat().st_size)
    print(f'public/ listo: {len(files)} archivos, {total / 1048576:.1f} MB '
          f'(el mayor: {big.relative_to(OUT)}, {big.stat().st_size / 1048576:.1f} MB)')
    unused = [x for x in skipped if x.endswith('(sin uso)')]
    print(f'omitidos por internos: {len(skipped) - len(unused)} · sin uso (no se publican): {len(unused)}')
    if '-v' in sys.argv:
        for s in skipped:
            print('  - ' + s)


if __name__ == '__main__':
    main()
