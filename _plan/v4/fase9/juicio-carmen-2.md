# Juicio de Carmen Paz · ronda 2 · /nueva_v9/ y /nueva_v9/carta/

> **Desde dónde miré.**
> - El proxy de este entorno bloquea `almudbar.pages.dev` (CONNECT 403), así que no pude abrir el sitio en línea.
> - Evalué el build local `public/nueva_v9/` y `public/nueva_v9/carta/` del commit `08be044` («correcciones aplicadas y publicadas en /nueva_v9/ y /nueva_v9/carta/»), servido en `http://localhost:8912`.
> - **Falta confirmar en línea** que lo publicado es este mismo build y que el mapa carga.
>
> **Cómo lo recorrí.**
> - Chromium (Playwright) a **390×844**, **1440×900** y **1920×1080**, en **ES** y **EN**.
> - Intro capturada a 0,15 / 0,7 / 1,5 / 3,2 s, y scroll con rueda de a 85 % de pantalla, con 1,3 s de espera por parada.
> - Interacciones en ES, a 390 y a 1440:
>   - ruleta de rincones;
>   - carrusel de tragos;
>   - 3 lanzamientos de la baraja;
>   - slider de fiestas, a mano y en avance solo;
>   - giro de una tarjeta del equipo;
>   - arrastre de las reseñas;
>   - cierre.
>
> **Capturas en `_plan/v4/fase9/carmen2/`:**
> - `{m|d|w}_{es|en}_home_sNN`;
> - `*_intro_*`;
> - `*_x_*` (interacciones);
> - `*_carta_sNN`;
> - `*_full`;
> - `report.json`.
>
> **Lo comprobado (12 combinaciones).**
> - **0 errores de JS** y **ningún scroll horizontal**.
> - **0 textos bajo 16 px**, también en la carta.
> - **13/13 videos en play**, mudos y en loop.
> - Todas las fotos llevan `alt`.
> - **Un aviso que no cuento:** un 404 suelto de `eventos-primavera-a-480.avif` en 1440 ES. El archivo existe y está en git, así que fue un tropiezo del servidor local, que se cayó durante la primera pasada.
>
> **Descartados a propósito por el dueño (no restan):**
> - la terraza de día en el cierre;
> - la garzona con pizza;
> - el video del queso;
> - el tamaño del video de Eventos;
> - los vacíos de color;
> - el «10» de El lugar;
> - los disfraces de Jalogüín.

## Nota: **19 / 20** (antes 18) · Entretención **4 / 4** (antes 3)

| Criterio | Antes | Ahora | Por qué, en mi voz |
|---|---|---|---|
| **A. Se siente Almud** | 4 | **4** | Sigue siendo mi bar: el almud que se abre, el color de la casa por sección y nada de circo. En 1920 la portada a sangre con mi mural Ojo Piojo y las cintas se ve grande y mía. |
| **B. Fotos y videos** | 3 | **4** | Ya no está el cliente con la botella en la boca: `quien-multitud-3-b` lo salta. Lo demás que pedí lo descartó el dueño y no lo cuento. Los Sillones por fin muestran mis sillones: capitoné, mesitas redondas y espejo. Abrir Tragos con el Peter grande y su burbuja de humo es mi foto de revista en movimiento. |
| **C. Voz** | 4 | **4** | Todo es literal. La bajada nueva de Eventos es mía y me hace reír: «Se comió, se tomó, se bailó, quedamos con dolor de guata de tanto reír» [IG-072]. |
| **D. Claridad turista** | 4 | **4** | Sin cambios: Carta rosa fija, EN, datos grandes al cierre, glosas EN en el inicio y en la carta. El mapa sigue sin poder verificarse aquí (sin red). |
| **E. Premium y técnica** | 3 | **3** | Ya no chocan los títulos: las «ssss» se estiran solo a lo ancho y «sabrosona!» late sin tocar «PERO MÁS». La carta quedó como pedí: paleta nueva, hoja centrada a 1440 y 1920, pestañas con los colores del local y nada bajo 16 px. **Pero apareció un choque nuevo:** en las reseñas, la **comilla gigante se monta sobre la primera línea** en algunas tarjetas («**De** los mejores bares…» de Oscar y «**Estuve** ahí cada día…» de aroggodoy). Pasa en celular (`m_es_home_x_resenas0.jpg`) y en escritorio (`w_es_home_s14.jpg`, `d_es_home_s14.jpg`). Es justo el tipo de detalle que me quitó el punto la vez pasada. |

**Lectura:** 19 = la publico con orgullo y la pongo en mi bio. Con la comilla arreglada, es un 20.

### Entretención: **4 / 4**
- **Tragos ya tiene su WOW.** El Peter con su humo casi a pantalla completa, con «Aquí te las traigo Peter» armándose letra por letra y su precio. Después siguen las columnas y el carrusel.
- **Las reseñas ahora son fiesta.** Son tarjetas de colores de la casa, con comilla gigante y la cita entera, que se detienen para leerlas y corren en sentidos contrarios. Ya no leo frases cortadas.
- **Eventos hace reír** con la frase del dolor de guata, y el slider entra con sus nombres gigantes.
- **Lo de antes sigue:** la intro, la ruleta que se inclina, la baraja de gente feliz (lo mejor), las tarjetas que giran y la frase que se escribe sola.
- **Cada sección tiene su momento sin pasarse, y dan ganas de ir.** El cierre sigue tranquilo (ver 12), pero ya no apaga la página: es la hora de los datos.

## Mis 14 cambios, punto por punto

| # | Cambio pedido | Estado |
|---|---|---|
| 1 | Cierre · loop nocturno de terraza | **Descartado por el dueño** (terraza de día). No resta. *Nota:* a 1920 ese loop va a ~900 px y trae un primer plano de uñas rosadas con vaso que se ve pixelado. Lo dejo anotado, sin descuento. |
| 2 | Con quién · sacar la botella en la boca | **Aplicado.** `quien-multitud-3-b` salta 55,53–56,73 s. |
| 3 | Lugar y Comida · títulos que no choquen | **Aplicado.** Revisado a 390, 1440 y 1920. |
| 4 | Tragos · rosa vacío antes de «Ver la carta completa» | **Descartado por el dueño** (vacíos de color). |
| 5 | Lugar · amarillo bajo la ruleta | **Descartado por el dueño** (vacíos de color). |
| 6 | Eventos · lila vacío y tamaño del video | **Descartado por el dueño** (vacíos y tamaño del video). |
| 7 | Equipo y Comida · bandas al pie | **Descartado por el dueño** (vacíos de color). |
| 8 | Carta · paleta nueva, 16 px, centrada | **Aplicado.** Negro único, hoja crema centrada, pestañas de color, 0 textos bajo 16 px, enlazada a /nueva_v9/. *Menor:* la nav de la carta («Escríbenos por DM» + EN) no es igual a la del inicio («Carta» rosa + EN). No resta. |
| 9 | Comida · `comida-queso` a 8–10 s | **Descartado por el dueño** (video del queso). Sigue en 7,3 s. |
| 10 | Cierre · confirmar que el mapa carga | **Queda por verificar en línea.** Aquí es un recuadro gris vacío (sin red) y no lleva texto mientras carga. |
| 11 | Tragos · momento WOW y nombres letra por letra | **Aplicado.** El Peter grande con su nombre armándose. El carrusel sigue con 5 tragos. |
| 12 | Cierre · golpe de brindis en «USTÉ SE LO MERECE!» | **Queda.** El título entra como los demás, sin choque ni brindis propio. No impide el 4 de Entretención, pero sería la guinda. |
| 13 | Reseñas · que se puedan leer enteras | **Aplicado y mejorado:** tarjetas de color, se detienen 2,4 s y encajan al soltar. **Trajo el choque de la comilla** (ver E). |
| 14 | Lugar · Sillones | **Aplicado.** Ahora se ven los sillones de verdad, con el pie alineado a los demás. |

## Lo que falta para el 20 (priorizado)
1. **Reseñas · comilla gigante · que no se monte sobre la primera línea.** Que la cita parta debajo de la comilla, con un `padding-top` igual a su alto, o que la comilla vaya detrás del texto con baja opacidad. Revisar las 10 tarjetas a 360, 390, 1440 y 1920. **Con esto, E → 4 y queda 20/20.**
2. **Cierre · mapa · confirmar en línea** que el iframe carga. Mientras carga, mostrar «Serrano 325, Castro» con el pin, para que no quede un recuadro gris mudo.
3. **Cierre · «USTÉ SE LO MERECE!»** (opcional, por gusto): que entre con el mismo choque de brindis que «no somos ná sin ustedes!».
4. **Confirmar que el sitio en línea es el commit `08be044`.** No pude abrir almudbar.pages.dev desde aquí.

— Carmen Paz
