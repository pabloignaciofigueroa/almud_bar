# Almud Bar v3: plan de 20 fases (método /web-regalo-cold-call)

**Meta.** El agente Carmen Paz debe dar ≥ 18/20 en "calidad Almud". Bajo 18 no se entrega: se corrige y se vuelve a evaluar.

**Fuente única.** Almud y su Instagram.

**Fuera.**
- Las skills Kowalski, Impeccable y Taste.
- El "Almudcito ito ito".
- Los sabanazos, los flecos y el circo.

**Reglas de trabajo.**
- Commit y push a `main` al cierre de cada fase, con una línea en `PROGRESS.md`.
- Videos: se reproducen solos, sin sonido y en loop. El scroll nunca los pausa, nunca los reproduce y nunca maneja su avance. Sin botón de sonido.
- La página v3 se construye en `/v3/` sin tocar la portada actual. Reemplaza a la actual solo en la fase 20.

---

## A · Material y marca

### 1. Inventario y diagnóstico de su Instagram
- **Qué:** reviso lo que ya está en el repo (180 posts, 57 reels, destacadas, 7 PDF de carta, 18 reseñas, catálogo de 693 archivos y ranking). Completo con lo que falte: posts recientes, bio actual y destacadas.
- **Agente Carmen Paz:** describe "cómo presento mi marca en Instagram":
  - qué tipo de foto publico;
  - qué escribo y qué nunca escribiría;
  - qué afiches hago;
  - qué me enorgullece del local.
- **Entregable:** `_plan/v3/01-inventario.md` y `_plan/v3/01-carmen-instagram.md`.
- **Listo cuando** cada sección futura tiene material real identificado.

### 2. Voz de marca premium
- **Qué:** reviso su corpus completo, guardado en `ig_captions.md`.
- **Agente Voz:**
  - separa frases que suben el nivel (ingenio, invitación, identidad) de las que lo bajan (exceso de diminutivos, emoji, chistes internos);
  - elige 10 a 15 titulares cortos y literales, con su fuente;
  - fija la lista de palabras prohibidas en la página, empezando por "Almudcito ito ito".
- **Agente Carmen Paz:** aprueba o veta cada titular.
- **Entregable:** `content/brand-voice-v3.md` con titulares aprobados, frases vetadas y reglas.
- **Listo cuando** hay un titular aprobado por sección.

### 3. Tipografías
- **Qué:** comparo en lámina sus afiches, su letrero y su carta contra la tipografía elegida. Big Shoulders va en títulos, Barlow Condensed en textos y Six Caps solo en el logo. Pruebo tamaños reales en 390 px y 1440 px.
- **Agentes Color y Carmen Paz:** validan que "se parece a lo nuestro y se lee".
- **Entregable:** `brand/typography-v3.md` y una lámina de muestra.
- **Listo cuando** Carmen Paz lo aprueba y todos los textos se leen en el celular.

### 4. Paleta
- **Qué:** extraigo colores con k-means de cuatro fuentes: las 30 mejores fotos (luz de noche cálida), sus afiches, el muro rosa y el letrero (blanco y azul).
- **Agente Color:**
  - define roles: fondo, texto, acento y un color por sección;
  - fija 1 o 2 acentos como máximo por pantalla, no arcoíris;
  - verifica el contraste por cálculo.
- **Entregable:** `brand/palette-v3.md` y los tokens CSS.
- **Listo cuando** Carmen Paz reconoce su local en la paleta.

### 5. Logo, favicon e imagen para compartir
- **Qué:**
  - reviso las variantes del isotipo y el logotipo;
  - hago un favicon nuevo;
  - armo la imagen OG de 1200×630 con la terraza llena y el logo, que es lo que se ve al compartir por WhatsApp.
- **Entregable:** `brand/`, `assets/og.jpg` y una lámina.
- **Listo cuando** la miniatura se ve bien en una simulación de WhatsApp.

## B · Contenido

### 6. Guion v3
- **Qué:** defino la estructura del servicio del bar, una pantalla por sección y como mucho un titular y una línea suyos por sección:
  1. Portada: video, logo y una frase.
  2. El lugar: rincones.
  3. Tragos: destacados.
  4. Comida: destacados.
  5. Con quién y para qué.
  6. Eventos: calendario.
  7. Equipo.
  8. Reseñas: internacionales, en idioma original.
  9. Cuándo y dónde.
  10. Pie.

  La carta completa va en su página aparte.
- **Agentes:**
  - Textos de página: decide qué palabras sobran;
  - Voz: asegura que todo sea literal;
  - Carmen Paz: veta cualquier frase que no diría.

  Las traducciones al inglés son para el turista.
- **Entregable:** `content/copy-v3.md`, con la fuente de cada texto, verificado por script contra sus captions.
- **Listo cuando** la página entera tiene menos de 150 palabras visibles, sin contar la carta.

### 7. Medios: fotos y videos
- **Agente Imágenes:** elige 1 a 3 fotos por sección desde el ranking y el jurado. Descarta las que tienen texto encima, las de terceros y las de exempleados.
- **Agente Video:**
  - elige un reel por sección donde suma;
  - lo corta en loops limpios de 5 a 8 segundos;
  - lo deja en 720p, en MP4 y WebM, con su póster.
- **Recortes:** reviso a mano que ninguna cara quede cortada.
- **Pesos:** el primer pantallazo pesa menos de 1,5 MB en el celular.
- **Entregable:** `tools/media_v3.py`, `assets/v3/` y una hoja de contacto.
- **Listo cuando** Imágenes y Video aprueban la hoja de contacto.

### 8. Dirección de arte
- **Qué:** dibujo el ritmo pantalla por pantalla, en celular y escritorio: qué foto o video, qué texto y qué color en cada pantalla.
  - **Un momento memorable:** el isotipo que se abre al video, sin texto encima.
  - **Movimiento:** revelado con máscara y parallax suave.
  - **Galería horizontal:** con el dedo, nunca atada al scroll.
- **Boceto:** hago un boceto en imagen de las 10 pantallas.
- **Agente Carmen Paz:** lo aprueba antes de escribir código.
- **Entregable:** `brand/art-direction-v3.md` y `_plan/v3/boceto.jpg`.
- **Listo cuando** Carmen Paz da ≥ 16/20 al boceto. El 18 se exige al sitio final.

## C · Construcción
Cada fase se cierra con capturas a 390 px y 1440 px, que reviso yo, y con commit.

### 9. Base y publicación
- **Qué:**
  - `src-v3/index.html`, `css/v3/`, `js/v3/`;
  - `tools/build_v3.py` con srcset, LQIP, versión en la URL de CSS y JS, y alt en inglés obligatorio;
  - `publish.py` ampliado para `/v3/`;
  - videos con `autoplay muted loop playsinline` en el HTML;
  - el JS solo carga la fuente, nunca pausa por scroll.
- **Listo cuando** `/v3/` carga en blanco con fuentes y paleta, sin errores.

### 10. Portada
- **Qué:** video a pantalla completa, de 100svh, reproduciéndose solo. Lleva el logo, una frase y el botón "Ver la carta". Nada más.
- **Listo cuando** el primer pantallazo del celular es impactante y se entiende en 3 segundos qué es Almud.

### 11. El lugar
- **Qué:** rincones con foto o video y su nombre: barra, salón, sillones, terraza techada, terraza abierta, cuadros y mural.
  - En el celular: galería que se desliza con el dedo.
  - En escritorio: mosaico o galería horizontal sticky, sin pin.
- **Listo cuando** un turista entiende cómo es el local por dentro sin leer.

### 12. Tragos y comida
- **Qué:** 4 a 6 destacados con foto real, nombre y precio literales, sobre fondo de color, con videos de la coctelera, el humo y la cazuela. Termina en "Ver la carta completa".
- **Listo cuando** dan ganas de pedir algo.

### 13. Con quién y eventos
- **Qué:**
  - Con quién: fotos de gente real en noches cualquiera.
  - Eventos: calendario con nombre, mes y foto, y el próximo marcado.
- **Listo cuando** se siente que todos los días hay ambiente.

### 14. Equipo, reseñas, dónde, pie y carta
- **Qué:**
  - Equipo: fotos con su @.
  - Reseñas: carrusel internacional con la nota de Google y Tripadvisor.
  - Dónde: dirección, horario, mapa que carga al tocarlo y DM.
  - Pie.
  - La página de la carta pasa al estilo v3.
- **Listo cuando** está todo y la página completa mide 10 a 12 pantallas en el celular.

## D · Calidad Almud

### 15. Ronda 1 de los 7 agentes, en el celular
- **Qué:** cada agente recorre `/v3/` en capturas reales de 390 px y pone nota de 20 en su tema, con una lista de cambios.
- **Correcciones:** las aplico todas, subo y repito las capturas.
- **Entregable:** `_plan/v3/ronda1.md`.

### 16. Ronda 2: escritorio y celular
- **Qué:** igual que la ronda 1, más la comparación con su Instagram lado a lado.
- **Listo cuando** cada agente da ≥ 17.
- **Entregable:** `_plan/v3/ronda2.md`.

### 17. Responsive y accesibilidad
- **Qué:**
  - anchos de 360, 390, 768, 1280, 1440 y 1920 px;
  - versión en inglés completa para el turista;
  - movimiento reducido;
  - sin JavaScript;
  - teclado;
  - contraste.
- **Listo cuando** nada se rompe en ningún ancho.

### 18. QA técnico
- **Qué:** sirvo `public/` y lo comparo con la raíz.
- **Criterio:** se cumple todo esto:
  - cero errores de JavaScript;
  - cero respuestas 4xx;
  - CLS menor a 0,01;
  - todos los videos con `paused=false` sin scroll;
  - caché versionado;
  - peso del primer pantallazo y LCP en celular.
- **Listo cuando** todo pasa.

## E · Cierre

### 19. Juicio final del agente Carmen Paz
- **Qué:** Carmen Paz recorre el sitio completo como dueña, comparándolo con su Instagram, y pone nota de 20 con justificación.
- **Si queda bajo 18:** vuelvo a la fase que corresponda.
- **Entregable:** `_plan/v3/juicio-carmen.md`.

### 20. Publicación y aviso
- **Qué:**
  1. La v3 reemplaza a la portada actual en almudbar.pages.dev.
  2. Cloudflare en verde.
  3. Verificación en línea: rutas internas, imágenes, videos y miniatura.
  4. Te mando el link con la nota de Carmen Paz y capturas.
