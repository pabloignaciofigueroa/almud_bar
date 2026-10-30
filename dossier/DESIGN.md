# DESIGN.md · Dossier-brochure de Almud Bar

Dossier que acompaña la web regalo de Almud Bar (almudbar.pages.dev), para Carmen Paz y Sylvain. Sigue la skill `dossier-brochure-web-regalo` y el caso de referencia Turismo Chiloé Mágico (`chiloe_magico_tours/dossier`).

## Archivos
- `build_dossier.py`: genera `almud-dossier-diseno.html` (autocontenido). Las cifras se calculan al construir desde `content/` y `tools/boceto_raiz.py` (la página principal).
- `capture.js`: capturas del sitio servido en local (`python3 -m http.server 8765` en la raíz). `SOLO=clave` rehace solo esas capturas de computador.
- `render.js`: PDF, PNG por lámina en `pages/` y revisión de desbordes (`overflow []`).
- `check.py`: frases de 4 palabras repetidas entre láminas, tecnicismos y citas literales contra sus fuentes. Todo debe dar vacío u OK.

## Formato
- 14 láminas de 13 × 8,5 in, composición libre, cada una con su fondo.
- Fondos alternados con los colores del sitio: crema, rojo cinta, verde, negro, amarillo, rosa muro, naranja.
- Letras del sitio: Big Shoulders Display (títulos, medallones, cápsulas, citas) y Barlow Condensed (texto).
- Gramática de la marca:
  - el rombo de la boca del almud como medallón;
  - las cintas del techo colgando del borde;
  - la baraja de polaroids;
  - los platos en redondo;
  - cápsulas de color con nombres y precios.
- Portada: el primer cuadro del video de portada del sitio (su letrero), a doble página, con el logo sobre la masa blanca al 75 %.
- Carta con el sello rojo «PARA ALMUD BAR ★ HECHO EN CASTRO ★ OCTUBRE 2026 ★».

## Texto
- Cada decisión parte de algo suyo: su post, su bio, su carta, sus clientes.
- Sin cuentas personales de Instagram, igual que el sitio.
- Las correcciones al original se dicen en letra pequeña: «corazón» en lugar del emoji y Elymar en singular.
- Sin tecnicismos ni frases que pongan al estudio como protagonista.
