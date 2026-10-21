# Fase 8 · Sistema de diseño v2: Almud Bar

Tokens: `css/v2/tokens.css` (solo propiedades personalizadas) + `css/v2/fonts.css` (los `@font-face`).
Contraste: `_plan/direccion/contraste.py`.
Lámina: `_plan/direccion/tile/index.html` (renders en `tile-1440-{1,2}.jpg` y `tile-390-{1,2}.jpg`).
Contrato: `contrato.md`.

---

## 1. Principios
1. **La noche es la de sus fotos.** El suelo es la sombra cálida de la barra, no un negro de plantilla.
2. **Un color de campo por pantalla, con su tinta.** Nunca arcoíris.
3. **Un solo acento (barra), solo en la acción.** Además, el foco sobre noche y la selección.
4. **Lo impreso vive solo en la carta:** papel, azul carta y magenta de precio.
5. **Esquinas rectas, sin sombras, sin líneas.** Se separa con espacio, tono o escala.
6. **Todo texto visible es de Almud.** Solo las etiquetas [UI] son nuestras.

---

## 2. Color

### 2.1 Suelo: #171515 contra #170e0b
Medí la sombra de las fotos (píxeles con L entre 8 y 40) en 16 fotos de la selección. La media es **#2a110c**: rojiza y cálida. Los afiches (Ojo Piojo) dan un negro neutro, #1f1e1d.

Lo que importa es la costura entre foto y suelo, que aparece en la portada a más de 1440 px y en cada foto del mosaico. Diferencia ΔE (CIELAB) contra los bordes de P189:

| Borde de P189 | `#171515` (neutro) | `#170e0b` (cálido) |
|---|---|---|
| izquierdo | 13,9 | **11,3** |
| derecho | 14,6 | **12,6** |
| inferior | 8,4 | **5,7** |

**Decisión: `--noche #170e0b`.** Las fotos se funden con el suelo y el negro no se ve "de plantilla". Los afiches entran como fotos, así que su negro propio no manda.

### 2.2 Roles
| Token | Hex | Rol |
|---|---|---|
| `--noche` | #170e0b | suelo de toda la página |
| `--noche-alta` | #2a1a14 | escalón de superficie (hoja del menú, paneles) |
| `--papel` | #f6ecdc | tinta sobre noche, y suelo de la carta |
| `--papel-suave` | #cbb9a5 | texto secundario sobre noche (nunca sobre campos) |
| `--barra` | #ff3f6c | **el único acento**: botón primario, selección, caret. Menos del 5 % de la pantalla |
| `--coral` `--turquesa` `--fucsia` `--amarillo` `--verde` | #f26343 #40b9c2 #cd0b61 #fac307 #06aa6b | campos de capítulo y del día (afiche Ojo Piojo) |
| `--carta-azul` | #2023e4 | nombres de la carta; botón sobre papel (`--allow palette-purple`: es el azul impreso) |
| `--carta-magenta` | #cd007a | precios. Es el impreso #ec008c oscurecido un 13 % en L para pasar AA |
| `--scrim` | rgb 12 7 5 | único degradado: scrim neutro y localizado bajo el tipo sobre foto |

### 2.3 Campos: a qué capítulo van
| Capítulo | Campo | Tinta | Razón |
|---|---|---|---|
| El lugar | noche | papel | el color lo ponen las cintas fotografiadas |
| Los tragos | **amarillo** | noche | complementa los muros rojo y rosa de P362, P297 y P184 (afiche Mambo Tiki). El fucsia de la fase 7 se empastaba |
| La comida | **verde** | noche | complementa la comida cálida |
| Con quién | **fucsia** | papel | la tira de gente de Ojo Piojo; fotos con poco rojo |
| Eventos | **coral** | noche | el primer color del afiche |
| Cuándo y dónde | noche | papel | cierre oscuro |
| Carta | papel | noche, azul, magenta | la única hoja |

El **día** (cosa viva) usa su propio campo: Mar coral · Mié turquesa · Jue fucsia · Vie amarillo · Sáb verde. La banda del día va inmediatamente después de la portada, y el capítulo que la sigue (El lugar) va sobre noche. Así dos campos nunca comparten pantalla.

### 2.4 Contraste (WCAG 2.x, calculado con `contraste.py`)
| Tinta | Fondo | Uso | Ratio | Mín. | |
|---|---|---|---|---|---|
| papel | noche | cuerpo y titulares | 16,26 | 4,5 | pasa |
| papel suave | noche | secundario | 9,98 | 4,5 | pasa |
| papel | noche alta | menú, paneles | 14,29 | 4,5 | pasa |
| papel suave | noche alta | secundario en panel | 8,77 | 4,5 | pasa |
| barra | noche | acento como texto o foco | 5,60 | 4,5 | pasa |
| noche | barra | texto del botón primario | 5,60 | 4,5 | pasa |
| noche | coral | tinta del campo | 6,02 | 4,5 | pasa |
| noche | turquesa | tinta del campo | 8,09 | 4,5 | pasa |
| papel | fucsia | tinta del campo | 4,70 | 4,5 | pasa |
| noche | amarillo | tinta del campo | 11,66 | 4,5 | pasa |
| noche | verde | tinta del campo | 6,31 | 4,5 | pasa |
| azul carta | papel | nombres | 7,41 | 4,5 | pasa |
| magenta #cd007a | papel | precios | 4,63 | 4,5 | pasa |
| noche | papel | descripciones de la carta | 16,26 | 4,5 | pasa |
| papel | azul carta | botón sobre papel | 7,41 | 4,5 | pasa |

**Pares rechazados, con su arreglo:**

| Par rechazado | Ratio | Arreglo |
|---|---|---|
| papel / coral | 2,70 | noche sobre coral |
| papel / turquesa | 2,01 | noche sobre turquesa |
| papel / amarillo | 1,39 | noche sobre amarillo |
| papel / verde | 2,58 | noche sobre verde |
| papel / barra | 2,90 | texto noche en el botón |
| noche / fucsia | 3,46 | papel sobre fucsia |
| magenta impreso #ec008c / papel | 3,63 | #cd007a |
| barra / fucsia | 1,62 | sobre un campo, el botón pasa a noche |

`rutas.md` decía "papel sobre coral y verde": no pasa, y queda corregido. Los anillos de foco cumplen el mínimo de 3:1 contra su fondo con la tinta de la superficie: papel sobre noche, noche sobre campos claros, papel sobre fucsia y azul sobre papel.

### 2.5 Tintes de la carta (fase 16)
La carta en su página lleva un fondo suave por pestaña: lo pidió el cliente y se mantiene. Desde la fase 16 ya no son hex escritos a mano: cada tinte **se deriva** de los tokens del sistema, mezclando el campo de su pestaña con `--carta-hoja` (#fffaf3, la hoja clara) en `tokens.css`:

| Token | Fórmula | Resultado | Magenta | Azul carta | Noche |
|---|---|---|---|---|---|
| `--tinte-fucsia` | `color-mix(in srgb, var(--fucsia) 8%, var(--carta-hoja))` | #fbe7e7 | 4,56 | 7,30 | 16,02 |
| `--tinte-turquesa` | `… var(--turquesa) 12% …` | #e8f2ed | 4,73 | 7,58 | 16,62 |
| `--tinte-amarillo` | `… var(--amarillo) 12% …` | #fef3d7 | 4,90 | 7,85 | 17,22 |
| `--tinte-coral` | `… var(--coral) 12% …` | #fde8de | 4,58 | 7,34 | 16,10 |
| `--tinte-verde` | `… var(--verde) 12% …` | #e1f0e3 | 4,58 | 7,34 | 16,10 |
| `--tinte-papel` | `var(--papel)` (Comilona) | #f6ecdc | 4,63 | 7,41 | 16,26 |

- La regla: 12 % de campo; el fucsia, que oscurece más, 8 %. Con más campo el magenta de los precios baja de 4,5:1.
- Se fueron los `-fuerte` (fondo de chips): los chips pasan a texto azul subrayado y el activo en noche (no hay superficie nueva).
- Se fue la hoja blanca de la promo de hoy: el día se marca solo con la etiqueta ‹Hoy›. La carta no tiene superficies elevadas.

---

## 3. Tipografía
**Dos familias, autoalojadas en `assets/fonts/`:**
- **Six Caps 400** para display. Viene de su letrero. Sus minúsculas son versalitas, así que se respeta la caja literal de la fuente.
- **Oswald 300 / 400 / 600** para todo lo demás. Es la letra de su carta.
- Big Shoulders y Caveat no se cargan en la v2: Big Shoulders vive solo dentro del SVG del logotipo.

**Prueba de Oswald para párrafos de 18 px (ES y EN), sobre noche y sobre papel:**

| Peso | Resultado |
|---|---|
| 300 a 18/1,55, +0,01em sobre oscuro | se lee bien. Con `max-width: 34em` da unos 66 caracteres por línea (Oswald es condensada: 60ch dan 66 caracteres) |
| 400 en cuerpo | pesa demasiado sobre noche (irradiación) |
| 400 a ≤16 px y en etiquetas | se mantiene |

**Decisión:**

| Uso | Peso |
|---|---|
| cuerpo | **300** |
| small, UI, datos | **400** |
| nombres de tragos, promo, botones | **600** |

Oswald aguanta párrafos de 1 a 4 frases, que es todo lo que tiene este sitio. No se componen textos largos.

**Escala (5 pasos):**
| Paso | Familia | Tamaño | Interlineado | Uso |
|---|---|---|---|---|
| display | Six Caps 400 | `clamp(96px, 52px + 11vw, 216px)` (96 → 210 en 1440) | 0,86 | titular de capítulo y del día, "La carta" |
| head | Six Caps 400 | `clamp(56px, 40px + 4vw, 104px)` (56 → 98) | 0,9 | categorías de la carta, precio de la promo |
| lead | Oswald 400/600 | `clamp(22px, 18px + 0.6vw, 28px)` | 1,25 | bio, nombres y precios de la carta, ítem de la promo |
| body | Oswald 300 | `clamp(17px, 16px + 0.14vw, 18px)` | 1,55 | párrafos, datos, enlaces |
| small | Oswald 400 | 14px | 1,4 | créditos, notas, "* Siempre sujeto a stock! *" |

- Display/body = 11,7×; head/body = 5,4×.
- Tracking: Six Caps +0,01em (en caja alta va de 0 a +0,03em); cuerpo sobre oscuro +0,01em.
- `text-wrap: balance` en titulares y `pretty` en cuerpo.
- `tabular-nums` en precios y horarios.

**Aritmética de dos líneas.** El `k≈0,40` de las notas es un valor genérico de las condensadas. **Six Caps medido da k = 0,22** (caja alta 0,223, en Chromium). Oswald 600 da 0,40. Se presupuesta con 0,22, y a mano se deja un margen del 15 % para el inglés.

| Ancho | Columna | Tamaño | Caracteres por línea | Ejemplo | Líneas |
|---|---|---|---|---|---|
| 390 | 358 px | 96 px | ≈17 | "mejor los / tomamos todos!" (9 + 14) | 2 ✓ |
| 1440 | 7 columnas, 790 px | 210 px | ≈17 | "Miércoles de / piscoleinnnn!" (12 + 13) | 2 ✓ |
| 1440 | 6 columnas, 676 px | 210 px | ≈14 | "tomamos todos!" (14) | se partía en 3: los titulares de capítulo toman **7 columnas** y el corte se autoriza con `<br>` |

**Presupuesto de titular:** ≤ 30 caracteres en display, ≤ 32 en head.

---

## 4. Grilla y espacio
- **Márgenes:** `clamp(16px, 2.2vw, 32px)`, iguales a ambos lados. La nav va en los mismos márgenes.
- **Columnas:** 4 en teléfono, 8 desde 700 px y 12 desde 1024 px. Gutter `clamp(12px, 1.6vw, 24px)`. La grilla nunca se dibuja.
- **Anclas de texto:** columna 1 y columna 8 (la línea del 58 %). Un solo momento centrado en toda la página: ninguno en la lámina.
- **Espaciado:** base 4 (4, 8, 12, 16, 24, 32, 48, 64, 96).
- **Entre secciones:** `clamp(72px, 4px + 11vw, 200px)`, que da 72 en teléfono y 162 en 1440. Más aire arriba de un titular que abajo.
- **Fotos:**
  - 4:5 (retrato) y 16:9 (banda) cubren todas salvo la portada, que tiene forma de pantalla.
  - `object-fit: cover` con `object-position` elegido por foto.
  - Esquinas rectas (`--radius: 0`), sin marco ni sombra.
  - Ninguna se amplía: `--photo-max: 1440px` para P189, y las bandas a sangre solo con fotos de unos 3000 px.
- **Portada a más de 1440 px:** la foto se queda en 1440 centrada, con noche a los lados (verificado a 1920). La nav ocupa todo el ancho.

---

## 5. Superficies del navegador
| Superficie | Tratamiento |
|---|---|
| `::selection` | fondo barra, texto noche (5,6:1) |
| `caret-color` | barra |
| Foco (`:focus-visible`) | contorno de 3 px a 3 px de distancia, en la **tinta de la superficie** (papel sobre noche, noche sobre campo claro, papel sobre fucsia, azul sobre papel). Nunca anima |
| Scrollbar | `scrollbar-color: papel-suave noche`; en carruseles, visible siempre |
| Subrayado | grosor .08em, `text-underline-offset: .18em` |
| Otros | `-webkit-tap-highlight-color: transparent`; `touch-action: manipulation` en controles; `theme-color #170e0b` |

---

## 6. Movimiento (Emil §6, tokens únicos)
**Curvas:**
- `--ease-out` cubic-bezier(.23,1,.32,1)
- `--ease-in-out` (.77,0,.175,1)
- `--ease-drawer` (.32,.72,0,1)
- `--ease-hover` ease

**Duraciones:**

| Token | Valor |
|---|---|
| `--d-press` | 140 |
| `--d-hover` | 200 |
| `--d-ui` | 240 |
| `--d-panel` | 400 (salida 250) |
| `--d-reveal` | 700 |
| `--d-hero` | 800 |
| `--stagger` | 40 |
| `--stagger-card` | 60 |
| `--d-fade-reduced` | 180 |

En GSAP se usa `CustomEase` con los mismos nombres y `gsap.defaults({ease:'out', duration:.24})`.

**Reglas:**
- **Un momento autoral:** "la franja se imprime" (ver `contrato.md`).
- Reveals `once` cortos: máscara de línea en los titulares, `clip-path` en las fotos. El cuerpo aparece sin animación.
- Presión .97 en todo lo presionable. Hover solo con `(hover:hover) and (pointer:fine)`, y cambia color, nunca el peso.
- Nunca ease-in, bounce, `scale(0)` ni bucles ociosos.
- `prefers-reduced-motion`: fades de 180 ms; fuera transform, scrub, parallax y Lenis.

---

## 7. Componentes (vocabulario)
- **Botón.** Se decide una vez:
  - Forma: rectángulo plano de esquinas rectas, alto 48 px, padding 0 22 px, Oswald 600 17 px, en minúsculas de frase. Uno primario por pantalla.
  - Por superficie: sobre **noche**, barra con tinta noche; sobre un **campo**, noche con tinta papel; sobre **papel**, azul carta con tinta papel.
  - Hover: se invierte a papel con tinta noche (en papel, a noche).
  - Presión: `scale(.97)` en 140 ms. El foco sigue la §5.
- **Enlace.** Oswald 400 en tamaño body, siempre subrayado, con área táctil de 44 px.
  - Hover sobre noche: el subrayado pasa a barra.
  - Hover sobre campo o papel: el subrayado engruesa a .16em.
  - Etiquetas [UI]: "Cómo llegar", "Escríbanos al DM", "Ver la carta", "Carta completa", "Menú".
- **Nav.**
  - Escritorio: barra plana sobre noche, de 72 px, con 5 enlaces (El lugar, Tragos, Comida, Con quién, Eventos) y [Ver la carta]. No va encima de la foto.
  - Teléfono: 56 px, con "Menú" en texto y [Ver la carta]. El menú es una hoja a pantalla completa sobre noche alta (`clip-path` en 400 ms con `--ease-drawer`, cierre en 250 ms, Escape cierra al instante).
- **Fila de carta.**
  - Nombre en Oswald 600, lead, MAYÚSCULAS, azul carta. Precio en Oswald 600, lead, magenta, tabular y alineado a la derecha en la misma línea base.
  - Descripción en Oswald 300 body, tinta noche, de 40em como máximo.
  - Filas separadas por 32 px de espacio, nunca con líneas; dos columnas desde 900 px.
  - Las categorías van en Six Caps head con tinta noche, y el título "La carta" en Six Caps display azul.
- **Marco de foto.** `figure` con proporción 4:5 o 16:9, `object-fit: cover`, fondo noche mientras carga, sin borde. Pie opcional en small con el crédito tal como lo da la marca ("Foto @estudiouno.prod").
  - En la carta, la lámina de un plato lleva su foto real según `carta.json › img`, y el nombre ya está en la fila.
- **Banda de campo (capítulo).** Ocupa el ancho completo con un solo campo plano y su tinta.
  - Titular literal en Six Caps display de 2 líneas, en 7 columnas.
  - Una foto líder (de 5 columnas o más, 4:5), un párrafo literal y un enlace.
  - Mosaico desigual de 3 fotos 4:5 a 4 columnas, con desfases de 0, 160 y 56 px.
  - Corte duro con la sección vecina, que nunca es otro campo.
- **Promo del día ("Hoy en Almud").** Banda del campo del día.
  - Titular: la caption literal del día en Six Caps display.
  - El ítem en Oswald 600 lead, "$ 4.500" en Six Caps head tabular, "de 18:00 a 22:00 hrs" y "* Siempre sujeto a stock! *".
  - Una frase literal, el botón y el enlace.
  - Foto del día (IG-019 el miércoles), en 5 columnas.
  - La semana completa en 4 columnas: el día de hoy en 400, los demás en 300.
  - Lleva el momento autoral.
- **Portada.** Ver el contrato (FIRST VIEWPORT). Scrim neutro y radial (`closest-side`, de .82 a 0) detrás de cada bloque de tipo en escritorio. En teléfono, lineal desde el 40 % inferior. Nunca un velo de color ni uno que cruce las caras.

---

## 8. Verificación
- **Renders mirados:** 1440, 1920 (portada) y 390. Hubo cuatro iteraciones; se corrigieron:
  - las caras tapadas por el logotipo;
  - la colisión de clases de campo;
  - el titular de 3 líneas;
  - los huecos del mosaico;
  - un desborde horizontal de 6 px a 390;
  - la imagen lazy en negro en la captura.
- **`lint.mjs` (Taste):** 0 FAIL, 0 WARN en `tile/index.html` y en `css/v2/`. Los tres degradados del scrim llevan `taste-skill-ignore` declarado: es la excepción que la propia regla nombra.
- **`inspect.mjs` (informativo, sobre la lámina):** quedan 4 FAIL propios del formato lámina.
  - `still-page`: la lámina es estática; el momento se ve con el botón "Repetir la franja".
  - `empty-screens` 1–2 y `covered-text`: las réplicas de teléfono son `inert` y `aria-hidden`, y el inspector las ignora o las ve recortadas.
  - Un falso eyebrow: el botón "Carta completa" al final de la carta.
  - **Advertencias:** `palette-cream`, que se defiende porque #f6ecdc es el papel de sus posavasos y lo pidió el cliente; `no-footage`, porque los videos van en el sitio y no en la lámina.
  - El sitio real debe pasar inspect con 0 FAIL a 390, 768 y 1440.
