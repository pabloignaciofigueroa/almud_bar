# Fase 7 · Dirección visual v2: tres rutas

Este documento es dirección, no código. Lo que manda: `brief-v2.md`, `PRODUCT.md`, `skills-notes.md`, `v1-antireferencia.md` y la selección del jurado (`seleccion.json`, 31 imágenes).
Seguí Impeccable new-work §3 (pasos 1–5) y la run de Taste (pasos 3 y 4).

**Imágenes** (en `_plan/direccion/`): moodboards `ruta-{a,b,c}.jpg`; bocetos de primer viewport `ruta-{a,b,c}-viewport.jpg` (1440×900 y 390×844, Six Caps y Oswald reales, copy literal); script `_render_rutas.py`.

Hoy es miércoles 21-10-2026, así que los bocetos muestran la promo real del miércoles [CARTA-7].

---

## 1. Mecanismo, escena y surco

**Mecanismo, en una frase.** Almud es el bar de Serrano 325 donde un martes cualquiera a las 18:00 se ve como un aniversario: la barra llena, el techo de cintas y tragos con nombre de chiste.

**Escena real.** Alguien en Castro, en el hostal o saliendo de la pega, mira el teléfono a las 17:30, de noche y a veces con mala señal, y decide adónde ir hoy.

**Hogar cultural.** La gráfica que el bar ya publica: sus afiches sobre negro (condensada en caja alta, una script, franjas de cinta; 13 de 21 afiches, `material.md` §8), su carta impresa (nombres azules, precios magenta), el letrero luminoso, el techo de cintas, Castro de noche.

**Qué debe probar la primera superficie.** Que hoy hay fiesta, y qué hay hoy, cuándo, dónde y con qué carta.

**El surco (fuera de la lista).**
- *La página que la categoría siempre hace:* el bar de coctelería "premium": casi negro, serif dorada, video de un chorro en cámara lenta, "Experiencia de mixología", botón Reservar.
- *Su opuesto predecible:* la web de cotillón: papel picado, arcoíris en todo, confeti y rotaciones. Es exactamente la v1.

Las dos quedan fuera.

## 2. Siete mundos candidatos (de la cultura de Almud, por resonancia)

| # | Mundo | Familia material | Por qué resuena | Cómo se ve |
|---|---|---|---|---|
| 1 | **Sus afiches nocturnos** (Ojo Piojo, 9° aniversario, PRIDE, Mambo Tiki) | impreso gráfico | Es el idioma con que Almud ya le habla a Castro cada semana. El público lo reconoce de su feed. | Negro #171515, condensada blanca gigante, franjas planas de color (Ojo Piojo: coral, turquesa, magenta, amarillo, verde) con una tira de foto adentro. |
| 2 | **El techo de cintas** de la terraza techada *(el candidato circo/fiesta)* | textil y arquitectura | Es la foto más "colors" y la portada del jurado (P189). Es lo que la gente fotografía. | Foto a sangre del techo y la gente debajo. El color lo pone la foto, nunca el CSS. |
| 3 | **La carta oficial** *(la herramienta del público: cuenta para el surco, máximo uno)* | impreso, documento | Sus nombres ya son literatura: Pinche Güey, Te espero en la cuneta. | Hoja blanca, nombres en Oswald azul #2023e4, precios magenta #ec008c, dos columnas. |
| 4 | **Las pinzas de colores** (foto de perfil, posavaso, lámpara de pinzas de V014) | objeto | Es el motivo más propio y menos explotado. | Filas de pinzas sobre negro. Riesgo: la v1 las falsificó en CSS, así que solo se podrían usar fotografiadas. |
| 5 | **El letrero luminoso** de la puerta (ALMUD blanco, BAR azul) | luz y señalética | Es el umbral de Serrano 325, lo último que uno ve antes de entrar. | Caja de luz sobre negro, blanco y azul #2ba0fd. Existe solo en video de 720p (V031). |
| 6 | **El almud**, la medida chilota *(el candidato literal)* | madera y medida | Le da nombre al bar y forma al isotipo. | La caja trapezoidal del isotipo como unidad de grilla y máscara. Ya fracasó como pin en la v1. |
| 7 | **Castro de tejuelas y palafitos** | arquitectura local | Es el lugar: el turista viene a Chiloé. | Tejuela de alerce y casas de color. Es de Chiloé, no de Almud: cualquier bar de Castro lo puede usar. |

Quedaron siete mundos en seis familias materiales. Hay uno solo de fiesta (el 2) y uno solo literal (el 6). La pizarra "Almudcito HORARIOS" es un casi-duplicado de la carta y cuenta como el 3.

## 3. Sorteo (sustituto de concept-seed)

`seed: none (unavailable)`. El binario `impeccable concept-seed` no está autorizado para descargarse.
**Sustituto declarado:** el sorteo de Taste, más el pesaje de Impeccable en sus dos ejes (identificación del público y claridad del producto), hecho a mano.

Comando (salida en `_plan/direccion/draw-options.txt`):
`node $S/draw.mjs --sector restaurant --brief "Almud Bar, coctelería de autor en Castro, Chiloé, desde 2014: todos los días son una fiesta" --have photography,video --keep palette,type --options 3`

| Dirección repartida | Candidato que mejor la carga | Veredicto (identificación · claridad) |
|---|---|---|
| `page-is-the-object` | 1 (el afiche) y 3 (la carta) | **wins**: alta · alta |
| `split-stage` | 5 (el letrero) y 2 (el techo) | **competitive**: media · alta. Su disciplina se toma prestada en la ruta A (columna de foto fija en la portada). |
| `place-carries-it` | 2 (el techo de cintas) | **competitive**: alta · media. El nombre como título de película es lo que hace todo bar con terraza. |

Las tres rutas que siguen salen de cruzar los tres mundos más fuertes (1, 2 y 3) con las direcciones repartidas. Usan tres familias materiales distintas: impreso gráfico, foto de lugar e impreso documento.

---

## 4. Ruta A · El afiche de hoy

**Idea.** *"En esta página, cada día de la semana se vuelve un afiche de Almud."*
Dirección: `page-is-the-object`, donde el objeto es su afiche nocturno, con la columna fija de `split-stage`.

```
THESIS: Almud ya imprime un afiche para cada noche; la web es el afiche de hoy. Rechaza el
        "hero video + Reservar" de bar premium y el cotillón arcoíris.
OWN-WORLD: negro afiche, Six Caps blanca a escala de cartel, un solo color de franja Ojo Piojo
        por pantalla, fotos en tiras rectas dentro de la franja, botón rosa barra cuadrado.
STORY: ve qué hay hoy (promo, hora, precio), cree que esto pasa todos los días porque las tiras
        muestran la terraza llena, y abre la carta o el mapa.
FIRST VIEWPORT: izquierda, 55 %: logotipo, el DÍA en Six Caps ~300 px, la promo en Oswald 600
        del color del día, precio y hora, bio, horario y dirección, [Ver la carta] + Cómo llegar
        + DM. Derecha, 45 %: campo del color del día con P189 cortada en 3 tiras (techo, gente, mesas).
FORM: afiche-página, 1.º de la lista ordenada, seed: none (unavailable)
FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the
        verdict, DESIGN.md, and every shipping raster carrying its provenance
```

**Color: Drenched + campo por capítulo.** Superficie = el negro de sus afiches, `--noche #171515` (medido en P063), tinta `--papel #f6ecdc` (logotipo claro). Un solo acento, `--barra #ff3f6c`, solo en la acción. Las cinco franjas de Ojo Piojo (medidas en P063) se reparten por día y por capítulo, nunca juntas: Mar `#f26343` · Mié `#40b9c2` · Jue `#cd0b61` · Vie `#fac307` · Sáb `#06aa6b`. Cada campo con su tinta: negro sobre turquesa y amarillo; papel sobre magenta, coral y verde.

**Tipo.** **Six Caps** (del letrero) solo en display: el día y los titulares de capítulo de ≤2 líneas. **Oswald** (de su carta) en todo lo demás: 600 en promo y nombres de tragos, 400/300 en cuerpo (18 px) y datos. Es el par real de sus afiches; la script vive solo dentro de los afiches fotografiados (Eventos).

**Momento autoral: "la franja se imprime".** Una vez, en la carga (≤1,2 s): el día sube con máscara de línea (800 ms) y las tres tiras se abren con `clip-path inset(0 100% 0 0) → inset(0)`, stagger 90 ms, `--ease-in-out`. El resto quieto; en la página, el color de capítulo entra con corte duro, sin barridos.

**La cosa viva: el afiche cambia según el día** (hora de Chile). Mar, Mié, Jue: su promo [CARTA-7]; Sáb: "Ramón a $ 4.500!" [CARTA-7]; Vie (sin promo): "Venga venga que nadie le detenga" [IG-003]; Dom y Lun: "Abrimos de Mar a Sáb a las 18:00hrs" [BIO] + el afiche del martes. Sin JS, la semana completa como lista. Nunca hora de cierre.

**Estructura del brief.**

| Sección | Color de la franja | Contenido |
|---|---|---|
| El lugar | coral | P093 en split, la terraza (P090/P039) como banda a sangre, P114 y el mural de ojos en tiras |
| Tragos | magenta | P362 a sangre (3072 px) y P297 como marco que crece una vez; el V021 en loop |
| Comida | amarillo | P036, P393, P305 y P091 en mosaico desigual |
| Con quién | turquesa | la escena Ojo Piojo de verdad: 5 tiras de gente (P254, P031, P041, P194, P258) sobre **un** color, con su cita literal al lado |
| Eventos | verde | calendario de tamaño normal; solo aquí aparecen los nombres y los afiches reales |
| Cuándo y dónde | negro | P199 (el megáfono en la puerta) más la dirección como titular |
| Carta | sin franja | sección propia; ver §7 |

**Teléfono.** Composición propia: logotipo y [Carta] (44 px) → las 3 tiras de P189 sobre el color del día a todo el ancho → el día en Six Caps ~150 px → promo y bio → horario y dirección a 16 px. Cabe en 844 px (boceto); las tiras cambian el 3:4 de P189 por tres 16:5 nítidos.

**Riesgo honesto.** Negro + condensada pesada roza el cuarto look IA de Impeccable ("tinta plana + display condensada pesada"), y "afiche" puede leerse como "hoy hay evento". Mitigación: las fotos mandan (≥1 foto líder por pantalla), el afiche es el de *todos los días*, y nada de cajas negras, sombras desplazadas ni afiches torcidos. Jue magenta `#cd0b61` debe distinguirse del rosa de acción.

**Pecados de la v1 que evita:** arcoíris en pantalla (un color por pantalla); flecos, pinzas y polaroids CSS (tiras = fotos rectas); cargador (el afiche se lee en <1,2 s); pin de 10 pantallas; eyebrows (en el boceto saqué "Hoy miércoles" de encima del día); léxico en píldoras; >2 familias.

---

## 5. Ruta B · Bajo las cintas

**Idea.** *"En esta página, el techo de cintas de la terraza se vuelve el cielo que cubre cada capítulo."*
Dirección: `place-carries-it`.

```
THESIS: el lugar es el argumento. Una terraza llena bajo cintas no necesita adjetivos. Rechaza
        el collage de cotillón: el color es solo fotográfico.
OWN-WORLD: noche cálida #140e12 tomada de la sombra de las fotos, tinta de luz #f1e3d8, rosa
        barra solo en la acción, fotos a sangre con scrim neutro, logotipo a escala de título.
STORY: entra bajo el techo (P189), recorre los rincones como quien camina el bar, decide ir.
FIRST VIEWPORT: P189 a sangre (1440×900 sin ampliar: el asterisco, alternativa 1). Logotipo
        ALMUD BAR ~210 px abajo a la izquierda, bio, horario y dirección; acción arriba a la
        derecha; nav sin barra.
FORM: lugar a sangre, 2.º de la lista ordenada, seed: none (unavailable)
FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the
        verdict, DESIGN.md, and every shipping raster carrying its provenance
```

**Color: Restrained.** Neutros teñidos `--noche #140e12` y `--salón #46201a` (k-means del top 30), tinta `--luz #f1e3d8`, acento `--barra #ff3f6c`; un único campo plano `--brasa #e6874c` en Comida. El resto lo ponen las cintas fotografiadas.

**Tipo.** Six Caps solo en titulares de capítulo (2–5 palabras literales, p. ej. "nos gusta el colorssss!" [IG-111]); el logotipo hace de h1 visual; Oswald 300/400 en cuerpo y datos.

**Momento autoral: "el techo se queda".** Al bajar, P189 retrocede, y su franja superior de cintas (22 vh) queda fija como cielo durante El lugar, ≤200 vh. Debajo pasan P093, P039 y P114, cada una con su caption literal. Al terminar el capítulo, el techo se suelta.

**La cosa viva: "¿Con quién viene?".** Cuatro botones [UI] (Solo · En pareja · Con amigos · De cumpleaños) que cambian la foto y la cita literal:

| Botón | Foto | Cita |
|---|---|---|
| Solo | P194 | "una gran barra, larga, de esas para sentarse y quedarse ahí" [VID-061] |
| En pareja | P258 | "Tantos amores como guarisnaques" [IG-032] |
| Con amigos | P259 | "no somos ná sin ustedes!" [IG-026] |
| De cumpleaños | P198 | "El japi berdey más celebrao" [IG-047] |

Sin JS se ven las cuatro apiladas.

**Estructura.** El lugar bajo el techo fijo · Tragos en split (P184 + P297) · Comida en campo brasa con mosaico · Con quién = la cosa viva · Eventos en calendario · Cuándo y dónde con P333 y el letrero V031 chico · Carta propia sobre noche, con pestañas.

**Teléfono.** P189 a sangre en 390×844, con el scrim desde el 45 %. El logotipo va a ~104 px, sobre la bio y los datos. Arriba, "Menú" y [Ver la carta].

**Riesgo honesto.** Es la más de categoría ("foto a sangre + nombre de película" lo hace cualquier bar con terraza). El scrim que pide el logotipo se come las caras, que son la prueba de "lleno" (se ve en el boceto). P189 (1440 px) se ve blanda en 1920. El techo fijo repite el pin de la v1 si se alarga.

**Pecados de la v1 que evita:** material falso (el color es foto), arcoíris CSS, más de un acento; el pin queda en ≤200 vh y siempre con contenido.

---

## 6. Ruta C · La carta de la casa

**Idea.** *"En esta página, la carta oficial de Almud se vuelve el índice del bar entero: cada rincón, trago y plato es una línea."*
Dirección: `page-is-the-object`, donde el objeto es la carta.

```
THESIS: la carta ya es su mejor texto; la web se compone como ella. Rechaza la "carta PDF
        escondida" y el hero de bar: la portada es la tapa de la carta.
OWN-WORLD: hoja blanca #fbfaf7, Six Caps y Oswald en azul carta #2023e4, precios magenta
        #ec008c tabulares, filas nombre…precio, fotos como láminas rectas que tocan el borde.
STORY: lee qué es (bio en Six Caps azul), ve la promo de hoy como una fila con precio, prueba un
        par de nombres de chiste, abre la carta completa.
FIRST VIEWPORT: izquierda, 55 %: logotipo oscuro, "COCTELERÍA DE AUTOR, / COMIDA & MÚSICA
        BONITA" en Six Caps azul de 2 líneas, datos, la fila de HOY con precio, 3 filas de la
        carta, [Ver la carta completa]. Derecha, 45 %: P189 a toda altura, a sangre.
FORM: hoja-carta, 3.º de la lista ordenada, seed: none (unavailable)
FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the
        verdict, DESIGN.md, and every shipping raster carrying its provenance
```

**Color: Committed.** El azul de la carta es dueño del 30–60 % de la tinta sobre la hoja `#fbfaf7`; magenta en precios y acción secundaria; cuerpo `#1b1a2e`; Eventos invertido a noche `#150b12`. Requiere `--allow palette-purple` justificado (es el azul impreso `#2023e4`).

**Tipo.** Six Caps azul para los titulares de capítulo, como los rótulos "COCTELERÍA de la CASA". Oswald 600 para los nombres y precios, y 300/400 para las descripciones.

**Momento autoral: "índice con lámina".** En El lugar, los rincones son filas de carta ("La barrita", "La terraza techada", "El fogón"…) con su caption literal como descripción. Al tocar o pasar el cursor, la foto de esa fila se abre anclada a la fila: clip de 320 ms, y las demás filas bajan a 0,4.

**La cosa viva: "Un coctelito al azar".** Un botón [UI] reparte una de las 14 de la casa, con nombre, descripción y precio literales [CARTA-2]. Sin JS, muestra la primera.

**Estructura.** El lugar como índice · Tragos y Comida en filas con láminas grandes (P297, P086, P036, P305) · Con quién en mosaico · Eventos como página negra (su pizarra) · Cuándo y dónde: fila de datos + P199 · la Carta completa, en su sección, es el clímax.

**Teléfono.** P189 en 390×340, debajo la bio en Six Caps azul a 70 px en 2 líneas, la fila de hoy y el botón.

**Riesgo honesto.** Página blanca leída de noche contradice la escena. "Carta como página" es la herramienta de la categoría. La fiesta queda en la foto y el resto se lee como menú: la más ordenada y la menos "todos los días son una fiesta". El azul ronda el índigo vetado.

**Pecados de la v1 que evita:** color rotado (dos tintas con rol), hairlines (filas por espacio), "platos de color" (sin foto, sin foto).

---

## 7. Lo que comparten las tres
- **Carta completa** en sección propia (Coctelería de la casa, Mocktails, Bebidas y jugos, Comilona), literal y con `tabular-nums`. Horario, Serrano 325, mapa y DM en el primer viewport. Sin hora de cierre, fila ni espera.
- 6–12 fotos que trabajan, 3–5 tratamientos; nada de ≤1440 px a sangre en 1920; P073, P221, P348 solo en Eventos.
- Textos literales con ID de fuente; solo [UI] es nuestro: "Ver la carta", "Cómo llegar", "Escríbanos al DM", "Menú".

## 8. Recomendación: ruta A, El afiche de hoy

**Test del competidor** (cambiar Almud por otro bar de Castro en la frase-idea):
- **B:** "el techo de [otro bar] se vuelve el cielo…". Funciona con cualquier terraza decorada. **Falla.**
- **C:** "la carta de [otro bar] se vuelve el índice…". La forma sirve para cualquier bar; solo el contenido es de Almud. **Pasa a medias.**
- **A:** "cada día se vuelve un afiche de [otro bar]". La frase sola podría prestarse, pero el sistema no:
  - el negro, la condensada y las franjas de Ojo Piojo son *sus* afiches publicados;
  - la semana Mar–Sáb con su promo es *su* carta [CARTA-7];
  - Six Caps viene de *su* letrero.

  Un competidor tendría que inventar todo eso. **Pasa.**

**Por qué A además de eso:** responde en el primer segundo y en tipo grande lo que la v1 dejaba a 10 pantallas ("¿qué hay hoy?"); vuelve "todos los días son una fiesta" un mecanismo (cada día su afiche), no un adjetivo; resuelve el asterisco de P189 sin ampliar (tres tiras de 624 px a resolución nativa); y es la única en que los dueños reconocen su propia gráfica.

**Disciplina que toma de B:** la foto lidera. Cada capítulo tiene una foto que ocupa ≥60 % de su pantalla. Hay una banda a sangre cada 3–4 pantallas (P362 y P039). La terraza llena se ve a su escala real al menos una vez, sin tiras. El negro nunca gana sobre la gente.

**Disciplina que toma de C:** "lo impreso". La sección Carta es la única hoja de papel (`#f6ecdc`) en la página negra, con nombres en Oswald 600 azul `#2023e4`, precios magenta `#ec008c` tabulares, dos columnas y separación por espacio, como su PDF. Así el azul y el magenta de la carta viven solo donde la marca los imprimió.

**Abierto para la fase 8:** contraste de cada franja con su tinta; texto del viernes; que Six Caps aguante "MIÉRCOLES" en 1–2 líneas a 768 px.
