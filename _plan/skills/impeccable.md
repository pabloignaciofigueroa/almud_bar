# Impeccable (v4.7.0) — notas aplicables al rediseño de Almud Bar

Fuente: `/mnt/user-data/outputs/skills/impeccable/` (SKILL.md + reference/*.md + scripts/). Leído completo: SKILL, routing, craft-floor, craft, new-work, mode-persuade, shape, init, document, critique, audit, polish, animate, delight, layout, typeset, colorize, bolder, quieter, distill, overdrive, adapt, optimize, harden, clarify, visualize y degraded/finish-reviewer. Se omitieron ios/android/*.native y live/live-setup/generate (navegador en vivo).
Las citas van en inglés, tal cual; la explicación en español.

---

## 1. Qué es y cómo se trabaja

**Qué es.** Una skill de dirección de diseño para interfaces. Su ambición declarada: *"design that earns the name out-of-distribution craft. Work as an award-winning design director would"*. Tres principios:
- *"Finish the job. No hedging, no shortcuts."*
- *"Scale ambition to the surface's mode."* Persuade y Experience: *"full commitment: bold, distinct work with a point of view"*.
- *"Verify by looking at the rendered result at the sizes it ships at, and batch the checks."*

**Reglas de diseño que mandan sobre todo lo demás (SKILL.md › How to design):**
- *"The brief wins."* Si el brief fija algo, se respeta aunque choque con un aviso de patrón saturado.
- *"Refinement preserves; redesign replaces."* Un rediseño *"keeps product truth, content, function, native affordances, and constraints, but treats the old look as evidence and anti-reference; choose a replacement world in new-work and replace DESIGN.md. **Never split the difference into polish on the discarded look.**"* → para Almud: no pulir la v1; reemplazar su mundo visual.
- *"Visual authority is evidence, not a filename."* Que no exista DESIGN.md no significa que no haya identidad (logo, Six Caps del logotipo, voz).
- Símbolos cargados fuera de la decoración (no aplica, pero queda dicho).

**Modos (qué es el éxito del visitante).** Persuade (decide y actúa: landings, marketing), Operate (tareas), Read (entender), Experience (está dentro de la obra: portafolios, galerías). Se elige por la superficie, no por el producto. **Almud = Persuade** (el visitante decide venir: dirección, horario, carta, DM), con secciones de historias que se comportan como Experience. En Persuade: *"the opening must make the offer intelligible and desirable, expose a clear action, and demonstrate something only this product can prove. The action is the one the category's visitors came to take, in its working form"* (para un bar: cómo llegar/horario/abrir mapa/escribir al DM visibles y funcionando, no un link decorativo).

**Setup (obligatorio).**
1. Correr `scripts/impeccable context` una vez por sesión (cwd en el proyecto; `--target src/index.html`). Carga PRODUCT.md, DESIGN.md y el surface brief, y da directivas (`NO_PRODUCT_MD`, `CONTEXT_STALE`, `IMAGE_GEN_AVAILABLE`…).
2. Cargar el playbook: el comando pedido o `new-work.md` para una superficie nueva o *replacement visual world*. Inspeccionar la verdad visual actual antes de editar.
3. *"read craft-floor.md immediately before any UI edit, including small refinements"*. No se carga para planificar.

**Qué hace el launcher (`scripts/impeccable`).** Script `sh` que ejecuta un binario autocontenido (sin Node). Busca en orden: `$IMPECCABLE_BIN`, `scripts/bin/<os>-<arch>/impeccable`, `~/.impeccable/bin/impeccable` (validado con `engine-probe`), caché por versión `~/.impeccable/bin/0.1.16/`, `impeccable` en PATH; como último recurso **descarga** `impeccable-linux-x64` desde `github.com/pbakaus/impeccable/releases/download/engine-v0.1.16/`, verifica su `.sha256` (falla cerrado si no puede) y lo cachea. **En nuestra copia no hay carpeta `scripts/bin/`**: sin red/permiso el launcher no corre. El binario provee todos los verbos: `context`, `signals`, `detect` (detector de anti‑patrones sobre HTML/CSS, `--json`, `--scope layout|type`, exit 0 limpio / 2 hallazgos), `concept-seed`, `serve-question` (página de decisión), `surface-brief read|write`, `critique-storage`, `build-phase`, `comp-spec`, `comp-diff`, `font-match` (usa `scripts/data/font-index.json`, 1,1 MB de huellas de Google Fonts), `embed-prompt`, `live-server`, `generate-image`, `pin`, `hooks`, `doctor`. `live-browser*.js` y `modern-screenshot` son el overlay del modo live (no lo usamos).
Reglas del detector que el texto nombra: gradient text, eyebrows/kickers, glass, side-stripe borders, contraste, `organic-clip-path` (clip-path de muchos vértices), `buried-raster` (imagen enterrada bajo un velo o a opacidad ~0), `straggler` y `unbalanced-heading` (cortes de línea, advisorios), paleta plana/gris.

**Si el launcher no corre** (nuestro caso salvo que se autorice la descarga): enviar antes de la siguiente herramienta *"Context loading did not run; I’ll read the existing project context directly."*, leer PRODUCT.md/DESIGN.md existentes sin inventar, y seguir. Lo que se pierde y hay que declarar: `concept-seed` (la tirada), `detect`, `serve-question`, `critique-storage`. En el contrato se escribe `seed: none (unavailable)` y cada sustitución se declara en una línea.

**Orden de comandos para el REDISEÑO de Almud.**
1. `impeccable context --target src/index.html` (o el aviso de fallback).
2. `init` → PRODUCT.md (no existe). Init *no* elige estética: solo verdad de producto.
3. `critique` sobre la v1 en línea (diagnóstico; la v1 es evidencia y anti‑referencia).
4. new-work › **Create or replace the visual world** (pasos 1–5) → dirección elegida → `## Direction contract` en el surface brief. (`shape` solo si queremos el brief sin código.)
5. Leer craft-floor → construir (camino **code-led**: ver §3) → `animate`, `typeset`, `colorize`, `layout` como pasadas *dentro* del mundo elegido.
6. Inspección: máx. dos rondas de capturas (desktop + 390 px), `detect --json`, **finish reviewer** fresco (subagente sin historial) → disposición `ship|fix|rebuild|recapture`.
7. Documenter → DESIGN.md + `.impeccable/design.json`.
8. `audit` → `polish` (último), con `harden`/`optimize`/`adapt`/`clarify` según hallazgos. `bolder`/`quieter`/`distill`/`delight`/`overdrive` solo con objetivo nombrado.

---

## 2. craft-floor.md — piso de calidad y prohibiciones (todas)

Se carga con la dirección ya decidida y se construye sin anunciar la lista. *"A pinned brief or the committed visual world overrides anything here; your own habit does not."*

**Verify (se chequean sobre el render, en una misma ronda):**
1. **Contrast:** texto y placeholder ≥ 4,5:1, texto grande ≥ 3:1. *"On colored surfaces tint secondary text from that hue or the foreground; never gray."*
2. **Depth:** sombras con offset y blur suave. *"A zero-offset colored halo is decoration."*
3. **Spacing:** grupos apretados, separación generosa, *"more space above a heading than below it"*; leer valores computados.
4. **Type:** medida 65–75ch, display máx. 6rem, tracking mínimo −0,04em, titulares balanceados, saltos de escala y peso obvios; correr el copy real en cada quiebre.
5. **Motion:** *"one authored moment, not scattered effects and not one identical entrance on every section. Exponential ease-out from an already-visible default."* Además de transform/opacity: blur, backdrop-filter, clip-path, mask, shadow si van fluidos.
6. **States:** hover, disabled, loading, error, empty + contenido real, controles que funcionan, composición responsive, foco de teclado.
7. **Browser surfaces:** selección de texto, caret, scrollbars, anillos de foco, `text-underline-offset`, numerales tabulares: tematizarlos desde la paleta. *"the cheapest signal that a page was built rather than assembled, and the one models skip most reliably."*
8. **Copy:** el lenguaje del producto; controles que nombran su acción; errores con problema y salida.
9. **Coverage:** cada requisito del brief presente y encontrable en segundos.

**Refuse — andamios de página:**
- Tarjetas iguales de icono + título + texto como estructura. *"Cards are the lazy container; nested cards are always wrong."*
- La plantilla hero‑métrica: número grande, etiqueta chica, stats de apoyo, acento.
- **Kicker/eyebrow sobre un título: prohibición absoluta** (*"no brief earns it back"*).
- Números de sección (01/02/03) salvo que la secuencia informe.
- Un modal para algo que no necesita interrupción ni foco protegido.

**Refuse — hábitos de superficie:**
- Texto con degradado (el énfasis va por peso o tamaño).
- Vidrio y blur como decoración.
- `border-left/right` de color > 1px en tarjetas, ítems, callouts, alertas.
- Sombras duras desplazadas (`4px 4px 0`) fuera de un mundo realmente neobrutalista.
- Sparklines, anillos de progreso y rectángulos redondeados con sombra suave en lugar de contenido.
- Monoespaciada como disfraz "técnico".
- Fuente de sistema (Impact, Arial Black, la sans de plataforma) como voz display; *"the closest installed font is a failure, not a fallback"* → autoalojar una fuente con el carácter correcto.
- Glifos Unicode o emoji en lugar de un sistema de iconos (iconos dibujados, de una librería o SVG propio, mismo trazo y peso).
- Máscaras geométricas imitando contornos orgánicos (círculo/polígono/radial que recorta a una persona): derivar un matte alfa real o un recorte.
- Claro u oscuro elegido por categoría: elegir por la escena de uso (quién, dónde, con qué luz).

Cierre: *"The floor holds the mechanics; it never picks the direction… when torn between refined and committed, commit."*

**Prohibiciones adicionales repartidas en otras referencias:**
- Fuentes "por defecto de entrenamiento" vetadas para Persuade salvo razón que ninguna otra cumpla: *Fraunces, Playfair Display, Cormorant, Lora, Crimson, Newsreader, Syne, Space Grotesk, Space Mono, IBM Plex, Inter-as-display, DM Sans, DM Serif, Outfit, Plus Jakarta Sans, Instrument Sans.* (Asociación temática nunca es razón: *"bookshops wanting hand-lettering"* está en la lista de asociaciones a romper.)
- Los cuatro looks‑IA a evitar si el brief no los pide: crema cálido + serif display de alto contraste + acento terracota/rojo; casi‑negro con un acento neón y bordes brillantes; editorial de hairlines + serif itálica + mono chica espaciada; tinta plana saturada con cajas negras, sombras desplazadas y display condensada pesada. Autotest: *"if someone could guess your aesthetic from the category alone… rework"*.
- *"Gradients, glass, generic icon tiles, and many-vertex clip-path polygons where an authored asset belongs are the gap wearing chrome."*
- Finish reviewer: *"faked physicality (CSS bevels, embossing, stamped-metal or chalk effects imitating a material the page never renders)… imitation material is the single most reliable mark of machine-made design."*
- animate: sin bounce/elastic por reflejo; quieter: *"Never bounce or elastic"*.
- delight: *"Never fake work or delay completion to stage a flourish."*
- overdrive: no apilar momentos extraordinarios que compiten.

---

## 3. new-work.md — elegir y comprometerse con un mundo

**Artefactos y quién es dueño de qué:** PRODUCT.md = verdad de producto (init). DESIGN.md = decisiones visuales durables (se escribe **al final**, desde lo construido, por el documenter). Surface brief = estrategia de esta ruta + `## Direction contract`.

**Paso 1 · Qué ya es verdad.** Rediseño: *"preserve product truth, content, function, constraints, and explicit brand commitments; replace the old visual world rather than polishing it."* (Para Almud: logo/isotipo, nombre, voz literal, carta, datos de contacto, fotos reales.)

**Paso 2 · Preguntar lo que cambia el trabajo** (2–3 preguntas con herramienta estructurada). Persuade: *who must act, what they should believe, which real proof, content, or assets earn that belief*; además, qué es éxito, qué no se toca y *"what would make a polished result feel wrong"*. Nunca preguntar valores CSS ni "carriles estéticos".

**Paso 3 · Crear o reemplazar el mundo (nuestro caso):**
1. Nombrar en una frase el **mecanismo único**, la **escena real** del público, su **hogar cultural** y lo que esta primera superficie debe probar. Anotar *la página que la categoría siempre hace y su opuesto predecible* (ambos son "el surco", fuera de la lista). Si el brief trae una metáfora literal (p. ej. "almud" = cajón de medida), gastar como máximo un candidato en ella.
2. Listar **siete** sistemas visuales, artefactos, lugares o rituales que el público conoce de memoria, ordenados por resonancia, cada uno con una línea de por qué resuena y otra de cómo se ve (fondo y colores, voces tipográficas, una firma reconocible). Incluir tradiciones gráficas y de pantalla (publicaciones, señalética, programas de identidad). Preguntar *cómo sería como objeto físico* y *cómo se veía su mundo antes de la web*. Casi‑duplicados cuentan una vez; si >3 de 7 comparten familia material, seguir cavando hasta cubrir ≥ 3 familias. En Persuade, las herramientas del público (aquí: coctelera, carta, posavasos) cuentan para el surco: máximo uno.
3. Convertir en direcciones completas (mundo reutilizable + experiencia concreta de primer viewport).
4. Correr `impeccable concept-seed --scope direction --mode persuade` (*"No substitute, no skip"*). Asigna la dirección y reparte retadores del catálogo; se "fusionan" y se pesan en **dos ejes: identificación del público y claridad del producto** → veredicto *wins / competitive / declined*; de cada declinado se toma una **disciplina** (no su ropa) y se escribe como línea "raise".
5. Presentar **una** dirección totalmente comprometida: *world, first viewport, visitor path, signature interaction, cross-surface reach, honest risk*; más alternativas, una carta "IMPECCABLE’S PICK" si aplica, re‑roll (plain/safer/bolder) y la salida estándar (canon) que es la puerta del usuario, nunca recomendación nuestra.
Todas las direcciones deben ser viables y veraces: *"What stays uninventable are commercial and factual claims."* (Encaja con nuestro método ghostwriter.)

**Paso 4 · Comprometer el mundo.**
- Estrategia de color antes que colores: **Restrained** (neutros teñidos + 1 acento), **Committed** (un color saturado cubre 30–60 %), **Full palette** (3–4 roles con nombre), **Drenched** (la superficie ES el color). Persuade tiene permiso para las audaces. *"Color commits at page scale: fields that own whole regions, not accents scattered over a neutral ground."*
- Claro/oscuro: escribir **una frase de escena física** (quién, dónde, qué luz) y que decida.
- Fuentes *"like objects from the subject's world"*, con punto de vista; fuera la lista de defaults.
- Prior propio a desconfiar: temas cálidos/familiares salen crema + serif + luz de lámpara: *"Treat that first palette as already spent."*

**Paso 5 · Registrar la decisión** antes del código, en el surface brief (`surface-brief write`), bajo `## Direction contract`, ~150 palabras, seis bloques. Plantilla para llenar:

```markdown
## Direction contract
THESIS: <la única idea que esta superficie posee y el arreglo por defecto de la categoría que rechaza>
OWN-WORLD: <paleta y lenguaje de componentes, reconocible sin contenido>
STORY: <qué entiende, cree y hace el visitante>
FIRST VIEWPORT: <composición exacta: qué va dónde, a qué escala, dónde está la acción principal>
FORM: <forma elegida, su lugar en la lista ordenada, seed: <16 hex> | seed: none (unavailable)>
FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance
```
Resto del brief, pequeño: *scope and visitor mode; audience, job, action/task, proof/content, and constraints; chosen direction and memorable moment; unresolved decisions.* **Nunca** copiar el contrato en el código, comentarios HTML, `data-*`, JSON‑LD ni nada servido. *"If a block reads like a mood, the direction is not decided yet."*

**PRODUCT.md (init) — plantilla con sus encabezados:**
```markdown
# Product
<!-- impeccable:product-schema 1 -->
## Platform            (web)
## Stack               (solo greenfield: "static HTML/CSS + GSAP + Lenis, publish desde public/")
## Users
## Product Purpose
## Positioning
## Operating Context
## Capabilities and Constraints
## Brand Commitments
## Evidence on Hand    (rutas reales: content/ig_posts.json, reviews.json, carta.json, assets/…; ausencias que no se pueden fabricar)
## Product Principles  (3–5, sin recetas visuales)
## Accessibility & Inclusion
```
Init no admite estética, modo, narrativa ni CTA (eso va al surface brief). `buildPath` se guarda en `.impeccable/config.json`, no en PRODUCT.md.

**DESIGN.md (document, al final) — frontmatter YAML con solo `colors`, `typography`, `rounded`, `spacing`, `components` (refs `{colors.x}`; componentes con ≤ 8 props: backgroundColor, textColor, typography, rounded, padding, size, height, width) y ocho secciones en este orden exacto, sin renombrar:**
```markdown
# Design System: Almud Bar
## Overview          (**Creative North Star: "…"** + 2–3 párrafos + **Key Characteristics:**)
## Colors            (### Primary / ### Secondary / ### Tertiary / ### Neutral / ### Named Rules)
## Typography        (**Display Font:** … **Body Font:** … **Character:** … ### Hierarchy: Display/Headline/Title/Body/Label)
## Layout
## Elevation & Depth (### Shadow Vocabulary)
## Shapes
## Components        (### Buttons / ### Chips / ### Cards / Containers / ### Inputs / Fields / ### Navigation / ### [Signature Component])
## Do's and Don'ts   (### Do: / ### Don't:)
```
Sidecar `.impeccable/design.json` (schemaVersion 2): `colorMeta` con rampas tonales de 8 pasos, `shadows`, `motion`, `breakpoints`, 5–10 componentes con HTML/CSS autocontenido prefijado `ds-`, y `narrative` (northStar, rules, dos, donts). Reglas con nombre: *"**The [Name] Rule.** [doctrine]"*, 1–3 por sección.

**Construcción (§6) y camino.** Persuade toma por defecto **comp-led** si hay generación de imágenes: tres comps, spec medido, *plates* generadas desde los recortes del comp, gate del hero al 72 %. **Para Almud corresponde code-led**: nuestras imágenes deben ser fotos reales, y en comp-led *"Every raster region ships as a plate… regenerated at asset resolution"*, lo que contradice la regla del método. En code-led *"the ambition lives in the direction contract's FIRST VIEWPORT block and the named signature interaction"* y el finish reviewer lo audita en comportamiento. (Se puede usar un comp solo como referencia de crítica, nunca como pixel enviado.) Reglas de ambos caminos:
- *"The first viewport is a thesis, not a header."* Test de memoria: qué describiría alguien una hora después de ver un solo viewport; si es "un ambiente", no hay concepto.
- *"Prove, don't claim."* *"Author the assets; never substitute chrome."*
- *"Pace the scroll like a studio. Vary density, scale, image, motion, and quiet inside one grammar… the page ends anchored by a real close."*
- *"Use real, verified imagery… one decisive photo beats five mediocre ones."*
- *"Commit every atom: nav, buttons, inputs, and links are rebuilt in the form's vocabulary, and a stock component inside a committed form is a lapse."*
- Mode‑persuade: el mundo es *el soporte* de la página, no un póster pintado; y tampoco *"a headline over subcopy and a button, a row of equal cards below"*. Un solo movimiento dominante; el resto quieto en el material del mundo.

**§7 Inspección y cierre:** una ronda de capturas (desktop + móvil + el ancho real del usuario), con todos los estados; dos rondas como techo. Capturas válidas: animaciones de entrada asentadas, desde el tope, sin zonas negras. `detect --json` una vez. Finish reviewer fresco con: pedido original, respuestas, ruta del artefacto, capturas, contrato, hallazgos, QUALITY BAR, comp de referencia, craft-floor. Revisa en orden: 0 evidencia, 1 persistencia, 2 fidelidad (filas obligatorias **TYPE, MATERIAL, GROUND**), 3 techo, 4 contrato bloque a bloque, 5 verdad, 6 piso. Devuelve una sola palabra de disposición y ≤ 8 *material_fixes*; máximo dos rondas de fix. Luego documenter.

---

## 4. critique.md — método y rúbrica

**Invariantes:** dos evaluaciones aisladas en subagentes paralelos: **A (revisión de diseño, sin ver al detector)** y **B (detector `impeccable detect --json` + navegador con overlay)**. Si se hacen en un solo contexto, la primera línea del informe debe ser `⚠️ DEGRADED: single-context (<reason>)`. Saltarse el detector = crítica fallida (salvo que el binario no exista o se caiga tras intentarlo). La pregunta al usuario es lo último del mensaje; sin preguntas ni línea `Questions skipped: <reason>` la corrida está incompleta.

**A evalúa:** especificidad del diseño (¿podría usarlo un producto ajeno sin cambios?) antes de ver el detector; diseño holístico; carga cognitiva; viaje emocional (regla pico‑final, valles, tranquilidad en momentos de alto riesgo); 10 heurísticas de Nielsen.

**Escala 0–4 por heurística** (4 = realmente excelente; *"Most real interfaces score 20-32 out of 40"*):
| # | Heurística | 0 | 2 | 4 |
|---|---|---|---|---|
| 1 | Visibilidad del estado | sin feedback | parcial, huecos grandes | toda acción confirma |
| 2 | Coincidencia con el mundo real | jerga pura | mezcla | habla su idioma |
| 3 | Control y libertad | atrapado | salidas solo en flujo principal | undo/cancel/back/esc en todo |
| 4 | Consistencia y estándares | parece varios productos | flujos principales coinciden | sistema cohesivo |
| 5 | Prevención de errores | sin barandas | errores comunes atrapados | casi imposibles |
| 6 | Reconocer antes que recordar | memorización | acciones principales visibles | todo descubrible |
| 7 | Flexibilidad y eficiencia | un camino rígido | atajos básicos | múltiples caminos |
| 8 | Estética y minimalismo | todo compite | periferia ruidosa | cada elemento se gana su pixel |
| 9 | Recuperarse de errores | crípticos | nombra el problema, no la salida | señala, sugiere, preserva |
| 10 | Ayuda y documentación | nada | FAQ no contextual | ayuda justo a tiempo |
(1 y 3 son los intermedios: 1 = casi sin/confuso; 3 = bueno con huecos menores.)
**En Persuade/Experience, 7 y 10 pueden ir `n/a`** con una línea de razón; el total se renormaliza (p. ej. /32). Bandas: 36–40 Excellent · 28–35 Good · 20–27 Acceptable · 12–19 Poor · 0–11 Critical; con n/a por porcentaje: ≥90 % / ≥70 % / ≥50 % / ≥30 % / menos.

**Carga cognitiva (8 ítems; fallas: 0–1 baja, 2–3 moderada, ≥4 crítica):** single focus; chunking (≤ 4 por grupo); grouping; visual hierarchy; one thing at a time; minimal choices (≤ 4 opciones visibles por decisión); working memory; progressive disclosure. Regla de memoria: ≤ 4 ítems ok, 5–7 al límite, 8+ sobrecarga (nav ≤ 5 ítems).

**Severidad:** P0 bloqueante (impide la tarea) · P1 mayor (dificultad seria; *"Would a user contact support about this?"* → al menos P1) · P2 menor · P3 pulido.

**Informe (orden):** línea de método → tabla de heurísticas → *Design Specificity Verdict* (LLM + escaneo determinista + overlays) → impresión general → 2–3 cosas que funcionan → 3–5 Priority Issues `[P?] What / Why it matters / Fix / Suggested command` → Persona red flags (landing: **Jordan** primerizo, **Riley** tester de bordes, **Casey** móvil con una mano; más 1–2 personas propias si hay contexto: p. ej. turista extranjero en Castro, local de Chiloé) → observaciones menores → preguntas provocadoras → snapshot en `.impeccable/critique/` + línea de tendencia → 2–4 preguntas con opciones concretas ligadas a hallazgos (prioridad, intención tonal, alcance, restricciones). Tras la respuesta: lista de comandos priorizada terminando en `/impeccable polish`. *"Don't soften criticism."*

---

## 5. audit.md y polish.md

**audit** (técnico, no estético; documenta, no arregla). Cinco dimensiones 0–4, total /20 (18–20 Excellent · 14–17 Good · 10–13 Acceptable · 6–9 Poor · 0–5 Critical):
- [ ] **Accesibilidad:** contraste < 4,5:1; `prefers-reduced-motion` con alternativa intencional (se marca un `0.01ms` global que mata feedback útil, flashes, movimiento que bloquea lectura/foco); ARIA faltante; foco visible, orden de tab, trampas; HTML semántico (jerarquía de títulos, landmarks, botones reales); alt; formularios.
- [ ] **Rendimiento:** layout thrashing; animaciones caras (propiedades de layout, blur/filter/shadow sin acotar); imágenes sin lazy/sin optimizar; `will-change` en exceso o permanente; bundle; renders.
- [ ] **Theming:** colores hardcodeados fuera de tokens; dark mode roto; tokens inconsistentes.
- [ ] **Responsive:** anchos fijos; targets < 44×44 px; **gestos táctiles rotos** en sliders/arrastres/tiras con scroll (handlers solo mouse, sin `touch-action`, estado de arrastre que no se limpia en cancel/blur) — decir con qué evidencia se probó; scroll horizontal; zoom de texto; breakpoints faltantes.
- [ ] **Integridad de implementación (CRÍTICA):** detector + verificación en contexto; atajos repetidos, deriva del sistema, contenido decorativo o engañoso, estructura intercambiable con otro producto.
Informe: tabla → *Implementation Integrity Verdict* (pass/fail) → resumen ejecutivo con conteo P0–P3 → hallazgos con ubicación, categoría, impacto, norma WCAG, recomendación, comando → patrones sistémicos → hallazgos positivos → acciones (terminar en polish). *"Keep P3s few."*

**polish** (refinamiento, *"never concealed redesign"*; si el concepto está mal, decirlo y recomendar rediseño o `bolder`).
1. Establecer el sistema; clasificar cada deriva: *missing token / one-off implementation / conceptual mismatch / local defect*; arreglar al nivel más estrecho correcto.
2. Evidencia: usar la página en desktop y móvil; leer el último snapshot de critique (`critique-storage latest`).
3. Triage en orden: (1) tareas rotas, pérdida de datos, estado engañoso, rutas inaccesibles; (2) estados faltantes loading/empty/error/success/disabled; (3) flujo, jerarquía, responsive, deriva del sistema; (4) inconsistencias visuales y de movimiento; (5) limpieza de código y assets.
4. Pulir el camino completo:
   - [ ] Flujo y jerarquía: tarea principal y estado actual obvios sin aplanar todo.
   - [ ] Layout y tipo: grilla y escala de espaciado; alineación óptica además de matemática; mismo rol = misma tipografía; medida, cortes, carga de fuentes; todos los viewports.
   - [ ] Color, imagen, iconos: tokens semánticos; contraste en todos los estados; familia de iconos coherente; sin CLS de imágenes, aspect‑ratio correcto, `srcset`, alt útil.
   - [ ] Interacción y estado: default/hover/focus/active/disabled/loading/error/success; foco visible; targets; movimiento coherente e interrumpible, *"Do not add animation merely to make polish visible."*
   - [ ] Contenido y código: terminología y puntuación consistentes (preguntar antes de cambiar afirmaciones); sacar debug, código muerto, estilos obsoletos.
5. Verificar: mouse, teclado, touch; móvil/intermedio/ancho; estados largos/vacíos; zoom; consola; CLS; latencia. Cerrar con diff limpio. Cerrar el snapshot de critique solo si se resolvieron todos sus Priority Issues.

---

## 6. Movimiento, tipo, color, layout y "más/menos"

**animate.** Persuade: *"motion may carry the voice. Prefer one rehearsed focal sequence to repeated section reveals."* Antes de implementar, una tesis: **Focal moment** (de este producto; *"A generic fade-and-rise, hover lift, parallax layer, or scroll reveal is not a thesis"*), **Continuity**, **Feedback**, **Budget**. Elegir material por significado: continuidad (FLIP, view transitions), foco (blur acotado, luz, sombra), revelado (máscaras, clip-path, recorte), energía (color, textura, shader). Stagger solo si algo aparece como lista, con tope total. Duraciones: 100–150 ms feedback · 150–300 estado · 300–500 layout/overlay · 500–800 entrada focal; salida más rápida que entrada; `cubic-bezier(0.16, 1, 0.3, 1)`; sin bounce/elastic por reflejo. Contenido visible por defecto si falla el script; no animar width/height/top/left/margins; `will-change` solo durante la animación; loops no esenciales se detienen fuera de pantalla. `prefers-reduced-motion`: menos movimiento espacial, conservando opacidad/color/estado. Test final: *"Removing an animation would lose meaning or authored character, not merely decoration."*

**typeset.** Persuade: *"display type may carry the voice."* Roles mínimos y familias mínimas; jerarquía por tamaño + peso + espacio + tono. Body ≥ 16 px, prosa 45–75ch, leading inverso a la medida; texto claro sobre oscuro: algo más de interlineado, tracking y un paso de peso. Cargar solo pesos usados, fallback con métricas compatibles. `text-wrap: balance` en titulares, `pretty` en cuerpo; cortes a mano solo entre frases y verificados en cada ancho. No introducir una segunda familia sin un rol que solo ella cumpla. Con el binario, `font-match` elige por huella de la letra real (útil para emparejar el lettering del logo o de sus pizarras).

**colorize.** Roles, no bolsa de muestras: canvas/superficies, texto 1º/2º, acción/foco/selección, bordes, semánticos. OKLCH; tono desde el significado del producto, no por asociación de categoría. *"Let the strongest color own a deliberate region or role instead of scattering tiny accents."* *"Keep the primary action easy to find; do not spend its color on decoration."* Texto secundario sobre color derivado del matiz, nunca gris. Contrastes: cuerpo 4,5:1, grande 3:1, controles/iconos/foco 3:1; color nunca como único código. *"Decoration without a relationship to hierarchy, state, content, or the visual world is not a color strategy."*

**layout.** Persuade: composición asimétrica o disruptiva si el mundo la gana. Preguntas: squint test (primario, secundario, grupos en orden), agrupación por proximidad antes que contenedores, ritmo de intervalos apretados vs generosos, topología según contenido (¿las tarjetas repetidas son de verdad equivalentes?), densidad, adaptación (orden DOM = orden visual), extremos. Escala de espaciado de base 4; `gap` para hermanos; profundidad solo si aclara jerarquía. *"Variation is not a goal by itself."*

**delight.** *"Delight is not a layer of generic whimsy; it is product character revealed through a useful interaction, a humane response, or an unexpectedly considered detail."* Una tesis en una frase (qué siente el visitante y por qué es de este producto). *"Copy must use the product's language. Generic whimsy is worse than neutral clarity."* No debe demorar la tarea, ni sonar sin consentimiento, ni volverse agotador al repetirse. Test: *"specific enough that a neighboring product could not use it unchanged."*

**bolder.** Con un mundo ya enviado, sube **una** sección al nivel que el sistema ya implica: *"The reflex answer, reaching for more effects, is the opposite of bold"*; *"If every element got louder, the section got flatter."* Test del esqueleto: sin el texto, ¿la estructura sola dice qué es la sección? (Ojo: "bolder/safer" dicho durante la ronda de dirección = registro del re‑roll, no este comando.)

**quieter.** Persuade: paleta más contenida, más aire, drama reducido no eliminado. *"Generic quiet looks like gray text on white, one sans at a uniform weight, and a grid of identical cards."* Quitar decoración sin propósito (degradados, sombras, patrones, texturas), glows, blur; movimiento a 10–20 px, ease‑out‑quart.

**distill.** Un objetivo principal; una acción obvia; 1–2 colores + neutros, 3–4 tamaños, 2–3 pesos; sin tarjetas para maquetar; copy a la mitad y otra vez a la mitad; *"say it once"*.

**overdrive.** Proponer 2–3 direcciones y pedir elección antes de codificar; mejora progresiva obligatoria (`@supports`, fallback CSS que se vea bien); 60 fps, pausar lo que no se ve; *"Layer multiple competing extraordinary moments"* está prohibido. Tests: wow, remoción, dispositivo, contexto. Candidatos sensatos aquí: scroll‑driven con fallback, view transitions, `@property`, video bien recortado; no partículas ni WebGL decorativo.

**adapt / harden / optimize / clarify (breve):** mobile‑first con `min-width`; breakpoints por contenido; `pointer`/`hover` en vez de tamaño; `env(safe-area-inset-*)` + `viewport-fit=cover`; `srcset`/`picture` con dirección de arte; nunca depender de hover. Harden: textos largos (nombres de tragos), cambio ES/EN (+30–40 % de largo), `min-width:0` en flex/grid, sin JS el contenido sigue. Optimize: LCP < 2,5 s, INP < 200 ms, CLS < 0,1; AVIF/WebP, dimensiones y `aspect-ratio`, no lazy en lo de arriba, `font-display: swap`, subset, precargar la fuente crítica. Clarify: verbo + objeto en acciones, enlaces con sentido fuera de contexto, alt que transmite información.

---

## 7. Aplicado a Almud

**Decisiones y reglas que la skill implica para la v2**
1. **Es un rediseño, no un polish**: la v1 queda como evidencia y anti‑referencia; se elige un mundo nuevo y se escribe DESIGN.md nuevo al final. Nada de "v1 limpiada".
2. **Modo Persuade** en el surface brief; la acción del visitante en forma funcional y visible desde el primer viewport: horario de hoy, Serrano 325 con "Abrir en Google Maps", DM y carta.
3. **Se conserva** (verdad y compromisos de marca): logo/isotipo/logotipo y su letra Six Caps, textos literales de IG con su ortografía ("usté", "colorssss"), carta y precios, reseñas con fuente, fotos y videos reales, créditos.
4. **Derivación del mundo desde las historias**, no desde "bar de cócteles": los siete candidatos salen del mundo cultural de Almud (Castro y Chiloé, la noche en Serrano, sus cuentos de IG con nombres y juegos de palabras, sus fiestas: Jalogüín, fonda, aniversarios, Teik Agüei, Ojo Piojo). "Circo" y "papel picado/fiesta" son el surco de la v1: como máximo un candidato. El almud como metáfora literal: máximo uno. ≥ 3 familias materiales.
5. **Correr concept-seed** si se autoriza la descarga del binario (verificada por sha256); si no, declarar `seed: none (unavailable)` y la sustitución en una línea.
6. **Camino code-led** (fotos reales, nada de *plates* generadas). Si se generan comps, solo como referencia de crítica y nunca se publican.
7. **Primer viewport = tesis**: una foto o video épico del jurado (ranking por likes + calidad + fuerza narrativa) a la escala que tiene en la vida, con un titular literal; nunca "headline + subcopy + dos botones pill" ni *split hero*.
8. **Una sola historia por capítulo, una foto decisiva**: *"one decisive photo beats five mediocre ones"*. Los cuentos (nombre + juego de palabras + gente) son la estructura; ritmo de estudio: denso, quieto, denso; cierre real.
9. **Claro/oscuro por escena**, por escrito: p. ej. "turista o local mirando el teléfono en Castro, de tarde o de noche, decidiendo dónde ir". No asumir oscuro por ser bar.
10. **Color desde las fotos ganadoras**, con estrategia explícita (Committed o Drenched por capítulo es coherente con "colorido"), regiones enteras y roles con nombre; nada de rotar seis colores por ítem.
11. **Tipografía**: Six Caps como voz display (viene del logotipo: es compromiso de marca, no default). Cuerpo ≥ 16 px y medida ≤ 75ch; revisar si Oswald condensada sirve para leer párrafos en ES/EN o si el cuerpo pide otra familia con rol propio. Nada de la lista de fuentes vetadas.
12. **Un momento autoral de movimiento** (candidato honesto: "el almud se abre" de la v1, ya que su rombo sale de la geometría real del isotipo y no imita un contorno fotográfico; se decide en la ronda de dirección, no por apego). Todo lo demás: feedback y continuidad, sin entradas idénticas por sección.
13. **Tematizar las superficies del navegador**: `::selection`, `caret-color`, anillos de foco, scrollbars visibles y con color en carruseles, `text-underline-offset`, numerales tabulares en precios y horario. La v1 no tiene ninguno y oculta scrollbars.
14. **Iconos dibujados** (SVG propio o una librería, un trazo); nada de ★, ←, →, 😘 como iconos.
15. **Cero kickers/eyebrows y cero números de sección**; el titular literal carga solo.
16. **Componentes reconstruidos en el vocabulario del mundo** (botones, pestañas de carta, menú, selector ES/EN); un pill genérico dentro de un mundo comprometido es "a lapse".
17. **Reseñas sin plantilla hero‑métrica**: si el 4,6 / 848 reseñas aparece, que sea dentro de una historia o como prueba integrada, no número gigante + etiqueta + estrellas.
18. **Prueba > afirmación**: los nombres de los tragos, la gente del equipo con sus @ y sus frases, las fotos de las fiestas son la demostración; ningún adjetivo propio.
19. **Reducción de movimiento intencional** (sin sticky animado, sin autoplay, todo visible) y **sin JS** el contenido completo.
20. **Cierre obligatorio**: dos rondas de capturas (390 / 768 / 1280–1600 / 1920), `detect`, finish reviewer fresco con contrato y capturas, documenter → DESIGN.md + `.impeccable/design.json`, luego audit → polish. *"unreviewed and undocumented is unfinished"*.
21. **Crítica de la v1** con rúbrica completa (heurísticas 7 y 10 `n/a` → /32), personas Jordan, Riley, Casey + "turista extranjero" y "local de Castro", y banner de modo degradado si no hay subagentes o detector.

**Veredicto honesto sobre los elementos de la v1**
| Elemento v1 | Veredicto | Por qué (regla de la skill) |
|---|---|---|
| Flecos de papel picado entre secciones (`.fringe`: `repeating-linear-gradient` + `mask`, se mecen con la velocidad) | **Condenado** | Imitación de material en CSS (*faked physicality*, "the single most reliable mark of machine-made design"); degradados donde debía ir un asset; decoración repetida entre secciones, no un movimiento dominante. Coincide con el "se ve barato" del cliente. Si hay papel picado real en el bar, que aparezca en sus fotos. |
| Cinta arcoíris `--rib` (6 franjas) en barras de progreso | **Condenado** | Color esparcido como acento sin rol; *"Decoration without a relationship to hierarchy… is not a color strategy"*. |
| Marquee de "palabras de la casa" en chips pill de colores rotativos | **Condenado como dispositivo** | Cinta de ticker = andamio de categoría; pills de contorno redondeado haciendo de contenido; color ciclado por `nth-child`; efecto suelto. Las palabras (literales) pueden volver *dentro* de sus cuentos. |
| Emoji (😘 gigante en el pie, 👌🏼 en titulares) y glifos ★ ← → | **Condenados como iconos/ornamento**; **tolerados dentro de citas literales** a tamaño de texto | *"Unicode glyphs or emoji standing in for an icon system"*. El método ghostwriter manda conservarlos en el copy citado, no ampliarlos como decoración. |
| Fuente manuscrita Caveat (notas rotadas, firmas, pies de polaroid) | **Condenada** | Disfraz de "cercanía" con una manuscrita genérica de Google; la skill rompe explícitamente la asociación "hand-lettering"; rotaciones esparcidas. Solo volvería si se empareja (font-match) con lettering real de su material (pizarras, afiches propios). |
| Polaroids colgadas con pinzas dibujadas en CSS (`.polaroid`, `.pinza`, cordel) | **Condenadas en su ejecución** | Pinzas y cordel son material falso en CSS; polaroid = cliché; rotaciones aleatorias. La pinza tiene raíz real (su foto de perfil): si el mundo la elige, debe ser una pinza fotografiada recortada con alfa, una sola vez. |
| Tablero de afiches con alfileres CSS (`.pin::before`) | **Condenado** | Igual que arriba: material imitado + rotaciones. |
| Pastillas de vidrio (`backdrop-filter: blur`) en menú, idioma y sonido | **Condenadas** | *"Glass and blur as decoration"*. |
| Grano de película animado a pantalla completa (loop infinito) | **Quitar o justificar** | Textura decorativa sin rol; loop no esencial que no se detiene; costo de pintura. |
| Cargador "Almud·cito·ito·ito" | **Condenado como bloqueo** | Demora el contenido para un floreo (*"never… delay completion to stage a flourish"*). El juego de palabras puede vivir en otra parte. |
| Botones magnéticos, cursor "Arrastrar", imagen *peek* al pasar | **Condenados como set** | *"scattered effects"*; hover no existe en touch; compiten con el momento autoral. |
| Botones/pestañas pill con relleno que sube | **Reemplazar** | Componente de stock; debe reconstruirse en el vocabulario del mundo nuevo. |
| Reseñas "4,6 ★★★★★ + 848 reseñas…" como titular | **Condenado** | Plantilla hero‑métrica + glifos. |
| Seis colores asignados por rotación a rincones, platos y tarjetas | **Condenado** | Bolsa de muestras, no roles; color que no posee regiones. |
| "El almud se abre" (rombo del isotipo → ventana al video) | **Sobrevive como candidato** | Es específico de la marca y es un solo momento autoral; la máscara deriva del logo, no imita un contorno orgánico. Debe pasar la ronda de dirección y el test de remoción. |
| Titulares = citas literales de IG en Six Caps | **Se conserva** | Copy en el idioma del producto; voz display con origen en el logotipo. |
| Degradado oscuro sobre el video del hero | **Se conserva si es funcional** | Sirve al contraste; no es decoración (verificar que no entierre la imagen: regla `buried-raster`). |
| Scrollbars ocultas en carruseles, sin `::selection` ni caret propios | **Defecto de piso** | *Browser surfaces*; además dificulta descubrir el scroll horizontal (Casey, Jordan). |
