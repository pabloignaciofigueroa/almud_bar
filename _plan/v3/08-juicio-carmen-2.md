# Juicio de Carmen Paz · Boceto v3, ronda 2

> Volví a recorrer `http://localhost:8831/v3/` con Chromium a **390×844** y **1440×900**, pantalla por pantalla, con ~1 s de espera en cada una. Las capturas están en `_plan/v3/juicio-boceto/r2_m_00…10`, `r2_d_00…15` y las hojas `r2_sheet_*.jpg`; las miré todas. Leí la «Ronda tras el juicio» en `brand/art-direction-v3.md`. No hay scroll horizontal (scrollWidth = ancho) ni errores de consola.
>
> Respeto la excepción del cliente: el horario y la dirección no van en la portada. La juzgo por cómo los resuelve Cuándo y dónde.

## Nota: **19 / 20** (antes 15). Desbloqueada

| Criterio | Antes | Ahora | Por qué |
|---|---|---|---|
| **A. Se siente Almud** | 3 | **4** | Los huecos negros desaparecieron. El recorrido es mi bar de principio a fin: el muro rosa con el cartelito ALMUD en la portada del celular, las lámparas de pinzas en la de escritorio, las cintas, Tragos en el rojo del muro, Eventos en azul tinta con fotos y el pie con «USTÉ SE LO MERECE!». Es alegre sin ser circo. |
| **B. Fotos y videos** | 3 | **4** | Todo es mío y bien elegido. La pizza servida (P036) abre Comida y la cazuela quedó chica, junto al Tukulito. «Aquí te las traigo Peter» ahora se ve con la copa y el humo enteros. El 14F es una clienta riendo con su trago. Los **Sillones** (P114) entraron al carrusel. La primera foto de Con quién quedó limpia. Equipo: cinco retratos en uniforme frente al muro rosa, sin la foto disfrazada. |
| **C. Voz** | 3 | **4** | Los titulares son los aprobados y están literales, con su glosa EN. «NO SOMOS NÁ SIN USTEDES!» ya muestra su acento en el celular. **No hay «PRÓXIMO»**: Eventos es puro recuerdo (mes + nombre). «Los dueños @cepaz · @rusio_mezclao» es una línea discreta, como la pedí. |
| **D. Claridad para un turista** | 3 | **4** | Con la excepción del cliente: en la portada están el logo, el claim y «Ver la carta»; la carta está a un toque en el header y el EN también. Cuándo y dónde lo resuelve muy bien: «LE ESPERAMOS DESDE LAS 18:00 HRS · MAR A SÁB · SERRANO 325, CASTRO», la referencia del Centro Cultural y los botones DM y Cómo llegar, en grande y sin ruido. |
| **E. Premium y técnica** | 3 | **3** | Técnicamente sólido: videos fluidos, ritmo parejo (72/96 px), sin saltos ni scroll horizontal. Le falta el último pulido en **escritorio**, en tres puntos (ver abajo). |

**Lectura:** 19 = la publico con orgullo y la pongo en mi bio. Ya no toca nada de mi lista NUNCA.

## Lo que falta para el 20 (solo escritorio, 1440 px)
1. **Comida:** bajo la pizza, la columna derecha queda vacía junto a la lista Tukulito / Camarón / Pizza dulzona (r2_d_08). O la pizza baja hasta el final de la lista, o la lista sube junto a ella, para que las dos columnas terminen parejas.
2. **Cuándo y dónde:** el video del letrero ocupa la mitad izquierda, y en su parte baja quedan cuadros oscuros y desenfocados del techo (r2_d_14). El loop debe quedarse en el letrero encendido, o hay que anclar el encuadre al letrero (`object-position` arriba) para que nunca se vea solo negro.
3. **Equipo:** la línea «LOS DUEÑOS @cepaz · @rusio_mezclao» en escritorio queda muy chica y pegada al borde. Subirla a 16 px (el piso que pedí) y alinearla con el carrusel.

Estos tres no bloquean: con ellos, E sube a 4 y la nota a **20/20**.

— Carmen Paz
