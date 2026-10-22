# Ronda 1 · Voz + Textos de página · web v3

Fase 15, ronda 1. Esta revisión la hacen juntos el agente Almud Voz y el agente Textos de página. No se editó el sitio.

**Cómo se revisó**
- Servidor `python3 -m http.server 8841`. Chromium 1194 con Playwright (`--no-sandbox`, `--autoplay-policy=no-user-gesture-required`).
- Páginas recorridas: `/v3/` y `/v3/carta/`, a 390×844 y a 1440×900, en ES y en EN (con el botón EN), pantalla por pantalla.
- En la carta se abrieron las 7 pestañas, una por una.
- Las capturas están en `_plan/v3/ronda1/voz/`. Hay unas 140 capturas `home-*`, `carta-*-t*` y las hojas de contacto `_sheet-*`. Todas se miraron.
- El texto visible real salió del DOM (`dom.json`, `dom-carta.json`). Se descartaron los nodos ocultos, los `display:none` y los `.sr-only`. Los scripts están en `_scripts/`.

**Verificación**
- `tools/verify_copy_v3.py`: 116 literales, 0 fallas, 0 prohibidos, 149 palabras. Cumple.
- `_scripts/verify_dom.py` corre la misma normalización y la misma lista PROHIB, pero contra el **texto visible del DOM**. El resultado está en `voz/verify-dom.txt`:
  - Landing ES: **0 textos fuera de lo aprobado** y **0 prohibidos**. Hay **148 palabras visibles** (meta ≤ 150).
  - Los únicos textos sin fuente en `copy-v3.md` son ‹Sillones›/“Lounge”, ‹Los dueños›/“The owners” y @cepaz/@rusio_mezclao. Los tres los pidió o aceptó Carmen en `08-juicio-carmen*.md`.
  - Carta: los "prohibidos" que salen (`pa l@s`, `muuuuuy`, `!!!`, `bigoteli` ×2, `aaalas`, `Almudcito`) están todos dentro de descripciones, grupos o notas impresas de la carta. `copy-v3.md §C` las manda "tal cual", así que no son errores de construcción (ver P3-6).
  - Los `[Valle …]` de los vinos son literales de `carta-v2.json`. Era un falso positivo.
- Ningún texto se corta en ES ni en EN, ni a 390 ni a 1440:
  - 0 `word-split`, 0 elipsis y 0 desbordes horizontales (`scrollWidth = ancho` en las 4 vistas).
  - La única excepción es la barra de pestañas de la carta en celular (P2-1).
- Los acentos se ven bien en las mayúsculas display: NÁ, SÁB, CÓMO, ESCRÍBENOS, JALOGÜÍN, USTÉ, CÓCTELES, COCTELERÍA.

---

## Nota: **17 / 20**

**Lo que sostiene la nota**
- Todo texto visible de la landing es literal de Almud o etiqueta [UI] aprobada. Los 10 titulares de Carmen van tal cual.
- No hay ningún prohibido en la landing: sin RESERVAR, cascadas, "Almudcito", fila ni espera. «colorssss» es la única excepción aprobada.
- La dosis es la justa:
  - «Le esperamos» aparece 1 vez y «USTÉ SE LO MERECE!» 1 vez.
  - «terracita» va 1 vez y recortada.
  - Eventos queda en mes + nombre, sin promesas.
- Son 148 palabras. Las fotos cargan la página: en celular cada pantalla tiene un titular y, como mucho, una línea.
- El modo EN funciona como se pidió. Los literales se quedan en español y la glosa va debajo, en tamaño de cuerpo y nunca en display. Los nombres de la carta y de los eventos no se traducen.

**Lo que resta 3 puntos**
1. La página Carta en EN deja al turista sin glosa justo donde más la necesita: en Promos (horario, días y aviso de stock; la glosa EN aprobada en copy-v3 no se construyó) y en las notas de precio de Espirituosos. **−1**
2. Una glosa EN dice lo contrario de lo que quiere decir. “Don't just take **their** word for it” va encima de las reseñas, que son justamente la palabra de *ellos*. Además se ve también en modo ES. **−1**
3. Hay detalles de inglés poco natural para un turista y desalineaciones entre el sitio y `copy-v3.md` que confunden a la próxima ronda. En celular, la barra de pestañas corta una palabra a la vista («CÓCTELES DEL MUNDO MUNDI…»). **−1**

---

## Cambios priorizados (selector o texto exacto → cambio)

### P1 · arreglar antes de la ronda 2

1. **Carta › Nuestras promos, glosa EN que falta** (`#promos p.gr__nota`, `#promos p.gr__pie`)
   - Ahora, en EN se ve solo «de 18:00 a 22:00 hrs» y «* Siempre sujeto a stock! *».
   - Cambio: agregar debajo `<span class="gloss gloss--s" lang="en">6 to 10 pm · Always subject to stock!</span>`. Es exactamente la glosa aprobada en `copy-v3.md §C › Nota promos`.
2. **Carta › Promos, días** (`span.pr__dia`: «Martes», «Miércoles», «Jueves», «Sábado»)
   - Cambio: agregar `data-en` con “Tue”, “Wed”, “Thu” y “Sat”. Son etiquetas, no literales de marca, así que se pueden traducir. Hoy un turista no sabe qué día rige cada promo.
3. **Reseñas, glosa del titular** (`.resenas .ttl-gloss .gloss--on`: “Don't just take their word for it”)
   - Cambio: “**See for yourself**”. Recoge el sentido de «Que no se lo cuenten» (vívalo usted) y no le quita valor a las reseñas que vienen debajo. Si se quiere la fórmula clásica de testimonios, la correcta es “Don't just take **our** word for it”.
   - Requiere el visto bueno de Carmen, porque la glosa fue aprobada.

### P2 · claridad para el turista y nada cortado

1. **Carta en celular, barra de pestañas** (`.tabs__l a.tab`)
   - Problema: a 390 px el borde corta «CÓCTELES DEL MUNDO MUNDI…» y, al avanzar, «…CTELERÍA DE LA CASA», «ESPUMANT…» y «…TAILS SIN ALCOHOL». Se lee como texto truncado.
   - Cambio: poner una máscara de desvanecido en los bordes (`mask-image: linear-gradient(90deg, transparent, #000 16px, #000 calc(100% - 32px), transparent)`) y `scroll-padding-inline:16px`. Así se entiende que la barra se desliza y no que el texto quedó roto.
2. **Carta › Espirituosos, notas de precio** (`p.gr__nota` «Precio del corto normal o XL / NO INCLUYE BEBIDA» y «Elija su medida 90 o 150 cc!»)
   - Cambio: agregar en EN la glosa “Single or XL pour · mixer not included” y “Choose 90 or 150 cc”.
   - Opcional: «Los whiscachos no incluyen bebida…» → “[no mixer included]”.
3. **Carta › Comilona, glosa** (`#comilona .panel__g`: “Comilona [food]”)
   - Problema: repite la palabra que está justo encima.
   - Cambio: “Food”.
4. **Landing › Eventos › Fondita** (`.ev .gloss` “[national holidays]”)
   - Problema: es vago.
   - Cambio: “[Chilean Independence Day fair]”, o bien “[Fiestas Patrias party]”.
5. **Landing › Cuándo y dónde, glosa del titular** (“We're expecting you from 6 pm”)
   - Problema: suena a cita agendada.
   - Cambio: “**See you from 6 pm**”, que conserva la invitación de «Le esperamos».
6. **Landing, destacados que enlazan a `carta/` sin ancla.** `copy-v3 §3` pide enlazar a su ítem. Hoy, al tocar «Tukulito Sakayama», la carta abre en Cócteles. Cambios:
   - `.it--hero`, `.it--a`, `.it--b` → `carta/#casa`
   - `.moc__it`, `.moc__n` → `carta/#mocktails-sin-alcohol-mocktails-de-la-casa`
   - Tukulito → `carta/#comilona-picoteos`
   - Camarón → `carta/#comilona-greditas`
   - Pizza dulzona → `carta/#comilona-somos-dulzones`

   `carta.js › go()` ya resuelve los hash de sub-grupo.
7. **`content/copy-v3.md` desalineado con el sitio aprobado.** Hay que actualizar el documento, no el sitio, para que la ronda 2 y `verify_copy_v3.py` midan lo que de verdad se ve. Diferencias:
   - Portada con 1 botón (sin ‹Cómo llegar›, excepción aceptada en juicio-2).
   - ‹Sillones›/“Lounge” vuelve al carrusel.
   - Línea ‹Los dueños› @cepaz · @rusio_mezclao / “The owners”.
   - Sin ‹Próximo›.
   - Equipo con 5 personas (sale @elymar_bocarejo, como decidió Carmen).
   - Créditos: 4 (salen @tamillanquileo y @dosistudio).
   - Botón ‹Escríbenos por DM› en la nav de la carta.
   - Etiquetas ‹Nuevo›/“New” y ‹Veggie› de la carta.

### P3 · pulido

1. **Glosas en minúscula inicial** (“a lot of love, colour and work”, “a simple kitchen…”, “we're nothing without you!”, “going all out!”, “a look is worth…”, “we leave nobody out”).
   - Problema: copian la minúscula del literal, y en inglés de cuerpo parecen error. Además, otras glosas empiezan con mayúscula.
   - Cambio: usar mayúscula inicial en todas las glosas (son nuestras).
2. **Pulir glosas de destacados**:
   - “[spiced, slightly hot sour]” → “[spiced sour with a little heat]”
   - “[baked shrimp clay pot]” → “[shrimp baked in a clay pot]”
   - “[Carménère, aged pisco, cinnamon]” → “[Carménère wine, aged pisco, cinnamon]”
   - “a lot of love, colour and work” → “A lot of love, colour and hard work”
3. **Formato y consistencia de glosas**:
   - “Tue to Sat” → “Tue–Sat”.
   - El aniversario lleva la glosa “Anniversary” sin corchetes, mientras los otros eventos van “[Valentine's Day]”, “[Halloween]”. Cambio: “[anniversary]”, o quitar los corchetes de todos.
4. **Glosa EN de Reseñas visible en modo ES** (`.gloss--on`). Es la única línea en inglés que ve un visitante en español. Hay que confirmar con Carmen si la "obligatoria" era solo para EN. Si es así, se quita `gloss--on` y queda como las demás.
5. **Escritorio, titular de Cuándo y dónde.** Queda partido como «LE / ESPERAMOS / DESDE LAS / 18:00 HRS», con «LE» huérfano en la columna angosta.
   - Cambio: `text-wrap: balance` en `.donde .ttl__t`, o ensanchar `.donde__t`.
6. **Contradicción entre guías** (no es del sitio):
   - `brand-voice-v3 §4` exime solo los *nombres* de la carta.
   - `copy-v3 §C` manda las descripciones "tal cual", y por eso se ven `pa l@s`, `muuuuuy rico`, `rico!!!`, `imperdible` y `bigoteli`.
   - Recomiendo dejar la carta literal (es su carta impresa) y corregir el §4 a "nombres **y descripciones** de la carta". Así ningún verificador lo vuelve a marcar.
7. **Superposición transitoria (para Diseño).**
   - Qué pasa: a 390 px, entre scrollY ≈ 720 y 764, el botón «VER LA CARTA» de la portada pasa por debajo de «CARTA · EN» de la nav, que todavía es transparente, y los dos textos se montan (captura `voz/home-m-es-01.jpg`).
   - Por qué pasa: `is-past` se activa en `hero.offsetHeight - 80`.
   - Cambio: subir el umbral para que se active antes de que el botón llegue a la franja de la nav.

---

**No hay que cambiar** los titulares, las líneas de rincón, los @ del equipo, las reseñas ni las firmas. Están literales, bien acentuados, en dosis justa y sin cortes. La landing ya cumple "mínimo texto, las fotos hablan".
