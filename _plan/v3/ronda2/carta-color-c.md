# Ronda 2c · Agentes ALMUD CARTA + ALMUD COLOR (commit 11c0784)

## Qué revisé

- **Páginas:** `/v3/carta/` y las secciones Tragos y Comida de `/v3/`. Las serví en local en el puerto 8863. `v3/` y `public/v3/` son idénticos (`cmp`).
- **Herramienta:** Playwright/Chromium a 390×844 y 1440×900, en ES y EN. Medí también 1024, 1100, 1280 y 1920 para la fila de pestañas.
- **Capturas:** `_plan/v3/ronda2/carta-color-c/`. Las de sección del home se tomaron ocultando el nav fijo.
- **Datos crudos:** `_plan/v3/ronda2/carta-color-c-audit.json`.
- No se editó el sitio.

## Verificaciones

| Prueba | Resultado |
|---|---|
| DOM vs `carta-v2.json` | **256/256** nombres exactos, **0** precios distintos |
| Pestañas y subgrupos | 7/7 y 29/29 a 390 y 1440. 0 errores de consola. EN: 0 nodos `data-en` sin traducir |
| 7 pestañas en una fila | **OK** a 1024, 1100, 1280, 1440 y 1920, sin desplazamiento. A 1024 la pestaña baja a **15 px** con padding de 9 px (desde 1280 ya son 16 px) |
| Cabezal | Alineado al borde del contenido de la hoja: «LA CARTA» empieza en x = 352, que es el borde de la hoja (280) + 72 de padding, a 1440 |
| Cabecera de tabla fija | **OK.** En Gin (40 filas), a scroll 900 y 2500 la `thead` queda en y = 185–235, justo bajo los chips |
| Negritas de ingredientes | 22 `<b>` en 600 y `--noche`: **20 en Casa** y 2 en Espirituosos. Comilona tiene 0, pero el impreso sí las usa ahí («**Especial pa compartir:**», «**Entre ponerle y no ponerle**») |
| Día de Promos | `--noche` 600. La línea de Promos queda con un solo acento (azul) |
| Filo de P362 | `box-shadow: 0 0 0 1px rgba(22,13,11,.4)` + sombra. Ya no se funde con el muro |
| Destacados del home | Cada foto tiene su nombre literal debajo (Sagüer on Faia, Sangría Foreva!, Peter, La moto chantá, Tukulito, Camarón). «Pizzas artesanales» va sin precio y enlaza a `#comilona-pizzas-artesanales`. Los 6 precios coinciden con el JSON |

## Contraste (pares reales, 390, ES y EN)

| Par | Ratio |
|---|---|
| Nombres `#3a3ad8` sobre la hoja | 5.83–6.32 |
| «NUEVO» `#b01a2e` sobre la hoja | 5.33 |
| Precios, días y negritas `--noche` sobre la hoja | 14.8–16 |
| Cintas | 11.59 |
| Home (mínimo) | 5.01 |

**Todo pasa AA con margen.**

---

## CARTA · **18/20** (2b: 17)

Ya se siente *su* carta: hoja clara, nombres en azul de imprenta, cintas, negritas en los ingredientes de la Coctelería de la casa y tablas NORMAL/XL con cabecera fija. En el celular se usa bien: el primer ítem está a unos 220 px, los chips son fijos y el chip activo se ve. Los destacados del home ya son honestos: cada foto lleva su nombre literal y la pizza no promete un ítem que no se puede identificar.

**Lo que queda (para 19–20):**
1. **Hay contenido que se transparenta bajo los chips fijos.** El fundido de 64 px a la derecha de `.chips` (`mask-image`) también vuelve transparente el fondo de la fila. Al bajar por una tabla, el precio de la fila de abajo se ve detrás («$ 10.500» fantasma en `carta-390-gin-scroll2500.jpg`). Arreglo: aplicar la máscara a un contenedor interno de los chips y no a la fila que lleva el fondo, o poner un `::before` con `var(--hoja)` detrás.
2. **Faltan negritas en Comilona y en otros grupos donde el impreso las tiene:** «Especial pa compartir:», «Entre ponerle y no ponerle», etc. Hoy solo están en Casa.
3. **La cabecera de columna «CORTO [90 cc]» se corta en 2 líneas a 390** («CORTO [90 / cc]»). Usar `white-space:nowrap` en la medida, o partir la línea antes del corchete: «CORTO / [90 cc]».
4. (Menor) Las pestañas a **15 px** en 1024 rompen el piso de 16 px de Carmen. Se puede volver a 16 px y bajar el tracking a 0, o abreviar en EN y ES entre 1024 y 1279.

## COLOR · **19/20** (2b: 18)

La paleta es fiel y cada pantalla tiene un solo acento real:
- **Carta:** el azul de imprenta en los nombres. El azul del logo, la tinta de las cintas y el chip activo son estructura.
- **Promos:** ahora tiene un solo acento.
- **Home:** Tragos va sobre muro con P362 enmarcada; Comida va sobre noche-2 con el ámbar solo en el titular.

No hay arcoíris ni colores fuera de la paleta, y todo pasa AA con margen.

**Lo que queda (para 20):**
- La cinta en carbón `#403c3d`, como el impreso, o en tinta, como ahora. Las dos pasan. Es una decisión de Carmen, no un defecto.
- El fantasma bajo los chips fijos (punto 1 de Carta) también es una mancha de color: un precio negro se ve a medio fundir sobre la hoja.

## Lista corta

| # | Cambio | Archivo |
|---|---|---|
| 1 | Máscara de `.chips` en un contenedor interno, o fondo sólido detrás del fundido | `css/v3/carta.css` |
| 2 | Negritas medidas del PDF también en Comilona (y en Mundo y Sin si aplica) | `content/carta-v2.json` y el generador |
| 3 | Cabeceras de tabla sin cortes raros a 390 (`nowrap` en la medida o salto antes del corchete) | `carta.css` (`.tbl__c`) |
| 4 | Pestañas a 16 px también entre 1024 y 1279 | `carta.css` |

**Notas ronda 2c:** CARTA 18/20 · COLOR 19/20.
