# v4 · Fase 2 · Videos: 8–10 s, siempre hacia adelante, con fundido

Regla del cliente: cada loop dura de 8 a 10 s, avanza siempre (nunca boomerang ni reverse), va a velocidad real y cierra con un fundido de 0,8–1,0 s del final al inicio. Son mudos, con autoplay, loop y playsinline, y nunca se pausan: el JS solo les asigna la fuente cuando están cerca de la pantalla.
Principio del cliente (ronda 2): **«la mejor manera de vender un bar es mostrar que siempre está lleno»**. Manda la multitud; el barman y los dueños no son el centro.

Generado con `python3 tools/media_v4.py` desde `tools/media_v4.json`. Salida: `assets/v4/video/` y `assets/v4/media-video.json`.
Hojas: `_plan/v4/fase2/hoja-loops.jpg` (ronda 1) y `_plan/v4/fase2/hoja-loops-2.jpg` (ronda 2: solo los nuevos y el movido). Hojas de contacto de los reels, con un cuadro cada 0,5 s: `_plan/v4/fase2/hojas/`. Duración del loop = tramo − fundido. KB = 1024 bytes.

## Estado actual (ronda 2)

| id | ref | archivo | tramo (s) | loop | fundido | salida | MP4 KB | WebM KB | póster webp KB | costura* | por qué ese tramo | post que lo respalda |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `portada-celular` | V007 | C3tFEcvJ80x_00.mp4 | 21,26–30,1 | 8,04 s | 0,8 s | 720×1280 | 1.231 | 1.248 | 40 | 25,3 (4,5)** | «La portada es el bar»: un solo plano que camina por la terraza techada repleta, bajo el techo de cintas, al atardecer; al final, una mesa de amigas de noche. Mide más nitidez que la portada anterior (varianza laplaciana mediana a 540 px: 53 contra 33) | IG-115, 23-feb-2024: «una noche beia llena de amistad, abrazos…» (164 ♥). Las cintas: IG-111 «Somos inquietos y nos gusta el colorssss!» |
| `portada-escritorio` | V031 | DFWLrRxyvVB_00.mp4 | 0,4–10,45 | 9,07 s | 1,0 s | 1278×720 | 2.461 | 2.423 | 17 | 4,9 (9,4) | Queda tal cual por decisión del cliente: letrero → puerta → cintas → mural de ojos → lámparas de pinzas, sin subtítulos | IG-061, 27-ene-2025, video institucional de @estudiouno.prod (266 ♥) |
| `lugar-noche` | V017 | C9lH7qfSTfo_00.mp4 | 9,8–18,68 | 8,1 s | 0,8 s | 720×900 | 1.365 | 1.180 | 44 | 6,1 (39,9) | El local lleno de noche: el salón repleto bajo las flores del «10», la terraza con estufas, las guirnaldas de luces y la barra rosa trabajando. Nitidez 105. Reemplaza a `lugar-cintas`, porque ese plano pasó a la portada | IG-098, 18-jul-2024, 10 años (156 ♥) |
| `tragos-coctelera` | V032 | DGLxTmGJ3ZV_00.mp4 | 0,6–10,15 | 8,67 s | 0,9 s | 720×900 | 1.291 | 1.172 | 27 | 3,5 (11,2) | Girasoles → barra roja → bartender con delantal ALMUD que bate y sirve → techo de cintas | IG-059, 17-feb-2025: «jornada de fotos & videitos entre nosotros» |
| `tragos-humo` | V038 | DOO7fgniNI6_00.mp4 | 7,0–16,75 | 8,68 s | 1,0 s | 720×900 | 953 | 618 | 19 | 3,4 (2,0) | La burbuja de humo crece y una mano la revienta. Es el trago «Aquí te las traigo Peter» (cubre `tragos-peter`) | IG-044, 5-sep-2025 |
| `comida-con-tuti` | V047 | DY0AUvhlHjI_07.mp4 | 0,25–10,4 | 9,17 s | 1,0 s | 720×900 | 1.266 | 1.143 | 62 | 3,0 (7,2) | Un plato con video propio: un cliente pica de la tabla en la terraza, en un solo plano. Es la misma tabla de la foto IG-066 «CON TUTI SI NO PA QUÉ!», que la carta asocia a ese plato. En la página lleva el nombre y el precio literales de la carta: «Con tuti si no pa qué!», $ 19.900, con enlace a Picoteos | IG-022, 26-may-2026: «tenemos una cocina sencilla pero más que sabrosona!»; IG-066 |
| `quien-multitud-1` | V036 | DM3n8lOy5qf_00.mp4 | 66,32–75,7 | 8,37 s | 1,0 s | 720×900 | 1.374 | 1.173 | 24 | 16,2 (11,4) | Una mesa entera levanta los vasos bajo las cintas, risas en las mesas y la terraza llena (cortes propios de ~1 s). Nitidez 73 | IG-051, 2-ago-2025, 11 años: «nuestros fieles parroquianos que brindaron y celebraron con nosotros» (117 ♥) |
| `quien-multitud-2` | V036 | DM3n8lOy5qf_00.mp4 | 27,6–37,7 | 9,2 s | 0,9 s | 720×900 | 1.327 | 1.145 | 11 | 3,6 (2,5) | Se sirve un trago y después vienen grupos en las mesas, risas, gente de pie y el salón lleno. Nitidez 87. Arranca en el plano del trago para que el fundido no caiga justo antes de un corte | IG-051 |
| `equipo-duenos` | V017 | C9lH7qfSTfo_00.mp4 | 32,9–42,9 | 9,0 s | 1,0 s | 720×1280 (se muestra 4:5) | 1.662 | 1.595 | 23 | 8,2 (11,8) | Es el loop que era portada de celular (bartender, Carmen Paz y Sylvain), reutilizado tal cual: solo se renombraron los archivos, sin recodificar. Va como primera tarjeta de Equipo | IG-098 |
| `donde-terraza` | V007 | C3tFEcvJ80x_00.mp4 | 0,0–8,92 | 8,14 s | 0,8 s | 720×720 | 1.350 | 1.195 | 52 | 17,9 (29,1) | La terraza de tarde con Castro detrás → mesas → trago rosado → terraza techada. El letrero solo existe en los 10 s de V031 que usa la portada de escritorio | IG-115 |

\* Costura: diferencia media de luminancia (0–255) entre el último y el primer cuadro del loop; entre paréntesis, la de dos cuadros consecutivos del mismo loop. Todas se revisaron también a ojo, cuadro a cuadro durante el fundido, y ninguna salta.
\*\* La portada mide alto porque el plano camina rápido justo donde empieza; a ojo el fundido es continuo.

**Pesos.** Fuera de la portada, todos quedan ≤ 1.200 KB WebM y ≤ 1.400 KB MP4. La portada de celular pesa 1.248 KB en WebM (meta ≤ 1.300) y 1.231 KB en MP4.

**Primer pantallazo del celular** (Playwright a 390×844, 5 s después de cargar, 12 archivos): 1.619 KB sin compresión, servido por el servidor local. Con gzip, como lo sirve Cloudflare, son ≈ 1.450 KB: HTML, CSS y JS pasan de 254 a 85 KB. Meta ≤ 1.536 KB. Las fotos que no son de portada ya no se piden al cargar la página: van con `data-srcset` y `data-src` y el JS las asigna cuando están a ≤ 0,5 pantallas (antes, Chrome traía de entrada las 6 fotos de El lugar y 4 de Tragos). Escritorio (1440×900): 2.774 KB, casi todo el video horizontal (2.423 KB), que se quedó tal cual.

## Cambios de la ronda 2 (decisiones del cliente)
- La portada de celular pasa a ser el bar lleno (V007). La de antes (V017, con los dueños) se movió a Equipo como `equipo-duenos`.
- Sale `quien-brindis` (V028, un solo hombre). En Con quién entran `quien-multitud-1` y `quien-multitud-2`: en escritorio encabezan la tercera columna y en celular van lado a lado.
- Sale `comida-cazuela` (sartén con carne bajo «Camarón que se duerme»). Entra `comida-con-tuti`, con el nombre y el precio del plato que se ve.
- Sale `lugar-cintas`, porque su plano es ahora la portada. Entra `lugar-noche`.

## Advertencia sobre `comida-con-tuti`
La carta actual dice «[Versión 2.0]» y marca el plato como veggie (champis, palta, quesos, aceitunas, frutos secos, fruta, pancito). El video (may-2026) y la foto IG-066 (ene-2025) muestran la versión anterior, que traía jamón serrano. Si Carmen prefiere no mostrar jamón bajo un plato veggie, hay que pedirles un video de la versión 2.0. Ninguna otra comida propia tiene video de 8 s o más con un plato identificable: V040 dura 8,3 s, V046 7,7 s, V044 6,4 s y V052 4,1 s.

## Slots pedidos que no se crean
- `tragos-peter`: el Peter es el trago del humo.
- `lugar-terraza`: la terraza llena ya está en la portada y en `donde-terraza`.

## Descartes de la revisión
- V021: después de 5 s de muro rosa viene un montaje de fotos que cambia cada 0,2 s, con DJ y tecladista.
- V022: visita de la embajadora de Flor de Caña (otra marca).
- V025 y V026: músicos y DJ invitados, y etiquetas de botellas en primer plano.
- V001 y V002: época de @vlanbartender.
- V034: desfile Esencial (otra marca).
- V055 y V037: multitud con luz violeta (la «fiesta morada» que Carmen rechazó para la portada).
- V008: bailarinas invitadas.
- V043: noche Rucalaf.
- V041 y V042: banda Isleños.
- V009, V052 y V040: demasiado cortos.
