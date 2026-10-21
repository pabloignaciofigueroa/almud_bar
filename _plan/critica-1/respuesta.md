# Fase 15 · Respuesta a la crítica 1

Cada punto de `critica.md` está marcado como hecho (con el cómo) o como no hecho (con el porqué).

**Evidencia "después":** `_plan/critica-1/after/`
- Capturas viewport por viewport: `r2-{landing|carta}-{320|375x667|390|414|768|1280|1440|1920|320-en|390-en|1440-en|390-rm|1440-rm}-vNN.jpg`.
- Estados del día: `dia{2,4,5,6,0}-landing-1440-vNN.jpg`.
- Métricas: `r2-metrics.json` (por captura: CLS, errores, pedidos fallidos, pedidos a terceros, ancho de scroll, fotos duplicadas por id y objetivos táctiles).
- Interacción: `interact.json`, `i-menu-390.jpg` e `i-mapa-390.jpg`.
- Taste: `inspect-landing/` e `inspect-carta/`.
- Scripts: `shoot.py` e `interact.py`.

## Resultados de la verificación
- **Taste lint:**
  - landing: 0 FAIL, 1 WARN (el falso positivo "more than a" de la glosa EN, ya declarado);
  - carta: 0 / 0;
  - `site.css` y `carta.css`: 0 / 0.
- **Taste inspect:**
  - landing: **0 FAIL**, 2 WARN: `palette-cream`, defendido en `sistema.md`, y `lopsided` en la fila del titular de El lugar (el texto va en la fila de abajo, a todo el ancho).
  - carta: **0 FAIL**, 3 WARN: `palette-cream`; `no-footage`, porque los loops borrosos salieron a pedido; y `still-page` con 8 elementos en movimiento, que es el mínimo.
- **Playwright (Chromium 1194), 26 capturas, landing y carta:**
  - CLS 0 al cargar y tras recorrer;
  - 0 errores de consola y 0 pedidos fallidos;
  - 0 pedidos a terceros;
  - scrollWidth igual al viewport (320 a 1920, también en EN);
  - 0 fotos repetidas por id de medio en los seis estados del día.
- **Menú:** 40 ráfagas aleatorias de abrir, cerrar y reabrir (de 1 a 4 clics, entre 0 y 260 ms) dieron **0 estados inconsistentes**. Escape cierra al instante.
- **Mapa:** 0 pedidos a terceros antes del toque; el iframe se crea después.
- **Carta:** con el teclado, la pestaña cambia con `transition-duration: 0s`, también el color. El h1 no anima al cargar.
- **Scripts del proyecto:**
  - `verify_copy.py`: 212/212 literales y 42/42 titulares;
  - `validate_carta.py`: OK;
  - `build_v2.py`: 231 literales, 150 glosas y 116 [UI] verificados.
- `public/` no se tocó (no se hizo build de prueba ahí). No hay commit.

## P0
- **P0-1 · carrera del menú: hecho.**
  - La hoja pasó de keyframes con `animationend` a una transición de `clip-path` sobre la clase `.abierta`: abre en 400 ms con `--ease-drawer` y cierra en 250 ms con `--ease-out`.
  - `visibility` se apaga con un retraso igual al cierre. No quedan manejadores pendientes y la transición es interrumpible desde el valor actual.
  - Teclado, Escape y los enlaces de la hoja son instantáneos (`.al-instante`). Con reduced motion queda un fade de 180 ms.
  - Probado con 40 ráfagas (ver arriba).

## P1
- **P1-1 · pestañas y chips de la carta: hecho.** Bajo 1024 px las siete pestañas van todas a la vista en una sola barra sticky, que se parte en filas:
  - 2 filas a 768;
  - 3 filas a 360–699, y también a 320, con un padding más ajustado.
  - Las pestañas son compactas: 44 px de alto, 14 px y fondo de botón.
  - Los chips también se parten en filas. Bajo 700 px no son sticky, para no sumar otra barra fija.
  - `carta.js` mide el alto real de la barra (`--tabs-h`, `--chips-h`) para el sticky, los `scroll-margin` y `align()`.
  - **Desvío:** no caben en 2 filas bajo 700 px sin bajar de 44 px o de 14 px (los títulos son literales y largos). Elegí 3 filas legibles antes que un borde con degradado.
- **P1-2 · viernes en la semana: hecho.**
  - La semana tiene 5 columnas desde 700 px, con el viernes como «Viernes» [IG-003] · «Venga venga que nadie le detenga!» [IG-003] y su glosa EN. No se inventó ninguna promo.
  - «Ramón a $ 4.500!» se deja tal cual: es el nombre literal del ítem en CARTA-7, no un precio agregado.
- **P1-3 · portada en teléfonos bajos: hecho.**
  - Bajo 900 px la portada es una grilla: la zona de la foto arriba y el bloque de tipo abajo.
  - La foto se ancla con unidades de contenedor (`cqh`/`cqw`) para que la línea del 70 % de la foto, bajo las caras (que van del 47 al 62 %), caiga justo en el borde de su zona. El tipo nunca pisa una cara.
  - El scrim crece con el bloque de tipo (`::before` del bloque, con un degradado de 48 px hacia arriba).
  - Bajo 760 px de alto, el logotipo baja a `min(150px, 40cqi)` y la bio a body.
  - Verificado a 320×568, 375×667, 390×844 y 414×896, en ES y en EN.
  - La glosa EN de la bio se mantiene en small: el texto de la marca sigue literal más su glosa.
- **P1-4 · colisiones de precio y glosa: hecho.**
  - Precio: `line-height: 1` y `padding-bottom: .08em`.
  - `.display + .gl-h` con `margin-top: 24px`.
  - En EN el precio aparece una sola vez ("CLP 4,500"; ver P2-11).
- **P1-5 · La barra: hecho.** Ahora muestra la barra larga y curva (P093, `lugar-barra-curva`):
  - 16:9 en 8 columnas desde 700 px, recortada por CSS desde el 4:5 de 1280 px, sin ampliar;
  - texto en las columnas 9–12, alineado abajo.
  - La lámpara pasa al par, junto a «Nos gustan los brillitos, las luces».
- **P1-6 · esqueletos repetidos: hecho.** Cada capítulo tiene su composición y no hay dos seguidos iguales:
  - Hoy: split.
  - El lugar: titular a lo ancho, banda a sangre, la barra ancha, mosaico y par.
  - Tragos: titular en una línea a 12 columnas, marco ancho que crece (bartender del muro rosa), par desigual con "Coctelería de la casa" y banda.
  - Sin alcohol: titular de afiche con la lista.
  - Comida: foto sostenida a la izquierda, titular y texto a la derecha, y mosaico.
  - La carta: índice.
  - Con quién: titular, párrafo debajo y mosaico ×2.
  - Equipo: titular, banda y texto con los nombres.
  - Reseñas: titular, una línea de cifras y citas.
  - Eventos: calendario a 12 columnas y tira de 4 fotos.
  - Dónde: datos con el mapa a la izquierda, la puerta a la derecha y la calle (video) ancha abajo.
- **P1-7 · huecos en Comida: hecho.** No queda columna verde vacía ni foto sticky sola: el texto va junto al titular y la foto es estática.
- **P1-8 · Eventos: hecho.**
  - `site.js` marca el próximo mes con evento según la fecha en America/Santiago: ‹Este mes› si es el mes en curso, ‹Próximo› si no.
  - Hoy (21-oct) marca Octubre · Jalogüín.
  - Sin JS no se marca nada y el calendario queda completo.
  - El hueco de 700 px desaparece: las fotos pasan a una tira debajo del calendario.
- **P1-9 · P189 en DPR 2: no se puede arreglar ahora, documentado.** Sigue el archivo nativo de 1440 px, nunca mostrado a más de 1440 px CSS. Queda en `informe.md` como requisito pedir el original en alta antes de mostrárselo al cliente. La portada no se tocó.

## P2
- **P2-1 · un primario por pantalla: hecho.**
  - El único botón barra es el de la nav.
  - En la portada, "Cómo llegar" pasa a enlace (los dos enlaces van en 600 en el teléfono).
  - Pasan a enlace "Ver la carta" de Sin alcohol, "Cómo llegar" de Con quién (al pie del párrafo) y "Cómo llegar" de Dónde.
  - Sobre campo se mantiene el botón noche (Hoy, Tragos, Comida) y sobre papel el azul (destacados), según `sistema.md` §7.
- **P2-2 · caja de los titulares: hecho.** `text-transform: uppercase` en `.display`, `.head` y `.firma`, y en los enlaces de la hoja. La caja literal queda en el DOM.
- **P2-3 · splash fuera: hecho.** El líder de Tragos es el bartender del muro rosa; la copa con salpicadura sale del landing.
- **P2-4 · rincones: hecho.**
  - La foto P114 va sin el rótulo "Los sillones" (queda su línea de IG-075, anotado en el guion).
  - La terraza (P039) se mantiene: es de noche, con guirnaldas.
  - Bajo 700 px, los mosaicos con texto van a 3/4 del ancho, alternando.
- **P2-5 · cifras: hecho.** Una línea de cuerpo bajo el titular de Reseñas: "4,6 Google (848 reseñas) · 4,6 Tripadvisor (209 reseñas, #1 de 6 bares en Castro) · oct-2026". En EN, solo la línea EN.
- **P2-6 · láminas de la carta: hecho.**
  - Las láminas de video borrosas se reemplazaron por fotos nítidas: Coctelería con el muro rosa (P184) y una copa tallada (P097), y Comilona con la gredita (P091).
  - Bajo 1024 px no hay lámina de pestaña: las filas con foto llevan la imagen, y la de grupo va a lo ancho en 16:9.
  - Si un grupo tiene alguna foto, todas sus filas llevan la columna de la foto: un solo borde izquierdo.
- **P2-7 · cabecera de la carta: hecho.**
  - Logo y ‹Inicio› (desde 700 px), ‹Cómo llegar› y ‹Escríbanos al DM› (‹DM› en el teléfono), como enlaces compactos, más ES/EN.
  - Las pestañas siguen fijas debajo.
- **P2-8 · promos: hecho.**
  - `.promo` con `margin: 0`: la hoja no se sale de la grilla.
  - El sábado queda en la misma columna gracias a la columna de foto vacía.
  - "Almudcito promos" va en caja de oración y en body (CSS sobre el literal en caja alta).
  - El día va en su propia línea.
- **P2-9 · encabezado de la semana: hecho.**
  - «siempre es un güen día pa compartir algo rico» pasa a body y cierra el bloque de la frase.
  - "Hoy" va como etiqueta en la tinta del campo, sin subrayado. "El martes" (Dom/Lun) tampoco va subrayado.
- **P2-10 · Dónde y mapa: hecho.**
  - El mapa se carga al tocar: un panel con la dirección y ‹Ver mapa›. Sin JS es un enlace a Maps; con JS crea el iframe de Google Maps solo después del toque (0 pedidos antes).
  - La calle (video) va ancha, en 9 columnas, y la puerta junto a los datos.
- **P2-11 · EN sin datos duplicados: hecho.**
  - `.dato-es` oculta en EN el literal cuando el dato es idéntico: horario (portada, hoja, Dónde, pies y Dom/Lun), precio, horario de la promo, nota de stock y cifras.
  - El texto de la marca sigue literal más su glosa.
- **P2-12 · objetivos táctiles: hecho.**
  - Créditos (`.pie a`): 24 px.
  - @ del equipo bajo 700 px: 44 px.
  - Medido: 0 objetivos sueltos bajo 24 px.
- **P2-13 · orden: hecho, según el brief y el director.** El equipo va después de Con quién; los destacados quedan pegados a Comida. El guion (§0) está actualizado.
  - **No hecho:** recortar El lugar a titular + banda + 3 rincones. Se quitó el loop de flecos, pero el mural (los cuadros, que pidió el cliente) y la barra se quedan.

## P3
- **P3-1 · crédito de la portada: hecho en el teléfono.** Va abajo a la derecha, al pie de la zona de la foto, dentro del scrim y sin fondo. En escritorio se mantiene la pastilla abajo a la derecha.
- **P3-2 · logo sobre el neón: hecho, en parte.** El logo baja (de .243 a .252 de S) y se achica (de .38 a .36 de S). La punta inferior todavía toca el neón "Almud" de la foto, sin pisar caras.
- **P3-3 · la "C" y el calefactor: hecho.** `.cover-info` queda a margen + 8 px y con un ancho de .25 de S.
- **P3-4 · hueco en Equipo: hecho.** `.equipo-txt { gap: 8px }`.
- **P3-5 · logo del pie: hecho.** `min(100% − 2·margen, 960px)`, alineado a la izquierda.
- **P3-6 · fotos repetidas: hecho.**
  - Jueves: `hoy-jueves-fiesta` (P084, IG-082, «jueves de sangriita», abrazo y carcajada). La sangría P228 queda solo para los destacados y la carta.
  - Sábado: `con-quien-barra` (P031) en lugar de `con-quien-solo`.
- **P3-7 · "Video @rober.patagonico" bajo una foto: no cambiado.** Es la portada de su reel y el crédito nombra la obra fuente (igual que el fotograma del mural). Agregar "(de su video)" sumaría texto nuestro.
- **P3-8 · banda rosada vacía en la carta: hecho.** `min-height` solo bajo 1024 px.
- **P3-9 · filas de Emil sin bloqueo: hecho.**
  - `--d-photo` (600 ms) y `--delay-hoy-h` / `--delay-hoy-foto` como tokens, sin ms escritos a mano en CSS.
  - Sin reveal en las reseñas: se quitó `fade-arm`.
  - La carta no anima al cargar.
  - Con el teclado, el color de pestañas y chips cambia al instante (`.kb`).
  - El video solo MP4 salió del landing (0 pedidos fallidos).
  - Lo que ya se ve al cargar sigue sin animar: solo se arma lo que está bajo el pliegue.

## Repetición del motivo de cintas
En las primeras 7 pantallas aparece 2 veces: la portada y la terraza techada (P090). El loop de flecos salió del landing.

## Otras notas
- **Movimiento en la carta.** Para pasar `still-page` sin volver a los loops borrosos:
  - la firma del pie usa la máscara de línea de los titulares;
  - la lámina de Coctelería suma la copa tallada (P097), que se revela al bajar.
- **Placeholders de imagen.** Las fotos ya no pintan su color dominante plano como fondo, solo el LQIP. El inspector lo leía como un "campo terracota" (`palette-claude`).
