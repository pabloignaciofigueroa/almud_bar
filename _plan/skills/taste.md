# Taste skill (tasteskill v2) — resumen operativo para el rediseño de Almud Bar

Fuente: `/mnt/user-data/outputs/skills/taste/` (SKILL.md + references/ salvo app-screens.md + scripts/ + library/). Leído completo el
2026-10-21. Este archivo es la versión accionable; ante duda, manda el original. Una página "de lectura y scroll" (bar/restaurante) sigue
**la run de página**, no la de app-screens.

Idea central: reemplazar los defaults de modelo por decisiones (script reparte direcciones; idea desde el sujeto; house style medido en
navegador; mirar capturas y corregir). **Quitar ornamentos es sólo la mitad**: una página pelada pierde contra una rica con tells; la otra
mitad es sustancia (tipo grande, campos de color, fotos reales, contenido completo).

---

## 1. La run (10 pasos)

1. **Leer brief y proyecto.** Qué es real: sujeto, público, la UNA cosa que la página debe lograr, stack, marca existente, y sobre todo
   **qué imágenes existen de verdad**. Si el pedido es vago, decidir y decirlo en una línea. **Inventario del sujeto: 8–12 cosas que son de
   este cliente y de ningún competidor** (nombre y qué significa, dirección/calle/barrio y cómo se ve, números del brief, la restricción con
   la que vive, materiales y colores, rituales y horarios, los impresos de su mundo: carta, ticket, afiche). "En tests ciegos, la página
   ganadora salió de un ítem de esa lista."
2. **Escribir el argumento.** La página como lista de claims con su prueba, una línea por sección (copy.md §1). Sección sin claim = se
   borra. Así se evita hero/logos/3 features/testimonio/precios/CTA.
3. **Sortear la dirección.** `draw.mjs --options 3` reparte 3; elegir la que mejor carga algo del inventario ("no la más familiar") y anotar
   por qué en una línea. Luego hoja completa con `--direction <id>`. **Adoptarla**, no mezclarla con lo que uno habría hecho. Redraw de un
   slot sólo con razón enunciable (contradice restricción de marca o pide un asset inexistente); nunca por comodidad; registrar cada redraw.
   Si una sección repartida no aguanta el contenido real: `--alternatives <role>` y `--redraw section:<role>=<id>`. Paleta: si choca con el
   sujeto, redraw una vez; si el sujeto tiene colores propios, mantener las **proporciones** repartidas y tomar los colores del sujeto.
4. **Encontrar la idea.** Escribir: *"En esta página, **[algo del sujeto]** se vuelve **[el dispositivo de la dirección]**."* Fuentes: su
   output, su objeto/forma, su nombre, su lugar, su ritual, su artefacto impreso, su opuesto. **Test del competidor**: poner al competidor
   más cercano en la frase; si sigue funcionando, la idea es de la categoría. **Una cosa viva** (live thing): algo que el visitante puede
   hacer o que cambia por visita, hecho con contenido real, usable con el pulgar, con fallback sin script, que nunca bloquea la lectura, y
   que es UNA cosa, no un parque de juegos. Las escenas de scroll también cargan la idea: decidir qué muestra cada una desde el inventario.
5. **Escribir las palabras** (copy deck en texto plano antes del markup). Todo titular ≤ 2 líneas a todo ancho (~32 caracteres seguros). Una
   frase de apoyo justo bajo el titular (32–48px abajo), visible con él. Una acción primaria con nombre de lo que hace, como botón real en
   la primera pantalla. La primera pantalla responde la primera pregunta en tipo grande (qué, cuándo, dónde). Cada sección a la que el
   visitante viene tiene heading propio y lugar en la nav. **Contenido completo** (toda la carta con precios). Prueba social jamás
   inventada.
6. **Construir, quieto** (sin motion en la cabeza). Orden: tokens → hero exacto al blueprint (desktop y teléfono) → cada sección desde su
   blueprint, la idea en todas (también FAQ y footer) → imágenes (orden de preferencia: propias > generadas > colecciones abiertas >
   dibujadas en código > fotos repartidas > tipo y color) → la cosa viva → escenas de scroll → plenitud (cada pantalla como afiche; 1
   descanso por página máx.) → el marco (márgenes iguales, nada amontonado a un lado, ningún tramo vacío > ½ pantalla, secciones a 120–240px
   en desktop, h1 en primera pantalla, heading en cada sección) → estados y semántica. **Piso de imágenes (lo mide el inspector): ≥4
   imágenes reales, normalmente 6–12**; SVG no cuenta. Con footage propio, la primera pantalla lo muestra grande (~40%+). Nunca una frase
   sobre de dónde vienen las fotos.
7. **Gate.** `lint.mjs` + `inspect.mjs` (+ `scenes.mjs` si hay escenas). Arreglar cada FAIL; cada WARN es un error salvo que se defienda en
   una frase ante un diseñador. "No discutir con el medidor ni esconderle cosas."
8. **Mirar.** Abrir TODAS las capturas y criticar con critique.md (14 pasadas, puntaje, caps). Escribir la crítica en su formato, arreglar
   los 3 problemas top, re-inspeccionar. Máx. 3 rondas. "Si se ve en la captura, es real, diga lo que diga el código."
9. **Mover.** Capa de motion obligatoria: el inspector cuenta elementos que se mueven al cargar y scrollear; **FAIL < 8, WARN < 16**.
   Partes: movimiento firma (uno), entrada por partes en cada sección (heading→texto→imagen, stagger 60–90ms, sube 16–32px con opacidad, una
   vez), feedback en cada control, una imagen en movimiento. Sólo transform/opacity; fallback `prefers-reduced-motion` que conserva el
   contenido.
10. **Reportar** sólo si: 0 FAIL a 1440/768/390 en la versión final; abriste cada captura tras el último cambio; con escenas, `scenes.mjs`
    limpio y leídas todas sus hojas; un extraño en 5 s dice qué es y qué hacer; cada sección con heading, márgenes iguales, nada vacío;
    crítica de la última ronda escrita en el formato §4. Reportar: dirección (nombre+seed) y redraws; frase-idea y cosa viva; puntajes
    finales y lo que falta; créditos de imágenes encontradas; qué contenido es muestra. "No afirmar un chequeo no hecho."

**Caso rediseño (nuestro caso):** 1) grabar el *before* (`inspect --out .taste-skill/before` + lint); 3) conservar stack, contenido y lo que
funciona (sin migraciones; revisar dependencias antes de agregar); un rediseño reparte dirección completa y reconstruye secciones desde
blueprints; 4) orden: tipo → color → marco → estados → componentes stock; 5) probar: inspect a `.taste-skill/after`, comparar a cada ancho,
clicar cada link/menú, reportar antes/después lado a lado. Marca existente: `--keep palette,type`, mapear colores/fuentes de la marca a los
roles; si la marca exige algo prohibido, conservarlo, decirlo y usar `--allow <regla>` sólo para esa regla.

---

## 2. House rules (todas; las mide inspect.mjs) y leyes del oficio

| Regla | En su lugar |
| --- | --- |
| Titulares ≤ 2 líneas a todo ancho (h1–h6 y la línea principal del hero) | Cortar palabras → ensanchar medida → tamaño al final |
| Título claro en la 1ª pantalla en el único `h1`; heading en cada sección | Nombre + qué hace / evento + fecha y lugar |
| Márgenes externos iguales; ninguna sección amontonada a un lado | Cerrar cada vacío con algo al otro lado |
| Sin tramos en blanco > ~½ pantalla | Gap normal; un descanso deliberado (foto o campo de color) por página |
| Las declaraciones son párrafos (`<p>`/`<blockquote>`), ≤36px desktop / 24px teléfono, ~25 palabras, 3 líneas | Más grande = titular y aplica la regla de 2 líneas |
| Sin eyebrows (label chico sobre heading, pill sobre el titular, chip "Nuevo ·") | Meter la info en el heading o la 1ª frase |
| Sin monospace fuera de código | Fuente de texto; cifras tabulares |
| Sin numeración índice (01/02/03, (001), "Paso 2") | Orden por posición/tamaño/palabras; `<ol>` real |
| Sin reglas finas (hairlines, cajas 1px, grillas, crosshairs, marcas de corte) | Espacio, escalón de tono, cambio de escala, forma rellena |
| Sin degradés (fondos, botones, texto) | Plano o foto real; única excepción: scrim neutro bajo texto sobre foto |
| Sin sombras en reposo, sin glows | Escalón de tono; sombra sólo en lo que flota (menú, diálogo) |
| Sin paleta de asistente (crema amarillento + terracota/óxido; violeta/índigo) | La paleta repartida |
| Sin mayúsculas diminutas espaciadas | Sentence case a tamaño legible |
| Sin feature cards con ícono, sin filas de cards idénticas | El blueprint repartido |
| Sin glass (backdrop blur, nav-píldora flotante) | Barra plana: wordmark, pocos links, una acción |
| Sin emoji, blobs de degradé, formas decorativas, dashboards falsos | Foto real, fragmento real, o nada |
| Sin palabra acento estilizada en el titular (itálica, serif, color, subrayado) | Una fuente, un color |
| Máximo dos tipografías (normalmente una) | El sistema repartido |

Excepciones que el inspector deja en paz: código real en `<pre>/<code>`, tablas y campos de formulario reales, fragmentos de interfaz con
`data-ui`. "Quitar ornamento deja espacio. Nunca llenarlo con otro ornamento": llenarlo con escala, contenido completo, una imagen hecha
para el sujeto o un campo de color.

**Leyes del oficio** — *Tipo*: 2–3 tamaños hacen el trabajo; ratio titular/cuerpo mediana 4.3 (top 4.7); tipo más grande del top 8.4vw vs
5.0vw en los débiles; display tracking −0.02 a −0.05em, leading 0.85–1.05; texto 16–20px, leading 1.45–1.6, 45–75 car./línea; 5 tamaños
techo; alineado a la izquierda, centrar un momento como mucho. *Espacio*: una grilla, un par de márgenes apretados 16–32px; bloques de texto
comparten 2–3 bordes izquierdos; asimetría dentro de la grilla, nunca en el marco; gap entre secciones claramente mayor que dentro
(120–240px); cada sección distinta de sus vecinas, ninguna es grilla de cards. *Color*: un fondo, una tinta, un acento (en la acción y quizá
otra cosa); texto corrido en tinta plena; superficies separadas por tono, nunca línea ni sombra; una sección puede cambiar el campo entero;
nada se funde en nada. *Imagen*: una dominante > seis chicas (hero ≥ ½ pantalla en 68% del top); mismas proporciones y tratamiento, esquinas
rectas; nada encima de un titular. *Componentes*: botones planos, un color, cuadrados o totalmente redondos, decidido una vez (radio "soft"
9–16px = default de sitio débil); nav: wordmark + 3–5 links + una acción, sin cromo; footer = cierre diseñado (el nombre a todo ancho), no
sitemap.

---

## 3. Registro de tells (tells.md)

**Ola 1 (2023–24):** degradés violeta/índigo (banned); texto con degradé (banned); glass/blur (warned ≥2); botón "Get started" con
glow/degradé (banned); sombra gris bajo cada card (banned); 3 cards idénticas con ícono en cuadrado redondeado (banned); emoji como
íconos/bullets (banned); titular centrado + subtítulo + 2 botones + screenshot (sin regla, el draw lo evita); la misma fuente en toda página
generada (warned). **Ola 2 (2025):** eyebrow/kicker (banned); pill badge sobre el hero (banned); una palabra del titular en itálica
serif/color/subrayado (warned); bento de tiles redondeados (warned); casi-negro + un neón con glow (banned vía sombra/degradé); nav-píldora
flotante con blur (warned); dashboard falso de barras grises; punto de estado decorativo ("disponible", pulsante); fade-and-rise en cada
sección. **Ola 3 (2025–26, "el arreglo que se volvió el look"):** crema amarillento + terracota/óxido (banned juntos; terracota sola banned;
crema warned); serif display como atajo a "premium"; titular serif itálico gigante; cosplay de periódico (hairlines por todas partes, radio
cero, columnas densas; banned vía hairline); labels performativos ("Field notes", "Quietly trusted by"). **Moda de galería prohibida como
house style:** labels/captions monospace (banned); numeración índice (banned); reglas finas, grillas, cajas 1px (banned, cajas ≥3); cromo de
herramienta de diseño (crosshairs, marcas de corte, guías punteadas, reglas; banned); micro-meta de agencia (hora local, coordenadas, clima,
"©2026 — Scroll", strings con punto medio; lint); mayúsculas diminutas espaciadas dispersas (banned ≥3). **Estructurales:** titular-frase de
3–4 líneas (banned); orden stock de secciones; todas las secciones con el mismo layout; todo centrado (warned > 72%); un radio medio 12–16px
en todo; nueve tamaños casi iguales (warned > 9); prueba social inventada; texto o caja CSS donde va una imagen. **Copy:** verbos/adjetivos
del género (unlock, seamless, elevate…); la corrección ("no es sólo X, es Y"); titulares en tricolon; "Get started"/"Learn more"; exceso de
guiones largos; lorem. **Motion:** el mismo fade-up en cada bloque; una docena de entradas escalonadas en el hero; hover-lift en cada card;
easing bounce; loops infinitos sin sentido; reveals que fallan y dejan franja en blanco. **Por qué quitar no basta:** página sin tells y sin
nada en su lugar = "estética de la evitación", también un tell. Los tells llenaban el hueco donde debía estar una idea.

---

## 4. Reglas por área

### Imagen (imagery.md)
- Piso **≥4 reales, típico 6–12** (mediana 7). Footage propio: mediana 3–4 clips; **un clip en movimiento por pantalla**. ~1/3 de la página
  es imagen; ≥1 de cada 4 pantallas sin imagen. **Una imagen lidera su pantalla (≥60%) o queda chica (<10%).**
- **3–5 ubicaciones distintas por página**, nunca la misma en secciones vecinas (≤2 ubicaciones: 7.31; ≥3: ~7.5). Ranking que favorece al
  top: split (foto en ½ o ⅔, a toda altura, tocando el borde del viewport por fuera, texto desde la línea del 50%; teléfono: foto primero a
  todo ancho), foto sostenida mientras pasa el texto, mosaico desigual (2–3 anchos, desfases verticales 120–190px, caption de una línea sin
  número), marco que crece (una vez por página, del 35–50% del ancho a pantalla completa en 720–2700px de scroll), recorte sobre campo
  plano, fotos con el tipo (entre palabras: 2–4 chips de la misma sesión). Banda full-bleed: 100% ancho, 100–150vh, una cada 3–4 pantallas,
  texto sólo en una esquina ≥32px adentro. Galería horizontal: 3 cards y una 4ª cortada, 25–35% del ancho; teléfono una card al 75–80%.
  Marquee de fotos lento (60–120 s por vuelta). **Galería 3D: no construir.** Collage disperso: con cuidado; **prints inclinados y stickers
  con sombra no son tratamiento**.
- **Recortes:** 2 ratios para ≥75% de las fotos (defaults 4:5 retrato, 16:9 o 3:2 paisaje); tercer ratio sólo como excepción. `object-fit:
  cover` + `object-position` elegido por foto. **Esquinas rectas** (94%); si se redondea, un radio (4px) para todas. Sin marcos, sin bordes,
  sin sombras, sin mockups.
- **Tratamiento único para toda la página:** intocado (default), o todo greyscale, o multiply sobre campo, o oscurecido para página oscura
  (`brightness(.85) contrast(1.05)`). **No son tratamientos:** lavados de color, duotono, blur, grano, viñeta, **polaroids inclinadas con
  sombra**.
- Texto sobre foto: sólo display, una línea y una acción; contraste medido en la posición del texto (4.5:1, o 3:1 ≥24px) a lo largo de todo
  el loop; si falla, scrim neutro (bloque 40–55% negro o fade 55%→0 en el tercio inferior), nunca overlay de color. Cuerpo de texto nunca
  sobre foto/video.
- Video: muted, loop, inline, `playsinline`, **poster obligatorio**, pausado fuera de vista y bajo reduced motion (snippet
  IntersectionObserver en imagery.md §11), 5–15 s, hero ≤10MB 1080p, inline ≤5MB 720p, `aria-hidden`. Teléfono: recorte retrato a pantalla
  completa.
- Markup: `width`/`height`, `loading="lazy"` salvo hero (`fetchpriority="high"`), `alt` descriptivo, fondo del contenedor.

### Tipo (type.md)
- Escala: small 13–14 / body 17–19 / lead 20–26 / head 32–64 / display (lo da el blueprint, en `clamp()`). Display ≥4× body; nada entre lead
  y head. Si dos tamaños se parecen, que sean iguales.
- Display >40px: leading 0.85–1.05, tracking −0.02…−0.05em (más apretado cuanto más grande), `text-wrap: balance`, `max-width` en ch, ajuste
  óptico −0.05em; mayúsculas: tracking 0…+0.03em, leading ~0.9. Nunca text-shadow, contorno ni degradé en display.
- Texto: medida 45–75 car. (warn >88), leading 1.45–1.6; secundario = misma fuente en `--muted`, nunca <13px; no centrar párrafos >3 líneas;
  no justificar. Claro sobre oscuro: bajar un peso o +0.01em.
- Dos familias máx., cada una con un trabajo fijo; no tercera para labels/números; itálica sólo para títulos de obras o énfasis real.
  Detalles: comillas tipográficas, `tabular-nums` en precios, subrayado con offset .18em, `hyphens:none` en headings, espacio sobre heading
  ≥2× el de abajo, no cambiar peso en hover. Errores invisibles al inspector: huérfana en la línea 2, corte que parte la frase, headings de
  sección casi tan grandes como el hero.

### Layout (layout.md)
- Márgenes `clamp(1rem, 2.2vw, 2rem)` (16–32px), iguales a ambos lados a todo ancho, nunca <16px (también teléfono); la nav en los mismos
  márgenes. Sin contenedor 1200px centrado por reflejo; restringir sólo la medida del texto. Grilla de 12 columnas, nunca dibujada.
- Texto colgado de 2–3 líneas ancla para toda la página (tercio, 42%, mitad); off-centre > centrado; "extremos opuestos" en una misma línea
  base; centrar es una decisión (un eje, flancos vacíos, un elemento).
- Vacío: un "rest" lo cierra algo (la foto, una foto al otro lado, el tipo grande); un "hole" no. Causas de huecos: gaps de 250–760px, texto
  en una mitad y nada en la otra, contenido que llega tarde (reveal), bloque corto estirado a 100vh, escena fijada que no contiene nada,
  fotos de distinta altura alineadas arriba. Secciones a 120–240px en desktop, 72–112px en teléfono.
- Primera pantalla: un `h1` display (50–150px), ≤2 líneas, que diga qué es; si es el nombre, debajo ≥18px que diga qué es. Heading en cada
  sección (mediana 57px, ~3.5× cuerpo), en el mismo ancla.
- Secciones: la idea llega al último píxel; ningún vecino comparte layout (contar las palabras de layout); alternar denso/vacío,
  imagen/tipo, claro/oscuro; módulo repetido sólo para archivos (carta, agenda); romper el sistema una vez a propósito.
- Nav: wordmark + 3 links (mediana) + acción, sin barra/borde/fondo; si fija, nunca encima de contenido; en teléfono, wordmark + acción y un
  "Menú" de texto que abre hoja a pantalla completa; ≤1/10 de la 1ª pantalla. Final: escena diseñada (nombre a todo ancho, hero invertido,
  el dato de contacto como titular), datos prácticos a tamaño legible.
- **Teléfono = segunda composición**: re-autorizar cortes de línea, re-recortar a retrato, mantener irregularidad con anchos alternos,
  márgenes 16–20px, cuerpo 16–18px, targets ≥44px.

### Color (colour.md)
- Roles: `--bg --surface --ink --muted --accent --accent-ink` (+ `--field-n` con su tinta). Todo por token; un hex suelto en un componente
  es una segunda paleta.
- Proporción: fondo 70–90%; tinta en texto y quizá una sección invertida; **acento <5% de cualquier pantalla** (la acción + una cosa
  recurrente). Paletas con campos (flat-loud): cada sección un campo a plena fuerza y la proporción vale dentro de la sección (campo, su
  tinta, nada más). El acento no va en headings/íconos/bullets/bordes. Un titular es tinta.
- Campos: bordes duros, nada se funde; cada campo con su tinta propia (nunca `--muted` sobre campo); vecinos difieren en luminosidad, no
  sólo tono; ordenarlos como capítulos (abrir fuerte, descanso, sorpresa, cierre muy oscuro o muy claro).
- Página oscura: `color-scheme: dark`, fondo profundo levemente teñido, tinta clara suave (no #fff/#000), `--muted` ≥4.5:1, profundidad por
  escalón de superficie, jamás glows.
- Contraste: cuerpo 4.5:1, display 3:1; el inspector falla <2.6:1 en fondos planos y no ve texto sobre fotos.
- Prohibidos: crema+terracota; violeta/índigo. Si la marca los posee: `--keep palette` + `--allow palette-purple` (o la regla) y anotarlo.

### Copy (copy.md)
- Argumento primero: quién lee, qué es (dicho como a un amigo), qué creer tras una pantalla, qué lo probaría, qué hace después; luego
  claims→prueba por sección.
- **Aritmética de dos líneas:** `caracteres/línea ≈ ancho px ÷ (tamaño px × k)`, k ≈ 0.40 condensadas, 0.50 grotescas/serif display, 0.58
  anchas/mayúsculas. Presupuestos: teléfono 350px a 44px ≈ 16/línea → **~32 caracteres**; a 34px ≈ 42; tablet 690px a 64px ≈ 44; desktop
  1100px a 104px ≈ 42; mitad 620px a 72px ≈ 34. Headings de sección: 2–5 palabras. Autorizar el corte (`<br>`), `text-wrap: balance`, sin
  huérfanas; nunca resolver sólo achicando.
- Formas que sirven: el nombre; qué es; el claim; la instrucción; **el lugar o el momento ("Lisboa, desde 1984")**. Evitar: mad-lib,
  tricolon, corrección, "X reimaginado", "Bienvenidos a…", pregunta no hecha, titular con dos puntos, palabra estilizada. Sentence case, sin
  punto final.
- Apoyo ≤22 palabras, concreto. Cuerpo: sustantivo específico y número real. Botones 1–3 palabras con la acción ("Ver la carta"); un
  primario por pantalla, el segundo es link de texto; una flecha como mucho.
- Prueba: nunca inventar clientes, citas, logos, cifras; detalles de muestra sí, listados en el reporte.
- Microtipografía: “ ” ’ …, guion medio en rangos, `&nbsp;` número-unidad, nada <13px, mayúsculas sólo hasta 3 palabras con 0.02–0.06em.

### Motion (motion.md)
- **Presupuesto**: 2–3 escenas de scroll (donde la página es audaz); **un momento firma** (el único fuerte); entradas coreografiadas por
  sección (orden de lectura, stagger 60–90ms, sube 16–32px, una vez, variando la manera según el contenido); feedback bajo la mano; una
  imagen en movimiento. Inspector: FAIL <8 elementos en movimiento, WARN <16.
- **Tokens:** `--ease-out: cubic-bezier(.22,1,.36,1)` (UI <600ms) · `--ease-expo: (.16,1,.3,1)` (reveals ≥800ms, line rises, aperturas) ·
  `--ease-in-out: (.76,0,.24,1)` (wipes, paneles) · `--ease-soft: (.33,1,.68,1)` (scale/drift lento en fotos) · `--ease-exit:
  (.55,.055,.675,.19)` (sólo salidas definitivas) · `--t-press 140ms` · `--t-hover 180ms` · `--t-ui 240ms` · `--t-reveal 800ms` · `--t-open
  1200ms` · `--stagger-line 90ms` · `--stagger-item 70ms`.
- **Duraciones**: press 140; hover color 180–200; hover que mueve 300–400; menús 240; reveals 700–900; aperturas de foto 1100–1300; salidas
  60–70% de la entrada. **Staggers**: líneas 80–110, ítems 50–90, caracteres 20–40 sólo en headings de 1–3 palabras; máx. 4 pasos por
  secuencia. **Reveals**: una vez, cuando el top está al 85–90% del viewport; nada visible oculto >900ms; nada sobre el pliegue espera
  scroll.
- **Recetas** (todas con gate `html.js` y estado oculto sólo en `no-preference`): Load sequence en 1.2 s (líneas suben 100–990ms, foto abre
  150–1150ms, frase y botón 420–980ms, máx. 4 cosas); Masked line reveal (900ms, 110ms entre líneas); Reveal on scroll (opacity 700ms +
  transform 900ms, rootMargin −12%); Image shutter (clip 1100ms in-out, img de 1.12 a 1 en 1500ms); Press and hover (scale .97, hover tras
  `(hover:hover)`); Scroll-linked progress (`animation-timeline: view()`, recorrido <8%); Pinned story (sticky top 18vh); Index with preview
  anclado a la fila (frame 30% ancho, clip 320ms, filas atenuadas a 0.4); Lines that rise on scroll (split tras fuentes, 900ms expo);
  Opening window (sección 200svh, ventana desde inset 20%/28% a full en contain 0–75%); Held picture, passing captions (pasos ~80svh,
  crossfade 500ms, inactivos 0.4, cuenta "2 de 4" en texto); Sideways gallery (fila nativa con snap; pin sólo ancho ≥900 y fila <3
  pantallas, 1:1); Receding hero (foto baja 8% y escala 1.06, velo de tinta ≤35%, texto sube 6%); Page to page (view transitions ≤480ms);
  Ink fill (una declaración por página, desde 45% de tinta, ≥32px, 3–5 líneas); Rolling figures (1100ms expo por columna); Accordion
  (`grid-template-rows` 0fr→1fr 320ms); Menu/dialog (desde 0.95–0.98, origen en el disparador).
- **Firmas**: Masked headline, Shutter image, Scaling wordmark, Pinned story, Index with preview, Curtain footer, **Slow crossfade** (la
  sugerida para restaurante: 3–4 fotos, 5–6 s c/u, fundido ~1.6 s), Edge-to-edge marquee (una, pausable), Drag row, Colour by chapter,
  Opening window, Ink fill, Sheet over a held picture, Sideways gallery, Pushed line, Rolling figures, Carried picture. Si no dice nada del
  sujeto, es decoración.
- **Prohibido/house:** sin preloader, contador, gate, cursor custom ni captura de rueda; Lenis sólo vía `Stage.smooth()` (lerp 0.1–0.14, off
  en touch y reduced); sin overshoot/bounce; sin scramble/typewriter; sin loops sin interruptor (grano, puntos pulsantes); nada se mueve
  sobre texto que se lee; atenuados ≥40%; blur ≤8px y se va; máx. 2 escenarios fijados, ~1 pantalla por paso, 3 por escenario; reduced
  motion = página terminada, loops detenidos.

### Escenas de scroll (scenes.md)
- Qué es: sección alta (hold+1 pantallas) con escenario `position: sticky`; un timeline GSAP se scrubea 0→1 con el scroll. Nada captura la
  rueda; la escena termina.
- **El catálogo está vacío en esta copia**: `library/scenes.json` no existe, `draw.mjs --list scenes` → "No scene library yet.";
  `assets/scenes/` sólo trae `stage.js` y `stage.css` (sin demos ni escenas). Por lo tanto **las escenas se construyen a mano sobre el
  Stage** (scenes.md §8): `Scenes['mi-escena'] = (root, opts) => Stage.scene(root, { hold, scrub, phone: 'same'|'rest'|{…}, build(tl, {q,
  phone}) {…} })`, primero el CSS de la composición terminada, luego `.scene.is-live`. API: `Stage.smooth()`, `Stage.scene()`,
  `Stage.split(el,'lines'|'words'|'chars')`, `Stage.ready()`, `Stage.init()` (arranca cada `section.scene[data-scene]`). Marcado: `<section
  class="scene" data-scene="id" data-options='{"hold":3}' aria-label="…"><div class="scene-stage">…`.
- Reglas: 2–3 por página de familias distintas, una sección quieta entre ellas (inspector: WARN >4 `many-scenes`, >60% de la página
  `scene-heavy`); cada una 1–4 pantallas (~1 por "beat"); scroll nativo; legible en sus puntos de reposo; transform/opacity/clip-path; house
  rules adentro (sin contadores 01/07, sin degradés, sin partículas); composición terminada diseñada (es lo que ven reduced motion, sin
  script, CDN caído — el stage agrega `.is-rest`; en desktop eso es FAIL `scene-not-live`). Llenarla con fotos de una sola familia (misma
  luz), declaraciones de 4–12 palabras, captions de 1–4 palabras. Si faltan fotos reales: redraw de escenas, nunca relleno. Tokens que leen:
  `--ground --ink --muted --accent --font-display --font-text`.
- Chequeo: `scenes.mjs <page>` (cada escena al 0,10…100%, desktop, teléfono, reduced) → `.taste-skill/scenes/`.

### Crítica (critique.md)
**14 pasadas** sobre capturas, nunca sobre el código: 1) un segundo, luego cinco (una sola respuesta; ¿qué es, para quién, qué hacer?); 2)
entrecerrar ojos (2–3 masas); 3) tapar el logo (¿podría ser de un competidor? ¿llega la idea a FAQ y footer?); 4) bordes (contar x de
inicio: 2–3 bien, 6 mal); 5) espacio y marco (rest vs hole, márgenes iguales, mitades vacías, tramos >½ pantalla); 6) tipo (salto ≥3×, ≤5
tamaños, huérfanas, medida, centrados); 7) color (proporciones; acento en una acción + un detalle); 8) imágenes (≥4 reales, una en
movimiento, ratios, luz común); 9) igualdad (una palabra de layout por sección; repetida seguida o 3 veces = plantilla); 10) teléfono
(composición propia); 11) plenitud (cada pantalla un afiche); 12) sustancia (cada sección completa, botón primario real en 1ª pantalla); 13)
colisiones (nada sobre titulares/botones, nada fuera del borde del teléfono); 14) competidor y cosa viva. **Puntaje Awwwards:** `overall =
0.4·diseño + 0.3·usabilidad + 0.2·creatividad + 0.1·contenido`. SOTD reales ≈ 7.5–8.0; un 8.5 honesto es raro; si te das 9, puntúa de nuevo
como jurado ajeno. **Caps:** FAIL vigente → overall ≤6.0 · titular ≥3 líneas, eyebrow, mono, 01/02/03, degradé decorativo, sombra en reposo
o hairline visible → overall ≤6.5 · pasada 3 falla → creatividad ≤6 · idea vale para el competidor → creatividad ≤7 · <4 fotos reales →
diseño ≤6.5 · página quieta o fade idéntico → diseño ≤7 · sin cosa viva → creatividad ≤7.5 · placeholder → contenido ≤5 · ≥2 pantallas
vacías o texto chico y gris → diseño ≤6.5 · sección pedida ausente o mínima → contenido ≤6 · sin botón primario real en 1ª pantalla →
usabilidad ≤7 · falla el test de 5 s → usabilidad ≤6 · márgenes desiguales/sección a un lado/tramo vacío → diseño ≤6.5 · sección de texto
sin heading → usabilidad ≤7 · algo tapa un titular → usabilidad ≤6 · franja en blanco por reveal o contenido cortado → usabilidad ≤5.
**Formato §4 (literal):**
```
ROUND n
Seen in one second: …
Idea (one sentence): …
Live thing: …
Layout words by section: hero=… / …=… / …
Scores: design _ · usability _ · creativity _ · content _ → overall _._
Caps applied: …
Top three problems (most visible first), each with the screenshot it shows in and the fix:
1. …
2. …
3. …
```
Orden de arreglo: idea → jerarquía → composición → tipo → imágenes → color → detalle → motion. Máx. 3 rondas; si la 3ª sigue <7.5, decirlo
sin redondear.

---

## 5. Scripts: cómo correrlos aquí y resultados

**Entorno:** Node `v22.22.0` (cumple 22+). Chromium en `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`. Corremos como root ⇒ Chrome
exige `--no-sandbox`, y `lib/cdp.mjs` no tiene forma de pasar flags extra; `findChrome()` sólo lee `CHROME_PATH` /
`PUPPETEER_EXECUTABLE_PATH`. Solución sin tocar la skill: un wrapper (copiado en `_plan/skills/chrome-nosandbox.sh`):
```sh
#!/bin/sh
exec /opt/pw-browsers/chromium-1194/chrome-linux/chrome --no-sandbox --disable-dev-shm-usage "$@"
```
**Red:** `draw.mjs`, `lint.mjs`, `inspect.mjs`, `scenes.mjs` funcionan offline (cero dependencias; el inspector sirve archivos locales por
un servidor 127.0.0.1). `assets.mjs` **no funciona**: el proxy rechaza api.openverse.org (403); tampoco hay acceso a cdn.jsdelivr.net ⇒ usar
GSAP/ScrollTrigger/Lenis de `vendor/` (ya están). No lo necesitamos: tenemos ~450 fotos + 54 reels propios.

**Comandos que funcionan (desde `/home/claude/almud_bar`):**
```bash
S=/mnt/user-data/outputs/skills/taste/scripts
CH=/home/claude/almud_bar/_plan/skills/chrome-nosandbox.sh     # chmod +x ya aplicado
node $S/draw.mjs --list sectors | roles | tones | directions | scenes
node $S/draw.mjs --sector restaurant --brief "Almud Bar, playful cocktail bar in Castro, Chiloé, Chile, since 2014" \
  --sections intro,gallery,list,about,contact,footer --have photography,video --keep palette,type --options 3
node $S/draw.mjs <mismos args sin --options> --direction <id>      # escribe .taste-skill/direction.json
node $S/draw.mjs --show | --redraw section:list | --alternatives list | --site <id>
node $S/lint.mjs index.html css js                                 # exit 1 si hay FAIL
CHROME_PATH=$CH node $S/inspect.mjs index.html --out .taste-skill/before   # luego --out .taste-skill/after
CHROME_PATH=$CH node $S/scenes.mjs index.html                       # cuando haya escenas
```
Notas: `--options` no escribe nada y **cada ejecución reparte otra terna** (no imprime seed); la hoja completa sí imprime seed y la guarda;
historial en `~/.taste-skill/history.json` (aislable con `TASTE_SKILL_HISTORY=…`). 22 sectores (el nuestro: **restaurant**; también
hospitality). Roles: features showcase how-it-works testimonial proof stats pricing faq cta footer intro about work gallery list contact
(menu→list, booking→contact, team→about). Tonos: quiet bold warm technical playful luxury editorial (sólo si el brief lo pide). Escenas: "No
scene library yet."

**Sorteo pedido (`--sector restaurant … --have photography,video --keep palette,type --options 3`):**
1. **`one-motif` — One motif**: una forma del sujeto gobierna todo (máscara de fotos, botón, bullets, una banda). Hoja completa de prueba
   (seed 1348726837): hero "Striped card beside the room" (50/50, foto sticky + tarjeta impresa con franja); intro "Statement with inline
   thumbnails"; gallery "Wall of word tiles"; list "Two-column menu, photo bullets"; about "Inset panel, shaped portrait"; contact "Clip-out
   coupon form"; footer "The mark, built large"; firma **Slow crossfade**.
2. **`place-carries-it` — The place carries it**: una foto full-bleed del lugar es el argumento, el nombre como título de película. Hoja de
   prueba (seed 935637284): hero "Sentence with a photo strip" (frase en condensada gigante con una foto en lugar de una palabra); intro
   "Pinned sentence, photographs pass"; gallery "Photographs gathered round a heading"; list "Statement, table pushed right"; about "Wide
   photo, colour tile, facts"; contact "Visit card on a photograph"; footer "Contact as the headline"; firma **Shutter image**.
3. **`page-is-the-object` — The page is the object**: la página es el impreso de su mundo (la carta, el ticket, el posavasos). Hoja de
   prueba (seed 1281947434): hero "Tabbed folder stack"; intro "Title, note, facts row"; gallery "Photo tiles with label strips"; list "The
   printed menu sheet" (hoja con bordes festoneados, grupos, precios tabulares); about "Founder's letter"; contact "Clip-out coupon form";
   footer "The back of the card" (postal con estampilla-foto); firma **Index with preview**.

Otra corrida de `--options` dio `dark-room`, `one-motif`, `name-as-monument` (`.taste-skill/options-run2.txt`). Hojas de prueba:
`.taste-skill/preview/<id>.txt` y `/<id>/direction.json`; no son la elección: al elegir, repartir de nuevo a `.taste-skill/`.

**Lint v1 (`.taste-skill/before/lint.txt`): 40 FAIL, 7 WARN.** FAIL: emoji ×18 (😘 ♥ 😉 ✨ 👌 💥…), gradient ×9 (incluye `--rib` y los flecos),
shadow ×11 (drop-shadow, text-shadow, box-shadow), hairline ×2 (`border-bottom/top:1px` en la carta). WARN: outlined-box ×3, glass ×2
(backdrop-filter), scale-zero ×2.

**Inspect v1 (`.taste-skill/before/inspect.txt`, `report.json`, 10 capturas): 13 FAIL, 12 WARN.** Medido: hero "ALMUD BAR" 389px (27vw) Six
Caps, 1 línea; fuentes Oswald 75% / Six Caps 19% / Caveat 5%; **32 tamaños de fuente**; 23 pantallas, 1801 palabras, 51 imágenes; 91
headings. FAIL: `headline-lines` en 1440/768/390 (párrafos de 9–22 palabras a 43–92px que dan 3–7 líneas: "con muchas opciones de
destilados…", "Con los años, hemos crecido muchísimo…", "Un lugar que fuera cálido…", "con el objetivo de entregar…"); `emoji`; `gradient`
(div.fringe, fringe--b, #jornadas linear-gradient); `shadow` ×22 (figure.mass…); `text-shadow` ×10; `hairline` ×20 (div.lexicon,
ul.carta__list, li.dish); `few-pictures` (sólo 3 contadas en 1440); `lopsided` ("Ya saben que no somos ná sin ustedes!", "Peazo de equipo
que tenemos!" con 67% del ancho vacío); `covered-text` (las palabras del loader "Almud/cito/ito" y la frase del hero quedan tapadas en
pantalla 1); `empty-screens` (11 de 12 pantallas desktop casi vacías); `palette-purple` (#9b5cff). WARN: mixed-font-headline (Caveat), glass
×3, palette-cream (#f6ecdc), font-count 3, size-count 32, no-poster, side-scroll, empty-middle, blank-gap (724 y 2964px), ragged-edges (12
inicios), pinned-over-picture. **Ojo con las capturas:** desde la 2ª pantalla, todas las hojas (desktop, tablet, móvil) muestran sólo el
isotipo rosa fijado ("un almud: la unidad de medida chilota") bajo la cinta de pills; el escenario `story__stage` fijado + marquee sticky
dominan la captura headless. Parte de `few-pictures`/`empty-screens` es efecto de ese pin, pero que el inspector lo vea así es en sí un
problema real (escena fijada que no sostiene contenido; tramo de 2964px "vacío"). Además v1 tiene preloader, grano fijo, cursor custom y
"peek" que sigue al puntero: los cuatro prohibidos por motion.md §9–10.

---

## 6. Aplicado a Almud: reglas y decisiones para el rediseño

**Inventario (borrador):** el nombre *almud* = la unidad de medida chilota de granos (y su isotipo es un almud de madera); Serrano 325,
Castro; "desde 2014"; abre Mar–Sáb 18:00; el muro rosa de la barra; las cintas de colores de la terraza y bancas verdes; el letrero
retroiluminado ALMUD (blanco) BAR (azul); la carta impresa (nombres en azul #2023e4, precios en magenta
#ec008c, Oswald); el léxico de la casa (GÜERGÜERO, COMILONA, EMPINAR EL CODO, CELEBREICHON, REFRESKEICHON, ÑAM ÑAM, GLUP GLUP,
PICHO CALUGA, MAGANÚO); las historias de Instagram como cuentos con nombres, juegos de palabras y gente; el equipo y los dueños; las
jornadas/noches.

**Decisiones**
1. Sector `restaurant`, `--have photography,video`, `--keep palette,type`, secciones en orden del argumento (no stock). No pasar `--tone
   playful` salvo que queramos forzarlo: el juego sale del copy de la marca, no del tono sorteado.
2. Elegir entre las tres sorteadas contra el inventario. Lectura honesta: **page-is-the-object** encaja mejor con lo que el cliente pidió
   (el carácter vive en las historias de IG ⇒ el artefacto puede ser *la historia/el cuento* o *la carta impresa*); **one-motif** tiene un
   motivo real y propio (el almud: la caja trapezoidal del isotipo como máscara de fotos, botón y bullet; o la medida "un almud" como regla
   de tamaño); **place-carries-it** es la más segura pero también la más de categoría. Recomiendo page-is-the-object o one-motif; aplicar el
   test del competidor ("otro bar de Castro") a la frase-idea.
3. Frase-idea candidata: *"En esta página, cada historia de Instagram de Almud (un cuento con nombres, chistes y gente) se vuelve una pieza
   de su papelería impresa."* o *"…el almud, la medida chilota, se vuelve la forma que enmarca cada foto y cada trago."*
4. **Cosa viva** (una sola, con contenido real): p. ej. "¿qué toca hoy?" que muestra la promo/jornada del día según la fecha (v1 ya tenía
   `promo.is-today`), o un sorteo de un cuento de IG por visita. Debe funcionar con el pulgar y tener fallback sin JS.
5. **Fotos = lo más épico/likeado**: piso 6–12 reales, con 3–5 ubicaciones distintas (split, banda full-bleed, mosaico desigual, foto
   sostenida mientras pasa texto, marco que crece una vez). Ordenar el banco por likes y elegir una familia de luz (noche cálida de barra).
   Dos ratios para ≥75% (4:5 y 16:9).
6. **Hero con footage propio a ≥40% (idealmente full-bleed)**: un reel corto (5–15 s) recortado, muted, loop, con poster; versión retrato
   para teléfono. Nada encima del `h1` salvo scrim neutro.
7. `h1` ≤2 líneas que diga qué es + frase de apoyo de la marca ("Coctelería de autor, comida & música bonita desde 2014" es ideal como
   apoyo, ≤22 palabras). Botón primario real "Ver la carta" en la 1ª pantalla; "Cómo llegar" como link de texto, no segundo botón.
8. **Copy literal de la marca**, pero recortado para encajar: las frases largas de v1 que hoy son "titulares" de 3–7 líneas pasan a `<p>` a
   ≤36px (≤24px móvil, ~25 palabras) o se acortan a ≤32 car. eligiendo un fragmento literal. Hacer la aritmética (Six Caps condensada
   k≈0.40).
9. **Tipografía: dos familias máximo.** Six Caps (display) + Oswald (texto). Big Shoulders sólo si se justifica como la "BAR" del logotipo
   dentro del wordmark (es el logo, no tipografía de página). **Caveat fuera.**
10. **Escala de 5 tamaños** (hoy 32): small 14, body 18, lead 24, head ~56, display por blueprint. Ratio display/body ≥4.
11. **Color con proporciones**: fondo `--noche`, tinta `--papel`, un acento (`--barra` rosa del muro) sólo en la acción + una cosa
    recurrente. Los demás colores de la marca (pisco, cinta, cielo, brasa) sólo como **campos planos por capítulo** (colour by chapter,
    cortes duros) con su tinta propia, nunca como arcoíris en una misma pantalla.
12. Violeta #9b5cff: es de las luces de fiesta, no del logo ⇒ **sacarlo** (falla `palette-purple`). El azul de la carta (#2a2de8) es
    índigo-ish: usarlo sólo sobre papel si es "la carta impresa", y si el inspector lo marca, `--allow palette-purple` justificado por la
    marca. `--papel` #f6ecdc gatilla `palette-cream` (WARN): defendible (posavasos/afiches reales) siempre que no haya terracota; o bajarle
    saturación.
13. Márgenes `clamp(16px,2.2vw,32px)` iguales (v1 usa hasta 64px); 2–3 anclas de texto; secciones a 120–240px; ninguna mitad vacía ("Ya
    saben que no somos ná…" y "Peazo de equipo…" necesitan su foto al otro lado).
14. Esquinas rectas en todas las fotos; botones: decidir cuadrado o píldora una vez.
15. **Motion**: sin loader, sin grano, sin cursor custom, sin "peek" que sigue al puntero, sin `magnetic`. Load sequence ≤1.2 s; una firma
    (la que reparta la dirección); 2–3 escenas hechas a mano sobre `stage.js` con GSAP/ScrollTrigger/Lenis de `vendor/`; ≥16 elementos en
    movimiento; reduced motion = página terminada.
16. La escena del isotipo fijado (v1 `story__stage`) se rehace: máx. 1–4 pantallas, cada pantalla con una línea de texto y algo que mirar,
    nada vacío; o se elimina.
17. Carta completa con precios (archivo de verdad: lista repetida está permitida aquí), sin hairlines entre platos: separar por
    espacio/tono; `tabular-nums` en precios.
18. Nada inventado: reseñas sólo las reales de `content/reviews.json`, con nombre tal cual; ninguna cifra de negocio inventada.
19. Footer como escena: el nombre a todo ancho o "el dorso de la tarjeta", con dirección y horario legibles.
20. Gate antes de entregar: `lint` 0 FAIL, `inspect` 0 FAIL a 3 anchos en `.taste-skill/after`, crítica escrita en el formato §4, tabla
    antes/después.

**Qué condena de v1 (y excepciones honestas)**
- **Flecos de papel entre secciones** (`.fringe`, repeating-linear-gradient): condenados por triple vía (gradient FAIL, "formas
  decorativas", y el cliente dice que se ven baratos). Reemplazo: corte duro de campo de color. Si la marca tuviera flecos reales (los hay
  en la terraza: "naranjo flecos"), mostrarlos **en foto**, no como ornamento CSS.
- **Degradés arcoíris** (`--rib`, `#jornadas` linear-gradient): FAIL. Los colores de la marca van como campos planos por capítulo.
- **Marquee de pills de colores** (lexicon): pills con borde 1px = hairline/outlined; pills multicolor = arcoíris; marquee de texto que hay
  que leer es "fail" en galerías. Excepción defendible: el léxico ES de la marca y es de lo más propio que tiene ⇒ conservarlo como **una**
  "Edge-to-edge marquee" de tipo grande, sin píldoras, un color por campo, lento y pausable, o como muro de palabras (word tiles).
- **Emoji** (18): FAIL. Aunque la marca los usa en IG, en la página se quitan del texto (el copy literal sin emoji sigue siendo literal).
- **Tipografía manuscrita (Caveat)**: tercera familia (WARN font-count), mezcla dentro de titulares (WARN mixed-font), y rotada. Fuera.
  Excepción: si una foto real de un afiche manuscrito suyo lo muestra, que lo muestre la foto.
- **Polaroids y "pins" inclinados** (`.polaroid`, `.pin`, `.pinza`, rotate): imagery.md §6 los nombra explícitamente como no-tratamiento;
  además llevan sombras. Fuera: fotos rectas, esquinas rectas, sin marco.
- **Eyebrows/labels pequeños** sobre headings y el `story__note`/`manifesto__sign` rotados: fuera; la info va en el heading o la primera
  frase.
- **Texto centrado**: v1 centra mucho y el inspector cuenta 12 bordes de inicio; pasar a izquierda con 2–3 anclas, un único momento
  centrado.
- **Sombras, text-shadows, glass, glow** (22 box-shadow, 10 text-shadow, 3 blur): fuera; tono y scrim.
- **Hairlines en la carta** (`border-*:1px`, 20): fuera; espacio.
- **Loader "Almud-cito-ito-ito"**: preloader prohibido y además tapa el hero (covered-text). El juego de palabras es buenísimo y es de la
  marca: rescatarlo como copy en una sección (p. ej. en el masked headline de una escena), no como pantalla de espera.
- **Cursor custom "Arrastrar", peek flotante, botones magnéticos, grano**: prohibidos (motion.md §9–10).
- **Isotipo gigante fijado durante 10+ pantallas**: escena que no contiene nada (empty-screens/blank-gap).
- **Lo que se salva**: la paleta extraída de sus fotos (con disciplina de proporción), Six Caps + Oswald (Oswald es la de su carta), el
  claim "Coctelería de autor, comida & música bonita desde 2014", la promo-del-día como cosa viva, la carta completa, el léxico de la casa,
  el footage del letrero retroiluminado (buen hero o banda), y "un almud: la unidad de medida chilota" como semilla de la idea.
