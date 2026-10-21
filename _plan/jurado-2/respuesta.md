# Fase 16 · Respuesta al jurado 2 (gráfico 7,6 · redes 8,2 · web 8,0)

Cada punto de `grafico.md`, `redes.md` y `web.md` queda como **hecho** (con el cómo) o **no hecho** (con el porqué). Las decisiones del director (1–13) mandan sobre las propuestas de los jurados cuando no coinciden.

**Evidencia "después":** `_plan/jurado-2/after/`
- Capturas viewport por viewport, ambas páginas: `r3-{landing|carta}-{320|390|768|1280|1440|1920|390-en|1440-en}-vNN.jpg` (final), `r2-*` (ronda 2). Métricas por captura en `r2-metrics.json` y `r3-metrics.json`.
- Interacciones y mediciones: `interact.json` y `i-*.jpg` (Hoy en los casos reportados, menú, pestañas por ancho, objetivos táctiles, srcset/DPR y LCP).
- Taste inspect: `inspect-landing/` e `inspect-carta/`.
- Scripts: `shoot.py` e `interact.py`.

## Resultados de la verificación (final)
| Medición | Resultado |
|---|---|
| `build_v2.py` | index.html 116 KB (229 literales, 149 glosas, 114 [UI]) · carta/index.html 117 KB (256 ítems) |
| `verify_copy.py` | 215/215 literales, 42/42 titulares, 0 palabras prohibidas |
| `validate_carta.py` | OK |
| Taste lint | index.html 0 FAIL, 1 WARN (el "more than a" de la glosa de IG-118, ya declarado) · carta, site.css, carta.css, tokens.css, site.js, carta.js: 0 / 0 |
| Taste inspect | landing **0 FAIL**, 2 WARN: `palette-cream` (el papel, defendido en sistema.md) y `no-poster` (el póster del video de Dónde se pide a una pantalla de distancia, ver P1-b). Carta **0 FAIL**, 4 WARN (palette-cream, no-footage, still-page: los mismos de la fase 15) |
| CLS (carga + recorrido completo) | landing ≤ 0,0032 en todos los anchos (320: 0,0018 · 1440: 0,0002); carta 0 |
| Consola / pedidos fallidos / terceros | 0 / 0 / 0 en 16 recorridos |
| Desborde horizontal | 0 (320 a 1920, ES y EN) |
| **LCP teléfono, Slow-4G (1,6 Mbps, 150 ms) + CPU ×4, 390@3x** | **2 176 ms** (mediana de 3; antes 3 200). LCP: `portada-terraza-m-1170.avif` (120 KB) |
| LCP escritorio 1440 (mismas condiciones) | 3 136 ms (antes 3 048–3 376). No era la meta: el archivo de 1440 px es el nativo |
| LCP carta 390@3x | 1 280 ms |
| Fotos repetidas por archivo fuente | 0 en el landing y 0 en la carta (solo la imagen OG comparte fuente con su foto, en `<meta>`) |
| srcset/DPR | 0 imágenes mostradas a más px CSS que su archivo, en 390@2x/3x, 1440@1x/2x y 1920; 0 `sizes` desajustados (> 10 %) |
| Objetivos táctiles | 0 controles fuera de texto corrido bajo 44 px (landing y carta, 390 y 1440) |
| `public/` de prueba | 462 archivos, 31,3 MB; **0 archivos sin uso** y 0 referencias rotas. 169 archivos sin uso quedan fuera. Restaurado con `git checkout -- public && git clean -fdq public` |

Nota: durante la ronda alguien creó el commit `078013f` "correcciones del jurado (en curso)" con parte de este trabajo. Yo no hice commit ni push.

## Decisiones del director

1. **Hoy en blanco (web P1-a): hecho.**
   - El `clip-path` pasó a `.hoy.arm > .hoy-dia`; la sección observada ya no se recorta. Mientras está armada, la sección es noche; al imprimirse, campo.
   - El relleno vertical vive en `.hoy-dia`, así que "la franja se imprime" barre todo el bloque.
   - El observador sigue mirando `#hoy` (`rootMargin -25 %` abajo). Se imprime si se cruza esa línea **o si el bloque ya quedó arriba** (`top < 75 % del alto`).
   - Red de seguridad general: el observador de `[data-rv]` y titulares también revela lo que quedó arriba de la pantalla (salto de ancla o scroll rápido).
   - Probado (`interact.json › hoy`, `i-hoy-*.jpg`): menú → El lugar → subir (390), 1920 bajando exactamente una pantalla (top −8), `scrollTo(offsetTop+50)` a 390/1024/1440/1920 y entrada con `#lugar` y subir. En los 7 casos queda `imprime` con `clip-path: inset(0)`.
2. **LCP del teléfono (web P1-b): hecho.**
   - Recorte propio `portada-terraza-m`: el 70 % superior de P189 a todo el ancho, que es exactamente la zona que el teléfono muestra.
   - Se emite en 720/960/1170 px, AVIF q48: 63/90/**120 KB**.
   - `<source media="(max-width: 899px)">` con `sizes="135vw"` (el ancho real de la foto en un teléfono alto es ~1,32×), y `width`/`height` propios.
   - Dos `<link rel=preload>` excluyentes por `media`, cada uno con su `imagesrcset`/`imagesizes`.
   - Escritorio: `sizes="min(100vw, 1440px)"`. La portada nunca pasa de 1440 px CSS (`--photo-max`); en DPR 2 se acepta la blandura (asterisco P189, sin original en alta).
   - Precargas de fuentes reducidas a Oswald 400 y 300 en el landing.
   - Los pósters de video se piden recién a una pantalla de distancia (`data-poster` + IO). Antes, el del martes, oculto, y el de Dónde, al fondo, competían con la portada.
   - Resultado: 3,2 s → **2,18 s**.
3. **OG/meta: hecho, en ambas páginas.**
   - URLs absolutas en `https://almudbar.pages.dev/`: `og:url`, `<link rel=canonical>`, `og:site_name`, `og:locale es_CL` + `og:locale:alternate en_US`, `og:image:type/width/height/alt`, `twitter:card summary_large_image` con title, description e image.
   - `/carta/` tiene su propia OG: `og-carta.jpg`, 1200×630 JPEG por `media_v2.py`, desde la foto de "Aquí te las traigo Peter" (V038-cover, la burbuja de humo).
   - `publish.py` sigue esas URLs absolutas: las imágenes OG se publican.
4. **@ de Lizze: hecho.**
   - **@lizzearellanol** en todo el sitio, texto y `href` (4 apariciones, 0 de "-no").
   - La lista de IG-010 se parte en tres literales verificados: «@pablete_bartender_ @javier.agmc» [IG-010] «@lizzearellanol» [IG-014] «@milagroosjm … @haqum.v99» [IG-010].
   - Anotado en el guion y en `informe.md`: **confirmar con Almud.**
5. **Eventos: hecho.**
   - Se mantiene la marca ‹Este mes›/‹Próximo›.
   - Sale «asegure su entrá hablándonos al DM!» (IG-057): vendía una edición 2026 que Almud no ha anunciado.
   - Cada fila conserva solo el nombre literal y una línea literal de ediciones pasadas.
   - Bajo toda la lista: ‹Ver en Instagram› y ‹Escríbanos al DM›, genérico.
6. **Teléfono y mapa: hecho.**
   - El número aparece solo en Tripadvisor y carta.menu, no en la ficha de Google (`research_web.md`, S1/S2/S9): se quitaron la fila y el `tel:`.
   - Todos los "Cómo llegar" (landing, Hoy y carta) abren `maps/search/?api=1&query=Almud Bar, Serrano 325, Castro`, la ficha del local.
   - El mapa embebido se carga al tocar "Ver mapa" y busca por nombre.
7. **Voz en la portada: hecho.**
   - «Véngase pal Almudcito ito ito» [IG-013] va bajo la bajada (Oswald 600, body), con glosa EN “Come on over to our little Almud”.
   - Elegí el fragmento corto: el resto de la caption («le esperamos desde las 6 pm») repetía el horario.
   - En teléfonos bajos (≤ 700 px de alto) la línea se oculta, para que horario y acciones no pierdan su lugar. A 390×844 entra sin tocar caras.
8. **Carta en el teléfono: hecho.**
   - Bajo 700 px: una sola fila deslizable (`nowrap`, `overflow-x`) de 52 px, contra 148–196 px antes.
   - El borde se desvanece solo del lado que tiene más: `.mas-izq` y `.mas-der` las pone `carta.js` al desplazar, con una máscara funcional.
   - Barra de desplazamiento fina en azul carta y pestañas de 44 px.
   - La activa se lleva a la vista fuera del borde que se desvanece (52 px). Se recalcula al terminar de cargar las fuentes y al cargar la página.
   - Sin scroll-snap: devolvía la pestaña activa al borde (pasaba a 320 con Comilona).
   - 700–1023 px: 2 filas. Escritorio: 1. Los chips usan la misma fila deslizable en el teléfono.
   - Verificado en 16 combinaciones de ancho × enlace profundo: la activa queda siempre visible.
   - **Tintes:** se mantienen, y ahora se derivan de los tokens con `color-mix(in srgb, campo 12 %, --carta-hoja)` (fucsia 8 %). Están documentados en `sistema.md §2.5` con su contraste (magenta ≥ 4,56, azul ≥ 6,79). Se fueron los `-fuerte` hechos a mano.
   - **Promo del miércoles:** sin la hoja blanca. El día se marca solo con ‹Hoy›.
   - **Promos:** siguen literales de CARTA-7 (no hay promo de viernes ahí) y ahora van **todas sin foto**. El sábado no tenía, y la del miércoles repetía a la garzona del Equipo.
   - **Títulos de grupo** (Picoteos, Pizzas artesanales, Cervezas sin alcohol…) en Six Caps, paso head, como pide `sistema.md §7`. Los subgrupos siguen en Oswald 600.
   - **Chips sobrios:** texto azul subrayado; el activo, en noche con papel.
9. **Fotos: hecho.**
   - **Repetición por archivo fuente (dHash + ruta):**
     - Miércoles de Hoy: P364 (clienta riendo con su vaso, IG-008) en vez de P331. La garzona del jockey queda solo en la banda del Equipo (P333).
     - Mosaico de Comida: la pizza en tránsito (P029) y la tabla de picoteo (P299) en vez de la hamburguesa y la cazuela. La cazuela (P091) era casi la misma foto que "Camarón que se duerme" (P099, dHash a 6 bits).
     - Lámina de Coctelería en la carta: P109 (bartender riendo, camisa floreada) en vez de P184.
     - Lámina de Comilona: P070 (tacos) en vez de la cazuela.
     - Resultado: 0 fuentes repetidas por página.
   - **Apertura de El lugar:** la banda "El salón" es ahora **P076**, el salón de verdad: mesas tras la reja de fierro, muro rojo, lámparas tejidas y luz ámbar. Es la mejor foto de interior sin uso del catálogo. Sale el aro de luz (P339).
     - Su archivo nativo da 1280 px, así que la banda se limita a 1280 px CSS (a 1440 queda centrada con noche a los lados, como la portada a 1920).
   - **Media pantalla muerta:** la foto líder 4:5 (P093, la barra curva) sube a las columnas 8–12, alineada con el titular. «Un lugar que fuera cálido, acogedor» y «y una gran barra, larga…» (los dos de VID-061) van debajo.
     - El bloque "La barra" desaparece (su foto ahora es la líder) y sale «Pucha que nos gusta nuestra barrita!!»: la página queda más corta.
   - **Fotos blandas:**
     - El mural va a 5 columnas (≈ 560 px de un fotograma de 960).
     - El video del letrero (1278 px) va a 5 columnas.
     - Tukulito ahora se exporta a su ancho nativo, 682 px (`media_v2.py` emite el ancho nativo del recorte cuando los estándar se quedan cortos, sin ampliar nunca), y también Coquette 854 y Viernes 819.
     - La hamburguesa salió.
   - **Miniaturas de la carta:** 240/320 w en el srcset (`extra_widths`). A DPR 1 y 2 se pide 240; a DPR 3, 320.
   - `sizes` corregidos: mosaicos de dos columnas en el teléfono (45vw), destacados (23vw), la puerta (39vw).
10. **Cuándo y dónde: hecho.**
    - La dirección aparece una vez (en la ficha). Sale el panel "SERRANO 325, CASTRO": "Ver mapa" es un enlace y el iframe aparece en 4:3 al tocarlo.
    - La puerta del megáfono arranca a la altura del titular (columnas 8–12).
    - ‹Dónde› [UI] / “Where” [EN] entra en la nav de escritorio.
    - Sale el "Cómo llegar" bajo la lámpara.
    - Los créditos de la lámpara (V014-cover) y del mural (fotograma de V031) dicen ‹Foto›. Solo el video del letrero dice ‹Video›.
11. **Accesibilidad: hecho.**
    - Con la hoja abierta, `main`, el pie, el salto, el logo, los enlaces de la nav y el botón "Ver la carta" quedan `inert` + `aria-hidden`.
    - El foco da la vuelta dentro (Tab desde "EN" vuelve a "Menú"; Mayús+Tab desde "Menú" va al último).
    - Escape devuelve el foco a "Menú".
    - Probado con 14 Tab y 3 Mayús+Tab: 0 escapes.
    - Objetivos táctiles: `.menu-b` y el "DM" corto de la carta con mínimo 44×44; enlaces de Dónde (`@almud_bar`, `@bazar_almud`) a 44 px; logo de la nav a 44 px.
    - Medido: 0 controles fuera del texto corrido bajo 44 px.
12. **"Cristal" bajo el isotipo: hecho.** Se agregó un segundo scrim radial (`.cover-title-box::after`) solo bajo la mitad inferior del isotipo, donde el letrero cruzaba el contorno. No toca caras ni la mitad alta de las cintas. A 1440 el letrero ya no se lee a través del isotipo.
13. **Archivos sin uso: hecho.**
    - Se borraron de `assets/v2/video` los videos `carta-muro-rosa*`, `carta-cazuela*` y `lugar-techo-flecos*`, y se sacaron del manifiesto.
    - Además, `publish.py` ahora publica **solo lo que se referencia**: sigue los enlaces desde las páginas a CSS/JS y de ahí a fuentes, imágenes y video, incluyendo las URLs absolutas propias (OG).
    - Prueba: 0 archivos sin uso y 0 referencias rotas.

## Jurado gráfico (7,6)
- **P1-1 a P1-3:** hechos (decisión 9).
- **P1-4, carta en el teléfono:** hecho (decisión 8). El chip activo va en noche y la pestaña activa en azul carta.
- **P2-5, tintes pastel:** **no se vuelve al papel**, por decisión del director (lo pidió el cliente). Ahora derivan estrictamente de los tokens (decisión 8).
- **P2-6, fotos blandas:** hecho (decisión 9).
- **P2-7, "Cristal":** hecho (decisión 12).
- **P2-8, Cuándo y dónde:** hecho (decisión 10).
- **P2-9, promos:** hecho en parte. Ninguna lleva foto y "Hoy" se marca solo con la etiqueta. **No** se agrega viernes: CARTA-7 no tiene promo de viernes y no se inventa (en el landing, el viernes lleva su línea de IG-003).
- **P2-10, Comilona:** hecho (títulos de grupo en Six Caps; chips sobrios).
- **P3-11, nav subrayada:** hecho. Subrayado solo al pasar o en la sección a la vista (`aria-current`, con IntersectionObserver).
- **P3-12, Hoy a 1440:** hecho en parte. La frase sube a la línea alta del ítem (`align-self: start`). La semana sigue a 7 columnas, como estaba.
- **P3-13, logo de portada a 390:** no hecho. Agrandarlo a ~330 px empuja la zona de foto y las caras; con la línea de voz nueva no cabe sin perder las acciones en pantallas bajas.
- **P3-14, mosaico del teléfono:** no hecho. Los mosaicos con texto ya alternan dos tamaños (3/4 izquierda y derecha); unificar los demás es un cambio de composición que no es barato.
- **P3-15, hueco en las filas de la carta:** no hecho. La columna de foto vacía es la regla de la fase 15 (un solo borde izquierdo por grupo).

## Jurado de redes (8,2)
- **P1-a, OG:** hecho (decisión 3).
- **P1-b, Lizze:** hecho (decisión 4). Pendiente: confirmar con el bar.
- **P2-a, "Este mes":** hecho (decisión 5).
- **P2-b, teléfono:** hecho (decisión 6).
- **P2-c, Maps:** hecho (decisión 6).
- **P2-d, voz en el hero:** hecho (decisión 7).
- **P2-e, cabecera de la carta:** hecho (decisión 8).
- **P3-a, pulseras / aro de luz:** el aro de luz salió (decisión 9). La pulsera verde en "Con amigos" (P259) se acepta; recortarla corta caras.
- **P3-b, "#1 de 6":** hecho. ‹#1 en bares de Castro› [UI] / “#1 bar in Castro”.
- **P3-c, abrir reseñas con Kevin B:** no hecho. El orden de §9 se eligió por fuente y fecha en la fase 13; cambiarlo toca el guion y la verificación de reseñas sin sumar un arreglo de los P1/P2.
- **P3-d, sábado después de las 22:00:** no hecho. La línea «de 18:00 a 22:00 hrs» es literal y dice la ventana; una variante horaria agrega lógica que ningún director pidió.
- **P3-e, media pantalla en El lugar:** hecho (decisión 9).
- **P3-f, foto de los dueños:** no hecho. No existe material confirmado (PRODUCT.md, "lo que no se fabrica").
- **P3-g, OG de /carta:** hecho (Peter con su burbuja).

## Jurado web (8,0)
- **P1-a:** hecho (decisión 1).
- **P1-b:** hecho (decisión 2). Precargas de fuentes reducidas a dos en el landing; en la carta se dejan las de cuerpo, porque sin Oswald 300 el CLS subía a 0,007.
- **P2-a, pestañas sticky:** hecho (decisión 8), con 52 px a 320 y a 390.
- **P2-b, foco fuera de la hoja:** hecho (decisión 11).
- **P2-c, OG:** hecho (decisión 3).
- **P2-d, portada a 1440@2x:** se acepta la blandura (decisión 2). Nunca más de 1440 px CSS; no hay archivo de 2048 px.
- **P2-e, objetivos táctiles:** hecho (decisión 11).
- **P3-a, miniaturas y `sizes`:** hecho (decisión 9).
- **P3-b, huecos del mosaico de El lugar a 1440:** mejora con la nueva cabecera. Los desfases del mosaico se mantienen (sistema §7).
- **P3-c, "Cómo llegar" bajo la lámpara y crédito "Video":** hecho (decisión 10).
- **P3-d, "Cuándo y dónde" en la nav:** hecho (‹Dónde›).
- **P3-e, largo del teléfono:** se acortó un poco (sale el bloque de la barra; 22 792 px a 390). Equipo y reseñas no se compactaron.
- **P3-f, video sin referencia:** hecho (decisión 13).
- **Detalle extra:** un enlace profundo de la carta (`#comilona-pizzas`) dejaba el panel enfocado, con anillo azul. Ahora se quita ese foco si no se llegó con el teclado.

## Archivos tocados
- `src-v2/index.html` y `src-v2/carta.html`.
- `tools/build_v2.py`: portada con recorte de teléfono, dos preloads, Maps, láminas, promos sin foto, pósters diferidos y `sizes`.
- `tools/media_v2.py`: `widths` y `quality` por recorte, `extra_widths` y ancho nativo.
- `tools/media_v2.json` (nuevos: `og-carta`, `hoy-miercoles-brindis`, `lugar-salon`, `comida-pizza-mano`, `comida-tabla`, `carta-lamina-barra`, recorte `m` de la portada) y `assets/v2/media.json`.
- `tools/publish.py`: solo lo referenciado.
- `css/v2/tokens.css` (tintes derivados), `site.css` y `carta.css`.
- `js/v2/site.js` (Hoy, red de seguridad de reveals, menú inerte, nav activa, pósters diferidos) y `carta.js` (borde que se desvanece, pestaña activa tras fuentes, foco del enlace profundo).
- `content/copy-v2.md`, `content/hoy-v2.json` y `content/alts-v2.json`.
- `_plan/direccion/sistema.md §2.5` y `_plan/build-v2/informe.md`.
