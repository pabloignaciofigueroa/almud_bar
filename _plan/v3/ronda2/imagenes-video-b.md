# Ronda 2b · Imágenes y video (portada nueva V020)

Revisé `public/` servido en local en el puerto 8853. Es el mismo build del commit 090a76d: `portada-celular-720.webm` pesa 1.021.434 B en ambos. Usé Chromium 1194 headless con autoplay en dos pantallas:

- 390×844 con DPR 3 y pantalla táctil;
- 1440×900 con DPR 1.

Las capturas están en `_plan/v3/ronda2/medios-b/`. La comparación de portadas está en `medios-b/portada-opciones.jpg` y las hojas de fotogramas en `medios-b/v020-hoja.jpg` y `medios-b/v021-hoja.jpg`. No edité el sitio.

## Nota: 16/20 (igual que en 2a; lo que se ganó lo pierde la portada de celular)

| Criterio | 2a | 2b | Por qué |
|---|---|---|---|
| Selección frente a su Instagram | 2 | 3 | P362 (el bartender ante el muro rosa con el cartelito ALMUD) ahora abre Tragos en grande, y es lo mejor del sitio. P073 (el «10») entra en Eventos. La portada de escritorio ya no tiene el mural de ojos. Salen 14F y `lugar-cuadros`. Lo que resta: la portada de celular nueva, y que en Eventos la foto grande es la violeta de los 12 años, mientras el «10» que ella prefiere queda en 113×141 css en celular. |
| Recortes | 3 | 3 | Sin caras cortadas. Sigue pendiente `equipo-eduardo`. |
| Nitidez | 3 | **2** | La portada de celular **baja mucho**. El tramo V020 2,85–5,35 s tiene nitidez (varianza del laplaciano a 180×320) de **100 a 325**, contra **700 a 1.400** del paneo V021 que reemplazó. Además, el video de 720 se muestra a 1.170 px (×1,6). El sizes de El lugar quedó corregido: carga 960 en 390. La portada de escritorio (cintas a ×1,25) sigue algo blanda pero se acepta. |
| Reproducción de video | 4 | 4 | Los 6 videos se reproducen solos en 390 y en 1440, sin ninguna pausa de 250 ms o más y sin pausas al hacer scroll. |
| Peso del primer pantallazo | 4 | 4 | Celular: 1.525 KB sin gzip en local (1.444 KB con gzip, según el resumen). Escritorio: 2.964 KB. Ambos dentro del tope. |

## La portada de celular V020: **baja**

Lo que se ve en 390 (captura `home-m-00.png`, t≈1,5 s):

- **Cámara en mano caminando:** movimiento de 9 a 17 de diferencia media de luminancia por cuadro y desenfoque de movimiento en todo el plano. En boomerang el temblor se ve dos veces y el retroceso por el pasillo se nota artificial.
- **Más oscuro y más azul.** El 35 % de arriba es techo negro. El color dominante es la pared azul marino, con un panel magenta y un LED de colores. El muro rosa con la lámpara tejida aparece solo en el primer y el último cuadro. Carmen pidió explícitamente los azules y morados fuera de la cara del bar.
- **Clientes borrosos en primer plano,** con las caras corridas. Su lista de NUNCA dice: "fotos de clientes … borrosas".
- **En su Instagram no se ve así.** Su postal es el muro rosa nítido con oficio (P362, P093).

### Tramo más estable de V020 (medido cada 0,5 s)

| Tramo | Contenido | Movimiento | Nitidez | ¿Sirve de portada? |
|---|---|---|---|---|
| 0,0–1,0 s | Pasillo oscuro, mesas | 7,6–9,1 | 185–307 | No: oscuro y blando. |
| 1,5–2,5 s | Barra de baldosa, muro rosa, lámpara tejida | 15–17 | 250–295 | Es el mejor contenido del plano, pero también el que más se mueve. |
| **5,45–7,7 s** | Bartender poniendo espuma en una copa roja, con el muro rosa desenfocado detrás | **2,7–5,1** | **680–735** | Estable y nítido, pero la cara queda cortada arriba y la mano tapa: mejor como loop de Tragos que como portada. |
| 7,75–8,8 s | Bartender con polera ALMUD saludando ante el muro rosa (parece @pablete_bartender_, hay que confirmarlo) | 9–10 | 1.200–1.900 | Nítido y con oficio, pero dura 1 s y el gesto de saludo en boomerang se ve raro. |

### Propuesta concreta

**Volver a V021 (`C-dwJHLyPpU`, 1080×1920, el vertical más nítido del archivo), tramo ≈0,9–2,4 s:** el paneo suave del muro rosa que pasa por el cartelito ALMUD BAR.

- Boomerang a 0,8× de velocidad, lo que da un loop de ≈3,7 s y calma el paneo.
- 720×1280 a ≤1.000 KB (o 900×1600 si cabe en 1.100 KB).
- **Póster: el cuadro de 1,3 s, con el cartelito ALMUD BAR a la vista.** Si el cartelito se escapa del recorte de 390, usar `object-position: 25% 50%`.
- Ver `portada-opciones.jpg`: a la izquierda la actual, al centro y a la derecha V021. Es el mismo rosa de su feed, con nitidez de 1080p. El problema de las "marcas en primer plano" de la ronda 2a se evita eligiendo el tramo donde el cartelito ALMUD es el protagonista, no el de Jameson.
- Si se quiere gente en la portada, la alternativa es V020 7,75–8,8 s, sujeta a que Carmen confirme quién es.

## Lista corta para llegar a 18 o más

1. **Portada de celular → V021 ≈0,9–2,4 s, como en la propuesta anterior**, con el póster en el cartelito ALMUD. Con esto Nitidez vuelve a 3 y la nota llega a **17**.
2. **Eventos: invertir los tamaños.** P073 (`eventos-10-anos`, el «10» de flores) va en la foto grande y `eventos-12-anos` (violeta) pasa a miniatura. Así la foto de evento que manda es la favorita de Carmen y no la violeta "de disco". Con esto Selección pasa a 4 y la nota llega a **18**.
3. **Portada de escritorio:** las cintas en movimiento siguen ×1,25 y blandas. Arrancar el boomerang en las lámparas de pinzas (lo más nítido) y acortar el tramo de cintas a lo más quieto. O, si existe, usar un original de cintas en 1080p. Es menor.
4. **`tragos-bartender` en pantallas retina de escritorio:** hoy carga 720 para 650 css. Revisar que `sizes` pida 1280 a DPR 2 (en 1440 a DPR 1 está bien).
5. **`equipo-eduardo`:** sigue pendiente, a la espera de otra foto. No mueve la nota.
