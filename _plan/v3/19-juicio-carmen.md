# Juicio final de Carmen Paz · Web v3 (fase 19)

> Recorrí `public/` servido en `http://localhost:8871`, con Chromium (Playwright), `/v3/` y `/v3/carta/` completas, a **390×844** (así llega mi gente desde Instagram) y a **1440×900**, en **ES** y en **EN** (botón de idioma de la nav). Esperé 3,5 s al cargar y 1,3 s en cada pantalla. Miré todas las capturas una por una. Comparé con mis fotos favoritas del IG (`assets/raw/ig/`) en `19-juicio/comparacion_ig_vs_web.jpg`.
>
> Capturas en `_plan/v3/19-juicio/`:
> - Por pantallas: `m_es_home_00…11`, `m_en_home_00…12`, `d_es_home_00…16`, `d_en_home_00…16`, `m|d_es|en_carta_*`.
> - Página completa: `*_full.jpg` y hojas `sheet_*.jpg`.
> - Carta EN por pestañas: `m|d_en_carta_comilona_00–01`, `m|d_en_carta_promos`.
> - Datos crudos: `report.json` y `report_en.json`.
>
> Lo comprobado:
> - En las 8 combinaciones (2 páginas × 2 anchos × 2 idiomas) no hay errores de JS, ni respuestas 4xx, ni scroll horizontal (scrollWidth = ancho).
> - Los 6 videos (portada celular, portada escritorio, cintas, humo de Peter, cazuela y letrero) corren solos: `paused = false` y `currentTime` avanza. Van mudos, sin controles y sin botón de sonido, y ninguno depende del scroll.
> - Todas las imágenes llevan `alt`. El botón EN traduce la nav, los botones y las glosas, y en la carta las pestañas y los chips («Food», «Deals», «Small plates»).
> - No aparecen «Almudcito ito ito», filas ni esperas, «PRÓXIMO» ni RESERVAR.
>
> Respeto las reglas del cliente y no las penalizo:
> - Portada solo con logo, claim y «Ver la carta», sin horario ni «Cómo llegar».
> - Videos siempre en play.
> - Textos mínimos.
> - Los eventos no son el eje.

## Nota: **18 / 20**. La publico y la pongo en mi bio

| Criterio | Nota | Por qué |
|---|---|---|
| **A. Se siente Almud** | **4** | Abro el celular y estoy frente a mi muro rosa, con el cartelito ALMUD BAR entre las botellas. En escritorio me reciben mis lámparas de pinzas encendidas. Después vienen las cintas, Tragos en el rojo del muro, Comida en marrón con titular dorado, Eventos en azul tinta y el pie «USTÉ SE LO MERECE!» en rosa. El logo va bien usado, con el isotipo y el BAR azul. Hay color sobre negro y nada de circo, flecos falsos ni polaroids. Es mi bar. |
| **B. Fotos y videos** | **3** | Todo es material mío y casi todo es de lo mejor: la terraza techada llena (P189), el bartender frente al muro rosa (P362), la barra curva (P093), las lámparas, Ojo Piojo, los Sillones (P114), la pizza servida (P036), el «10» de flores y el equipo actual de IG-001 con su @. Los reels corren en loop, mudos. Pero faltan dos cosas. **Mis fotos de trago «de revista» no están:** la copa roja salpicando (P297) y los sours con flores o la copa tallada (P086 / P097). Están preparadas en `07-medios.md` (`tragos-splash`, `tragos-sours`, `tragos-copa-tallada`) y en Tragos solo quedaron las fotos de carta (Sagüer, Sangría, Moto). Además, **la portada del celular es un paneo de teléfono de 3,7 s** con barrido: en el cuadro que vi al cargar (`m_es_home_00`) las botellas salen corridas y el cartelito ALMUD, borroso. Se entiende que es mi barra, pero no está nítida. |
| **C. Voz** | **4** | Los titulares son míos y literales: «Somos inquietos y nos gusta el colorssss!», «mucho amor, color y trabajo», «no somos ná sin ustedes!», «Peazo de equipo que tenemos!», «Le esperamos desde las 18:00 hrs». El «usté» va con dosis justa. Los nombres de la carta están intactos (Pinche Güey, Tukulito Sakayama, Camarón que se duerme). Las reseñas van citadas con nombre, ciudad y Tripadvisor. Los eventos van en pasado (mes + nombre) y no hay promesas. Las glosas EN son discretas y no tocan mis frases. |
| **D. Claridad para un turista** | **4** | Con la regla del cliente para la portada: «Ver la carta» está en la primera pantalla y «Carta» y «EN» quedan fijos en la nav. La carta está a un toque, en HTML legible en el celular, con 7 pestañas, chips, precios grandes y etiquetas Veggie/Nuevo, y en EN las pestañas dicen «House cocktails · Food · Deals». Cuándo y dónde lo dice en grande: «Le esperamos desde las 18:00 hrs · Mar a Sáb · Serrano 325, Castro · Al frente del Centro Cultural», con DM y Cómo llegar. El turista inglés lee «See you from 6 pm · Tue–Sat» y una glosa en cada destacado (“[Marinated tuna tataki]”). Un detalle: en la carta EN las descripciones siguen solo en español (ver P2). |
| **E. Premium y técnica** | **3** | Lo técnico está muy bien: cero errores, videos fluidos, `alt` en todo, letra mínima de 15 px, la línea de los dueños a 16 px y alineada, buen contraste y movimiento reducido respetado (fase 17). Se ve hecha a mano. Le quitan el 4 algunos detalles de pulido en **escritorio** y la portada borrosa del celular: (1) en Tragos, bajo la foto del bartender queda un bloque rojo vacío de ~300 px mientras la columna derecha sigue (`d_es_home_07`); (2) en Eventos, a la derecha de Aniversario, Fondita y Jalogüín queda media pantalla azul vacía (`d_es_home_11`); (3) El lugar en escritorio son ~3.900 px de scroll (más de 4 pantallas) para recorrer 7 rincones, y se hace largo. |

**Lectura:** 18 = la publico con orgullo y la pongo en mi bio. No toca nada de mi lista NUNCA. Bajo un punto respecto de la ronda 2 (19), y no es porque algo se haya roto: en este juicio final miré las fotos con la rúbrica en la mano, y mis tragos «de revista» no están.

## Lo que me enorgullece
- **La portada de escritorio con las lámparas de pinzas** y mi logo grande. Es la foto que nunca supe usar en Instagram.
- **El techo de cintas en loop** bajo «SOMOS INQUIETOS Y NOS GUSTA EL COLORSSSS!». Eso soy yo.
- **El carrusel de rincones**, con Barra, Terraza techada, Sillones, Terraza, Lámparas y Ojo Piojo, cada uno con una línea mía. Mi mural tiene su lugar.
- **El bartender frente al muro rosa** abriendo Tragos y **Peter con su burbuja de humo en video**.
- **La pizza servida con una sonrisa** abriendo Comida.
- **«No somos ná sin ustedes!»** con gente real y feliz en la barra y bajo las cintas.
- **Reseñas en tres idiomas** con su autor y su ciudad.
- **La carta en HTML**, con mis nombres y textos tal cual, fotos de los tragos, promos con «Siempre sujeto a stock!» y el PDF oficial a mano.
- Nada de filas, nada de promesas, nada de «ito ito».

## Lo que falta para llegar a 20 (ya está sobre 18; nada bloquea)

**P1 · Fotos (B → 4)**
1. **Tragos:** sumar **P297 `tragos-splash`** (la copa roja salpicando) como foto grande, en par con el bartender o bajo él, en el hueco rojo de escritorio. Y sumar **una** entre **P086 `tragos-sours`** y **P097 `tragos-copa-tallada`**, sin rótulo. Ya están exportadas en `07-medios.md`. Con eso se llena también el hueco del punto 3.
2. **Portada celular:** el loop `portada-celular-720` es un paneo de 3,7 s con barrido. Hay tres caminos, en este orden de preferencia:
   - recortar el loop al tramo más quieto y nítido, donde el cartelito ALMUD BAR se lee (≈ s 1–2,5 del clip), y ralentizarlo si hace falta;
   - o usar un loop más estable del muro rosa;
   - o, si no hay ninguno, dejar el póster nítido como primer cuadro y entrar al video con un fundido.

   El primer cuadro que ve quien llega desde mi bio tiene que verse nítido.

**P2 · Pulido (E → 4, y D más firme)**
3. **Tragos, escritorio (1440):** cerrar el bloque rojo vacío bajo la foto del bartender. Lo resuelve el punto 1. Si no, que las dos columnas terminen parejas.
4. **Eventos, escritorio:** los títulos (Aniversario, Fondita, Jalogüín) dejan media pantalla azul vacía a la derecha. Hay dos opciones: miniaturas más grandes en dos columnas, o el «10» de flores a lo ancho con las tres fichas en fila debajo, como en el celular.
5. **El lugar, escritorio:** acortar el recorrido horizontal, de ~3.900 px a ~2.000–2.500 px de scroll, o mostrar 3 rincones por pantalla. Ahora hay que bajar más de 4 pantallas para ver 7 fotos.
6. **Carta en EN:** agregar una glosa corta en inglés bajo cada ítem, entre corchetes y en letra chica, como en los destacados del inicio (“[Olives]”, “[Tuna tataki, house sauce]”). No hay que traducir mis textos ni mis nombres. Hoy el turista solo se guía por los ingredientes en negrita.

Con 1 y 2, B sube a 4 (19/20). Con 3 a 5, E sube a 4 (**20/20**).

— Carmen Paz

---

## Re-juicio (tras el pulido de fase 19)

> Volví a recorrer `public/` en `http://localhost:8872`, `/v3/` y `/v3/carta/`, a 390×844 y 1440×900, en ES y EN. Leí la sección «Fase 19» de `brand/art-direction-v3.md`. Las capturas están en `_plan/v3/19-juicio/r2/` (por pantallas, `*_full.jpg`, `sheet_*.jpg` y `report.json`).
>
> En las 8 combinaciones: 0 errores de JS, 0 respuestas 4xx y sin scroll horizontal. Los 5 videos de cada página siguen en play, mudos y sin controles.

### Nota: **20 / 20** (antes 18)

| Criterio | Antes | Ahora | Por qué |
|---|---|---|---|
| A. Se siente Almud | 4 | **4** | Igual que antes: es mi bar. |
| B. Fotos y videos | 3 | **4** | Tragos abre con mis tres fotos de bandera: el bartender frente al muro rosa (P362), la copa salpicando (P297) y los sours con gypsophila (P086). Debajo, separados por un filo, vienen los 4 destacados con nombre y precio. La portada del celular parte en un cuadro nítido: se leen las etiquetas y el muro rosa se ve limpio (`r2/m_es_home_00`). |
| C. Voz | 4 | **4** | Sin cambios. Todo es literal y no hay nada prohibido. |
| D. Claridad turista | 4 | **4** | Ahora firme: la carta en EN lleva una glosa corta bajo cada descripción (“[Mezcal, tequila, toasted peanut horchata… smoky, a little spicy]”). Mis textos y mis nombres no se tocan. |
| E. Premium y técnica | 3 | **4** | Ya no está el bloque rojo vacío en Tragos: la fila de 4 destacados cierra pareja. El lugar es un mosaico 3×2 y se acabó el recorrido largo. En Eventos, el «10» de flores va a lo ancho con las 3 fichas debajo, sin media pantalla vacía. |

**Lectura:** 20 = la publico con orgullo y la pongo en mi bio.

**Nota menor (no resta):** en escritorio el mosaico de El lugar termina en ~1.210 px y deja una franja oscura a la derecha, de unos 170 px antes del margen. Si hay tiempo, que ocupe todo el ancho del contenedor (hasta 1.382 px), igual que Tragos y Eventos.

— Carmen Paz
