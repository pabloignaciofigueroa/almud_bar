# Jurado 2 · Redes sociales (estratega IG para hospitalidad) · sitio construido

> Revisión del sitio construido, no del plan. Servido en :8792 y capturado con Chromium, pantalla por pantalla, a 390×844 (principal, como llega la gente desde el link de la bio) y a 1440×900. Capturas en `_plan/jurado-2/shots-redes/`: `home-m-00…27`, `home-d-00…25`, `carta-m-00…04`, `carta-d-00…04`, `home-m-hoy-{lunes,viernes,sabado-noche}.png` y `og-image.jpg`. Revisé todas las capturas. Fecha simulada: hoy, miércoles 21-10-2026.

## Puntaje: 8,2 / 10 · Veredicto: **FIX** (corto, 1–2 h). Con los P1 resueltos queda APPROVE (≈8,8)

Si Carmen Paz y Sylvain lo abren hoy, se reconocen. Es su Instagram en sus mejores noches: banderines, muro rosa, caras reales y su propia voz en titulares enormes ("NOS GUSTA EL COLORSSSS!", "PA CHUPARSE EL BIGOTELI", "NO SOMOS NÁ SIN USTEDES!", "QUE NO SE LO CUENTEN! BESIIIII"). Lo que frena el APPROVE no es el diseño: es que el regalo se manda por DM, y lo primero que ellos van a ver es la vista previa del link, que hoy probablemente sale sin imagen. Además hay un @ del equipo que puede llevar a una cuenta que no es la de ella.

## Fortalezas (lo que no hay que tocar)
1. **Los primeros 5 segundos en el teléfono son ejemplares** (`home-m-00`). Una sola pantalla trae la foto de portada P189 (terraza techada llena, risas en primer plano, techo de cintas), el logo, el claim de la bio, "Abrimos de Mar a Sáb a las 18:00hrs · Serrano 325, Castro" y dos acciones: **Cómo llegar** y **Escríbanos al DM**. Arriba hay un header fijo con el botón rosado "Ver la carta". Sé cuándo y dónde sin hacer scroll. Es un sitio pensado para el link de la bio.
2. **El bloque "Hoy" es el gancho de "voy esta noche"** (`home-m-01`, `home-m-hoy-*`). El miércoles muestra "MIÉRCOLES DE PISCOLEINNNN!" a $4.500, de 18:00 a 22:00, con la garzona del jockey. El lunes dice "ABRIMOS DE MAR A SAB" con el video del Negroni, el viernes "VIERNES YA!" y el sábado "ÚLTIMO DÍA DE LA SEMANA". Es lo que hacen las cuentas de bares que funcionan: cada día tiene su motivo. Bien resuelto.
3. **Caras y alegría de verdad.** "Con quién" (`home-m-16…19`) junta parejas de distintas edades, tres amigos, amigas brindando frente al muro rosa, el brindis eufórico de P198 y la clienta riendo sin motivo. Todo es de noche, con calidez y sin disfraces. Se siente el "quiero estar ahí", y el brief lo pedía: un día cualquiera es fiesta.
4. **La voz es literal y tiene encanto**: usté, celebreichons, complikeichon, terracita ita ita, "ideal pa venir a bien-tratarse", "porque usté se lo merece y punto!". No encontré frases corporativas ni "experiencias únicas", y no aparece nada sobre filas ni esperas (lo busqué con grep).
5. **Dan sed y hambre.** En la carta de la portada (`home-m-13…14`) están Aquí te las traigo Peter con la burbuja de humo, Sagüer on Faia con el soplete, Sangría Foreva!, La moto chantá, Tukulito Sakayama y Camarón que se duerme, con precio y descripción literal. En `/carta` hay 7 pestañas con fotos que funcionan como láminas. "Ver la comilona" es un buen guiño.
6. **El equipo está presente y vigente.** Están "PEAZO DE EQUIPO QUE TENEMOS!" con las dos garzonas de IG-014, la lista de IG-010 (julio de 2026, vigente) y "los papis del almud: el franchuto @rusio_mezclao y la disharashera @cepaz". El mural sale firmado "Proyecto @cepaz". @vlanbartender no aparece y ninguna exempleada se presenta como equipo actual.
7. **Los eventos están en su lugar**, con un calendario mes a mes y años (`home-m-22…24`). Las fotos que delatan la fecha (el "10" de flores, la torta, el Jalogüín) quedan solo ahí. El CTA "asegure su entrá hablándonos al DM!" sale de ellos.
8. **Hay acciones claras en toda la página**: ig.me/m/almud_bar (abre el DM directo en la app), Maps ×11 y @almud_bar. Los créditos a los fotógrafos (@estudiouno.prod, @isosur.prod, @catarsis.fotografia…) están bien hechos y además conviene: son cuentas que lo van a compartir.
9. Probé 390 px sin scroll horizontal y no hubo errores de consola ni requests fallidos.

## Fixes priorizados

### P1 (antes de mandar el regalo)
- **P1-a · OG con URL relativa** (`index.html` y `carta/index.html`, `<head>`). Hoy está `og:image="assets/v2/img/og-terraza.jpg"` y `"../assets/…"`. Los scrapers de WhatsApp, Instagram DM y Facebook necesitan una **URL absoluta https**, y con una relativa la vista previa suele salir sin foto.
  - **Fix:** usar `og:image` absoluta con el dominio final. Agregar `og:url` (canónica), `og:site_name="Almud Bar"`, `og:locale="es_CL"`, `og:image:width=1200`, `og:image:height=630`, `og:image:alt` y `twitter:card=summary_large_image`. Después, validarlo en el Sharing Debugger de Facebook y mandándose el link a uno mismo por WhatsApp. La imagen sí está bien (`og-image.jpg`, 1200×630, P189 con caras riendo bajo los banderines). Es la mejor que se podía elegir.
- **P1-b · @ de Lizze con dos grafías y dos destinos** (`home-m-20…21` y `home-d-18`, sección Equipo). El pie de la foto dice @lizzearellanol y apunta a `instagram.com/lizzearellanol/`. La lista de abajo dice @lizzearellano y apunta a `instagram.com/lizzearellano/`. En los captions, "-nol" aparece 11 veces (2023–2026, incluido IG-050) y "-no" 3 veces (IG-010, IG-031, IG-131), así que uno de los dos links probablemente cae en otra cuenta o en un 404. Una habitué lo nota al tiro, y a ella le da vergüenza ajena.
  - **Fix:** confirmar el handle vigente (abrir los dos perfiles). Dejar el texto literal de IG-010 si se quiere, pero los **dos `href` tienen que ir al perfil que existe**.

### P2 (mejoran el regalo)
- **P2-a · "Este mes" en Jalogüín** (`home-m-23`, Eventos). La etiqueta [UI] "Este mes", junto a "asegure su entrá hablándonos al DM!", promete un Jalogüín 2026 que Almud todavía no anuncia (no hay post 2026 sobre el tema; los años listados son 2023 · 2024 · 2025). Si el evento no se hace, el regalo queda mal parado.
  - **Fix:** quitar la etiqueta "Este mes" o cambiarla por un rótulo neutro de mes. El CTA de DM se deja genérico, debajo de toda la lista.
- **P2-b · Teléfono sin confirmar** (`home-m-25`, Cuándo y dónde). "+56 65 253 0084" viene de Tripadvisor y brand-voice §6 lo marca como "confirmar". Si un cliente llama y no contesta nadie, la culpa es del sitio.
  - **Fix:** confirmarlo con el bar o sacar la fila; el DM ya cubre ese uso.
- **P2-c · El mapa abre un pin pelado** (todos los "Cómo llegar"). `maps/search/?query=-42.48…,-73.76…` deja caer un pin en coordenadas, sin ficha.
  - **Fix:** `query=Almud+Bar+Serrano+325+Castro` (o `query_place_id=`). Así se abre la ficha de Google, con fotos, horario, "cómo llegar" y las 848 reseñas de 4,6★. En redes, eso convierte mejor que un pin.
- **P2-d · En el hero falta el guiño de voz** (`home-m-00`). El hero tiene los datos y la foto, pero lo primero que se lee es el claim de la bio, que suena a cualquier bar.
  - **Fix:** agregar una línea literal sobre el claim o bajo los datos: "Véngase pal Almudcito ito ito, le esperamos desde las 6 pm :)" [IG-013]. Así los 5 segundos ya suenan a Almud.
- **P2-e · El header de la carta en móvil se come la pantalla** (`carta-m-01…03`). Las 7 pestañas sticky arman 3 filas, unos 150 px de 844.
  - **Fix:** en móvil, una sola fila con scroll horizontal (overflow-x con snap) y la pestaña activa visible.

### P3 (pulido)
- **P3-a · Pulseras de evento** visibles en "El salón" (aro de luz, `home-m-03` / `home-d-03`: pulsera en la muñeca de la derecha) y en "Con amigos" (pulsera verde arriba, `home-m-17`). Delatan una noche con entrada.
  - **Fix:** recortar el borde o aceptarlo. En "El salón", esa foto (selfies con aro de luz) además cuenta poco del salón: P114 (sillón) o la lámpara de mimbre con gente lo dirían mejor.
- **P3-b · "#1 de 6 bares en Castro"** (`home-m-21`, Reseñas). El "de 6" achica el logro.
  - **Fix:** "#1 de bares en Castro · Tripadvisor".
- **P3-c · Reseñas en inglés como titular** en una página en español (`home-m-21`). Para un parroquiano de Castro se lee raro.
  - **Fix:** abrir con Kevin B ("Ahora entiendo porque se habla tanto del lugar…") y dejar las de turistas después. Las extranjeras igual suman para quien viene de visita.
- **P3-d · Sábado después de las 22:00** (`home-m-hoy-sabado-noche`). A las 23:30 sigue mostrando "Ramón a $4.500, de 18:00 a 22:00".
  - **Fix:** pasadas las 22:00, mostrar la variante sin precio ("Venga venga que nadie le detenga!").
- **P3-e · Escritorio: "NOS GUSTA EL COLORSSSS!"** (`home-d-02`) deja media pantalla vacía, con una línea suelta ("Un lugar que fuera cálido, acogedor").
  - **Fix:** subir ahí una foto del lugar (P093, la barra curva) o centrar el bloque.
- **P3-f · Los dueños no tienen cara.** Aparecen solo como @. Si el bar confirma quién es quién (¿es Sylvain el de la torta de los 11?), una foto de "los papis del almud" juntos sería lo que más se comparte. **No** usar el reel IG-007 (♥1488): es de creadores externos.
- **P3-g · OG de /carta**: usa la misma terraza. Un trago (Peter con burbuja) diría "carta" en la vista previa.

## Riesgos revisados
- **Caras de clientes:** todas salen de posts de "sociales" que el propio Almud publicó, en momentos favorables y sin primeros planos con flash. Conviene pedir un OK general al bar al entregar el regalo. No vi menores.
- **Contenido de terceros:** no hay reels de creadores ni fotos en Rucalaf. Los músicos externos no aparecen. Las marcas (Mistral, Coca-Cola) salen solo como fondo, sin problema.
- **Equipo desactualizado:** la lista es de julio de 2026. La única inconsistencia es el @ de P1-b.
- **Promesas:** la etiqueta "Este mes" (P2-a) y el teléfono (P2-b) son las únicas dos promesas que el sitio no puede garantizar.

## Si tuviera que defenderlo en una frase
Es el Instagram de Almud con dirección, horario y carta: abre con fiesta y caras, cuenta el día de hoy y cierra con un "Besiiii". Basta arreglar la vista previa del link y el @ de Lizze para mandarlo con orgullo.
