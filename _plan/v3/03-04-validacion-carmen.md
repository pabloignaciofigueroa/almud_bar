# Validación de Carmen Paz · Tipografía (fase 3) y Paleta (fase 4)

> Revisé las láminas `_plan/v3/03-tipografia.jpg` y `_plan/v3/04-paleta.jpg`, y los documentos `brand/typography-v3.md` y `brand/palette-v3.md`.

## Veredicto: **APROBADO CON CAMBIOS**

Me representa: es de noche, cálida y condensada, como mis afiches y mi letrero. Se lee. Puede ser premium si se corrigen los puntos de abajo. Ninguno obliga a empezar de nuevo.

---

## Tipografía

**¿Me representa?** Sí. Big Shoulders Display 800 en mayúsculas es la voz de mis afiches (MAMBO TIKI, CHUPATELO): titulares altos, gruesos y alegres. Barlow Condensed para el texto también va con mi identidad angosta. Estoy de acuerdo con sacar la manuscrita (Caveat).

**¿Se lee?** Los títulos, perfecto. En la lámina de celular, el texto corrido se ve chico, delgado y apretado. La descripción del "Aquí te las traigo Peter" casi cuesta leerla.

**¿Es premium?** Los títulos sí. El logo de la lámina no.

### Cambios de tipografía
1. **El logo no se escribe con una fuente.** En la lámina, "ALMUD" sale en Six Caps finita y "BAR" en una letra delgada y gris. Mi letrero es grueso, inclinado, con ALMUD blanco y BAR azul, y lleva el isotipo. En la web se usa siempre el SVG de `brand/` (`almud-horizontal-oscuro.svg` / `almud-logotipo.svg`). Six Caps queda fuera de la web. Si se mantiene en algún lado, solo como decoración ≥ 120 px y nunca en lugar del logo.
2. **Texto corrido en celular:** Barlow Condensed **500** (no 400), **18 px mínimo** con interlineado **1,5**, color `--papel` #f5e9db. El 400 sobre noche se ve débil. Escritorio: 20 px / 1,5, con medida ≤ 48 caracteres (eso está bien).
3. **Texto secundario** (horario, dirección, ingredientes): 16 px como piso absoluto, 500. Nada bajo 16 px, ni siquiera los rótulos.
4. **Rótulos/kicker en mayúsculas** (TRAGOS, COMIDA, "LA BARRA · EL SALÓN"): Barlow Condensed 600 con **tracking +0,06 em** y 14–15 px. Así se ven finos y no gritan.
5. **Títulos:** celular 44 px está bien, pero **máximo 3 líneas**. "PA CHUPARSE EL BIGOTELI" en 2–3 líneas grandes es demasiado. Escritorio: tope **120 px** (136 es mucho para una frase larga), interlineado 0,92–0,95 y tracking −0,01 em.
6. **Precios:** Barlow Condensed 600, 20 px, en `--papel` (no en rosa). En la lámina el precio rosa compite con el título. El rosa queda para la acción.
7. **Las frases de muestra no son el copy final.** "NOS GUSTA EL COLORSSSS!" y "NO SOMOS NÁ SIN USTEDES!" me sirven. "PA CHUPARSE EL BIGOTELI" y "MEJOR LOS TOMAMOS TODOS!" no van como titulares de la web: son de caption. Como mucho, dentro de la descripción de un plato o de un trago.

---

## Paleta

**¿Me representa?** Sí, mucho más que la v1. La noche marrón #160d0b es la de mis fotos, no un violeta de discoteca. El muro rosa como acento principal y el azul del letrero como secundario son exactamente lo mío. Celebro que se hayan ido el arcoíris y la franja de colores: mis colores ya están en las fotos.

**¿Se lee?** Sí. Los contrastes están calculados y pasan. Me gusta que corrigieran los pares que fallaban.

**¿Es premium?** Noche, papel y muro rosa, sí. Las pantallas planas de ámbar y de azul tinta, tal como están en la lámina, se ven de marca de cereal o de club deportivo, no de coctelería.

### Cambios de paleta
1. **La lámina de tipografía no usa la paleta v3.** Su fondo es violáceo (#150b13, la noche vieja de la v1) y el titular amarillo (#f7bf50) no existe en la v3. Hay que rehacerla con `--noche` #160d0b, y no quiero amarillo suelto en la web.
2. **Agregar un `--dorado` #d9a441** (sale del dorado de mis afiches, #d59f31): es el color de aniversarios y eventos (9º aniversario, 12 años). Uso: **solo** títulos y marcas en la sección Eventos y en detalles de aniversario. Contraste: 6,16 sobre `--tinta` y 8,52 sobre `--noche`. **Reemplaza al rosa como marca de "próximo" en Eventos**, porque el rosa sobre tinta da 3,76 y apenas pasa.
3. **Ámbar #e5a05c como fondo de sección: reducirlo.** Una pantalla completa naranja con letra negra no es Almud. Propuesta: Comida va sobre `--noche-2` #22140f, con las fotos de los platos a sangre, y el ámbar se usa solo como banda o titular (ámbar sobre noche) o en una franja angosta. Si se insiste en el fondo ámbar, que sea un bloque chico, nunca una pantalla entera en el celular.
4. **Tinta #142a5c como fondo de Eventos:** lo acepto, porque viene de mi letrero y de la carta, siempre que lleve una foto o un afiche mío dentro. Sin foto, el azul plano se ve institucional.
5. **Muro #a8222d (Tragos):** sí, es mi pared en sombra. El botón ahí en `--papel` con texto `--noche` está bien.
6. **Letrero azul #2aa1f8:** solo para el "BAR" del logo, el anillo de foco y enlaces chicos. No como color de bloques ni de títulos: en grande se ve tecnológico.
7. **`--papel-2` #c8af9c para texto secundario:** subirlo a **#d8c2b0** (11,18 sobre noche). Con letra condensada, el #c8af9c se apaga.
8. **Botones:** la píldora completamente redonda se ve de app. Quiero **radio 4 px**, mayúsculas Barlow Condensed 600 a 16–18 px y altura ≥ 48 px. Así quedan rectos y firmes, como el letrero.

### Sobre "RESERVAR"
**En Almud no hay reservas online.** No quiero ver "RESERVAR" en ninguna parte de la web, ni como ejemplo en las láminas finales. Los botones reales son:
- **"VER LA CARTA"** (principal, muro rosa).
- **"ESCRÍBENOS POR DM"** → abre instagram.com/almud_bar (para grupos y consultas).
- **"CÓMO LLEGAR"** → mapa de Serrano 325.

---

## Lista corta de cambios (para el equipo)
| # | Qué | Valor |
|---|---|---|
| T1 | Logo siempre en SVG, Six Caps fuera del logo | `brand/almud-horizontal-oscuro.svg` |
| T2 | Texto corrido | Barlow Condensed 500, 18 px / 1,5 (cel) · 20 px (escr.) |
| T3 | Piso de tamaño | 16 px |
| T4 | Kicker | Barlow Condensed 600, 14–15 px, +0,06 em |
| T5 | Título | 44 px cel, máx. 120 px escr., máx. 3 líneas, lh 0,92–0,95 |
| T6 | Precio | 600, 20 px, `--papel` |
| P1 | Rehacer lámina 03 con la paleta v3 | fondo #160d0b, sin #f7bf50 |
| P2 | Nuevo `--dorado` | #d9a441, solo Eventos y aniversarios, marca "próximo" |
| P3 | Comida sin pantalla ámbar completa | fondo #22140f + ámbar como acento |
| P4 | Eventos en tinta solo con foto o afiche | #142a5c |
| P5 | `--papel-2` | #c8af9c → #d8c2b0 |
| P6 | Azul solo para BAR, foco y enlaces | #2aa1f8 |
| P7 | Botones | radio 4 px, 600, ≥ 48 px de alto |
| P8 | Sin "RESERVAR" | VER LA CARTA · ESCRÍBENOS POR DM · CÓMO LLEGAR |

— Carmen Paz
