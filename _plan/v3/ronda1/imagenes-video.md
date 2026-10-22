# Ronda 1 · Imágenes y video (agente Almud Imágenes + Almud Video)

Revisión de `/v3/` y `/v3/carta/` con Chromium 1194 headless (`--autoplay-policy=no-user-gesture-required`) a 390×844 (DPR 3, táctil), 768×1024 (DPR 2) y 1440×900 (DPR 1). Recorrido pantalla por pantalla con capturas en `_plan/v3/ronda1/medios/` (`home-m-NN`, `home-t-NN`, `home-d-NN`, `carta-m-NN`, `carta-d-NN`, más recortes `zoom-*`) y datos crudos en los `*.json` del mismo directorio. No se editó el sitio.

## Nota: 13/20

| Criterio | Nota | Por qué |
|---|---|---|
| Selección y propiedad | 3/4 | Todo es material propio, sin terceros a la vista, sin exempleados y con disfraces solo en Eventos. No se repite ningún archivo dentro de una página. Pero **faltan las favoritas de trago de Carmen**: P297 splash, P086 sours, P097 copa tallada y P003 old fashioned están preparados en `media.json` y no aparecen en el sitio. Tragos se arma con fotos de la carta (saguer, sangría, moto), que además se repiten en `/carta/`. |
| Recortes | 3/4 | No hay caras cortadas en celular. Fallan: `comida-pizza` en escritorio (caja de 538×1206 que corta la pizza o la cara según el scroll) y el hero de 768 (ojos gigantes). En `equipo-eduardo` el jockey queda rozando el borde superior. En `con-quien-amigas` la clienta de la izquierda sale con los ojos cerrados (va contra la regla de Carmen). |
| Nitidez | 2/4 | En celular (DPR 3) todas las fotos cargan el ancho correcto: el archivo es ≥ al tamaño mostrado por el DPR. Pero el **hero de escritorio** (1278×720 estirado a 1440×900, ×1,25) se ve blando, con bloques de compresión y un fondo blanco lavado. El **hero en 768** usa el video horizontal recortado a vertical, ampliado ~×2,8: se ve muy pixelado. Otros casos: `comida-cazuela` en 768 sale ×1,9 y blanda; `comida-pizza` sale ×1,34 en 1440 y ×1,4 en 768; el letrero de `donde-letrero` a sangre en celular sale ×2,9 (se tolera porque es un letrero luminoso). |
| Reproducción de video | 3/4 | Los 6 `<video>` arrancan solos sin scroll, con `paused=false` y `currentTime` avanzando en el viewport inicial y después de cada salto. El scroll nunca los pausa: en un barrido continuo de 60 px cada 40 ms hubo 0 eventos de pausa. Los loops dan la vuelta sin congelarse en escritorio. En celular se midieron **micro-congelamientos de 0,3 a 1,2 s** en cintas, humo y cazuela (5 decodificaciones simultáneas, ver abajo). El modo de movimiento reducido (`prefers-reduced-motion`) no detiene ningún video. |
| Peso del primer pantallazo | 2/4 | En celular, **sin hacer scroll**, se descargan **≈5,0 MB**: ≈1,95 MB antes del evento `load` (hero 1.347 KB + 6 pósters 217 KB + 4 fotos de El lugar 270 KB + fuentes, CSS y JS) y +3,0 MB justo después, porque `rest()` conecta todos los videos en `load`. El tope del plan era 1.536 KB. En escritorio son ≈6,0 MB. |

## Lo medido

**Videos (celular 390):**

| id | archivo cargado | dur. | estado |
|---|---|---|---|
| `portada-celular` | `portada-celular-900.webm` 1.347 KB, 900×1600 | 4,15 s | Avanza y da la vuelta. Un congelamiento de 0,43 s. |
| `lugar-cintas` | 600×750, 1.181 KB | 5,93 s | Seis congelamientos de 0,36 a 1,0 s en 16 s. |
| `tragos-humo` | 720×900, 564 KB | 7,4 s | Dos congelamientos (1,0 s y 0,44 s). |
| `comida-cazuela` | 720×900, 1.197 KB | 7,8 s | Un congelamiento de 1,18 s al entrar. |
| `donde-letrero` | 958×540, 150 KB | 3,13 s | Sin cortes, 5 vueltas en 16 s. |

En 1440 no hubo ningún congelamiento en los cinco. La diferencia apunta a la carga de decodificación de 5 videos a la vez en celular (los que están fuera de pantalla siguen decodificando), no a los archivos. En un teléfono de gama media de Chiloé será peor que en este headless.

Pósters: todos son WebP correctos y coinciden con el primer frame. En celular también se descarga `portada-escritorio-poster.webp` (52 KB que no se usan), y en escritorio pasa lo mismo con el póster de celular.

**Imágenes:** ninguna se repite dentro de una página. En celular todas usan un `currentSrc` adecuado: 960 para tarjetas de 296 css, 720 para el mosaico de 174 css y 360 para las de la carta de 104 css. No hay ninguna estirada en 390.

## Cambios priorizados

1. **Peso y decodificación en celular.** `js/v3/site.js` → `rest()`: no conectar todos los videos en `load`. Conectar cada `video.v:not([data-hero])` con un IntersectionObserver (`rootMargin: '100% 0px'`) y solo una vez, sin pausarlos nunca después, para mantener la regla de no pausar por scroll. Esto baja el pantallazo de 5 MB a ≈2 MB y quita la decodificación simultánea que causa los congelamientos.
2. **Hero en 768–1023 (tablet vertical).** `css/v3/site.css:68` y `site.js` (`desk = matchMedia('(min-width:768px)')`): elegir la variante por orientación y no por ancho. Usar `(min-width:768px) and (min-aspect-ratio:1/1)` para el video horizontal y `portada-celular-900` en cualquier pantalla vertical. Hoy el iPad vertical muestra ojos borrosos ampliados ~×2,8.
3. **Bajar el hero de celular a ≤1.536 KB en total.** Volver a `portada-celular` en 720×1280 (el plan decía 1.358 KB) o recomprimir el de 900 a ≤1,25 MB. Hoy 1.347 KB de video más pósters, fotos y fuentes ya superan el tope. No precargar el póster de la variante oculta: dejar el atributo `poster` vacío en el `<video>` oculto y ponerlo desde el JS.
4. **`portada-escritorio`.** Rehacer el tramo para que no abra con el techo de cintas sobre fondo blanco de día (frame inicial lavado, "pastel"). Que empiece en lámparas u ojos de noche, o subir la superposición oscura `.hero__veil` en la parte de arriba. Además es 1278×720 estirado: buscar una fuente de 1080p o mantener la recomendación del plan (V021 vertical a alto completo en columna). Es el criterio que más pesa en la primera impresión en escritorio.
5. **Tragos: poner las favoritas de Carmen.** En la sección 3 de `v3/index.html`, reemplazar `carta-saguer` y `carta-sangria` por `tragos-splash[a]` (P297) y `tragos-sours[a]` (P086) o `tragos-copa-tallada[a]` (P097). Dejar las fotos `carta-*` solo en `/carta/`, para que no se repitan entre páginas. Sumar `tragos-old-fashioned` (P003) si hay espacio.
6. **`comida-pizza` en ≥1024.** La caja mide 538×1206 (proporción ~1:2,2) sobre una foto 4:5 y carga el archivo de 720 por `sizes="(min-width:768px) 36vw"`. Fijar `aspect-ratio:4/5` en esa figura (o `object-position:50% 30%` si se mantiene alta) y corregir `sizes` a `(min-width:1024px) 38vw, (min-width:768px) 64vw, 100vw` para que cargue 1280 en 768 y en 1440.
7. **`comida-cazuela` en 768.** Se muestra a ~678 css (≈1356 px a DPR 2) con una fuente de 720: limitar la figura a `max-width:420px` en tablet o reemplazarla por `comida-ceviche[a]` (foto de 1920). En celular también se ve como una "crema" sin la greda: recortar el boomerang a la parte con la greda negra visible.
8. **`con-quien-amigas`.** La clienta de la izquierda tiene los ojos cerrados (regla de Carmen). Cambiarla por `con-quien-barra[a]`, hoy oculta en celular. En celular se ocultan `con-quien-barra` y `con-quien-amigos`: mostrar `con-quien-amigos` en su lugar, porque tiene caras completas y sonrientes.
9. **Movimiento reducido.** `site.js` `attach()`: con `prefers-reduced-motion: reduce`, no llamar `play()` y quitar el atributo `autoplay`, dejando solo el póster. Carmen lo pide explícitamente en el criterio E.
10. **`equipo-eduardo[a]`.** Bajar el encuadre (`object-position:50% 20%` o un recorte nuevo con más aire arriba): el jockey toca el borde superior.
11. **`eventos-14f[a]`.** El alt dice "manos con uñas rosadas…", pero el recorte muestra la cara completa de una persona: confirmar con Carmen que es clienta o del equipo y no una creadora invitada (es la portada de un reel). Ajustar el alt a lo que se ve.
12. **`donde-letrero` en celular.** A sangre en 390 sale ×2,9 y con frecuencia el frame corta "BAR". Darle margen de 16 px como a las demás tarjetas, o un `object-position` que centre el letrero (`50% 60%`).
13. **`lugar-cuadros`.** En escritorio es una miniatura de 313×209 css con luz azul, flotando arriba del titular. Su aporte es menor: quitarla o reemplazarla por `lugar-salon[d]`.
