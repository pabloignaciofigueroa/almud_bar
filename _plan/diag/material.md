# Diagnóstico del material visual propio — Almud Bar (web v2)

> Fuente: todo `assets/raw/ig/` (453 jpg + 57 mp4, 180 posts dic-2022 → oct-2026) y `assets/raw/hl/` (121 jpg + 62 mp4, 4 destacadas + portadas + foto de perfil).
> Método: 34 hojas de contacto rotuladas en `_plan/diag/sheets/` (`img_01…19`, `vid_01…15`, más `top30.jpg` y `vid_V031_horizontal.jpg`), todas revisadas a ojo. A cada video se le sacaron 3 frames (12 %, 50 % y 88 %) y se midió con ffprobe. Por imagen se calcularon resolución, nitidez (varianza del laplaciano a 800 px), brillo, saturación y un índice de "gráfica". El tipo, el espacio, la luz y los puntajes son juicio visual.
> Catálogo completo: `_plan/diag/catalogo.csv` (693 filas, una por archivo). La columna `ref` (P001…P455 fotos/gráficas, V001…V119 videos, `-cover` = portada de un video) es la misma que aparece en las hojas.
> Likes normalizados = likes / mediana de likes de los posts del mismo semestre. Medianas: 2022H2 167 · 2023H1 98 · 2023H2 99 · 2024H1 112 · 2024H2 132 · 2025H1 180 · 2025H2 91 · 2026H1 58 · 2026H2 96,5.

---

## 1. Inventario en una mirada

| Tipo | n | Comentario |
|---|---|---|
| foto | 375 | 70 % vertical (3:4 = 158, 4:5 = 91), 1:1 = 46, horizontal = 67 (3:2 = 38) |
| afiche | 21 | piezas gráficas de eventos, casi todas sobre negro |
| video (reel) | 57 | 56 verticales (40 son 720×1280) y **1 solo horizontal** (V031, 1278×720) |
| story | 121 | 59 jpg + 62 mp4: Tiki Night/Chapter44 (feb-2020), Teik Agüei (pandemia 2020), 12 añitos (jul-2026), Horarios. Casi todo son reposteos de terceros con stickers |
| portada de video | 119 | el jpg de portada de cada mp4 (heredan los atributos del video) |

- **Resolución de las fotos:** mediana de 1440 px de ancho. Hay 89 fotos de ≥3000 px (todas de 2026: sesiones @isosur.prod de los 12 años, la noche Rucalaf y el nuevo techado) y 29 de <1000 px (2023 temprano, Jalogüín 2024, reposteos).
- **Época:** 2026 = 140 fotos · 2025 = 86 · 2024 = 89 · 2023 = 54 · 2022 = 6. Lo más nítido y abundante es lo más reciente.
- **Fotógrafos acreditados en captions** (hay que pedirles permiso y créditos): @estudiouno.prod (sesión de comida de día, IG-062, y el video institucional V031, IG-061), @isosur.prod (12 años, IG-009/IG-008), @tamillanguileo y @catarsis.fotografia (9° aniversario, afiche IG P047), @mariannefuentealba (P252, siluetas en blanco y negro, IG-033).

## 2. Cobertura por espacio (lo que pidió el cliente)

Conteo sobre foto + reel (n / con calidad técnica ≥4 y épica ≥4 / de esas, con luz "noche cálida"):

| Espacio | n | buenas | buenas en noche cálida | Diagnóstico |
|---|---|---|---|---|
| **Barra** | 62 | 40 | 36 | Sobra. Es el corazón visual: muro de botellas rosa-rojo, lámparas de flecos/varillas, barra curva |
| **Patio techado** (terraza techada) | 40 | 25 | 13 | Muy bien cubierto: techo de banderines/flecos multicolor, estufas. Desde ago-2025 muchas fotos llevan luz LED violeta |
| **Personal** (equipo) | 36 | 20 | 17 | Bien: bartenders, garzonas con jockey ALMUD, equipo completo |
| **Mesas interiores** (salón) | 16 | 5 | 5 | Justo. Hay pocas tomas limpias del salón como lugar |
| **Terraza descubierta** (patio) | 18 | 8 | 2 | Media: hay buenas de noche con guirnaldas (2023) y del patio de día (2026), más dos reels |
| **Fogón** | 5 | 4 | 1 | Escaso. P385 (brasero nuevo, oct-2026). P283/P290 son de la noche **Almud & Rucalaf** (IG-025): hay que confirmar si la locación es Almud |
| **Cuadros/arte** | 4 (+afiches/stories) | 0 | 0 | **Brecha.** Muro de marcos vacíos de colores, mural "Ojo Piojo" de ojos, mural de corazones y papel mural floral del baño: aparecen sobre todo en video o de fondo |
| **Sofás / rincón sillones** | 2 | 1 | 1 | **Brecha crítica.** Solo P114 sirve |
| Dueños | 9 | 3 | 0 | No se sabe con seguridad quién es quién; el reel V056 identifica a Sylvain |
| Fachada/letrero | 2 | 0 | 0 | Solo en video: V031 de 1 a 4 s (letrero luminoso + puerta de madera) |
| Vista/atardecer | 1 | 0 | 0 | P020 (techos de Castro y el mar, 2023). El mar aparece de fondo en P157, V010, V028 y V042 |

### Mejores 3 por espacio pedido
- **Sofás:** `ig/DBMtYELSzNS_14.jpg` (P114: mujer riendo en un sillón con cojines estampados, 1440×1800), `ig/DCIEfJUylnY_15.jpg` (P136: grupo disfrazado en sillones, 1071 px, solo como apoyo). No hay una tercera foto válida, así que hay que **pedirla o fotografiarla**.
- **Mesas interiores:** `ig/C-V5Lc7SZ-K_00.jpg` (P076: mesas con ventanal de reja y muro rojo, horizontal), `ig/C9dHAAxJkSi_00.jpg` (P073: el "10" de flores sobre el salón), `ig/Dbg3ekilC4P_02.jpg` (P339: lámpara de mimbre, muro rojo, 3072 px). Alternativa: `ig/CnFUpxNpG_E_03.jpg` (P012, con el muro de cuadros, pero 853 px).
- **Barra:** `ig/DAMHps8JVVr_07.jpg` (P093: barra curva completa con banderines), `ig/DCIEfJUylnY_03.jpg` (P124: bartender lanzando una botella frente al muro, horizontal), `ig/DU35ZDPCBcH_00.jpg` (P254: dos clientas brindando frente al muro rosa; x6,16, el récord de likes normalizados en foto).
- **Patio techado:** `ig/DM_Ih5dyVKH_07.jpg` (P189: techo de banderines sobre la terraza llena), `ig/DAMHps8JVVr_04.jpg` (P090: faroles de papel y flecos), `ig/Ct7e1vopLTU_00.jpg` (P046: túnel de cintas verticales, pero 873 px). Del techado nuevo de oct-2026: `ig/Dd94G-HlL-W_01.jpg` (P382, de día y vacío, 887 px) y `ig/Dbok2NyFNdb_02.jpg` (P359).
- **Terraza descubierta:** `ig/Cqn78DFp5Nm_00.jpg` (P039: guirnaldas, árboles y bancas), `ig/Cp5baHfLpgx_00.jpg` (P035: ripio, mesas llenas, pérgola), `ig/Dbok2NyFNdb_00.jpg` (P357: pérgola en violeta, 3072 px). En movimiento: V042 y V010.
- **Cuadros:** `ig/DFWLrRxyvVB_00.mp4` (V031, de 7 a 8 s: mural Ojo Piojo, horizontal), `ig/C3VODtYsjNX_00.mp4` (V006: el mural en el patio), `ig/CnFUpxNpG_E_03.jpg` (P012: muro de marcos detrás de la barra). Complemento: el afiche "Ojo Piojo" (P063) y el mural de corazones (P174).
- **Personal:** `ig/DaWM8rlo1FR_00.jpg` (P333: dos garzonas con corbata y jockey, 3219 px), `ig/CqEI2nSJP2__00.jpg` (P036: garzona con pizza mirando por sobre el hombro, x3,05), `ig/C-bY0mLNYRz_00.jpg` (P077: el equipo tras la barra, horizontal). Fotos de grupo: `ig/DEP9IUpR9G4_00.jpg` (P157, con el mar detrás) y `ig/DNEpXfOpDyN_00.jpg` (P202, trae franjas negras).

## 3. Cobertura por historia/evento

| Cuento | Posts/archivos | Calidad | Nota |
|---|---|---|---|
| 11 años (ago-2025) | IG-050 `DM_Ih5dyVKH_*` (20 fotos), IG-047 `DNT1_BYS_Yf_*` (19) | 4–5 | Lo mejor en noche cálida. x2,99 y x4,19 |
| 12 años (jul/ago-2026) | IG-009 `Dbg3ekilC4P_*`, IG-008 `Dbok2NyFNdb_*` (40 fotos de 3072 px), V055, destacada 12 añitos | 4 | Alta resolución, pero en luz mixta violeta |
| Fondita / Fiestas Patrias (2024 → 2026) | IG-079 `DAMHps8JVVr_*` (13), afiches P085, P224, P377 y P378 | 5 | La serie más pulida: banderines, faroles, barra |
| Jalogüín (2023 → 2025) | IG-071, IG-070, `DShtzZ0FD9H_*`, afiche P058 | 3–4 | Mucho disfraz. Las fotos de 2024 son de 700–1068 px |
| Primavera / música en vivo (oct-2024) | IG-075 `DBMtYELSzNS_*` (20) | 4 | Abanicos de papel, músicos, rincón sillones |
| 10 años (jul-2024) | IG-100, IG-106, V018, V021 | 4 | El "10" de flores |
| Sesión de comida de día (ene-2025) | IG-062 `DE5w6nMyEyI_*` (@estudiouno.prod) | 4 | Luz de día, mesa exterior: rompe la familia nocturna |
| Tardes en el Almud / Isleños (2026) | V041, V042 (x6,6 y x5,57) | 4 | Banda en el patio con el mar. Es contenido de la banda (colaboración) |
| Almud & Rucalaf (may-2026) | IG-025 `DYnU3NTFFQP_*`, afiche P255 | 4 | Fogón, humo, luces de color. Locación a verificar |
| Sociales (may-2026) | IG-026 `DYiMMUrlBk1_*` | 3–4 | Fotos de flash posadas, x5,0. Muchas caras de clientes |
| Teik Agüei (pandemia 2020) | 44 stories | 1–2 | Valor solo documental/gráfico: etiquetas kraft, bolsas, mascarillas |
| Tiki Night / Chapter44 (feb-2020) | 54 stories | 1–2 | Reposteos de terceros. Afiches menta/turquesa |

## 4. Distribución de calidad

- **Fotos (375), calidad técnica:** 5 = 17 · 4 = 256 · 3 = 86 · 2 = 16. **Épica:** 5 = 12 · 4 = 140 · 3 = 198 · 2 = 25. Hay unas 150 fotos utilizables como foto fuerte y apenas 12 son héroe indiscutible.
- **Reels (57):** calidad 4 = 17 · 3 = 34 · 2 = 6. Casi todos son 720p comprimidos de Instagram; solo V012 (gráfica) y V021 llegan a 1080×1920.
- **Stories (121):** calidad 1–2 casi en su totalidad: 360–828 px, stickers, filtros y reposteos.
- **Nitidez (varianza del laplaciano):** no sirve sola para medir calidad. Las mejores fotos usan poca profundidad de campo (bokeh) y marcan valores bajos (p. ej. P297 = 365, P013 = 24). Los afiches y las fotos de día con sol marcan alto.

## 5. Familias de luz (fotos)

| Familia | n | % | Dónde |
|---|---|---|---|
| **Noche cálida** (ámbar + muro rosa-rojo) | 220 | 59 % | 2023–2025: barra, Fondita, 11 años, primavera. **Es la familia de la casa.** |
| Mixto (LED violeta/azul/verde + cálido) | 80 | 21 % | 12 años, Rucalaf, techado nuevo (ago-2025 → 2026). Choca con la regla "una sola familia de luz" |
| Día | 45 | 12 % | Comida (@estudiouno), equipo en el pasto, terraza de día |
| Flash | 28 | 7 % | "Sociales" de IG-026 y algunas de los 11 años |
| Blanco y negro | 2 + afiches | — | P252 (siluetas en la barra), P346, P350 |

Consecuencia: la v2 se puede armar entera en noche cálida, con fotos de 2023 a 2025. Las de 2026 en alta resolución sirven solo si se aceptan los acentos violeta o si se recortan zonas cálidas (p. ej. P339 y P362 sí son cálidas).

## 6. Las ~30 candidatas más fuertes (ver `sheets/top30.jpg`)

Puntaje = 2×épica + técnica + 0,6×min(likes normalizados, 3), corregido a mano para que haya variedad de espacios.

| # | Archivo (assets/raw/) | Espacio | Res. | ♥ / norm | Por qué |
|---|---|---|---|---|---|
| 1 | ig/DM_Ih5dyVKH_07.jpg | patio techado | 1440×1919 | 272 / 2,99 | Techo de banderines sobre la terraza llena: el "colors" de la marca en una imagen |
| 2 | ig/DAMHps8JVVr_07.jpg | barra | 1440×1701 | 186 / 1,41 | La barra curva completa, con banderines, flores y botellas. Plano de lugar |
| 3 | ig/DCIEfJUylnY_03.jpg | barra | 1068×714 | 241 / 1,83 | Bartender lanzando una botella frente al muro rojo. Horizontal |
| 4 | ig/DAMHps8JVVr_04.jpg | patio techado | 1440×1708 | 186 / 1,41 | Faroles y flecos de papel sobre la gente |
| 5 | ig/Dbg3ekilC4P_11.jpg | público | 3072×4096 | 247 / 2,56 | Multitud de los 12 años desde arriba. Luz mixta |
| 6 | ig/C9dHAAxJkSi_00.jpg | salón | 1334×1667 | 307 / 2,33 | El "10" de flores: un hito |
| 7 | ig/Cqn78DFp5Nm_00.jpg | terraza abierta | 1332×1665 | 106 / 1,08 | El patio con guirnaldas y árboles |
| 8 | ig/CpVyxXJJrhO_00.jpg | barra | 1332×1665 | 99 / 1,01 | Clientas riendo con tragos de colores |
| 9 | ig/DYsZ0GNo_88_00.jpg | trago | 3177×3177 | 32 / 0,55 | Splash rojo en copa coupe. Técnicamente la mejor foto de trago |
| 10 | ig/DBMtYELSzNS_09.jpg | barra | 1440×1800 | 254 / 1,92 | Bartender riendo, camisa floreada, muro rosa |
| 11 | ig/DM_Ih5dyVKH_02.jpg | barra | 1440×1920 | 272 / 2,99 | Bartender sirviendo frente al muro de botellas |
| 12 | ig/DAMHps8JVVr_00.jpg | trago | 1440×1708 | 186 / 1,41 | Tres copas con espuma y flores secas |
| 13 | ig/DAMHps8JVVr_11.jpg | trago | 1440×1708 | 186 / 1,41 | Copa tallada con el muro rosa desenfocado detrás |
| 14 | ig/DAMHps8JVVr_01.jpg | barra | 1440×1708 | 186 / 1,41 | Bartender con polera rayada preparando un martini |
| 15 | ig/DU35ZDPCBcH_00.jpg | barra | 1440×1920 | 357 / 6,16 | Brindis frente al muro rosa. Récord de likes normalizados |
| 16 | ig/DNT1_BYS_Yf_01.jpg | barra | 1440×1920 | 381 / 4,19 | Botella en alto bajo la lámpara de flecos |
| 17 | ig/DNT1_BYS_Yf_18.jpg | dueños? | 1440×1920 | 381 / 4,19 | Torta de los 11 años bajo el letrero luminoso ALMUD BAR |
| 18 | ig/DaWM8rlo1FR_00.jpg | personal | 3219×4096 | 316 / 3,27 | Dos garzonas con corbata y jockey |
| 19 | ig/CqEI2nSJP2__00.jpg | personal | 1332×1665 | 299 / 3,05 | Garzona con pizza mirando a cámara |
| 20 | ig/DEP9IUpR9G4_00.jpg | personal | 1440×960 | 347 / 2,63 | El equipo con el mar de Castro detrás (día) |
| 21 | ig/Cmce2h1J3Wl_00.jpg | trago | 1280×1600 | 176 / 1,05 | Negroni sobre el posavaso con logo |
| 22 | ig/Ct7e1vopLTU_00.jpg | patio techado | 873×873 | 245 / 2,50 | Túnel de cintas. Baja resolución: solo en tamaño medio |
| 23 | ig/Dd94G-HlL-W_04.jpg | fogón | 3072×4096 | 238 / 2,47 | Brasas del brasero nuevo |
| 24 | ig/Dd94G-HlL-W_01.jpg | patio techado nuevo | 887×887 | 238 / 2,47 | Bancas fucsia, amarillas y azules bajo el policarbonato (día) |
| 25 | ig/C-V5Lc7SZ-K_00.jpg | salón | 1335×890 | 62 / 0,47 | Mesas interiores y muro rojo. Horizontal |
| 26 | ig/DBMtYELSzNS_14.jpg | sillones | 1440×1800 | 254 / 1,92 | La única foto buena del rincón de sillones |
| 27 | ig/Dbok2NyFNdb_05.jpg | barra | 3072×4096 | 299 / 3,10 | Muro rojo con el cartel ALMUD, en alta resolución y luz cálida |
| 28 | ig/Dbok2NyFNdb_02.jpg | patio techado | 3072×4096 | 299 / 3,10 | Terraza repleta desde arriba (mixta) |
| 29 | ig/DYnU3NTFFQP_07.jpg | fogón | 3072×4096 | 148 / 2,55 | Vapor sobre la olla. Locación Rucalaf por confirmar |
| 30 | ig/CnNM_XSprlB_00.jpg | trago | 1067×1067 | 74 / 0,76 | Soplete sobre el vaso tallado, fondo negro |

Reservas: `ig/C51H8bIpXth_00.jpg` (muro de botellas EXPENDIO DE ALCOHOLES, sin gente), `ig/DUmXnQYiXwo_00.jpg` (siluetas en blanco y negro, horizontal 1440×1080), `ig/CrMRBMNpdIF_00.jpg` (carcajada frente al muro de cintas), `ig/DNT1_BYS_Yf_05.jpg`, `ig/DShtzZ0FD9H_02.jpg`.

## 7. Reels para portada (hero)

| Ref | Archivo | Formato | Dur. | Movimiento / loop | Uso |
|---|---|---|---|---|---|
| **V031** | ig/DFWLrRxyvVB_00.mp4 | **1278×720 horizontal** (el único) | 59 s | Entre **1,0 y 10,4 s no hay subtítulos**: letrero luminoso → puerta → banderines → mural de ojos → lámparas de varillas. Después de los 11 s los subtítulos vienen quemados en la imagen | **Hero de escritorio**: cortar 1–10,4 s, sin audio, con poster en el frame de 3 s. Es 720p, así que conviene un scrim o un leve oscurecido a sangre. Hecho por @estudiouno.prod para Almud |
| **V009** | ig/C5WAi8PLHni_00.mp4 | 720×1280 | 7,1 s | Paneo lento por el techo de flecos con luces. Casi abstracto y el loop no se nota | **Hero móvil** o fondo vertical |
| V038 | ig/DOO7fgniNI6_00.mp4 | 720×1280 | 16,8 s | Burbuja de humo que estalla sobre una coupe roja | Cuento del trago / segundo hero |
| V025 | ig/DBJy4NbJ-h9_00.mp4 | 720×1280 | 73,5 s | Chorros a contraluz ámbar, margaritas, shots: cinematográfico | Cortar 4–6 s |
| V032 | ig/DGLxTmGJ3ZV_00.mp4 | 720×1280 | 37,9 s | Muro rojo con lámpara de flecos, cazuela, trago ámbar | Cortes para la barra |
| V020 | ig/C-YrpVjpCqN_00.mp4 | 720×1280 | 27,7 s | Recorrido por el pasillo de la barra llena | Prueba de "barra larga" |
| V054 | ig/DZ8c3yiIdpa_00.mp4 | 720×1280 | 3,3 s | Piel de naranja sobre un negroni | Microloop (Negroni Week) |
| V021 | ig/C-dwJHLyPpU_00.mp4 | **1080×1920** | 12,1 s | Muro rosa, terraza con estufa, shots | El vertical más nítido |
| V042 | ig/DXzcB3QzWQT_00.mp4 | 720×1280 | 26,1 s | Isleños tocando en el patio con el mar (de día) | Cuento de la música. **Contenido de la banda**: pedir permiso. V041 trae el título ISLEÑOS sobreimpreso |
| V056 | ig/DcuYoBrtSTo_00.mp4 | 720×1280 | 41 s | Reel de creadores sobre Sylvain (dueño), con subtítulos | 1488 ♥ (x15,4), el más viral. Sirve como cita, no como hero (es contenido de terceros) |

Conclusión: no existe un footage propio que sea a la vez horizontal, de alta resolución y sin texto. La mejor combinación es **V031 (1–10 s) para la portada horizontal y V009 para la vertical**. Ambos son de 720p, así que se tratan como textura (oscurecidos y a sangre), nunca como foto nítida en pantalla completa.

## 8. Lenguaje gráfico propio (afiches, stories, objetos)

La v2 tiene que salir de esto, no de una estética importada.

1. **Fondo negro como lienzo.** 13 de los 21 afiches van sobre negro casi puro (#020201–#282827, entre 50 % y 83 % del área): P047, P058, P063, P064, P065, P071, P072, P173, P178, P179, P253, P332 y P380. Otros 4 van sobre una foto oscura (P085, P224, P225, P379). Solo P177 (Desfile, crema) es claro.
2. **Pareja tipográfica:** una **script de pincel/caligráfica** (dorada en el 9° aniversario y en los 12 años; blanca en "Almud es amor", "Negroni Week" y "Chaolin verano"; café en el Desfile Esencial; roja en "Amor es amor" de PRIDE) con una **palo seco condensada en caja alta** (PRIDE gigante, MAMBO TIKI, "HOY DESDE LAS 16:30", la pizarra de HORARIOS y el propio logotipo ALMUD BAR). Esto respalda el par Six Caps + Oswald para la condensada. La script es parte de la marca, pero no tiene equivalente en la v2: si sale Caveat, la script se rescata solo como imagen dentro de los afiches.
3. **Franjas arcoíris de cinta** como recurso recurrente: franja diagonal de cintas (P047), franjas de ojos (P063), arco de cintas (P065), barras verticales (P255), degradé (P332, tarjeta #12AÑOS en V116). Sale de las cintas reales del techo. Funciona como "campo plano por capítulo" o como corte duro.
4. **Collage con foto propia:** afiches de Fondita sobre una foto de banderines (P085, P224, P377) con letras gruesas contorneadas en amarillo #f2d03b, rojo y azul (bandera chilena); Rucalaf sobre una foto aérea.
5. **Ilustración floral y corazones** (P173, P253): ramos de flores dibujados y corazón rojo. Aparece en San Valentín y Amor.
6. **Era 2020:** menta/turquesa #13ceb3 con mostaza (Tiki Night, Chapter44), amarillo #edca3b con script negra (#Teik agüei), crema #e3ddb3 con azul marino (carta para retiro), etiquetas kraft con tipografía de máquina de escribir, cajas de pizza con patrón de azulejo (V099).
7. **El isotipo de pinzas.** La foto de perfil son pinzas de ropa de colores en filas sobre negro (#4c479d, #92241a, #c1933b, #3b6f24). Las pinzas también son el logo del posavaso y de la bolsa kraft (P423, P425, P438) y una **lámpara real de pinzas** en el bar (V014). Es el motivo más propio y menos explotado: sirve como patrón, ícono SVG de un solo trazo o separador.
8. **Objetos de marca:** posavasos kraft, delantales y jockeys con logo, poleras de pinzas, la polera calavera azul/naranja (P153) y el letrero luminoso blanco y azul (V031 a 1 s, P221).

## 9. Paleta real de las mejores fotos (k-means sobre el top 30)

**Global (k = 10, % de píxeles):** #140e12 (24,2) · #46201a (16,5) · #9e6e57 (11,0) · #72452f (10,4) · #e2a07d (9,5) · #dd693d (7,6) · #a63016 (7,0) · #f1d7cb (5,1) · #453d65 (5,1) · #919cbb (3,5).
**Píxeles saturados** (S > 0,55, V > 0,45; son el 25 % del total): #8f4e28 · #bc6d3a · #8e2010 · #eb9b4b · #d2351a · #f05755 · #8e2d95 · #2b399f.
**Por familia de tono (representante vivo):** rojo #f45852 (33 % de lo saturado) · naranja/brasa #e6874c (51 %) · ámbar/pisco #f5c658 (6 %) · rosa/magenta #e92b69 (4 %) · azul #5660d4 (2 %) · violeta #863fd0 (2 %) · verde #4d9b70 (0,4 %).

Lectura:
- Las fotos son **noche ámbar-brasa sobre casi negro cálido** (#140e12 / #46201a).
- El "rosa del muro" aparece como coral-rojo #f05755 / #f45852 por el balance cálido, y solo se ve fucsia (#e92b69) en las tomas más limpias. Eso respalda `--barra` #ff3f6c como único acento.
- El verde y el azul casi no existen en las fotos fuertes: `--cinta` y `--cielo` vienen de los banderines y conviene limitarlos a campos planos.
- El violeta (#863fd0 / #453d65) solo entra en las fotos de 2026: queda confirmado que es de las luces y no de la marca.
- La paleta por foto está en `sheets/top30.jpg` (4 muestras bajo cada miniatura).

## 10. Brechas y riesgos

- **Sofás y cuadros casi sin fotos.** Son dos de los siete espacios que pidió el cliente. Hay que pedir material o resolverlos con frames de video (V031 a 7–8 s y V006 para el mural; V084 para los marcos, aunque es una story 480p).
- **Ningún video horizontal en alta resolución.** Solo existe V031, en 720p. Todos los demás reels son verticales.
- **Proporciones:** las fotos son mayoritariamente 3:4 y 4:5. La regla pide "4:5 y 16:9 ≥75 %". Para tener 16:9 hay que recortar de 3:4. Solo las de 3072 px (2026, luz mixta) aguantan un 16:9 a sangre en retina; las de 1440 px dan 1440×810, que alcanza para bandas medias pero no para pantalla completa. Hay solo 16 horizontales nativas de ≥1400 px de ancho.
- **Baja resolución:** 29 fotos tienen <1000 px (Jalogüín 2024, enero de 2023, reposteos de 2026 como P263/P264). Las stories de 2020 son de 360–828 px.
- **Texto sobreimpreso y marcas de agua:** subtítulos quemados (V031 después de los 11 s, V056), título "ISLEÑOS" (V041), stickers y @handles en casi todas las stories y gráficas animadas (V012). Las fotos del feed vienen limpias.
- **Filtros:** blanco y negro (P080, P252, P346, P350), larga exposición/barrido (P287, P337, P140), filtro VHS y tintes en las stories de 2020, luz LED violeta saturada en 2025–26.
- **Contenido de terceros:** V041/V042 (de la banda Isleños), V056 (creadores de contenido), stories reposteadas (Chapter44, DJ, clientes), noche Rucalaf (colaboración en una locación posiblemente ajena). Faltan créditos y permisos.
- **Caras:** decenas de clientes identificables en primer plano (las sociales de IG-026, Jalogüín, 12 años). Conviene preferir fotos de equipo o de público desenfocado para los usos grandes. **No se identificaron menores de edad** con claridad en todo el material; en las fotos de terraza aparecen jóvenes que parecen adultos.
- **Duplicados/reposteos:** P263 = P153, P264 = P133, P300 = P091, P312 = P107, P316 = P040, P320 = P166, P327 = P018, P395 = P109, V057 = V050. Usar siempre la versión original.
- **Espacio cambiado:** el techado nuevo de oct-2026 (IG-004) hace que el "patio techado" de 2024–25 ya no se vea igual. Las fotos viejas del techo de banderines siguen siendo las más épicas, pero conviene contrastar con P382/P384.
- **Identidad de los dueños:** solo las captions (@rusio_mezclao, @cepaz) y V056 (Sylvain) la confirman. No hay que rotular a nadie en las fotos sin verificarlo.

## 11. Implicancias para una web nueva (v2)

1. **Portada:** V031 entre 1 y 10,4 s como loop horizontal muted, con poster en la puerta o el letrero, y V009 (techo de flecos) como versión vertical. Ambos a sangre con scrim neutro y nunca a nitidez 1:1. El h1 va encima, a 2 líneas como máximo.
2. **Una sola familia de luz:** se arma con noche cálida 2023–2025 (Fondita, 11 años, primavera, barra). Lo violeta de 2026 se usa solo en el cuento "aniversarios/fiesta", y como mosaico, no como foto decisiva.
3. **Foto decisiva por cuento (propuesta):**
   - Barra: P093
   - Patio techado: P189
   - Patio abierto: P039
   - Trago: P297
   - Equipo: P333 o P036
   - Fiesta: P348
   - Hito de los 10 años: P073
   - Fogón: P385
   - Sillones: P114, la única foto, con mosaico de apoyo
4. **Tratamientos:**
   - banda a sangre: P189 o P090 (recorte 16:9 desde 1440×1708);
   - split: P093 + P124;
   - mosaico desigual: las 20 fotos de IG-050 / IG-079, todas de la misma sesión y luz;
   - foto sostenida: P039;
   - marco que crece: P297.
5. **El color sale de las fotos:** fondo #140e12, ámbar-brasa como luz y `--barra` como único acento. Las franjas arcoíris se usan solo como cortes duros entre capítulos, porque así lo hacen sus propios afiches (P047, P065, P255).
6. **Motivo propio:** las pinzas de ropa (perfil, posavaso, lámpara) como patrón o ícono, y el letrero luminoso blanco y azul como cierre. Es más de ellos que cualquier ornamento nuevo.
7. **Antes de producir hay que pedir al cliente:**
   - 3–5 fotos del rincón de sillones y del muro de cuadros con luz de noche;
   - una toma horizontal de la fachada;
   - los originales en alta resolución de @estudiouno.prod e @isosur.prod (sobre todo el master de V031 sin subtítulos);
   - la confirmación de la locación de la noche Rucalaf;
   - permiso de Isleños para V042.
