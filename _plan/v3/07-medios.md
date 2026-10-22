# Fase 7 · Medios v3 (imágenes y video)

Generado por `python3 tools/media_v3.py --qa` desde `assets/v3/media.json` (manifiesto `tools/media_v3.json`). KB = 1024 bytes. Hoja de contacto: `_plan/v3/07-medios.jpg` (borde azul = póster de video; etiqueta rosa = por confirmar).

Solo material propio de @almud_bar (fotógrafos encargados por el bar, acreditados). Sin terceros, sin exempleados, sin afiches ni texto encima; disfraces solo en Eventos. Ningún archivo se repite entre secciones. Nunca se amplía: el mayor ancho emitido es ≤ al recorte de la fuente.

## Videos (loops)

| id | sección | ref | tramo (s) | loop | salida | dur. | WebM VP9 | MP4 H.264 | póster AVIF/WebP/JPG | presupuesto | costura* |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `portada-celular` | 1 Portada · celular | V021 | 0.6–3.3 | boomerang | 720x1280 | 5.37 s | 1.358 | 1.331 | 33 / 43 / 96 | ≤1380 pasa | 19.41 (21.2) |
| `portada-escritorio` | 1 Portada · escritorio | V031 | 4.3–10.4 | crossfade | 1278x720 | 5.5 s | 2.374 | 1.999 | 39 / 51 / 106 | ≤2500 pasa | 13.2 (10.37) |
| `lugar-cintas` | 2 El lugar | V009 | 0.3–3.3 | boomerang | 600x750 | 5.93 s | 1.153 | 1.159 | 30 / 41 / 73 | ≤1200 pasa | 14.07 (18.61) |
| `tragos-humo` | 3 Tragos | V038 | 8.6–12.1 + 12.2–16.7 | crossfade | 720x900 | 7.4 s | 551 | 847 | 13 / 18 / 48 | ≤1200 pasa | 4.33 (2.01) |
| `comida-cazuela` | 4 Comida | V052 | 0.0–3.95 | boomerang | 720x900 | 7.8 s | 1.168 | 1.093 | 25 / 33 / 73 | ≤1200 pasa | 13.85 (12.69) |
| `donde-letrero` | 9 Dónde | V031 | 0.7–4.15 | boomerang | 1278x720 | 6.87 s | 1.144 | 1.174 | 9 / 17 / 39 | ≤1200 pasa | 1.54 (15.8) |

*Costura: diferencia media de luminancia (0–255) entre el último y el primer frame del loop; entre paréntesis, la de dos frames consecutivos del mismo loop. Si la primera es del orden de la segunda, el salto no se nota.

## Primer pantallazo

| Pantalla | Qué carga | Peso | Tope |
|---|---|---|---|
| Celular (<900 px) | póster AVIF 33 + video 720x1280 (el mayor de WebM/MP4: 1.358) | 1.391 KB | video ≤ 1.843 · pantallazo ≤ 1.536 KB: pasa |
| Escritorio (≥900 px) | póster AVIF 39 + video 1278x720 (2.374) | 2.413 KB | video ≤ 2.560 KB: pasa |

Fuentes, CSS, logo y JS van aparte (los cuenta el build). El `<video>` lleva `preload="auto"` solo en la variante que corresponde al ancho (`<source media>` no aplica a video en todos los navegadores: el build debe elegir la fuente por JS mínimo o servir dos `<video>` con `display:none` + `preload="none"` en el oculto).

## Imágenes

| id | sección | rincón / evento / @ / ítem | ref · post | fuente | recorte | anchos | celular AVIF¹ | mayor AVIF | mayor WebP | crédito | estado |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `lugar-barra` [a] | 2 El lugar | barra | P093 · IG-079 | 1440x1701 | 4:5 | 480/720/960/1280/1361 | 720: 56 | 1361: 121 | 187 | @almud_bar | ok |
| `lugar-salon` [d] | 2 El lugar | salón | P076 · IG-094 | 1335x890 | 1335:890 | 480/720/960/1280 | 720: 28 | 1280: 56 | 79 | @almud_bar | ok |
| `lugar-salon` [m] | 2 El lugar | salón | P076 · IG-094 | 1335x890 | 4:5 | 480/712 | 712: 31 | 712: 31 | 44 | @almud_bar | ok |
| `lugar-sillones` [a] | 2 El lugar | sillones | P114 · IG-075 | 1440x1800 | 1440:1800 | 480/720/960/1280/1440 | 720: 25 | 1440: 56 | 80 | @estudiouno.prod | ok |
| `lugar-sillones` [s] | 2 El lugar | sillones | P114 · IG-075 | 1440x1800 | 1:1 | 480/720/960/1280/1440 | 720: 22 | 1440: 48 | 68 | @estudiouno.prod | ok |
| `lugar-terraza-techada` [a] | 2 El lugar | terraza techada | P189 · IG-050 | 1440x1919 | 4:5 | 480/720/960/1280/1440 | 720: 80 | 1440: 195 | 327 | @estudiouno.prod | ok |
| `lugar-terraza-techada` [d] | 2 El lugar | terraza techada | P189 · IG-050 | 1440x1919 | 16:9 | 480/720/960/1280/1440 | 720: 41 | 1440: 101 | 173 | @estudiouno.prod | ok |
| `lugar-terraza-abierta` [a] | 2 El lugar | terraza abierta | P039 · IG-144 | 1332x1665 | 4:5 | 480/720/960/1280 | 720: 55 | 1280: 116 | 168 | @catarsis.fotografia | ok |
| `lugar-lampara-pinzas` [a] | 2 El lugar | luces | V014-cover · IG-103 | 3216x5712 | 4:5 | 480/720/960/1080 | 720: 57 | 1080: 107 | 180 | @rober.patagonico | ok |
| `lugar-ojo-piojo` [a] | 2 El lugar | mural Ojo Piojo | V005-cover · IG-118 | 902x902 | 1:1 | 480/720/902 | 720: 29 | 902: 39 | 54 | @almud_bar | ok |
| `lugar-ojo-piojo` [m] | 2 El lugar | mural Ojo Piojo | V005-cover · IG-118 | 902x902 | 4:5 | 480/720 | 720: 32 | 720: 32 | 46 | @almud_bar | ok |
| `lugar-cuadros` [a] | 2 El lugar | cuadros | P012 · IG-171 | 853x568 | 853:568 | 480/720/853 | 720: 28 | 853: 35 | 53 | @almud_bar | ok |
| `tragos-splash` [a] | 3 Tragos |  | P297 · IG-023 | 3177x3177 | 4:5 | 480/720/960/1280/1440/1920 | 720: 31 | 1920: 134 | 198 | @almud_bar | ok |
| `tragos-splash` [s] | 3 Tragos |  | P297 · IG-023 | 3177x3177 | 1:1 | 480/720/960/1280/1440/1920 | 720: 26 | 1920: 106 | 158 | @almud_bar | ok |
| `tragos-sours` [a] | 3 Tragos |  | P086 · IG-079 | 1440x1708 | 4:5 | 480/720/960/1280/1366 | 720: 31 | 1366: 85 | 109 | @almud_bar | ok |
| `tragos-copa-tallada` [a] | 3 Tragos |  | P097 · IG-079 | 1440x1708 | 4:5 | 480/720/960/1280/1366 | 720: 22 | 1366: 79 | 97 | @almud_bar | ok |
| `tragos-old-fashioned` [a] | 3 Tragos |  | P003 · IG-178 | 1280x1600 | 4:5 | 480/720/960/1280 | 720: 17 | 1280: 40 | 52 | @tamillanquileo | ok |
| `comida-pizza` [a] | 4 Comida |  | P036 · IG-147 | 1332x1665 | 4:5 | 480/720/960/1280 | 720: 32 | 1280: 87 | 112 | @catarsis.fotografia | ok |
| `comida-ceviche` [a] | 4 Comida |  | P298 · IG-022 | 3024x4032 | 4:5 | 480/720/960/1280/1440/1920 | 720: 49 | 1920: 183 | 210 | @almud_bar | ok |
| `comida-hamburguesa` [a] | 4 Comida |  | P305 · IG-022 | 3024x4032 | 4:5 | 480/720/960/1280/1440/1920 | 720: 46 | 1920: 142 | 192 | @almud_bar | ok |
| `con-quien-amigas` [a] | 5 Con quién |  | P254 · IG-031 | 1440x1920 | 4:5 | 480/720/960/1280/1440 | 720: 62 | 1440: 162 | 253 | @almud_bar | ok |
| `con-quien-barra` [a] | 5 Con quién |  | P031 · IG-152 | 1332x1665 | 4:5 | 480/720/960/1280 | 720: 27 | 1280: 69 | 90 | @almud_bar | ok |
| `con-quien-risa` [a] | 5 Con quién |  | P041 · IG-142 | 1332x1665 | 4:5 | 480/720/960/1280 | 720: 23 | 1280: 59 | 75 | @almud_bar | ok |
| `con-quien-amigos` [a] | 5 Con quién |  | P259 · IG-026 | 3276x2621 | 3276:2621 | 480/720/960/1280/1440 | 720: 38 | 1440: 169 | 293 | @almud_bar | ok |
| `con-quien-solo` [a] | 5 Con quién |  | P194 · IG-050 | 1440x1919 | 4:5 | 480/720/960/1280/1440 | 720: 44 | 1440: 110 | 176 | @estudiouno.prod | ok |
| `con-quien-brindis` [a] | 5 Con quién |  | P182 · IG-050 | 1440x1920 | 4:5 | 480/720/960/1280/1440 | 720: 57 | 1440: 132 | 214 | @estudiouno.prod | ok |
| `eventos-12-anos` [a] | 6 Eventos | 12 años | P348 · IG-009 | 3072x4096 | 4:5 | 480/720/960/1280/1440/1920 | 720: 70 | 1920: 297 | 431 | @isosur.prod | ok |
| `eventos-jaloguin` [a] | 6 Eventos | Jalogüín | P234 · IG-038 | 1440x1919 | 4:5 | 480/720/960/1280/1440 | 720: 36 | 1440: 85 | 133 | @almud_bar | ok |
| `eventos-fondita` [a] | 6 Eventos | Fondita | P090 · IG-079 | 1440x1708 | 4:5 | 480/720/960/1280/1366 | 720: 61 | 1366: 136 | 206 | @almud_bar | ok |
| `eventos-14f` [a] | 6 Eventos | 14F | V006-cover · IG-117 | 2268x4032 | 4:5 | 480/720/960/1080 | 720: 40 | 1080: 74 | 98 | @almud_bar | ok |
| `eventos-negroni-week` [a] | 6 Eventos | Negroni Week | P226 · IG-042 | 1423x1897 | 4:5 | 480/720/960/1280/1423 | 720: 26 | 1423: 84 | 112 | @almud_bar | ok |
| `eventos-primavera` [a] | 6 Eventos | Primavera | P102 · IG-075 | 1440x1800 | 4:5 | 480/720/960/1280/1440 | 720: 61 | 1440: 132 | 201 | @estudiouno.prod | ok |
| `eventos-10-anos` [a] | 6 Eventos | 10 años | P073 · IG-100 | 1334x1667 | 4:5 | 480/720/960/1280 | 720: 53 | 1280: 107 | 167 | @estudiouno.prod | ok (opcional) |
| `equipo-milagros` [a] | 7 Equipo | @milagroosjm | P391 · IG-001 | 1067x1067 | 4:5 | 480/720/854 | 720: 25 | 854: 31 | 44 | @almud_bar | ok |
| `equipo-javier` [a] | 7 Equipo | @javier.agmc | P392 · IG-001 | 3072x4096 | 4:5 | 480/720/960/1280/1440 | 720: 43 | 1440: 107 | 164 | @almud_bar | ok |
| `equipo-eduardo` [a] | 7 Equipo | @eduu.ardoo | P393 · IG-001 | 3072x4096 | 4:5 | 480/720/960/1280/1440 | 720: 40 | 1440: 109 | 188 | @almud_bar | ok |
| `equipo-liz` [a] | 7 Equipo | @lizzearellano | P078 · IG-088 | 1334x1667 | 4:5 | 480/720/960/1280 | 720: 22 | 1280: 45 | 63 | @almud_bar | ok |
| `equipo-pablete` [a] | 7 Equipo | @pablete_bartender_ | P251 · IG-034 | 1440x1920 | 4:5 | 480/720/960/1280/1440 | 720: 33 | 1440: 74 | 109 | @almud_bar | ok |
| `equipo-elymar` [a] | 7 Equipo | @elymar_bocarejo | P396 · IG-001 | 1128x1504 | 4:5 | 480/720/960/1128 | 720: 34 | 1128: 68 | 91 | @almud_bar | por-confirmar |
| `equipo-duo` [a] | 7 Equipo | @milagroosjm @lizzearellano | P333 · IG-014 | 3219x4096 | 4:5 | 480/720/960/1280/1440/1920 | 720: 37 | 1920: 132 | 198 | @almud_bar | ok |
| `equipo-duo` [d] | 7 Equipo | @milagroosjm @lizzearellano | P333 · IG-014 | 3219x4096 | 3:2 | 480/720/960/1280/1440/1920 | 720: 20 | 1920: 69 | 101 | @almud_bar | ok |
| `equipo-grupo` [a] | 7 Equipo |  | P077 · IG-091 | 1207x805 | 1207:805 | 480/720/960/1207 | 720: 43 | 1207: 82 | 133 | @almud_bar | por-confirmar |
| `donde-puerta` [a] | 9 Dónde |  | P199 · IG-050 | 1440x1919 | 4:5 | 480/720/960/1280/1440 | 720: 42 | 1440: 181 | 358 | @estudiouno.prod | ok |
| `carta-olvidar` [a] | Carta destacada | Cómo te voy a olvidar | V057-cover · IG-002 | 720x720 | 1:1 | 360/480/720 | 720: 25 | 720: 25 | 28 | @almud_bar | ok |
| `carta-saguer` [a] | Carta destacada | Sagüer on Faia | V030-cover · IG-063 | 3794x6738 | 4:5 | 360/480/720/960 | 720: 31 | 960: 46 | 69 | @almud_bar | ok |
| `carta-sangria` [a] | Carta destacada | Sangría Foreva! | P228 · IG-039 | 1440x1814 | 4:5 | 360/480/720/960 | 720: 24 | 960: 33 | 50 | @almud_bar | ok |
| `carta-coquette` [a] | Carta destacada | A veces me pongo Coquette | P074 · IG-096 | 1067x1067 | 4:5 | 360/480/720/854 | 720: 16 | 854: 20 | 27 | @almud_bar | ok |
| `carta-moto` [a] | Carta destacada | La moto chantá | P336 · IG-011 | 1600x2000 | 4:5 | 360/480/720/960 | 720: 16 | 960: 23 | 33 | @almud_bar | ok |
| `carta-tukulito` [a] | Carta destacada | Tukulito Sakayama | P044 · IG-139 | 852x852 | 1:1 | 360/480/720/852 | 720: 29 | 852: 35 | 52 | @almud_bar | ok |
| `carta-contuti` [a] | Carta destacada | Con tuti si no pa qué! | P158 · IG-066 | 1440x1800 | 4:5 | 360/480/720/960 | 720: 36 | 960: 50 | 75 | @almud_bar | ok |
| `carta-camaron` [a] | Carta destacada | Camarón que se duerme | P099 · IG-077 | 1334x1667 | 4:5 | 360/480/720/960 | 720: 28 | 960: 40 | 62 | @almud_bar | ok |

¹ Celular = AVIF del menor ancho ≥ 720 px (tarjeta de ~360 css a DPR 2). Total: 458 archivos de imagen, 32.914 KB en disco.

## Alt (ES / EN)

**1 Portada**
- `portada-celular`: La cámara recorre el muro rosa de botellas iluminadas y el cartelito ALMUD BAR. / *The camera glides along the glowing pink bottle wall and the little ALMUD BAR sign.*
- `portada-escritorio`: El techo de cintas de colores, el mural de ojos y las lámparas de pinzas encendidas, uno tras otro. / *The coloured-ribbon ceiling, the eye mural and the glowing clothespin lamps, one after another.*

**2 El lugar**
- `lugar-cintas`: Paneo lento por el techo de miles de cintas de colores con luces cálidas. / *A slow pan across the ceiling of thousands of coloured ribbons and warm lights.*
- `lugar-barra`: La barra curva de madera con frente de baldosa, el muro rojo de botellas, banderines y lámparas tejidas. / *The curved wooden bar with a tiled front, the red bottle wall, bunting and woven lamps.*
- `lugar-salon`: El salón interior de noche: mesas de madera, luz cálida y gente conversando tras una mampara de vidrio. / *The indoor room at night: wooden tables, warm light and people talking behind a glass partition.*
- `lugar-sillones`: Una mujer ríe y aplaude en el rincón de sillones, con cojines estampados y baldosa hidráulica. / *A woman laughs and claps in the lounge corner, with patterned cushions and encaustic tiles.*
- `lugar-terraza-techada`: La terraza techada llena de gente bajo el techo de miles de cintas de colores, con estufas encendidas. / *The covered terrace packed with people under a ceiling of thousands of coloured ribbons, heaters glowing.*
- `lugar-terraza-abierta`: La terraza abierta de noche: ripio, árboles, guirnaldas de ampolletas y mesas de picnic llenas. / *The open terrace at night: gravel, trees, string lights and full picnic tables.*
- `lugar-lampara-pinzas`: Lámparas hechas con pinzas de ropa de madera, encendidas sobre la barra. / *Lamps made from wooden clothespins, glowing above the bar.*
- `lugar-ojo-piojo`: Mural de cientos de ojos fotografiados, con una planta desenfocada delante. / *A mural of hundreds of photographed eyes, with an out-of-focus plant in front.*
- `lugar-cuadros`: Gente conversando en la barra con el muro de marcos de colores al fondo. / *People chatting at the bar, with the wall of colourful frames in the background.*

**3 Tragos**
- `tragos-humo`: Una burbuja de humo crece sobre una copa roja y una mano la revienta: el humo se escapa sobre la barra. / *A smoke bubble swells over a red coupe and a hand pops it, smoke spilling across the bar.*
- `tragos-splash`: Un cóctel rojo salpica fuera de una copa coupé sobre la barra de madera, con botellas desenfocadas detrás. / *A red cocktail splashes out of a coupe on the wooden bar, bottles blurred behind.*
- `tragos-sours`: Tres copas con espuma y gypsophila seca sobre la barra. / *Three foamy coupes garnished with dried baby's breath on the bar.*
- `tragos-copa-tallada`: Copa tallada con un trago naranja y espuma, frente al muro rosa de botellas desenfocado. / *A cut-glass coupe with an orange drink and foam against the blurred pink bottle wall.*
- `tragos-old-fashioned`: Un trago ámbar con hielo y una frutilla sobre el posavasos de Almud, en madera cálida. / *An amber drink on ice with a strawberry on an Almud coaster, on warm wood.*

**4 Comida**
- `comida-cazuela`: Cazuela cremosa de mariscos burbujeando en greda negra, con cilantro picado. / *A creamy seafood stew bubbling in a black clay pot, with chopped coriander.*
- `comida-pizza`: Una garzona sonríe a la cámara mientras sostiene una pizza recién salida. / *A server smiles at the camera holding a freshly baked pizza.*
- `comida-ceviche`: Ceviche de atún con palta, pimentón y cilantro en una greda negra, con pan tostado al lado. / *Tuna ceviche with avocado, pepper and coriander in a black clay bowl, with toasted bread.*
- `comida-hamburguesa`: Hamburguesa en pan con sésamo, con cebolla caramelizada, hojas verdes y queso derretido. / *A sesame-bun burger with caramelised onion, greens and melted cheese.*

**5 Con quién**
- `con-quien-amigas`: Dos amigas brindan con sus tragos frente al muro rosa de botellas iluminadas. / *Two friends toast with their drinks in front of the glowing pink bottle wall.*
- `con-quien-barra`: Un grupo de amigas ríe y brinda en la barra con tragos de colores. / *A group of friends laughs and toasts at the bar with colourful drinks.*
- `con-quien-risa`: Una mujer ríe a carcajadas en la mesa, frente a un muro de cintas verticales de colores. / *A woman bursts out laughing at her table, in front of a wall of vertical coloured ribbons.*
- `con-quien-amigos`: Tres amigos abrazados sonríen a la cámara; una de ellas sostiene una brocheta. / *Three friends hug and smile at the camera; one holds a skewer.*
- `con-quien-solo`: Gente acodada en la barra bajo una lámpara de flecos dorados mientras el bartender prepara tragos. / *People leaning on the bar under a golden fringe lamp while the bartender mixes drinks.*
- `con-quien-brindis`: Una mesa brinda bajo el techo de cintas de colores, junto a una estufa de pilar encendida. / *A table toasts under the coloured-ribbon ceiling, next to a lit patio heater.*

**6 Eventos**
- `eventos-12-anos`: La celebración de los 12 años de Almud: la terraza repleta bajo los banderines, vista desde arriba. / *Almud's 12th anniversary: the terrace packed under the bunting, seen from above.*
- `eventos-jaloguin`: Jalogüín en Almud: una catrina con corona de flores levanta un trago rojo bajo la lámpara de flecos. / *Halloween at Almud: a Catrina with a flower crown raises a red drink under the fringe lamp.*
- `eventos-fondita`: La fondita de Almud: faroles de papel azul y naranja colgando entre las cintas, sobre la terraza llena. / *Almud's Fiestas Patrias "fondita": blue and orange paper lanterns hanging among the ribbons over the busy terrace.*
- `eventos-14f`: 14 de febrero en Almud: manos con uñas rosadas sostienen un trago rosa con una mariposa de papel. / *Valentine's Day at Almud: hands with pink nails hold a pink cocktail topped with a paper butterfly.*
- `eventos-negroni-week`: Un bartender revuelve un negroni con hielo sobre la barra, con luz ámbar. / *A bartender stirs a negroni over ice on the bar, in amber light.*
- `eventos-primavera`: Bienvenida a la primavera en Almud: mesas llenas bajo un techo de banderines de papel de colores. / *Welcoming spring at Almud: busy tables under a ceiling of colourful paper bunting.*
- `eventos-10-anos`: Los 10 años de Almud: un gran número 10 hecho de flores bajo el techo de banderines. / *Almud's 10th anniversary: a giant number 10 made of flowers under the bunting.*

**7 Equipo**
- `equipo-milagros`: Una garzona del equipo sonríe mientras atiende una mesa, con abanicos de papel de colores detrás. / *A member of the floor team smiles while serving a table, colourful paper fans behind her.*
- `equipo-javier`: Un bartender del equipo sirve concentrado frente al muro rojo de botellas y el cartel ALMUD. / *A bartender from the team pours, focused, in front of the red bottle wall and the ALMUD sign.*
- `equipo-eduardo`: Un garzón del equipo, tatuado, con camisa estampada y gorro, lleva un plato al salón. / *A tattooed server from the team, in a patterned shirt and cap, carries a plate to the room.*
- `equipo-liz`: Una garzona del equipo, rubia, sonríe mientras deja un trago en la mesa. / *A blonde server from the team smiles as she sets a drink on the table.*
- `equipo-pablete`: Un bartender del equipo, con barba, ríe mientras bate la coctelera frente al muro rosa. / *A bearded bartender from the team laughs as he shakes a cocktail by the pink wall.*
- `equipo-elymar`: Una garzona del equipo sonríe frente al muro rosa, con delantal de Almud. / *A server from the team smiles by the pink wall, wearing an Almud apron.*
- `equipo-duo`: Dos garzonas del equipo sonríen con corbata, jockey y delantal. / *Two servers from the team smile in ties, caps and aprons.*
- `equipo-grupo`: El equipo de Almud reunido tras la barra, frente al muro rosa de botellas. / *The Almud team gathered behind the bar, in front of the pink bottle wall.*

**9 Dónde**
- `donde-letrero`: El letrero luminoso ALMUD BAR y la cámara que baja hasta la puerta de vidrio y madera de la entrada. / *The illuminated ALMUD BAR sign, the camera tilting down to the glass-and-wood entrance door.*
- `donde-puerta`: En la puerta de madera de Almud, una mujer con megáfono y polera «Te espero en la cuneta». / *At Almud's wooden door, a woman with a megaphone wears a "Te espero en la cuneta" T-shirt.*

**Carta destacada**
- `carta-olvidar`: Vino tinto tiñe un vaso con una gran esfera de hielo y una lámina de manzana seca. / *Red wine streams into a glass with a large ice sphere and a dried apple slice.*
- `carta-saguer`: Un soplete ahúma un trago ámbar sobre un posavasos de madera. / *A torch smokes an amber drink on a wooden coaster.*
- `carta-sangria`: Copa tallada con sangría roja, hielo y flores secas sobre la barra. / *A cut-glass goblet of red sangria with ice and dried flowers on the bar.*
- `carta-coquette`: Una clienta sonriente recibe un trago rosado y cremoso con flores. / *A smiling guest receives a creamy pink drink topped with flowers.*
- `carta-moto`: Mocktail naranja de mango y maracuyá con borde de sal y una rodaja de pepino. / *An orange mango-passion fruit mocktail with a salted rim and a cucumber slice.*
- `carta-tukulito`: Tataki de atún sellado en láminas con pan tostado y salsa, en plato de vidrio. / *Sliced seared tuna tataki with toasted bread and sauce on a glass plate.*
- `carta-contuti`: Tabla para compartir vista desde arriba: quesos, jamón, aceitunas, frutos secos y naranja. / *A sharing board from above: cheeses, ham, olives, nuts and orange.*
- `carta-camaron`: Cazuela negra con camarones y champiñones en salsa cremosa. / *A black clay dish of prawns and mushrooms in a creamy sauce.*

## Notas de selección

- `portada-celular`: Celular <900 px. Paneo continuo 0,6–3,3 s (antes del corte de 5,19 s; sin el guest bartender), pasa por el cartelito ALMUD BAR. Boomerang: el paneo vuelve, no salta. Fuente 1080p; a 1080 y 900 px el paneo de botellas no cabe en 1,38 MB con calidad digna (1080: 3,5 MB a CRF 28), así que sale al mayor ancho que cabe. Presupuesto 1,38 MB para que el primer pantallazo quede ≤1,5 MB con póster.
- `portada-escritorio`: ≥900 px. Tramo 4,3–10,4 s (cintas → ojos → lámparas), corta antes del subtítulo de 10,5 s; crossfade 0,6 s lámparas→cintas. 1278x720 nativo: el CSS lo estira (≈1,1x en 1440, 1,5x en 1920). Mitigar con overlay noche; alternativa: V021 vertical a alto completo en columna.
- `lugar-cintas`: Un solo plano de 7,1 s; boomerang de 3 s (6 s). Textura de cintas muy cara de comprimir: 720 px si cabe en 1,2 MB con CRF ≤28, si no 600 px.
- `tragos-humo`: Dos planos (burbuja creciendo / mano que la revienta, corte propio del reel en 12,16 s) y crossfade 0,6 s del humo a la copa. Es el trago «Aquí te las traigo Peter»: la carta enlaza a este loop (no se repite la portada del reel).
- `comida-cazuela`: Plano único de 4 s con acercamiento lento: boomerang.
- `donde-letrero`: Un plano continuo 0,7–4,15 s (letrero → fachada → puerta), antes del corte de 4,23 s. Boomerang. Es la única vista de fachada propia. No se repite con la portada de escritorio (tramo 4,3–10,4).
- `lugar-sillones`: Única foto nítida del rincón (V014 9,3 s es un frame 720p casi negro y con cortes cada 0,5 s: no da loop). "a" sin recorte deja ver el sillón y los cojines estampados abajo a la izquierda; "s" 1:1 baja el encuadre para dar más sillón.
- `lugar-terraza-techada`: Favorita n.º 1 de Carmen. Ya no es la portada (la portada es video), así que encabeza El lugar. 1440 px: nunca a sangre en 1920.
- `lugar-lampara-pinzas`: Portada de reel sobremuestreada (3216x5712 desde un original menor): tope 1080 px.
- `lugar-ojo-piojo`: Foto que Carmen nombra para Ojo Piojo (IG-118). 902 px: solo tarjeta, nunca a sangre.
- `lugar-cuadros`: Única foto propia del muro de cuadros (853x568): solo mosaico ≤600 px css. Lleva algo de luz azul.
- `tragos-old-fashioned`: Carmen lo llama old fashioned; IG-178 no lo nombra: sin nombre de trago.
- `comida-pizza`: No se presenta como equipo (no está en IG-001).
- `comida-ceviche`: Luz de día (la única de comida en alta). Parece «Todo que ver!» pero el post no lo nombra: sin nombre.
- `con-quien-amigos`: 5:4 sin recorte: un 4:5 cortaba la cara de la derecha. Lleva flash (va en mosaico, no a sangre).
- `eventos-12-anos`: Violeta permitido solo en Eventos.
- `eventos-14f`: Portada del reel 14F (IG-117), sobremuestreada: tope 1080 px. El afiche IG-116 tiene texto: descartado.
- `eventos-negroni-week`: HUECO: el post de Negroni Week (IG-005) solo tiene afiches con texto. Esta es un negroni de la casa (IG-042), no del evento: el alt no dice que sea la Negroni Week.
- `eventos-10-anos`: Extra opcional: la favorita de Carmen "de evento".
- `equipo-liz`: Se prefiere IG-088 (luz cálida) al retrato violeta de IG-001 #4.
- `equipo-pablete`: IG-001 #5 es un repost de 1067 px (original P109, 2024); IG-034 (feb-2026) es más nuevo y de 1440 px.
- `equipo-elymar`: Su única foto lleva tiara y alas (disfraz). Carmen no acepta disfraces fuera de Eventos: confirmar con ella o pedir otro retrato. El recorte 4:5 no elimina la tiara.
- `equipo-duo`: Equipo actual confirmado por IG-014 y IG-001; foto grupal segura (alta resolución).
- `equipo-grupo`: «Estuvimos todo el equipo juntos» (10 años, ago-2024, 1207 px). Puede incluir exempleados: Carmen confirma; si no, el grupo es equipo-duo.

## Descartes

- V056: Reel de creadores externos (IG-007) con texto encima: contenido de terceros.
- V041/V042: Banda Isleños: terceros.
- P100/P111/P115/P116: Músicos invitados (terceros).
- P283/P294: Rucalaf: terceros.
- P027: Despedida de un exbartender.
- P379/P380, P064: Afiches con texto (Negroni Week, 14F).
- P229/P242/P136/P347: Disfraces y tortas fuera de Eventos; para Jalogüín se elige P234.
- V021 5,2–12 s: Guest bartender (tercero) y cortes rápidos.
- V031 >10,5 s: Subtítulos quemados.
- P362: Mismo bartender y misma sesión que P392 (IG-001), que va en Equipo: no se repite.
- P091: Cazuela: ya está el loop V052 y el ítem Camarón que se duerme; no se repite el motivo.
- P157: Foto grupal de dic-2024 al aire libre: muchos posibles exempleados; se prefiere la de la barra (C-bY0mLNYRz) por confirmar y el dúo P333.
- P394 (IG-001 #4): Retrato de Liz en luz violeta; se usa IG-088 en luz cálida.
- P109 / P395: Pablete 2024 (repost en IG-001 #5); se usa IG-034 de 2026.
- V014 9,3 s: Sillones casi negro, 720p y cortes cada 0,5 s: sin loop posible.
