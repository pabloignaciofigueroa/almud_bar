# Fase 9 · Juicio del panel de agentes · /nueva_v9/ y /nueva/carta/

**Cómo se revisó.**
- Servidor local en :8912 y Playwright con Chromium (/opt/pw-browsers).
- Tamaños: 390×844 (DPR 2, táctil) y 1440×900, en ES y en EN.
- Se recorrió cada sección arriba y abajo.
- Se probaron: la ruleta de rincones (arrastre), el carrusel de tragos, la baraja (lanzar ×2), el slider de fiestas (3 indicadores), la primera tarjeta del Equipo (dar vuelta) y la cinta de reseñas (arrastre).
- Capturas: `_plan/v4/fase9/agentes/` (las hojas resumen son `hoja-*.jpg`). Las costuras de los loops están en `costuras-loops.jpg`.

**Datos duros.**
- 0 errores de consola en las 4 combinaciones.
- 0 desborde horizontal en el inicio y en la carta.
- Ningún texto visible bajo 16 px.
- 13 de 13 videos en loop y sin pausa.
- Largo: 16,3 pantallas en el celular y 15,2 en el escritorio.
- Los 13 destacados con precio coinciden 13/13 con `carta-v2.json` (nombre y precio).
- Contraste del texto por sección:

  | Fondo | Texto | Contraste |
  |---|---|---|
  | Amarillo | negro | 11,97 |
  | Rosa | negro | 5,29 |
  | Naranja | negro | 7,03 |
  | Verde | crema | 5,25 |
  | Lila | negro | 6,58 |
  | Rojo | crema | 4,97 |
  | Crema | negro | 16,32 |

  «Ver la carta» y «Carta» van en negro sobre rosa (5,29).
- Las costuras de los loops calzan: el último cuadro está fundido con el primero, así que no hay salto.
- En Chromium sin pantalla, varios loops se quedan 2 a 5 s en el último cuadro antes de volver a 0. Pasa con los dos servidores probados. Es probable que sea la decodificación por software con 13 videos a la vez, pero no es concluyente: **hay que confirmarlo en un celular real**.
- El mapa de Google sale como un recuadro gris porque este entorno no tiene red. Hay que confirmarlo en línea.

## Notas

| Rol | Nota |
|---|---|
| 1 · Voz y textos | **18 / 20** |
| 2 · Imágenes y video | **15 / 20** |
| 3 · Carta y color | **18 / 20** |
| 4 · Entretención y movimiento | **16 / 20** |

---

## 1 · Voz y textos: 18/20

**Fortalezas**
- Los títulos y las líneas son literales y tienen fuente:
  - del IG: colorssss [IG-111], «Pucha que nos gusta nuestra barrita!», «no dejamos a nadie ajuera», «no somos ná sin ustedes!», «tirar la casa por la ventana!», «Peazo de equipo que tenemos!», los apodos del equipo [IG-067/045/034/014], «usté se lo merece!» y «le esperamos desde las 18:00 hrs»;
  - de la bio: el claim y «Mar a Sáb»;
  - de la carta: los nombres, «Pizzas artesanales» y «Mocktails».
- La ortografía está bien (ná, usté, Jalogüín, Sagüer, Chantá, débil).
- Las reseñas van en su idioma original y con su país.
- El inglés es natural y juguetón: "Restless souls who love colorssss!", "Gosh, we love our little bar!", "One heck of a team!", "Doors open at 6 pm — see you there!".
- La glosa de la carta en EN ya va en su propia línea.
- El texto que se arma letra por letra trae `sr-only` más `aria-hidden`, así que el lector de pantalla lo lee una sola vez.

**Lista priorizada para llegar a 19–20**
1. **Cuándo y dónde · «LE ESPERAMOS DESDE LAS 18:00 HRS» · 390 px.** «HRS» queda huérfano en la tercera línea, en ES y en EN. Hay que forzar el corte «LE ESPERAMOS / DESDE LAS / 18:00 HRS», con `white-space:nowrap` en «18:00 hrs». La v3 ya lo había resuelto.
2. **Cuándo y dónde · orden de lectura.**
   - Hoy «USTÉ SE LO MERECE!» es el título de Cuándo y dónde. En el celular va antes de «Le esperamos» y en el escritorio queda abajo a la izquierda, debajo del video, después de los datos.
   - El plan de la fase 8 lo pone en el Pie, a pantalla completa.
   - Hay que moverlo al pie (o dejarlo como cierre de la sección, después del mapa) para que la sección empiece con «Le esperamos desde las 18:00 hrs».
3. **El lugar · rincón «Sillones» / "Lounge".**
   - No tiene línea propia, y la foto es una mujer riendo y no los sillones.
   - `copy-v3` dice que el nombre va solo si la foto muestra los sillones.
   - Hay que cambiar la foto por una de sillones o sacar el rincón.
4. **Glosas EN contra `copy-v3`.** La portada dice "good music" donde la tabla aprobada dice "lovely music", y Rincón dice "LAMPS" donde la tabla dice "The lamps". Hay que alinear una de las dos, la página o `copy-v3`, para que el verificador no lo vuelva a marcar.
5. **Carta en el celular · fila de pestañas.** «SPIRITS» / «ESPIRITUOSOS» sigue cortado en el borde (es el P2 pendiente de la ronda 2). Falta el desvanecido de unos 40 px o el `scroll-snap-align:start`.

## 2 · Imágenes y video: 15/20

**Fortalezas**
- La portada es la terraza techada repleta en el celular y el video institucional en el escritorio, sin una persona como protagonista.
- La multitud manda en El lugar, Con quién y Eventos.
- Los loops duran de 8 a 9,2 s, van hacia adelante y tienen el fundido bien hecho (hoja `costuras-loops.jpg`).
- Las fotos se ven nítidas: se sirve el srcset de 2× en el celular.
- No se vio ningún recorte forzado que corte caras.
- El video de los dueños va en 9:16 y el de la terraza en 1:1.

**Lista priorizada para llegar a 18 o más**
1. **Comida · foto grande (`comida-pizza`, la garzona con la pizza).**
   - Es un primer plano de una sola persona fuera de Equipo, y ella no aparece en las tarjetas.
   - El plato casi no se ve: en el celular la pizza queda en el 15 % inferior.
   - En el escritorio la etiqueta «Pizzas artesanales» queda lejos de la foto.
   - Hay que cambiarla por una pizza sola, o por una mesa con platos, o recortar a la pizza sin la cara. **(−1,5)**
2. **Cuándo y dónde · video `donde-terraza`.** Muestra clientes en primer plano: una joven de rojo que toma con bombilla (celular) y una pareja mayor en la mesa del frente (escritorio). Hay que elegir un tramo de V007 con la terraza y Castro de fondo y gente lejana, o reencuadrar el 1:1 hacia el paisaje. **(−1)**
3. **Con quién · primeros planos individuales.**
   - Están `con-quien-solo` (hombre solo en la barra), «Una mujer ríe a carcajadas…» y los cuadros de `quien-multitud-1` donde llena el encuadre una sola persona (un garzón con bandeja y una mujer con copa).
   - Hay que reemplazarlos por fotos de grupo del mismo corpus (P196, P185 y P359 ya están aprobadas), y en `quien-multitud-1` elegir un tramo donde se vea una mesa o un grupo. **(−1)**
4. **Eventos · Jalogüín.** Las dos piezas son individuales: un hombre con disfraz rosado en video y la catrina. Hay que sumar o cambiar a un plano de grupo disfrazado (el alt del video ya lo promete: «mesas llenas de gente disfrazada»). **(−0,5)**
5. **Comida · `comida-queso` dura 7,33 s**, bajo la regla de 8 a 10 s. Hay que extender el tramo o cortar otro de 8 s o más. **(−0,5)**
6. **El lugar · video `lugar-noche`.** Arranca bajo el «10» de flores, que el cliente sacó por falta de contexto (decisión #29). Hay que iniciar el loop en el tramo de la terraza o de la barra. **(−0,5)**
7. **Verificar en un celular real** que los 13 loops no se quedan en el último cuadro. En las pruebas sin pantalla, el de la coctelera y el de la portada de escritorio se detienen de 3 a 5 s.

## 3 · Carta y color: 18/20

**Fortalezas**
- 13 de 13 nombres y precios coinciden con `carta-v2.json`:
  - Peter 6.700, Sagüer 7.900, Sangría 6.500, Olvidar 6.800, Coquette 7.100 y Moto 6.400;
  - Tukulito 15.900, Carne 11.900, Cosa poca 11.900, Todo que ver 16.000, Con tuti 19.900, Chambreao 10.900 y Camarón 15.900.
- Las glosas EN son fieles a la carta (tataki, ceviche de atún rojo, "Chilean-style baked cheese fondue").
- Cada sección tiene un solo color del local: amarillo, rosa, naranja, verde, lila, rojo, crema y negro.
- Todo el texto medido queda en 4,5:1 o más.
- La única llamada de acción es «Ver la carta completa», a la derecha y en negro.

**Lista priorizada para llegar a 19–20**
1. **Comida · los dos videos con rótulo** («La carne es débil» y «Una cosa poca»).
   - En 390 px miden 113×141 px y el nombre se lee apretado en dos líneas.
   - Hay que darles media columna cada uno (2 + 1 en vez de 3 en fila), o pasar «Tukulito Sakayama» a la grilla de abajo.
2. **Carta · fila de pestañas y chips en el celular.** Lo mismo que el punto 5 de Voz: el último elemento visible queda cortado.
3. **Carta · paleta.** Sigue con el negro y el rosa pálido con nombres en azul violeta. Está previsto para la fase 10, pero conviene adelantar al menos el rosa del botón y el negro único, para que el salto entre el inicio y la carta no se note.
4. **Equipo · rojo con crema, 4,97:1.** Pasa justo. Si se agrega texto chico (16 px) en el dorso, conviene oscurecer el rojo a #b51d27 para tener margen.

## 4 · Entretención y movimiento: 16/20

**Fortalezas**
- Cada sección tiene su juego, y todos funcionaron en las pruebas: la intro del almud, la ruleta con balanceo, el carrusel de tragos, la baraja infinita, el slider de fiestas con sus nombres gigantes, las tarjetas que se dan vuelta, las cintas de reseñas y el «Le esperamos» que se escribe.
- Nada va atado al scroll.
- Se siente como su feed: color pleno, gente, fiesta.
- Dan ganas de ir.

**Lista priorizada para llegar a 18 o más**
1. **Reseñas.** Es la sección más plana.
   - Es texto suelto entre filetes, sin tarjeta y sin estrellas, y en 1440 px el texto se ve chico y gris.
   - Hay que darle a cada reseña una tarjeta de color (los colores de las secciones, rotando) con una comilla gigante y la cita a 20–22 px.
   - Que la bandera sea más grande.
   - Agregar un leve giro al arrastrar, igual que en la ruleta. **(+1)**
2. **Eventos · diapositiva de Fondita** (y Jalogüín en el escritorio). Tienen una sola foto (o dos individuales) y queda un gran vacío lila. Hay que sumar 2 o 3 fotos por fiesta, del corpus de [IG-080] y [IG-072], para que «se repartan» como en Aniversario. **(+0,5)**
3. **Pie · «USTÉ SE LO MERECE!».** No llena la pantalla y el brindis de los almudes no se vio en las capturas. Hay que llevarlo al pie a 100 svh, con el brindis visible al llegar (ver el punto 2 de Voz). **(+0,5)**
4. **Cuándo y dónde · mapa.** Mientras carga (o si no hay red) es un bloque gris grande. Hay que poner como póster una foto de la fachada o del letrero hasta que cargue el iframe, o reducir el mapa a un botón. **(+0,5)**
5. **Comida · el WOW** (los platos que entran girando y «más que sabrosona!» que late) se pierde porque los videos son diminutos. Con el cambio del punto 1 de Carta y color también sube el ritmo.

**No tocar:** la intro, los colores por sección, la ruleta, la baraja, el slider, el carrusel de tragos, los títulos literales y los precios.
