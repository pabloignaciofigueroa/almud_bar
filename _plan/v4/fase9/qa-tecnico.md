# QA técnico · /nueva_v9/ y /nueva/carta/ (fase 9)

2026-10-23 · Playwright con Chromium headless (`/opt/pw-browsers`), servidor local `127.0.0.1:8913` con gzip y Range sobre `public/`. Solo medí; no se editó el sitio.
Entorno: 2 CPU, GPU SwiftShader (render por software), VP9 decodificado por software, sin H.264 y sin red externa. Por eso Google Maps, Instagram y uqr.to no se verificaron. Los scripts están en el scratchpad de la sesión (`qa_widths.py`, `qa_videos.py`, `qa_inter.py`, `qa_a11y.py`, `qa_rm.py`, `qa_perf.py` y `contraste_v9.py`, que es `tools/contraste_v4.py` apuntado a `/nueva_v9/` y con un recorrido de la página antes de medir).

**Veredicto: no hay bloqueantes técnicos.** No hay errores JS ni 4xx/5xx, no hay desborde horizontal y el CLS es 0 en los 8 anchos × ES/EN. Los 13 videos visibles corren y la ruleta, el carrusel, la baraja, el slider, las tarjetas y las reseñas responden al toque, al mouse y al teclado. Antes de publicar como principal hay que reescribir las rutas de `/nueva/…` (ver §7).

---

## 1 · Resultados por ancho

Medición con carga, 4 s sin tocar nada (CLS «carga») y luego un recorrido programático de toda la página sin input (CLS «recorrido»). En «textos < 16 px» se cuenta cada nodo de texto visible con `font-size` < 16. Para validar el observador de CLS hice un control: al empujar 200 px el contenido, mide 0,237.

| Ancho × alto | Página | Errores JS ES/EN | 4xx/5xx | Desborde (scrollWidth / scrollX) | CLS carga · recorrido | Textos < 16 px | Alto ES/EN |
|---|---|---|---|---|---|---|---|
| 360×780 | v9 | 0 / 0 | 0 | 360 / 0 ✔ | 0 · 0 | 0 | 13 081 / 13 789 |
| 390×844 | v9 | 0 / 0 | 0 | 390 / 0 ✔ | 0 · 0 | 0 | 13 755 / 14 470 |
| 412×915 | v9 | 0 / 0 | 0 | 412 / 0 ✔ | 0 · 0 | 0 | 14 260 / 14 932 |
| 768×1024 | v9 | 0 / 0 | 0 | 768 / 0 ✔ | 0 · 0 | 0 | 18 857 / 19 383 |
| 1024×768 | v9 | 0 / 0 | 0 | 1024 / 0 ✔ | 0 · 0 | 0 | 11 319 / 11 639 |
| 1280×800 | v9 | 0 / 0 | 0 | 1280 / 0 ✔ | 0 · 0 | 0 | 12 435 / 12 729 |
| 1440×900 | v9 | 0 / 0 | 0 | 1440 / 0 ✔ | 0 · 0 | 0 | 13 647 / 13 926 |
| 1920×1080 | v9 | 0 / 0 | 0 | 1920 / 0 ✔ | 0 · 0 | 0 | 15 265 / 15 541 |
| 360 → 1920 (los 8) | carta | 0 / 0 | 0 | ✔ en todos | 0 · 0 | **3** (en los 8 anchos) | 2 268 – 4 331 |

Textos bajo 16 px en la carta, todos de 15 px: `nav .nav__dm` («Escríbenos por DM» / «Message us on Instagram»), el `span` del botón de idioma (EN/ES) y `h2.panel__t` («Coctelería de la casa»). La home v9 no tiene ninguno.

Nota: a 768 la página mide 18 857 px, 37 % más que a 390. Es una observación de diseño, no un fallo técnico.

## 2 · Videos (390, 768 y 1440)

- **Primer pantallazo sin scroll:** la portada que corresponde (celular a 390/768, escritorio a 1440) tiene `paused=false` y su `currentTime` avanza unos 1,5 s en 1,5 s. ✔
- **En pantalla tras `scrollIntoView`:** los 13 videos de contenido, Jalogüín incluido (se llega a él con su indicador del slider), dan `paused=false`, `readyState 4` y avanzan unos 1,2 s en 1,2 s. Los valores negativos que salen en la medición son el loop que vuelve a empezar. A 1440, `quien-multitud-1` aparece con `readyState 2` pero igual avanza 1,04 s. ✔ El video de portada que no corresponde al ancho queda sin cargar, que es lo correcto.
- **Ningún video está atado al scroll:** intercepté `currentTime=` y `pause()` desde un init script y no hubo ni una llamada. Al hacer scroll ±200 px el tiempo avanza en forma lineal (+0,16 s cada 150 ms). ✔
- **Pósters:** todos los videos que se cargan tienen `poster`. ✔
- **Proporción:** ninguno se deforma, porque todos usan `object-fit: cover`. Recortes medidos:

| Video | Caja / video | Recorte |
|---|---|---|
| 11 videos de sección (lugar, tragos, comida, quien ×3, eventos-fiesta, equipo, donde) | idéntica (0,800 / 0,800; 0,562 / 0,562; 1 / 1) | 0 % |
| eventos-jaloguin-540 | 0,825 / 0,801 | ~3 % del alto |
| Portada celular a 360 / 390 / 412 | 0,46 · 0,46 · 0,45 / 0,5625 | 18–20 % del ancho |
| Portada celular a 768×1024 (vertical) | 0,75 / 0,5625 | **25 % del alto** |
| Portada escritorio a 1024×768 | 1,333 / 1,775 | **25 % del ancho** |
| Portada escritorio a 1280 / 1440 | 1,60 / 1,775 | 10 % |
| Portada escritorio a 1920×1080 | 1,778 / 1,775 | 0 % |

El recorte de la portada viene de su diseño a pantalla completa (`100svh`). Lo dejo anotado porque a 768 y 1024 se pierde una cuarta parte del encuadre.

## 3 · Interacciones (390 táctil con `Input.dispatchTouchEvent`; 1440 con mouse y rueda)

| Componente | 390 táctil | 1440 mouse | ¿Un deslizamiento vertical mueve la página? |
|---|---|---|---|
| Intro en negro | Entra en negro (luminancia media 16/255 a 0,3 s, clip-path de la boca activo). Toque, swipe o tecla la saltan al tiro (progress → 1 en 200 ms). Sin tocar nada dura 2,85 s. ✔ | Luminancia 15/255. Rueda, clic y tecla la saltan. ✔ | El swipe la salta y además desplaza ✔ |
| Ruleta de rincones | Swipe −260 px → x −617; flecha → −925 ✔ | Arrastre → −416; flecha → −833 ✔ | 285 px ✔ / rueda 300 px ✔ |
| Carrusel de tragos | Swipe → −295; flecha → −590 ✔ | Arrastre → −367; flecha → −735 ✔ | 285 px ✔ / 300 px ✔ |
| Baraja «Con quién» (15 lanzamientos alternando lados) | Las 12 cartas siempre visibles, siempre un solo `.is-top`, 15/15 cambios. La región viva cuenta 2 → 12 → 1 → 4 (da la vuelta). **Nunca se vacía** ✔ | Ídem ✔ | 402 px ✔ / 300 px ✔ |
| Slider de fiestas | Avanza solo (0 → 1 a los 5,6 s). Arrastre izq. → 2, der. → 1, flecha → 2. Fuera de pantalla se pausa (sigue en 2 después de 6 s) ✔ | Ídem ✔ | 285 px ✔ / 300 px ✔ |
| Tarjetas del equipo (6) | Un toque las gira (`is-on`, rotateY 180°) y otro las devuelve ✔. Con teclado, al enfocar su @ las 6 giran −180° ✔ | Clic, hover y foco ✔ | 354 px ✔ / 300 px ✔ |
| Reseñas (2 cintas) | Avanzan solas (unos 37 px/s), se detienen con el foco y se arrastran (−222 px) ✔ | Avanzan solas, se detienen con hover y con foco y se arrastran ✔ | 285 px ✔ / 300 px ✔ |
| Mapa | El iframe está desde la carga (`loading=lazy`, 358×320) y su title es correcto en ES ✔ | 547×360 ✔ | 208 px sobre el iframe vacío (sin red). No pude verificar el gesto sobre el embed real de Google ⚠ |

No hubo `pageerror` en ninguna corrida.

## 4 · prefers-reduced-motion y sin JS (390 y 1440, ES y EN)

- **Movimiento reducido:** no hay intro (la clase `intro` no se pone) y ningún video corre; todos muestran su póster (13/13, la portada del otro ancho queda sin cargar como corresponde). Se cargaron las 53 imágenes. Sin desborde. El slider pasa a 3 fichas apiladas (1 110 px a 390) y la baraja a 12 fotos en grilla. Contenido completo ✔.
  Los textos de la ruleta de rincones que quedan a la derecha (Sillones, Terraza, Lámparas, Ojo Piojo) están en un contenedor con `overflow:hidden`. Se llega a ellos arrastrando o con las flechas, porque la ruleta sigue activa (sin el giro de entrada). Es aceptable.
- **Sin JS:** los `<noscript>` reemplazan las 53 fotos diferidas y los 14 videos por sus pósters. Las capturas de página completa (`noscript-390`, `reduce-390`) se ven completas y legibles en todas las secciones, de la portada a los créditos. No hay textos ocultos ni opacos ni desborde ✔.
- **Carta:** con movimiento reducido o sin JS se lee completa. Las pestañas ocultan los paneles que no están activos, que es su diseño. Hay 4 fotos `loading=lazy` dentro de pestañas ocultas que no se cargan hasta que se abre su pestaña, lo que es esperado.

## 5 · Accesibilidad básica

- **lang:** `<html lang="es">` pasa a `en` con el botón. Las 48 glosas EN llevan `lang="en"` y las reseñas sus `lang` fr/es/en ✔.
- **Alt y nombres:** las 53 `img` tienen `alt` y ninguno está vacío fuera de `aria-hidden`. Los 46 controles tienen nombre accesible. Los 14 videos tienen `aria-label`, también en EN ✔. No hay elementos enfocables dentro de `aria-hidden` (los clones de las reseñas quedan fuera del tab) ✔.
- **Foco visible:** contorno de 2 px `#2AA1F8` en todos los controles, salvo el iframe del mapa (ver fallos).
- **Orden de tabulación (45 paradas):** salto → logo → EN → Carta → «Ver la carta» → ruleta → carrusel de tragos (5 tarjetas) → La moto chantá → «Ver la carta completa» → comida (8 platos) → «Ver la carta completa» → baraja → slider + 3 indicadores → 9 @ del equipo → reseñas → DM → mapa → «Abrir en Google Maps» → 4 créditos. Sigue el orden de las secciones ✔. Dentro de Comida y Equipo el orden es el del DOM y no la lectura visual: a 1440 salta arriba y abajo (y: 5759 → 6347 → 6297 → 6730 → 6694…) ⚠.
- **Contraste** (`contraste_v9.py`, 390 y 1440, ES y EN, v9 y carta): se midieron 1 182 textos y **ninguno queda bajo el mínimo AA** ✔. El texto sobre foto o video no lo mide la herramienta.

## 6 · Rendimiento

| Medida | Resultado | Meta |
|---|---|---|
| Primer pantallazo a 390 (DPR 2 y 3, gzip, 9 s sin scroll) | **1 483 KiB** (1,52 MB decimales) en 12 peticiones: video de portada 1 248, fuentes 78, JS 63, póster 40, HTML 37, CSS 16 | ≤ 1,5 MB: cumple en MiB y queda **2 % sobre la meta** si se lee en MB decimales ⚠ |
| Primer pantallazo a 1440 | 3 861 KiB: portada escritorio 2 424 y **lugar-noche 1 181** (entra por el `rootMargin` del 15 %) | — |
| LCP a 390 con 4G lento (1,6 Mbps, RTT 150 ms) y CPU ×4, 3 corridas | **Mediana 2 088 ms** (2 080–2 100). El elemento LCP es `p.hero__claim`; FCP 1,2–1,4 s | ≤ 2,5 s ✔ |
| Scroll a 390 con CPU ×4 (6 000 px táctil) | 60,2 fps, p95 16,7 ms, 0 cuadros de más de 33 ms. Igual con los videos detenidos | ✔ |
| Baraja a 390 con CPU ×4 (8 lanzamientos) | **48 fps con videos**, p95 33 ms y 35 cuadros largos. **57 fps con los videos detenidos** (8 cuadros largos) | ⚠ |
| Baraja a 390 con CPU ×1 | 36,8 fps con videos frente a 59,6 fps detenidos | — |

**Diagnóstico:** el límite de la baraja en este entorno es la **decodificación de video**. La baraja comparte pantalla con quien-multitud 1, 2 y 3 en VP9 por software, sobre 2 CPU y con SwiftShader. Al detener los videos se recuperan casi 60 fps, y con CPU ×1 el resultado es peor que con ×4 porque coincidieron más videos decodificando. En un teléfono con decodificación por hardware el resultado debería ser mejor, pero habría que confirmarlo en uno real.

## 7 · Enlaces

| Enlace | Destino | Estado |
|---|---|---|
| «Ver la carta» (portada) | `/nueva/carta/` | 200 ✔ |
| CARTA (nav) | `/nueva/carta/` | 200 ✔ |
| «Ver la carta completa» (Tragos) | `/nueva/carta/#casa` | 200, el ancla existe y queda visible tras el clic (top 180 px) ✔ |
| «Ver la carta completa» (Comida) | `/nueva/carta/#comilona` | 200, el ancla existe y queda visible ✔ |
| Tarjetas de tragos y platos | `#casa`, `#mocktails-sin-alcohol-mocktails-de-la-casa`, `#comilona-pizzas-artesanales`, `#comilona-picoteos`, `#comilona-sanguches`, `#comilona-greditas` | 200 y las 6 anclas existen ✔ |
| DM | `https://ig.me/m/almud_bar` (`target=_blank rel=noopener`) | Externo, sin red para verificarlo |
| «Abrir en Google Maps» | `google.com/maps/search/?api=1&query=Almud+Bar+Serrano+325+Castro` | Externo, sin red |
| Créditos | @catarsis.fotografia, @estudiouno.prod, @isosur.prod, @rober.patagonico (pie); @cepaz y @rusio_mezclao (dueños); 5 @ del equipo | Externos, todos `noopener` |
| Carta → home | `/nueva/` ×2 («Almud Bar · Inicio») | 200, pero apunta a la versión vieja `/nueva/` y no a `/nueva_v9/` ⚠ |
| Carta: 37 anclas internas y «Carta oficial (PDF)» `uqr.to/ppvi` | — | Anclas ✔; el PDF es externo |

No hay enlaces internos rotos ✔.

**Al publicar como principal**, hay que reescribir:
- en `/nueva_v9/index.html`, las **19** `href="/nueva/carta/…"` por `/carta/…`;
- el canonical y `og:url` (`https://almudbar.pages.dev/nueva_v9/`) por `/`;
- quitar `<meta name="robots" content="noindex">`;
- en la carta, los 2 `href="/nueva/"` por `/`, el canonical y `og:url` (`/nueva/carta/`) por `/carta/`, y su `noindex`.

`_redirects` no tiene reglas para `/nueva_v9/` ni para `/nueva/`, y `_headers` no tiene regla de caché para `/assets/v4/*`, donde están los videos de esta versión.

## 8 · Archivos y peso

- **Referencias faltantes:** ninguna. Revisé 553 rutas de v9 (src, srcset, data-src, data-poster, data-webm/mp4, fuentes CSS) y 74 de la carta ✔.
- **Peso total con recorrido completo** (gzip; los 3 slides del slider abiertos):
  - v9 a 390 (DPR 3): **18,0 MiB** en 87 peticiones (video 15,1 MiB, imágenes 3,1 MiB, fuentes 78 KiB, JS 63 KiB, HTML 37 KiB, CSS 16 KiB).
  - v9 a 1440: **17,7 MiB** en 89 peticiones (video 15,9 MiB, imágenes 1,6 MiB).
  - Carta: **721 KiB** (551 KiB son el video del humo).
  - No incluye el embed de Google Maps, que no cargó sin red y en la práctica suma su propio peso al llegar al cierre.

---

## Fallos encontrados (sección, elemento, cómo reproducir)

1. **Eventos · `.eventos .ttl` (site.js, línea 527):** un comentario `// desde el borde superior… (overflow: clip)` quedó en medio del objeto de `G.from` y anula `rotation`, `opacity: 0`, `duration: 1.25` y `ease: 'bounce.out'`. Las palabras de «tirar la casa por la ventana!» caen en 0,5 s con `power1.out`, sin giro ni rebote.
   *Reproducir:* abrir /nueva_v9/ a cualquier ancho, bajar hasta Eventos y ver que el título entra sin rebote. En la fuente, todo lo que sigue a `//` en esa línea es comentario.
2. **Nav · `a.nav__logo`:** es la 2ª parada del Tab con `opacity:0` en la portada. El contorno se pinta sobre un elemento invisible (WCAG 2.4.7).
   *Reproducir:* cargar la página arriba, pulsar Tab dos veces; el foco queda en un logo que no se ve.
3. **Cierre · `.mapa iframe`:** al enfocarlo con Tab no tiene contorno (`outline: none`).
   *Reproducir:* tabular hasta después de «Escríbenos por DM».
4. **Cierre · `.mapa iframe` en EN:** el `title` sigue en español («Mapa: Almud Bar…») porque `setLang` solo traduce `data-alt-en` y `data-aria-en`, y no `data-title-en`.
   *Reproducir:* cambiar a EN y leer `document.querySelector('.mapa iframe').title`.
5. **Comida y Equipo · orden de tabulación:** el foco sigue el DOM y no la lectura visual; en Comida a 1440 salta abajo y vuelve arriba.
   *Reproducir:* a 1440, tabular desde «Ver la carta completa» de Tragos y mirar cómo saltan las coordenadas.
6. **Carta · `.nav__dm`, botón EN/ES y `h2.panel__t`:** 15 px, bajo los 16 px, en los 8 anchos.
7. **Portada · video:** a 768×1024 y 1024×768 se recorta el 25 % del encuadre (el móvil 9:16 en una caja 3:4, el 16:9 en una caja 4:3).
8. **Primer pantallazo a 390:** 1 483 KiB = 1,52 MB decimales. La meta de 1,5 MB se cumple solo si se lee en MiB. Casi todo es `portada-celular-720.webm` (1 248 KiB).
9. **Baraja con CPU ×4:** 48 fps con los videos vecinos corriendo (57 sin ellos). El límite es la decodificación de video; falta medirlo en un teléfono real.
10. **site.js · mapa:** el bloque `[data-mapa]`/`.mapa__ph` (insertar el iframe al tocar) es código muerto. El HTML ya trae el iframe y `<div class="mapa">` no tiene `data-mapa`.
11. **Carta → home:** apunta a `/nueva/` (versión anterior) y no a la candidata.

## Correcciones priorizadas

**Bloqueante (al publicar como principal)**
- B1 · Reescribir las 19 rutas `/nueva/carta/…` → `/carta/…` en la home. En la carta, `/nueva/` → `/`. Actualizar canonical y `og:url` de ambas páginas y quitar los `noindex`. Si no se hace, la home publicada lleva a la carta de prueba y no se indexa (§7).

**Importante**
- I1 · Fallo 1: sacar el comentario de la línea 527 de `js/nv9/site.js` para que el título de Eventos recupere el giro y el rebote.
- I2 · Fallo 2: el logo del nav no debe recibir foco mientras está invisible (`visibility:hidden` o `tabindex=-1` hasta `.is-past`), o debe mostrarse al enfocarlo.
- I3 · Fallo 8: bajar el video de portada del celular unos 60–100 KiB (bitrate o duración) para cumplir 1,5 MB también en decimales, con margen.
- I4 · Fallo 9: confirmar en un teléfono real los fps de la baraja con quien-multitud corriendo. Si baja de unos 50 fps, considerar pausar los videos de «Con quién» que estén fuera de pantalla mientras se usa la baraja, sin atarlos al scroll.

**Menor**
- M1 · Fallo 3: darle foco visible al iframe (`.mapa iframe:focus-visible{outline:2px solid var(--focus)}`).
- M2 · Fallo 4: traducir `data-title-en` en `setLang`.
- M3 · Fallo 6: subir a 16 px `.nav__dm`, el botón de idioma y `.panel__t` en la carta.
- M4 · Fallo 5: alinear el orden del DOM de Comida y Equipo con la lectura visual, o aceptarlo como está.
- M5 · Fallo 7: revisar el encuadre de la portada a 768–1024 (`object-position` o un video 3:4).
- M6 · Fallo 10: borrar el código muerto del mapa en site.js.
- M7 · A 1440, lugar-noche (1,18 MB) entra en el primer pantallazo por el margen del 15 %. Evaluar si conviene.
- M8 · Agregar `/assets/v4/*` a `_headers` con caché larga, como `/assets/v3/*`.
