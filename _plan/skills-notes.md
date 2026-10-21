# Almud v2 · Reglas de las skills (fase 1)

Notas completas por skill: `_plan/skills/impeccable.md` (294 l.), `_plan/skills/taste.md` (446 l.), `_plan/skills/emil.md` (258 l.).
Este archivo es la síntesis: lo que manda en la v2 y cómo se resuelven los choques entre las tres skills y el método ghostwriter.

## 0. Postura
- **Es un rediseño, no un pulido.** La v1 es evidencia y anti-referencia (Impeccable: *"never split the difference into polish on the discarded look"*).
- **Se conserva lo que es verdad de la marca:**
  - logotipo e isotipo, y Six Caps, que viene de su letrero;
  - Oswald, que es la letra de su carta;
  - los textos literales de IG con su ortografía;
  - la carta con sus precios;
  - las reseñas con su fuente;
  - fotos y videos reales;
  - los créditos.
- **Modo Persuade** (Impeccable). Desde el primer viewport tienen que estar a mano el horario, Serrano 325 con el mapa, la carta y el DM.
- **Camino code-led.** Nada de imágenes generadas: solo su material.

## 1. Proceso (orden de trabajo de las fases 2–20)
1. **Fase 2 · Diagnóstico.**
   - Crítica Impeccable de la v1: las heurísticas de Nielsen, de 0 a 4. La 7 y la 10 quedan n/a, así que el total es sobre 32. Personas: turista extranjero, local de Castro, Jordan, Riley y Casey.
   - Lint e inspect de Taste: ya corridos.
   - review-animations de Emil: ya hecho. Veredicto **Block**.
2. **Fases 5–7 · Jurado y dirección.**
   - PRODUCT.md con las plantillas de `impeccable.md` §3.
   - new-work: 7 candidatos de mundo, todos salidos de la cultura de Almud y no de "bar de cócteles". Máximo un candidato de "circo/fiesta" y uno de "el almud literal".
   - Sorteo de dirección de Taste y la frase-idea *"En esta página, [X] se vuelve [dispositivo]"*.
   - El contrato de dirección en 6 bloques: THESIS, OWN-WORLD, STORY, FIRST VIEWPORT, FORM y FINISH.
3. **Fase 8.** DESIGN.md (YAML y 8 secciones) más `.impeccable/design.json`.
4. **Fases 15–17 · Compuerta de cierre.**
   - `lint` y `inspect` de Taste con 0 FAIL a 390, 768 y 1440, guardados en `.taste-skill/after`.
   - Crítica escrita en el formato §4 de Taste.
   - Dos rondas de capturas de Impeccable, un *finish reviewer* nuevo, audit y polish.
   - review-animations de Emil con su tabla Before/After/Why y el modo "peor caso" de break-ui (EN, nombres largos, 320 px).

**Comandos que funcionan aquí** (desde `almud_bar/`):
```
S=/mnt/user-data/outputs/skills/taste/scripts
node $S/draw.mjs --sector restaurant --brief "…" --have photography,video --keep palette,type --options 3
CHROME_PATH=_plan/skills/chrome-nosandbox.sh node $S/inspect.mjs index.html --out .taste-skill/after
node $S/lint.mjs index.html
```

**Limitaciones:**
- `assets.mjs` (openverse) está bloqueado por el proxy. No importa: solo usamos su material.
- El motor de Impeccable (concept-seed, detect) es un binario que se descarga de GitHub releases. No lo ejecuto sin tu permiso. Mientras tanto se trabaja en modo degradado (`seed: none (unavailable)`), declarando cada sustituto.
- Taste no trae catálogo de escenas. Las 2 o 3 escenas de scroll se construyen a mano sobre `stage.js`.

## 2. Fotografía (el corazón del feedback)
- La v1 tenía en la práctica 3 fotos visibles por pantalla, según inspect. La v2 tendrá **entre 6 y 12 fotos épicas como mínimo**, repartidas en **3 a 5 tratamientos distintos**:
  - banda a sangre,
  - split,
  - mosaico desigual,
  - foto sostenida mientras pasa el texto,
  - un marco que crece una sola vez.
- **Una foto decisiva por cuento.** Impeccable: *"one decisive photo beats five mediocre ones"*.
- **Selección:** likes normalizados por época, más calidad técnica, más fuerza narrativa (fases 3–5).
  - Una sola familia de luz: la noche cálida de la barra.
  - Dos proporciones cubren al menos el 75 % de las fotos (4:5 y 16:9).
- **Tratamiento:**
  - esquinas rectas;
  - sin marco, sin polaroid, sin rotación, sin sombra;
  - si una foto lleva texto encima, solo un scrim neutro.
- **Portada:** footage propio que ocupe al menos el 40 % de la pantalla (ideal: a sangre), con loop corto, muted y poster, en versión horizontal y vertical.

## 3. Texto y voz
- **h1 en la primera pantalla y en 2 líneas como máximo.** El apoyo va con la bio: "Coctelería de autor, comida & música bonita desde 2014".
- **Aritmética de 2 líneas.** Las citas literales largas que en la v1 eran titulares de 3 a 7 líneas pasan a `<p>` de ≤36 px (≤24 px en móvil). Si no, se elige un fragmento literal de ≤32 caracteres. Six Caps tiene k≈0,40.
- **Sin eyebrows, sin numeración de secciones, sin rótulos chicos sobre los títulos.** El titular literal se basta solo.
- **Prueba antes que afirmación.** Hablan por sí solos los nombres de los tragos, el equipo con sus @ y las fotos de sus fiestas. Ningún adjetivo es nuestro.
- **Emoji (choque resuelto).**
  - Taste los marca FAIL; Impeccable los tolera dentro de citas.
  - Decisión: **se quitan los glifos emoji del texto visible.** Va como corrección mínima documentada, igual que en la carta. La palabra literal se mantiene.
  - Nunca se usan como icono ni como ornamento. Los iconos son SVG propios, de un solo trazo.
- **Léxico de la casa** (GÜERGÜERO, CELEBREICHON…). Es lo más propio que tienen, así que sobrevive, pero no como píldoras:
  - o una sola marquesina de letra grande, plana, lenta y pausable;
  - o las palabras vuelven *dentro* de sus cuentos.
- **"Almudcito ito ito"** se rescata como texto dentro de una escena, no como pantalla de carga.

## 4. Tipografía, color y grilla
- **Tipografía:**
  - Dos familias como máximo: Six Caps (display) y Oswald (texto). Big Shoulders queda solo dentro del logotipo. **Caveat sale.**
  - Hay que probar si Oswald aguanta párrafos en ES/EN. Cuerpo ≥16 px (objetivo 18) y medida ≤75ch.
  - Cinco tamaños (la v1 tenía 32): 14 / 18 / 24 / ~56 / display. El display mide al menos 4 veces el cuerpo.
- **Color con roles, no muestrario:**
  - noche de fondo y papel de tinta;
  - **un solo acento**: el rosa del muro (`--barra`), solo en acciones y en un recurrente;
  - pisco, cinta, cielo y brasa solo como **campos planos por capítulo**, con cortes duros. Nunca arcoíris en una misma pantalla.
  - La paleta final se deriva de las fotos ganadoras (fase 8).
- **Violeta y crema:**
  - El violeta #9b5cff **sale**: es de las luces, no de la marca.
  - El azul de la carta va solo sobre papel, como "lo impreso", con `--allow palette-purple` justificado.
  - El crema #f6ecdc se queda (sale de sus posavasos), pero sin terracota.
- **Superficies del navegador con marca:**
  - `::selection`, `caret-color` y anillos de foco;
  - scrollbars visibles en los carruseles;
  - `text-underline-offset`;
  - `tabular-nums` en precios y horarios.
- **Grilla:**
  - márgenes iguales de `clamp(16px, 2,2vw, 32px)`;
  - 2 o 3 anclas de texto, alineadas a la izquierda, con un solo momento centrado;
  - separación de secciones de 120 a 240 px;
  - ninguna media pantalla vacía.
- **Sin** sombras de reposo, text-shadow, glass/blur, degradados decorativos ni hairlines (la carta se separa con espacio y tono). Los botones son planos y su forma se decide una sola vez.

## 5. Movimiento (Emil, más los presupuestos de Taste e Impeccable)
**Tokens únicos** (prohibido escribir curvas sueltas):

| Token | Valor |
|---|---|
| `--ease-out` | `cubic-bezier(.23,1,.32,1)` |
| `--ease-in-out` | `cubic-bezier(.77,0,.175,1)` |
| `--ease-drawer` | `cubic-bezier(.32,.72,0,1)` |
| `--d-press` | 140 ms |
| `--d-hover` | 200 ms |
| `--d-ui` | 240 ms |
| `--d-panel` | 400 ms |
| `--d-reveal` | 700 ms |
| `--d-hero` | 800 ms |
| `--stagger` | 40 ms |
| `--stagger-card` | 60 ms |

En GSAP: `CustomEase` con los mismos nombres y `gsap.defaults({ease:'out', duration:.24})`.

**Reglas:**
- **Un único momento autoral** (Impeccable) y la firma que reparta Taste. Candidato: "el almud se abre", rehecho a ≤300 vh, con texto y algo que mirar en cada pantalla. Si no pasa la ronda de dirección, se elimina.
- **Entradas cortas:**
  - desplazamiento de 8 a 16 px, o una máscara de línea;
  - fotos con `clip-path: inset(0 0 100% 0) → inset(0)`, 600 ms, `--ease-in-out`;
  - todo `once`, salvo un único scrub;
  - el cuerpo de texto aparece sin animación.
- **Salidas** a ~60 % de su entrada (el panel abre en 400 ms y cierra en 250 ms).
- **Nunca:**
  - ease-in, elastic, back o bounce;
  - escalar desde `scale(0)` (mínimo .92);
  - nada acoplado a la velocidad del scroll;
  - loader, grano animado, cursor propio, botones magnéticos, una foto que siga al puntero, contadores desde 0;
  - bucles ociosos;
  - animar algo que no sea transform, opacity o clip-path, o usar `transition: all`.
- **Feedback de presión en todo lo presionable:** `:active scale(.97)` en 140 ms. Es el mayor hueco de la v1.
- **Hover** solo bajo `(hover:hover) and (pointer:fine)`. **El teclado nunca anima.**
- **Portada:** legible y clicable en ≤1,2 s. Letras con máscara de 800 ms y stagger de 35 ms; el video pasa de 1.04 a 1.
- **Parallax** solo en fotos sin texto: ±6 %, y nunca en móvil.
- **Menú:** clip-path de 400 ms con `--ease-drawer`, cierre de 250 ms por el mismo borde; Escape cierra al instante.
- **Pestañas de la carta:** 200 ms.
- **Carruseles:** `scroll-snap` nativo antes que JS.
- **Presupuesto Taste:** al menos 8 elementos en movimiento (objetivo 16) y una "cosa viva" con contenido real. Propuesta: "¿qué toca hoy?", con la promo del día, que ya existe.
- **Reduced motion = menos y más suave, no cero:** se mantienen los fades de opacidad de 150 a 200 ms. Fuera transform, scrub, marquesina y Lenis. La página queda terminada y legible.
- **Rendimiento:** CSS y WAAPI primero; GSAP solo para las timelines de scroll. `will-change` únicamente si se mide.
- **Regla de oro:** si una animación no se justifica en una palabra (feedback, espacio, estado, explicación, delight único), se borra.

## 6. Veredicto sobre la v1
| Elemento | Veredicto | Motivo |
|---|---|---|
| Flecos CSS entre secciones | **Fuera** | Material falso, degradado y oscilan con la velocidad del scroll. Las tres skills lo condenan y tú también. |
| Cinta arcoíris `--rib` y 6 colores rotados por ítem | **Fuera** | Color sin rol. |
| Marquesina de chips de colores | **Fuera como píldoras** | El léxico se queda (§3). |
| Emoji gigantes y ★ ← → | **Fuera** | Se reemplazan por iconos SVG. |
| Caveat, notas rotadas | **Fuera** | Era una tercera familia y una cercanía disfrazada. |
| Polaroids, pinzas, tendedero, alfileres | **Fuera** | Material falso y rotaciones. |
| Botones de vidrio, sombras, grano animado | **Fuera** | — |
| Cargador "Almudcito ito ito" | **Fuera** | Tapa la portada. La frase vuelve como texto. |
| Magnéticos, cursor "Arrastrar", peek | **Fuera** | — |
| Contador 0→4,6 y número gigante con estrellas | **Fuera** | La prueba se integra en el relato. |
| Isotipo fijado durante más de 10 pantallas vacías | **Se rehace o se va** | — |
| Default GSAP `expo.out` 1 s (todo dura 0,7–1,6 s) | **Fuera** | Se reemplaza por los tokens. |
| Sin `::selection`, scrollbars ocultas, sin feedback de presión | **Defecto** | Se corrige. |
| Six Caps + Oswald, paleta de sus fotos, bio, carta completa, promo del día, letrero en video, "un almud: la unidad de medida chilota" | **Se queda** | Ahora con disciplina. |

## 7. Mediciones de partida de la v1 (`.taste-skill/before/`)
- **lint:** 40 FAIL y 7 WARN.
  - 18 emoji;
  - 9 degradados;
  - 11 sombras;
  - 2 hairlines.
- **inspect:** 13 FAIL y 12 WARN.
  - titulares de 3 a 7 líneas;
  - 22 box-shadow y 10 text-shadow;
  - 20 hairlines;
  - el violeta;
  - solo 3 fotos contadas;
  - el loader tapando la portada;
  - 11 de 12 pantallas de escritorio casi vacías por el pin;
  - 32 tamaños de letra y 3 familias.
- **review-animations:** Block. 33 animaciones auditadas; la tabla está en `emil.md` §5.
- **Meta de la v2:** 0 FAIL en lint e inspect a 3 anchos, Approve en review-animations y crítica Impeccable ≥ 26/32.
