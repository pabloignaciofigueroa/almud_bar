# Fases 11–14 · Construcción del sitio v2: informe

Sitio nuevo, hecho desde cero sobre `tokens.css` y la lámina aprobada (portada ruta B con P189, capítulos-afiche con un campo plano por pantalla, "Hoy en Almud", la carta en papel). La v1 (`src/index.html`, `css/main.css`, `js/main.js`, `tools/build.py`) no se tocó ni se reusó: queda en el repo por historia y fuera de `public/`.

## Archivos

| Archivo | Qué es |
|---|---|
| `src-v2/index.html` | plantilla (secciones en el orden de `copy-v2.md`, textos literales marcados con su fuente) |
| `tools/build_v2.py` | build → `index.html` (raíz) |
| `css/v2/site.css` | estilos sobre `tokens.css` (sin colores, curvas ni duraciones sueltas) |
| `js/v2/site.js` | 7 KB, sin dependencias |
| `content/alts-v2.json` | alts finales ES/EN de las 49 imágenes y videos (sin nombrar eventos ni personas) |
| `content/hoy-v2.json` | guion de "Hoy en Almud" por día (literales con fuente; ítem y precio salen de `carta-v2.json`) |
| `tools/publish.py` | lista blanca v2: `index.html`, `css/v2`, `js/v2`, `vendor`, `assets/v2`, `assets/fonts`, `brand` |
| `_plan/build-v2/shoot.py` | capturas y mediciones (Playwright) |
| `_plan/build-v2/shots/final-*` | capturas finales: 390, 768, 1280×720, 1440, 1920, 390/1440 con reduced motion, 390/1440 en EN (pliegue + tramos de 3 pantallas) |

## El build (`tools/build_v2.py`)

**Qué inyecta:**
- `<picture>` con AVIF y WebP, `srcset` + `sizes`, `width`/`height`, LQIP y color dominante como fondo del `<img>`, y `object-position` desde el foco de `media.json`. La portada va `eager` + `fetchpriority="high"` y con `<link rel=preload imagesrcset>`; el resto, `lazy`.
- Videos `muted playsinline loop preload="none"`, con póster WebP, fuentes AV1/WebM + MP4 y botón de pausa.
- La carta completa desde `carta-v2.json` (10 secciones, 35 grupos, 256 ítems).
- Las 6 reseñas de §9: el recorte sale del guion, y el autor, la fuente y la fecha de `reviews.json`.
- Las seis variantes de "Hoy en Almud".
- Los créditos desde `media.json` (`post` como fuente).
- El logotipo como `<symbol>` desde `brand/almud-horizontal-claro.svg` (en `currentColor`).
- Los @ como enlaces.
- Los precios literales (`{{precio:…}}`).
- `lang="es"` en cada literal.
- Los titulares partidos en líneas con máscara.

**Falla (sale con código 1 sin escribir `index.html`) si:**
- falta un id de media, un recorte o un archivo;
- falta el alt en español o en inglés;
- hay un emoji visible;
- un texto `data-src` no es literal del guion con esa fuente;
- una glosa [EN]/[ES] o una etiqueta [UI] (o un `data-en`) no está en el guion;
- queda texto visible **sin marca** (sin fuente);
- aparece una palabra prohibida (fila o espera).

Se probó en negativo: un literal alterado, un id falso, un emoji y un texto suelto dan 4 errores.

**Etiquetas [UI] nuestras fuera del guion (`UI_EXTRA`, declaradas):** "Saltar al contenido / Skip to content", "Pausar video / Pause video", "Reproducir video / Play video", "Almud Bar" (texto oculto del h1) y el aria "Índice de la carta / Menu index".

Última corrida: 176 KB (40 KB con gzip), 37 imágenes y 6 videos. Se verificaron 220 literales, 175 glosas, 107 [UI] y 110 `data-en`.

## Qué se construyó, sección por sección

1. **Nav.** Barra plana sobre noche, sticky: 72 px en escritorio y 56 px en teléfono. Lleva el logotipo, 5 enlaces, ES/EN y [Ver la carta] en barra. En el teléfono, "Menú" abre una hoja a pantalla completa sobre noche alta: `clip-path` en 400 ms con drawer, cierre en 250 ms. Escape, el teclado y los enlaces la cierran al instante, y el foco vuelve al botón. ES/EN también va en la hoja.
2. **Portada.** P189 a 1:1 hasta 1440 px, con noche a los lados en 1920.
   - Escritorio: el ancla de la lámina (`top -19,7 %`) más un **"lift"** que sube foto y tipo juntos en pantallas bajas. Así se resuelve la decisión abierta 2: a 1280×720 las caras se ven y el tipo queda sobre la pared.
   - El scrim radial va solo detrás de cada bloque de tipo. Hubo que darle `z-index: 0` a los bloques, igual que en la lámina; sin eso no se pintaba.
   - Teléfono: el tipo queda en el 40 % inferior, bajo las caras, y el crédito sube a la esquina.
   - Bio [BIO], horario y dirección [BIO], Cómo llegar (botón barra, Google Maps con las coordenadas -42.4825681, -73.7617619) y Escríbanos al DM (`ig.me/m/almud_bar`).
   - No se anima nada en la carga.
3. **Hoy en Almud.** Un script en línea, inmediatamente después de la sección, elige el día por `America/Santiago` antes de pintar, sin corrimiento. `?dia=N` lo fuerza, para probar.
   - Campos: Mar coral · Mié turquesa · Jue fucsia · Vie amarillo (sin promo) · Sáb verde · Dom/Lun coral ("Abrimos de / Mar a Sáb" + "El martes").
   - **Sin JS** queda la variante "Abrimos de Mar a Sáb", que siempre es verdad, con la semana completa.
   - La semana marca el día con "Hoy" y `aria-current`.
   - El sábado usa P194 (alias de `media.json`) y el martes el loop V054.
   - **El momento autoral, "la franja se imprime"**, ocurre una vez al entrar: campo `clip-path inset(0 100% 0 0) → 0` en 700 ms in-out, líneas del titular en 800 ms out (+240 ms, stagger de 60 ms) y foto abriéndose de arriba abajo en 600 ms (+360 ms).
4. **El lugar** (noche). Split: titular, cuerpo y la idea de VID-061, con P093 como foto líder. La barra con la lámpara de pinzas.
   - **Mosaico desigual** (desfases 0/160/56): sillones, terraza techada y terraza, cada uno con rótulo, literal y crédito.
   - **Banda a sangre** con P339 (salón).
   - Par: el mural (fotograma V031, Proyecto @cepaz) y el loop V009, con "Nos gustan los brillitos, las luces" y Cómo llegar.
5. **Los tragos** (amarillo).
   - P297 como **marco que crece** (`clip-path inset(10%) → 0` en 800 ms out, una vez).
   - Cuerpo IG-046 e IG-021, y Coctelería de la casa con 4 tragos: nombre y precio literales de la carta, más su línea de IG.
   - Mosaico P086, P097 y P184 (con IG-045 y crédito).
   - Cierra con la banda a sangre P362, sin crédito: está por confirmar.
6. **Sin alcohol** (noche). Head «no dejamos a nadie ajuera», La moto chantá destacada y los 4 rótulos de carta enlazados a sus anclas. Sin foto, según el guion.
7. **La comida** (verde).
   - **Foto sostenida** P036, sticky en escritorio, mientras pasa el texto: cocina, 4 platos con precio, pizzas y las 6 categorías enlazadas.
   - Mosaico P305, P393 y P091.
8. **El equipo** (noche). Titular, cuerpo IG-001, los @ de IG-010 enlazados y "los papis del almud". Banda a sangre P333 con su pie IG-014.
9. **Con quién** (fucsia). Titular, IG-060 y botón noche. Dos mosaicos (desfases invertidos en el segundo) con Solo, En pareja, Con amigos, A celebrar y Sin motivo.
   - P258 y P259, que tienen flash, quedan juntas en el primer grupo.
   - P254 va sin nombre.
   - P031 queda fuera, para no pasar de 6.
10. **Reseñas** (noche).
    - Cifras [DATO] en Six Caps (4,6 · 848 · 209 · #1 de 6), con fecha oct-2026.
    - 6 reseñas en 3 + 3 en su idioma (`lang` por cita), con glosa ES en modo ES y glosa EN en modo EN.
    - En el teléfono se ven 3, más "Ver más reseñas"; sin JS se ven las 6.
11. **Eventos** (coral). Calendario de 7 filas: mes, nombre literal, línea y años. P073 al costado y mosaico P221, P348 (con crédito @isosur.prod) y P229. CTA «asegure su entrá hablándonos al DM!» y "Ver en Instagram".
12. **Cuándo y dónde** (noche). Titular, cuerpo IG-004, datos en `dl` (horario sin cierre, dirección con "Al frente del Centro Cultural", `tel:` y @almud_bar / @bazar_almud), Cómo llegar y DM. P199 y loop V031 con crédito.
13. **La carta** (papel), `#carta`.
    - Título azul, bajada IG-011 y "Carta completa" (`uqr.to/ppvi`).
    - **Índice de anclas de las 10 secciones**, sticky bajo la nav desde 700 px y en varias líneas en el teléfono: no hay scroll lateral.
    - Categorías en Six Caps head y grupos en Oswald.
    - Nombres en azul y MAYÚSCULAS. Precios magenta, tabulares y a la derecha.
    - **Columnas multiprecio** con rótulo alineado: NORMAL / CORTO XL, CORTO / GIN & TONIC… Cada precio lleva su medida en texto oculto para lectores de pantalla.
    - Notas y pies de grupo. Tags veggie / vegan / picante / nuevo con **iconos SVG de un trazo** más la palabra (EN: veggie / vegan / spicy / new).
    - Horario de las promos ("de 18:00 a 22:00 hrs") y stock en el grupo Nuestras promos.
    - Láminas sticky en escritorio: Peter, loop del muro rosa, P003, La moto chantá, Con tuti y el loop de la cazuela.
    - Jugos, cervezas 0° y calientes van en un trío.
    - Glosas EN para secciones y grupos con juego de palabras.
14. **Pie.** Firma «Que no se lo cuenten! Besiiiii» en Six Caps, datos, DM y carta, créditos de fotos y afiches, nota y ©. Cierra con el logotipo a todo el ancho.

**Tratamientos de imagen (5):**
- banda a sangre: P339, P362, P333;
- split: P093, Hoy, P199;
- mosaico desigual 4:5: ×5;
- foto sostenida: P036;
- marco que crece: P297.

Todas van en 4:5 y 16:9 (P189 en su forma original), con esquinas rectas y sin marco, sombra ni rotación.

## Decisiones

- **GSAP, ScrollTrigger y Lenis no se cargan** (siguen en `vendor/`). No queda ninguna línea de tiempo atada al scroll: todo es `once`, más un momento autoral. Emil pide CSS/WAAPI primero, y Lenis es el doble suavizado que condena la v1 (prohibido 35).
  - El movimiento es CSS con los tokens, disparado por IntersectionObserver. Son unos 110 KB menos.
  - Se observa el **padre** de cada marco, porque un blanco recortado entero por `clip-path` no cuenta como visible.
  - Al revelar, las imágenes lazy de ese marco pasan a `eager`.
- **Los estados ocultos solo los pone JS** y solo a lo que está bajo el pliegue. Sin JS, o si algo falla, todo queda visible.
  - Con reduced motion solo hay fades de opacidad de 180 ms, nada de transform ni clip, y los videos se quedan en el póster con "Reproducir video".
  - El teclado nunca anima.
  - La presión .97 aplica a todo lo presionable, y el hover solo bajo `(hover:hover) and (pointer:fine)`.
- **Videos.** Corren solo a la vista (≥25 %, IntersectionObserver) y llevan botón de pausa (WCAG 2.2.2, loops de más de 5 s). Ninguno queda en el primer pliegue del teléfono.
- **i18n.** Las glosas `.gl` las controla CSS por `html[lang]`, fijado en el `<head>` antes de pintar. Los rótulos usan `data-en`, `data-alt-en`, `data-aria-en` y `data-meta-en`.
  - Los del primer pliegue se cambian con un script en línea tras la portada.
  - Se precargan las 4 fuentes: el CLS en EN venía del cambio de Oswald 300/600 y quedó en 0.
- **Six Caps en teléfono a tracking 0.** El sistema lo permite (0…+0,03em). "nuestro barsucho" medía 362 px en una columna de 358 y se partía en 3 líneas.
- **Mapa:** solo el enlace a Google Maps con las coordenadas. No existe la imagen estática del mapa y no se fabricó.
- **Firma del pie:** se mantiene «Que no se lo cuenten! Besiiiii», porque Reseñas usa el titular principal y no el Alt 1.

## Mediciones

| Medición | Resultado |
|---|---|
| `tools/verify_copy.py` | 199/199 literales, 42/42 titulares, 0 prohibidas (exit 0) |
| `tools/validate_carta.py` | OK, todas las secciones |
| Taste `lint.mjs index.html` | **0 FAIL**, 1 WARN |
| Taste `inspect.mjs` (1440, 768, 390 y reduced) | **0 FAIL**, 1 WARN · `.taste-skill/after/` |
| CLS (9 configuraciones, carga y recorrido completo) | **0** en todas |
| LCP local (Playwright) | 100–230 ms (456 ms en 390 con reduced motion) · el elemento LCP es siempre la portada AVIF |
| LCP con 4G simulado (9 Mbps, 150 ms) y CPU ×4 | **1,04 s** a 390 · **1,40 s** a 1440 |
| Errores de consola | 0 en las 9 configuraciones |
| Desborde horizontal | ninguno (`scrollWidth` igual al ancho en todas) |
| Peso inicial transferido | ~0,6–0,7 MB a 390 · ~0,8–0,9 MB a 1440 (servidor sin gzip) |
| `index.html` | 176 KB (40 KB con gzip) |
| `site.css` | 34 KB |
| `site.js` | 7 KB |
| `public/` | 508 archivos, 42,9 MB (el mayor es `carta-muro-rosa.mp4`, 1,4 MB) |

**Las dos advertencias:**
- Lint `copy`: "more than a" es la glosa literal de IG-118 ("worth more than a thousand words").
- Inspect `palette-cream`: el papel #f6ecdc de los posavasos, defendido en `sistema.md`.

**Pruebas de interacción** (Playwright, 390): se abre el menú y el foco va al primer enlace. Escape lo cierra y devuelve el foco. Un enlace lo cierra y navega. EN desde la hoja persiste en `localStorage`. "Ver más reseñas" muestra las 3 que faltan.

**Rondas de corrección:**
1. Los reveals nunca se disparaban (clip-path y el observador), así que había marcos vacíos. En el teléfono, el logotipo quedaba sobre las caras. La foto de Hoy no cargaba dentro de la franja recortada. El precio y el nombre se desalineaban en Tragos y Comida. El aviso de stock salía duplicado en la carta.
2. En EN, un error en `dataset` cortaba todo el JS y el CLS daba 0,014 (por las fuentes). A 1280×720 el tipo caía sobre las cintas y el scrim no se pintaba.
3. Inspect dio 2 FAIL:
   - falsos eyebrows entre las secciones de la carta, porque había poco aire: se subió `padding-top` a 120–168 px;
   - "lo rico de nuestro barsucho" se partía en 3 líneas a 390: se resolvió con tracking 0, y a 1440 el titular pasó a 8 columnas.

## Pendientes

- **P189 en pantallas DPR 2:** a 1:1 en retina se ve a media resolución. Hay que pedir el original en alta (asterisco del veredicto, alternativa 3).
- **Crédito de P362:** va sin crédito hasta que se confirme @isosur.prod.
- **"@lizzearellano" o "@lizzearellanol":** cada fuente se respeta tal cual. Hay que preguntarle al bar cuál está vigente.
- **Fotos de ítem de la carta sin uso:** Cómo te voy a olvidar, Sagüer, Sangría, Coquette, Tukulito, Camarón, Topiturrón y P070 (los tacos no están en la carta). Hay una lámina por sección, no una foto por fila.
- **P031 fuera del sitio.**
- **CARTA-7:** no queda claro si "de 18:00 a 22:00 hrs" aplica a todas las promos. Se muestra como nota del grupo (duda heredada de `carta-v2.json`).
- **Captura de página completa:** a veces muestra el LQIP en la foto de Hoy (768 y 390). Es un artefacto del redimensionado de Playwright: en el viewport real la imagen carga (verificado: `complete`, AVIF de 480).
- **Falta lo que exige la compuerta de cierre:** la crítica Impeccable y la tabla Before/After de review-animations de Emil (fases 15–17), DESIGN.md, y una prueba en un teléfono real de gama media.
- **Nada se desplegó ni se subió:** `public/` está listo para el commit.

---

# Fase 15 (parte 1) · La carta sale del landing

Pedido del cliente: la carta completa no va en el landing; ahí solo destacados con foto y un botón a la carta; la carta vive en su propia página, sin pantallas blancas, con una barra fija de secciones que muestra una sección a la vez.

## Qué cambió

| Archivo | Cambio |
|---|---|
| `src-v2/carta.html` (nuevo) → `carta/index.html` | página de la carta: cabecera (logotipo → `../`, ES/EN persistente), "La carta" + bajada IG-011 + "Precios de la carta oficial, octubre 2026." + ‹Carta oficial (PDF)› (`uqr.to/ppvi`), pestañas, paneles y pie (horario, dirección, Cómo llegar, DM, PDF, Volver arriba, créditos) |
| `tools/build_v2.py` | construye las dos páginas (falla sin escribir ninguna si una falla); `<x-destacados/>`, `<x-carta-tabs/>`, `<x-carta-estado/>`; rutas `../` en la subcarpeta; el Checker literal corre en ambas |
| `src-v2/index.html` | sin la carta completa. Nueva sección **La carta (destacados)** entre La comida y El equipo. Tragos, Sin alcohol y Comida pierden sus listas de ítems (quedan titular, fotos, cuerpo y enlaces a su pestaña o grupo). Nav, Hoy, pie y capítulos enlazan a `carta/…` |
| `css/v2/carta.css` (nuevo) · `css/v2/site.css` · `css/v2/tokens.css` | estilos de la página; destacados en el landing; 6 tintes suaves + `--carta-hoja` + `--d-tab` |
| `js/v2/carta.js` (nuevo, 7 KB) | pestañas y grupos accesibles, historial, entrada |
| `content/copy-v2.md` | §6b (destacados, con fuente), §C reescrita para `carta/`, notas de fase 15 en §1, §5, §5b y §6; verify 211/211 |
| `tools/media_v2.json` · `assets/v2/media.json` · `content/alts-v2.json` | 7 assets nuevos (abajo) |
| `tools/publish.py` | lista blanca con `carta/index.html`; verifica sus referencias desde `carta/` |
| `_plan/build-v2/shoot_carta.py` | capturas y pruebas (`shots-carta/`, `r*-medidas.json`) |

## Landing: destacados
Siete productos con su mejor foto real, nombre, descripción y precio literales de `carta-v2.json` (nombre y descripción verificados como [CARTA-n]): Coctelería de la casa (Aquí te las traigo Peter, Sagüer on Faia, Sangría Foreva!), Mocktails de la casa (La moto chantá), Comilona (Tukulito Sakayama, Camarón que se duerme, Pizza dulzona). Cada rótulo enlaza a su pestaña. Botón ‹Ver la carta completa› → `carta/`. Escritorio: 3 + 1 / 3 + botón; tablet 3 columnas; teléfono foto a la izquierda y texto a la derecha.
Quedaron fuera aunque tienen foto: Cómo te voy a olvidar (720 px, de día), Coquette (desenfocada), Con tuti (la foto es anterior a la "[Versión 2.0]": lleva jamón) y Topiturrón (la foto es la versión de mango y maracuyá; la carta dice "[Reloaded]"). Siguen con su foto en `carta/`.

## carta/: pestañas
- 7 pestañas con los títulos literales: Coctelería de la casa · Cócteles del mundo mundial · Espirituosos · Vinos & espumantes · Mocktails sin alcohol (las cuatro secciones del PDF CARTA-5) · Comilona · Nuestras promos.
- Chips de grupo (filtran: un grupo a la vez) en Cócteles del mundo mundial (8), Espirituosos (6; Whiscachos lleva Blended, Irish, Single Malt y Bourbon), Mocktails sin alcohol (5) y Comilona (6). Las cortas (casa 14, vinos 15, promos 4) van enteras.
- Barra de pestañas sticky en todos los anchos (la cabecera no es fija aquí); los chips, sticky debajo. En teléfono y tablet se deslizan de lado con barra de desplazamiento fina azul/noche; la pestaña o chip activo se trae a la vista. Objetivos ≥ 44 px.
- Anclas: `#casa` … `#promos` y `#<pestaña>-<grupo>` (`#comilona-pizzas`, `#espirituosos-gin`, `#sin-alcohol-jugos`…). Clic = `pushState`; flechas = `replaceState`; atrás/adelante restaura (probado).
- **Sin corrimiento al cargar:** un script en `<head>` lee el hash y el día (America/Santiago, `?dia=N` para probar) y pone `data-tab`, `data-sub-*` y `data-dia` en `<html>`; un `<style>` generado por el build muestra solo lo elegido. Sin JS no aplica nada: las 7 secciones apiladas, pestañas y chips son anclas.
- Accesibilidad: role tablist/tab/tabpanel (también en los chips), aria-selected, tabindex itinerante, ← → ↑ ↓ Inicio Fin con activación automática, Espacio/Enter. Teclado e historial cambian al instante; ratón/toque: entrada WAAPI 200 ms opacity + 8 px con `--ease-out`; reduced motion: solo opacidad 180 ms. Si ya se bajó más allá de la barra, el panel nuevo empieza justo bajo ella (salto instantáneo, nunca un recorrido).
- Promos: la de hoy con "Hoy" y hoja `--carta-hoja`; la pestaña toma el tinte del día (como Hoy en Almud). Nota "de 18:00 a 22:00 hrs" y "* Siempre sujeto a stock! *".
- Entrada única al cargar: "La carta" y el título de la sección abierta suben por línea con máscara; fotos de ítem y láminas con el reveal de clip del landing; la firma del pie con fade.

## Tintes (WCAG AA; se ajustó el tinte, no la tinta)
| Pestaña | Tinte | Magenta | Azul | Noche |
|---|---|---|---|---|
| Coctelería de la casa | fucsia #fae7ef | 4,58 | 7,32 | 16,1 |
| Cócteles del mundo mundial | turquesa #ddf2f4 | 4,66 | 7,47 | 16,4 |
| Espirituosos | amarillo #feeec4 | 4,71 | 7,53 | 16,5 |
| Vinos & espumantes / Promos (dom-mar) | coral #fee9dd | 4,62 | 7,40 | 16,2 |
| Mocktails sin alcohol | verde #e1efde | 4,54 | 7,27 | 15,9 |
| Comilona | papel #f6ecdc | 4,63 | 7,41 | 16,3 |
| Promo de hoy | hoja #fffaf3 | 5,22 | 8,35 | 18,3 |
Chips: tinte "fuerte" con tinta noche (≥ 10,3:1); activo noche/papel (16,3). Mezclas de cada campo con blanco cálido al 10–18 %: el magenta (4,63 sobre papel) no deja oscurecer más.

## Fotos
Por ítem, solo si la foto es ese ítem: las 10 de `carta.json › img` (Peter, Cómo te voy a olvidar, Sagüer on Faia, Sangría Foreva!, Coquette, La moto chantá, Tukulito, Con tuti, Camarón, Topiturrón) + **Pizza dulzona (P310, nuevo)**: la caption IG-022 no la nombra, pero es la única pizza dulce de la carta y la foto muestra su descripción (avellana, crema, frutos rojos glaseados, almendras fileteadas, menta). Promos: martes **V054-cover (nuevo, IG-016)**, miércoles P331 (alias, IG-019: bandeja de piscolas), jueves P228.
Láminas sin nombre de ítem: casa loop V021 (muro rosa), mundo P086 (`tragos-sours`), grupo Negroni **P226 (nuevo, IG-042)**, grupo Spritz **P016 (nuevo, IG-167, @catarsis.fotografia)**, Espirituosos P003, Vinos **P191 (nuevo, IG-050, @estudiouno.prod)**, Comilona loop V052 (gredita, IG-018), grupo Pizzas **P042 (nuevo, IG-141, @catarsis.fotografia)**. En teléfono y tablet la lámina de pestaña va arriba a media columna y la de grupo después de su lista (al cambiar de chip la lista no se mueve). Descartadas: P306 "Tartufita" (562 px y no se ve pimentón), P305/P303 hamburguesas (son de carne; la Hamburguesa Almud es de lentejas), P070 tacos y P134 (fuera de carta). `media_v2.py --only …`: sin ampliar, AVIF + WebP + LQIP.

## Mediciones
| Medición | Resultado |
|---|---|
| `build_v2.py` | index.html 111 KB (218 literales, 143 glosas, 102 [UI]) · carta/index.html 115 KB (256 ítems; 13 literales, 25 glosas, 23 [UI]) |
| `verify_copy.py` | 211/211 literales, 42/42 titulares, 0 prohibidas |
| `validate_carta.py` | OK |
| Taste lint | index.html 0 FAIL, 1 WARN (el "more than a" literal de IG-118) · carta/index.html, carta.css, site.css, tokens.css, carta.js: 0 FAIL, 0 WARN |
| Taste inspect | landing 0 FAIL, 1 WARN (palette-cream) · `.taste-skill/after-f15` · carta 0 FAIL, 3 WARN · `.taste-skill/carta`: palette-cream (papel, defendido), side-scroll (la barra de pestañas deslizable que pidió el cliente), still-page "little motion" (8: es una carta para leer) |
| Consola | 0 errores en 390/768/1440, ES y EN |
| CLS | carga 0; cambios de pestaña y chip 0 en todos los anchos, **contando también los que siguen a la interacción** (ronda 1 daba 0,20 en 390 por la lámina de grupo y 0,25 en 1440 porque la columna cambiaba de ancho: resuelto con el orden en teléfono y una lámina de pestaña en Comilona) |
| Enlace profundo `#comilona-pizzas` | abre Comilona › Pizzas, con el grupo a 120–124 px del borde (bajo las barras) |
| Desborde horizontal | 0 en ambas páginas |
| Sin JS | 7 paneles a la vista |

**Rondas:** r1 (todas las capturas) → alineación de las tarjetas de destacados, corrimiento al cambiar de grupo, columna que cambiaba de ancho; r2 → la pestaña activa quedaba cortada en 768 (el scroll-snap la devolvía: fuera el snap); r3/r4 inspect "still-page" FAIL (0 → 8 elementos: reveals de fotos, máscara de títulos, lámina de video en Coctelería de la casa); r5 → las glosas EN salían en papel suave sobre el tinte (ahora tinta noche). Capturas finales: `shots-carta/r4-*` (390, 768, 1440, ES y EN, cada pestaña, chips Pizzas y Gin, enlace profundo, sin JS) y `r5-*` (390 tras la corrección de glosas).

## Notas
- `public/` se generó para probar (537 archivos, 44,0 MB, `carta/` incluida) y se restauró al HEAD (sigue en v1). Nada se commiteó ni se subió.
- "Mocktails sin alcohol" se usa como título de la pestaña que reúne las cuatro secciones de CARTA-5 (es el título de esa carta). Glosa EN nueva: “Alcohol-free mocktails & drinks”.
- Pendiente: confirmar con el bar si la foto de Con tuti y la de Topiturrón siguen sirviendo para la versión actual; la crítica Impeccable y la tabla de Emil de la compuerta de cierre incluyen ahora esta página.

## Fase 15 · Ronda de arreglos de la crítica 1 (resumen; detalle en `_plan/critica-1/respuesta.md`)

- **P189 en retina (asterisco vigente).** No hay original en alta por ahora. La portada sigue sirviendo el archivo nativo (máx. 1440 px de ancho) y nunca se muestra a más de 1440 px CSS (`--photo-max`); a DPR 1 es 1:1. A DPR ≥ 2 el navegador usa el mismo 1440w y la foto se ve a media resolución: **no tiene arreglo sin el original**. Se deja la portada como está y el original en alta queda como requisito antes de mostrársela al cliente.
- Orden del landing según el brief: Portada, Hoy, El lugar, Los tragos (+ Sin alcohol), La comida, La carta (destacados), Con quién, **El equipo**, Reseñas, Eventos, Cuándo y dónde, pie.
- Medios nuevos: `hoy-jueves-fiesta` (P084, IG-082, 4:5 hasta 1280, sin ampliar); `hoy-sabado` pasa a alias de `con-quien-barra` (P031). Ninguna foto se repite en el landing, en ninguno de los seis estados del día (verificado por id de medio).
- `lugar-techo-flecos` (el único video solo MP4) sale del landing: ya no hay ningún pedido a un WebM inexistente ni un loop que no corre.
- Etiquetas [UI] nuevas, declaradas en el guion: ‹Este mes›, ‹Próximo›, ‹Ver mapa›, ‹Mapa: Serrano 325, Castro› (título del iframe), ‹Inicio›, ‹DM›. Literal nuevo: «Viernes» [IG-003] en la semana.
