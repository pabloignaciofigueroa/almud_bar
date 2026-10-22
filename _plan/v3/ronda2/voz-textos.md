# Ronda 2 · Voz + Textos de página · web v3

Fase 16, ronda 2. Esta revisión la hacen juntos el agente Almud Voz y el agente Textos de página. No se editó el sitio.

## Cómo se revisó

- Servidor en el puerto 8854. Chromium 1194 con Playwright.
- Páginas: `/v3/` y `/v3/carta/`, a 390×844 y 1440×900, en ES y en EN. En la carta se abrieron las 7 pestañas.
- Las capturas están en `_plan/v3/ronda2/voz/`: `home-*`, `carta-*-t*` y las hojas `_sheet-*`. Todas se miraron.
- El texto visible salió del DOM (`dom.json`, `dom-carta.json`). La comparación con la ronda 1 se hizo con un diff del DOM.
- Los scripts son los de `_plan/v3/ronda1/voz/_scripts/`, con el puerto y la carpeta cambiados.

## Verificación

**`tools/verify_copy_v3.py`**
- 113 literales, 0 fallas, 0 prohibidos.
- 148 palabras: **cumple** la meta de ≤ 150.

**DOM real (`voz/verify-dom.txt`)**
- Landing ES: 0 textos fuera de lo aprobado, 0 prohibidos y **148 palabras visibles**.
- Lo que el script marca "no aprobado" en la carta EN son las pestañas y chips en inglés ("World classics", "Small plates", "Tue"…). Son falsos positivos: `copy-v3.md` ahora los aprueba (cabecera: "pestañas y chips con EN", "días de promo en EN"), pero solo en prosa, sin la marca “…”. Por eso el script no los ve.
- Los "prohibidos" de la carta (`pa l@s`, `muuuuuy`, `!!!`, `bigoteli`, `aaalas`, `Almudcito`) siguen dentro de descripciones, grupos y notas impresas. `copy-v3 §C` los manda "tal cual".

**Nada cortado ni desbordado**
- 0 palabras partidas y 0 elipsis. El ancho del documento es igual al del viewport en las 8 vistas.
- La única excepción son las filas deslizables de pestañas y chips de la carta en celular (ver P2-1).

**Cambios de la ronda 1, comprobados en pantalla**

| Cambio | Estado |
|---|---|
| "See for yourself" (solo EN) | Ya no aparece en modo ES. |
| "See you from 6 pm" · "Tue–Sat" | Aplicado. |
| "[Fiestas Patrias party]" · "[Anniversary]" | Aplicado. |
| Glosas con mayúscula inicial | Aplicado. |
| Destacados pulidos ("[Spiced sour with a little heat]", "[Shrimp baked in a clay pot]", "[Carménère wine, aged pisco, cinnamon]") | Aplicado. |
| Promos EN: "6 to 10 pm · Always subject to stock!" y días TUE/WED/THU/SAT | Aplicado. |
| Espirituosos: "Single or XL pour · mixer not included" | Aplicado. |
| "Comilona [food]" → la pestaña dice "Food" | Aplicado. |
| Anclas de los destacados | Aplicado. |
| `copy-v3.md` sincronizado | Hecho. |
| «LE / ESPERAMOS» huérfano en escritorio | Resuelto: ahora «LE ESPERAMOS / DESDE LAS / 18:00 HRS». |
| Superposición del botón de portada con la nav | Resuelta: el umbral pasó a `-170`. |

**Novedad: «Huerta sabrosa» reemplaza a «Pizza dulzona»**
- El literal está en [CARTA-1] y la glosa “[Pizza: cherry tomato, mushrooms, greens]” es fiel a la carta.
- Ahora el destacado calza con la foto P036, que muestra una pizza salada.

## Tono comparado con sus captions de Instagram

- Los titulares y las líneas en español son recortes literales de sus captions: [IG-111], [IG-045], [IG-022], [IG-026], [IG-010], [IG-048], [IG-024], [IG-155], [IG-087]. La voz es la de ellos: usté, «ná», «ajuera», «Peazo», «colorssss».
- Se quedó en Instagram lo que la marca y Carmen excluyeron para la web: las cascadas, los -eichon, los «Besi», el carrete y las promesas.
- La dosis se parece a la de su feed: una frase por pantalla y la foto adelante.
- Las glosas EN son más sobrias que el original. Es inevitable, y correcto:
  - "See you from 6 pm" pierde el «usté», pero conserva la invitación.
  - "Going all out!" y "We're nothing without you!" mantienen la exclamación y el calor.
- En la carta EN, las pestañas traducidas ("World classics", "Deals", "Food") pierden el juego de «del mundo mundial» y «Comilona». Funcionan porque el literal sigue arriba en cada panel («CÓCTELES DEL MUNDO MUNDIAL») y la regla "la glosa nunca reemplaza al literal" se cumple dentro del contenido.

---

## Nota: **18 / 20**

Sube un punto respecto de la ronda 1 (17). Se resolvieron todos los P1 y casi todos los P2:
- La carta en EN ya orienta al turista: pestañas, chips, días, horario de promos y notas de precio.
- La glosa de Reseñas dice lo que debe decir.
- La landing sigue literal, limpia y con 148 palabras.

**Lo que impide el 19–20 (−2):**
1. En la carta, en celular, las filas deslizables siguen mostrando palabras cortadas en el borde, aunque ya hay desvanecido. En ES se ve «CÓCTELES DEL MUNDO MUNDI», «VINOS & ESPUMANT» y el chip «Jugos & be…». **−1**
2. Quedan detalles menores de texto en la carta:
   - El subtítulo en EN es una sola línea bilingüe: «tenemos pa todos los gustos! something for every taste!».
   - Al final de la carta el botón ‹Escríbenos por DM› aparece dos veces en pantalla.
   - `brand-voice-v3 §4` sigue contradiciendo a `copy-v3 §C` sobre las descripciones.

   En total, **−1**.

## Lo que falta (ya está en ≥ 17; esto es para llegar a 19–20)

### P2

1. **Carta en celular, filas deslizables** (`.tabs__l`, la fila de `a.chip`).
   - Que el desvanecido del borde derecho cubra unos 40 px. Si no, que el último elemento visible quede entero, con `scroll-snap-type:x mandatory` y `scroll-snap-align:start` en cada `a.tab` y `a.chip`.
   - Alternativa para los chips: `flex-wrap: wrap` en 390 px. En la ronda 1 los chips ya se veían en 2–3 filas sin cortes.
2. **Carta, subtítulo en EN** (`p.carta__b` + `.gloss`).
   - Hoy: «tenemos pa todos los gustos! something for every taste!» en una sola línea.
   - Cambio: poner la glosa en su propia línea (`display:block`), como en el resto del sitio. Hoy se lee como una sola frase mitad en español.

### P3

1. **Botón DM repetido al final de la carta.** Con la nav fija ya tiene ‹Escríbenos por DM›, así que el botón grande del pie (`.carta` foot `a.btn--rosa`) duplica el mismo texto en la misma pantalla. Hay que dejar uno: sacar el del pie, o bajar el de la nav solo en celular.
2. **`content/brand-voice-v3.md §4`**: cambiar "salvo los **nombres de ítems de la carta**" por "salvo los **nombres, descripciones y notas impresas de la carta**". Así la guía queda alineada con `copy-v3 §C` y deja de marcar `pa l@s`, `muuuuuy`, `!!!`, `bigoteli` y `aaalas`.
3. **`tools/verify_copy_v3.py` y `copy-v3.md`**: dar a las pestañas y chips EN su propia tabla con la marca “…”. Así el verificador del DOM las da por aprobadas y una tercera ronda no las vuelve a reportar.
4. **Opcional, carta EN.** Los encabezados de grupo sin glosa («PICOTEOS», «GREDITAS», «SANGUCHES») quedan bajo chips en inglés ("Small plates", "Clay pots", "Sandwiches"). Se entienden, pero una glosa chica bajo el `h3.gr__t` igual a la del chip haría que el turista no tenga que mirar dos lugares.

**No tocar:** los titulares, las líneas de rincón, la dosis, el equipo, las reseñas, Cuándo y dónde, el pie y las glosas de la landing. Están literales, con acentos correctos, sin cortes y con el tono de sus captions.
