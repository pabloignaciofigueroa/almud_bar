# Ronda 2c · Imágenes y video (commit 11c0784)

Revisé `public/` servido en local (puerto 8854; `portada-celular-720.webm` = 900.812 B, el del build) con Chromium 1194 headless y autoplay, en dos pantallas:

- **Celular:** 390×844, DPR 3, táctil.
- **Escritorio:** 1440×900, DPR 1.

Capturas, JSON y fotogramas están en `_plan/v3/ronda2/medios-c/`. No edité el sitio.

## Nota: **18/20** (2b: 16)

| Criterio | 2b | 2c | Por qué |
|---|---|---|---|
| Selección frente a su Instagram | 3 | **4** | La portada de celular vuelve al muro rosa de su feed, con el cartelito ALMUD BAR y sin botellas con marca dominando. P362 abre Tragos en grande. P073 (el «10» de flores) es ahora la foto mayor de Eventos y se ve completo en el recorte de celular (`el-ev10-m.png`). P189 y P093 siguen en El lugar. Cada trago lleva su foto con el nombre literal. Ya no hay nada violeta como protagonista. |
| Recortes | 3 | 3 | No hay caras cortadas. P362 (4:5) y el «10» (16:10, `object-position: 50% 40%`) quedan bien encuadrados. Sigue pendiente `equipo-eduardo`: el jockey toca el borde, problema de la foto original. |
| Nitidez | 2 | **3** | Medí la nitidez de la portada de celular sobre el archivo publicado a 180×320 (varianza del laplaciano): mínimo 308, mediana 503. La V020 rondaba 100 a 325. Ya no hay desenfoque de cámara en mano, solo algo de desenfoque de paneo en el centro del boomerang. Las fotos cargan el ancho que necesitan, con dos excepciones que restan: la portada de escritorio sigue a 1278 px estirada ×1,25 y las cintas se ven blandas; `lugar-salon[m]` sale ×1,25 en celular porque su tope es 712 px. |
| Reproducción de video | 4 | 4 | Los 6 videos se reproducen solos en 390 y 1440, con 0 pausas ≥250 ms en 16 s por video y 0 pausas por scroll. Portada de celular: 3,7 s, costura 14,7, del orden de un paso entre cuadros (12,6): no hay salto. |
| Peso del primer pantallazo | 4 | 4 | Sin scroll: 1.417 KB en celular (sin gzip, en local) y 2.856 KB en escritorio. |

## Portada de celular V021: **sube**

El paneo es el mismo rosa de su postal, nítido, y el cartelito ALMUD BAR pasa por el centro del recorte de 390 (`frames-celular.jpg`). Detalle menor: en t≈1,5 s el cartelito queda a la altura del velo y del logotipo grande, así que se ve oscurecido y compite con él. No baja la nota.

## Lo mínimo para mantener 18 o subir a 19

1. **`equipo-eduardo`.** Pedir a Carmen otro retrato de @eduu.ardoo o recortar con margen arriba desde un original mayor. Es lo único que impide el 4 en Recortes.
2. **Portada de escritorio.** Que el boomerang pase menos tiempo en las cintas (lo más blando a ×1,25) y más en las lámparas de pinzas, que se ven nítidas. O, en ≥1440, mostrar la variante con un velo más denso en la zona de cintas.
3. **P297 (splash) y P086 (sours).** Salieron de Tragos porque sus captions no traen nombre. Son dos de las favoritas que Carmen nombra. Sin inventar nombres, pueden volver donde no se requiere nombre de trago: el encabezado de `/carta/` o el og:image de la carta. Opcional, no resta nota.
4. **Menor:** `lugar-salon[m]` sale ×1,25 en celular. Si molesta, usar `lugar-salon[d]` (1280) con `object-position` en vez del recorte 4:5 de 712.
