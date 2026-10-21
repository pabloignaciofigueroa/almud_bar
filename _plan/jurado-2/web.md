# Jurado 2 · Diseñador web: revisión del sitio construido (fase 16)

**Puntaje: 8,0 / 10 · Veredicto: FIX** (aprueba cuando se cierren los dos P1. Son arreglos chicos y acotados.)

Probé las páginas reales (`index.html`, `carta/index.html`) servidas en :8793 con Chromium 1194 + Playwright, en 7 viewports (320, 390×844, 768×1024, 1024×768, 1280×720, 1440×900, 1920×1080). Hay 232 capturas viewport por viewport en `shots-web/` (hojas de contacto en `shots-web/sheets/`) y capturas de interacciones en `shots-web/x-*.jpg`. Las vi todas por hoja. Los scripts de medición viven en el scratchpad de la sesión y no tocan el sitio.

## Mediciones

| Métrica | Portada (teléfono 390@3x) | Portada (escritorio 1440@1x) | Carta 390 | Carta 1440 |
|---|---|---|---|---|
| LCP local sin throttling | 120 ms (portada-terraza 1440.avif) | 132 ms | 108 ms (texto) | 116 ms |
| LCP Slow-4G (1,6 Mbps, 150 ms) + CPU ×4 | **3 200 ms** ✗ | 3 048 ms ✗ | 1 388 ms | 1 876 ms |
| CLS (carga + recorrido completo) | 0,000 | 0,000 | 0,000 | 0,000 |
| Peso de la primera vista, sin compresión | 555 KB / 48 req | 555 KB / 48 req | 299 KB / 20 req | 349 KB / 25 req |
| Peso tras recorrer toda la página | 3,38 MB / 84 req | 2,46 MB / 84 req | 325 KB / 22 | 359 KB / 26 |
| HTML / CSS con gzip (estimado) | 29 KB / 9 KB site.css | | 27 KB | |
| Errores de consola / 404 | 0 / 0 en los 14 recorridos | | | |
| Overflow horizontal | ninguno en los 7 anchos, en ambas páginas | | | |
| Fuentes < 13 px | ninguna (mínimo 14 px) | | | |

- **Contraste (calculado sobre colores computados):** tinta noche sobre turquesa da 8,1; sobre amarillo 11,7; sobre verde 6,3; sobre coral 6,0. Papel sobre fucsia da **4,70** (pasa AA, pero justo, con Oswald 300 a 18 px). El botón barra con tinta noche da 5,6. El precio magenta sobre papel da 4,63. Las glosas `--papel-suave` sobre noche dan 9,98. Todo pasa AA.
- **srcset por DPR (ancho del archivo ÷ px físicos necesarios):** 390@3x mediana 1,21 · 390@2x 1,36 · 1440@1x 1,08 · 1920@1x 1,08. Aparecen tres faltas:
  - **Portada a 1440@2x, 0,50:** el máximo es 1440w, así que se agranda 2× en un MacBook.
  - **Lugar barra 0,70 y mural 0,60** a 1440@2x.
  - **Miniaturas de la carta en exceso:** el mínimo es 480w para 104–144 css, lo que da 3,3–4,6× a DPR1. En mosaicos a 390@1x, 15 imágenes reciben 2,8×.
- **Encabezados:** un solo h1 por página, h2 por capítulo, h3 y h4 sin saltos. En la carta hay 41 encabezados con una jerarquía limpia. Los h2 de los días ocultos van dentro de `[hidden]`, así que no contaminan el esquema.
- **lang:** `html lang` cambia a `en`. Hay 151 `lang="en"` en las glosas y 1 `lang="fr"` en una reseña. Correcto.
- **Meta:** están title, description (con su versión EN), theme-color, favicon SVG + ICO y apple-touch-icon. **Faltan** `og:url`, `canonical` y `twitter:card`, y el **`og:image` es relativo** (`assets/v2/img/og-terraza.jpg`). No hay manifest (no es necesario).

## Interacciones verificadas

- **Menú del teléfono:**
  - Abre con clip-path, `aria-expanded` cambia y el foco pasa al primer enlace.
  - Escape cierra y devuelve el foco a `.menu-b`. Tocar un enlace cierra el menú y deja la sección a 56 px, justo bajo la barra.
  - El scroll de fondo se bloquea. ES/EN viven dentro de la hoja con 44×44.
- **Navegación de escritorio:** el ancla deja el capítulo exactamente bajo la barra de 72 px.
- **ES/EN:** el cambio es instantáneo, sin corrimiento, y persiste a `carta/` (que queda en `lang=en` con "The menu" y "Home"). Las glosas EN aparecen debajo del texto literal y se respeta la voz.
- **Hoy en Almud** (`?dia=0…6`):
  - Dom y Lun muestran "Abrimos de Mar a Sáb". Mar coral, Mié turquesa, Jue fucsia, Vie amarillo, Sáb verde.
  - "Hoy" está bien marcado en la semana con `aria-current="date"`. Sin JS queda el bloque genérico.
- **Carta:**
  - El deep link `#comilona-pizzas` abre Comilona › Pizzas a 148 px.
  - Pestañas y chips actualizan `aria-selected` y el hash. Atrás y adelante restauran pestaña y chip.
  - Las flechas, Inicio y Fin funcionan sin animar, y Tab sale de la lista de pestañas al panel.
  - Sin JS, las 7 secciones quedan apiladas y legibles.
- **Mapa:** antes del clic hay 0 pedidos a Google. El clic crea el iframe con `title` y foco.
- **Videos:** corren solo en vista (umbral de 0,25) y se pausan al salir. El botón Pausar/Reproducir conserva su estado y su texto en ES y EN. Con reduced motion quedan en el póster.
- **Teclado:** el skip link es lo primero y aterriza en `#hoy`. Probé 80 tabulaciones en la portada: todas tienen outline sólido de 3 px con un color adaptado al campo (papel, noche o azul). El outline nunca se pierde.

## Fortalezas

1. Es un sistema serio. Cada campo de color tiene su tinta, todo pasa AA y CLS = 0 en todos los anchos aunque haya LQIP, video y tipografía display. No hay errores ni 404.
2. Hoy en Almud es la mejor idea del sitio y está bien ejecutada. El día cambia el color, el titular y la promo literal de la carta, y la semana queda como referencia. Funciona sin JS.
3. La carta es un producto en sí misma: deep links, historial, semántica ARIA de pestañas, teclado sin animación, sticky medido con ResizeObserver y precios en dos columnas legibles.
4. Movimiento según Emil §6: CSS + IO sin GSAP, revelados de una sola vez, nada atado a la velocidad del scroll. Reduced motion pasa a opacidad. El mapa y los videos son diferidos y respetuosos.
5. Bilingüe sin traicionar la voz: el texto literal va arriba y la glosa entre corchetes explica el modismo ("hidrateichon [hydration]").

## Correcciones priorizadas

**P1-a · Hoy en Almud queda invisible si se entra a la sección sin cruzar su borde superior.**
- *Evidencia:* `x-P1-hoy-vacio-390.jpg` muestra la pantalla entera negra. Se reproduce así: menú → "El lugar" → subir; `#hoy` queda `arm` sin `imprime` con top −667.
- *A 1920×1080:* bajar exactamente una pantalla deja la sección en top −8 y en blanco (`home-1920-s00.jpg`, cuadro 2).
- *Cualquier salto dentro de la sección:* `scrollTo(offsetTop+50)` en 390, 1024, 1440 y 1920 deja la sección `clip-path: inset(0 100% 0 0)` para siempre.
- *Causa:* el observador mira `#hoy`, que es el mismo elemento recortado a ancho 0. Ese mismo problema está documentado y resuelto para `[data-rv]` ("se observa el padre"), pero no para Hoy. Con reduced motion no falla, porque ahí no hay clip.
- *Arreglo:* en `css/v2/site.css` l.540–545, mover el recorte a los hijos (`.hoy.arm > .hoy-dia { clip-path: inset(0 100% 0 0) }` y `.hoy.arm.imprime > .hoy-dia { clip-path: inset(0); transition: … }`) y mantener `hio.observe(hoy)` en `js/v2/site.js` l.171–180, porque la sección ya no está recortada. Como red de seguridad, agregar `threshold: 0` y `if (es[0].isIntersecting || es[0].boundingClientRect.top < innerHeight)`.

**P1-b · El LCP del teléfono es de 3,2 s en Slow-4G (meta ≤ 2,5 s).**
- *Causa:* a 390@3x el hero descarga `portada-terraza-a-1440.avif` (276 KB) por `sizes="… 150vw"`, y el ~29 % del recorte queda fuera de pantalla.
- *Arreglo (art direction):* en `src-v2` (generador de la portada), poner un `<source media="(max-width: 899px)">` con un recorte 4:5 propio de 720/960/1170w a AVIF q≈50, de ~110–150 KB, con `sizes="100vw"`. Igualar el `imagesrcset`/`imagemedia` del `<link rel=preload>`.
- *Opcional:* bajar los preloads de fuentes a dos (Six Caps + Oswald 400). Objetivo: ≤ 2,4 s.

**P2-a · La barra de pestañas sticky de la carta ocupa 31 % del alto a 320 (196 px, 4 filas) y 18 % a 390 (148 px).**
- *Evidencia:* `x-sticky.jpg`, `carta-320-s00.jpg`.
- *Arreglo:* en `css/v2/carta.css` l.44, bajo `@media (max-width: 699px)`, poner `.tabs-l { flex-wrap: nowrap; overflow-x: auto; scroll-snap-type: x proximity; scrollbar-width: none; }` y un degradado de borde que sugiera que hay más. El `reveal()` de `carta.js` ya desliza la pestaña activa a la vista. Queda una fila de ~52 px.

**P2-b · El foco se escapa de la hoja del menú abierta.** Tab pasa de "EN" a "Cómo llegar" del contenido tapado por la hoja.
- *Arreglo:* en `site.js` `setMenu()`, agregar `d.querySelector('main').inert = open` (y lo mismo para el pie y el resto de `.nav`, salvo `.menu-b`).

**P2-c · OG roto al compartir por WhatsApp o Instagram**, con `og:image` relativo.
- *Arreglo:* en las plantillas del `<head>` de `tools/build_v2.py`, usar una URL absoluta del dominio final y agregar `og:url`, `<link rel=canonical>`, `og:locale` es_CL, `og:image:width/height/alt` y `twitter:card=summary_large_image`.

**P2-d · Portada a 1440@2x agrandada 2×** (máximo 1440w), y a 1920 queda contenida en 1440 con laterales negros. Lo segundo lo acepto, porque es honesto con la fuente. Lo primero se arregla así:
- generar 2048w o 2560w si el original lo permite;
- si no, cambiar `--photo-max` para que la portada no supere 1,3× en retina.

**P2-e · Objetivos táctiles < 44 px:**
- `.menu-b` 33×44 → `min-width: 44px`.
- `.nav-carta .l-corto` "DM" 17×44 → `min-width: 44px; text-align: center`.
- En "Cuándo y dónde", `+56…` 111×32, `@almud_bar` 79×32 y `@bazar_almud` 88×25 → `.donde dd a { display: inline-block; padding-block: 6px; }`.

**P3:**
- (a) Miniaturas de la carta: agregar `carta-*-a-240` y `-320` al srcset, y ajustar `sizes` de los mosaicos a 390 (`(max-width: 699px) 45vw`).
- (b) A 1440 el mosaico de El lugar deja huecos grandes junto a la barra y al mural (`home-1440-s01.jpg`). Conviene alinear `align-self` o reducir el desfase.
- (c) El "Cómo llegar" bajo la lámpara de El lugar y el crédito "Video" sobre fotos fijas (`@rober.patagonico`, mural) confunden. Hay que quitar el enlace y decir "Foto" (o poner el reel).
- (d) En escritorio el nav no tiene "Cuándo y dónde", aunque el teléfono sí.
- (e) La portada mide 23 000 px en teléfono (27 pantallas). Equipo y reseñas podrían compactarse.
- (f) Hay 6,6 MB de video sin referencia en `assets/v2/video` (`carta-*`, `lugar-techo-flecos*`). O se usan o se excluyen del deploy.
