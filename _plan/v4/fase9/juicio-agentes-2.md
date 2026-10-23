# Fase 9 · Juicio del panel de agentes, ronda 2 · /nueva_v9/ y /nueva_v9/carta/

**Cómo se revisó.**
- `almudbar.pages.dev` está bloqueado por el proxy de este entorno (403 al CONNECT). Por eso se evaluó la copia local de `public/`, que es la del commit publicado `08be044`, la del paso 10 de `avance.log`. Se sirvió en :8912.
- Playwright con Chromium, a 390×844 (DPR 2, táctil) y 1440×900, en ES y en EN.
- Se probaron la ruleta, el carrusel, la baraja, el slider de fiestas, el Equipo y las reseñas, y además la carta.
- Rúbrica: la misma de `juicio-agentes.md`.
- Las decisiones del dueño no restan:
  - la terraza de día en el cierre;
  - la garzona con la pizza;
  - el video del queso;
  - el tamaño del video de Eventos;
  - los vacíos de color;
  - el «10» en El lugar;
  - los disfraces de Jalogüín;
  - el video propio de Eventos.
- Capturas en `_plan/v4/fase9/agentes2/` (las hojas resumen son `hoja-*.jpg`, y el defecto de las reseñas está en `zoom-resena-comilla.jpg`).

**Datos duros.**
- 0 errores de consola.
- 0 desborde en el inicio y en la carta.
- 0 textos bajo 16 px.
- 13 de 13 videos sin pausa (con los nuevos `portada-celular-b` y `quien-multitud-3-b`).
- Todas las interacciones responden.
- Los 13 nombres y precios coinciden con `carta-v2.json`.
- Largo: 17,0 pantallas en el celular y 16,1 en el escritorio.

## Notas

| Rol | Ronda 1 | Ronda 2 | Meta ≥ 17 |
|---|---|---|---|
| 1 · Voz y textos | 18 | **19** | ✔ |
| 2 · Imágenes y video | 15 | **17** | ✔ |
| 3 · Carta y color | 18 | **19** | ✔ |
| 4 · Entretención y movimiento | 16 | **18** | ✔ |

---

## Lo que mejoró

**Voz**
- «LE ESPERAMOS / DESDE LAS / 18:00 HRS» ya no deja «HRS» solo en una línea, en ES ni en EN.
- Eventos estrena bajada literal: «Se comió, se tomó, se bailó, quedamos con dolor de guata de tanto reír». Está verificada textual en [IG-072], y su glosa EN es natural: "We ate, we drank, we danced, our bellies hurt from laughing so much".
- La carta en EN tiene pestañas claras y el subtítulo en dos líneas.

**Imágenes**
- El rincón «Sillones» por fin muestra los sillones (cuadro de V014).
- La portada del celular usa el corte «-b».
- En Con quién, `quien-multitud-3-b` ya no muestra la botella en la boca del cliente.
- La foto de Fondita llena la ficha sin recorte.

**Carta y color**
- La carta v9 pasa a la paleta nueva: negro único, hoja crema y pestañas con los colores del local.
- Las reseñas rotan los colores de las secciones.
- La herramienta propia reporta 0 textos bajo AA en 2.472.
- El Peter con su precio literal ($ 6.700) es el destacado grande de Tragos.

**Entretención**
- Tragos tiene por fin su WOW: el Peter con humo casi a pantalla completa en el celular y el nombre que se arma letra por letra.
- Las reseñas pasan de texto suelto a tarjetas de color con comilla gigante, que avanzan, se detienen y encajan.
- Eventos tiene bajada.
- Fondita ya no se ve vacía.

---

## Lo que falta, priorizado (sección · elemento · cambio)

1. **Reseñas · comilla gigante · todas las tarjetas, celular y escritorio** (Voz, Entretención).
   - La comilla «❝» se monta sobre la primera línea y tapa las primeras letras: «De los», «Estuve». Se ve en `zoom-resena-comilla.jpg`.
   - Cambio: dar `padding-top` a la cita, unos 0,9 em del alto de la comilla, o sacar la comilla del flujo con `position:absolute; top:-.2em` y un `z-index` debajo del texto.
   - Es el único defecto visible nuevo.
2. **Reseñas · alto de la tarjeta en el celular.**
   - Las citas cortas dejan unos 200 px de color vacío entre el texto y el autor.
   - Cambio: un alto mínimo menor en 390 px, o la cita a 22–24 px cuando tiene menos de 80 caracteres.
3. **Con quién · `con-quien-solo` y `con-quien-risa`** (Imágenes).
   - Siguen siendo primeros planos de una sola persona en la sección de la multitud, y no están entre las excepciones del dueño.
   - Cambio: reemplazarlas por fotos de grupo del corpus o moverlas atrás en la baraja.
4. **Carta en el celular · fila de pestañas en ES** (Carta y color).
   - «CÓCTELES DEL MUNDO MUNDI…» sigue cortado en el borde: el fundido de 40 px atenúa, pero no deja la palabra entera.
   - Cambio: `scroll-snap-align:start` en cada pestaña y `scroll-padding-inline` para que el último elemento visible quede entero, o permitir dos filas a 390 px.
5. **Glosas EN contra `copy-v3`** (Voz).
   - La portada y su meta dicen "good music" y la tabla aprobada dice "lovely music".
   - El rincón dice "LAMPS" y la tabla dice "The lamps".
   - Cambio: alinear una de las dos.
6. **Tragos · el Peter en el escritorio** (Entretención).
   - A 1440 px el video queda en unos 420 px de ancho, centrado y con mucho rosa a los lados. El WOW del celular se diluye.
   - Cambio: llevarlo a unos 60–70 vw, o ponerlo a la izquierda con el título grande a la derecha.
7. **Cuándo y dónde · mapa.** Sin red se ve como un bloque gris. Hay que confirmarlo en línea y, si demora, poner un póster (la puerta o el letrero) hasta que cargue el iframe.
8. **Loops en un dispositivo real.** En Chromium sin pantalla algunos videos se quedan de 2 a 5 s en el último cuadro, y el fundido se ve como doble exposición si la captura cae en la costura. Hay que confirmarlo en un celular, porque no es concluyente aquí.

**No tocar:** la intro, la paleta por sección, la ruleta, la baraja, el slider, el Equipo, el «Le esperamos» que se escribe, los títulos literales y los precios.
