# Product
<!-- impeccable:product-schema 1 -->

## Platform
Sitio web público de una sola marca, servido como página estática. El uso principal es el teléfono: alguien en Castro, o planeando ir, decide adónde salir. El escritorio se usa para planificar viajes y para compartir el enlace.

## Stack
HTML/CSS/JS estático. La animación usa GSAP 3 con ScrollTrigger y Lenis, servidos desde `vendor/`; no hay CDN en tiempo de ejecución. Las fuentes son autoalojadas. El sitio se genera con `tools/build.py` y se publica desde `public/` con `tools/publish.py` en Cloudflare Pages (proyecto `almudbar`, rama `main`).

## Users
- **Visitantes y turistas en Castro y Chiloé**, chilenos y extranjeros. Buscan un buen lugar para una noche y leen en español o en inglés.
- **Gente de Castro** que ya conoce Almud o lo tiene en el radar. Quiere saber qué hay hoy, la carta y si pasar después del trabajo.
- **Cualquier compañía y cualquier ocasión:** solo en la barra, en pareja, con dos amigos, de cumpleaños o sin motivo.
- **Los mismos dueños y el equipo** (Carmen Paz Oyarzun @cepaz y Sylvain @rusio_mezclao). Es un regalo en frío: la página tiene que hacer que se reconozcan.

## Product Purpose
Ordenar y mostrar lo que entrega el bar: **un lugar donde estar, tragos para disfrutar, una cocina para comer, entretención y buena conversación**. El visitante debe salir con la decisión de ir y con lo necesario para hacerlo: el horario, la dirección, la carta y cómo escribirles.

## Positioning
Almud Bar, en Serrano 325, Castro, "Coctelería de autor, comida & música bonita desde 2014" [BIO]. Es #1 de 6 bares en Castro en Tripadvisor (4,6, 209 reseñas) y tiene 4,6 en Google con 848 reseñas [DATO, oct-2026].

Su diferencia es que **cualquier día es una fiesta**. No es un bar clásico ni fome: es de vanguardia, con mucho color, la barra larga, la terraza techada bajo cintas de colores, una cocina sabrosa y un equipo con nombre propio. Sus eventos son de escala de ciudad.

## Operating Context
- Se lee de noche, en el teléfono, a menudo con mala señal móvil o por WiFi de alojamiento. El primer viewport tiene que cargar rápido y ser útil.
- El idioma por defecto es el español, con inglés para el turismo. El texto de la marca se queda literal en español; el inglés traduce la interfaz y glosa lo necesario.
- El horario publicado es solo "Abrimos de Mar a Sáb a las 18:00hrs" [BIO]. **No hay hora de cierre confirmada por la marca**, así que no se publica.

## Capabilities and Constraints
- **Solo material propio de Almud.** Fotos y reels de su Instagram (catálogo en `_plan/diag/catalogo.csv`, selección en `_plan/jurado/seleccion.json`), su carta oficial, su bio, el video de su historia y sus afiches. No hay fotos de stock ni imágenes generadas.
- **Resolución limitada:** la mayoría de las fotos tiene 1440 px de ancho y los reels son de 720p. Solo unas 13 fotos de 2026 tienen 3072 px. No se agranda ninguna imagen por encima de su tamaño real.
- **Sin backend:** no hay reservas ni pedidos. La acción es ir, abrir el mapa o escribir al DM de Instagram.
- **Muestra de regalo:** los originales en alta, el video 4K y las fotos faltantes (sillones, pared de cuadros, mocktails, fachada) se piden después, si les gusta.

## Brand Commitments
- **Identidad:** logotipo ALMUD BAR e isotipo (el almud, la medida chilota), su letra condensada Six Caps (del letrero) y Oswald (la de su carta).
- **Voz:** todo texto visible es literal de Almud, con su fuente (`content/copy.md`, `content/historias.json`, `content/brand-voice.md`). Eso incluye "usté", "Almudcito ito ito", "-eichon", diminutivos, "le esperamos" y "Besi". Nunca se usa la voz de quien hace la web; los textos nuestros se limitan a etiquetas de interfaz mínimas.
- **Nunca se menciona** hacer fila, esperar mesa ni esperar que se desocupe.
- **Personas:** solo se nombra con @ a quien la marca presentó y sigue en el equipo (2025–26).
- **Créditos fotográficos** como la marca los da: @estudiouno.prod, @catarsis.fotografia, @tamillanquileo, @isosur.prod y @dosistudio.

## Evidence on Hand
- `content/ig_posts.json`: 180 publicaciones con caption, likes y archivos. `content/historias.json`: 35 cuentos con citas literales.
- `content/carta.json`: hoy cubre coctelería de la casa, mocktails, comilona y promos. **Pendiente:** completar con los otros PDFs de `assets/raw/carta/` (Cócteles del mundo mundial, Espirituosos, Vinos y espumantes, Jugos & bebidas, Cervezas sin alcohol, Bebidas calientes).
- `content/reviews.json`: 18 reseñas reales con autor, fecha, fuente e idioma.
- `content/research_web.md`: ratings, dirección, coordenadas y teléfono +56 65 253 0084.
- `_plan/diag/material.md`, `ranking.md` y `_plan/jurado/veredicto.md`: diagnóstico y selección de imágenes.
- **Lo que no existe y no se fabrica:**
  - hora de cierre;
  - foto de mocktail;
  - foto de cumpleaños de un cliente;
  - foto nítida de la pared de cuadros;
  - vista de la fachada desde la calle;
  - identidad visible de los dueños en fotos.

## Product Principles
1. **El servicio primero, la fiesta siempre.** La página se ordena por lo que el bar entrega (lugar, tragos, comida, compañía, cuándo y dónde), y cada parte se siente como una noche llena.
2. **Lo cotidiano es el evento.** Las mejores fotos de sus fiestas muestran un día cualquiera. Los nombres de los eventos viven solo en su propia sección.
3. **Ellos hablan, nosotros ordenamos.** Su texto literal manda; el diseño le da escala y lugar, nunca lo reescribe.
4. **Útil en diez segundos.** Horario, dirección, carta y DM están a mano desde el primer viewport, en el teléfono.
5. **Prueba, no adjetivos.** Sus tragos con nombre y precio, su gente con nombre, sus fotos y reseñas reales.

## Accessibility & Inclusion
- WCAG 2.2 AA: contraste ≥ 4,5:1 para texto (≥ 3:1 para texto grande), foco visible, navegación completa por teclado y objetivos táctiles ≥ 44 px.
- `prefers-reduced-motion`: la página queda terminada y legible, con fades breves de opacidad y sin scrub, parallax ni loops.
- El contenido completo es legible sin JavaScript. Los videos van muted, con póster, y no son necesarios para entender nada.
- Bilingüe ES/EN: `lang` correcto en cada bloque, glosas en inglés para su léxico local y precios en CLP con formato local.
- Peso controlado para redes móviles lentas: LCP < 2,5 s en 4G y CLS < 0,01.
