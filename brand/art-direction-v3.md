# Dirección de arte v3 · Almud Bar

Fase 8 del plan v3. Manda sobre `brand/art-direction.md` (v1).
Boceto funcional: `v3/index.html` + `css/v3/site.css` + `js/v3/site.js` (generado por `tools/boceto_v3.py` desde `assets/v3/media.json`).
Capturas: `_plan/v3/boceto/` · hojas `_plan/v3/08-boceto-390.jpg` y `_plan/v3/08-boceto-1440.jpg`.

## Idea

**Entrar a Almud un viernes.** La puerta es el almud: su boca se abre y adentro está el bar encendido. Después, el recorrido es el del cliente: el lugar, la barra (tragos), la cocina, la gente, las fiestas, el equipo, lo que dicen de nosotros y cómo llegar.

- La noche marrón (`--noche`) es el piso; el color lo ponen las fotos y los videos, no la interfaz.
- Tres pantallas cambian de luz, como cuando uno pasa de una sala a otra: **muro** (Tragos), **noche-2 con ámbar** (Comida) y **tinta** (Eventos).
- Texto mínimo: 1 titular literal por pantalla, todo de `content/copy-v3.md`. Las fotos y los loops hablan.
- Nada de flecos dibujados, polaroids, pinzas decorativas, rotaciones, emojis ni Six Caps. El logo es siempre SVG (`brand/v3/*-claro.svg`).

## El momento memorable (uno solo)

**El isotipo que se abre al video**, al cargar (no depende del scroll):

1. 0,0–0,8 s: sobre negro se dibujan las líneas del isotipo (trazo papel, `stroke-dashoffset`).
2. 0,5–1,05 s: la **boca del almud** (el rombo interior) se llena con el video de portada que ya está corriendo.
3. 1,0–2,05 s: la boca se abre hasta la pantalla completa (`clip-path` de 8 vértices, `expo.inOut`), mientras las líneas del isotipo pasan "por al lado de la cámara" (escala 5,5 y se desvanecen). Sin texto encima.
4. 1,7–2,6 s: entra el logotipo con máscara de izquierda a derecha, luego el claim y el botón.

Duración total ≈ 2,6 s. Con `prefers-reduced-motion` o sin JS no hay intro: la portada aparece tal cual. Si el JS falla, un respaldo CSS deja todo visible a los 3,6 s. Por qué esta idea y no otra: el almud es la medida chilota que le da nombre al bar, y su boca abierta es literalmente "lo que se llena": la única vez que la marca se anima, y lo hace para dejar ver el bar real.

## Sistema de movimiento

| Pieza | Qué hace | Curva / tiempo |
|---|---|---|
| Titulares | cada palabra sube desde una máscara (`yPercent 110 → 0`), una vez | `expo.out` 1,05 s, desfase 0,045 s |
| Fotos y loops | revelado con máscara de abajo hacia arriba (`clip-path inset`) + la imagen baja de escala 1,18 → 1 | `expo.out` 1,15 s / 1,6 s |
| Textos chicos | suben 26 px y aparecen | `expo.out` 0,9 s |
| Parallax (≥768 px) | masas a distinta velocidad con `data-speed` (−0,16 … +0,22) | `scrub`, lineal |
| El lugar (≥1024 px) | galería horizontal en un contenedor **sticky** (sin pin): el scroll vertical la desplaza | `scrub .6` |
| El lugar, Equipo, Reseñas (celular) | carrusel con el dedo (`scroll-snap`), nunca atado al scroll | nativo |
| Hover (escritorio) | la foto crece 4 % | `cubic-bezier(.16,1,.3,1)` 1,1 s |

- Lenis solo con mouse/trackpad; en táctil, scroll nativo. `ScrollTrigger` sincronizado con Lenis; nada de `pin`.
- **Videos**: `autoplay muted loop playsinline` + póster. El JS solo les pone la fuente (portada: la variante visible, `portada-celular` <768 px y `portada-escritorio` ≥768 px; el resto al evento `load`). Nunca se pausan ni se reproducen por scroll ni por `IntersectionObserver`.
- Todo se anima con `transform`, `opacity` y `clip-path`: CLS medido = 0.

## Ritmo pantalla por pantalla

Alto medido: celular 390×844 ≈ **10,5 pantallas**; escritorio 1440×900 ≈ 15,3 (incluye el recorrido de la galería sticky).

### Celular (390 px)

```
┌──────────────────────┐ 1 PORTADA · noche · 100svh
│ (isotipo→video)  CARTA EN│ video portada-celular (muro rosa de botellas)
│                      │
│ ALMUD BAR [iso]      │ logotipo SVG claro
│ Coctelería de autor… │ claim [BIO]
│          [VER LA CARTA]│ botón rosa a la derecha
└──────────────────────┘
┌──────────────────────┐ 2 EL LUGAR · noche · ~1,5 pant.
│ SOMOS INQUIETOS Y    │ titular 44 px, 3 líneas
│ NOS GUSTA EL COLORSSSS!│
│ ▓▓ loop cintas 4:5 ▓▓│ lugar-cintas
│ [barra][techada][…]→ │ swipe: Barra · Terraza techada · (salón) ·
│ BARRA / línea        │ Terraza · Lámparas · Ojo Piojo
└──────────────────────┘
┌──────────────────────┐ 3 TRAGOS · muro #a8222d · ~1,5 pant.
│ MUCHO AMOR, COLOR Y  │
│ TRABAJO              │
│ ▓ loop humo 4:5 ▓    │ = «Aquí te las traigo Peter» $ 6.700
│ [Sagüer] [Sangría↓]  │ 2 tarjetas desfasadas
│ ── MOCKTAILS ─────── │ moto chantá + «no dejamos a nadie ajuera»
└──────────────────────┘
┌──────────────────────┐ 4 COMIDA · noche-2, titular ámbar · ~1,4 pant.
│ UNA COCINA SENCILLA… │
│ ▓ loop cazuela 4:5 ▓ │
│ [tukulito] [pizza↓]  │
│ TUKULITO ……… $15.900 │ lista tipo carta, puntos ámbar
│ CAMARÓN… ……… $15.900 │
│ PIZZA DULZONA $12.500│
└──────────────────────┘
┌──────────────────────┐ 5 CON QUIÉN · noche · ~1 pant.
│ NO SOMOS NÁ SIN      │
│ USTEDES!             │ 2 columnas desfasadas, 4 fotos de gente
└──────────────────────┘
┌──────────────────────┐ 6 EVENTOS · tinta + fotos · ~1 pant.
│ TIRAR LA CASA POR LA │
│ VENTANA!             │ 2×2: FEB 14F · JUL ANIVERSARIO ·
│ [14F][Aniv.]         │ SEP FONDITA · OCT JALOGÜÍN (solo mes + nombre)
│ [Fondita][Jalogüín]  │
└──────────────────────┘
┌──────────────────────┐ 7 EQUIPO · noche · ~0,8 pant.
│ PEAZO DE EQUIPO QUE  │ swipe de 5 retratos 4:5 con su @
│ TENEMOS!  [■][■]→    │ LOS DUEÑOS @cepaz · @rusio_mezclao
└──────────────────────┘
┌──────────────────────┐ 8 RESEÑAS · noche-2 · ~0,8 pant.
│ QUE NO SE LO CUENTEN │ + glosa EN siempre visible
│ [«Super soirée…»]→   │ swipe de 6 citas (fr/en/es), borde rosa
└──────────────────────┘
┌──────────────────────┐ 9 CUÁNDO Y DÓNDE · noche · ~1,2 pant.
│ ▓ loop letrero ▓     │ 52svh
│ LE ESPERAMOS DESDE   │
│ LAS 18:00 HRS        │
│ MAR A SÁB            │
│ SERRANO 325, CASTRO  │ + «Al frente del Centro Cultural…»
│ [ESCRÍBENOS POR DM]  │ rosa
│ [CÓMO LLEGAR]        │ contorno
└──────────────────────┘
┌──────────────────────┐ 10 PIE · noche · ~0,8 pant.
│ USTÉ SE LO MERECE!   │ display rosa (firma)
│ [logo vertical]      │ ALMUD papel + BAR azul
│ IMÁGENES @… @…       │
└──────────────────────┘
```

### Escritorio (1440 px)

```
1 PORTADA  ┌───────────────────────────────────────────────┐
           │ video portada-escritorio (cintas→ojos→pinzas)  │
           │ ALMUD BAR [iso] (grande)        claim (derecha)│
           │                                 [VER LA CARTA] │
           └───────────────────────────────────────────────┘
2 EL LUGAR ┌──────────────┬────────┬──────────────────┐
           │   [sillones]↑ (masa rápida)  │ loop cintas 82vh │
           │ SOMOS INQUIETOS…             │   (masa lenta)   │
           └──────────────────────────────┴──────────────────┘
           sticky 100vh → galería horizontal (6 rincones, alternan ±5vh)
3 TRAGOS   ┌───────────────┬─────────────────────────────┐ muro
           │ MUCHO AMOR…   │ [Sagüer]   [Sangría ↓16vh]  │
           │ ▓ Peter loop ▓│ ── mocktails: moto + línea  │
4 COMIDA   ┌───────────────────────┬──────────────────┐ noche-2
           │ UNA COCINA… (ámbar)   │ loop cazuela 84vh │
           │ [tukulito][pizza ↓]   │                   │
           │ lista carta 3 ítems   │                   │
5 CON QUIÉN  titular a todo el ancho + 3 columnas a 3 velocidades
6 EVENTOS    tinta · 4 tarjetas, pares bajan 9vh · solo mes + nombre
7 EQUIPO     5 retratos en fila + línea de dueños, pares bajan 8vh
8 RESEÑAS    grilla 3×2, la columna del medio baja 5vh
9 DÓNDE    ┌───────────────────────────┬─────────────────┐
           │ loop letrero (100vh)      │ LE ESPERAMOS…   │
           │                           │ datos + 2 botones│
10 PIE       USTÉ SE LO MERECE! (180 px máx.) · logo vertical · créditos
```

## Color por pantalla

| # | Pantalla | Fondo | Acento (1–2) | Medio |
|---|---|---|---|---|
| 1 | Portada | video + velo noche | muro-rosa (botón), letrero-azul (BAR del logo) | `portada-celular` / `portada-escritorio` |
| 2 | El lugar | noche | — (color de las fotos) | `lugar-cintas`, barra, techada, salón, terraza, pinzas, Ojo Piojo, sillones (escr.) |
| 3 | Tragos | muro | papel, muro-2 | `tragos-humo`, `carta-saguer`, `carta-sangria`, `carta-moto` |
| 4 | Comida | noche-2 | ámbar (titular y puntos) | `comida-cazuela`, `carta-tukulito`, `comida-pizza` |
| 5 | Con quién | noche | — | 6 fotos `con-quien-*` (4 en celular) |
| 6 | Eventos | tinta (siempre con foto) | tinta-2 (mes) | `eventos-14f`, `-12-anos`, `-fondita`, `-jaloguin` |
| 7 | Equipo | noche | papel-2 (@) | 6 retratos `equipo-*` |
| 8 | Reseñas | noche-2 | muro-rosa (filete) | — |
| 9 | Dónde | noche | muro-rosa (DM) | `donde-letrero` |
| 10 | Pie | noche | muro-rosa (firma), letrero-azul (BAR) | logo vertical |

## Tipo y botones (Carmen P)
Titulares Big Shoulders 800 mayúsculas, 44 px en celular (≤ 3 líneas), tope 120 px en escritorio, lh 0,93. Texto Barlow Condensed 500 18/20 px · 1,5; nada bajo 16 px; rótulos 600 15 px +0,06 em; precios 600 20 px en papel. Botones radio 4 px, 600 17 px, 52 px de alto: **Ver la carta** (portada, sola y a la derecha) · **Escríbenos por DM** y **Cómo llegar** (solo en Cuándo y dónde). Sin RESERVAR.

## Ronda tras el juicio de Carmen (15/20)
- Eventos: sin «Próximo»; el calendario es solo mes + nombre (recuerdo, en pasado).
- Acentos: la máscara de cada palabra tiene aire arriba (padding .26 em) y queda `overflow:visible` al terminar; revisado a 320/390/768/1440.
- Peter: en celular, loop al 62 % con nombre y precio al lado (la copa entera cabe en una pantalla con el titular).
- Comida: la pizza servida P036 es la imagen principal; la cazuela queda como loop chico, junto al Tukulito.
- 14F: cuadro de 18,6 s del reel «El 14F estuvo hermoso!» (C3tFEcvJ80x): una clienta riendo con el trago. Reprocesado con `tools/media_v3.py`.
- El lugar: Sillones (P114) entra al carrusel entre Salón y Terraza, con el rótulo [UI] ‹Sillones› / “Lounge”. La masa del encabezado de escritorio pasa a ser el muro de cuadros (P012).
- Con quién: la primera foto (P254) va cuadrada y anclada abajo, sin la franja de repisa. En escritorio las columnas se compensan para que terminen parejas.
- Equipo: sale @elymar_bocarejo (solo hay foto disfrazada). Bajo el carrusel va ‹Los dueños› @cepaz · @rusio_mezclao.
- Ritmo: padding de sección de 72 px en celular y 96 px en escritorio; El lugar y Comida pasan a dos columnas recién desde 1024 px.
- Portada celular: el loop arranca en 1,5 s, con el cartelito ALMUD BAR sobre el muro rosa (900 px, 1,35 MB).
- La portada sigue con logo, claim y ‹Ver la carta›, sin horario ni dirección (decisión del cliente).

## Decisiones y pendientes
- Portada: solo logo, claim y ‹Ver la carta› (corrección del cliente); horario y dirección viven en Cuándo y dónde.
- Comida: las fotos son ambiente y la **lista** nombra los platos, porque no hay foto propia confirmada de la Pizza dulzona (no se inventa la relación foto-plato).
- Créditos del pie: solo autores usados (@catarsis.fotografia, @estudiouno.prod, @isosur.prod, @rober.patagonico). Salen @tamillanquileo y @dosistudio (sus imágenes no se usan).
- Mapa embebido: no va en el boceto; ‹Cómo llegar› abre Google Maps. Si se quiere el mapa al tocar, se agrega en fase 14.
- El `<video>` de portada oculto (la otra variante) queda sin fuente y en pausa a propósito: no se descarga.
- EN: etiquetas [UI] cambian; los literales quedan en español con glosa debajo; clave `almud-idioma`.

## Construcción (fases 9–14)
- Detalles de Carmen r2 (escritorio):
  - Comida: la pizza se estira a todo el alto de la columna izquierda, así que las dos columnas terminan parejas.
  - Cuándo y dónde: el loop del letrero se recortó a 0–1,6 s (boomerang, solo el letrero encendido) y va anclado arriba (`object-position 50% 30%`).
  - Equipo: «Los dueños» va a 16 px (los @ a 18 px), alineado con el carrusel.
- Técnica:
  - El CSS y el JS se cargan con `?v=<md5>`, que calculan los generadores, así el celular nunca usa una versión vieja en caché.
  - `<html lang="es">`, favicon `brand/v3/favicon.svg`, OG/Twitter con la imagen absoluta `https://almudbar.pages.dev/assets/v3/og.jpg` y canonical.
  - Todas las imágenes llevan `data-alt-en` y todos los videos `data-aria-en`.
- Carta: `v3/carta/index.html`, generada por `tools/carta_v3.py` desde `content/carta-v2.json`, con `css/v3/carta.css` y `js/v3/carta.js`.
  - Header con logo → `/v3/`, ‹Escríbenos por DM› y EN.
  - 7 pestañas fijas (sticky) bajo el header; cada una muestra solo su sección. Sin alcohol reúne Mocktails, Jugos, Cervezas sin alcohol y Bebidas calientes.
  - Las secciones largas tienen subgrupos filtrables (chips); los subgrupos de Whiscachos van dentro de su chip.
  - Cada pestaña tiñe el fondo con `color-mix` de la paleta: muro, rosa, ámbar, vino, tinta, ámbar 2 y dorado.
  - Fotos propias `carta-*` y el loop de Peter. Nombres, descripciones y precios literales; las etiquetas son Nuevo, Veggie, Vegan y Picante.
  - Abajo: «* Siempre sujeto a stock! *» (en Promos), ‹Carta oficial (PDF)› → uqr.to/ppvi e ‹Inicio›.
  - Sin JS, todo se ve apilado. Todos los «Ver la carta» y «Carta» de `/v3/` llevan a `carta/`.

## Ronda 1 de calidad (imágenes y video 13, carta 14, color 16, voz 17)
- **Videos:**
  - La portada se elige por **orientación**: vertical → `portada-celular` 720×1280, 948 KB; horizontal (≥768 px) → `portada-escritorio`. La conecta un script en línea, con póster diferido.
  - `portada-escritorio` arranca en las lámparas de pinzas de noche. Lleva velo más oscuro arriba y `contrast/saturate` suaves. Sobre 1.664 px queda centrada a ≤1,3x, con viñeta.
  - El resto de los videos se conecta una sola vez, cuando entra a 0,15 pantallas del viewport (IO solo para cargar, nunca pausa).
  - Con movimiento reducido: solo póster.
  - Primer pantallazo del celular: 1,49 MB.
- **Fotos:**
  - Tragos usa las favoritas de Carmen: splash P297, sours P086 y copa tallada P097 (esta solo en escritorio). Sagüer y Sangría van como lista.
  - En Comida, la pizza se muestra 4:5 con `sizes` corregido y la lista nombra «Huerta sabrosa».
  - Con quién sin `con-quien-amigas`.
  - Tragos, El lugar y Cuándo y dónde pasan a dos columnas recién desde 1024 px.
- **Carta:**
  - Hoja de papel con nombres en `--letrero-azul-tinta`, cinta `--tinta` en los grupos y precios en noche. Cada pestaña tiñe la hoja con un tinte de la paleta al 4–30 % (AA verificado: rosa-tinta ≥4,5 en todas).
  - Cabezal compacto. Chips fijos bajo las pestañas, y tocar un chip vuelve al inicio. Las pestañas deslizan con fundido en los bordes.
  - EN en pestañas, chips, días y notas de precio. Etiquetas a 16 px.
  - Pie: DM rosa; PDF e Inicio en contorno.
  - BAR del logo en `--letrero-azul`.
- **Textos:** reseñas con “See for yourself” (solo EN), glosas con mayúscula, destacados con ancla a su pestaña o subgrupo, la nav cambia antes (sin solape con «Ver la carta») y «LE» ya no queda huérfano. `content/copy-v3.md` refleja el sitio.
- **Pendiente:** `equipo-eduardo`. El jockey toca el borde superior en la foto original (el recorte ya parte en y=0), así que no hay aire que ganar sin otra foto.

## Ronda 2 de calidad (voz 18, color 17, carta 16, imágenes y video 16)
- **Portada celular:** nuevo loop V020 (IG C-YrpVjpCqN). Es un plano continuo de 2,85–5,35 s en boomerang (4,9 s), 720×1280 y 933 KB: el muro rosa de botellas con la lámpara tejida y gente en la barra. Ya no salen las botellas con marcas en primer plano. El póster es el primer cuadro.
- **Portada escritorio:** sin el mural de ojos. Solo lámparas de pinzas y cintas, en boomerang de 6,7 s.
- **Primer pantallazo del celular:** 1.444 KB con los textos comprimidos con gzip, como los sirve Cloudflare (1.596 KB sin comprimir en el servidor local).
- **Tragos:** P362, el bartender frente al muro rosa con el cartelito ALMUD, es la foto grande de la sección (`tragos-bartender`, nueva en `media_v3.json`). Sale la copa tallada.
- **El lugar:** `sizes` 76vw/44vw/60vh y sin `lugar-cuadros`.
- **Eventos:** sale 14F. Aniversario usa P073 (el «10» de flores) y la foto de los 12 años va grande y sin rótulo. Calendario de 3 fechas.
- **Carta:**
  - Las medidas (Espirituosos, Vermú…) van en tabla, con las cabeceras literales del PDF.
  - Pestañas: en escritorio entran las 7; en celular encajan por elemento, con fundido de 64 px. El chip activo queda visible al entrar por enlace.
  - Hoja de 880 px en escritorio. La glosa EN del subtítulo va en línea propia y hay un solo DM (el de la nav).
  - Color: nombres `#3a3ad8`, solo en la hoja (≥5,81). Tres tintes cálidos (papel, rosa 7 %, dorado 12 %). «NUEVO» y los días van en `#b01a2e` (≥5,32) y los precios en negro.
- **Guía de voz:** `brand-voice-v3 §4` exime nombres, descripciones y notas impresas de la carta.
