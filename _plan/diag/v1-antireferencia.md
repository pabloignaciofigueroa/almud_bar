# Almud v1 · Diagnóstico como anti-referencia

⚠️ DEGRADED: single-context (no se ejecutó el detector de Impeccable, que es un binario sin autorizar; la evidencia determinista sale de Taste `lint`/`inspect` y de las capturas propias).

**Encuadre del cliente.** La v2 es un sitio **nuevo**, construido desde los activos de Almud. **No es la v1 mejorada.**
Este documento no es una lista de arreglos. Tiene tres partes:
- lo que la v2 **nunca** debe repetir;
- las pocas **verdades de marca** que la v1 desenterró, que pasan como contenido y no como diseño;
- las **lecciones de proceso** que conviene conservar.

Nada de la v1 se "pule" (Impeccable: *never split the difference into polish on the discarded look*).

**Evidencia**
- Taste: `.taste-skill/before/`
  - `lint.txt`: 40 FAIL y 7 WARN.
  - `inspect.txt`: 13 FAIL y 12 WARN.
  - Capturas `desktop-*`, `tablet-*`, `mobile-*`.
- Capturas propias por sección a 390, 768 y 1440 px en `_plan/diag/v1/`, con prefijos `m-`, `t-` y `d-`.
- Auditoría de movimiento de Emil (33 animaciones, veredicto **Block**) en `_plan/skills/emil.md` §5.
- Fuente: `index.html`, `css/main.css`, `js/main.js`.

---

## 1. Crítica Impeccable (modo Persuade)

### 1.1 Veredicto de especificidad
La v1 tiene **material** propio y **forma** genérica. Los textos, las fotos, la carta y las reseñas son de Almud, pero el esqueleto es la plantilla de "bar con onda" que sirve para cualquier bar de cualquier ciudad:

hero → historia → manifiesto → galería → carta → comida → eventos → equipo → reseñas → mapa

A cada sección se le aplicó un efecto distinto, sacado del repertorio de los sitios premiados:
- pin con scrub;
- palabra a palabra;
- carrusel horizontal;
- masas en parallax;
- tablero de afiches;
- tendedero;
- contador;
- magnéticos.

Ningún dispositivo nace de lo que es Almud. "Colorido y fiestero" se tradujo como *cada cosa de un color distinto* (`d-10-manifesto.jpg`) y *material de cotillón falso*: flecos, pinzas, polaroids.

### 1.2 Puntaje de salud (Nielsen, 0–4; la 7 y la 10 quedan n/a)

| # | Heurística | Puntaje | Problema clave (evidencia) |
|---|---|---|---|
| 1 | Visibilidad del estado | 2 | El cargador "Almudcito ito ito" tapa el hero ~1,8 s (`inspect`: *covered-text*, screen 1, 100 % oculto). En el pin no hay señal de cuánto falta (`desktop-page-01..03.jpg`). Lo bueno: la promo de hoy se marca sola. |
| 2 | Coincidencia con el mundo real | 3 | La voz literal, los precios reales y "Serrano 325, al frente del Centro Cultural" hablan como el bar. Pero en modo EN siguen en español 118 bloques `lang="es"`, entre ellos las descripciones de los 54 platos y tragos. |
| 3 | Control y libertad | 1 | La historia está fijada durante 3.545 px en móvil y 4.301 px en tablet, y no se puede saltar. Lenis suaviza el input. El cierre del menú con Escape también se anima. En 11 de 12 pantallas de escritorio solo se ve el isotipo (`desktop-page-02.jpg`, `mobile-page-01.jpg`). |
| 4 | Consistencia y estándares | 1 | 3 familias tipográficas y 32 tamaños (`inspect`). El color de cada titular cambia por sección: azul, amarillo, verde, rosado (`d-03`, `d-05`, `d-06`, `d-08`). Hay cinco idiomas de tarjeta: píldora, polaroid, afiche con alfiler, tarjeta redondeada y plato de color. |
| 5 | Prevención de errores | 2 | Las filas laterales parecen cortadas (`inspect`: *side-scroll*). El tendedero solo se arrastra con mouse. El *peek* de foto existe solo en hover, así que en touch no llega. |
| 6 | Reconocer antes que recordar | 2 | Horario, dirección y DM aparecen en el hero y vuelven a aparecer recién ~18 pantallas más abajo (`d-08-llegar.jpg`). La cabecera se esconde al bajar. La promo del día queda en la 4.ª pestaña de la carta. |
| 7 | Flexibilidad y eficiencia | n/a | Superficie Persuade, sin tareas repetidas. |
| 8 | Estética y minimalismo | 1 | Pasan a la vez: marquesina de 12 píldoras de colores, grano animado, flecos arcoíris, emoji gigantes (`d-09-foot.jpg`), sombras, vidrio y la nota en Caveat. Medido: 22 box-shadow, 10 text-shadow y 20 hairlines. |
| 9 | Recuperación de errores | 2 | Hay respaldo sin GSAP y el mapa usa una imagen hasta el clic. Pero un video no tiene poster (`inspect`: *no-poster*) y el texto tapado no tiene salida. |
| 10 | Ayuda y documentación | n/a | Landing de un bar. |
| **Total** | | **14/32 (44 %)** | **Pobre.** La meta v2 es ≥26/32. |

### 1.3 Carga cognitiva: 4 de 8 ítems fallan, carga **alta**
- ✗ **Foco único.** Marquesina, grano y cursor "Arrastrar" compiten con el titular desde la primera pantalla.
- ✗ **Agrupación en bloques de ≤4.** Hay 9 rincones en una fila horizontal, 18 reseñas en carrusel, 54 ítems de carta y 12 palabras de léxico en fila.
- ✓ **Agrupación por proximidad.**
- ✗ **Jerarquía visual.** Cada sección grita en display y en un color propio, así que nada es lo más importante.
- ✓ **Una cosa a la vez.**
- ✓ **Pocas opciones.** El hero tiene 2 CTAs, idioma y menú.
- ✗ **Memoria de trabajo.** Lo que se ve arriba (abre a las 18:00, Serrano 325) hay que recordarlo durante ~20 pantallas.
- ✓ **Revelado progresivo.** Acordeones de la carta y mapa al clic.

### 1.4 Lo que funcionaba (como contenido, no como forma)
1. **La voz literal con su fuente.** Cada texto lleva su clave `[IG-NNN]`, `[VID-061]` o `[CARTA-n]` en `content/copy.md`. No hay adjetivos inventados.
2. **La carta real.** 54 ítems, sus precios de octubre 2026 y la promo semanal con el día de hoy destacado (`js/main.js:127-129`).
3. **La prueba social con nombre, fuente, año e idioma.** 18 reseñas ES/EN/FR, más 848 en Google y 209 en Tripadvisor (`d-07-reviews.jpg`).

### 1.5 Problemas prioritarios
- **[P0] El isotipo fijado durante ~10 pantallas vacías.**
  - *Por qué:* la historia (VID-061) es lo más valioso que hay, y en `inspect` se ve como 11 de 12 pantallas vacías (`desktop-page-01..03.jpg`, `mobile-page-01/02.jpg`, `tablet-page-02.jpg`). Quien no tiene GSAP en buen estado o baja rápido ve un logo rosado repetido. Además, el texto se monta sobre el isotipo y el letrero (`d-01-historia-0.jpg`).
  - *Para la v2:* si hay un momento con scroll, dura ≤300 vh y cada pantalla tiene texto y algo que mirar.
- **[P1] Párrafos puestos como titulares.**
  - Las líneas 2, 5 y 6 de VID-061 llegan a 6–7 líneas a 92 px. "Tantos coctelcitos…" y "Ya saben que no somos ná…" ocupan 4 líneas y dejan vacío el 67 % del ancho (`d-03-carta.jpg`, `d-05-jornadas.jpg`; `inspect`: *headline-lines*, *lopsided*).
- **[P1] Color sin rol.**
  - `--rib`, el arcoíris, aparece en flecos, barras de progreso, platos y pestañas. Las clases `c-*` rotan seis colores por ítem (`css/main.css:20,40,165,169,235,245`). El violeta `#9b5cff` viene de las luces del bar, no de la marca.
  - Resultado: el rosa de la barra, el único color propio, se diluye.
- **[P1] Lo útil queda lejos.**
  - El horario no dice a qué hora cierra. La promo de hoy está a ~10 pantallas y una pestaña de distancia. El DM aparece recién en "Cómo llegar".
  - El local de Castro que pregunta "¿qué hay hoy?" no tiene respuesta en la primera pantalla.
- **[P2] Pocas fotos que trabajan.**
  - `inspect` cuenta 3 fotos visibles por pantalla. 44 de los 54 platos muestran un "plato" de color con el nombre repetido en vez de una foto (`m-03-carta.jpg`).
  - La comida está en recortes chicos con sombra flotando (`d-04-food.jpg`).

### 1.6 Personas: qué se les rompe

**Turista extranjero en Castro** (EN, teléfono, decide esta noche):
- Toca EN y cambian 55 rótulos, pero titulares, descripciones de tragos y citas siguen en chileno coloquial ("complikeichon", "pa ajuera") sin glosa.
- "Abrimos de Mar a Sáb a las 18:00hrs" no dice hasta qué hora.
- El cargador y el pin le cuestan ~4 pantallas antes de saber qué se toma.
- No hay precio de referencia en la primera pantalla.

**Local de Castro** (ya conoce el bar; quiere saber la promo, si hay evento y si hay mesa):
- La promo del día está en la 4.ª pestaña.
- Los eventos son todos pasados (tablero 2024–2026) y no hay "próximo".
- Para reservar hay que ir al DM, que está al final.
- El léxico en píldoras le resulta autoparódico: es su forma de hablar convertida en adorno.

**Casey** (móvil, distraída):
- 21 pantallas de página (18.070 px a 390).
- Botones "Cómo llegar" a medio cargar sobre el video (`m-00-fold.jpg`).
- Si sale y vuelve, otra vez el cargador (solo lo salta dentro de la misma sesión).

**Jordan** (primera vez):
- "Jornadas recreativas" y "Comilona" son etiquetas de menú que no anticipan su contenido.
- La nota manuscrita "un almud: la unidad de medida chilota" aparece rotada y en Caveat, con 10 pantallas de por medio.

**Riley** (prueba de estrés):
- Nombres largos en Six Caps en `.dish__n`.
- Captions con emoji ZWJ (`🫶🏼`).
- Con 320 px y EN, "Open in Google Maps" desborda la píldora.
- Sin GSAP la página funciona, pero el tablero y el tendedero pierden su orden.

### 1.7 Preguntas
- ¿Qué pasa si la primera pantalla responde *"¿abren hoy, qué hay hoy y dónde queda?"* antes que *"quiénes somos"*?
- ¿Qué pasa si la historia de VID-061 se *lee* como texto junto a su video, en vez de *pasar* sobre el video?
- ¿Cuál es el único dispositivo que solo Almud puede tener? ¿La medida, la barra larga, el letrero?

---

## 2. Prohibido en la v2

Fuente de cada regla: **I** = Impeccable · **T** = Taste · **E** = Emil · **C** = cliente.

### Estructura
1. **El orden de plantilla de bar**: hero → historia → manifiesto → galería → carta → equipo → reseñas → mapa. La v2 ordena según lo que el visitante necesita (modo Persuade) y según su propio relato. *(I: category-reflex; C)*
2. **Un pin de más de 300 vh, o cualquier pantalla de solo isotipo o solo fondo.** Una pantalla vacía sirve de pausa una sola vez por página. *(T: empty-screens, blank-gap; E §6.11; I)*
3. **Una sección por efecto.** No se elige un truco distinto para cada bloque (pin, palabra a palabra, carrusel, masas, tendedero, contador). Hay un solo momento autoral. *(I; E: cohesión)*
4. **Horario, dirección, carta y DM lejos de la primera pantalla**, o escondidos tras pestañas o tras una cabecera que se oculta. *(I: Persuade; C)*
5. **Cargador o pantalla de entrada.** El hero queda legible y clicable en ≤1,2 s. *(E #1; T: covered-text)*
6. **Secciones cargadas a un lado con el 67 % del ancho vacío**, y textos que arrancan en 12 líneas de margen distintas. *(T: lopsided, ragged-edges)*
7. **Filas cortadas en el borde** como única pista de que se puede deslizar. *(T: side-scroll)*

### Tipografía y texto
8. **Párrafos como titulares.** Un h1 o h2 ocupa ≤2 líneas. Una cita literal larga va en `<p>`/`<blockquote>` de ≤36 px (≤24 px en móvil). *(T: headline-lines)*
9. **Más de dos familias** (Caveat sale; Big Shoulders vive solo dentro del logo) y **más de ~5 tamaños**. La v1 tenía 32. *(T: font-count, size-count)*
10. **Titulares con cambio de familia o de color a mitad de línea** (el manifiesto palabra por color). *(T: mixed-font-headline)*
11. **Nota manuscrita rotada** como "cercanía" fingida. *(T; I)*
12. **Emoji como UI, ornamento o icono** (😘 gigante, ★, ←, →). La palabra literal se conserva; el glifo sale. *(T: emoji; skills-notes §3)*
13. **Eyebrows, rótulos chicos sobre los títulos y numeración de secciones.** *(skills-notes §3; I)*
14. **El léxico de la casa en píldoras de colores.** *(C; T)*
15. **Adjetivos nuestros.** Habla la prueba: nombres de tragos, @ del equipo, fotos de sus fiestas. *(I; skills-notes §3)*

### Color y superficie
16. **Colores rotando por ítem, pestaña o sección** (`c-*`, `plate--0..5`, titulares de un color cada uno). El color tiene roles. Hay un solo acento, el rosa de la barra. Los demás van como campos planos por capítulo, con cortes duros. *(T; I)*
17. **El arcoíris `--rib`** en barras, progresos o flecos. Tampoco el violeta `#9b5cff`. *(T: palette-purple; C)*
18. **Degradados decorativos.** Solo se admite un scrim neutro sobre una foto. *(T: gradient)*
19. **Sombras en reposo, text-shadow, vidrio/blur y hairlines.** La carta se separa con espacio y tono, no con líneas. *(T: shadow, text-shadow, glass, hairline)*
20. **Materiales falsos**: flecos CSS, polaroids, pinzas, tendedero, alfileres, afiches torcidos, grano animado. *(C; T; I)*
21. **"Platos" de color con el nombre repetido** como sustituto de foto. Si un ítem no tiene foto, se queda sin foto. *(T: few-pictures; I)*
22. **Esquinas redondeadas, marcos, rotaciones o sombra en las fotos.** *(skills-notes §2)*

### Imagen
23. **Menos de 6 fotos que trabajen**, o fotos en recortes chicos flotando. Se pide una foto decisiva por cuento y 3–5 tratamientos. *(T: few-pictures; I)*
24. **Repetir el mismo plano** (el letrero en el hero y otra vez en la historia, `d-00` / `d-01-historia-0`) y **video sin poster**. *(T: no-poster)*
25. **Texto grande montado sobre una foto o un isotipo mientras se hace scroll.** *(T: pinned-over-picture, covered-text)*
26. **Imágenes generadas o de stock.** Solo material de Almud. *(C; skills-notes §0)*

### Movimiento (Emil, review-animations: Block)
27. **Nada acoplado a la velocidad del scroll**: flecos con skew, balanceo del tendedero, marquesina acelerada. *(C; E #7, #8, #15)*
28. **`ease-in`, `elastic`, `back` o `bounce`**, y **`scale(0)`** o escalas menores a .92 (isotipo .4, cursor, sello "hoy"). *(E #3, #20, #27)*
29. **Duraciones de UI sobre 300 ms.** No vuelve el default `expo.out` de 1 s: el menú tardaba ~1,5 s, las pestañas 700 ms, la vitrina 900 ms. Se usan solo los tokens de `skills-notes` §5. *(E #22–#24)*
30. **Botones magnéticos, cursor propio, foto que sigue al puntero, contador 0→4,6.** *(E #17, #19–#21)*
31. **Bucles ociosos**: grano en movimiento, indicador de scroll infinito, ecualizador que anima `height`. *(E #6, #29, #30)*
32. **Texto que se lee mientras se mueve**: manifiesto en opacidad .2, afiches con `data-speed`, parallax sobre tarjetas. *(E #10, #13)*
33. **Hover sin `(hover:hover) and (pointer:fine)`, teclado que anima, falta de `:active`.** *(E #25, #26; reglas 7, 8, 17)*
34. **Reduced-motion que lo apaga todo** con `*{animation:none!important}`. Debe ser menos y más suave, no cero. *(E #32)*
35. **Doble suavizado (Lenis + `scrub: .6`)** y tickers por frame que leen layout. *(E #7, #9, #31)*

---

## 3. Verdades de marca que encontró la v1 (pasan como **contenido**)
Todo esto está en `content/` con su fuente. La v2 lo usa como material, sin heredar su puesta en página.

1. **La historia de VID-061.** Son los 9 subtítulos literales del video de @estudiouno.prod: *"Almud nace en el invierno de 2014… una gran barra, larga, de esas para sentarse y quedarse ahí… hemos aprendido y construido a pausa"*. Es el relato fundacional y está en sus propias palabras.
2. **"Un almud: la unidad de medida chilota"** (reseña Seo2, Tripadvisor 2015). El nombre tiene un significado concreto y local, y puede sostener un concepto.
3. **"Almudcito ito ito"** y el sufijo que se repite ("terracita ita ita", "comilona ona ona", "barsucho ucho ucho", "Crumblecito ito ito"). Es un gesto verbal propio. Vuelve como texto dentro de un cuento; no como cargador.
4. **El léxico de la casa**: guarisnaque, güergüero, comilona, empinar el codo, celebreichon, refreskeichon, ñam ñam, glup glup, picho caluga, macanúo, choriflai, "Besi". Todas las palabras salen de sus captions (`copy.md` §1).
5. **La carta como obra de autor.** Los nombres de los tragos ya son el copy: *Pinche Güey, Aquí te las traigo Peter, Te espero en la cuneta, Tranquilein John Wayne, Sagüer on Faia, Otra cosa mariposa, La moto chantá, Camarón que se duerme, Muéveme el pollo, Pa los chichichos, Somos dulzones*. Son 54 ítems con precio (`content/carta.json`).
6. **La promo del día.** Martes Negroni y Fernet, miércoles Piscolein y Gin Tonic, jueves sangría, sábado Ramón, a $4.500 de 18:00 a 22:00, *"siempre sujeto a stock"*. Es la única "cosa viva" con contenido real y responde "¿qué hay hoy?".
7. **Reseñas reales** con nombre, origen, fuente, año e idioma (18 en `content/reviews.json`), más 4,6 sobre 848 en Google y el #1 de 6 bares en Tripadvisor. Frases que ya hacen trabajo: *"Chiloé: palafitos, curanto y Almud"*, *"The bar tenders are artists, sit on the bar and watch"*, *"Estuve ahí cada día de mi estancia"*.
8. **Lugar y gente.** Serrano 325, *al frente del Centro Cultural de Castro*. El equipo con sus @ y los dueños, *"el franchuto @rusio_mezclao y la disharashera @cepaz"*. Los rincones con su caption: barra rosada, lámparas de varillas, fogón, terraza con vista a los techos y el mar, techo de cintas, mural Ojo Piojo.
9. **El calendario propio**: 12 años, Negroni Week, Jalogüín, Mambo Tiki, Fondita, 14F, Tardes en el Almud, Almud & Rucalaf. Prueba de que es un bar que celebra, no un adjetivo.
10. **Identidad heredada**:
    - Six Caps, que viene del letrero;
    - Oswald, que es la letra de la carta;
    - el rosa del muro de botellas como único acento;
    - el crema de los posavasos;
    - el logotipo vectorizado desde la carta oficial;
    - los créditos de fotos (@estudiouno.prod, @catarsis.fotografia, @tamillanquileo, @isosur.prod, @dosistudio).

---

## 4. Lecciones técnicas que se conservan (son **proceso**, no diseño)
1. **Medir el CLS en cada cierre.** La v1 cerró con 0,0008 en escritorio y 0,0007 en móvil gracias a `width`/`height` en cada `<img>` y a un LQIP en base64. Se mantiene la vara (<0,01) y el método.
2. **Bilingüe por atributos.** `data-en`, `data-alt-en`, `data-aria-en` y `data-meta-en` con `localStorage` (`js/main.js:15-37`) funcionan sin framework. Lección: el EN tiene que cubrir también la carta y los titulares, con glosa del habla local y no traducción plana. Además hay que probar el peor caso (EN, 320 px, nombres largos).
3. **Reduced motion como variante diseñada.** Ya existía la versión estática de la historia y había respaldo sin GSAP (`html.has-gsap`). Se conserva como requisito de QA, con la regla de Emil: menos, no cero.
4. **Contenido trazable.** `content/copy.md` con claves de fuente, `carta.json` y `reviews.json` separados de la maqueta, y correcciones mínimas documentadas. Se repite el método.
5. **Canal de publicación.** `tools/build.py`, `tools/media.py` (WebP 800/1800 y videos con poster) y `tools/publish.py` dejan `public/` en Cloudflare Pages "almudbar". `publish.py` ya prueba los fallos (.md, archivo faltante, >25 MB) y `public/_headers` define la caché. Se reutiliza tal cual.
6. **Compuerta medible antes de publicar.**
   - Taste `lint` e `inspect` con 0 FAIL a 390, 768 y 1440.
   - review-animations en Approve.
   - Crítica Impeccable ≥26/32.
   - Capturas por sección: las de `inspect` no pasan del pin, así que hay que tomar capturas propias como `_plan/diag/v1/*`.
