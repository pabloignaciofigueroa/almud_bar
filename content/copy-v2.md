# Guion v2 · Almud Bar: "una noche cualquiera en Almud"

Fase 9. Sitio nuevo; la v1 es solo anti-referencia (`_plan/diag/v1-antireferencia.md`). Este guion manda sobre `content/copy.md` (v1): de la v1 se reusan fuentes, no estructura.
Vinculantes: `_plan/brief-v2.md`, `PRODUCT.md`, `_plan/direccion/contrato.md`, `_plan/direccion/sistema.md`, `_plan/jurado/seleccion.json`, `_plan/jurado/veredicto.md`.

## 0. Cómo leer este guion

**Marcas** (las lee `tools/verify_copy.py`):
- `«…» [FUENTE]`: texto visible **literal** de Almud. Fuentes: `[IG-NNN]` caption (`content/ig_posts.json`) · `[BIO]` bio y destacadas (`content/bio.txt`) · `[VID-061]` subtítulos quemados del video de IG-061 (transcripción en `content/copy.md`) · `[CARTA-n]` PDF n de la carta oficial (`content/carta.json` + `content/carta_raw.txt`) · `[RESEÑA:autor]` (`content/reviews.json`) · `[DATO]` (`content/research_web.md`).
- `{display}` / `{head}` tras la fuente: es titular y se mide con la aritmética de abajo. ` / ` dentro de un titular es **nuestro corte de línea** (`<br>`), no parte del texto.
- `‹…› [UI]`: etiqueta de interfaz nuestra, mínima y neutra.
- `“…” [EN]`: traducción nuestra. El léxico de la casa queda en español, con glosa breve entre corchetes. `“…” [ES]`: glosa nuestra al español de una reseña en otro idioma.
- `…` dentro de un literal: recorte nuestro de una frase de ellos (se verifica cada trozo, en orden).
- Los glifos emoji se quitan de todo texto visible (ver Correcciones mínimas). Nada de fila, esperar mesa ni "que se desocupe": el script lo revisa.

**Inglés.** Por regla de `PRODUCT.md`, el texto de la marca se queda literal en español también en modo EN; la línea `[EN]` aparece debajo como glosa (`lang="en"`, body o small, papel suave sobre noche / tinta del campo sobre campo). **Nunca va en display**, así que la aritmética de titulares solo mide el español. Las etiquetas `[UI]` sí se reemplazan por su `[EN]`.

**Aritmética de dos líneas** (sistema.md §3: Six Caps k = 0,22; caracteres por línea = columna ÷ (0,22 × tamaño)):

| Paso | 390 (columna 358 px) | 1440 (7 columnas, 790 px) | Presupuesto |
|---|---|---|---|
| display | 96 px → 358 ÷ 21,1 = **16,9 → 17 car./línea** (16 holgado) | 210 px → 790 ÷ 46,2 = **17,1 → 17 car./línea** | ≤ 30 car. en 2 líneas |
| head | 56 px → 358 ÷ 12,3 = **29 car./línea** | 98 px → 790 ÷ 21,6 = **36 car./línea** | ≤ 32 car. |

Regla práctica: **cada línea de display ≤ 17 caracteres** en ambos anchos (el cuello es el mismo), total ≤ 30. La capacidad exacta a 390 es 16,9: una línea de 17 se marca "justo" (cabe con el `<br>` puesto y sin `text-wrap: balance`; si en el render se parte, se usa la alternativa). El script calcula cada titular (tabla al final).

**Orden de la página** y campo de cada pantalla (nunca dos campos seguidos):

| # | Sección | Campo (tinta) |
|---|---|---|
| 1 | Nav | noche (papel) |
| 2 | Portada | foto P189 sobre noche |
| 3 | Hoy en Almud | campo del día: Mar coral · Mié turquesa · Jue fucsia · Vie amarillo · Sáb verde · Dom/Lun coral |
| 4 | El lugar | noche (papel) |
| 5 | Los tragos | amarillo (noche) |
| 5b | Sin alcohol (cierre de Los tragos) | noche (papel) |
| 6 | La comida | verde (noche) |
| 6b | La carta: destacados (fase 15) | papel (noche, azul carta, magenta) |
| 7 | El equipo | noche (papel) |
| 8 | Con quién y para qué | fucsia (papel) |
| 9 | Reseñas | noche (papel) |
| 10 | Eventos | coral (noche) |
| 11 | Cuándo y dónde | noche (papel) |
| 12 | Pie | noche (papel) |
| C | La carta completa: página propia `carta/` (fase 15) | papel; cada pestaña con su tinte suave |

Nota de orden: sistema.md §2.3 pone Tragos (amarillo) junto a Comida (verde) y Comida junto a Con quién (fucsia). Para cumplir "nunca dos campos seguidos" se intercalan dos beats sobre noche que el brief ya pide: **Sin alcohol** (cierra Los tragos) y **El equipo** (entre La comida y Con quién: los garzones de la comida llevan al equipo).

---

## 1. Nav

- **Propósito:** llegar a cualquier parte y a la carta desde cualquier pantalla.
- **Campo:** noche, barra plana de 72 px (56 px en teléfono). No va sobre la foto.
- **Logotipo:** ALMUD BAR + isotipo (SVG claro, `brand/almud-horizontal-claro.svg`), enlace al inicio.
- **Enlaces [UI]:** ‹El lugar› [UI] · ‹Tragos› [UI] · ‹Comida› [UI] · ‹Con quién› [UI] · ‹Eventos› [UI]
  - [EN]: “The place” [EN] · “Drinks” [EN] · “Food” [EN] · “Who with” [EN] · “Events” [EN]
- **Botón primario (barra):** ‹Ver la carta› [UI] → `carta/` (la página de la carta, fase 15) · “See the menu” [EN]
- **Teléfono:** ‹Menú› [UI] / “Menu” [EN] abre la hoja (incluye además ‹Cuándo y dónde› [UI] / “When & where” [EN]).
- **Idioma:** ‹ES› [UI] · ‹EN› [UI]

---

## 2. Portada (ruta B: la terraza llena)

- **Propósito:** ver que hoy está lleno y saber en 10 s qué es, cuándo abre y dónde queda.
- **Campo:** foto a sangre sobre noche.
- **Imagen:** **P189** (`assets/raw/ig/DM_Ih5dyVKH_07.jpg`), a 1:1 hasta 1440 px, noche a los lados en pantallas mayores. Techo de cintas ~45 %, caras en el tercio inferior sin nada encima. Scrim radial neutro solo detrás de cada bloque de tipo (escritorio); en teléfono, lineal desde el 40 % inferior, tipo debajo de las caras. Asterisco del veredicto vigente (alternativas: P362 en escritorio; original en alta).
  - Crédito (small, sobre la foto, abajo a la derecha): ‹Foto› [UI] «@estudiouno.prod» [IG-050] · “Photo” [EN]
- **Titular:** el logotipo ALMUD BAR + isotipo (38 % del ancho, a la izquierda, sobre la pared de zinc). No hay titular de texto en display: la marca es el titular.
- **Bajada (lead):** «Coctelería de autor, comida & música bonita desde 2014» [BIO]
  - “Signature cocktails, food & lovely music since 2014” [EN]
- **Datos (body, tabular):** «Abrimos de Mar a Sáb a las 18:00hrs» [BIO] · «Serrano 325, Castro» [BIO]
  - “Open Tue to Sat from 6 pm” [EN] · “Serrano 325, Castro” [EN]
- **CTA:** ‹Cómo llegar› [UI] (botón barra → mapa) · ‹Escríbanos al DM› [UI] (enlace → `https://ig.me/m/almud_bar`)
  - “Get directions” [EN] · “Message us on Instagram” [EN]
- Sin hora de cierre (no existe confirmada).

---

## 3. Hoy en Almud (la cosa viva; momento autoral "la franja se imprime")

- **Propósito:** responder "¿qué hay hoy?" con la promo real del día (zona `America/Santiago`), y volver mecanismo el "todos los días son una fiesta".
- **Rótulo [UI]:** ‹Hoy en Almud› [UI] · “Today at Almud” [EN]
- **Campo:** el del día (tabla). Tinta: noche sobre coral, turquesa, amarillo y verde; papel sobre fucsia. Botón sobre campo: noche con tinta papel.
- **Estructura fija** (sistema.md §7): titular del día (display, 7 col) · ítem (Oswald 600 lead) · precio (Six Caps head, tabular) · horario · nota · una frase literal · botón + enlace · foto del día (5 col, 4:5) · la semana completa (4 col; hoy en 400, el resto en 300). La semana completa es también el estado sin JS.
- **Constantes de la promo:** «$ 4.500» [CARTA-7] · «de 18:00 a 22:00 hrs» [CARTA-7] · «* Siempre sujeto a stock! *» [CARTA-7]
  - “CLP 4,500” [EN] · “6 to 10 pm” [EN] · “* Always subject to stock! *” [EN]
- **CTA:** ‹Ver la carta› [UI] (botón) · ‹Cómo llegar› [UI] (enlace) · [EN] “See the menu” [EN] · “Get directions” [EN]

### 3.1 Martes · campo coral
- **Titular:** «Amamos los / martes» [IG-016] {display}
  - Alt 1: «Negronicito / ito ito» [IG-016] {display}
  - Alt 2: «Por más negronis / siempre» [IG-016] {display}
  - “We love Tuesdays” [EN]
- **Ítem:** «Negroni & Fernet c/Coca Cola» [CARTA-7] · “Negroni & Fernet with Coca-Cola” [EN]
- **Frase:** «aguante este clásico infalible, maravilloso, delichus, contundente, elegante, finoli» [IG-016]
  - “long live this classic: unfailing, marvellous, delichus [delicious], bold, elegant, finoli [posh]” [EN]
- **Foto:** V054 (`DZ8c3yiIdpa_00.mp4`, piel de naranja sobre negroni, 3,3 s, loop; póster `DZ8c3yiIdpa_00.jpg`, 721 px: va a 5 col sin ampliar). Fuera de los 31 del jurado: revisar. Respaldo: P184.

### 3.2 Miércoles · campo turquesa
- **Titular:** «Miércoles de / piscoleinnnn!» [IG-019] {display}
  - Alt 1: «Mitad de / semana» [IG-019] {display}
  - Alt 2: «combinaitos / itos itos!!!» [IG-019] {display}
  - “Piscolein [pisco & cola] Wednesday!” [EN]
- **Ítem:** «Piscolein & Gin Tonic» [CARTA-7] · “Piscolein [pisco & cola] & Gin Tonic” [EN]
- **Frase:** «Mitad de semana, y es justo y necesario salir a tomar aire y muchos combinaitos itos itos!!!» [IG-019]
  - “Midweek: it's only right to get some fresh air and lots of little mixed drinks!!!” [EN]
- **Foto:** P331 (`DZap3klI-um_00.jpg`, la foto de IG-019: garzona con jockey ALMUD y bandeja, 3072 px). Fuera de los 31: revisar.

### 3.3 Jueves · campo fucsia
- **Titular:** «Jueves de / Sangría!» [IG-039] {display}
  - Alt 1: «está que arden / las sangrías» [IG-098] {display}
  - Alt 2: «Sangriita rica / delichussss!» [IG-074] {display}
  - “Sangría Thursday!” [EN]
- **Ítem:** «Sangría de la casa» [CARTA-7] · “House sangría” [EN]
- **Frase:** «Además que con estos días, la hidrateichon es justa y muy necesaria!» [IG-039]
  - “Besides, in weather like this, hydreichon [hydration] is fair and very necessary!” [EN]
- **Foto:** P228 (`DRkwz2OlC01_00.jpg`, la foto de IG-039: copa tallada con trago morado y canela, 1440 px). Fuera de los 31: revisar.

### 3.4 Viernes · campo amarillo (sin promo)
- **Titular:** «Viernes ya!» [IG-003] {display}
  - Alt 1: «Es viernes!» [IG-042] {display}
  - Alt 2: «Ya es / viernes!!!» [IG-073] {display}
  - “Friday at last!” [EN]
- **Ítem (en lugar de la promo):** «Venga venga que nadie le detenga!» [IG-003] · “Come on, come on, let nobody stop you!” [EN]
- **Frase:** «Le esperamos con cantidá de cosas ricas ricas pal buche y pa empinar ese codo regalón» [IG-003]
  - “We're expecting you with loads of tasty things for the belly and for bending that elbow [having a drink]” [EN]
- Sin precio, sin horario de promo, sin nota de stock.
- **Foto:** P386 (`DeAdh-JFOsY_00.jpg`, la de IG-003: mesa con pizza y tragos, 1280 px). Fuera de los 31: revisar. Respaldo: P031.

### 3.5 Sábado · campo verde
- **Titular:** «Último día / de la semana» [IG-020] {display}
  - Alt 1: «pa que venga a / guarisnaquearse!» [IG-023] {display} (31 car.: pasa por línea, se pasa 1 del presupuesto)
  - Alt 2: «Mejor / empinarsss!» [IG-023] {display}
  - “Last day of the week” [EN]
- **Ítem:** «Ramón a $ 4.500!» [CARTA-7] (el precio va dentro del ítem; no se repite «$ 4.500») · “Ramón [house cocktail] for CLP 4,500!” [EN]
- **Frase:** «Es una precisa mezcla: gin, licor marrasquino, limón y romero.» [CARTA-2]
  - “A precise mix: gin, maraschino liqueur, lemon and rosemary.” [EN]
- **Foto:** V051 (`DZQtKNMo1Bk_00.mp4`, la de IG-020: paneo por el muro de botellas rosa con el letrero, 7 s; póster 1215 px). Fuera de los 31: revisar. Respaldo: P194.

### 3.6 Domingo y lunes (cerrado) · campo coral
- **Titular:** «Abrimos de / Mar a Sáb» [BIO] {display}
  - Alt 1: «Amamos los / martes» [IG-016] {display}
  - “We open Tuesday to Saturday” [EN]
- **Dato:** «Abrimos de Mar a Sáb a las 18:00hrs» [BIO] · “Open Tue to Sat from 6 pm” [EN]
- Debajo, la promo del martes (3.1) con su rótulo: ‹El martes› [UI] · “On Tuesday” [EN]
- **Foto:** la del martes.

### 3.7 La semana (siempre visible)
- **Encabezado de la lista (small):** «siempre es un güen día pa compartir algo rico» [IG-013]
  - “every day is a good day to share something tasty” [EN]
- Filas (día + ítem): «Martes» [CARTA-7] «Negroni & Fernet c/Coca Cola» [CARTA-7] · «Miércoles» [CARTA-7] «Piscolein & Gin Tonic» [CARTA-7] · «Jueves» [CARTA-7] «Sangría de la casa» [CARTA-7] · «Sábado» [CARTA-7] «Ramón a $ 4.500!» [CARTA-7]
  - [EN] “Tuesday” [EN] · “Wednesday” [EN] · “Thursday” [EN] · “Saturday” [EN] (los ítems se glosan como arriba)
- El viernes no aparece en la lista de promos (no tiene). Hoy se marca con peso 400 y ‹Hoy› [UI] / “Today” [EN].

---

## 4. El lugar (noche)

- **Propósito:** recorrer los espacios que pidió el cliente (barra, salón, sillones, terraza techada, terraza abierta, cuadros) como una noche llena, sin nombrar eventos.
- **Campo:** noche; el color lo ponen las cintas fotografiadas.
- **Titular:** «nos gusta el / colorssss!» [IG-111] {display}
  - Alt 1: «Lo más güeno / qué hay» [IG-160] {display}
  - Alt 2: «Venga pa / la selfie» [IG-111] {display}
  - “we love colourrrs!” [EN]
- **Cuerpo:** «Somos inquietos y nos gusta el colorssss! Tratando siempre de hacer nuestro Almudcito beio para su deleite» [IG-111]
  - “We're restless and we love colourrrs! Always trying to make our Almudcito [our little Almud] lovely for your delight” [EN]
- **Cuerpo 2 (small, la idea de origen):** «Un lugar que fuera cálido, acogedor» [VID-061]
  - “A place that would be warm and welcoming” [EN]
- **Imágenes:** foto líder **P093** (barra curva, 5+ col, 4:5) + mosaico desigual de 3 a 4 col (desfases 0/160/56): **P090**, **P039**, **P114**. Después, los espacios en filas de dos. Loop V009 (techo de flecos, IG-111, 7 s) junto a la terraza techada.

### 4.1 La barra
- Rótulo: ‹La barra› [UI] · “The bar” [EN]
- «Pucha que nos gusta nuestra barrita!!» [IG-087] · “Gosh, we love our little bar!!” [EN]
- «y una gran barra, larga, de esas para sentarse y quedarse ahí» [VID-061] · “and a great long bar, the kind you sit at and stay” [EN]
- Imágenes: **P093** (`DAMHps8JVVr_07.jpg`, barra curva completa) y **V014-cover** (`C9BDvFvJk4z_00.jpg`, lámpara de pinzas; el video V014 como loop opcional).
  - Crédito V014: ‹Video› [UI] «@rober.patagonico» [IG-103] · “Video” [EN]. P093 sin crédito en su caption (IG-079): no se acredita.

### 4.2 El salón y las mesas
- Rótulo: ‹El salón› [UI] · “The room” [EN]
- «Se deslizan como angelitos, con trago en mano por los salones» [IG-067] · “They glide like little angels, drink in hand, through the rooms” [EN]
- Imagen: **P339** (`Dbg3ekilC4P_02.jpg`, mujeres bajo lámpara de mimbre, muro rojo; 3072 px, puede ir a sangre).
  - Crédito: ‹Foto› [UI] «@isosur.prod» [IG-009]

### 4.3 El rincón de los sillones
- Rótulo: ‹Los sillones› [UI] · “The sofas” [EN]
- **No existe** una línea literal de Almud sobre los sillones (búsqueda "sill/sofá/cojín/rincón" en las 180 captions: 0). Más cercana, de la caption de la misma foto (IG-075):
  - «pa compartir, pa escuchar güena música, pa ponerle algo delichus al buche» [IG-075] · “to share, to listen to good music, to put something delichus [delicious] in the belly” [EN]
  - Opción en voz de reseña (atribuida): «comfy seats» [RESEÑA:Benjamín]
- Imagen: **P114** (`DBMtYELSzNS_14.jpg`, mujer riendo en el sillón de cojines estampados). Crédito: ‹Foto› [UI] «@estudiouno.prod» [IG-075]

### 4.4 La terraza techada
- Rótulo: ‹La terraza techada› [UI] · “The covered terrace” [EN]
- «Techamos parte de la terraza, le pusimos todo el colors y calor del mundo mundial» [IG-004]
  - “We roofed part of the terrace and gave it all the colours and warmth in the whole wide world” [EN]
- «sin mojarse y calentit@, qué mejor?!» [IG-004] · “without getting wet and nice and warm, what could be better?!” [EN]
- Imágenes: **P090** (`DAMHps8JVVr_04.jpg`, faroles y flecos sobre la gente) + loop **V009** (`C5WAi8PLHni_00.mp4`). La portada (P189) ya es esta terraza llena.

### 4.5 La terraza abierta
- Rótulo: ‹La terraza› [UI] · “The open terrace” [EN]
- «Tardes y nochecitas de terraza! Lo más güeno qué hay» [IG-160] · “Terrace afternoons and evenings! The best there is” [EN]
- «Amamos los atardeceres desde nuestra terracita ita ita!» [IG-163] · “We love the sunsets from our little terrace!” [EN]
- Imagen: **P039** (`Cqn78DFp5Nm_00.jpg`, patio descubierto de noche: guirnaldas, árboles, mesas llenas). Crédito: ‹Foto› [UI] «@catarsis.fotografia» [IG-144]

### 4.6 Los cuadros y el mural
- Rótulo: ‹El mural› [UI] · “The mural” [EN]
- «Dicen que una mirada vale más que mil palabras…» [IG-118] · “They say a look is worth more than a thousand words…” [EN]
- «OJO PIOJO es un proyecto hecho con mucho amor, paciencia y tiempo» [IG-118] · “OJO PIOJO [‘eyes peeled’] is a project made with a lot of love, patience and time” [EN]
- Crédito: «Proyecto @cepaz» [IG-118] · “Project by @cepaz” [EN]
- Imagen: fotograma **F:V031_mural-ojos_6.60s** (`_plan/diag/frames/V031_mural-ojos_6.60s.jpg`); no hay foto fija nítida de la pared de cuadros (hueco declarado). Crédito del video: ‹Video› [UI] «@estudiouno.prod» [IG-061]
- OJO PIOJO es una obra del espacio, no un evento: puede nombrarse aquí.

### 4.7 Las luces (cierre del capítulo)
- «Nos gustan los brillitos, las luces» [IG-147] · “We like sparkles and lights” [EN]
- Enlace: ‹Cómo llegar› [UI] · “Get directions” [EN]

---

## 5. Los tragos (amarillo)

- **Propósito:** creer en la coctelería de autor por sus nombres, su gente y sus fotos; abrir la carta.
- **Campo:** amarillo, tinta noche.
- **Titular:** «mejor los / tomamos todos!» [IG-046] {display}
  - Alt 1: «Tantos / coctelcitos» [IG-046] {display}
  - Alt 2: «Etiquetas pa / regodearse!» [IG-020] {display}
  - “best to drink them all!” [EN]
- **Cuerpo:** «Tantos coctelcitos entre los cuales decidirse! Demasiada complikeichon elegir, mejor los tomamos todos!» [IG-046]
  - “So many little cocktails to choose from! Too much complikeichon [complication] choosing, best to drink them all!” [EN]
- **Cuerpo 2 (de autor):** «Tantos creadores con tantísimo talento e innumerables horas de probar, probar y probar» [IG-021]
  - “So many creators with so much talent and countless hours of tasting, tasting and tasting” [EN]
- **Cuerpo 3 (la barra):** «En esta barrita pasan tantas maravillas en forma de coctelcitos» [IG-045]
  - “So many wonders happen at this little bar, in the shape of little cocktails” [EN]
- **Rótulo del grupo:** «Coctelería de la casa» [CARTA-2] · “House cocktails” [EN]
- **Fase 15:** la lista de cuatro tragos sale del capítulo (el cliente pidió la carta fuera del landing; los tragos con foto van en §6b). Quedan el rótulo y el botón ‹Ver la carta› [UI] → `carta/#casa`. Lo que sigue queda como registro de la versión anterior.
- **Cuatro de la casa** (versión anterior; nombre y precio de `carta.json › coctel`; una línea literal cada uno):
  - «Aquí te las traigo Peter» [CARTA-2] $ 6.700 · «Hermoso y ricardo» [IG-044] · “Gorgeous and ricardo [yummy]” [EN]
  - «Cómo te voy a olvidar» [CARTA-2] $ 6.800 · «este cóctel que está 10/10» [IG-002] · “this cocktail that's a 10/10” [EN]
  - «Sagüer on Faia» [CARTA-2] $ 7.900 · «es como un sour, pero acanelado y medio picantito» [IG-063] · “it's like a sour, but cinnamony and a bit spicy” [EN]
  - «A veces me pongo Coquette» [CARTA-2] $ 7.100 · «una delicia rosada, cremosa y dulzona!» [CARTA-2] · “a pink, creamy, sweet delight!” [EN]
  - Los nombres no se traducen (son juegos de palabras); en EN se glosan entre corchetes en small solo si hace falta: “[I'll bring them to you, Peter]” [EN], “[How could I forget you]” [EN], “[Sour on fire]” [EN], “[Sometimes I get coquettish]” [EN].
- **CTA:** ‹Ver la carta› [UI] (botón noche) · “See the menu” [EN]
- **Imágenes:** foto líder **P297** (`DYsZ0GNo_88_00.jpg`, splash rojo en coupe, 3177 px, "marco que crece"); mosaico 4:5 **P086** (tres sours con flores), **P184** (bartender frente al muro rosa), **P097** (copa tallada naranja); banda a sangre **P362** (`Dbok2NyFNdb_05.jpg`, 3072 px, bartender y letrero ALMUD). Loop opcional V021 (muro rosa) si no va en la carta.
  - Créditos: P184 ‹Foto› [UI] «@estudiouno.prod» [IG-050]. P297, P086, P097 y P362: sus captions no acreditan (P362 es del 12.º aniversario, cuyas fotos acredita IG-009 a @isosur.prod: **por confirmar**, no se publica sin confirmar).

### 5b. Sin alcohol (noche, cierre de Los tragos)
- **Propósito:** que nadie quede fuera; mocktails, jugos y bebidas.
- **Campo:** noche (separa amarillo de verde).
- **Titular (head):** «no dejamos a nadie ajuera» [IG-011] {head}
  - Alt 1: «tenemos pa todos los gustos!» [IG-011] {head}
  - “we leave nobody out” [EN]
- **Cuerpo:** «un manjar pa los menores de edá, embarazás, abstemi@s» [IG-011]
  - “a treat for minors, pregnant folks, teetotallers” [EN]
- **Cuerpo 2:** «Y si usted es sobri@ y alocad@ tenemos unos mocktail que están de pelos!» [IG-141]
  - “And if you're sober and up for fun, we've got mocktails that are just great!” [EN]
- **Fase 15:** el destacado pasa a §6b (con su foto). Los cuatro rótulos enlazan a su grupo en `carta/` (`#sin-alcohol-mocktails`, `-jugos`, `-cervezas`, `-calientes`) y el botón a `carta/#sin-alcohol`.
- **Destacado (versión anterior):** «La moto chantá» [CARTA-5] $ 6.400 · «Juguito de mango y maracuyá, pepino, jarabe simple, limón y bitter pepino!» [CARTA-5]
  - “[‘The stalled motorbike’] Mango and passion-fruit juice, cucumber, simple syrup, lemon and cucumber bitters!” [EN]
- **Rótulos de la carta que se enlazan:** «Coctelcitos sin alcohol» [CARTA-5] · «Jugos & bebidas» [CARTA-5] · «Cervezas sin alcohol» [CARTA-5] · «Bebidas calientes» [CARTA-5]
  - “Alcohol-free cocktails” [EN] · “Juices & soft drinks” [EN] · “Alcohol-free beers” [EN] · “Hot drinks” [EN]
- **Imagen:** no hay foto de mocktail (hueco declarado; no se fabrica). Sin foto, o P031 como la más cercana si el diseño la pide (ya usada en Con quién: preferir sin foto).
- **CTA:** ‹Ver la carta› [UI] · “See the menu” [EN]

---

## 6. La comida (verde)

- **Propósito:** la cocina como protagonista, con sus platos por nombre.
- **Campo:** verde, tinta noche.
- **Titular:** «pa chuparse / el bigoteli» [IG-139] {display}
  - Alt 1: «Puro / manjarshhhh» [IG-022] {display}
  - Alt 2: «comilona / ona ona!» [IG-092] {display}
  - “to lick your bigoteli [little moustache]: finger-licking good” [EN]
- **Cuerpo:** «Mire que tenemos una cocina sencilla pero más que sabrosona!» [IG-022]
  - “Look, our kitchen is simple but more than tasty!” [EN]
- **Cuerpo 2:** «Nos gustan los brillitos, las luces, los coctelcitos y la comida que deja el ombligo pa ajuera!» [IG-147]
  - (si 4.7 ya usa la primera mitad, aquí va solo: «la comida que deja el ombligo pa ajuera!» [IG-147] · “food that leaves your belly button sticking out!” [EN])
- **Rótulos (categorías):** «Picoteos» [CARTA-1] · «Greditas» [CARTA-1] · «Sanguches» [CARTA-1] · «Pizzas artesanales» [CARTA-1] · «Pa los chichichos» [CARTA-1] · «Somos dulzones» [CARTA-1]
  - “Small plates” [EN] · “Greditas [clay-pot dishes]” [EN] · “Sandwiches” [EN] · “Artisan pizzas” [EN] · “For the little ones” [EN] · “Sweet tooth” [EN]
- **Fase 15:** los cuatro platos salen del capítulo (van con foto en §6b). Las seis categorías enlazan a su grupo en `carta/` (`#comilona-picoteos` … `#comilona-dulzones`) y ‹Ver la comilona› [UI] a `carta/#comilona`.
- **Cuatro platos** (versión anterior; nombre y precio de `carta.json › comilona`; una línea literal):
  - «Tukulito Sakayama» [CARTA-1] $ 15.900 · «pa usté solit@ o pa compartir!» [IG-139] · “for you alone or to share!” [EN] (si se usa en Con quién, aquí: «Tataki de lomo de atún marinado» [CARTA-1] · “Marinated tuna loin tataki” [EN])
  - «Con tuti si no pa qué!» [CARTA-1] $ 19.900 · «Especial pa compartir» [CARTA-1] · “[‘All in, or why bother!’] Made for sharing” [EN]
  - «Camarón que se duerme» [CARTA-1] $ 15.900 · «Calentitas, contundentes, enjundiosas: otsea, 10 de 10.» [IG-018] · “[Gredita] Hot, hearty, full of substance: I mean, 10 out of 10.” [EN]
  - «Topiturrón» [CARTA-1] $ 6.900 · «turrón de chocolate con galletas y nueces, gel de mango y maracuyá» [IG-040] · “chocolate nougat with biscuits and walnuts, mango and passion-fruit gel” [EN]
- **Pizzas (una línea):** «Si le gustan las pizzas con masa delgadita y con una propuesta choriflai de mezclas» [IG-141]
  - “If you like thin-crust pizzas with choriflai [cool] combinations” [EN]
- **CTA:** ‹Ver la comilona› [UI] → `carta/#comilona` · “See the food menu” [EN]
- **Imágenes:** foto líder **P036** (`CqEI2nSJP2__00.jpg`, garzona con pizza); mosaico **P305** (hamburguesa, alta res), **P091** (cazuela de ñoquis), **P393** (`DeNQ8A2lDgg_02.jpg`, garzón tatuado con plato; 3000 px, puede ir a sangre).
  - Créditos: P036 ‹Foto› [UI] «@catarsis.fotografia» [IG-147]. P305 (IG-022), P091 (IG-079) y P393 (IG-001) sin crédito en caption.

---

## 6b. La carta: destacados (papel; fase 15)

- **Propósito:** el cliente pidió sacar la carta completa del landing. Aquí quedan solo los productos con su mejor foto real (la foto es de ese ítem: caption que lo nombra o `carta.json › img`), con nombre, descripción y precio literales de `content/carta-v2.json`, y un botón claro a la página de la carta.
- **Campo:** papel (entre La comida, verde, y El equipo, noche). Nombres azul carta en MAYÚSCULAS, precio magenta.
- **Título:** ‹La carta› [UI] · “The menu” [EN] · **Bajada:** «En su Almudcito tenemos pa todos los gustos!» [IG-011] · “At your Almudcito [our little Almud] we've got something for every taste!” [EN]
- **Grupos** (rótulo literal, enlazado a su pestaña):
  - «Coctelería de la casa» [CARTA-2] · “House cocktails” [EN] → `carta/#casa`
    - «Aquí te las traigo Peter» [CARTA-2] $ 6.700 · «Este es tan lindo! Le lleva: Mistral Nobel Cristalino, licor de flor de saúco, cranberry, limoncito y un toque dulce de jarabe. Pero lejos lo más bacán es la burbuja que viene aquí!» [CARTA-2] · foto V038 (IG-044)
    - «Sagüer on Faia» [CARTA-2] $ 7.900 · «Este es un sour bien especial: va con Mistral Nobel Fire, limón y jarabe que complementa este cóctel especiado, medio picantito y muy rico!!!» [CARTA-2] · foto V030 (IG-063)
    - «Sangría Foreva!» [CARTA-2] $ 6.500 · «Esta versión te dejará como perro con dos colas! Vino Carménère, toda la malicia del pisco añejado, jarabe de canela, unos toques frutales infaltables y mucho amor» [CARTA-2] · foto P228 (IG-039)
  - «Mocktails de la casa» [CARTA-5] · “House mocktails” [EN] → `carta/#sin-alcohol-mocktails`
    - «La moto chantá» [CARTA-5] $ 6.400 · «Juguito de mango y maracuyá, pepino, jarabe simple, limón y bitter pepino! [El vasito va con crusta de sal]» [CARTA-5] · foto P336 (IG-011)
  - «Comilona» [CARTA-1] · “Comilona [food]” [EN] → `carta/#comilona`
    - «Tukulito Sakayama» [CARTA-1] $ 15.900 · «Tataki de lomo de atún marinado pa chuparse el bigoteli. Acompañado de pancito y salsa de la casa.» [CARTA-1] · foto P044 (IG-139)
    - «Camarón que se duerme» [CARTA-1] $ 15.900 · «Delichus mix: camarones, mezclado con queso crema, cebollín, cilantro, champiñones, jengibre desglasado con vino blanco» [CARTA-1] · foto P099 (IG-077)
    - «Pizza dulzona» [CARTA-1] $ 12.500 · «Ideal para compartir! Es una pizza, pero dulce, está super delichus! Pasta de avellana, crema, frutos rojos glaseados, almendras fileteadas y hojitas de menta.» [CARTA-1] · foto P310 (IG-022, sin nombre en la caption: es la única pizza dulce de la carta y se ve su descripción)
  - Fuera de los destacados, aunque tienen foto: Cómo te voy a olvidar (foto de día, 720 px), Coquette (desenfocada), Con tuti (la foto es anterior a la «[Versión 2.0]» y lleva jamón, que la versión actual no menciona) y Topiturrón (la foto es la versión con gel de mango y maracuyá; la carta actual es «[Reloaded]»). Siguen con su foto en `carta/`.
- **CTA:** ‹Ver la carta completa› [UI] (botón azul carta → `carta/`) · “See the full menu” [EN] · ‹Precios de la carta oficial, octubre 2026.› [UI]

---

## 7. El equipo (noche)

- **Propósito:** prueba sin adjetivos: la gente con nombre propio (solo equipo confirmado 2025–26, veredicto).
- **Campo:** noche.
- **Titular:** «Peazo de equipo / que tenemos!» [IG-048] {display}
  - Alt 1: «qué pedazo de / team tenemos!» [IG-010] {display}
  - Alt 2: «Somos una banda / variada» [IG-067] {display}
  - “What a team we've got!” [EN]
- **Cuerpo:** «Est@s guapetones son parte de nuestro equipo, son los encargados de barra y salón» [IG-001]
  - “These good-lookers are part of our team, in charge of the bar and the room” [EN]
- **Cuerpo 2:** «le ponen una sonrisota con cada cóctecito ito ito, comida delichus y la atención más güena!» [IG-001]
  - “they bring a big smile with every little cocktail, delichus [delicious] food and the best service!” [EN]
- **Nombres** (solo los @, tal como los da la lista más reciente, IG-010, jul-2026):
  - «@pablete_bartender_ @javier.agmc @lizzearellano @milagroosjm @eduu.ardoo @elymar_bocarejo @jaav11 @daweed.cagliano @haqum.v99» [IG-010]
- **Los dueños:** «los papis del almud: el franchuto @rusio_mezclao y la disharashera @cepaz» [IG-067]
  - “the Almud parents: the Frenchie @rusio_mezclao and the disharashera [a play on ‘dicharachera’, chatty] @cepaz” [EN]
  - Confirmados 2025 en IG-048. No se rotula a nadie como dueño en ninguna foto.
- **Pie de la foto P333:** «Nuestras chicas super poderosas, super bacanas y super hermosas!» [IG-014] · «@milagroosjm y @lizzearellanol» [IG-014]
  - “Our super-powered, super-cool, super-beautiful girls!” [EN]
- **Imágenes:** **P333** (`DaWM8rlo1FR_00.jpg`, dos garzonas con corbata y jockey, 3219 px; es la foto de IG-014 y puede ir a sangre). Sin crédito en su caption. Va aquí y no en Cuándo y dónde (P199 queda allá).
- No se nombra a nadie de antes de 2025 ni a terceros (P027, despedida de @vlanbartender, fuera).

---

## 8. Con quién y para qué (fucsia)

- **Propósito:** cualquier compañía, cualquier ocasión; solo líneas literales.
- **Campo:** fucsia, tinta papel. Fotos con poco rojo.
- **Titular:** «no somos ná / sin ustedes!» [IG-026] {display}
  - Alt 1: «Venga a celebrar / la vida» [IG-142] {display}
  - Alt 2: «esta vida es / una sola!» [IG-157] {display}
  - “we're nothing without you!” [EN]
- **Cuerpo:** «Pa agarrar perso, pa pasar las penas, las alegrías, celebreichons, pa entrar en calor, pa refrescarse» [IG-060]
  - “To work up the nerve, to get over sorrows, for joys, for celebreichons [celebrations], to warm up, to cool down” [EN]
- **Ocasiones** (rótulo [UI] + línea literal + foto):

| Rótulo [UI] | [EN] | Línea literal | [EN] | Foto |
|---|---|---|---|---|
| ‹Solo› [UI] | “On your own” [EN] | «pa usté solit@ o pa compartir!» [IG-139] | “for you alone or to share!” [EN] | **P194** (acodados en la barra) |
| ‹En pareja› [UI] | “As a couple” [EN] | «celebremos el amor en todas sus formas, con las piernas, amiguis, hij@s, como usté quiera!» [IG-060] | “let's celebrate love in all its forms: with your piernas [other half], amiguis [friends], kids, however you like!” [EN] | **P258** (pareja frente a la barra) |
| ‹Con amigos› [UI] | “With friends” [EN] | «celebrar la vida, la amistad, el amors y el buen clima» [IG-065] | “celebrate life, friendship, love and good weather” [EN] | **P259** (tres amigos) · **P254** (brindis frente al muro rosa) |
| ‹A celebrar› [UI] | “To celebrate” [EN] | «A celebrar se ha dicho!» [IG-015] | “Let's celebrate, it's decided!” [EN] | **P198** (brindis eufórico) |
| ‹Sin motivo› [UI] | “For no reason” [EN] | «porque usté se lo merece y punto!» [IG-150] | “because you deserve it, full stop!” [EN] | **P041** (risa frente a las cintas) · **P031** (brindis en la barra) |

- **Huecos declarados:**
  - **Solo:** no hay una línea que diga "venga solo". La más cercana es «pa usté solit@ o pa compartir!» (IG-139, dicha de un plato). Otra: «ideal pa venir a bien-tratarse a la terracita o a la barra» [IG-162] · “ideal for coming to treat yourself well on the terrace or at the bar” [EN].
  - **Cumpleaños de un cliente:** no existe línea ni foto (todos los "japi berdey" son del bar). Se propone la ocasión genérica «A celebrar se ha dicho!» (IG-015) con P198. Otra: «celebreichons» dentro del cuerpo (IG-060).
  - **En pareja:** la línea viene del post del 14F (IG-060), pero el recorte no nombra el evento.
- **Personas:** P254 son @milagroosjm y @lizzearellano (equipo, IG-031): aquí van sin nombre ni pie que las haga pasar por clientas. P258 y P259 tienen flash: van juntas en su propio grupo del mosaico (regla de luz del jurado).
- **CTA:** ‹Cómo llegar› [UI] (botón noche) · “Get directions” [EN]

---

## 9. Reseñas (noche)

- **Propósito:** lo dicen otros, en su idioma; cero adjetivos nuestros.
- **Campo:** noche.
- **Titular:** «lo rico de / nuestro barsucho» [IG-088] {display}
  - Alt 1: «Que no se lo / cuenten!» [IG-032] {display} (si se usa, el pie cambia su firma a la de IG-001)
  - Alt 2: «Ya sabe ya» [IG-088] {display}
  - “how good our little bar is” [EN]
- **Cifras [DATO]** (small, tabular): ‹Google› [UI] «4,6» [DATO] · «848 reseñas» [DATO] — ‹Tripadvisor› [UI] «4,6» [DATO] · «209» [DATO] ‹reseñas› [UI] · ‹#1 de 6 bares en Castro› [UI] (de "#1 of 6 'Bares y pubs' in Castro" [DATO])
  - “Google 4.6 · 848 reviews — Tripadvisor 4.6 · 209 reviews · #1 of 6 bars in Castro” [EN]
  - Fecha de las cifras: ‹oct-2026› [UI].
- **Seis reseñas**, idioma original, con autor, fuente y fecha (de `reviews.json`). Ninguna habla de esperas:
  1. «What really sets Almud apart is that the food isn't an afterthought – it's fantastic.» [RESEÑA:Holger K] · Holger K · Google · 2025-12 · `lang="en"`
     - Glosa en modo ES (nuestra): “Lo que de verdad distingue a Almud es que la comida no es un detalle de último momento: es fantástica.” [ES]. En modo EN no lleva glosa.
  2. «Ahora entiendo porque se habla tanto del lugar. Lindo, rapido, rico, céntrico y económico. Super sugerido» [RESEÑA:Kevin B] · Kevin B · Google · 2026-02 · `lang="es"`
     - “Now I understand why people talk about this place so much. Lovely, quick, tasty, central and affordable. Highly recommended” [EN]
  3. «The bar tenders are artists, sit on the bar and watch.» [RESEÑA:Ai T] · Ai T · Google · 2024-01 · `lang="en"`
     - Glosa en modo ES (nuestra): “Los bartenders son artistas: siéntese en la barra y mire.” [ES]. En modo EN no lleva glosa.
  4. «su terraza permite con sol o lluvia una tremenda vista» [RESEÑA:Visitante] · Google · 2026-04 · `lang="es"`
     - “its terrace gives a tremendous view, sun or rain” [EN]
  5. «Super soirée à Castro ! Le service est sympa, super ambiance, avec musique très sympa!» [RESEÑA:Dorothee M] · Dorothee M, Épinal · Tripadvisor · 2016-12 · `lang="fr"`
     - “Great night out in Castro! Friendly service, great atmosphere, with really nice music!” [EN] · glosa en modo ES (nuestra): “¡Gran noche en Castro! Atención simpática, gran ambiente, con música muy simpática.” [ES]
  6. «Estuve ahí cada día de mi estancia, porque es imposible no volver.» [RESEÑA:arqggodoy] · arqggodoy, Iquique · Tripadvisor · 2016-11 · `lang="es"`
     - “I was there every day of my stay, because it's impossible not to go back.” [EN]
- La reseña 4 es un recorte de la de "Visitante" (se omite "Ricos tragos y tablitas…" y el emoji final). La 5 corta antes de "… Les cocktails sont à tomber".
- **Formato:** 3 + 3 en escritorio (sin carrusel cortado en el borde); en teléfono, pila de 3 con ‹Ver más reseñas› [UI] / “More reviews” [EN] que despliega las otras 3.
- **Imagen:** ninguna (la sección es tipo).

---

## 10. Eventos (coral; calendario)

- **Propósito:** los eventos de escala de ciudad, con su nombre (el único lugar donde aparecen) y el mes en que vuelven. Tamaño normal, nada de capítulo gigante.
- **Campo:** coral, tinta noche. Aquí se permiten la luz violeta y los disfraces.
- **Titular:** «tirar la casa / por la ventana!» [IG-010] {display}
  - Alt 1: «Vamos por / más!» [IG-041] {display}
  - Alt 2: «tirar el bar / por la ventana» [IG-081] {display}
  - “to throw the house out the window [to go all out]!” [EN]
- **Cuerpo:** «Nos vemos en las próximas cositas que se vienennnn bomba» [IG-010]
  - “See you at the next little things coming up, they'll be a blast” [EN]
- **Calendario** (mes [UI] · nombre literal · una línea literal · años en que pasó, de las captions):

| Mes [UI] | [EN] | Nombre | Línea | [EN] | Años | Foto |
|---|---|---|---|---|---|---|
| ‹Febrero› [UI] | “February” [EN] | «14F» [IG-116] | «Amamos el 14F pa brindar en honor al amor!» [IG-116] | “We love 14F [Valentine's Day] to raise a glass to love!” [EN] | 2024 · 2025 · 2026 | — |
| ‹Marzo› [UI] | “March” [EN] | «chaolin bombín al verano» [IG-030] | «Y se nos van los mesesitos queridos de verano y vakeichons… y hay que despedirlos como corresponde» [IG-114] | “Our dear summer months and vakeichons [holidays] are leaving us… and they must be sent off properly” [EN] | 2024 · 2026 | — |
| ‹Julio› [UI] | “July” [EN] | «nuestro mes de aniversario» [IG-098] | «Cuánto coctelcito ha pasado bajo este puente» [IG-010] | “So many little cocktails under this bridge” [EN] | 2023 (9) · 2024 (10) · 2025 (11) · 2026 (12) | **P073** (el "10" de flores, 2024) · **P221** (torta, 2025) · **P348** (12 años, 2026, a sangre) |
| ‹Julio› [UI] | “July” [EN] | «Tiki Night» [BIO] | «con todo el sabor tiki!» [IG-053] | “with all the tiki flavour!” [EN] | 2025 (dentro de los 11 años) | — |
| ‹Septiembre› [UI] | “September” [EN] | «fondita ita ita» [IG-081] | «Nos endieciochamos contra viento y marea» [IG-043] | “We go full dieciocho [Chile's national holidays] come wind or high water” [EN] | 2023 · 2024 · 2025 · 2026 | — |
| ‹Septiembre› [UI] | “September” [EN] | «negroni week» [IG-005] | «esperada por much@s ya está aquí» [IG-005] | “awaited by many, it's here” [EN] | 2025 · 2026 | — |
| ‹Octubre› [UI] | “October” [EN] | «Bendita Primavera» [IG-076] | «nuestro día de bienvenida a la esperada primavera!» [IG-075] | “our day to welcome the long-awaited spring!” [EN] | 2024 | — |
| ‹Octubre› [UI] | “October” [EN] | «Jalogüín» [IG-071] | «traguitos y travesuras 1313» [IG-124] | “little drinks and mischief, hee hee [1313]” [EN] | 2023 · 2024 · 2025 | **P229** (disfraces frente a la barra rosa, 2025; fuera de los 31, permitido solo aquí) |

- **Notas del calendario:**
  - "Años" se toma de las fechas de las captions (`ig_posts.json`), no de una agenda. **No se anuncia fecha futura** (no la hay publicada).
  - Marzo 2026 fue en el patio de Rucalaf (IG-030): el calendario no nombra lugar ni a terceros.
  - "Tiki Night" es el nombre de la destacada [BIO]; en 2025 fue el viernes de los 11 años (IG-053).
  - Bendita Primavera ocurrió una sola vez (2024): queda opcional.
  - Fuera del calendario: desfile de modas (2025, una vez), Almud & Rucalaf (locación ajena), Isleños (terceros), 8M (conmemoración, no fiesta de ciudad).
- **Fotos con fecha:** solo aquí. P073 (IG-100, crédito «@estudiouno.prod» [IG-100]), P221 (IG-047, sin crédito en caption), P348 (`Dbg3ekilC4P_11.jpg`, 3072 px, crédito «@isosur.prod» [IG-009]); P229 (IG-038, sin crédito). Opcional: P136 (disfrazados en los sillones, 1071 px, tamaño medio).
- **CTA:** «asegure su entrá hablándonos al DM!» [IG-057] (como texto del enlace) → `https://ig.me/m/almud_bar`
  - “get your ticket by messaging us on Instagram!” [EN]
  - Y ‹Ver en Instagram› [UI] / “See on Instagram” [EN] → `https://www.instagram.com/almud_bar/`

---

## 11. Cuándo y dónde (noche)

- **Propósito:** cerrar con todo lo necesario para ir: horario, dirección, mapa, DM, teléfono, Instagram.
- **Campo:** noche.
- **Titular:** «Venga venga, / le esperamos!» [IG-160] {display}
  - Alt 1: «Véngase pal / Almudcito ito ito» [IG-013] {display} (línea 2 justo en 17)
  - Alt 2: «Les amamos, / les esperamos!» [IG-092] {display}
  - “Come on, come on, we're expecting you!” [EN]
- **Cuerpo:** «Si usté no ha venido, vengase pa acá, ya le estamos esperando» [IG-004]
  - “If you haven't been yet, come on over, we're expecting you” [EN]
- **Datos** (body, tabular, en este orden):
  - ‹Horario› [UI] · “Hours” [EN]: «Abrimos de Mar a Sáb a las 18:00hrs» [BIO] · “Open Tue to Sat from 6 pm” [EN]. Nada más: sin cierre, sin lunes de verano.
  - ‹Dirección› [UI] · “Address” [EN]: «Serrano 325, Castro» [BIO] · «Al frente del Centro Cultural de Castro» [DATO] · “Opposite the Castro Cultural Centre” [EN]
  - ‹Teléfono› [UI] · “Phone” [EN]: «+56 65 253 0084» [DATO] → `tel:+56652530084`
  - ‹Instagram› [UI]: ‹@almud_bar› [UI] → `https://www.instagram.com/almud_bar/`
  - «Nuestro bazar @bazar_almud» [BIO] · “Our shop: @bazar_almud” [EN]
- **CTA:** ‹Cómo llegar› [UI] (botón barra) → `https://www.google.com/maps/search/?api=1&query=-42.4825681,-73.7617619` · ‹Escríbanos al DM› [UI] → `https://ig.me/m/almud_bar`
  - “Get directions” [EN] · “Message us on Instagram” [EN]
- **Imágenes:** **P199** (`DM_Ih5dyVKH_17.jpg`, la puerta de madera con megáfono; crédito ‹Foto› [UI] «@estudiouno.prod» [IG-050]). Loop chico **V031** (`DFWLrRxyvVB_00.mp4`, 1–10,4 s, sin sonido) con ‹Video› [UI] «@estudiouno.prod» [IG-061]. P333 pasó a El equipo.
- **Mapa:** imagen estática hasta el clic (no iframe de entrada). Coordenadas -42.4825681, -73.7617619 [DATO].

---

## 12. Pie (noche)

- **Propósito:** firmar como firman ellos y dar crédito.
- **Firma (lead):** «Que no se lo cuenten! Besiiiii» [IG-032] · “Don't let anyone tell you about it, come see! Besiiiii [kisses]” [EN]
  - Si Reseñas usa su Alt 1, la firma pasa a «Gracias totales! Se les quiere» [IG-001] · “Thanks a million! Love you all” [EN]
- **Repetición útil (small):** «Abrimos de Mar a Sáb a las 18:00hrs» [BIO] · «Serrano 325, Castro» [BIO] · ‹Escríbanos al DM› [UI] · ‹Ver la carta› [UI]
- **Créditos (small):** ‹Fotos y videos:› [UI] «@estudiouno.prod» [IG-050] · «@catarsis.fotografia» [IG-147] · «@tamillanquileo» [IG-178] · «@isosur.prod» [IG-009] · «@rober.patagonico» [IG-103] · ‹Afiches:› [UI] «@dosistudio» [IG-081]
  - “Photos and videos:” [EN] · “Posters:” [EN]
- **Nota (small):** ‹Hecho con fotos, textos y carta publicados por Almud Bar.› [UI] · “Made with photos, texts and menu published by Almud Bar.” [EN]
- © ‹Almud Bar · Castro, Chiloé› [UI]

---

## C. La carta (página propia `carta/`, papel; fase 15)

- **Propósito:** la carta completa como la imprimen, en su propia página (`carta/index.html`, plantilla `src-v2/carta.html`), con acceso desde la nav, Hoy en Almud, Tragos, Sin alcohol, Comida, los destacados y el pie. Antes de la fase 15 era una sección del landing (`#carta`).
- **Campo:** papel #f6ecdc arriba; **cada pestaña con su tinte suave** (derivado del campo del landing y mezclado con blanco cálido, mucho más claro): Coctelería de la casa fucsia · Cócteles del mundo mundial turquesa · Espirituosos amarillo · Vinos & espumantes coral · Mocktails sin alcohol verde · Comilona papel · Nuestras promos el color del día (como Hoy en Almud). Nombres en azul carta (Oswald 600, MAYÚSCULAS), precios en magenta (tabular, a la derecha), descripciones en noche (Oswald 300). Contraste AA verificado en cada tinte (el magenta manda: ≥ 4,5).
- **Cabecera:** logotipo → `../` (inicio) e ES/EN (persistente, la misma clave que el landing).
- **Título:** ‹La carta› [UI] {display: 8 car., 1 línea} · “The menu” [EN]
- **Bajada:** «En su Almudcito tenemos pa todos los gustos!» [IG-011] · “At your Almudcito [our little Almud] we've got something for every taste!” [EN]
- **Pestañas** (sticky en teléfono, tablet y escritorio; una sección a la vez): los títulos literales de cada sección de `carta-v2.json`. La de sin alcohol reúne las cuatro secciones del PDF CARTA-5 bajo su título «Mocktails sin alcohol» [CARTA-5] · “Alcohol-free mocktails & drinks” [EN]. Nav de pestañas: ‹Secciones de la carta› [UI] (aria) · “Menu sections” [EN].
- **Grupos** (chips filtrables, uno a la vez) en las pestañas largas: Cócteles del mundo mundial, Espirituosos, Mocktails sin alcohol y Comilona. Nombres literales de grupo; las glosas EN van bajo el título del grupo: “Juices & soft drinks” [EN] · “Alcohol-free beers” [EN] · “Hot drinks” [EN] (y las de abajo).
- **Anclas:** `#casa` `#mundo` `#espirituosos` `#vinos` `#sin-alcohol` `#comilona` `#promos`, y por grupo `#<pestaña>-<grupo>` (p. ej. `#comilona-pizzas`, `#espirituosos-gin`, `#sin-alcohol-jugos`).
- **Promos:** la del día se marca con ‹Hoy› [UI] / “Today” [EN] y la pestaña toma el tinte del día.
- **PDF oficial:** ‹Carta oficial (PDF)› [UI] → `https://uqr.to/ppvi` · “Official menu (PDF)” [EN] (cabecera y pie). ‹Volver arriba› [UI] / “Back to top” [EN] en el pie.

- **Índice (anclas) y categorías**, en el orden del brief (tragos, sin alcohol, bebidas, comilona) y agrupadas por PDF. Nombres de categoría literales del PDF; los ítems (nombre, descripción, precio) salen de `content/carta.json` (otro proceso lo está completando: aquí solo la estructura):

| Ancla | Título de grupo (PDF) | Categorías (literales) | Fuente | Estado en carta.json |
|---|---|---|---|---|
| `#carta-casa` | «Coctelería de la casa» [CARTA-2] | (14 cócteles de autor) | CARTA-2 | completo (`coctel`) |
| `#carta-mundo` | «Cócteles del mundo mundial» [CARTA-3] | «Clásicos» [CARTA-3] «[Algunos recomendados de su Almudcito]» [CARTA-3] · «Vermú» [CARTA-3] · «Mule» [CARTA-3] · «Negroni» [CARTA-3] · «Spritz» [CARTA-3] · «Sagüer» [CARTA-3] · «Mojitos» [CARTA-3] · «Red Bull te da aaalas» [CARTA-3] | CARTA-3 | pendiente |
| `#carta-espirituosos` | «Espirituosos» [CARTA-4] | «Piscolein o combinadito» [CARTA-4] · «Vodkita» [CARTA-4] · «Ron poromponpon» [CARTA-4] · «Whiscachos» [CARTA-4] · «Amamos el GIN!» [CARTA-4] · «Tequilazos & mezcalazos» [CARTA-4] | CARTA-4 | pendiente |
| `#carta-sin-alcohol` | «Mocktails de la casa» [CARTA-5] | «Coctelcitos sin alcohol» [CARTA-5] · «Mocktails clásicos» [CARTA-5] · «Jugos & bebidas» [CARTA-5] · «Cervezas sin alcohol» [CARTA-5] · «Bebidas calientes» [CARTA-5] | CARTA-5 | mocktails completos (`mocktail`); jugos, cervezas 0° y calientes pendientes |
| `#carta-vinos` | ‹Vinos y espumantes› [UI] (del PDF «Vinos Espumantes» [CARTA-6]) | «Tintelis» [CARTA-6] · «Blanquelis» [CARTA-6] · «Espumantes» [CARTA-6] · «Por copa» [CARTA-6] | CARTA-6 | pendiente |
| `#carta-comilona` | «Comilona» [CARTA-1] | «Picoteos» [CARTA-1] · «Greditas» [CARTA-1] · «Sanguches» [CARTA-1] · «Pizzas artesanales» [CARTA-1] · «Pa los chichichos» [CARTA-1] · «Somos dulzones» [CARTA-1] | CARTA-1 | completo (`comilona`) |
| `#carta-promos` | «Promos» [CARTA-7] | la semana de 3.7 + «$ 4.500» [CARTA-7] · «de 18:00 a 22:00 hrs» [CARTA-7] | CARTA-7 | completo (`promos`) |

- [EN] de los títulos de grupo: “House cocktails” [EN] · “Cocktails from all over the world [del mundo mundial]” [EN] · “Spirits” [EN] · “House mocktails” [EN] · “Wines & sparkling” [EN] · “Comilona [food]” [EN] · “Weekly deals” [EN]. Las categorías con juego de palabras se glosan: “Tintelis [reds]” [EN], “Blanquelis [whites]” [EN], “Whiscachos [whiskies]” [EN], “Ron poromponpon [rum]” [EN], “Vodkita [vodka]” [EN], “Pa los chichichos [kids]” [EN], “Somos dulzones [desserts]” [EN].
- Los títulos de grupo de CARTA-3, 4 y 6 salen del nombre del PDF de la carta oficial (`carta_3_Cocteles_Del_Mundo_Mundial.pdf`, `carta_4_Espirituosos.pdf`, `carta_6_Vinos_Espumantes.pdf`); el PDF no imprime ese título en la página.
- Las descripciones y nombres de ítems **no se traducen**; en modo EN, cada categoría lleva una glosa breve [EN] bajo su título. (Decisión abierta 3 del contrato: si el cliente pide traducción de descripciones, va como `<details>` por ítem.)
- **Notas (small):** «* Siempre sujeto a stock! *» [CARTA-7] · ‹Precios de la carta oficial, octubre 2026.› [UI] · “Prices from the official menu, October 2026.” [EN]
- **CTA (antes de la fase 15):** ‹Carta completa› [UI] (botón azul carta → `https://uqr.to/ppvi`, los PDF oficiales) · “Full menu (PDF)” [EN] · ‹Volver arriba› [UI] / “Back to top” [EN]
- **Imágenes (fase 15):** foto por ítem solo donde la foto es ese ítem: Peter, Cómo te voy a olvidar, Sagüer on Faia, Sangría Foreva!, Coquette, La moto chantá, Tukulito, Con tuti, Camarón que se duerme, Topiturrón, Pizza dulzona (P310) y las promos del martes (V054-cover, IG-016), miércoles (P331, IG-019) y jueves (P228, IG-039). Láminas sin nombre de ítem (fotos de ambiente o de grupo): Coctelería de la casa (loop V021, el muro rosa), Cócteles del mundo mundial (P086, tres copas con espuma), grupo Negroni (P226, IG-042), grupo Spritz (P016, IG-167, ‹Foto› [UI] «@catarsis.fotografia» [IG-167]), Espirituosos (P003), Vinos & espumantes (P191, ‹Foto› [UI] «@estudiouno.prod» [IG-050]), Comilona (loop V052 de una gredita, IG-018; lámina de pestaña para que la columna no cambie de ancho entre grupos) y Pizzas artesanales (P042, ‹Foto› [UI] «@catarsis.fotografia» [IG-141]).
- **Imágenes (antes de la fase 15; láminas dentro del papel):** **P003** (`Cmce2h1J3Wl_00.jpg`; crédito ‹Foto› [UI] «@tamillanquileo» [IG-178]) y **P070** (`C7HV31OLXTJ_00.jpg`, tacos de atún; sin crédito en caption). Reels V021 (muro rosa, IG-090) y V052 (cazuela burbujeando, IG-018) como loops. **Ninguna lleva nombre de plato o trago**: P003 no es un Negroni según su caption (es «EN QUÉ TOPAMOH?!», IG-178, ya fuera de carta) y los tacos de P070 (IG-105) no están en la carta actual.
- La fila de un ítem con foto real usa `carta.json › img` (IG-044 Peter, IG-002 Cómo te voy a olvidar, IG-063 Sagüer on Faia, IG-039 Sangría Foreva!, IG-096 Coquette, IG-011 La moto chantá, IG-139 Tukulito, IG-066 Con tuti, IG-077 Camarón que se duerme, IG-040 Topiturrón).

---

## Correcciones mínimas

1. **Emoji quitados** de todo texto visible (glifo fuera, palabra intacta). Dentro de un literal usado hay uno solo: «Nuestro bazar @bazar_almud» (BIO: "Nuestro bazar 👉🏼 @bazar_almud"; columna "Emoji quitado" del script). Pegados al borde de un recorte, y por eso fuera del texto: «Hermoso y ricardo» (IG-044, "😂!" después), «traguitos y travesuras 1313» (IG-124, "🧡" antes y "😂!" después), «Que no se lo cuenten! Besiiiii» (IG-032, "😘" al final), «A celebrar se ha dicho!» (IG-015, "🌈" después), «Vamos por más!» (IG-041, "💪🏼" después), «Nos vemos en las próximas cositas que se vienennnn bomba» (IG-010, "💣💥!" después), «Dicen que una mirada vale más que mil palabras…» (IG-118, "✨" después), «su terraza permite con sol o lluvia una tremenda vista» (reseña de Visitante, "🫰🏾" al final).
2. **Espacio antes de puntuación** que queda al quitar un emoji (p. ej. "bomba 💥, picho" → "bomba, picho"): se normaliza.
3. **Saltos de línea** de las captions se leen como un espacio; ` / ` en los titulares es nuestro corte (`<br>`).
4. **Recortes:** los titulares son fragmentos de frases más largas y conservan su caja original (minúscula inicial en «nos gusta el colorssss!», «mejor los tomamos todos!», «pa chuparse el bigoteli», «lo rico de nuestro barsucho», «tirar la casa por la ventana!»). Six Caps tiene minúsculas en versalitas, así que se respeta la caja literal.
5. **Caja en la carta:** los PDF imprimen nombres y categorías en mayúsculas ("COCTELERÍA de la CASA", "TINTELIS"). Se escriben en caja de oración y la verificación contra el PDF es sin distinguir mayúsculas; en pantalla, los nombres vuelven a MAYÚSCULAS por CSS (sistema.md §7).
6. **Títulos de grupo de la carta** sacados del nombre del PDF (CARTA-3, 4 y 6), porque la página no los imprime: "Cócteles del mundo mundial" (se restituye la tilde que el nombre de archivo no lleva; la verificación contra el nombre de archivo ignora tildes), "Espirituosos" tal cual, y "Vinos y espumantes" como etiqueta [UI] (el archivo dice "Vinos_Espumantes").
7. **Carta heredada** de `carta.json`: "Le llea" → "Le lleva" (Peter), "refrecante" → "refrescante" (Desde que te conocí), punto en Tukulito ("bigoteli. Acompañado").
8. **VID-061:** se verifica contra la transcripción de los subtítulos quemados que está en `content/copy.md` (v1), no contra el video. Reconfirmar a ojo los dos recortes usados.
9. **@ del equipo:** se respeta cada fuente: "@lizzearellano" en IG-010 y IG-031, "@lizzearellanol" en IG-014, IG-048 e IG-067. Pedir al bar cuál es la vigente antes de publicar.
10. **Reseñas:** ortografía original intacta ("porque se habla", "rapido"). Recortes marcados en §9.
11. **Promo del sábado:** «Ramón a $ 4.500!» ya trae el precio; no se repite «$ 4.500».
12. **"Escríbanos al DM"** es [UI] nuestro en el "usted" de la marca (la v1 decía "Escríbenos").

---

## Verificación

`python3 tools/verify_copy.py` extrae cada `«…» [FUENTE]` de este archivo, lo normaliza (glifos emoji fuera, saltos de línea y ` / ` como espacio, espacios colapsados, sin espacio antes de puntuación) y lo busca **literal** en el texto de su fuente (sin distinguir mayúsculas solo en CARTA). Un recorte con `…` se verifica trozo a trozo, en orden. También mide los titulares `{display}`/`{head}` con la aritmética de §0, cuenta palabras de los bloques (aviso si > 25) y busca palabras prohibidas (fila, esperar mesa, desocupar, queue…). Sale con código 1 si algo falla.

<!-- VERIFICACION:INICIO -->
Resultado: **211/211 literales pasan**; **42/42 titulares caben en 2 líneas**; palabras prohibidas: 0. Generado por `tools/verify_copy.py`.

### Literales

| # | Texto literal | Fuente | Verificación | Modo | Emoji quitado |
|---|---|---|---|---|---|
| 1 | @estudiouno.prod | IG-050 | pasa | exacto |  |
| 2 | Coctelería de autor, comida & música bonita desde 2014 | BIO | pasa | exacto |  |
| 3 | Abrimos de Mar a Sáb a las 18:00hrs | BIO | pasa | exacto |  |
| 4 | Serrano 325, Castro | BIO | pasa | exacto |  |
| 5 | $ 4.500 | CARTA-7 | pasa | exacto (sin mayúsc.) |  |
| 6 | de 18:00 a 22:00 hrs | CARTA-7 | pasa | exacto (sin mayúsc.) |  |
| 7 | * Siempre sujeto a stock! * | CARTA-7 | pasa | exacto (sin mayúsc.) |  |
| 8 | Amamos los / martes | IG-016 | pasa | exacto |  |
| 9 | Negronicito / ito ito | IG-016 | pasa | exacto |  |
| 10 | Por más negronis / siempre | IG-016 | pasa | exacto |  |
| 11 | Negroni & Fernet c/Coca Cola | CARTA-7 | pasa | exacto (sin mayúsc.) |  |
| 12 | aguante este clásico infalible, maravilloso, delichus, contundente, elegante, finoli | IG-016 | pasa | exacto |  |
| 13 | Miércoles de / piscoleinnnn! | IG-019 | pasa | exacto |  |
| 14 | Mitad de / semana | IG-019 | pasa | exacto |  |
| 15 | combinaitos / itos itos!!! | IG-019 | pasa | exacto |  |
| 16 | Piscolein & Gin Tonic | CARTA-7 | pasa | exacto (sin mayúsc.) |  |
| 17 | Mitad de semana, y es justo y necesario salir a tomar aire y muchos combinaitos itos itos!!! | IG-019 | pasa | exacto |  |
| 18 | Jueves de / Sangría! | IG-039 | pasa | exacto |  |
| 19 | está que arden / las sangrías | IG-098 | pasa | exacto |  |
| 20 | Sangriita rica / delichussss! | IG-074 | pasa | exacto |  |
| 21 | Sangría de la casa | CARTA-7 | pasa | exacto (sin mayúsc.) |  |
| 22 | Además que con estos días, la hidrateichon es justa y muy necesaria! | IG-039 | pasa | exacto |  |
| 23 | Viernes ya! | IG-003 | pasa | exacto |  |
| 24 | Es viernes! | IG-042 | pasa | exacto |  |
| 25 | Ya es / viernes!!! | IG-073 | pasa | exacto |  |
| 26 | Venga venga que nadie le detenga! | IG-003 | pasa | exacto |  |
| 27 | Le esperamos con cantidá de cosas ricas ricas pal buche y pa empinar ese codo regalón | IG-003 | pasa | exacto |  |
| 28 | Último día / de la semana | IG-020 | pasa | exacto |  |
| 29 | pa que venga a / guarisnaquearse! | IG-023 | pasa | exacto |  |
| 30 | Mejor / empinarsss! | IG-023 | pasa | exacto |  |
| 31 | Ramón a $ 4.500! | CARTA-7 | pasa | exacto (sin mayúsc.) |  |
| 32 | Es una precisa mezcla: gin, licor marrasquino, limón y romero. | CARTA-2 | pasa | exacto (sin mayúsc.) |  |
| 33 | Abrimos de / Mar a Sáb | BIO | pasa | exacto |  |
| 34 | siempre es un güen día pa compartir algo rico | IG-013 | pasa | exacto |  |
| 35 | Martes | CARTA-7 | pasa | exacto (sin mayúsc.) |  |
| 36 | Miércoles | CARTA-7 | pasa | exacto (sin mayúsc.) |  |
| 37 | Jueves | CARTA-7 | pasa | exacto (sin mayúsc.) |  |
| 38 | Sábado | CARTA-7 | pasa | exacto (sin mayúsc.) |  |
| 39 | nos gusta el / colorssss! | IG-111 | pasa | exacto |  |
| 40 | Lo más güeno / qué hay | IG-160 | pasa | exacto |  |
| 41 | Venga pa / la selfie | IG-111 | pasa | exacto |  |
| 42 | Somos inquietos y nos gusta el colorssss! Tratando siempre de hacer nuestro Almudcito beio para su deleite | IG-111 | pasa | exacto |  |
| 43 | Un lugar que fuera cálido, acogedor | VID-061 | pasa | exacto |  |
| 44 | Pucha que nos gusta nuestra barrita!! | IG-087 | pasa | exacto |  |
| 45 | y una gran barra, larga, de esas para sentarse y quedarse ahí | VID-061 | pasa | exacto |  |
| 46 | @rober.patagonico | IG-103 | pasa | exacto |  |
| 47 | Se deslizan como angelitos, con trago en mano por los salones | IG-067 | pasa | exacto |  |
| 48 | @isosur.prod | IG-009 | pasa | exacto |  |
| 49 | pa compartir, pa escuchar güena música, pa ponerle algo delichus al buche | IG-075 | pasa | exacto |  |
| 50 | comfy seats | RESEÑA:Benjamín | pasa | exacto |  |
| 51 | @estudiouno.prod | IG-075 | pasa | exacto |  |
| 52 | Techamos parte de la terraza, le pusimos todo el colors y calor del mundo mundial | IG-004 | pasa | exacto |  |
| 53 | sin mojarse y calentit@, qué mejor?! | IG-004 | pasa | exacto |  |
| 54 | Tardes y nochecitas de terraza! Lo más güeno qué hay | IG-160 | pasa | exacto |  |
| 55 | Amamos los atardeceres desde nuestra terracita ita ita! | IG-163 | pasa | exacto |  |
| 56 | @catarsis.fotografia | IG-144 | pasa | exacto |  |
| 57 | Dicen que una mirada vale más que mil palabras… | IG-118 | pasa | exacto |  |
| 58 | OJO PIOJO es un proyecto hecho con mucho amor, paciencia y tiempo | IG-118 | pasa | exacto |  |
| 59 | Proyecto @cepaz | IG-118 | pasa | exacto |  |
| 60 | @estudiouno.prod | IG-061 | pasa | exacto |  |
| 61 | Nos gustan los brillitos, las luces | IG-147 | pasa | exacto |  |
| 62 | mejor los / tomamos todos! | IG-046 | pasa | exacto |  |
| 63 | Tantos / coctelcitos | IG-046 | pasa | exacto |  |
| 64 | Etiquetas pa / regodearse! | IG-020 | pasa | exacto |  |
| 65 | Tantos coctelcitos entre los cuales decidirse! Demasiada complikeichon elegir, mejor los tomamos todos! | IG-046 | pasa | exacto |  |
| 66 | Tantos creadores con tantísimo talento e innumerables horas de probar, probar y probar | IG-021 | pasa | exacto |  |
| 67 | En esta barrita pasan tantas maravillas en forma de coctelcitos | IG-045 | pasa | exacto |  |
| 68 | Coctelería de la casa | CARTA-2 | pasa | exacto (sin mayúsc.) |  |
| 69 | Aquí te las traigo Peter | CARTA-2 | pasa | exacto (sin mayúsc.) |  |
| 70 | Hermoso y ricardo | IG-044 | pasa | exacto |  |
| 71 | Cómo te voy a olvidar | CARTA-2 | pasa | exacto (sin mayúsc.) |  |
| 72 | este cóctel que está 10/10 | IG-002 | pasa | exacto |  |
| 73 | Sagüer on Faia | CARTA-2 | pasa | exacto (sin mayúsc.) |  |
| 74 | es como un sour, pero acanelado y medio picantito | IG-063 | pasa | exacto |  |
| 75 | A veces me pongo Coquette | CARTA-2 | pasa | exacto (sin mayúsc.) |  |
| 76 | una delicia rosada, cremosa y dulzona! | CARTA-2 | pasa | exacto (sin mayúsc.) |  |
| 77 | no dejamos a nadie ajuera | IG-011 | pasa | exacto |  |
| 78 | tenemos pa todos los gustos! | IG-011 | pasa | exacto |  |
| 79 | un manjar pa los menores de edá, embarazás, abstemi@s | IG-011 | pasa | exacto |  |
| 80 | Y si usted es sobri@ y alocad@ tenemos unos mocktail que están de pelos! | IG-141 | pasa | exacto |  |
| 81 | La moto chantá | CARTA-5 | pasa | exacto (sin mayúsc.) |  |
| 82 | Juguito de mango y maracuyá, pepino, jarabe simple, limón y bitter pepino! | CARTA-5 | pasa | exacto (sin mayúsc.) |  |
| 83 | Coctelcitos sin alcohol | CARTA-5 | pasa | exacto (sin mayúsc.) |  |
| 84 | Jugos & bebidas | CARTA-5 | pasa | exacto (sin mayúsc.) |  |
| 85 | Cervezas sin alcohol | CARTA-5 | pasa | exacto (sin mayúsc.) |  |
| 86 | Bebidas calientes | CARTA-5 | pasa | exacto (sin mayúsc.) |  |
| 87 | pa chuparse / el bigoteli | IG-139 | pasa | exacto |  |
| 88 | Puro / manjarshhhh | IG-022 | pasa | exacto |  |
| 89 | comilona / ona ona! | IG-092 | pasa | exacto |  |
| 90 | Mire que tenemos una cocina sencilla pero más que sabrosona! | IG-022 | pasa | exacto |  |
| 91 | Nos gustan los brillitos, las luces, los coctelcitos y la comida que deja el ombligo pa ajuera! | IG-147 | pasa | exacto |  |
| 92 | la comida que deja el ombligo pa ajuera! | IG-147 | pasa | exacto |  |
| 93 | Picoteos | CARTA-1 | pasa | exacto (sin mayúsc.) |  |
| 94 | Greditas | CARTA-1 | pasa | exacto (sin mayúsc.) |  |
| 95 | Sanguches | CARTA-1 | pasa | exacto (sin mayúsc.) |  |
| 96 | Pizzas artesanales | CARTA-1 | pasa | exacto (sin mayúsc.) |  |
| 97 | Pa los chichichos | CARTA-1 | pasa | exacto (sin mayúsc.) |  |
| 98 | Somos dulzones | CARTA-1 | pasa | exacto (sin mayúsc.) |  |
| 99 | Tukulito Sakayama | CARTA-1 | pasa | exacto (sin mayúsc.) |  |
| 100 | pa usté solit@ o pa compartir! | IG-139 | pasa | exacto |  |
| 101 | Tataki de lomo de atún marinado | CARTA-1 | pasa | exacto (sin mayúsc.) |  |
| 102 | Con tuti si no pa qué! | CARTA-1 | pasa | exacto (sin mayúsc.) |  |
| 103 | Especial pa compartir | CARTA-1 | pasa | exacto (sin mayúsc.) |  |
| 104 | Camarón que se duerme | CARTA-1 | pasa | exacto (sin mayúsc.) |  |
| 105 | Calentitas, contundentes, enjundiosas: otsea, 10 de 10. | IG-018 | pasa | exacto |  |
| 106 | Topiturrón | CARTA-1 | pasa | exacto (sin mayúsc.) |  |
| 107 | turrón de chocolate con galletas y nueces, gel de mango y maracuyá | IG-040 | pasa | exacto |  |
| 108 | Si le gustan las pizzas con masa delgadita y con una propuesta choriflai de mezclas | IG-141 | pasa | exacto |  |
| 109 | @catarsis.fotografia | IG-147 | pasa | exacto |  |
| 110 | En su Almudcito tenemos pa todos los gustos! | IG-011 | pasa | exacto |  |
| 111 | Este es tan lindo! Le lleva: Mistral Nobel Cristalino, licor de flor de saúco, cranberry, limoncito y un toque dulce de jarabe. Pero lejos lo más bacán es la burbuja que viene aquí! | CARTA-2 | pasa | exacto (sin mayúsc.) |  |
| 112 | Este es un sour bien especial: va con Mistral Nobel Fire, limón y jarabe que complementa este cóctel especiado, medio picantito y muy rico!!! | CARTA-2 | pasa | exacto (sin mayúsc.) |  |
| 113 | Sangría Foreva! | CARTA-2 | pasa | exacto (sin mayúsc.) |  |
| 114 | Esta versión te dejará como perro con dos colas! Vino Carménère, toda la malicia del pisco añejado, jarabe de canela, unos toques frutales infaltables y mucho amor | CARTA-2 | pasa | exacto (sin mayúsc.) |  |
| 115 | Mocktails de la casa | CARTA-5 | pasa | exacto (sin mayúsc.) |  |
| 116 | Juguito de mango y maracuyá, pepino, jarabe simple, limón y bitter pepino! [El vasito va con crusta de sal] | CARTA-5 | pasa | exacto (sin mayúsc.) |  |
| 117 | Comilona | CARTA-1 | pasa | nombre del PDF (sin tildes ni mayúsc.) |  |
| 118 | Tataki de lomo de atún marinado pa chuparse el bigoteli. Acompañado de pancito y salsa de la casa. | CARTA-1 | pasa | exacto (sin mayúsc.) |  |
| 119 | Delichus mix: camarones, mezclado con queso crema, cebollín, cilantro, champiñones, jengibre desglasado con vino blanco | CARTA-1 | pasa | exacto (sin mayúsc.) |  |
| 120 | Pizza dulzona | CARTA-1 | pasa | exacto (sin mayúsc.) |  |
| 121 | Ideal para compartir! Es una pizza, pero dulce, está super delichus! Pasta de avellana, crema, frutos rojos glaseados, almendras fileteadas y hojitas de menta. | CARTA-1 | pasa | exacto (sin mayúsc.) |  |
| 122 | Peazo de equipo / que tenemos! | IG-048 | pasa | exacto |  |
| 123 | qué pedazo de / team tenemos! | IG-010 | pasa | exacto |  |
| 124 | Somos una banda / variada | IG-067 | pasa | exacto |  |
| 125 | Est@s guapetones son parte de nuestro equipo, son los encargados de barra y salón | IG-001 | pasa | exacto |  |
| 126 | le ponen una sonrisota con cada cóctecito ito ito, comida delichus y la atención más güena! | IG-001 | pasa | exacto |  |
| 127 | @pablete_bartender_ @javier.agmc @lizzearellano @milagroosjm @eduu.ardoo @elymar_bocarejo @jaav11 @daweed.cagliano @haqum.v99 | IG-010 | pasa | exacto |  |
| 128 | los papis del almud: el franchuto @rusio_mezclao y la disharashera @cepaz | IG-067 | pasa | exacto |  |
| 129 | Nuestras chicas super poderosas, super bacanas y super hermosas! | IG-014 | pasa | exacto |  |
| 130 | @milagroosjm y @lizzearellanol | IG-014 | pasa | exacto |  |
| 131 | no somos ná / sin ustedes! | IG-026 | pasa | exacto |  |
| 132 | Venga a celebrar / la vida | IG-142 | pasa | exacto |  |
| 133 | esta vida es / una sola! | IG-157 | pasa | exacto |  |
| 134 | Pa agarrar perso, pa pasar las penas, las alegrías, celebreichons, pa entrar en calor, pa refrescarse | IG-060 | pasa | exacto |  |
| 135 | celebremos el amor en todas sus formas, con las piernas, amiguis, hij@s, como usté quiera! | IG-060 | pasa | exacto |  |
| 136 | celebrar la vida, la amistad, el amors y el buen clima | IG-065 | pasa | exacto |  |
| 137 | A celebrar se ha dicho! | IG-015 | pasa | exacto |  |
| 138 | porque usté se lo merece y punto! | IG-150 | pasa | exacto |  |
| 139 | ideal pa venir a bien-tratarse a la terracita o a la barra | IG-162 | pasa | exacto |  |
| 140 | lo rico de / nuestro barsucho | IG-088 | pasa | exacto |  |
| 141 | Que no se lo / cuenten! | IG-032 | pasa | exacto |  |
| 142 | Ya sabe ya | IG-088 | pasa | exacto |  |
| 143 | 4,6 | DATO | pasa | exacto |  |
| 144 | 848 reseñas | DATO | pasa | exacto |  |
| 145 | 209 | DATO | pasa | exacto |  |
| 146 | What really sets Almud apart is that the food isn't an afterthought – it's fantastic. | RESEÑA:Holger K | pasa | exacto |  |
| 147 | Ahora entiendo porque se habla tanto del lugar. Lindo, rapido, rico, céntrico y económico. Super sugerido | RESEÑA:Kevin B | pasa | exacto |  |
| 148 | The bar tenders are artists, sit on the bar and watch. | RESEÑA:Ai T | pasa | exacto |  |
| 149 | su terraza permite con sol o lluvia una tremenda vista | RESEÑA:Visitante | pasa | exacto |  |
| 150 | Super soirée à Castro ! Le service est sympa, super ambiance, avec musique très sympa! | RESEÑA:Dorothee M | pasa | exacto |  |
| 151 | Estuve ahí cada día de mi estancia, porque es imposible no volver. | RESEÑA:arqggodoy | pasa | exacto |  |
| 152 | tirar la casa / por la ventana! | IG-010 | pasa | exacto |  |
| 153 | Vamos por / más! | IG-041 | pasa | exacto |  |
| 154 | tirar el bar / por la ventana | IG-081 | pasa | exacto |  |
| 155 | Nos vemos en las próximas cositas que se vienennnn bomba | IG-010 | pasa | exacto |  |
| 156 | 14F | IG-116 | pasa | exacto |  |
| 157 | Amamos el 14F pa brindar en honor al amor! | IG-116 | pasa | exacto |  |
| 158 | chaolin bombín al verano | IG-030 | pasa | exacto |  |
| 159 | Y se nos van los mesesitos queridos de verano y vakeichons… y hay que despedirlos como corresponde | IG-114 | pasa | exacto |  |
| 160 | nuestro mes de aniversario | IG-098 | pasa | exacto |  |
| 161 | Cuánto coctelcito ha pasado bajo este puente | IG-010 | pasa | exacto |  |
| 162 | Tiki Night | BIO | pasa | exacto |  |
| 163 | con todo el sabor tiki! | IG-053 | pasa | exacto |  |
| 164 | fondita ita ita | IG-081 | pasa | exacto |  |
| 165 | Nos endieciochamos contra viento y marea | IG-043 | pasa | exacto |  |
| 166 | negroni week | IG-005 | pasa | exacto |  |
| 167 | esperada por much@s ya está aquí | IG-005 | pasa | exacto |  |
| 168 | Bendita Primavera | IG-076 | pasa | exacto |  |
| 169 | nuestro día de bienvenida a la esperada primavera! | IG-075 | pasa | exacto |  |
| 170 | Jalogüín | IG-071 | pasa | exacto |  |
| 171 | traguitos y travesuras 1313 | IG-124 | pasa | exacto |  |
| 172 | @estudiouno.prod | IG-100 | pasa | exacto |  |
| 173 | asegure su entrá hablándonos al DM! | IG-057 | pasa | exacto |  |
| 174 | Venga venga, / le esperamos! | IG-160 | pasa | exacto |  |
| 175 | Véngase pal / Almudcito ito ito | IG-013 | pasa | exacto |  |
| 176 | Les amamos, / les esperamos! | IG-092 | pasa | exacto |  |
| 177 | Si usté no ha venido, vengase pa acá, ya le estamos esperando | IG-004 | pasa | exacto |  |
| 178 | Al frente del Centro Cultural de Castro | DATO | pasa | exacto |  |
| 179 | +56 65 253 0084 | DATO | pasa | exacto |  |
| 180 | Nuestro bazar @bazar_almud | BIO | pasa | exacto | sí |
| 181 | Que no se lo cuenten! Besiiiii | IG-032 | pasa | exacto |  |
| 182 | Gracias totales! Se les quiere | IG-001 | pasa | exacto |  |
| 183 | @tamillanquileo | IG-178 | pasa | exacto |  |
| 184 | @dosistudio | IG-081 | pasa | exacto |  |
| 185 | Mocktails sin alcohol | CARTA-5 | pasa | nombre del PDF (sin tildes ni mayúsc.) |  |
| 186 | Cócteles del mundo mundial | CARTA-3 | pasa | nombre del PDF (sin tildes ni mayúsc.) |  |
| 187 | Clásicos | CARTA-3 | pasa | exacto (sin mayúsc.) |  |
| 188 | [Algunos recomendados de su Almudcito] | CARTA-3 | pasa | exacto (sin mayúsc.) |  |
| 189 | Vermú | CARTA-3 | pasa | exacto (sin mayúsc.) |  |
| 190 | Mule | CARTA-3 | pasa | exacto (sin mayúsc.) |  |
| 191 | Negroni | CARTA-3 | pasa | exacto (sin mayúsc.) |  |
| 192 | Spritz | CARTA-3 | pasa | exacto (sin mayúsc.) |  |
| 193 | Sagüer | CARTA-3 | pasa | exacto (sin mayúsc.) |  |
| 194 | Mojitos | CARTA-3 | pasa | exacto (sin mayúsc.) |  |
| 195 | Red Bull te da aaalas | CARTA-3 | pasa | exacto (sin mayúsc.) |  |
| 196 | Espirituosos | CARTA-4 | pasa | nombre del PDF (sin tildes ni mayúsc.) |  |
| 197 | Piscolein o combinadito | CARTA-4 | pasa | exacto (sin mayúsc.) |  |
| 198 | Vodkita | CARTA-4 | pasa | exacto (sin mayúsc.) |  |
| 199 | Ron poromponpon | CARTA-4 | pasa | exacto (sin mayúsc.) |  |
| 200 | Whiscachos | CARTA-4 | pasa | exacto (sin mayúsc.) |  |
| 201 | Amamos el GIN! | CARTA-4 | pasa | exacto (sin mayúsc.) |  |
| 202 | Tequilazos & mezcalazos | CARTA-4 | pasa | exacto (sin mayúsc.) |  |
| 203 | Mocktails clásicos | CARTA-5 | pasa | exacto (sin mayúsc.) |  |
| 204 | Vinos Espumantes | CARTA-6 | pasa | nombre del PDF (sin tildes ni mayúsc.) |  |
| 205 | Tintelis | CARTA-6 | pasa | exacto (sin mayúsc.) |  |
| 206 | Blanquelis | CARTA-6 | pasa | exacto (sin mayúsc.) |  |
| 207 | Espumantes | CARTA-6 | pasa | exacto (sin mayúsc.) |  |
| 208 | Por copa | CARTA-6 | pasa | exacto (sin mayúsc.) |  |
| 209 | Promos | CARTA-7 | pasa | exacto (sin mayúsc.) |  |
| 210 | @catarsis.fotografia | IG-167 | pasa | exacto |  |
| 211 | @catarsis.fotografia | IG-141 | pasa | exacto |  |

### Titulares (Six Caps, k = 0,22; car. por línea / capacidad)

| Titular | Fuente | Paso | 390 · 1440 | Cabe | Nota |
|---|---|---|---|---|---|
| Amamos los / martes | IG-016 | display | 390: 10+6/17 · 1440: 10+6/17 | pasa |  |
| Negronicito / ito ito | IG-016 | display | 390: 11+7/17 · 1440: 11+7/17 | pasa |  |
| Por más negronis / siempre | IG-016 | display | 390: 16+7/17 · 1440: 16+7/17 | pasa |  |
| Miércoles de / piscoleinnnn! | IG-019 | display | 390: 12+13/17 · 1440: 12+13/17 | pasa |  |
| Mitad de / semana | IG-019 | display | 390: 8+6/17 · 1440: 8+6/17 | pasa |  |
| combinaitos / itos itos!!! | IG-019 | display | 390: 11+12/17 · 1440: 11+12/17 | pasa |  |
| Jueves de / Sangría! | IG-039 | display | 390: 9+8/17 · 1440: 9+8/17 | pasa |  |
| está que arden / las sangrías | IG-098 | display | 390: 14+12/17 · 1440: 14+12/17 | pasa |  |
| Sangriita rica / delichussss! | IG-074 | display | 390: 14+12/17 · 1440: 14+12/17 | pasa |  |
| Viernes ya! | IG-003 | display | 390: 11/17 · 1440: 11/17 | pasa |  |
| Es viernes! | IG-042 | display | 390: 11/17 · 1440: 11/17 | pasa |  |
| Ya es / viernes!!! | IG-073 | display | 390: 5+10/17 · 1440: 5+10/17 | pasa |  |
| Último día / de la semana | IG-020 | display | 390: 10+12/17 · 1440: 10+12/17 | pasa |  |
| pa que venga a / guarisnaquearse! | IG-023 | display | 390: 14+16/17 · 1440: 14+16/17 | pasa | total 31 > 30 |
| Mejor / empinarsss! | IG-023 | display | 390: 5+11/17 · 1440: 5+11/17 | pasa |  |
| Abrimos de / Mar a Sáb | BIO | display | 390: 10+9/17 · 1440: 10+9/17 | pasa |  |
| nos gusta el / colorssss! | IG-111 | display | 390: 12+10/17 · 1440: 12+10/17 | pasa |  |
| Lo más güeno / qué hay | IG-160 | display | 390: 12+7/17 · 1440: 12+7/17 | pasa |  |
| Venga pa / la selfie | IG-111 | display | 390: 8+9/17 · 1440: 8+9/17 | pasa |  |
| mejor los / tomamos todos! | IG-046 | display | 390: 9+14/17 · 1440: 9+14/17 | pasa |  |
| Tantos / coctelcitos | IG-046 | display | 390: 6+11/17 · 1440: 6+11/17 | pasa |  |
| Etiquetas pa / regodearse! | IG-020 | display | 390: 12+11/17 · 1440: 12+11/17 | pasa |  |
| no dejamos a nadie ajuera | IG-011 | head | 390: 25/29 · 1440: 25/37 | pasa |  |
| tenemos pa todos los gustos! | IG-011 | head | 390: 28/29 · 1440: 28/37 | pasa |  |
| pa chuparse / el bigoteli | IG-139 | display | 390: 11+11/17 · 1440: 11+11/17 | pasa |  |
| Puro / manjarshhhh | IG-022 | display | 390: 4+11/17 · 1440: 4+11/17 | pasa |  |
| comilona / ona ona! | IG-092 | display | 390: 8+8/17 · 1440: 8+8/17 | pasa |  |
| Peazo de equipo / que tenemos! | IG-048 | display | 390: 15+12/17 · 1440: 15+12/17 | pasa |  |
| qué pedazo de / team tenemos! | IG-010 | display | 390: 13+13/17 · 1440: 13+13/17 | pasa |  |
| Somos una banda / variada | IG-067 | display | 390: 15+7/17 · 1440: 15+7/17 | pasa |  |
| no somos ná / sin ustedes! | IG-026 | display | 390: 11+12/17 · 1440: 11+12/17 | pasa |  |
| Venga a celebrar / la vida | IG-142 | display | 390: 16+7/17 · 1440: 16+7/17 | pasa |  |
| esta vida es / una sola! | IG-157 | display | 390: 12+9/17 · 1440: 12+9/17 | pasa |  |
| lo rico de / nuestro barsucho | IG-088 | display | 390: 10+16/17 · 1440: 10+16/17 | pasa |  |
| Que no se lo / cuenten! | IG-032 | display | 390: 12+8/17 · 1440: 12+8/17 | pasa |  |
| Ya sabe ya | IG-088 | display | 390: 10/17 · 1440: 10/17 | pasa |  |
| tirar la casa / por la ventana! | IG-010 | display | 390: 13+15/17 · 1440: 13+15/17 | pasa |  |
| Vamos por / más! | IG-041 | display | 390: 9+4/17 · 1440: 9+4/17 | pasa |  |
| tirar el bar / por la ventana | IG-081 | display | 390: 12+14/17 · 1440: 12+14/17 | pasa |  |
| Venga venga, / le esperamos! | IG-160 | display | 390: 12+13/17 · 1440: 12+13/17 | pasa |  |
| Véngase pal / Almudcito ito ito | IG-013 | display | 390: 11+17/17 · 1440: 11+17/17 | pasa | justo |
| Les amamos, / les esperamos! | IG-092 | display | 390: 11+14/17 · 1440: 11+14/17 | pasa |  |

### Avisos

- CARTA-2: 33 palabras «Este es tan lindo! Le lleva: Mistral Nobel Cristal…»
- CARTA-2: 27 palabras «Esta versión te dejará como perro con dos colas! V…»
<!-- VERIFICACION:FIN -->
