# v4 · Fase 2 · Videos: 8–10 s, siempre hacia adelante, con fundido

Regla del cliente: cada loop dura de 8 a 10 s, avanza siempre (nunca boomerang ni reverse), va a velocidad real y cierra con un fundido de 0,8–1,0 s del final al inicio. Son mudos, con autoplay, loop y playsinline, y nunca se pausan: el JS solo les asigna la fuente cuando están cerca de la pantalla.

Generado con `python3 tools/media_v4.py` desde `tools/media_v4.json`. Salida: `assets/v4/video/` y `assets/v4/media-video.json`. Hoja: `_plan/v4/fase2/hoja-loops.jpg`. Hojas de contacto de los reels (un cuadro cada 0,5 s): `_plan/v4/fase2/hojas/`. Duración del loop = tramo − fundido. KB = 1024 bytes.

| id | ref | archivo | tramo (s) | loop | fundido | salida | MP4 KB | WebM KB | póster webp KB | costura* | por qué ese tramo | post que lo respalda |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `portada-celular` | V017 | C9lH7qfSTfo_00.mp4 | 32,9–42,9 | 9,0 s | 1,0 s | 720×1280 | 1.662 | 1.595 | 23 | 8,2 (11,8) | Un bartender bate frente al muro rosa, se reparten shots y una clienta se ríe en la barra: oficio, gente y color en 9 s. Es el muro rosa en su mejor luz (cinematográfico, nítido). Sin DJ (32,2 s) ni techo (43,5 s) | IG-098, 18-jul-2024, 10 años: «Esto es una partecita de lo chanchi que lo pasamos en nuestro cumple feliz número 10!» (156 ♥) |
| `portada-escritorio` | V031 | DFWLrRxyvVB_00.mp4 | 0,4–10,45 | 9,07 s | 1,0 s | 1278×720 | 2.461 | 2.423 | 17 | 4,9 (9,4) | El único horizontal propio. Usa toda la apertura sin subtítulos: letrero ALMUD BAR → puerta → techo de cintas → mural de ojos → lámparas de pinzas. Termina antes del subtítulo de 10,5 s. El fundido va de las lámparas al letrero | IG-061, 27-ene-2025: «Hicimos este video pa contar un poquito de nuestro Almudcito!», realizado por @estudiouno.prod (266 ♥) |
| `lugar-cintas` | V007 | C3tFEcvJ80x_00.mp4 | 21,27–31,4 | 9,16 s | 1,0 s | 720×900 | 1.367 | 1.176 | 38 | 27,2 (6,3)** | Un solo plano caminando bajo el techo de cintas de la terraza llena al atardecer, que sale al patio con guirnaldas; termina en una mesa de amigas y una clienta riendo. El reel de las cintas que se usaba antes (V009) dura 7,1 s y no alcanza | IG-115, 23-feb-2024: «una noche beia llena de amistad, abrazos…» (164 ♥). Las cintas: IG-111 «Somos inquietos y nos gusta el colorssss!» |
| `tragos-humo` | V038 | DOO7fgniNI6_00.mp4 | 7,0–16,75 | 8,68 s | 1,0 s | 720×900 | 953 | 618 | 19 | 3,4 (2,0) | La burbuja de humo crece sobre la copa (corte propio del reel en 12,16 s) y una mano la revienta. Es el trago «Aquí te las traigo Peter», así que este video cubre también el slot `tragos-peter` | IG-044, 5-sep-2025: «Aquí te las traigo Peter! Hermoso y ricardo» |
| `tragos-coctelera` (nuevo) | V032 | DGLxTmGJ3ZV_00.mp4 | 0,6–10,15 | 8,67 s | 0,9 s | 720×900 | 1.291 | 1.172 | 27 | 3,5 (11,2) | Girasoles → barra roja → bartender con delantal ALMUD bate y sirve (4,7–8,4 s) → techo de cintas. Cortes lentos de ellos; las marcas quedan de fondo, desenfocadas | IG-059, 17-feb-2025: «una jornada de fotos & videitos entre nosotros no más» |
| `comida-cazuela` | V049 | DY0AUvhlHjI_12.mp4 | 0,2–9,9 | 8,71 s | 1,0 s | 720×900 | 1.309 | 1.149 | 23 | 12,4 (5,8) | Cocina en acción: un solo plano del sartén salteando sobre el fuego. Las cazuelas propias (V052 de 4,1 s, V044 de 6,4 s, V040 de 8,3 s) no llegan a 8 s con el fundido | IG-022, 26-may-2026: «tenemos una cocina sencilla pero más que sabrosona!» (el mismo título de la sección Comida) |
| `quien-brindis` (nuevo) | V028 | DEYU6RjyjoC_00.mp4 | 0,25–9,85 | 8,6 s | 1,0 s | 720×900 | 1.364 | 1.165 | 45 | 14,4 (9,1) | Un solo plano: amigos chocan copas en una mesa de la terraza bajo el bambú y siguen conversando. El fundido une dos cuadros casi iguales | IG-065, 3-ene-2025: «celebrar la vida, la amistad, el amors y el buen clima» |
| `donde-terraza` (reemplaza a `donde-letrero`) | V007 | C3tFEcvJ80x_00.mp4 | 0,0–8,92 | 8,14 s | 0,8 s | 720×720 | 1.350 | 1.195 | 52 | 17,9 (29,1) | El patio de tarde con Castro detrás → mesas → trago rosado → terraza techada de cintas. El letrero solo existe en V031 (0–4,2 s) y esos 10,4 s sin subtítulos los usa enteros la portada de escritorio: repetirlos abajo mostraría dos veces el mismo plano | IG-115, 23-feb-2024 (164 ♥) |

\* Costura: diferencia media de luminancia (0–255) entre el último y el primer cuadro del loop; entre paréntesis, la de dos cuadros consecutivos del mismo loop. Las 8 se revisaron también a ojo, cuadro a cuadro durante el fundido: ninguna salta.
\*\* En `lugar-cintas` la costura mide alto porque el plano camina rápido (con desenfoque de movimiento) justo donde empieza; a ojo el fundido es continuo.

Presupuestos: fuera de la portada, ≤ 1.200 KB WebM y ≤ 1.400 KB MP4 a 720 px de ancho (cumplen los 6). Portada de celular: ≤ 1.600 KB WebM (1.595), póster de 23 KB. Portada de escritorio: ≤ 2.500 KB.

## Slots pedidos que no se crean
- `tragos-peter`: el Peter es el trago del humo (`tragos-humo`); un segundo video sería el mismo reel.
- `lugar-terraza`: la terraza llena ya está en `lugar-cintas` (atardecer) y en `donde-terraza` (tarde). No hay otro plano propio de 8 s sin terceros: V042/V041 son de la banda Isleños, V043 es la noche Rucalaf y V010 dura 6,6 s.

## Descartes de esta revisión
- V021 (portada anterior, 1080p): el muro rosa dura 5 s y después viene un montaje de fotos que cambia cada 0,2 s (con DJ y tecladista), muy brusco para un loop.
- V022 (C-6PtKKJ7uc): visita de la embajadora de Flor de Caña (otra marca).
- V026 (DBPUjQfyBTx) y V025 (DBJy4NbJ-h9): guitarristas y DJ invitados, y etiquetas de botellas en primer plano.
- V001 y V002 (dic-2022 y ene-2023): época de @vlanbartender.
- V036, V037 y V055 (11 y 12 años): planos de menos de 1 s y luz violeta; V033 (desfile) y V039 (Jalogüín) son eventos o disfraces.
- V009 (C5WAi8PLHni, 7,1 s) y V052 (DZgLFzooZB_, 4,1 s): demasiado cortos.

## Dónde van en /nueva/
- Portada: `portada-celular` (vertical) y `portada-escritorio` (horizontal), igual que antes.
- El lugar: `lugar-cintas` junto al título.
- Tragos: `tragos-coctelera` es una cuarta pieza de la banda de ambiente, sin parallax: en celular va a todo el ancho y en escritorio debajo de la salpicadura. `tragos-humo` sigue en el Peter.
- Comida: `comida-cazuela`, en el mismo lugar.
- Con quién: `quien-brindis` encabeza la tercera columna; en celular se ve solo el video, a todo el ancho.
- Cuándo y dónde: `donde-terraza` en lugar del letrero.
