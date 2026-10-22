# Ronda 2b · Agentes ALMUD CARTA + ALMUD COLOR (commit 090a76d)

## Qué revisé

- **Páginas:** `/v3/carta/` y las secciones Tragos y Comida de `/v3/`. Las sirvo en local en el puerto 8853. `v3/` y `public/v3/` son idénticos (`cmp`).
- **Herramienta:** Playwright/Chromium a 390×844 y 1440×900, en ES y EN. Medí también 1024 para las pestañas.
- **Capturas:** `_plan/v3/ronda2/carta-color-b/`.
- **Datos crudos:** `_plan/v3/ronda2/carta-color-b-audit.json`.
- No edité el sitio.
- **Nota sobre las capturas:** en los recortes de sección se ven el nav y el enlace «Saltar al contenido» encima del contenido. Es un artefacto de la captura por elemento, no del sitio: `.skip` está en `top:-60px` y solo baja con `:focus`.

## Verificaciones

| Prueba | Resultado |
|---|---|
| DOM vs `carta-v2.json` | **256/256**: 135 filas de lista y 121 filas de tabla. Nombres exactos y **0 precios distintos** |
| Una sección por pestaña y un subgrupo por chip | OK: 7/7 y 29/29 a 390 y 1440 |
| Chip activo al entrar por enlace (390) | **Arreglado.** «Somos dulzones» queda en x 197–318, «Tequilazos» en 146–318 y «Por copa» en 238–318 |
| Pestañas en 1440 | **Arreglado.** Entran las 7 sin desplazamiento; «Nuestras promos» termina en x = 1258 |
| Pestañas en 1024 | Pasan a 2 filas, con «Nuestras promos» sola en la segunda. Se lee, pero se ve accidental |
| Primer ítem (390) | Casa a 219 px, Comilona a unos 333 px y Espirituosos a unos 413 px, incluidas la cinta y las notas. Antes estaba en 450–700 px |
| Tabla NORMAL / XL | Cabeceras literales del PDF y precios tabulares alineados. A 390 la fila mide 48–70 px, antes eran unos 130 |
| Hoja | 880 px en escritorio. Tintes: papel (Espirituosos y Sin), rosa 7 % (Casa, Mundo, Vinos) y dorado 12 % (Comilona, Promos). Se fue el gris |
| EN | Las 7 pestañas y los chips traducidos; quedan 0 nodos `data-en` sin cambiar. Los nombres de la carta quedan intactos |
| Enlaces | Un solo DM (el de la nav, `ig.me/m/almud_bar`). PDF `uqr.to/ppvi`. Logo a `/v3/` |
| Consola | 0 errores |
| Destacados del home | Enlazan a `#casa`, `#mocktails-…-de-la-casa`, `#comilona-picoteos`, `#comilona-greditas` y `#comilona-pizzas-artesanales`. Los precios coinciden con el JSON |

## Contraste en pares reales (390, ES y EN)

| Par | Ratio | Uso |
|---|---|---|
| `#b01a2e` sobre la hoja rosa/dorada | 5.33 / 5.39 | «NUEVO» y los días, 16 px. Antes daba 4.51 |
| `#3a3ad8` sobre la hoja | 5.83–6.32 | nombres; la etiqueta Veggie da 5.89 |
| `#160d0b` sobre la hoja | 14.8–16.0 | precios y texto |
| `#f5e9db` sobre la cinta `#142a5c` | 11.59 | cintas |
| Home: kicker `#f7cfc4` sobre `#a8222d` | 5.01 | el mínimo; el resto queda ≥5.19 |

**Todo pasa AA, y ahora con margen.**

---

## CARTA · **17/20** (ronda 2: 16)

**Lo que la sube:**
- La hoja ya es *su* carta: nombres en azul rey de imprenta, cintas, precios en negro.
- Espirituosos y Vermú en tabla, como el PDF. Es el mayor salto de usabilidad: los 26 piscos se recorren en unas 3 pantallas.
- Cabezal compacto.
- Chips fijos que muestran el activo.
- Las 7 pestañas visibles en escritorio.
- En escritorio la hoja de 880 px deja el precio cerca del nombre.
- EN completo.

**Lo que falta para 18+:**
1. **Destacados del home: falta coherencia entre foto e ítem.**
   - **Comida:** la foto grande es una pizza con trozos de carne, cebolla morada y hojas verdes (P036). El ítem listado es **Huerta sabrosa**, que es vegetariana (tomate cherry, champiñones, hojas). Por ingredientes, la foto parece la **Zorrona** ($ 16.900: carne en trozos, cebolla morada, champiñones, hojas verdes). Hay que confirmarlo con Carmen y listar esa, o no nombrar la pizza de la foto.
   - **Tragos:** la copa salpicada (P297) y los tres sours con gypsophila no tienen nombre. Sagüer on Faia y Sangría Foreva! aparecen sin foto. El lector las cruza mal: cree que los sours son el Sagüer. Hay dos salidas:
     - poner un pie con el nombre real de cada foto, si es de la carta;
     - o volver a las fotos del Sagüer (soplete) y de la Sangría junto a su línea.
2. **Pestañas en 1024–1200:** evitar el huérfano. Bajar el padding a 10 px y el tracking a .02 em entre 1024 y 1279, o dejar la fila deslizable con fundido como en el celular.
3. **(Fidelidad) Ingredientes en negrita** como en la impresa («va con **Vodka Pera**…). Es una marca `<b>` en el JSON o en el generador. Es lo último que separa la descripción web de la impresa.
4. (Menor) **Cabezal en 1440:** «LA CARTA» queda corrido a la izquierda del eje de la hoja y la bajada está pegada a la derecha. Conviene alinear las dos al borde izquierdo de la hoja de 880 px, para que el ojo baje en línea recta.
5. (Opcional) En las tablas largas (Gin, 40 filas), dejar la cabecera de columnas `position:sticky` bajo los chips.

## COLOR · **18/20** (ronda 2: 17)

**Lo que la sube:**
- El azul `#3a3ad8` del impreso solo en la hoja.
- Tres tintes cálidos y sin gris.
- `#b01a2e` con margen.
- Precios en negro.
- Un solo CTA rosa (DM en la nav).
- Fondo de página único `--noche`.
- Por pantalla de carta: el azul del logo, la tinta de las cintas y el azul de los nombres. En Promos se suma el rojo tinta de los días. No hay arcoíris.
- En el home: Tragos usa muro con P362 (muro rosa dentro de la foto), Comida va sobre noche-2 con el ámbar solo en el titular, y todo pasa AA.

**Para 19+:**
1. **Promos junta tres tintas sobre la hoja dorada:** día en rojo, nombre en azul y precio en negro. Propuesta: el día en `--noche` 600 con tracking, o en negrita, para dejar un solo acento (el azul de los nombres).
2. **Tragos (home):** la foto de P362 (pared rosa) sobre el fondo plano muro `#a8222d` se funde en los bordes: rojo sobre rojo. Ayudaría un filo de 1 px `rgba(22,13,11,.35)`, o pasar la foto a sangre hasta el borde de la sección en el celular.
3. (Decisión de Carmen) La cinta en carbón `#403c3d`, como el impreso, o en tinta, como ahora. Las dos pasan. No resta puntos.

## Lista corta para llegar a 18+ en las dos notas

| # | Cambio | Archivo |
|---|---|---|
| 1 | Pizza del home: confirmar la de P036 y listar esa (probable **Zorrona $ 16.900**) en vez de Huerta sabrosa | `v3/index.html` (#comida) |
| 2 | Tragos del home: pie con el nombre en las fotos de la salpicada y de los sours, o volver a las fotos del Sagüer y la Sangría junto a su línea | `v3/index.html` (#tragos) |
| 3 | Pestañas 1024–1279: sin huérfano (padding y tracking menores, o fila deslizable) | `css/v3/carta.css` |
| 4 | Negrita en los ingredientes de las descripciones, según el PDF | `content/carta-v2.json` y el generador |
| 5 | Promos: día en `--noche` 600 en vez de `#b01a2e` | `carta.css` (`.pr__dia`) |
| 6 | Cabezal 1440 alineado al borde izquierdo de la hoja | `carta.css` (`.carta__head`) |

**Notas ronda 2b:** CARTA 17/20 · COLOR 18/20. Con los puntos 1, 2 y 3, CARTA llega a 18. Con el 4, a 19.
