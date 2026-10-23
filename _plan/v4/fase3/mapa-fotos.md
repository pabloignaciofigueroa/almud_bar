# v4 · Fase 3 · Mapa de fotos de /nueva_v2/

Principio del cliente: «la mejor manera de vender un bar es mostrar que siempre está lleno». La protagonista es la multitud, no el barman ni los dueños.

- **Antes:** 27 fotos + 14 videos. **Después:** 52 fotos + 14 videos (los mismos videos, en el mismo lugar).
- Fotos nuevas: 25. Trece ya tenían recorte en `assets/v3` y se reutilizan sin recodificar; doce son recortes nuevos en `assets/nv2/img`, hechos con `tools/media_nv2.py` desde `tools/media_nv2.json`.
- Los nombres y precios son literales de `content/carta-v2.json`. Un plato o trago lleva nombre solo si la foto muestra ese plato. Las glosas EN salen de `content/carta-glosas-en-v3.json`.
- Todas las fotos nuevas cargan diferido (`data-src`/`data-srcset`), con `srcset` AVIF + WebP de 480 a 1440 px y `sizes` según su ancho real en la grilla.

## Fotos nuevas (25)

| # | Foto (id) | Fuente · ref | Sección | Rótulo | Por qué (Instagram / ranking) |
|---|---|---|---|---|---|
| 1 | `lugar-techada-llena` | DM_Ih5dyVKH_14 · P196 | El lugar, franja «lleno» | — | [IG-050] 11 años, día 1: terraza techada con todas las mesas ocupadas bajo las cintas. Ranking #27 (techado, multitud) |
| 2 | `lugar-salon-lleno` | DM_Ih5dyVKH_03 · P185 | El lugar | — | [IG-050] «a tod@s nuestros fieles amiguis que siempre nos acompañan». Muestra el local lleno, no vacío |
| 3 | `lugar-terraza-repleta` | Dbok2NyFNdb_02 · P359 | El lugar | — | [IG-008] 12 años, «carretitos como este, llenos de güena ondi». Ranking #39, terraza repleta vista desde arriba (@isosur.prod) |
| 4 | `tragos-copa-tallada` | DAMHps8JVVr_11 · P097 | Tragos, banda de ambiente | — | Selección del jurado (Los tragos). [IG-079] La copa no se puede identificar en la carta, así que va sin nombre |
| 5 | `tragos-old-fashioned` | Cmce2h1J3Wl_00 · P003 | Tragos, banda | — | Selección del jurado (Carta). [IG-178] lo llama «EN QUÉ TOPAMOH?!», que ya no está en la carta actual: va sin nombre |
| 6 | `eventos-negroni-week` (foto de un negroni) | DP7O0BElPhW_00 · P226 | Tragos, banda | — | [IG-042] «cómo estamoh pa un Negroni?». Es un negroni de la casa y no del evento Negroni Week, por eso no va en Eventos |
| 7 | `tragos-brindis-copas` | DBMtYELSzNS_08 · P108 | Tragos, banda | — | [IG-075] primavera, «pa compartir». Un brindis de dos copas: la gente sin mostrar caras. Ranking #43 |
| 8 | `carta-olvidar` | DeC9NEioZFw_00 · V057 | Tragos con nombre | **Cómo te voy a olvidar** · $ 6.800 | [IG-002] el post nombra el trago y muestra el vino que lo tiñe; la foto es ese trago |
| 9 | `carta-coquette` | C9xrKP8Jehi_00 · P074 | Tragos con nombre | **A veces me pongo Coquette** · $ 7.100 | [IG-096] #avecesmepongocoquette: el trago rosado y cremoso de la carta, entregado a una clienta |
| 10 | `comida-ceviche` | DY0AUvhlHjI_00 · P298 | Comida | **Todo que ver!** · $ 16.000 | [IG-022] «una cocina sencilla pero más que sabrosona!». Se identifica por los ingredientes: es el único ceviche de la carta (atún rojo, pimentón amarillo, palta, cebolla morada, cilantro, pan de la casa) |
| 11 | `comida-hamburguesa` | DY0AUvhlHjI_13 · P305 | Comida | **Chambreao** · $ 10.900 | [IG-022]. Hamburguesa de vacuno con queso derretido, cebolla caramelizada y hojas verdes: coincide con la descripción de la carta |
| 12 | `carta-camaron` | DAbw0xKSimd_00 · P099 | Comida | **Camarón que se duerme** · $ 15.900 | [IG-077] «cáchese esta gredita». La greda tiene camarones, champiñones y salsa de queso crema |
| 13 | `carta-contuti` | DEVtFfySKVY_00 · P158 | Comida | **Con tuti si no pa qué!** · $ 19.900 | [IG-066] el post se llama igual que el plato («CON TUTI SI NO PA QUÉ!»). Es la tabla para compartir: el plato de la multitud |
| 14 | `quien-sillones-llenos` | Dbg3ekilC4P_19 · P356 | Con quién, columna 1 | — | [IG-009] 12 años: un grupo grande sentado junto, bajo los banderines |
| 15 | `quien-carcajadas` | DAMHps8JVVr_09 · P095 | Con quién, columna 1 | — | [IG-079] «ya sabe ya que no somos ná sin ustedes»: una mesa riendo a carcajadas |
| 16 | `quien-grupo-peter` | DYiMMUrlBk1_04 · P260 | Con quién, columna 2 | — | [IG-026] es el post de las «sociales» de los parroquianos y repite el título de la sección: «Ya saben que no somos ná sin ustedes!» |
| 17 | `quien-copas-arriba` | DNT1_BYS_Yf_06 · P209 | Con quién, columna 2 | — | [IG-047] 11 años, «el japi berdey más celebrao»: un grupo con las copas en alto |
| 18 | `quien-grupo-flecos` | DYiMMUrlBk1_01 · P257 | Con quién, columna 3 | — | [IG-026] parroquianos bajo las lámparas de flecos |
| 19 | `quien-mesa-llena` | DYiMMUrlBk1_10 · P266 | Con quién, cierre a lo ancho | — | [IG-026] una mesa larga de amigas. En el celular cierra la sección a lo ancho, sin hueco |
| 20 | `eventos-cotillon-12` | Dbg3ekilC4P_17 · P354 | Eventos, tira de fiestas | — | [IG-009] 12 años, «guanderful jornada recreativa cumpleañística». Coronas y antifaces: los disfraces solo van en Eventos. Reemplaza a P349, que era el mismo instante de la foto de Aniversario |
| 21 | `eventos-baile-12` | Dbok2NyFNdb_18 · P375 | Eventos, tira | — | [IG-008] «muchísima energía fiestera y risas»: la gente baila apretada |
| 22 | `eventos-primavera` | DBMtYELSzNS_02 · P102 | Eventos, tira | — | [IG-075] «nuestro día de bienvenida a la esperada primavera»: mesas llenas bajo los banderines |
| 23 | `eventos-10-anos` | C9dHAAxJkSi_00 · P073 | Eventos, tira | — | [IG-100] «GRACIAS por estos 10 años». Ranking #2. Era la favorita de Carmen «de evento»; en la tira sí tiene contexto, junto a las otras fiestas |
| 24 | `equipo-duo` | DaWM8rlo1FR_00 · P333 | Equipo, cierra la fila (recorte 3:2 en escritorio) | — | [IG-014] «Nuestras chicas super poderosas… @milagroosjm y @lizzearellano». Es el equipo actual confirmado |
| 25 | `donde-puerta` | DM_Ih5dyVKH_17 · P199 | Cuándo y dónde, junto a la dirección | — | Selección del jurado (Cuándo y dónde): la puerta de madera con el megáfono y la polera «Te espero en la cuneta». La puerta es justamente la dirección |

Las fotos 4–6, 8–13, 22–25 vienen de `assets/v3` (ya estaban recortadas, pero la página no las mostraba). Las fotos 1–3, 7 y 14–21 son recortes nuevos en `assets/nv2`.

## Conteo por sección (fotos, sin videos)

| Sección | Antes | Después | Videos (sin cambios) |
|---|---|---|---|
| El lugar | 6 | 9 | lugar-noche |
| Tragos | 6 | 12 | coctelera, humo |
| Comida | 2 | 6 | carne, queso |
| Con quién | 6 | 12 | multitud 1 (arriba a la izq.), 2 (al medio de la der.), 3 (abajo al centro) |
| Eventos | 2 | 6 | fiesta 12, jalogüín |
| Equipo | 5 | 6 | dueños (primero, a la izquierda) |
| Cuándo y dónde | 0 | 1 | terraza |
| **Total** | **27** | **52** | 14 con la portada |

## Descartadas en esta fase

| Foto | Motivo |
|---|---|
| `equipo-grupo` (C-bY0mLNYRz, IG-091) | Es de 2024 y etiqueta a personas que ya no figuran en el equipo de 2025 (IG-050), como @k.o_ds. **Duda para el cliente** |
| `equipo-elymar` (P396) | Lleva disfraz (tiara y alas) fuera de Eventos |
| P198 (hombre que brinda) | Primer plano de una sola persona que no es del equipo |
| P349 (brazos arriba, 12 años) | Mismo instante que la foto de Aniversario (P348) |
| DM_Ih5dyVKH_01/02/09/18 (bartenders, 11 años) | [IG-050] agradece a bartenders invitados de @elgobernadorofficialcl: pueden ser terceros. Además, el protagonista no es el barman |
| DJ de IG-050 y músicos de IG-075 | Terceros (músicos invitados) |
| `lugar-salon`, `lugar-cuadros`, frames de 720 px | Baja resolución |
| `eventos-14f`, afiches de Negroni Week | Llevan texto encima |
| P242, P229, P234 (Jalogüín) | Disfraces: Jalogüín ya está como video en Eventos |
