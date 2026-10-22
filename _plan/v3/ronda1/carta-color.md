# Ronda 1 · Agentes ALMUD CARTA + ALMUD COLOR

Revisé `/v3/` y `/v3/carta/` servidos en local (puerto 8843) con Playwright/Chromium a 390×844 (vista principal), 768×1024 y 1440×900. Probé las 7 pestañas y los 29 subgrupos en los tres anchos, el cambio a EN, los enlaces (PDF, DM, logo→`/v3/`), los deep links por hash y el teclado (flechas en las pestañas).
Capturas: `_plan/v3/ronda1/carta-color/` (88 jpg). Datos crudos: `_plan/v3/ronda1/carta-color-audit.json`. Script: Playwright + `getComputedStyle`. No se editó el sitio.

## Verificaciones automáticas

| Prueba | Resultado |
|---|---|
| Ítems en el DOM vs `content/carta-v2.json` | **256 / 256**. Los nombres coinciden 1:1 sin contar el texto de las etiquetas (Nuevo/Veggie). **Ningún precio difiere**, incluidos los de varias medidas (NORMAL/CORTO XL, CORTO/GIN & TONIC). |
| Destacados del home vs JSON | Los 7 coinciden: Peter $6.700, Sagüer on Faia $7.900, Sangría Foreva! $6.500, La moto chantá $6.400, Tukulito $15.900, Camarón que se duerme $15.900, Pizza dulzona $12.500 |
| Cada pestaña muestra solo su sección | OK en los 3 anchos (7/7). `aria-selected` es correcto y el hash se actualiza |
| Cada chip muestra solo su subgrupo | OK en los 3 anchos (29/29) |
| Deep links `#comilona`, `#comilona-pizzas-artesanales`, `#espirituosos-amamos-el-gin` | Abren la pestaña y el subgrupo correctos. Un hash desconocido no rompe la página |
| Logo → | `/v3/` OK |
| PDF | `https://uqr.to/ppvi`, en pestaña nueva |
| DM | `https://ig.me/m/almud_bar`, en pestaña nueva |
| Teclado | Con → se pasa de pestaña. El anillo de foco es `#2aa1f8` de 2 px |
| Errores de consola o JS | 0 |
| EN | Traduce el título (THE MENU), la bajada, el DM, el pie y los gloss de sección y grupo. **No traduce** las pestañas ni los chips, que quedan en español. Los nombres de los tragos quedan intactos, que es lo correcto |

## Contraste WCAG (pares reales del DOM, color de texto compuesto sobre su fondo efectivo)

**Home:** todos los pares pasan. Los más bajos:

| Par | Ratio | Dónde |
|---|---|---|
| `#f7cfc4` sobre `#a8222d` | 5.01 | kicker "Mocktails", 15 px |
| `#160d0b` sobre `#f24350` | 5.19 | CTA "Ver la carta" |
| `#f24350` sobre `#160d0b` | 5.19 | "USTÉ", 56 px |
| `#f5e9db` sobre `#a8222d` | 5.99 | precios en Tragos |

El resto queda entre 8.1 y 16.

**Carta:** un solo par falla.

| Par | Ratio | Mínimo | Dónde |
|---|---|---|---|
| `#f24350` sobre `#421315` (etiqueta "NUEVO" en la pestaña Casa) | **4.26** | 4.5 | 13 px |

Los demás pares mínimos están entre 5.19 ("Inicio") y 14.7. La etiqueta Veggie `#9fd39a` sobre `#49301e` da 7.11, pero ese color no está en la paleta.

**Tamaños bajo el piso de 16 px que pidió Carmen:**

| Clase | Tamaño | Uso |
|---|---|---|
| `.tag` | 13 px | Nuevo / Veggie / Picante |
| `.pr__c` | 14 px | NORMAL [90 cc] |
| `.pr__meta` y `.pr__dia` | 15 px | |

## Acentos por pantalla (colores saturados visibles en el viewport, 390)

### Home

| Pantalla | Acentos |
|---|---|
| Portada | rosa CTA + azul "BAR" = 2 |
| Tragos | fondo muro, sin otro acento |
| Comida | ámbar en el titular sobre noche-2 |
| Eventos | tinta + tinta-2 |
| Dónde | rosa |

Siempre hay 2 o menos. No hay arcoíris.

### Carta

Solo aparecen el azul del logo, el dorado en Promos y el rosa del botón "Inicio" al final. Los acentos están bien.

**El problema es otro:** cada pestaña tiñe el fondo del body con un color distinto, con una transición de 0,7 s.

| Pestaña | Fondo | Tono |
|---|---|---|
| Casa | `#421315` | vino |
| Mundo | `#331414` | |
| Espirituosos | `#2f1f15` | |
| Vinos | `#351018` | sale de `#5a1428`, **un color fuera de la paleta**, fijado a mano en `carta.css` |
| Sin | `#151f3d` | azul |
| Comilona | `#49301e` | marrón ámbar |
| Promos | `#312213` | |

Son 7 fondos para un solo documento. Cada uno es sobrio, pero recorridos en fila son un arcoíris apagado. Además, la carta deja de verse como una sola pieza.

---

## CARTA · **14/20**

**Lo que funciona**
- Los datos son impecables: 256 ítems, nombres literales ("Pinche Güey", "Tranquilein John Wayne", "Crumblecito ito ito") y ningún precio desalineado. Están las promos fijas con "* Siempre sujeto a stock! *", tal como en la carta.
- En el celular se lee bien: nombre en display de 24 px, precio de 600 a 20 px en papel alineado a la derecha y con cifras tabulares, y descripción de 17 px.
- Las medidas múltiples (90 cc / 150 cc) están bien resueltas, con la etiqueta encima de cada precio.
- Las pestañas sticky funcionan y el chip activo en papel se distingue bien. El PDF oficial y el DM quedan siempre a mano.
- Los destacados del home están bien elegidos en tragos: el Peter con burbuja de humo (foto de revista), el Sagüer on Faia con soplete (oficio), la Sangría y el mocktail (su "no dejamos a nadie ajuera").

**Lo que le quita puntos**
1. **No se siente *su* carta** (−3). La carta de Carmen es blanca, con títulos en cintas azul marino, nombres en condensada azul y precios en negrita [01-carmen-instagram §2]. La v3 es una lista oscura genérica: los nombres van en papel y los títulos de grupo son texto suelto. La paleta ya define la "pantalla clara" para la carta (`papel` + `letrero-azul-tinta`), pero no se usó.
2. **Hay mucho cabezal antes del primer trago en el celular** (−1). El hero "LA CARTA" + la barra de pestañas + el título de sección (que repite la pestaña) + los chips empujan el primer ítem a unos 450 px en Casa y unos 700 px en Espirituosos.
3. **Los subgrupos tienen un costo** (−1).
   - Solo se ve un subgrupo a la vez y los chips no son sticky. En "Amamos el GIN!" (40 ítems), quien está al fondo tiene que volver arriba para cambiar de subgrupo.
   - Tampoco se puede recorrer Comilona de corrido, como en la carta de papel.
   - Al tocar un chip la página no se lleva al inicio del subgrupo.
4. **Hay un destacado incoherente en el home** (−0,5). La foto grande de Comida es una pizza salada servida (P036), pero el único ítem de pizza listado es **Pizza dulzona**, que es un postre. Además, los 7 destacados enlazan a `carta/` a secas y no a su pestaña o subgrupo, aunque los deep links funcionan.
5. **El EN queda a medias** (−0,5). Las pestañas y los chips siguen en español ("Mocktails sin alcohol", "Pa los chichichos"). Para un turista, el gloss bajo el título no basta para navegar.
6. **En 1440 queda mucho vacío.** El hero "LA CARTA" ocupa la mitad izquierda y la derecha queda vacía. En la grilla de 2 columnas, las filas con foto y sin foto tienen alturas desparejas.

## COLOR · **16/20**

**Lo que funciona**
- La paleta es fiel. Noche marrón `#160d0b`, papel, muro rosa solo en la acción principal, azul solo en "BAR" y en el foco, dorado solo en Promos (los días) y precios en papel. Se cumplen P2, P5, P6 y P7 de la validación de Carmen.
- En el home, Comida va sobre noche-2 con el ámbar solo en el titular (P3 cumplido), Eventos va en tinta con fotos (P4) y Tragos en muro. Nunca hay más de 2 acentos por pantalla y no hay arcoíris ni franjas.
- El contraste está muy sano: el mínimo en el home es 5.01 y en la carta hay un solo fallo, marginal.

**Lo que le quita puntos**
1. **Hay 7 fondos de pestaña en la carta** (−1,5), con uno fuera de la paleta (`#5a1428`). La carta se ve teñida y cambiante. El fondo azul `#151f3d` de "Sin alcohol" y el marrón ámbar de Comilona rompen la unidad. Es la versión discreta del arcoíris que se eliminó.
2. **La etiqueta "NUEVO" en rosa sobre vino da 4.26** a 13 px y falla AA (−0,5). La etiqueta Veggie usa un verde `#9fd39a` que no es de la paleta (−0,5).
3. **El rosa (acento principal) está en "INICIO"** al pie de la carta (−0,5). La acción importante ahí es el DM o el PDF, no volver al home.
4. **Al logo SVG le falta pasar a los tokens** (−0,5). "BAR" es `#36a3ff` y "ALMUD" es `#f6ecdc`, pero los tokens dicen `#2aa1f8` y `#f9f8f9`. La diferencia es mínima, pero conviene que el logo salga de los tokens.
5. **El fondo de Tragos en el home es premium en escritorio**, pero en el celular es una pantalla roja larga y plana (unos 1.400 px). Funciona, aunque está al límite de lo que Carmen pidió para el ámbar.

---

## Cambios priorizados

| # | Tema | Cambio concreto | Archivo |
|---|---|---|---|
| 1 | Carta/Color | **Un solo fondo para toda la carta.** Eliminar `--bg-muro/rosa/ambar/vino/tinta/ambar2/dorado` y las reglas `html.js[data-tab=…] body{background}`, y dejar `--noche`. Eliminar `#5a1428` | `css/v3/carta.css`, `<style>` del head de `v3/carta/index.html` |
| 2 | Carta | **Darle a la carta la cara de su carta en papel.** Panel de lista en "hoja" `--papel` con texto `--noche`, nombres en `--letrero-azul-tinta` #1d5fae (5.32), precios 600/20 px en `--noche` y títulos de grupo como **cinta** `--tinta` #142a5c con texto papel (11.59). Las pestañas y el cabezal siguen sobre noche, para no apagar la noche. Antes de aplicarlo, validar con Carmen una pestaña de muestra | `css/v3/carta.css` |
| 3 | Carta | **Compactar el cabezal en el celular.** "LA CARTA" de 56 px a 36–40 px. Eliminar el `.panel__t`, que repite la pestaña, o dejarlo como kicker de 15 px. Meta: primer ítem visible antes de unos 320 px | `carta.css`, `v3/carta/index.html` |
| 4 | Carta | **Subgrupos:** chips sticky bajo las pestañas, o mostrar todos los subgrupos apilados con los chips como índice (scroll-spy). Como mínimo, que el clic en un chip llame a `top()` | `js/v3/carta.js`, `carta.css` |
| 5 | Color | **Etiquetas:** subir a 15–16 px. "Nuevo" en `--dorado` (8.5 sobre noche) o en papel con borde. Veggie/Vegan en `--papel-2` con borde, no en verde | `carta.css` (`.tag*`) |
| 6 | Carta | **Destacados del home:** reemplazar "Pizza dulzona" por una pizza artesanal (coherente con la foto de P036) o cambiar la foto. Enlazar cada destacado a su ancla: `carta/#casa`, `carta/#mocktails-sin-alcohol-mocktails-de-la-casa`, `carta/#comilona-picoteos`, `#comilona-greditas`, `#comilona-pizzas-artesanales` | `v3/index.html` |
| 7 | Color | **Pie de la carta:** el CTA rosa pasa a "ESCRÍBENOS POR DM". "Carta oficial (PDF)" e "Inicio" quedan como ghost | `v3/carta/index.html` |
| 8 | Carta | **EN:** agregar `data-en` a las pestañas (House cocktails, Classics, Spirits, Wines, Alcohol-free, Food, Promos) y a los chips de grupo genéricos (Clásicos→Classics, Jugos & bebidas→Juices & soft drinks). Mantener los nombres propios | `v3/carta/index.html` |
| 9 | Tipografía/Color | Subir `.pr__c` a 16 px y `.pr__meta` y `.pr__dia` a 16 px (piso de Carmen) | `carta.css` |
| 10 | Color | Pasar los fills del SVG del logo a los tokens (`#2aa1f8`, `#f9f8f9`) o a `currentColor` | `brand/v3/*.svg` y el inline del nav |
| 11 | Carta | **En 1440:** cabezal en dos columnas (título a la izquierda; bajada, PDF y DM a la derecha) o el título más bajo. Grilla `.prs` con `align-items:start` y la foto en la misma posición en todas las filas, o con una sola columna de lectura de unos 760 px | `carta.css` |
| 12 | Color | (Opcional) En el celular, partir el fondo plano muro de Tragos con una foto a sangre al medio, para que no sea una pantalla roja continua | `css/v3/site.css` |

**Notas:** CARTA 14/20 · COLOR 16/20.
