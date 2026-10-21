# Fase 15 · Crítica, ronda 1: landing (`index.html`) y carta (`carta/index.html`)

⚠️ DEGRADED: single-context (crítico independiente en un solo contexto; el detector de Impeccable es un binario sin autorizar). La evidencia determinista sale de Taste `lint`/`inspect`, de Playwright (CLS, consola, red, anclas, objetivos táctiles, líneas de titular) y de capturas propias viewport por viewport.

**Evidencia**
- Capturas en `_plan/critica-1/shots/`:
  - Pasadas por viewport: `{landing|carta}-{390|768|1280|1440|1920}-sNN.jpg`.
  - Variantes EN y reduced motion: `*-en-*` y `*-rm-*` a 390 y 1440.
  - Estados: `i-menu-390.jpg`, `i-menu-race-390.jpg`, `i-carta-tab-comilona-*.jpg`, `i-carta-chip-*.jpg`, `i-carta-promos-*.jpg`, `i-hover-cover-1440.jpg`, `i-focus-*-1440.jpg`, `i-cover-dpr2-crop.png`, `i-320-en-cover.jpg`, `i-375x667-{es,en}-cover.jpg`.
  - Recortes: `z-*.jpg`. Hojas de contacto: `sheet-*.jpg`.
  - Métricas por captura: `*-metrics.json`.
- Taste:
  - `lint` landing: 0 FAIL, 1 WARN (copy: "more than a", que es la glosa EN `index.html:171`, un falso positivo).
  - `lint` carta: 0 / 0.
  - `inspect` landing (`_plan/critica-1/inspect-landing/`): 0 FAIL, 1 WARN (palette-cream, defendido en `sistema.md`).
  - `inspect` carta (`_plan/critica-1/inspect-carta/`): 0 FAIL, 3 WARN (palette-cream, **still-page** y **side-scroll a 768 y 390**).
- Técnica:
  - CLS 0 en los 5 anchos y en las dos páginas.
  - 0 errores de consola y 0 anclas rotas. No hay desborde horizontal, ni siquiera a 320 en EN.
  - Las imágenes "incompletas" son todas de días o pestañas ocultas (lazy, correcto). Ninguna se queda en LQIP después de revelarse.
  - Un fallo de red: `lugar-techo-flecos.mp4`, el único video **sin fuente WebM**. En este Chromium sin H.264 no corre; queda en su póster con el botón "Pausar video" mintiendo.
- Copy: revisé **las 121** líneas con `data-src` de las dos páginas contra `ig_captions.md` y `bio.txt` (no solo 15), todas literales. No aparecen "fila", "esperar mesa" ni "desocupe".

---

## 1. Puntajes

### Impeccable (Nielsen, 0–4; la 7 y la 10 n/a) → **22/32 (69 %) · Aceptable**, en el borde de Bueno. La meta era ≥ 26.

| # | Heurística | Puntaje | Problema clave |
|---|---|---|---|
| 1 | Visibilidad del estado | 3 | "Hoy" se marca solo y las pestañas tienen estado claro. Pero el menú del teléfono puede quedar **invisible con el scroll bloqueado** (`i-menu-race-390.jpg`), y el calendario no dice cuál es el próximo evento. |
| 2 | Coincidencia con el mundo real | 3 | La voz literal es impecable. Pero la semana de "Hoy en Almud" **no tiene viernes** (Mar, Mié, Jue, Sáb), justo en la página cuyo lema es "todos los días son una fiesta". Y "Los sillones" se ilustra con un primer plano donde no hay sillones. |
| 3 | Control y libertad | 3 | La carta no tiene vuelta al inicio salvo el logo, ni enlaces a Cómo llegar o DM arriba. El botón atrás funciona con las pestañas. |
| 4 | Consistencia | 2 | Hay titulares en caja literal: unos en caja alta pareja y otros "Mayúscula + versalitas" ("La carta", "Peazo de equipo", "Que no se lo cuenten!"). "Ver la carta" aparece en 3 estilos. Hay dos botones barra por pantalla. Las filas de la carta saltan de margen según tengan foto o no. El sábado de promos no tiene foto. "Hoy" va subrayado como si fuera enlace. |
| 5 | Prevención de errores | 3 | En el teléfono, 5 de las 7 pestañas de la carta, Comilona entre ellas, quedan fuera de pantalla sin ninguna pista (`carta-390-s00.jpg`; inspect *side-scroll*). |
| 6 | Reconocer antes que recordar | 3 | Horario y dirección están en la portada y en "Cuándo y dónde", y la nav es fija. Falta el mapa que pide el brief. |
| 7 | Flexibilidad | n/a | Superficie Persuade. |
| 8 | Estética y minimalismo | 2 | Hay cuatro pantallas de escritorio con media pantalla vacía por accidente: La barra (`landing-1440-s03`), Comida (`s10`/`s11`), Eventos (`s21`) y el video de Dónde (`s24`). El "4,6 / 4,6" es el bloque de métrica de plantilla. En EN cada dato sale dos veces. |
| 9 | Recuperación de errores | 3 | Sin JS el contenido queda completo y los videos llevan póster. Hay un video solo MP4 y una carrera de estado en el menú. |
| 10 | Ayuda | n/a | Landing de un bar. |
| **Total** | | **22/32** | **Aceptable (69 %)** |

**Carga cognitiva:** 2 de 8 ítems fallan, carga **moderada**.
- ✗ **Memoria de trabajo:** la landing mide 26 pantallas a 1440 y 28 a 390 (31 en EN).
- ✗ **Pocas opciones:** "Ver la carta" aparece 9 veces y "Cómo llegar" 5.
- Lo demás pasa: foco único por pantalla, agrupación, jerarquía y revelado progresivo con chips, pestañas y "Ver más reseñas".

### Taste (formato §4)
```
ROUND 1
Seen in one second: el techo de cintas sobre una mesa llena de caras riendo, con ALMUD BAR encima.
Idea (one sentence): Almud abre bajo su techo lleno y después habla en afiches planos de un color por capítulo, con una franja del día que cambia cada día; la carta es la única hoja de papel.
Live thing: "Hoy en Almud" (la promo literal del día en America/Santiago, con su campo de color). Real, y la primera respuesta a "¿qué hay hoy?".
Layout words by section: hero=foto-a-sangre / hoy=split / lugar=split → mosaico → banda → par / tragos=split → mosaico → banda / sin=statement+lista / comida=split-sticky → mosaico / carta=índice-grilla / equipo=statement → banda / quién=statement → mosaico×2 / reseñas=statement+cifras → grilla / eventos=split-lista / dónde=split-datos → video / pie=firma+logo
Scores: design 6.5 · usability 7 · creativity 7.5 · content 8 → overall 7.0
Caps applied: design ≤ 6.5 (secciones con la mitad del ancho vacía y tramos vacíos de más de media pantalla en La barra, Comida, Eventos y Dónde-video). Usability 7 por la carta con pestañas cortadas en el teléfono, el bug del menú y la portada a 375×667, que monta el logo sobre las caras.
Top three problems (most visible first):
1. El mismo split "titular display a la izquierda + 4:5 a la derecha" abre Hoy, El lugar, Tragos, Comida, Con quién, Eventos y Dónde: 7 veces "split". El afiche se vuelve plantilla, y cada split deja media pantalla de campo vacío bajo el titular (landing-1440-s02, s07, s10, s16, s20, s23).
2. Huecos de media pantalla: La barra (s03), Comida (s10/s11), Eventos (s21, la columna derecha vacía ~700 px bajo la foto) y el video de Dónde (s24).
3. Teléfono: en la carta solo se ven 2 de 7 pestañas, y la portada a 375×667 / 320 EN pone el logo y la bio sobre las caras y las cintas sin scrim.
```

### Emil (review-animations) → **Block** (un solo bloqueo funcional; el resto está a un paso de Approve)

| Before | After | Why |
|---|---|---|
| `site.js:85-87` el cierre agrega `animationend {once}` y no lo retira; si se reabre antes de 250 ms, el `animationend` de `hoja-in` ejecuta el handler viejo → `hoja.hidden = true` con `aria-expanded="true"` y `html.hoja-on` (scroll bloqueado) | Guardar el handler (`let onEnd`) y en `openMenu()` hacer `hoja.removeEventListener('animationend', onEnd)`; dentro del handler, `if (!hoja.classList.contains('cierra')) return;` | Rompe la interacción: queda una página congelada sin menú visible (`i-menu-race-390.jpg`). Bloqueante |
| `site.css:553-556` `.hoja.abre/.cierra` con `@keyframes` sobre clip-path | `.hoja { clip-path: inset(0 0 100% 0); transition: clip-path var(--d-panel-out) var(--ease-out); } .hoja.abierta { clip-path: inset(0); transition-duration: var(--d-panel); transition-timing-function: var(--ease-drawer); }` | Interrumpible: un toggle rápido retoma desde el estado actual en vez de reiniciar desde cero (Emil std. 6) |
| `site.css:539` y `:552` `600ms` escrito a mano | `--d-photo: 600ms` en `tokens.css` y `var(--d-photo)` | El sistema prohíbe duraciones sueltas (`sistema.md` §6) |
| `site.css:544-545` `.fade-arm` (opacity + 12 px, 700 ms) en las 6 reseñas | Quitar `data-rv="fade"` de `.res`, o reducirlo a opacidad 240 ms sin desplazamiento | "El cuerpo aparece sin animación" (`sistema.md` §6). Son citas de lectura, y 700 ms es un reveal de foto puesto sobre texto |
| `carta.js:291-297`: "La carta" y el título de la pestaña suben con máscara de 700 ms **al cargar**, en la primera pantalla | Borrar la entrada al cargar (dejar el h1 quieto) | Frecuencia: es la página que el local abre cada vez. Es animación de primera pantalla que retrasa el título (Emil std. 2; el contrato dice "la portada queda quieta a propósito") |
| `carta.css:37` `.tab` hace transición de `background-color` y `color` también al cambiar con flechas | `.tab:focus-visible, .chip:focus-visible { transition: none; }` o quitar la transición de color de `[aria-selected]` | El teclado nunca anima (Emil std. 2; `sistema.md` §6) |
| `index.html:178` video `lugar-techo-flecos` solo `.mp4` | Agregar `<source src="…lugar-techo-flecos.webm" type="video/webm">` primero, como los otros tres | Sin H.264 el loop no corre y el botón dice "Pausar video" sobre un póster quieto |

**Veredicto por niveles**
1. **Regresiones que se sienten:** la carrera del menú. Nada más: no hay ease-in, ni `scale(0)`, ni `transition: all`; el hover está gateado, la presión es .97 en 140 ms y el keyboard-instant está en menú y pestañas.
2. **Simplificaciones perdidas:** el reveal de las reseñas y la entrada de la carta al cargar.
3. **Rendimiento:** limpio. Solo clip-path, transform y opacity, sin GSAP ni Lenis y con un IO por anfitrión.
4. **Interrumpibilidad:** los keyframes de la hoja.
5. **Cohesión:** "la franja se imprime" es un momento autoral bien atado al contenido vivo. No hay ninguno más compitiendo. Bien.
6. **Accesibilidad:** reduced motion = fades de 180 ms y videos en póster ("Reproducir video"). Verificado en `landing-rm-*` y `carta-rm-*`. Correcto.

**Decisión: Block.** Con la primera fila arreglada pasa a **Approve**; las demás filas son de pulido.

---

## 2. Veredictos pedidos

- **¿Entrega "todos los días son una fiesta"?** A medias.
  - La franja del día lo vuelve mecanismo y está muy bien.
  - Pero **falta el viernes en la semana** (`landing-1440-s02`, `landing-390-s02`), así que la promesa se cae justo en el día más fiestero.
  - Además, después de la franja vienen ~5 pantallas de "El lugar" sobre noche con las fotos de menos energía de la página: una lámpara, espaldas de día en la terraza de grava y un primer plano. La fiesta reaparece recién en Con quién (pantalla 16 de 26).
- **¿Respeta el orden del servicio?** Casi.
  - El brief pide lugar → tragos → comida → con quién → eventos → cuándo/dónde.
  - El build inserta sin alcohol, **carta destacada**, **equipo** y **reseñas** entre comida y con quién: con quién queda 10 pantallas después de comida, y la carta destacada repite los tragos y platos que ya mostraron Tragos y Comida.
- **Asterisco de portada (P189): aceptable con condición.**
  - A DPR 1 y a 1280–1440 funciona: el logo va sobre el zinc, las caras quedan libres y a 1920 hay noche a los lados, como manda el contrato.
  - A DPR 2 (`i-cover-dpr2-crop.png`) la piel se ve cerosa y blanda. Para un cliente que ya notó detalles baratos, el original en alta es **requisito antes de entregar**, no un "después".
  - Tampoco es aceptable en teléfonos bajos: ver P1-3.
- **Repetición de fotos:**
  - El motivo de las cintas aparece 4 veces en las primeras 7 pantallas: portada, terraza techada, el loop "brillitos" y el 10 de flores.
  - Los jueves, la foto de la sangría sale dos veces: en Hoy y en Sangría foreva!.
  - El día sin promo reutiliza `con-quien-solo`, que vuelve en Con quién.
  - La garzona del gorro sale en Hoy y en la banda de Equipo.

---

## 3. Lista de arreglos priorizada

Formato: **[P] página · ancho · captura** → qué está mal → arreglo exacto → regla violada.

### P0
**P0-1 · landing · 390–1023 (menú del teléfono) · `i-menu-race-390.jpg`**
- **Qué está mal:** abrir, cerrar y reabrir rápido el menú deja la hoja oculta con `aria-expanded="true"` y `html.hoja-on { overflow:hidden }`. La página queda congelada sin menú.
- **Arreglo:** en `site.js`, guardar el handler de cierre y quitarlo en `openMenu()`; dentro del handler, `if (!hoja.classList.contains('cierra')) return;`. Mejor aún, pasar la hoja de keyframes a transición de clip-path (tabla de Emil).
- **Regla:** Emil std. 6 (interrumpible); Nielsen 3.

### P1
**P1-1 · carta · 390 y 768 · `carta-390-s00.jpg`, inspect *side-scroll***
- **Qué está mal:** la barra de pestañas muestra "Coctelería de la casa" y "Cócteles del mundo mundial", y la segunda termina justo en el borde. No hay pista de que existen Espirituosos, Vinos, Mocktails, **Comilona** y Promos.
- **Arreglo:** por debajo de 700 px, `.tabs { height:auto } .tabs-l { flex-wrap: wrap; overflow: visible; row-gap: var(--sp-1); padding-block: var(--sp-2) }`. Con 7 pestañas cortas caben en 3 filas de 48 px. Si se quiere mantener el scroll, `--tabs-h` ≥ 96 y dos filas. Lo mismo para `.chips` de Comilona (6 chips; se corta "Somos dulzones").
- **Regla:** Taste side-scroll y pass 13; Nielsen 5 y 6.

**P1-2 · landing · todos · `landing-1440-s02.jpg`, `landing-390-s02.jpg`**
- **Qué está mal:** la semana de Hoy en Almud omite el **viernes**. La lista es Mar, Mié, Jue, Sáb y el viernes solo existe como día oculto.
- **Arreglo:** agregar el `<li>` del viernes entre jueves y sábado con su literal de `contrato.md` ("Viernes ya!" [IG-003]), sin precio, y pasar `.semana-l` a 5 columnas desde 700 px (`grid-template-columns: repeat(5,1fr)`). De paso, "Ramón a $ 4.500!" es el único ítem con precio: dejar el precio en todos (es el mismo $ 4.500) o en ninguno.
- **Regla:** brief ("todos los días son una fiesta"), Nielsen 2 y 4.

**P1-3 · landing · 375×667 y 320 EN · `i-375x667-es-cover.jpg`, `i-320-en-cover.jpg`**
- **Qué está mal:** en teléfonos bajos el bloque de tipo (logo 200 px, bio, datos y CTAs) mide más que el scrim del 44 % inferior. El logo cae sobre la cabeza de la rubia y sobre la mesa. A 320 EN, el logo y la glosa quedan sobre cintas claras sin scrim y casi no se leen.
- **Arreglo:**
  - `@media (max-width:899px) and (max-height:720px) { .cover-logo { width: min(150px, 40cqi) } .cover-bio { font-size: var(--t-body) } }`.
  - El scrim debe crecer con el bloque y no con un % fijo: `.cover-scrim` → `linear-gradient(to top, rgb(var(--scrim)/.86) 0, rgb(var(--scrim)/.7) calc(var(--tipo-h) * .8), rgb(var(--scrim)/0) calc(var(--tipo-h) + 48px))`, con `--tipo-h` medido por JS en `resize`. Alternativa sin JS: en `max-height:720px`, `.cover-stage { justify-content: flex-start }` y el tipo debajo de la foto, sobre noche.
  - En EN ocultar la glosa de la bio en la portada (`html[lang=en] .cover .gl-lead { display:none }`); con "Signature cocktails…" basta y sobra la bio en ES.
- **Regla:** contrato FIRST VIEWPORT ("caras sin nada encima"); Taste pass 13 (collisions).

**P1-4 · landing · 1440 y 1280 · `z-hoy-precio-1440.jpg`, `landing-en-1440-s01.jpg`**
- **Qué está mal:** el "$" de Six Caps baja y toca "de 18:00 a 22:00 hrs". En EN choca con "CLP 4,500", y la glosa "Piscolein [pisco & cola] Wednesday!" queda pegada al "!" del titular.
- **Arreglo:** `.hoy-promo .precio { line-height: 1; padding-bottom: .08em; }` y `.hoy-glh { margin-top: var(--sp-4) }` (hoy hereda `.gl-h { margin-top: 12px }`, que no alcanza contra el interlineado de 0,86).
- **Regla:** Taste pass 13; craft-floor Spacing.

**P1-5 · landing · 1440/1280/1920 · `landing-1440-s03.jpg`**
- **Qué está mal:** "La barra": la foto (una lámpara de perritos, "Video @rober.patagonico", que en realidad es un fotograma quieto) en las columnas 2–4, y el texto "una gran barra, larga…" en las 6–10, abajo. Encima del texto y a la derecha quedan ~700×450 px de noche vacía, y la foto no muestra la barra.
- **Arreglo:**
  - Cambiar la imagen por una de la barra larga: P362, P297 y P184 ya están en la selección. La lámpara puede ir al par.
  - Componer: `.barra-foto { grid-column: 1 / span 7; aspect-ratio: 16/9 }` y `.barra-txt { grid-column: 9 / span 4; align-self: end }`. O que la barra sea la **banda** a sangre (la barra es "de esas para sentarse y quedarse ahí") y El salón pase al par.
  - El crédito de un fotograma de video se escribe "Foto (video) @rober.patagonico" o se usa el video.
- **Regla:** Taste pass 5 y cap "half the width empty"; Impeccable "one decisive photo".

**P1-6 · landing · ≥1024 · `landing-1440-s02, s07, s10, s16, s20, s23`**
- **Qué está mal:** siete capítulos abren con el mismo split: display de 7 columnas a la izquierda y 4:5 de 5 columnas a la derecha (o vacío, en Comida y Con quién). Esto es lo que vuelve la página "kit" después de la tercera pantalla.
- **Arreglo:** dar a cada capítulo una composición propia del vocabulario que ya existe en `skills-notes.md` §2:
  - **El lugar:** abre con la **banda a sangre**, con el titular encima de una franja de noche.
  - **Tragos:** titular de 12 columnas en una línea ("MEJOR LOS TOMAMOS TODOS!", 25 caracteres caben en 12 columnas a 210 px) con el mosaico debajo; la copa splash sale (ver P2-3).
  - **Comida:** foto sostenida a la **derecha** (8 / span 5) con el titular y el texto a la izquierda; hoy la derecha de `s10` es campo verde vacío.
  - **Con quién:** queda como statement + mosaico, pero con el párrafo literal bajo el titular, no flotando a la derecha.
  - **Eventos:** el calendario a 12 columnas, con las fotos en tira debajo.
- **Regla:** Taste pass 9 (sameness), tells §5; Impeccable "una sección por efecto": aquí es lo contrario, un mismo esqueleto para todas.

**P1-7 · landing · ≥1024 · `landing-1440-s10.jpg`, `s11.jpg`**
- **Qué está mal:** en Comida, bajo "PA CHUPARSE EL BIGOTELI" quedan ~700×480 px de verde vacío a la derecha. Después, la foto sticky de la izquierda corre sola mientras la columna derecha (el texto ya terminó con "Ver la comilona") queda vacía por otra pantalla entera (`s11`).
- **Arreglo:** `.comida-txt { grid-row: 1 / span 3; grid-column: 8 / span 5; align-self: end }` para subir el texto junto al titular, y quitar el `position: sticky` de `.sostenida`: no hay texto que pase junto a ella.
- **Regla:** Taste cap "blank stretch > half a screen".

**P1-8 · landing · todos · `landing-1440-s21.jpg`, `landing-390-s22.jpg`**
- **Qué está mal:** el calendario de Eventos solo lista años pasados. Hoy es 21 de octubre de 2026 y "Octubre · Jalogüín · 2023·2024·2025" no avisa que viene en 10 días. Es lo primero que pregunta el local. A la derecha quedan ~700 px vacíos bajo la foto.
- **Arreglo:**
  - Marcar el próximo evento por mes en JS (mismo mecanismo que "Hoy", en America/Santiago): `li[data-mes="10"]` recibe `.es-prox` (Oswald 600, y "Este mes" [UI] como `.es-hoy-m`, **sin subrayado**).
  - Mover `.eventos-foto` a `grid-row: 4` junto al calendario (`9 / span 4`, `align-self: start; position: sticky`) o cambiarla a tira de 3 bajo la lista.
- **Regla:** Nielsen 1; persona local; Taste pass 5.

**P1-9 · landing y carta · DPR 2 · `i-cover-dpr2-crop.png`**
- **Qué está mal:** P189 a 1:1 en retina se ve cerosa (compresión de IG + 1440 px). La portada es el 100 % del primer viewport.
- **Arreglo:** pedir el original en alta **antes** de mostrarlo al cliente. Mientras tanto, servir `srcset` con la versión de 1440 a 1× y no ampliarla con CSS (ya se cumple). Bajar `object-position` en ningún caso: no hay más píxeles.
- **Regla:** PRODUCT "no se agranda ninguna imagen"; cliente premium.

### P2
**P2-1 · landing · todos · `landing-1440-s01.jpg`, `s10`, `s17`; nav**
- **Qué está mal:** dos botones barra en la primera pantalla (nav "Ver la carta" y "Cómo llegar"). "Ver la carta" aparece en barra (nav), en noche (Hoy y Tragos), en barra otra vez (Sin alcohol, `s10` arriba) y en azul (carta).
- **Arreglo:** el botón de la portada pasa a enlace (`.cover .btn` → `.link`, "Cómo llegar" subrayado) y deja el único primario de la pantalla al de la nav. En "Sin alcohol" (`index.html`, `.sin-acc`), "Ver la carta" pasa a `.link`.
- **Regla:** `sistema.md` §7 ("uno primario por pantalla"); Nielsen 4.

**P2-2 · landing y carta · todos · `landing-1440-s14.jpg` ("Peazo de equipo"), `s12` ("La carta"), `s25` (firma), carta ("Cocteleria de la casa", "Comilona")**
- **Qué está mal:** Six Caps con minúsculas da Mayúscula alta + versalitas, mientras otros titulares salen en caja alta pareja. Leído en conjunto parece un error de cuerpo de letra en la inicial.
- **Arreglo:** decidirlo una vez: `.display, .head, .firma { text-transform: uppercase }`. La caja literal se conserva en el DOM y en el lector de pantalla, y visualmente todo va en el registro del letrero.
- **Regla:** Nielsen 4; Taste pass 6.

**P2-3 · landing · todos · `landing-1440-s07.jpg`**
- **Qué está mal:** la foto líder de Tragos es una copa con salpicadura sobre bokeh. Es justo el "bar premium de chorro" que rechaza THESIS en `contrato.md`, y la que menos dice "Almud".
- **Arreglo:** líder = el bartender del muro rosa (`tragos-bartender-muro-rosa`, que hoy está en el mosaico); la salpicadura sale o pasa a ser la más chica del mosaico.
- **Regla:** contrato THESIS; Impeccable especificidad.

**P2-4 · landing · todos · `landing-1440-s04.jpg`, `landing-390-s04.jpg`, `landing-390-s05.jpg`**
- **Qué está mal:**
  - "Los sillones" es un primer plano de una clienta y no se ve ningún sillón.
  - "La terraza" es de día, de espaldas, sobre grava: la foto más fome de la página y en el capítulo que abre después de la fiesta.
  - En el teléfono, las dos columnas del mosaico dejan los textos en ~170 px (líneas de 3 a 4 palabras).
- **Arreglo:**
  - Rotular lo que se ve ("Los sillones" solo cuando llegue la foto pedida; mientras, que la foto vaya sin rótulo de rincón) y cambiar la terraza por la de noche con guirnaldas (la de la esquina de `s03`).
  - En <700 px, `.mosaico .mo-1, .mo-2 { grid-column: 1 / -1 }` con `.mo-2 { margin-top: var(--sp-7) }` alternando 3/4 de ancho izquierda y derecha (`1 / span 3` y `2 / span 3`) para que los textos tengan ≥ 270 px.
- **Regla:** Taste pass 8 ("every image doing a job"); Nielsen 2.

**P2-5 · landing · 1440 · `landing-1440-s19.jpg`, `z-cifras-1440.jpg`; 390 `landing-390-s20.jpg`**
- **Qué está mal:** "4,6 / 4,6" en Six Caps head apilados, con las comas casi tocando la línea siguiente y "oct-2026" suelto debajo. Es el bloque de métrica de plantilla. A 390, "Castro" queda viuda.
- **Arreglo:** pasar las cifras a una sola línea de cuerpo dentro del párrafo: "4,6 en Google (848 reseñas) · 4,6 en Tripadvisor, #1 de 6 bares en Castro · oct-2026". Si se mantiene el número grande, uno solo (Tripadvisor #1) con `line-height: 1` y `margin-bottom: var(--sp-3)`.
- **Regla:** craft-floor Refuse ("hero-metric template").

**P2-6 · carta · 1440 y 390 · `carta-1440-s00.jpg`, `carta-390-s00.jpg`, `i-carta-chip-1440.jpg`**
- **Qué está mal:**
  - La lámina de pestaña es un fotograma de video borroso: botellas inclinadas en Coctelería y una cazuela con desenfoque de movimiento en Comilona. En el teléfono va a media columna con la otra mitad vacía, y la primera pantalla de la carta no muestra ni un trago.
  - Las filas con miniatura empiezan en x = 775 y las sin miniatura en x = 615, con dos bordes izquierdos alternando.
- **Arreglo:**
  - Lámina = la mejor foto real del grupo (Pinche Güey / Sagüer on Faia, Pizza). El video, si queda, va en loop solo a ≥ 1024 y con un póster nítido.
  - En <1024, `.lamina { grid-column: 1 / -1 }` (ancho completo, 16:9) o eliminarla y dejar que las filas con foto lleven la imagen.
  - Filas: dar a todas la columna de miniatura (`.fila { grid-template-columns: var(--th) 1fr auto }` con la celda vacía cuando no hay foto), o a ninguna miniatura en ≥ 1024 y las fotos solo en la lámina.
- **Regla:** Taste pass 4 (edges) y pass 8; PRODUCT "no se agranda".

**P2-7 · carta · todos · `carta-1440-s00.jpg`**
- **Qué está mal:** la cabecera de la carta solo tiene el logo e ES/EN. No hay "Inicio", "Cómo llegar" ni "Escríbanos al DM" hasta el pie, y el turista que llegó a la carta desde un enlace compartido no tiene la acción a mano.
- **Arreglo:** en `.nav-carta`, `.nav-end` con "Cómo llegar" (enlace) y "Escríbanos al DM" (`.btn` barra); a la izquierda, junto al logo, "← Inicio" [UI] en `.link`.
- **Regla:** PRODUCT principio 4 ("útil en diez segundos"); Nielsen 3.

**P2-8 · carta · 390 · `i-carta-promos-390.jpg`**
- **Qué está mal:**
  - El sábado no tiene foto: su nombre arranca en x = 16 mientras los otros arrancan en x = 136.
  - La hoja de "Hoy" (`.promo { margin: -12px }`) se sale del margen hasta x = 4.
  - "ALMUDCITO PROMOS" va en mayúsculas chicas bajo el título, como un eyebrow invertido.
  - Día en noche + trago en azul en la misma línea: dos colores en un titular.
- **Arreglo:**
  - `.promo { margin-inline: 0; padding-inline: var(--sp-3) }`, y que la hoja quede dentro de la grilla.
  - El sábado con la celda de foto vacía (misma columna) o la foto del Ramón si existe.
  - "Almudcito promos" en caja de oración, tamaño body.
  - El día en una línea propia (`.fdia { display:block }`).
- **Regla:** Taste tells §2 (eyebrow) y §2 (una palabra en otro color); pass 4.

**P2-9 · landing · todos · `landing-1440-s02.jpg`, `landing-390-s02.jpg`**
- **Qué está mal:** "siempre es un güen día pa compartir algo rico" va en small sobre la lista de días, como rótulo chico encima de un bloque. Y el "Hoy" del miércoles va subrayado como si fuera un enlace.
- **Arreglo:** subir la frase a `body` y ponerla como cierre del bloque de la promo (después de "Mitad de semana…"), no como rótulo. `.es-hoy-m { text-decoration: none; background: var(--tinta); color: var(--campo); padding: 2px 6px }`, el mismo tratamiento que `.hoy-m` de la carta.
- **Regla:** skills-notes §3 ("sin rótulos chicos sobre los títulos"); Nielsen 4.

**P2-10 · landing · ≥1024 · `landing-1440-s24.jpg`**
- **Qué está mal:** el video de la fachada (el único plano de la calle que existe y lo más útil para "¿cómo lo reconozco?") va a 6 columnas, con la mitad derecha vacía y separado ~1 pantalla de "Cómo llegar". El brief pide **mapa** y no hay ninguno.
- **Arreglo:**
  - `.donde-video { grid-column: 1 / span 7 }` y, en las columnas 9–12 de la misma fila, un mapa estático (imagen de OSM de Serrano 325, `<a>` a Google Maps, `alt` "Mapa: Serrano 325, al frente del Centro Cultural de Castro").
  - Que el video vaya antes de la foto del megáfono (el reconocer la puerta es parte de llegar).
- **Regla:** brief §6; Taste cap "half the width empty".

**P2-11 · landing · EN 390/1440 · `landing-en-1440-s01.jpg`, `sheet-landing-en-390-*`**
- **Qué está mal:** en EN cada dato sale dos veces (ES y glosa): "de 18:00 a 22:00 hrs / 6 to 10 pm", "* Siempre sujeto a stock! * / * Always subject to stock! *", "$ 4.500 / CLP 4,500". La landing pasa de 28 a 31 pantallas.
- **Arreglo:** glosar solo lo que no se entiende: léxico, titulares y citas. Los datos universales (horas, precios y "stock") van **solo en EN** dentro de `html[lang=en]` usando `data-en` sobre el mismo nodo, como las etiquetas [UI], no como `.gl` adicional.
- **Regla:** carga cognitiva; Nielsen 8.

**P2-12 · landing · todos · `landing-*-metrics.json` (`small`)**
- **Qué está mal:** los créditos "Foto @…" miden 21 px de alto, por debajo del mínimo AA de 24 px (WCAG 2.5.8). Los @ del equipo miden 32 px a 390.
- **Arreglo:** `.pie a, .banda-pie a { display:inline-block; padding-block: 2px; min-height: 24px }`; `.equipo-nombres a { min-height: 44px; display:inline-flex; align-items:center }` a <700 px.
- **Regla:** PRODUCT Accesibilidad (≥ 44 px), WCAG 2.2.

**P2-13 · landing · todos (estructura)**
- **Qué está mal:** "Con quién" llega 10 pantallas después de Comida, y la carta destacada repite tragos y platos ya vistos. La página mide 26 pantallas.
- **Arreglo:**
  - Orden: Hoy → Lugar → Tragos (con "No dejamos a nadie ajuera" como sub-bloque dentro del amarillo, no como sección propia) → Comida → **carta destacada** (pegada a Comida, como "lo que hay") → Con quién → Equipo (o dentro de Lugar/Tragos: "son los encargados de barra y salón") → Reseñas → Eventos → Dónde.
  - Recortar "El lugar" a titular + banda + 3 rincones. "El salón" y "El mural" quedan como par solo si cada uno trae una foto que no se repita.
- **Regla:** brief "Estructura"; Taste pass 11.

### P3
- **P3-1 · landing · 390/768 · `landing-390-s00.jpg`:** el crédito de la portada es una pastilla gris semitransparente arriba a la derecha, sobre las cintas, y parece calcomanía. Arreglo: moverlo abajo a la derecha dentro del scrim, sin fondo (`background:none`), en papel-suave.
- **P3-2 · landing · 1440 · `z-cover-1440-logo.jpg`:** el isotipo se monta sobre el letrero neón "Almud" de la foto, con dos logos superpuestos, y la punta superior entra en las cintas. Arreglo: `.cover-title-box { top: calc(var(--S) * .252 - var(--lift)) }` (bajar ~13 px a 1440) o `.cover-logo { width: calc(var(--S) * .35) }`, y comprobar que la punta inferior siga sobre el zinc y no sobre las cabezas.
- **P3-3 · landing · 1440 · `z-cover-1440-info.jpg`:** la "C" de "Coctelería" toca la rejilla del calefactor. Arreglo: `.cover-info { right: calc(var(--margin) + 8px); width: calc(var(--S) * .25) }`, o subir el bloque `0.01·S`.
- **P3-4 · landing · 1440 · `landing-1440-s15.jpg`:** en Equipo hay un hueco de línea vacía entre "Est@s guapetones…" y "le ponen una sonrisota…" (dos `<p>` con `gap` + `margin`). Arreglo: `.equipo-txt { gap: var(--sp-2) }`.
- **P3-5 · landing · todos · `landing-1440-s25.jpg`:** el logo gigante del pie es una pantalla entera sin nada que leer. Arreglo: `.pie-logo { width: min(100% - 2*var(--margin), 960px) }` alineado a la izquierda, o que ocupe el espacio vacío bajo la firma.
- **P3-6 · landing · jueves:** `hoy-jueves-sangria` aparece en Hoy y en la carta destacada. Arreglo: otra foto de sangría para el día, o la destacada usa la de `carta-v2.json › img`. Además, `con-quien-solo` se repite en el día sin promo y en Con quién.
- **P3-7 · landing · todos:** el crédito "Video @rober.patagonico" va bajo una foto fija. Arreglo: "Foto @rober.patagonico (de su video)" o el video.
- **P3-8 · carta · 1440 · `carta-1440-s03.jpg`:** una banda rosada de ~200 px de `.cp` vacía antes del pie, por el `min-height: calc(100svh - var(--tabs-h))` aplicado a una pestaña corta. Arreglo: `.js .cp { min-height: 0 }` y aceptar el salto del pie, o `min-height` solo en <1024.
- **P3-9 · motion:** las filas de Emil que no bloquean (600 ms suelto, reveal de reseñas, entrada de la carta al cargar, color de pestaña por teclado, WebM faltante).

---

## 4. Personas

**Turista extranjero en Castro** (EN, teléfono, decide hoy)
- La portada en EN se entiende: "Signature cocktails…" y "Open Tue to Sat from 6 pm".
- Pero a 375×667 la portada le pone el logo sobre las caras (P1-3), y la franja del miércoles le muestra cada dato dos veces (P2-11).
- En la carta, desde el teléfono no ve que existe "Comilona" (P1-1), y la carta no tiene "Cómo llegar" arriba (P2-7).
- No hay mapa (P2-10).

**Local de Castro** (ya conoce el bar)
- Se lleva lo que busca en 1 pantalla: la promo de hoy. Bien.
- Pero el viernes no está en la semana (P1-2), y Jalogüín, que es en 10 días, no aparece como próximo (P1-8).
- Si abre la carta en el teléfono para ver pizzas, tiene que adivinar que la barra se desliza.

**Casey** (móvil, distraída)
- 28 pantallas.
- Si toca "Menú" dos veces rápido, la página queda congelada (P0-1).

**Sam** (teclado/lector)
- Skip link, h1 con texto oculto y foco visible en tinta de superficie (`i-focus-9-1440.jpg`): bien.
- El orden de foco sigue el visual.
- Los créditos de 21 px están bajo el mínimo (P2-12).

**Riley** (estrés)
- A 320 EN no hay desborde (scrollWidth 320), pero la portada colapsa la legibilidad (P1-3).

---

## 5. Lo que está bien y no se toca

1. **La portada a 1280–1920 (DPR 1).** El techo de cintas, el logo sobre el zinc, las caras libres en el tercio inferior y el scrim radial que no se ve como velo. A 1920, la foto queda en 1440 con noche a los lados, como manda el contrato (`landing-1440-s00`, `landing-1920-s00`).
2. **"Hoy en Almud" como cosa viva:** el campo del día, el titular literal enorme, la foto propia y "la franja se imprime" como único momento autoral. Es la mejor idea de la página; se arregla el viernes, no el dispositivo.
3. **La voz.** 121 de 121 líneas son literales y trazables. No hay ni un adjetivo nuestro ni menciones a fila o espera.
4. **Los campos planos con su tinta y sus cortes duros.** Amarillo para tragos, verde para comida, fucsia para con quién y coral para eventos, sin dos campos por pantalla. El sistema de contraste se cumple.
5. **La carta destacada en papel del landing** (`landing-1440-s13/s14`): nombres azules en mayúsculas, precio magenta tabular, fotos 4:5 reales y descripción literal. Es lo más "premium" del sitio.
6. **La carta completa como objeto:** pestañas con estado claro, chips por grupo, hash y botón atrás, sin JS apilada, "Hoy" marcado en promos y teclado instantáneo.
7. **Lo técnico:** CLS 0, cero errores, cero anclas rotas, sin GSAP ni Lenis, reduced motion como variante diseñada, foco de marca, `::selection` y scrollbars con la paleta.
8. **Con quién (`landing-1440-s17/s18`):** el mosaico desigual con gente real riendo es la fiesta del brief. No se toca, salvo el botón huérfano "Cómo llegar" que flota sobre la columna central (`s17`, arriba): pasarlo a `.link` al pie del texto.
