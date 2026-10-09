# Bitácora

- 2026-10-08 18:30 — Inicio. Repo vacío, rama main. Acceso a carpeta local y Descargas.
- Instagram: 168 posts capturados (2022-12 → 2026-07) vía navegador del usuario.
- 21:00 — Fases 3–9: tipografías (Six Caps + Big Shoulders + Oswald + Caveat), paleta, logo vectorizado desde la carta oficial, guion con fuentes, medios (64 imágenes WebP, 4 videos), build.py + publish.py (probado: falla con .md, archivo faltante y >25 MB).
- 21:30 — Fases 10–16: secciones completas, primera revisión visual en 1536 px.
- 22:15 — Fases 17–19: QA (CLS 0,0008 escritorio / 0,0007 móvil, sin 4xx, sin errores; raíz = public/), auditorías independientes de voz y de código; correcciones aplicadas (fallback sin GSAP, foco, ancla al cruzar 760px, contraste magenta, reseña solicitada reemplazada, etc.).
- 22:25 — Fase 20: Cloudflare Pages "almudbar" (main, sin build, salida public/). En línea: https://almudbar.pages.dev. Verificado: 14 rutas internas devuelven el index (no se publican), og.jpg responde image/jpeg, 51 imágenes cargan, check "Cloudflare Pages" en verde, solo rama main.
