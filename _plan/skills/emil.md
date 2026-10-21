# Emil Kowalski · reglas de movimiento aplicadas a Almud v2

Fuente: `/mnt/user-data/outputs/skills/emil-kowalski/` leído completo: emil-design-eng, animate (+RECIPES), review-animations (+STANDARDS), improve-animations (SKILL, AUDIT, PLAN-TEMPLATE), animation-performance, animation-vocabulary, find-animation-opportunities, apple-design, break-ui (+CATALOG), prototype (+PICKER), pick-ui-library.
No aplican: write-swift, animate-expo (React Native), ask-sonner (no hay toasts). `mobile-native` no es nativo sino web en el teléfono: sí aplica en parte (ver §3.3).
Feedback del cliente que manda sobre todo: **premium, rápido al entrar, suave al salir, usado con maestría; los flecos que se mecen con la velocidad del scroll se ven baratos.**

---

## 1. Filosofía y marco de decisión

**Ideas base.** El gusto se entrena, no es innato. Los detalles que nadie nota se acumulan ("mil voces apenas audibles cantando afinadas"). La belleza es palanca. La mejor animación a veces es ninguna ("You Don't Need Animations"): el buscador de oportunidades **rechaza la mayoría** de candidatas. Ante la duda, borrar la animación es el movimiento más fuerte.

**Las cuatro preguntas, en orden (las dos primeras deciden si se escribe código):**

1. **¿Debe animarse?** Por frecuencia:

| Frecuencia | Decisión |
| --- | --- |
| 100+ veces/día (atajos de teclado, paleta de comandos) | Nunca. Raycast no anima su apertura y es lo correcto |
| Decenas/día (hover, navegar listas) | Quitar o reducir drásticamente (casi imperceptible) |
| Ocasional (modales, drawers, toasts) | Animación estándar |
| Rara / primera vez (onboarding, éxito, celebración) | Aquí vive el presupuesto de *delight* |

**Nunca animar acciones iniciadas por teclado** (descalificador, no juicio).

2. **¿Para qué?** Debe nombrarse en una palabra: *Feedback*, *Consistencia espacial*, *Indicar estado*, *Evitar un cambio brusco*, *Explicación* (solo marketing/onboarding), *Delight* (solo en tier raro). "Se ve bacán" en algo frecuente = no. Y **función**: lo que el usuario está leyendo o usando no se mueve por estilo.

3. **¿Qué curva?** Entra o sale → `ease-out`. Se mueve/transforma en pantalla → `ease-in-out`. Hover/color → `ease`. Movimiento constante (marquesina, progreso) → `linear`. Por defecto → `ease-out`. **Nunca `ease-in` en UI** (retrasa justo el instante que el ojo mira; `ease-out` a 200 ms *se siente* más rápido que `ease-in` a 200 ms). Las curvas nativas de CSS son débiles; usar estas exactas (no inventar, si falta una sacarla de easing.dev / easings.co):

```css
--ease-out:    cubic-bezier(0.23, 1, 0.32, 1);    /* ease-out fuerte para UI */
--ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);   /* movimiento en pantalla */
--ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);    /* drawer tipo iOS (Ionic) */
```

4. **¿Cuánto dura?**

| Elemento | Duración |
| --- | --- |
| Feedback de presión de botón | 100–160 ms |
| Tooltips, popovers chicos | 125–200 ms |
| Dropdowns, selects | 150–250 ms |
| Modales, drawers | 200–500 ms |
| Marketing / explicativo | Puede ser más largo |

**UI bajo 300 ms.** Un select de 180 ms se siente más rápido que uno de 400 ms; un spinner que gira rápido hace sentir que carga antes; tras el primer tooltip, los siguientes salen sin delay ni animación.

**Resortes (springs).** Para drag con momentum, elementos "vivos" (Dynamic Island), gestos interrumpibles y seguimiento decorativo del mouse. Config Apple (recomendada): `{ type: "spring", duration: 0.5, bounce: 0.2 }`; física: `{ mass: 1, stiffness: 100, damping: 10 }`; para mouse: `useSpring(…, { stiffness: 100, damping: 10 })`. Bounce sutil **0.1–0.3**, evitarlo en la mayoría de UI; reservar para drag-to-dismiss y lo lúdico. Apple: por defecto **damping 1.0** (sin rebote); rebote (~0.8) **solo si el gesto traía momentum**. Valores Apple: mover 1.0/0.4, rotación 0.8/0.4, drawer 0.8/0.3 (damping/response). Un resorte conserva velocidad al interrumpirse; keyframes reinician desde cero.

**Cohesión.** El movimiento calza con la personalidad: lo lúdico puede rebotar más, un dashboard es seco. Sonner usa `ease` y algo más lento para sentirse elegante. Revisar al día siguiente, en cámara lenta (2–5×) y cuadro a cuadro (DevTools › Animations).

## 2. Principios por componente

- **Botones:** `:active { transform: scale(0.97) }` con `transition: transform 160ms ease-out`; rango 0.95–0.98. Aplica a todo lo presionable. Apple: feedback en *pointer-down*, nunca solo en `click`; `scale(0.97)` a 100 ms ease-out.
- **Nunca `scale(0)`:** partir de `scale(0.9–0.97)` + `opacity: 0` ("un globo desinflado igual tiene forma").
- **Popovers con origen:** `transform-origin` en el disparador (`var(--transform-origin)` en Base UI). **Modales exentos**: quedan centrados.
- **Recetas exactas (RECIPES):** dropdown/popover `opacity+transform 200ms --ease-out` desde `scale(0.95)`; tooltip `125ms` desde `scale(0.97)` + `[data-instant]{transition-duration:0ms}`; modal `250ms --ease-out` desde `scale(0.96)` + backdrop opacity 250 ms; drawer `transform 500ms --ease-drawer` desde `translateY(100%)`; toast `400ms ease` con `@starting-style { opacity:0; transform:translateY(100%) }`; acordeón `height+opacity 200ms --ease-out` (único caso tolerado de `height`, medir en JS, nunca a `auto`).
- **Transiciones, no keyframes, para UI que se dispara rápido:** las transiciones se re-dirigen desde el valor actual; los keyframes parten de cero.
- **`@starting-style`** para entrar sin JS; fallback: atributo `data-mounted`.
- **Blur para tapar un crossfade que no cuaja:** `filter: blur(2px)` + `opacity: .7` durante 200 ms `ease`; blur siempre < 20 px (2–5 px basta), caro en Safari.
- **Transforms:** `translateY(100%)` en porcentajes (relativo al propio elemento) antes que px; `scale()` escala a los hijos (es una virtud); 3D con `preserve-3d`.
- **clip-path `inset(t r b l)`** (cada valor "come" desde ese lado): revelado de imagen al scroll `inset(0 0 100% 0) → inset(0 0 0 0)` en **600 ms `--ease-in-out`**, disparado una vez (`IntersectionObserver` / `useInView({ once: true, margin: "-100px" })`), solo en superficies de marketing; hold-to-delete `inset(0 100% 0 0)` → `inset(0)` en **2 s linear** al presionar y **200 ms ease-out** al soltar; tabs con color perfecto (lista duplicada, se recorta la copia activa, 250 ms `--ease-in-out`); slider antes/después.
- **WAAPI** con curva exacta: `el.animate([{clipPath:'inset(0 0 100% 0)'},{clipPath:'inset(0 0 0 0)'}], {duration:1000, fill:'forwards', easing:'cubic-bezier(0.77, 0, 0.175, 1)'})`.
- **Drag/gestos:** descartar por velocidad, no solo por distancia (`|d|/ms > 0.11`); `setPointerCapture`; ignorar toques extra (`if (isDragging) return`); amortiguar más allá del borde (rubber-band `(o·d·0.55)/(d+0.55·|o|)`), fricción en vez de muro. Apple: seguimiento 1:1 respetando el punto de agarre, ~10 px de histéresis, entregar la velocidad al resorte, proyectar el destino `actual + (v/1000)·0.998/(1−0.998)` y ajustar al snap más cercano a esa proyección; animar siempre desde el valor presente; nunca bloquear input durante una transición.
- **Stagger:** 30–80 ms entre ítems (receta: 0/50/100/150 ms, `translateY(8px)` + opacity, 300 ms ease-out). Decorativo: nunca bloquea interacción.
- **Asimetría:** lento donde el usuario decide, rápido donde responde el sistema; **la salida más rápida que la entrada**. Simetría en press/release o hold = hallazgo.
- **Consistencia espacial (Apple):** sale por donde entró; reversibles con curva espejo; el movimiento intermedio apunta al destino.

## 3. Rendimiento y accesibilidad

### 3.1 Rendimiento
- **Solo `transform` y `opacity`** (más `clip-path` como cuarto sancionado). Niveles: *solo composite* (`transform`, `opacity`; en Chrome/Firefox también `filter`, `clip-path`, `background-color`), *paint* (`box-shadow`, `border-radius`, `color`), *layout* (`width`, `height`, `padding`, `margin`, `top`, `left`, `border-width`).
- Swaps: tamaño → `scale()`; mover → `translate()`; `display/visibility` → `opacity`; `box-shadow` animado → `filter: drop-shadow()`.
- **Nunca `transition: all`.**
- Presupuesto: 16,7 ms a 60 Hz, **8 ms a 120 Hz** (diseñar contra el menor). El MacBook es el dispositivo menos representativo: medir en un teléfono gama media.
- **Dónde corre:** JS + rAF (GSAP, Lenis) siempre en el hilo principal; CSS y WAAPI pueden ir fuera de él. Lo que suena mientras la página está ocupada (carga, hidratación, navegación) → CSS/WAAPI. Reparto: CSS para lo predeterminado, JS para lo dinámico e interrumpible.
- **Variables CSS heredables:** cambiar una var en un padre recalcula estilos de todos los hijos; escribir `transform` directo en el elemento. Animar una var nunca se acelera.
- No animar vía estado/render por frame; escribir en `el.style`.
- **`will-change: transform`** solo tras ver el salto de 1 px o frames perdidos medidos; nunca en `*` ni contenedores grandes (cada capa cuesta memoria GPU). Orden de diagnóstico: propiedades → hilo ocupado → re-render por frame → empeora con más contenido (var heredada) → var animada → blur > 20 px → recién `will-change`.
- *Layout thrashing* = animar propiedades que fuerzan layout cada frame (vocabulario).

### 3.2 Accesibilidad
- `prefers-reduced-motion: reduce` = **menos y más suave, no cero**: conservar opacidad/color que ayudan a entender; quitar posición, escala, parallax, rebote. Apple: además `prefers-reduced-transparency` (superficies sólidas) y `prefers-contrast: more`; evitar fondos a pantalla completa que se mueven, oscilaciones lentas (~0,2 Hz) y saltos bruscos de brillo.
- Hover con movimiento solo bajo `@media (hover: hover) and (pointer: fine)`; el touch recibe `:active`.

### 3.3 mobile-native (web en el teléfono, aplica)
`-webkit-tap-highlight-color: transparent` + `:active` propio; `touch-action: manipulation` en botones/enlaces; `100svh` en el hero (ya está), `100dvh` en el menú a pantalla completa; `user-select: none` solo en controles; carruseles con `scroll-snap` nativo o `touch-action: pan-y`; `theme-color` por esquema (hoy hay uno solo); nunca `user-scalable=no`; probar en hardware real.

## 4. Checklists de revisión

### 4.1 review-animations · los 10 estándares
1. Movimiento justificado. 2. Acorde a la frecuencia. 3. Easing que responde (custom, nada de `ease-in`). 4. UI < 300 ms. 5. Origen y física correctos (nada de `scale(0)`; modales exentos). 6. Interrumpible (transiciones/resortes). 7. Solo propiedades GPU. 8. Accesible (reduced-motion suave + hover con media query). 9. Entrada/salida asimétrica. 10. Cohesión con la personalidad.

**Disparadores de escalamiento (marcar a la vista):** `transition: all`; `scale(0)` o entradas solo-fade sin transform inicial; `ease-in` en UI o easing nativo débil en algo deliberado; animación en atajo de teclado / acción 100+/día; UI > 300 ms sin razón; `transform-origin: center` en popover anclado; keyframes en toasts/toggles; propiedades de layout; shorthands `x/y/scale` de Motion bajo carga; var CSS en padre moviendo hijos; falta reduced-motion; `:hover` sin gate; timing simétrico en press/hold; todo entrando a la vez donde corresponde stagger 30–80 ms.

**Jerarquía de remedio:** 1 borrar → 2 reducir → 3 arreglar easing → 4 origen/física → 5 interrumpible → 6 a GPU → 7 asimetría → 8 pulido (blur, stagger, `@starting-style`, resorte) → 9 accesibilidad y cohesión.
**Formato obligatorio:** tabla única `| Before | After | Why |` (nunca lista "Before:/After:"), luego veredicto por niveles (regresiones que rompen la sensación → simplificaciones perdidas → rendimiento → interrupción/timing → origen/cohesión → accesibilidad) y decisión explícita **Block / Approve** con `file:line`.

### 4.2 improve-animations · AUDIT + PLAN-TEMPLATE
Flujo: **Recon** (stack, dónde vive el movimiento, tokens, personalidad, mapa de frecuencia; greps: `transition`, `animation`, `@keyframes`, `ease-in`, `transition: all`, `scale(0)`, `prefers-reduced-motion`, `transform-origin`) → **Auditoría en 8 categorías** (propósito y frecuencia · easing y duración · física y origen · interrupción · rendimiento · accesibilidad · cohesión y tokens · oportunidades perdidas) → **Vetar** (re-leer cada `file:line`, descartar lo exento) → tabla `# | Severidad | Categoría | Ubicación | Hallazgo | Fix` (HIGH = rompe la sensación; MEDIUM = notoriamente mal; LOW = pulido) + 2–4 oportunidades → **Planes**.
Cada plan (`plans/NNN-slug.md`): encabezado (Status, Commit, Severity, Category, Scope) · **Problem** con código actual verbatim y `file:line` · **Target** con todos los valores escritos · **Repo conventions** con un ejemplo a imitar · **Steps** (una edición por paso) · **Boundaries** (no tocar fuera de alcance, sin dependencias nuevas, si el código cambió: parar) · **Verification** (mecánica + *feel check* a 10 % de velocidad, toggle de reduced-motion en Rendering, "Done when"). Luego `plans/README.md` con orden y dependencias. Regla: el ejecutor no tiene contexto ni gusto; nada de "la curva que vimos".

### 4.3 find-animation-opportunities
Compuerta de 4 preguntas (frecuencia, propósito, velocidad dentro del presupuesto, función). Máximo 5–7 sugerencias por app. Reporte: tabla de oportunidades con valores exactos + **candidatas rechazadas obligatorias** con la pregunta que las mató + veredicto de un párrafo.

### 4.4 break-ui · lo que aplica a esta web
Datos peores pero plausibles, entrando por la misma frontera que los datos demo (el HTML / `data-en`), con un toggle *Demo / Peor caso* solo en desarrollo. Para Almud:
- **Textos traducidos más largos** (EN ~30 % más en FR; botones como "How to get here", "Open in Google Maps"): botones con ancho por contenido y `min-width`, nunca `width` fijo.
- **Nombres de platos y tragos largos** en la tipografía display (`.dish__n`, `.show__n`) y la nav del menú a 120 px: probar 320 px y zoom 200 %.
- **Reseñas:** nombre largo con diacríticos (`Aleksandra Wiśniewska-Kowalczyk`), nombre de 2 letras, texto muy largo vs. una línea, emoji y ZWJ (`👩🏽‍💻`) → `line-clamp` o altura de tarjeta predecible; idioma de la reseña (ya hay `rev__lang`).
- **Números:** nota `4,6`/`4.6` con `Intl.NumberFormat` según idioma (hoy se reemplaza a mano) y `font-variant-numeric: tabular-nums` si cambia en vivo; precios con separador de miles; plurales con `Intl.PluralRules`.
- **Leyendas de polaroids/afiches con emoji** (`💥`, `😜`, `🫶🏼`) y saltos de línea; captions largos en `.pin figcaption`.
- **Medios:** imagen que no carga (fallback a `.plate`), panorámicas con `object-fit: cover`, `aspect-ratio` fijo para no generar *layout shift*.
- **Estados/entorno:** promo "hoy" ausente (domingo sin promo), mapa sin iframe, sin JS/sin GSAP, 320 px, 2560 px, zoom 200 %, touch (acciones que solo existen en hover quedan inalcanzables: el *peek* y el cursor).
Firmas típicas: `min-width: 0` en columnas flex/grid, `overflow-wrap: anywhere` en URLs/emails, `flex-shrink: 0` en íconos, nunca truncar precios ni fechas.

### 4.5 prototype y pick-ui-library
- **prototype:** cuando una decisión de movimiento no se resuelve leyendo código (p. ej. cómo entra el hero), construir 3 variantes divergentes en un eje nombrado ("Quieto", "Editorial", "Lúdico"), cada una cumpliendo el estándar, tras el picker verbatim (píldora oscura abajo al centro, highlight 250 ms `cubic-bezier(0.23, 1, 0.32, 1)`, cambio de variante instantáneo, teclas 1–N, ←/→, R, `?v=`). Todo en un HTML aislado; se borra al elegir.
- **pick-ui-library:** Motion (motion.dev) para resortes/salidas/gestos, **NumberFlow** para números que cambian, base-ui para diálogos/menús accesibles, Sonner para toasts, Embla/Vaul como referencia de proyección. Para un fade basta CSS. Almud ya usa GSAP: no sumar una librería paralela salvo que haga falta un resorte real (Motion `animate()` funciona sin React).

## 5. Auditoría de la v1 (`js/main.js`, `css/main.css`)

Contexto: GSAP con `gsap.defaults({ ease: 'expo.out', duration: 1 })` (main.js:267) y `--ease: cubic-bezier(.16,1,.3,1)` (main.css:17) = easeOutExpo. Es un ease-out fuerte (no está mal) pero **el default de 1 s es el problema de fondo**: todo dura 0,7–1,6 s, que en una web de marketing se lee "lento y teatral", no premium. Equivalencias para v2: `--ease-out` (0.23,1,0.32,1) = easeOutQuint = GSAP `power4.out`; `--ease-in-out` (0.77,0,0.175,1) ≈ `power3.inOut`. Para valores exactos en GSAP: `CustomEase.create('out', '0.23,1,0.32,1')` y `CustomEase.create('inOut', '0.77,0,0.175,1')`.

| # | Animación | Dónde | Hoy | Veredicto | Fix preciso |
| --- | --- | --- | --- | --- | --- |
| 1 | **Cargador** | main.js:288-292; css:48-53 | 4 palabras con `back.out(2)` (rebote), stagger 140 ms, cortina `clip-path` 0,8 s `expo.inOut`; ~1,8 s antes de ver el hero | **Cambiar** (o quitar) | Rara/primera vez: hay presupuesto de delight, pero no puede bloquear ~2 s. Sin `back.out`: palabras `translateY(40%)`+opacity 300 ms `--ease-out`, stagger 50 ms; cortina `inset(0 0 100% 0)` 500 ms `--ease-in-out`; total ≤ 1 s. Si `almud-seen`: **no mostrarlo**. Ideal v2: que el propio revelado del hero sea la intro y eliminar el loader |
| 2 | **Letras del hero** | main.js:293; css:99-100 | máscara `yPercent:105`, 1,2 s, stagger 50 ms | **Mantener, acortar** | Es el momento de marca y usa transform (no solo fade): bien. 800 ms `--ease-out`, stagger 35 ms, empezar 100 ms antes de que termine la cortina |
| 3 | **Iso elástico** | main.js:294; css:101 | `rotate:-25, scale:.4`, `elastic.out(1,.6)` 1,3 s | **Cambiar** | `scale(.4)` está bajo el mínimo 0.9 y el elástico oscila varias veces (rebote sin gesto que lo justifique = barato). `scale(.92)`, `rotate(-6deg)`, opacity, 700 ms `--ease-out`. Si se quiere un guiño lúdico: un solo resorte `{duration:.5, bounce:.2}` (Motion), nunca elastic |
| 4 | Copy y CTAs del hero | main.js:295-296 | `yPercent:110` 1 s stagger 80 ms; CTAs `y:30` 1 s stagger 80 ms | **Cambiar** | 600 ms `--ease-out`, `y: 12px`, stagger 50 ms; los CTA deben ser clicables desde el primer frame (stagger nunca bloquea) |
| 5 | Parallax del hero | main.js:306-307 | media `yPercent:10`, texto `-18%` + opacity .2, scrub | **Mantener, reducir** | Media `yPercent: 6`; texto solo opacity → .4 sin desplazamiento (no mover lo que se lee). Mejora: CSS `animation-timeline: scroll()` para sacarlo del hilo principal |
| 6 | Indicador de scroll | css:106-108 | keyframes infinito 1,8 s | **Cambiar** | Bucle eterno = movimiento ocioso que Apple pide evitar. `animation-iteration-count: 3` y ocultarlo al primer scroll |
| 7 | **Marquesina léxico** | main.js:310-313; css:125-129 | rAF por frame, velocidad `.5 + vel*.12` hasta 12 px/frame, lee `offsetWidth` cada frame | **Cambiar** (o quitar si el léxico sale del guion) | Acoplar a la velocidad del scroll es la misma familia que los flecos. Marquesina = `linear` constante: `@keyframes` CSS `translateX(-50%)` con 2 copias, `linear infinite`, ~40 s el ciclo (corre fuera del hilo principal). Pausa en `:hover` con gate. Reduced-motion: lista estática envuelta (ya existe) |
| 8 | **Flecos con skew por velocidad** | main.js:321-325; css:163-170 | `skewX` ±14° por ticker cada frame, sobre elemento con `mask` + `filter: drop-shadow` | **Quitar** | Feedback del cliente + sin propósito nombrable + repinta máscara y sombra cada frame (paint, no composite) + un ticker por fleco aunque la velocidad sea 0. Borrar markup (index.html:147, 232, 325), CSS y JS |
| 9 | **Historia: el almud se abre** | main.js:328-356; css:131-154 | 420 vh, polígono `clip-path` reescrito por frame, `scrub: .6`; iso `scale 3.2` `power2.in`; líneas entran `power3.out`, salen `power2.in` | **Mantener la idea, cambiar** | Es *Explicación/Delight* de única vez: el momento memorable. Arreglos: (a) `power2.in` → `none` o `inOut` (nada de ease-in); (b) salida de cada línea más corta que la entrada (`seg*.2` vs `seg*.35`) y con `--ease-out`; (c) `scrub: true` (o ≤ .3) porque Lenis ya suaviza: doble suavizado = sensación gomosa y con lag; (d) bajar a ~300 vh; (e) el iso no debe superar `scale(2)` con opacity a 0 en el primer 60 % |
| 10 | **Manifiesto palabra a palabra** | main.js:359-366; css:159-161 | cada palabra de opacity .2 → 1 con scrub; firma `elastic.out` desde `scale .7` | **Cambiar** | Texto a 0,2 de opacidad no se puede leer: se mueve lo que se lee. Rango más corto (`top 80%` → `center 55%`), opacidad inicial .3, o mejor: revelado por líneas una sola vez (máscara `yPercent:100`, 700 ms `--ease-out`, stagger 60 ms). Firma: `scale(.95)`+opacity, 500 ms `--ease-out`, sin elastic |
| 11 | Revelado de títulos `.h-display` | main.js:316-318 | máscara 1,2 s `once` | **Mantener, acortar** | 700 ms `--ease-out`, stagger 60 ms entre líneas, `start: 'top 85%'`, una vez |
| 12 | **Rincones horizontales** | main.js:369-379; css:173-196 | sticky + `x` scrub .5 + parallax interno ±3 % por imagen + barra | **Mantener (escritorio)** | Consistencia espacial legítima. `scrub: true` por el doble suavizado; parallax interno ±2 % o fuera (son 9+ tweens de scroll); `will-change` del track gigante: medir memoria y quitarlo si no hay salto de 1 px. Móvil: `scroll-snap` nativo ya está (bien) |
| 13 | **Masas a distinta velocidad** | main.js:382-386; index.html:219-251 | `y` ±`s·0,6·innerHeight` (hasta ±135 px); **también aplicado a los afiches del tablero**; `.food__copy` desde `scale .85` 1,4 s | **Cambiar** | Masas: tope ±60 px. **Quitar `data-speed` de `.pin`** (contenido con texto que se lee no debe flotar). `.food__copy`: `scale(.96)`+opacity, 700 ms `--ease-out` |
| 14 | Afiches que caen + hover | main.js:389; css:275-284 | `scale .8` 1,2 s cada uno; hover `rotate/scale` 600 ms sin gate | **Cambiar** | Entrada `scale(.96)` + `y:12px`, 600 ms `--ease-out`, stagger 50 ms por fila (batch). Hover bajo `(hover:hover) and (pointer:fine)`, 200 ms `ease` |
| 15 | **Tendedero: balanceo por velocidad** | main.js:392-396; css:295 | tween de la var `--sw` por polaroid en cada cambio de velocidad; entrada `y:-60` `back.out(1.6)` 1,2 s | **Quitar el balanceo; cambiar la entrada** | Mismo patrón barato que los flecos y además anima una **variable CSS** (recalcula estilos, no acelera). Entrada: `y:-16px`+opacity, 600 ms `--ease-out`, stagger 50 ms, sin `back` |
| 16 | Arrastrar el tendedero | main.js:206-211 | solo mouse, `scrollLeft` 1:1, se detiene en seco al soltar | **Cambiar** | Al soltar, proyectar con `v·0.998/(1−0.998)/1000` y animar `scrollLeft` con `--ease-out` 400 ms; o mejor `scroll-snap-type: x mandatory` + snap nativo. Umbral 10 px antes de considerar drag (no comerse clicks) |
| 17 | **Número de reseñas 0 → 4,6** | main.js:399-400; css:311 | contador 1,6 s `expo.out` reescribiendo texto, sin cifras tabulares | **Quitar** (o reducir) | Contar desde 0 muestra por un instante una nota falsa. Mostrar `4,6` estático con `Intl.NumberFormat`. Si se conserva: NumberFlow o 500 ms con `tabular-nums` |
| 18 | Swiper de reseñas | main.js:221-225 | `speed: 800`, flechas magnéticas, teclado activo | **Cambiar** | 400 ms y `.swiper-wrapper{transition-timing-function: var(--ease-out)}`. Con teclado: el cambio debería ser casi instantáneo (regla de teclado) |
| 19 | **Botones magnéticos** | main.js:409-414; index.html:48,94-95,291-292,309-310 | `x/y` hasta 30–35 % de la distancia, 600 ms | **Quitar** | Aleja el objetivo del puntero (rompe "contenido y dedo se mueven juntos"), se repite decenas de veces y es otro efecto "de plantilla". Reemplazar por `:active scale(.97)` 160 ms `--ease-out` |
| 20 | **Cursor "Arrastrar"** | main.js:239-245, 415-417; css:358 | burbuja desde `scale(0)`, sigue al puntero con retraso 450 ms | **Quitar** | `scale(0)` está prohibido; el retraso se siente pesado. `cursor: grab/grabbing` nativo + pista estática "arrastra →" junto al tendedero/reseñas |
| 21 | Vistazo de foto del plato | main.js:132-142, 416-417; css:359 | `scale .6→1` 500 ms; sale 400 ms; sigue al puntero | **Cambiar** (o quitar) | Hover de lista = decenas de veces: casi imperceptible. `scale(.95)`+opacity 180 ms `--ease-out`, salida 120 ms; `transform-origin` hacia el puntero. Solo puntero fino (ya) |
| 22 | **Menú** | main.js:157-176; css:76-88 | abre `clip-path` 900 ms `expo.inOut` + links 1 s con delay 250 ms (~1,5 s); cierra 700 ms por el lado opuesto; Escape también anima | **Cambiar** | Modal/drawer: abrir `clip-path` 400 ms `--ease-drawer`; links `yPercent:100→0` 350 ms `--ease-out`, stagger 40 ms, empezando a 100 ms. Cerrar 250 ms `--ease-out` **por el mismo borde** (reverso), salida más rápida que entrada. Escape: cierre instantáneo o ≤ 150 ms. Re-tomar desde el valor actual (`gsap.to`, no `fromTo`) para que abrir durante un cierre no salte. Fotos del menú: crossfade 250 ms con `blur(2px)` en el cruce; hover de link `translateX` 200 ms con gate. `100dvh` |
| 23 | Cambio de pestaña de la carta | main.js:91; css:204-206 | panel `opacity 0, y:24` 700 ms; `tab:hover translateY(-2px)` 350 ms sin gate | **Cambiar** | Decenas por visita y también con flechas: 200 ms opacity + `y:8px` `--ease-out`; 0 ms si vino del teclado. Hover con gate, 150 ms |
| 24 | Plato activo (vitrina) | main.js:116-119; css:215-224 | foto `clip-path inset(100%…)` 900 ms; textos `y:30` 800 ms; acordeón `grid-template-rows` 550 ms | **Cambiar** | Foto `inset(0 0 100% 0)→0` 350 ms `--ease-out`; textos `y:8px` 250 ms stagger 30 ms; acordeón 200 ms `--ease-out` (único `height` tolerado). `refresh` de ScrollTrigger al terminar, no con `setTimeout(600)` |
| 25 | Botones `.btn` (relleno) | css:111-122 | `::before translateY` 550 ms, color 450 ms, sin gate, sin `:active` | **Cambiar** | Relleno 250 ms `--ease-out`, color 200 ms `ease`, todo bajo gate de hover; `:focus-visible` igual; **agregar `:active { transform: scale(.97) }` 160 ms** |
| 26 | Hovers sueltos | css:72-73, 85-87, 215-217, 240-243, 328-329 | burger 500 ms, links menú 500 ms, platos 450 ms, promo `scale(1.06)` 1 s, flechas 350 ms; **ninguno con gate** | **Cambiar** | Todos bajo `@media (hover:hover) and (pointer:fine)`, 150–250 ms; promo `scale(1.03)` 400 ms (imagen, marketing) |
| 27 | Sello "hoy" de la promo | css:247-249 | `rotate(-6deg) scale(0)` → `scale(1)` | **Cambiar** | `scale(.9)` + opacity, 250 ms `--ease-out`, 300 ms de delay al entrar en vista |
| 28 | Cabecera que se esconde | main.js:283; css:56-58 | `translateY(-110%)` 600 ms | **Mantener, acortar** | Ocultar 250 ms `--ease-out`, mostrar 200 ms (respuesta del sistema = rápida) |
| 29 | Barras de sonido | css:148-152 | keyframes de **`height`** infinitos | **Cambiar** | Indica estado (bien), pero `height` es layout: `transform: scaleY()` con `transform-origin: bottom` |
| 30 | **Grano** | css:43-46 | capa fija 200 % con `mix-blend-mode: overlay`, keyframes `steps(6)` infinitos | **Cambiar** | Fondo a pantalla completa en movimiento perpetuo + mezcla sobre toda la página cada frame. Grano estático (sin animación) o quitarlo |
| 31 | Lenis | main.js:270-276 | `duration 1.1`, easing expo | **Revisar en dispositivo** | Agrega latencia al input (Apple: "matar la latencia"). Si se mantiene: más corto y sin doble suavizado en los scrub; nunca en touch (ya es así por defecto) |
| 32 | Reduced-motion global | css:402-421 | `*{animation:none!important;transition:none!important}` | **Cambiar** | Hoy mata también el feedback. Conservar transiciones de `opacity`/`color` a 150–200 ms; quitar solo transform, parallax, marquesina, scrub y el loader |
| 33 | Skip link | css:33-34 | anima `top` 300 ms | **Cambiar** | `transform: translateY()` 200 ms `--ease-out` |

**Veredicto review-animations sobre la v1: Block.** Regresiones que rompen la sensación: flecos y balanceo por velocidad, `scale(0)` (cursor, sello), rebotes elásticos sin gesto, `ease-in` en scrub, duraciones de 0,7–1,6 s en UI (menú, pestañas, vitrina), magnéticos. Rendimiento: tickers por frame, var CSS animada, `height` en keyframes, grano a pantalla completa, máscara+sombra repintada. Accesibilidad: hovers sin gate, reduced-motion que lo apaga todo.

**Priorización estilo improve-animations (impacto ÷ esfuerzo), para convertir en planes `plans/NNN-*.md`:**

| # | Severidad | Categoría | Hallazgos | Plan |
| --- | --- | --- | --- | --- |
| 001 | HIGH | Propósito | 8, 15, 19, 20 | Borrar flecos, balanceo, magnéticos y cursor (puro borrado, cero riesgo) |
| 002 | HIGH | Easing y duración | todos | Tokens de §6 + `CustomEase` + `gsap.defaults` a 240 ms; reemplazar `expo.out`/`elastic`/`back`/`power2.in` |
| 003 | HIGH | Física | 3, 20, 21, 27 | Eliminar `scale(0)`/`scale(.4–.85)`; mínimo `.92` |
| 004 | MEDIUM | Duración UI | 22, 23, 24, 18 | Menú, pestañas, vitrina y Swiper al presupuesto de UI |
| 005 | MEDIUM | Accesibilidad | 25, 26, 32 | Gate de hover, `:active`, reduced-motion suave |
| 006 | MEDIUM | Rendimiento | 7, 29, 30, 13 | Marquesina a CSS, `scaleY` en barras, grano estático, parallax acotado |
| 007 | LOW | Pulido | 1, 2, 4, 9-12 | Loader, hero, historia (`scrub:true`, 300 vh), revelados a 700 ms |

**Candidatas rechazadas (find-animation-opportunities):**
- Animar el cambio de idioma con letras que se re-escriben (*text morph*): rechazado por frecuencia y por mover texto que se lee; basta un crossfade de 150 ms.
- Revelar cada precio de la carta al hacer scroll: rechazado por función (dato que se compara) y frecuencia.
- Parallax en las tarjetas de reseñas: rechazado por función (texto largo que se lee).
- Contador de "12 años" en el tablero: rechazado, mismo problema que el 0 → 4,6.

**Oportunidades perdidas (aditivas):** `:active` en todo lo presionable (hoy no existe); `@starting-style` para el iframe del mapa al cargar (fade 200 ms) en vez de aparecer de golpe; feedback de estado al cambiar idioma (crossfade 150 ms del texto con `blur(2px)` en vez de reemplazo seco).

## 6. Aplicado a Almud · reglas de movimiento v2

**Tokens (en `:root`, únicos; prohibido escribir curvas o duraciones sueltas):**

```css
--ease-out:    cubic-bezier(0.23, 1, 0.32, 1);   /* entradas, salidas, respuestas */
--ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);  /* cortinas, cosas que cruzan la pantalla */
--ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);   /* menú a pantalla completa */
--ease-hover:  ease;                             /* color y hover */
--d-press: 140ms;  --d-hover: 200ms;  --d-ui: 240ms;  --d-panel: 400ms;
--d-reveal: 700ms; --d-hero: 800ms;   --stagger: 40ms; --stagger-card: 60ms;
```
En GSAP: `CustomEase` con las mismas curvas (`'out'`, `'inOut'`, `'drawer'`) y `gsap.defaults({ ease: 'out', duration: .24 })`: el default es UI, lo largo se pide explícito.

**Esqueleto CSS base (copiar tal cual en v2):**

```css
html { -webkit-tap-highlight-color: transparent; }
button, a, [role="button"] { touch-action: manipulation; }
.pressable { transition: transform var(--d-press) var(--ease-out); }
.pressable:active { transform: scale(.97); }

@media (hover: hover) and (pointer: fine) {
  .btn::before { transition: transform var(--d-ui) var(--ease-out); }
  .btn:hover::before { transform: none; }
  .link:hover { color: var(--accent); transition: color var(--d-hover) var(--ease-hover); }
}

.reveal-img { clip-path: inset(0 0 100% 0); transition: clip-path 600ms var(--ease-in-out); }
.reveal-img[data-visible] { clip-path: inset(0 0 0 0); }

@media (prefers-reduced-motion: reduce) {
  .reveal-img { clip-path: none; }
  .fade-only { transition: opacity 180ms ease; transform: none !important; }
}
```

**Arranque GSAP (v2):**

```js
gsap.registerPlugin(ScrollTrigger, CustomEase);
CustomEase.create('out', '0.23,1,0.32,1');
CustomEase.create('inOut', '0.77,0,0.175,1');
CustomEase.create('drawer', '0.32,0.72,0,1');
gsap.defaults({ ease: 'out', duration: 0.24 });           // UI por defecto; lo largo se pide explícito
const mm = gsap.matchMedia();
mm.add('(prefers-reduced-motion: no-preference)', () => { /* solo aquí: reveals, scrub, parallax */ });
```

**Vocabulario para pedir movimiento sin ambigüedad (animation-vocabulary):** *Reveal* (clip-path), *Scroll reveal* (una vez), *Scroll-driven animation* (la historia), *Parallax*, *Stagger*, *Orchestration* (hero), *Press feedback*, *Origin-aware animation*, *Crossfade* (+ *Blur* para tapar el cruce), *Marquee* (linear), *Interruptible animation*, *Rubber-banding*, *Momentum*, *Tabular numbers*. Evitar en v2: *Pop in*, *Bounce*, *Wiggle*, *Idle animation*, *Float*, *Pulse*.

1. **Rápido al entrar, suave al salir, nunca al revés:** "rápido al entrar" = la curva arranca de inmediato (`--ease-out`, sin delay previo); "suave al salir" = sin cortes ni aceleración final (también `--ease-out`, con opacidad), **no** más lento: según Emil la salida dura ~60 % de su entrada (panel 400 → 250 ms). Los reveals no tienen salida: son `once`.
2. **Nunca `ease-in`, `elastic`, `back` ni `bounce`** en la web. El único rebote permitido: ninguno por defecto; si un momento lúdico lo pide, un resorte `{duration:.5, bounce:.2}` y solo uno en toda la página.
3. **Nada parte de `scale(0)`:** mínimo `scale(.92)`; para fotos y bloques `scale(.96)`.
4. **Desplazamientos cortos:** entradas con `y` de 8–16 px o máscara `yPercent:100` dentro de `overflow:hidden`; nunca 30–60 px.
5. **Fuera todo lo acoplado a la velocidad del scroll** (flecos, balanceo, marquesina acelerada, skew). El scroll puede *revelar* una vez o *conducir* una historia, nunca sacudir decoración.
6. **Fuera magnéticos, cursor personalizado y contadores desde cero.** Cursor nativo, `cursor: grab`, cifras estáticas con `Intl.NumberFormat`.
7. **Presión en todo lo presionable:** `:active { transform: scale(.97) }`, `transition: transform var(--d-press) var(--ease-out)`, respuesta en *pointer-down*.
8. **Hover:** solo bajo `@media (hover:hover) and (pointer:fine)`, `var(--d-hover)`, color con `ease`; desplazamiento máximo 4 px o `scale(1.03)` en imágenes.
9. **Revelados de scroll:** una sola vez (`once: true`, `start: 'top 85%'`), títulos por línea con máscara `var(--d-reveal) var(--ease-out)` + `--stagger-card`; imágenes con `clip-path: inset(0 0 100% 0) → inset(0)` 600 ms `--ease-in-out` (receta de Emil). Máximo un revelado por bloque visual: el texto de cuerpo aparece sin animación.
10. **Hero (momento único):** letras con máscara `var(--d-hero)` stagger 35 ms; foto/video detrás `scale(1.04)→1` en 1,2 s `--ease-out`; copy y CTAs 600 ms. Todo el hero legible y clicable en ≤ 1,2 s. Sin loader en visitas repetidas; idealmente sin loader.
11. **Un solo momento scrubbed de "explicación"** (la historia que se abre o su sucesor en v2), con `scrub: true`, curvas `none`/`inOut`, ≤ 300 vh, sin `ease-in`. Todo lo demás es `once`.
12. **Parallax:** solo en fotos sin texto encima, tope ±60 px o `yPercent` ±6; nunca en tarjetas con texto, nunca en móvil.
13. **Menú:** abre 400 ms `--ease-drawer` (`clip-path`), links 350 ms stagger 40 ms; cierra 250 ms por el mismo borde; Escape cierra al instante; interrumpible desde el valor actual.
14. **Carta:** cambio de pestaña 200 ms (opacity + 8 px), 0 ms por teclado; vitrina del plato 350 ms foto / 250 ms texto; acordeón móvil 200 ms.
15. **Carruseles (reseñas, rincones en móvil, tendedero):** `scroll-snap` nativo antes que JS; si hay Swiper, 400 ms `--ease-out`; drag con umbral 10 px y proyección por velocidad al soltar.
16. **Marquesina (si sobrevive):** CSS `linear infinite`, velocidad constante, pausa en hover; nunca rAF.
17. **Teclado nunca anima:** foco, tabs con flechas, Escape, atajos del carrusel → cambio instantáneo.
18. **Solo `transform`, `opacity` y `clip-path`.** Nada de `top`, `height` (salvo acordeón 200 ms), `box-shadow` animado (usar `filter: drop-shadow` estático), ni variables CSS animadas. Nunca `transition: all`.
19. **Hilo principal libre:** lo predeterminado en CSS/WAAPI; GSAP solo para timelines de scroll. Ningún `gsap.ticker` permanente salvo Lenis; nada que lea layout por frame.
20. **`will-change`** solo donde se mida el salto de 1 px o frames perdidos (nunca en el track entero sin medir).
21. **Sin bucles ociosos:** ni grano animado ni indicadores infinitos; un indicador de scroll corre 3 ciclos y se va. Las ecualizadores del sonido solo mientras suena, con `scaleY`.
22. **Reduced-motion = menos y más suave:** se quedan los fades de opacidad (150–200 ms) y los cambios de color; se van transform, parallax, scrub, marquesina, loader y Lenis; la historia se muestra estática y legible (ya existe la variante).
23. **Móvil:** `-webkit-tap-highlight-color: transparent`, `touch-action: manipulation` en controles, `100svh` hero / `100dvh` menú, `theme-color` por esquema; probar en un teléfono de gama media real (120 Hz → 8 ms de presupuesto).
24. **Revisión obligatoria antes de publicar:** tabla Before/After/Why de review-animations sobre el diff, cámara lenta a 10 %, toggle de reduced-motion en DevTools, mirar de nuevo al día siguiente; toggle *Demo / Peor caso* de break-ui con textos EN, nombres largos y 320 px.
25. **Regla de oro para el cliente ("con maestría"):** si una animación no se puede justificar en una palabra (feedback, espacio, estado, explicación, delight único), se borra. Menos piezas, cada una exacta.
