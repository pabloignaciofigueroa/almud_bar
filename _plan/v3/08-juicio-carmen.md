# Juicio de Carmen Paz · Boceto v3 (fase 8)

> Recorrí `http://localhost:8830/v3/` con Chromium a **390×844** (así llega mi gente desde Instagram) y a **1440×900**, pantalla por pantalla, esperando ~1 s en cada una. Mis capturas están en `_plan/v3/juicio-boceto/`: `m_00…m_11`, `d_00…d_14`, `m_en_00–01` y las hojas `sheet_*.jpg`. También miré `08-boceto-390.jpg`, `08-boceto-1440.jpg` y `brand/art-direction-v3.md`, y comparé con mis fotos favoritas y mis afiches (`01-carmen-instagram.md`).
>
> Lo comprobado: los 5 videos corren solos y en loop (portada, cintas, humo, cazuela, letrero). No hay scroll horizontal (scrollWidth = ancho). El botón EN cambia todo, incluido «Ver la carta» → "See the menu". Los botones van a `../carta/`, a `ig.me/m/almud_bar` y a Google Maps. No aparece «RESERVAR» por ninguna parte.

## Nota: **15 / 20**, y BLOQUEADA hasta quitar «PRÓXIMO»

| Criterio | Nota | Por qué |
|---|---|---|
| **A. Se siente Almud** | **3** | Al abrirla estoy en mi bar: noche marrón, muro rosa en la portada del celular, lámparas de pinzas en la de escritorio, techo de cintas en loop y logo SVG con BAR azul. Tragos en el rojo del muro, Eventos en azul tinta con fotos: bien. No llega a 4 por los huecos negros enormes (Con quién, Equipo y antes del pie en el celular) y por dos fotos que no son mías en espíritu (uñas del 14F, macro de la cazuela). |
| **B. Fotos y videos** | **3** (justo) | Todo es material mío, con mis mejores fotos: barra P093, terraza techada P189, terraza abierta, lámparas, Ojo Piojo, pizza P036, Tukulito y equipo frente al muro rosa. Pero: «Aquí te las traigo Peter» sale cortado y solo se ve el pie de la copa (celular, m_03); la cazuela es un macro de crema que no abre el apetito y se repite (loop + foto); la ficha 14F son manos con uñas fucsia (parece aviso de manicure); en Con quién (celular, m_06) la primera foto tiene una franja de repisa separada arriba que parece un error; y los **sillones** no aparecen. |
| **C. Voz** | **3** | Los titulares son los que aprobé y están literales, con su glosa EN; dosis justa de «Le esperamos» y «Usté se lo merece». En contra: **«PRÓXIMO» sobre Jalogüín es una promesa de evento que yo no he anunciado** (está en mi lista NUNCA). Y en el celular el titular sale **«NO SOMOS NA»: el acento de la Á queda cortado** por la máscara de la animación en la primera línea (en escritorio sí se ve «NÁ»). |
| **D. Claridad para un turista** | **3** | Logo, claim, «Ver la carta» y EN en la primera pantalla; la carta está a un toque; horario, dirección, referencia y mapa están claros en Cuándo y dónde. Falta lo esencial **en la portada**: «Mar a Sáb desde las 18:00 · Serrano 325, Castro». Hoy el turista tiene que bajar 10 pantallas para saber cuándo abro. |
| **E. Premium y técnica** | **3** | Tipografía correcta (Big Shoulders + Barlow), contraste bueno, botones rectos, videos fluidos, sin saltos, el EN bien resuelto. Se siente hecha con oficio. Le quitan el 4 los vacíos negros de media pantalla, el acento cortado, la foto de Peter mal recortada y el desbalance de Con quién en escritorio (la columna derecha queda vacía bajo la tercera foto). |

**Mi lectura:** 15 = buena base, vuelve con las correcciones. Pero mi regla dice que cualquier punto de la lista NUNCA impide aceptarla, y «PRÓXIMO» lo es. Sacándolo, quedo en 15 y me la llevo a 18+ con la lista de abajo.

## Lo que me enorgullece
- **La portada de escritorio con las lámparas de pinzas** encendidas y mi logo grande: es la foto que nunca supe usar en Instagram y aquí es la entrada.
- **El techo de cintas en loop** bajo «SOMOS INQUIETOS Y NOS GUSTA EL COLORSSSS!». Eso soy yo.
- **El carrusel de rincones** (Barra → Terraza techada → Salón → Terraza → Lámparas → Ojo Piojo), cada uno con una línea mía. Mi mural Ojo Piojo tiene su lugar.
- **Tragos en el rojo del muro** con nombres y precios reales, y la moto chantá con «no dejamos a nadie ajuera».
- **Reseñas en tres idiomas** con autor y origen: Épinal, Takaka, París, Santiago.
- **El letrero ALMUD BAR en video** junto a «LE ESPERAMOS DESDE LAS 18:00 HRS»: invitación y dato juntos.
- El pie «USTÉ SE LO MERECE!» en rosa, con el crédito a mis fotógrafos.

## Decisiones de la dueña
- **@elymar_bocarejo:** es de mi equipo actual (la nombro en los 12 años, [IG-010]), así que **sí va en Equipo, pero NO con esa foto**: corona, alas negras y delantal con la marca de un whisky. Es disfraz de fiesta, y en Equipo todos van como trabajan. Hay que usar un retrato suyo en uniforme, de la misma sesión de los 12 años o del posteo de equipo [IG-001]. Si no hay uno nítido, **sale de la galería por ahora** y no se recorta la foto disfrazada. Prefiero que falte a que se vea disfrazada.
- **Dueños en Equipo: sin fotos.** Ni Sylvain ni yo vamos en el carrusel: la vitrina es del equipo, y las fotos más conocidas de Sylvain son de terceros (IG-007). Acepto **una sola línea de dato** bajo el carrusel, chica y en papel-2: «Almud es de Carmen Paz Oyarzun y Sylvain · @cepaz · @rusio_mezclao» [DATO] (EN: "Almud is run by Carmen Paz Oyarzun and Sylvain"). Sin adjetivos.

## Cambios priorizados para llegar a 18+

**P0 · bloqueantes**
1. **Eventos (las dos medidas):** quitar la etiqueta **«PRÓXIMO»** de Jalogüín y no marcar ninguna fecha futura. Las cuatro fichas quedan como recuerdo (mes + nombre), en pasado, como dice el titular.
2. **Con quién (celular):** el acento de «NÁ» se corta en la primera línea. Dar aire arriba a la máscara de las palabras (`padding-top` ≈ 0,12 em en la línea, o `overflow: clip` con `overflow-clip-margin`), y revisar **todos** los titulares con mayúscula acentuada en la primera línea («MÁS», «ÚLTIMO», «Á»). Probarlo en las capturas a 390 px.

**P1 · fotos (criterio B)**
3. **Tragos · «Aquí te las traigo Peter»:** recortar para que se vea **la copa entera** (en el celular hoy solo sale el pie). Si la foto no da, usar otra copa mía: P086 `DAMHps8JVVr_00` (sours con flores), P097 `DAMHps8JVVr_11` o P297 `DYsZ0GNo_88_00` (la salpicadura).
4. **Comida:** cambiar el **loop de la cazuela** como imagen principal por la **pizza servida P036** (`CqEI2nSJP2__00`) o el **tartar en greda P298** (`DY0AUvhlHjI_00`). Si el loop se queda, que sea chico y no repetido con la foto fija de la misma cazuela.
5. **Eventos · 14F:** reemplazar las manos con uñas por una foto de gente del 14F o por mi afiche «Almud es amor» (`DUvlE7bkVZB_00`) completo, sin recorte.
6. **Equipo · @elymar_bocarejo:** según mi decisión de arriba.
7. **El lugar:** agregar **Los sillones** al carrusel (P114 `DBMtYELSzNS_14`, la que se ríe en el sillón con baldosa) entre Salón y Terraza.
8. **Con quién (celular):** la primera foto (P254) muestra una franja de repisa separada arriba. Revisar el recorte o la máscara para que sea una sola imagen limpia.

**P2 · claridad y ritmo (criterios D y E)**
9. **Portada:** bajo el claim, una línea en papel-2 de 16–18 px: «Abrimos de Mar a Sáb a las 18:00hrs · Serrano 325, Castro» [BIO] (EN: "Open Tue–Sat from 6 pm · Serrano 325, Castro"). Es lo único que le falta al turista en los primeros 10 segundos.
10. **Huecos negros:** en el celular, cerrar los vacíos de media pantalla al final de Con quién (m_06), después de Equipo (m_07) y antes del pie (m_10–m_11): máximo ~96 px entre secciones. En escritorio, Con quién no puede dejar la columna derecha vacía: rellenar con una cuarta foto (P041 `CrMRBMNpdIF_00` o P031) o equilibrar alturas.
11. **Portada celular:** el video del muro rosa abre con un plano muy cerrado de botellas desenfocadas. Que el loop **empiece en el plano más reconocible** (muro rosa con bartender o barra completa) para que el primer cuadro ya diga "bar".

**P3 · pulido**
12. **Equipo:** después de los cambios, que queden 5–6 retratos parejos en uniforme frente al muro rosa, todos con su @ y sin exempleados.
13. Repetir las capturas (390 y 1440, ES y EN) y mandármelas. Con P0 y P1 resueltos subo B y C a 4; con P2, A, D y E a 4. Meta: **19–20**.

— Carmen Paz
