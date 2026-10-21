# Ranking final de fotos — Almud v2 (fase 4)

> Entradas: `catalogo.csv` (693 filas), `material.md`, `skills-notes.md` §2 y `skills/taste.md` (imagen). Solo material propio de Almud; los originales HD llegan después.
> Salidas: `ranking.csv` (60 filas, todas las columnas) · `top60/ranking_1-30.jpg` · `top60/ranking_31-60.jpg` · `top60/coverage.jpg` · `top60/heroes.jpg` · frames de video en `frames/` (26 JPEG, el más nítido de cada ventana por varianza del laplaciano).
> Las hojas muestran cada foto **ya recortada** con el recorte y el foco propuestos. Todo se revisó a ojo, y las 10 más dudosas también al 100 %.

## 1. Fórmula

`score = 100 × (0,35·E + 0,25·Q + 0,25·L + 0,15·N) − penalizaciones`

- **E** = (épica − 1)/4 · **Q** = (q_tecnica − 1)/4 (frames reevaluados a mano: 720p = 2–3, story 480p = 1) · **L** = min(ln(1 + likes_norm)/ln 5, 1), log con tope en x4 la mediana del semestre; los frames heredan los likes de su reel, stories sin likes = x1 · **N** = narrativa 0–1 a mano (1 = momento con persona; 0,7–0,8 = gesto o lugar icónico; 0,4–0,5 = plato u objeto).
- **Penalizaciones:** lado corto <1000/<800/<600 px −4/−8/−12 · luz violeta −4 (pequeña, no excluye) · flash −3 · día o B/N −2 · subtítulos/story con stickers −8 · franjas negras −3 · terceros −5 y marcado.
- **Colapsos** (queda la mejor versión): P395, P120 → P109 · P392 → P362 · P300 → P091 · P312 → P107 · casi-duplicados de sesión P197 → P333, P217 → P221, V010 ≈ V006 21,9 s. Las portadas de video "3000+ px" (V014, V030) son sobremuestreo de IG, blandas al 100 %: se tratan como 1080 px efectivos.
- **Cuotas** (mínimo por espacio, luego orden por score): barra 6 · equipo 5 · techado 4 · terraza 3 · mesas 3 · sillones 3 · cuadros 4 · tragos 5 · comida 4 · fiestas 5 · fachada 2 · vista 2 · dueños 2. Topes: barra 10, fiestas 8, equipo 8, techado 7, tragos 6, comida 5, dueños 2, violeta 10.
- **Máx. px de display** = ancho del recorte propuesto (sin agrandar). Umbrales: portada a sangre ≥1920 · media ≥960 · mosaico ≥600.

## 2. Top 60

`ig/` y `frames/` son relativas a `assets/raw/` y `_plan/diag/`. Foco = x,y en %.

| # | Archivo | Score | Espacio | Recorte @foco | Máx px | Notas |
|---|---|---|---|---|---|---|
| 1 | ig/DM_Ih5dyVKH_07.jpg (P189) | 95,0 | patio techado | 16:9 @50,38 | 1440 | |
| 2 | ig/C9dHAAxJkSi_00.jpg (P073) | 87,4 | fiestas | 4:5 @50,45 | 1333 | el 10 de flores |
| 3 | ig/DAMHps8JVVr_04.jpg (P090) | 85,7 | patio techado | 16:9 @50,40 | 1440 | |
| 4 | ig/DM_Ih5dyVKH_02.jpg (P184) | 84,7 | barra | 4:5 @45,40 | 1440 | |
| 5 | ig/DM_Ih5dyVKH_18.jpg (P200) | 84,7 | barra | 4:5 @55,45 | 1440 | |
| 6 | ig/DAMHps8JVVr_07.jpg (P093) | 84,2 | barra | 4:5 @50,55 | 1360 | barra curva, sin gente |
| 7 | ig/DNT1_BYS_Yf_01.jpg (P204) | 83,5 | barra | 4:5 @35,30 | 1440 | |
| 8 | ig/DU35ZDPCBcH_00.jpg (P254) | 83,5 | barra | 4:5 @50,40 | 1440 | x6,2 likes |
| 9 | ig/DCIEfJUylnY_03.jpg (P124) | 83,2 | barra | 16:9 @45,38 | 1068 | baja res |
| 10 | ig/Dbg3ekilC4P_11.jpg (P348) | 83,0 | fiestas | 4:5 @50,45 | 3072 | violeta, @isosur.prod |
| 11 | ig/CqEI2nSJP2__00.jpg (P036) | 81,7 | equipo | 4:5 @50,40 | 1332 | |
| 12 | ig/DBMtYELSzNS_09.jpg (P109) | 81,4 | barra | 4:5 @55,35 | 1440 | |
| 13 | ig/DNT1_BYS_Yf_18.jpg (P221) | 81,0 | dueños | 4:5 @50,40 | 1440 | violeta, identidad sin confirmar |
| 14 | ig/DaWM8rlo1FR_00.jpg (P333) | 81,0 | equipo | 4:5 @50,40 | 3219 | @isosur.prod |
| 15 | ig/DM_Ih5dyVKH_13.jpg (P195) | 80,0 | equipo | 4:5 @40,40 | 1440 | |
| 16 | ig/DM_Ih5dyVKH_16.jpg (P198) | 80,0 | fiestas | 4:5 @50,35 | 1440 | |
| 17 | ig/Ct7e1vopLTU_00.jpg (P046) | 79,7 | patio techado | 1:1 @50,40 | 873 | baja res |
| 18 | ig/Dbok2NyFNdb_05.jpg (P362) | 78,9 | barra | 4:5 @50,40 | 3072 | luz cálida, 3072 px |
| 19 | ig/DM_Ih5dyVKH_05.jpg (P187) | 78,5 | equipo | 4:5 @50,45 | 1440 | |
| 20 | ig/CpVyxXJJrhO_00.jpg (P031) | 78,1 | barra | 4:5 @50,40 | 1332 | |
| 21 | ig/DNT1_BYS_Yf_07.jpg (P210) | 77,5 | fiestas | 4:5 @45,40 | 1440 | flash, caras |
| 22 | ig/Cqn78DFp5Nm_00.jpg (P039) | 77,1 | terraza | 4:5 @50,45 | 1332 | |
| 23 | ig/DM_Ih5dyVKH_00.jpg (P182) | 77,0 | patio techado | 4:5 @50,40 | 1440 | |
| 24 | ig/DShtzZ0FD9H_13.jpg (P242) | 76,7 | equipo | 4:5 @50,45 | 1440 | disfraz |
| 25 | ig/DShtzZ0FD9H_02.jpg (P231) | 76,7 | barra | 4:5 @45,40 | 1440 | |
| 26 | ig/DYsZ0GNo_88_00.jpg (P297) | 75,8 | tragos | 1:1 @50,45 | 3177 | |
| 27 | ig/DM_Ih5dyVKH_14.jpg (P196) | 75,5 | patio techado | 4:5 @50,40 | 1440 | |
| 28 | ig/CpGaJiYpOd3_00.jpg (P027) | 75,4 | equipo | 4:5 @50,40 | 852 | |
| 29 | ig/DBMtYELSzNS_14.jpg (P114) | 75,1 | sillones | 4:5 @45,45 | 1440 | la única buena |
| 30 | ig/DeNQ8A2lDgg_02.jpg (P393) | 75,0 | comida | 4:5 @50,40 | 3072 | |
| 31 | ig/Dbg3ekilC4P_10.jpg (P347) | 74,2 | dueños | 4:5 @50,35 | 3072 | violeta |
| 32 | ig/DAMHps8JVVr_00.jpg (P086) | 73,9 | tragos | 4:5 @50,50 | 1366 | |
| 33 | ig/DAMHps8JVVr_11.jpg (P097) | 73,9 | tragos | 4:5 @50,55 | 1366 | |
| 34 | ig/DShtzZ0FD9H_00.jpg (P229) | 73,7 | fiestas | 4:5 @50,45 | 1440 | disfraz |
| 35 | ig/Dbg3ekilC4P_02.jpg (P339) | 73,7 | mesas interiores | 4:5 @50,45 | 3072 | |
| 36 | ig/DBMtYELSzNS_00.jpg (P100) | 73,6 | fiestas | 4:5 @50,55 | 1333 | |
| 37 | ig/DBMtYELSzNS_11.jpg (P111) | 73,6 | fiestas | 4:5 @50,40 | 1440 | |
| 38 | ig/DYnU3NTFFQP_07.jpg (P283) | 73,4 | fiestas | 4:5 @45,35 | 3072 | Rucalaf, violeta |
| 39 | ig/Dbok2NyFNdb_02.jpg (P359) | 73,4 | patio techado | 16:9 @50,45 | 3072 | violeta |
| 40 | ig/Co5h1HsJqiK_00.jpg (P025) | 73,1 | equipo | 4:5 @50,40 | 1332 | |
| 41 | ig/CrMRBMNpdIF_00.jpg (P041) | 73,0 | mesas interiores | 4:5 @50,40 | 1332 | |
| 42 | ig/DEP9IUpR9G4_00.jpg (P157) | 72,5 | vista/Castro | 16:9 @50,45 | 1440 | día; también equipo |
| 43 | ig/DBMtYELSzNS_08.jpg (P108) | 72,1 | tragos | 4:5 @50,40 | 1440 | |
| 44 | ig/Dbok2NyFNdb_00.jpg (P357) | 71,9 | terraza | 4:5 @50,50 | 3072 | violeta |
| 45 | ig/CoIvWmcpFBq_00.jpg (P021) | 71,6 | patio techado | 4:5 @50,45 | 1332 | |
| 46 | ig/Cmce2h1J3Wl_00.jpg (P003) | 71,4 | tragos | 4:5 @55,50 | 1280 | |
| 47 | ig/Cp5baHfLpgx_00.jpg (P035) | 70,7 | terraza | 4:5 @50,50 | 1332 | |
| 48 | ig/DYnU3NTFFQP_18.jpg (P294) | 68,7 | mesas interiores | 4:5 @60,40 | 3072 | Rucalaf |
| 49 | frames/V042_banda-mar_7.33s.jpg | 67,0 | vista/Castro | 4:5 @50,40 | 720 | Isleños: pedir permiso |
| 50 | ig/DG8_Ysrybgq_00.jpg (P174) | 63,0 | cuadros/murales | 4:5 @50,50 | 1440 | día |
| 51 | ig/DM_Ih5dyVKH_17.jpg (P199) | 62,0 | fachada | 4:5 @50,40 | 1440 | puerta |
| 52 | ig/DY0AUvhlHjI_00.jpg (P298) | 59,6 | comida | 4:5 @50,50 | 3024 | día |
| 53 | ig/DAMHps8JVVr_05.jpg (P091) | 55,9 | comida | 4:5 @50,50 | 1366 | |
| 54 | ig/C9BDvFvJk4z_00.jpg (V014-cover) | 55,6 | cuadros/murales | 4:5 @50,30 | 1080 | lámpara de pinzas |
| 55 | frames/V031_letrero_0.87s.jpg | 55,4 | fachada | 16:9 @55,40 | 1278 | @estudiouno.prod |
| 56 | frames/V031_mural-ojos_6.60s.jpg | 55,4 | cuadros/murales | 16:9 @50,45 | 1278 | @estudiouno.prod |
| 57 | ig/DY0AUvhlHjI_02.jpg (P299) | 55,4 | comida | 4:5 @50,50 | 3072 | |
| 58 | ig/CnFUpxNpG_E_03.jpg (P012) | 53,9 | cuadros/murales | 16:9 @50,50 | 853 | muro de marcos, baja res |
| 59 | ig/DCIEfJUylnY_15.jpg (P136) | 53,4 | sillones | 16:9 @50,50 | 1071 | baja res, disfraz |
| 60 | frames/V014_sillones_9.30s.jpg | 31,1 | sillones | 4:5 @50,65 | 720 | Chesterfield, muy oscuro |

**Proporciones:** 4:5 = 49 y 16:9 = 9 → 97 % en los dos ratios (mínimo 75 %); dos 1:1 de excepción. Cada fila del CSV trae un `crop_alt` con su ancho (toda vertical de 1440 da un 16:9 de 1440×810).
**Luz:** noche cálida 49 · violeta 6 · día 4 · flash 1. **Anchos:** solo 13 archivos llegan a ≥1920 (todos de 2026, 3072 px); 42 sirven a media pantalla y 5 solo a mosaico.

## 3. Cobertura (ver `top60/coverage.jpg`)

| Espacio | En top 60 | Mejores 2 | Estado |
|---|---|---|---|
| Barra | 10 | P184, P200 (y P093 de lugar) | sobra |
| Equipo/personal | 7 | P036, P333 | sobra |
| Patio techado | 7 | P189, P090 | sobra |
| Fiestas/eventos | 8 | P073, P348 | sobra |
| Tragos | 5 | P297, P086 | bien |
| Comida | 4 | P393, P298 | justo: platos de día (@estudiouno.prod) o de noche sin cuento |
| Terraza descubierta | 3 | P039, P357 | justo: P357 es violeta |
| Mesas interiores | 3 | P339, P041 | justo: no hay un plano limpio del salón vacío |
| Cuadros/murales | 4 | P174, lámpara de pinzas (V014-cover) | débil: los marcos solo en P012 (853 px) y en la story V084 (480p, reserva) |
| Sillones | 3 | P114, P136 | **crítico**: P114 es la única nítida; el rincón Chesterfield solo existe en un frame oscuro (V014 a 9,3 s) |
| Fachada/letrero | 2 | P199, V031 a 0,9 s | débil: sin foto de la fachada desde la calle. V056 a 6,2 s la muestra, pero con creador y subtítulos |
| Vista/Castro | 2 | P157, V042 a 7,3 s | débil: V042 es de terceros. Reservas propias: V010 a 0 s, V028 a 1,8 s, P020 (960 px) |
| Dueños | 2 | P221, P347 | identidad sin confirmar: no se rotula a nadie |

## 4. Portada: 8 candidatas (ver `top60/heroes.jpg`)

1. **H1 · V031 1,0–10,4 s** (escritorio): único horizontal propio y sin texto quemado en ese tramo (letrero → puerta → banderines → ojos → lámparas). Poster `frames/V031_letrero_0.87s.jpg`. Es 720p: textura con `brightness(.85)` + scrim, nunca foto nítida. Crédito @estudiouno.prod.
2. **H2 · V009 0–7,1 s** (móvil 9:16): techo de flecos en paneo; el loop no se nota, sin caras ni texto. Poster `frames/V009_techo-flecos_2.00s.jpg`.
3. **H3 · P189**: la #1, colores de la marca y gente en noche cálida. 16:9 de 1440: banda contenida, no llena 1920.
4. **H4 · P362**: **la única fija a ≥1920 en luz cálida** (3072): muro rojo, cartel ALMUD, gesto del bartender. Foto sostenida o 16:9 a sangre.
5. **H5 · P090**: faroles y flecos, abstracta y cálida; aguanta texto con scrim. 1440.
6. **H6 · P093**: la barra curva entera, foto de lugar para split o "marco que crece". 1440.
7. **H7 · P124**: la botella en el aire, el gesto más fuerte, pero 1068 px: media pantalla o split.
8. **H8 · P348**: 12 años desde arriba, 3072 px, violeta: solo para el cuento "aniversarios".

**Recomendación:** H1 escritorio + H2 móvil; primera banda a sangre H4; H3 y H5 en bandas a ≤1440; H6 + H7 como split de la barra.

## 5. Familia de luz: decisión

**Noche cálida** (ámbar-brasa sobre casi negro, muro rosa-rojo) es la familia única: 49 de 60 y 10 de las 12 primeras. El violeta (6, todo 2026) entra solo en "aniversarios/fiesta" y en mosaico (P348, P359, P221, P347), nunca como foto decisiva salvo P357 (no hay otra terraza nocturna en alta). El día (P157, P174, P298, V042) se agrupa en un capítulo "de día / el mar" con corte duro. Flash y B/N (P210, P346, P252) quedan de reserva. Tratamiento único: `brightness(.85) contrast(1.05)`.

## 6. Qué falta y cómo lo resuelve la v2

- **Sillones:** P114 es la foto decisiva a media pantalla; el frame Chesterfield (V014 9,3 s) y P136 solo en mosaico chico. Pedir una toma nocturna.
- **Cuadros/marcos:** el mural de ojos va en movimiento (V031 6,6–8 s dentro del loop, V006 9,7 s); corazones con el equipo (P174); la lámpara de pinzas (V014-cover) como motivo propio; el muro de marcos solo en miniatura (P012; reserva V084 9,1 s, 480p).
- **Fachada:** letrero de V031 (0,9 s) como poster y cierre; P199 (puerta) en "cómo llegar". Falta la fachada de día desde la calle (V056 6,2 s la tiene, pero con creador y subtítulos).
- **Vista/Castro:** P157 en banda 16:9 de 1440; frames V010/V028 en mosaico; V042 solo con permiso de Isleños.
- **Resolución:** nada se agranda. En 1920 las bandas van a `max-width:1440px` o se usan las de 3072 (P362, P333, P339, P393, P297). `srcset` 600/960/1440 (+1920/2560 en las de 3072).
- **Mesas interiores:** mosaico de una misma noche cálida (P339, P041, frame V020 15,7 s). Falta un plano limpio del salón.
- **Terceros y créditos:** Rucalaf (P283, P294: confirmar locación), Isleños (V042), creadores (V056, fuera del top). Créditos @isosur.prod (P333, P348, P362) y @estudiouno.prod (V031, V028, P298, P164).
- **Frames extraídos** (`frames/`, 26): V031 letrero/puerta/banderines/ojos/lámparas · V009 flecos · V084 marcos ×2 · V014 sillones · V013 salón con cuadros, equipo con poleras · V020 salón · V006 ojos, patio con mar · V002 corazones ×2, techado de cintas · V010 patio-mar · V028 brindis-mar · V042 Isleños · V056 fachada · V021 muro con cartel, torta 10 · V023 barra · V032 flecos de día · V038 coupe.
