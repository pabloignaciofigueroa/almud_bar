# Ronda 2 (fase 16) · Agentes ALMUD CARTA + ALMUD COLOR

## Qué revisé

- **Páginas:** `/v3/` y `/v3/carta/`, servidas en el puerto 8853.
- **Herramienta:** Playwright/Chromium a 390×844, 768×1024 y 1440×900, en ES y EN.
- **Recorrido:**
  - Las 7 pestañas y los 29 subgrupos en cada ancho (87 combinaciones).
  - Los deep links, el logo, el PDF y el DM.
  - El teclado.
  - El contraste en pares reales (`getComputedStyle`), también en EN.
- **Capturas:** `_plan/v3/ronda2/carta-color/`.
- **Datos crudos:** `_plan/v3/ronda2/carta-color-audit.json`.
- **Hoja lado a lado:** `_plan/v3/ronda2/carta-vs-impresa.jpg`. Junta las 7 cartas PDF (`assets/raw/carta/*.pdf`, pág. 1 rasterizada) con su pestaña web a 390.
- No se editó el sitio.

## Verificaciones

| Prueba | Resultado |
|---|---|
| DOM vs `carta-v2.json` | **256/256** nombres exactos y **0** precios distintos, incluidos los de varias medidas |
| Destacados del home | Peter, Sagüer on Faia, Sangría Foreva!, La moto chantá, Tukulito, Camarón que se duerme y **Huerta sabrosa $13.900**. Coinciden con el JSON y ahora **enlazan a su ancla** (`#casa`, `#mocktails…-de-la-casa`, `#comilona-picoteos`, `#comilona-greditas`, `#comilona-pizzas-artesanales`). La pizza salada ya es coherente con la foto |
| Una sección por pestaña / un subgrupo por chip | OK, 7/7 y 29/29 en los 3 anchos |
| Fondo de página | `--noche` en todas las pestañas. La hoja lleva un tinte suave de la paleta |
| EN | 7 pestañas traducidas (House cocktails… Deals), 28 de 29 chips traducidos ("Red Bull te da aaalas" queda, por ser un nombre propio). Quedan 0 nodos `data-en` sin cambiar. Los nombres de los tragos quedan intactos |
| Enlaces | El logo lleva a `/v3/`. El PDF (`uqr.to/ppvi`) y el DM (`ig.me/m/almud_bar`) abren en pestaña nueva. El CTA rosa del pie ahora es "Escríbenos por DM" |
| Consola | 0 errores |
| **Bug: pestañas en escritorio** | `.tabs__l` tiene un tope de 1100 px, pero las pestañas ocupan 1262 px. Por eso **"Nuestras promos" queda cortada en 1440 y en 1920**, con el fundido encima y sin barra de desplazamiento |
| **Bug: chip activo fuera de la vista** | Con `#comilona-somos-dulzones` a 390, el chip activo queda en x = 569–690, fuera de la pantalla. `reveal()` solo se aplica a las pestañas, no a los chips. Además, si se cambia el idioma, la fila de pestañas no vuelve a centrar la activa |

## Contraste (texto compuesto sobre su fondo real, 390, ES y EN)

Todo pasa AA. Los pares mínimos:

| Par | Ratio | Uso |
|---|---|---|
| `#c41e34` sobre hoja `#f1dfc5`/`#f5ddd1` | **4.51 / 4.52** | "NUEVO" y días de Promos, 16 px. **Pasan con margen 0** |
| `#1d5fae` sobre la hoja | 4.89–5.04 | nombres de 23 px (texto grande, pasa holgado) |
| `#160d0b` sobre `#f24350` | 5.19 | CTA |
| `#f5e9db` sobre cinta `#142a5c` | 11.59 | cintas |
| `#160d0b` sobre la hoja | 14.7–15.2 | precios y texto |

**Home:** el mínimo es 5.01 (kicker "Mocktails" sobre muro).

## Lado a lado con la carta impresa (lo que veo en `carta-vs-impresa.jpg`)

| | Impresa | Web ronda 2 |
|---|---|---|
| Papel | blanco con guarda de baldosa gris | crema `--papel` con tinte por pestaña. El de "Sin alcohol" (`#e8e2de`) se ve **gris frío** |
| Cinta de título | **carbón** `#403c3d` (medido), en letra display serif en caja mixta ("COCTELERÍA de la CASA") | azul tinta `#142a5c`, Big Shoulders en mayúsculas. Carmen la describió como "azul marino". La tinta funciona y es de la paleta, pero no es literal |
| Nombres | **azul rey vivo** `#4346db` (azul con algo de violeta), grandes y centrados | `#1d5fae`, un azul acero más apagado y más chico. **Es la diferencia que más se nota** |
| Precios | negrita **magenta** `#db67b2`, bajo cada descripción | negro `--noche`, a la derecha (más legible y alineado; Carmen pidió precios sin rosa) |
| Ingredientes | **en negrita** dentro de la descripción | texto plano |
| Espirituosos | **tabla** con columnas NORMAL / XL: 26 piscos en media página | lista con los 2 precios apilados por ítem, unos 130 px por fila. Son unas 10 pantallas en Piscolein y 40 ítems en Gin |
| Composición | 2 columnas, todo centrado | 1 columna. En 1440 el precio queda a unos 900 px del nombre |

**Veredicto del lado a lado:** ahora sí "es su carta": hoja clara, nombres azules en condensada y cintas de grupo. Lo que todavía la separa es el tono del azul, la tabla de espirituosos y la composición de escritorio.

---

## CARTA · **16/20** (ronda 1: 14)

**Mejoró:**
- La hoja papel con nombres azules y cintas.
- Cabezal compacto: a 390 el primer trago aparece a unos 260 px, antes estaba a unos 450.
- Chips fijos bajo las pestañas.
- EN completo en la navegación.
- Destacados del home coherentes y con enlace profundo.
- Promos con el día en rosa tinta, como en su afiche.
- Datos intactos.

**Falta para ≥17:**
1. **Espirituosos y Vermú en tabla de columnas** (−1). Encabezado de columnas fijo (NORMAL 90 cc · XL 150 cc) una sola vez por grupo, y una línea por botella: nombre a la izquierda, 2 precios tabulares a la derecha. Así es la carta impresa. En el celular cada fila baja de unos 130 px a unos 48 px.
2. **Bug de pestañas en escritorio** (−0,5). "Nuestras promos" queda oculta en 1440. Quitar el `max-width:1100px` de `.tabs__l` en ≥1024 px, o bajar el padding y el tracking para que las 7 entren en una línea.
3. **Revelar el chip activo** (−0,5). Llamar a `reveal()` sobre la `.chips` del panel en `paint()`, igual que con las pestañas, y volver a centrar las pestañas después de `setLang()`.
4. **Escritorio a 2 columnas dentro de la hoja**, como el impreso (≥1024: `.prs{grid-template-columns:1fr 1fr;column-gap:56px}`), o bien acercar el precio al nombre con un ancho de lectura de unos 720 px. Hoy en 1440 el precio queda lejísimo.
5. (Opcional, + fidelidad) **Ingredientes en negrita.** Requiere marcar `<b>` en el JSON o en el generador, a partir del PDF.

## COLOR · **17/20** (ronda 1: 16)

**Mejoró:**
- Fondo único `--noche` y tintes solo de la paleta (se eliminó `#5a1428`).
- Etiquetas de 16 px en tintas de la paleta (Veggie ya no es verde).
- CTA rosa en el DM.
- El logo usa `#2aa1f8`.
- Máximo 2 acentos por pantalla: azul del logo + tinta, o rosa tinta en Promos.
- Contraste AA en todo, ES y EN.

**Falta para ≥18:**
1. **Nombres en el azul de su carta.** Cambiar `--letrero-azul-tinta` (solo dentro de `.hoja`) de `#1d5fae` a un azul rey cercano al impreso: **`#3a3ad8`** (6.32 sobre papel, 5.81 sobre el tinte rosa) o `#4346db` (5.60 / 5.15). Es más fiel y además mejora el contraste. Se puede declarar como `--carta-azul` para no tocar el token global.
2. **Tintes de hoja:** dejar 2 como máximo, o ninguno. El de "Sin alcohol" (`#e8e2de`, por `tinta-2`) se ve gris oficina, justo lo que Carmen dijo que nunca. Propuesta: hoja `--papel` en todas las pestañas, o solo un tinte cálido (rosa en Casa, dorado en Promos).
3. **Rosa tinta en 4.51–4.52:** pasa, pero sin margen sobre los tintes. Si se mantienen los tintes, oscurecer el "NUEVO" y el día de Promos a `#b01a2e` (unos 5.3) o ponerlos sobre `--papel` puro.
4. (Decisión de Carmen) **Cinta carbón `#403c3d`** como en el impreso, o tinta `#142a5c` como está ahora. Las dos pasan (texto papel: 9.5 / 11.6). Ella habló de azul marino, así que la tinta se puede quedar. Si se quiere fidelidad literal, carbón.
5. (Opcional) **Precios en magenta como el impreso:** `#db67b2` no pasa (2.66). Habría que usar `#a8226e` (5.63). Contradice la regla T6 de Carmen ("precios en papel, no rosa"), así que solo con su visto bueno. Recomiendo dejarlos en `--noche`.

## Lista priorizada

| # | Cambio | Archivo | Tema |
|---|---|---|---|
| 1 | Tabla de columnas para los grupos con `columnas` (Espirituosos, Vermú y Por copa si aplica) | generador de `v3/carta/index.html`, `css/v3/carta.css` | Carta |
| 2 | Nombres `#3a3ad8` dentro de `.hoja` | `carta.css` (`.pr__n`, `.gr__t--sub`) | Color/Carta |
| 3 | Pestañas completas en escritorio (sin el tope de 1100 en `.tabs__l` ≥1024) | `carta.css` | Carta |
| 4 | `reveal()` del chip activo y volver a centrar las pestañas después del cambio de idioma | `js/v3/carta.js` | Carta |
| 5 | Hoja: eliminar el tinte gris de "Sin" y dejar 0–2 tintes cálidos | `carta.css` (`--hoja-*`) | Color |
| 6 | Escritorio: 2 columnas en `.prs` o ancho de lectura de unos 720 px | `carta.css` | Carta |
| 7 | "NUEVO" y días de Promos a `#b01a2e`, o sobre papel puro | `carta.css` | Color |
| 8 | (Opcional) negritas en los ingredientes; cinta carbón según lo que decida Carmen | JSON/generador, `carta.css` | Carta/Color |

**Notas ronda 2:** CARTA 16/20 · COLOR 17/20. Con los puntos 1–4, CARTA llega a 17–18. Con los puntos 2, 5 y 7, COLOR llega a 18.
