# Almud Bar — web

Web de **Almud Bar** (Serrano 325, Castro, Chiloé) hecha con el material público de la marca: su Instagram @almud_bar, su carta oficial (uqr.to/ppvi) y reseñas de Google y Tripadvisor.

**En línea:** https://almudbar.pages.dev

## Cómo editar
1. Textos y estructura: `src/index.html` · carta: `content/carta.json` · reseñas: `content/reviews.json` · estilos: `css/main.css` · movimiento: `js/main.js`.
2. Imágenes y videos nuevos: agregarlos a `tools/media.py` y correr `python3 tools/media.py --videos`.
3. Generar y publicar:
   ```
   python3 tools/build.py
   python3 tools/publish.py
   git add -A && git commit -m "…" && git push origin main
   ```
   Cloudflare Pages publica solo la carpeta `public/` (Build output directory: `public`, sin build command).

## Mapa del repositorio
- `public/` lo único que se publica (lo genera `tools/publish.py`).
- `content/` guion con fuentes (`copy.md`), guía de voz, carta, reseñas e investigación.
- `brand/` logo vectorizado, paleta, tipografía y dirección de arte.
- `_plan/` plan y bitácora.
