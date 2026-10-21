# Jurado 2 · Diseñador gráfico / director de arte: sitio construido (fase 16)

> Lente: tipografía (Six Caps, cortes, rag, jerarquía, aire), color (campos, tinta, acento), dirección de arte de la imagen (recorte, secuencia, pareo, resolución, repetición), composición por pantalla, y si se lee como **una sola pieza dirigida** hecha con el mundo de afiches de Almud o como plantilla.
> Capturas en `_plan/jurado-2/shots-grafico/`: `landing-1440-vNN`, `landing-1440-offNN` (desfase de 450 px), `landing-390-vNN` (más hojas de contacto `sheet-landing-390-NN`), `landing-1920-v00`, `carta-1440-vNN`, `carta-1440-tab-*`, `carta-390-vNN` (`sheet-carta-390-00`).

## Nota: 7,6 / 10 · Veredicto: **FIX** (correcciones acotadas, no estructurales)

El sistema funciona y se reconoce: suelo noche cálido, un campo plano por pantalla, Six Caps a escala de afiche y la carta en papel con azul y magenta impresos. Lo que la separa de un 9 es dirección de arte de imagen, no tipografía: hay fotos repetidas, un par de fotos blandas en tamaño grande, una foto de apertura que no muestra el lugar y dos o tres pantallas con media página muerta. La carta mezcla tintes pastel que no son del sistema y en teléfono la ahoga una botonera de tres filas.

## Fortalezas (se mantienen)
1. **Portada** (`landing-1440-v00`, `landing-1920-v00`): P189 con el techo de flecos como cielo, el logotipo grande en papel y la mesa riendo abajo. Es la tesis del brief en una imagen. A 1920 el tope de 1440 px con noche a los lados se ve bien, sin costura.
2. **Six Caps a escala de afiche.** "MIÉRCOLES DE / PISCOLEINNNN!", "PA CHUPARSE / EL BIGOTELI", "NO SOMOS NA / SIN USTEDES!", "TIRAR LA CASA / POR LA VENTANA!" y "VENGA VENGA, / LE ESPERAMOS!" tienen cortes limpios en 2 líneas, interlineado apretado y tracking correcto. "MEJOR LOS TOMAMOS TODOS!" en una sola línea de 1.180 px (`off06`) es el mejor momento tipográfico del sitio.
3. **Disciplina de campo.** Turquesa (hoy), amarillo, verde, fucsia y coral nunca comparten pantalla, y cada uno lleva su tinta: noche sobre claros, papel sobre fucsia. El cierre noche con el logotipo gigante (`v25`) firma bien.
4. **Precio de la promo** "$ 4.500" en Six Caps sobre turquesa (`v01`): se lee como afiche y no como tarjeta de producto.
5. **Carta en papel**: los nombres en mayúsculas azul carta y los precios magenta tabulares a la derecha (`carta-1440-v01`) se leen como su menú impreso. Es lo más fiel al material.
6. **Eventos** (`v20`–`v21`): la lista tipo calendario con los años alineados a la derecha y las 4 fotos con desfase sobre coral. Ordenado, festivo y sin ruido.
7. **Acento barra** limitado a nav y CTA; no se filtra a los campos.

## Correcciones priorizadas

### P1 (antes de entregar)
1. **Foto de apertura de El lugar no muestra el lugar.** `landing-1440-v03` / `off03`, banda "El salón", 1440 y 390 (`sheet-landing-390-00`, 4.º panel). El primer plano grande del capítulo es una selfie con aro de luz y celulares: se lee como photobooth de evento o influencer, no como salón.
   - Fix: reemplazar por `lugar-barra-curva` (P093) o `lugar-salon-mimbre` con salón y gente. El aro pasa a mosaico chico o sale.
2. **Repetición de fotos** (rompe la sensación de pieza editada):
   - Garzona con gorra y piscolas: hoy (`v01`), carta/promos (`carta-1440-tab-nuestras`) y la misma persona en la banda Equipo (`v17`).
     Fix: en la banda Equipo la foto se queda; en Hoy y en promos, otra.
   - Cazuela de camarones: mosaico comida (`v11`), adelanto de carta (`v13`) y foto líder de Comilona (`carta-1440-tab-comilona`).
     Fix: dejar una sola por página: en el landing, que el mosaico use P299 (tabla de picoteo) o la pizza; en la carta, que la líder de Comilona sea otra.
   - Bartender sobre muro rosa: apertura de Tragos (`off06`) y foto líder de la carta (`carta-1440-v00`).
     Fix: en la carta usar P362 recortada o P109.
3. **Media pantalla muerta en la apertura de El lugar.** `landing-1440-v02`, 1440. Bajo "NOS GUSTA EL COLORSSSS!" las columnas 8 a 12 quedan vacías 550 px y "Un lugar que fuera cálido, acogedor" flota sola abajo a la derecha.
   - Fix: subir una foto líder 4:5 (P093) a las columnas 8 a 12, alineada con la línea alta del titular, y dejar la frase lead bajo la foto, como en Comida (`v10`).
4. **Carta en teléfono: botonera de 3 filas fija.** `sheet-carta-390-00` / `carta-390-v01..v03`, 390. Se come unos 150 px (18 % del alto) en cada pantalla.
   - Fix: en teléfono, una sola fila con scroll horizontal (`overflow-x:auto`, `scroll-snap`), alto 48 px, y el chip activo en azul carta.

### P2
5. **Tintes pastel en la carta.** `carta-1440-v00..v03` (rosa) y `carta-1440-tab-nuestras` (celeste), 1440 y 390. Son colores que no están en el sistema; junto al papel crema dan dos papeles y un aire de plantilla de restaurante.
   - Fix: todos los paneles van en `--papel` #f6ecdc. Si se quiere diferenciar la pestaña, basta una franja de 8 px del campo de la sección sobre el título.
6. **Fotos blandas a tamaño grande** (en pantallas 2x se nota):
   - mural de ojos a 793 px de ancho con fuente máxima de 960 (`v05`–`v06`), 1440;
   - video del letrero a 720p, oscuro y blando, en banda de 8 columnas (`v23`–`v24`), 1440;
   - `carta-tukulito` existe solo en 480 y se pinta a 327 px (`v13`);
   - `hoy-viernes-mesa` es de 720 ("Sin motivo", `v16`);
   - la hamburguesa (`v11`) es de teléfono, fría y plana frente al resto ámbar.
   - Fix: el mural baja a 4 o 5 columnas, como textura. El letrero pasa a 5 columnas o a banda baja de 21:9 con `brightness(.85)`. Tukulito necesita la exportación de 960 o sale. La hamburguesa se cambia por la pizza en tránsito (P029).
7. **Logotipo de portada sobre el letrero "Cristal".** `landing-1440-v00`, 1440. El guion "Cristal" del fondo se ve a través del isotipo y ensucia el contorno.
   - Fix: mover `object-position` unos 4 % a la izquierda o reforzar el scrim radial solo bajo el isotipo.
8. **Cuándo y dónde: redundancia y vacío.** `v22`–`v24`, 1440. La dirección aparece en la ficha, en el panel "SERRANO 325, CASTRO" y en el pie. El panel noche-alta es la única "tarjeta" de la landing y se ve de plantilla.
   - Fix: quitarlo, dejar "Ver mapa" en la ficha y subir la foto del megáfono para que arranque a la altura del titular.
9. **Promos en la carta.** `carta-1440-tab-nuestras`. Falta Viernes, que sí está en el landing ("Venga venga que nadie le detenga!"), así que la grilla queda 2+2 con un hueco. Sábado no tiene foto y la tarjeta blanca de Miércoles es la única superficie elevada del sitio.
   - Fix: poner los 5 días, cada uno con foto o ninguno con foto, y marcar "Hoy" con el chip, sin tarjeta.
10. **Subcategorías de Comilona.** `carta-1440-tab-comilona`. Hay chips beige y debajo se repite "Picoteos" en Oswald 400, que se lee pobre. El sistema pide categorías en Six Caps head.
   - Fix: basta con el título Six Caps de la subcategoría y chips más sobrios: texto azul subrayado, el activo en noche.

### P3
11. **Nav subrayada.** Todas las capturas, 1440. Los 5 enlaces subrayados a la vez se ven utilitarios.
    - Fix: subrayado solo en hover o en la sección activa.
12. **Hoy, 1440** (`v01`, `off01`): el bloque se dispersa en tres columnas (ítem, párrafo flotante a media altura y foto).
    - Fix: el párrafo debe alinearse con la línea alta del precio, y la semana debe ocupar las 7 columnas de la izquierda.
13. **Portada a 390** (`sheet-landing-390-00`): el logotipo mide unos 200 px y compite con 4 líneas de texto.
    - Fix: llevarlo al 85 % del ancho (unos 330 px) y bajar el bio a small.
14. **Mosaico en teléfono** (`sheet-landing-390-01`, `-04`): los anchos alternan 265, 358 y 173 px con sangrías izquierda y derecha que parecen azar.
    - Fix: usar dos tamaños fijos, 100 % y 66 % alineado a un lado, alternando.
15. **Carta, 1440** (`carta-1440-v01`–`v02`): con miniatura y sin miniatura, la columna de texto queda a 775 px y deja un hueco de 140 px.
    - Fix: las filas sin foto pueden empezar en la columna de la miniatura.

## Resumen
Es una pieza con identidad propia: sus afiches, su letrero y su carta, no una plantilla. Los arreglos P1 son de edición de imagen y de composición de dos pantallas, más la botonera de la carta en teléfono. Con P1 y P2 resueltos, la pieza queda en 8,5–9.
