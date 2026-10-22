# Ronda 2 · Imágenes y video (agente Almud Imágenes + Almud Video)

Revisé `/v3/` y `/v3/carta/` igual que en la ronda 1. Usé Chromium 1194 headless (`--autoplay-policy=no-user-gesture-required`) servido en el puerto 8852, a tres tamaños:

- 390×844 con DPR 3 y pantalla táctil;
- 768×1024 con DPR 2;
- 1440×900 con DPR 1.

Recorrí cada página pantalla por pantalla. Las capturas y los JSON están en `_plan/v3/ronda2/medios/` y la hoja comparativa con Instagram en `_plan/v3/ronda2/medios-vs-ig.jpg`. No edité el sitio.

## Nota: 16/20 (ronda 1: 13)

| Criterio | R1 | R2 | Por qué |
|---|---|---|---|
| Selección frente a su Instagram | 3 | **2** | Las fotos ya están a la altura de su feed. La terraza techada (P189), la barra (P093), el splash (P297), los sours (P086) y la copa tallada (P097) se ven igual que en IG, con el mismo color y el mismo recorte. Pero las **dos portadas pierden frente a su postal**. En celular es un paneo de botellas donde mandan las etiquetas de Jameson y Glenfiddich, sin nadie trabajando. En escritorio, 2 de los 6 fotogramas son el mural de ojos en macro, que llena toda la pantalla. Su foto de "esto es Almud" (P362/P204: un bartender ante el muro rosa) no aparece en ningún lugar del sitio. Del top 20 del ranking faltan P184 (n.º 4), P200 (n.º 5), P195 (n.º 15), P187 (n.º 19) y P073 (el «10», su favorita de evento). |
| Recortes | 3 | 3 | No hay caras cortadas. `comida-pizza` ya se ve en 4:5 en todos los anchos. Sigue pendiente `equipo-eduardo`: el jockey toca el borde (problema de la foto original). `eventos-14f` sigue sin confirmar: en el recorte sale una cara completa y viene de la portada de un reel. |
| Nitidez | 2 | 3 | El hero de tablet se arregló: ahora es vertical, 720×1280 en 768×1024. La cazuela ya no se amplía. El hero de escritorio sigue en 1278×720 estirado ×1,25: las cintas y las lámparas aguantan, pero el macro de ojos se ve blando. Hay una regresión menor: en 390 las 7 tarjetas de El lugar cargan el archivo de 720 para una caja de 296 css × 3 = 888 px (×1,23), porque `sizes` dice `52vw` y la tarjeta mide 76vw. |
| Reproducción de video | 3 | **4** | Los 6 videos se reproducen solos en los tres anchos, con `paused=false` y el tiempo avanzando. Los **congelamientos bajaron a 0**: ninguna pausa de ≥250 ms en 16 s de muestreo por video, con 2 a 5 vueltas de loop cada uno. El scroll nunca los pausa (0 eventos en un barrido continuo). Al saltar directo a #donde, su video se conecta y arranca. Con movimiento reducido no se descarga ningún video, solo quedan los pósters. Los pósters son correctos y ya no se baja el de la variante oculta. |
| Peso del primer pantallazo | 2 | **4** | Sin scroll: celular **1.419 KB** (antes ≈5.000), tablet 1.488 KB y escritorio 2.840 KB (video de 2.401 KB, dentro de su tope de 2.560). `/carta/` pesa 713–720 KB. |

## Comparación con su Instagram (hoja `medios-vs-ig.jpg`)

1. **Portada celular y tablet frente a P362.** El rosa del muro coincide, pero en IG la postal es *oficio*: un bartender trabajando con el cartelito ALMUD. En la web son botellas con marcas de terceros en primer plano y movimiento borroso. El cartelito ALMUD BAR aparece solo al inicio y al final del boomerang.
2. **Portada escritorio frente a P093.** En la captura (t≈1,5 s) se ve solo el mural de ojos en macro, blando. Es su proyecto Ojo Piojo y se agradece, pero como portada no se entiende "bar". La barra curva de P093 está más abajo, en El lugar.
3. **El lugar frente a P189.** Es el mismo encuadre, la misma luz y la misma nitidez. Es lo más fiel del sitio.
4. **Tragos frente a P297 y P086.** Iguales a IG y nítidos (archivo de 720 para 519 px). Muy bien.
5. **Equipo frente a P204.** Las 5 tarjetas cumplen (equipo actual con su @), pero son chicas y en ninguna se ve el gesto de oficio que ella publica: botella en el aire, shaker.
6. **Eventos frente a P073.** Las cuatro fechas se leen bien. Falta el «10» de flores, que ella nombra como su favorita de evento y que en el ranking (n.º 2) supera a las cuatro elegidas.

## Lo que falta para llegar a ≥17 (en orden)

1. **`portada-escritorio`: sacar el tramo de ojos.** Rehacer el loop solo con lámparas y cintas, sin el macro de Ojo Piojo, que ya tiene su tarjeta en El lugar. Si con eso queda corto, alternar con un plano de terraza llena. Así la primera impresión deja de ser "pared de ojos borrosa" y queda noche cálida. Con este punto, Selección pasa a 3 y la nota a 17.
2. **Oficio arriba de la página.** Llevar una foto de bartender en acción frente al muro rosa a un lugar visible: por ejemplo, la primera tarjeta de Equipo en grande (2 columnas en ≥1024) o el inicio de Tragos. Las candidatas son P204 (`DNT1_BYS_Yf_01`), P184 (`DM_Ih5dyVKH_02`) o P200 (`DM_Ih5dyVKH_18`), todas de 1440 px. **Antes hay que confirmar con Carmen que siguen en el equipo** (IG-001), porque no están entre los @ de Equipo. Si no siguen, usar `equipo-javier` en grande, que ya es "oficio ante el muro rojo".
3. **`sizes` de las tarjetas de El lugar** (`v3/index.html`, las 7 `<source>`/`<img>` de `.rin`): cambiar `(min-width:1024px) 60vh, 52vw` por `(min-width:1024px) 60vh, (min-width:768px) 44vw, 76vw`. Así cargan 960 en celular y no 720 ampliado ×1,23.
4. **`eventos-14f` → `eventos-10-anos` (P073).** Es su favorita de evento, tiene mejor puntaje y se evita confirmar si la chica del reel es clienta o creadora. Si se quiere mantener 14F, confirmar con Carmen y corregir el alt, que hoy dice "manos con uñas…" y la foto muestra una cara.
5. **Póster de `portada-celular`.** Usar el fotograma con el cartelito ALMUD BAR (el inicio del boomerang) como póster y como primer cuadro. Hoy el primer frame visible es solo botellas con etiquetas.
6. **`lugar-cuadros` en ≥1024.** Sigue como miniatura de 313×209 con luz azul flotando sobre «Somos inquietos». Quitarla o cambiarla por `lugar-salon[d]`.
7. **`equipo-eduardo`.** Pedir otra foto o aceptar el borde. Es menor y no mueve la nota.
8. **`comida-cazuela` en celular.** Se lee como "crema" sin la greda negra. Si hay tramo en V052 con el borde de la greda, recortar el boomerang ahí. Es menor.

## Datos

- Videos en 390: `portada-celular-720.webm` de 971 KB (4,15 s, 2 vueltas sin congelamientos), `lugar-cintas-600`, `tragos-humo-720`, `comida-cazuela-720` y `donde-letrero-958`. Todos se conectan por IO al acercarse, todos se reproducen y ninguno se pausa.
- Imágenes: ninguna se repite dentro de una página. `/carta/` vuelve a usar `carta-saguer`/`carta-sangria`, que en la home ahora van solo como lista sin foto. En celular todas cargan un ancho ≥ al necesario, salvo las de El lugar (punto 3).
