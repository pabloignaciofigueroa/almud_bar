# Almud Bar v3: plan de 20 fases (método /web-regalo-cold-call)

**Meta.** El agente Carmen Paz debe dar **≥ 18/20** en "calidad Almud" antes de entregar. Si da menos, se corrige y se vuelve a evaluar; no hay entregas intermedias.

**Fuente única.** Almud y su Instagram: posts, reels, destacadas, bio, carta oficial, afiches y reseñas reales.

**Fuera.** Las skills Kowalski, Impeccable y Taste, el "Almudcito ito ito", los sabanazos, los flecos y el circo.

**Repo.** Commit y push a `main` al cierre de **cada fase**, con una línea en `_plan/PROGRESS.md`.

**Videos.**
- Se reproducen solos, en silencio y en loop, desde que cargan.
- El scroll es una herramienta para navegar: nunca pausa ni pone play a un video, y nunca maneja su avance.
- Sin botón de sonido.

**Doble público.** Su identidad, sus secciones y su vida, pero clara y presentable para un turista que no los conoce.

## Equipo de agentes especialistas en Almud
| Agente | Responde por |
|---|---|
| **Voz** | Su manera de hablar: modismos, invitación, humor; qué frases suyas suben el nivel y cuáles lo bajan. |
| **Imágenes** | Qué fotos los representan de verdad y cuáles bajan el nivel. |
| **Video** | Qué reels usar, recortes y loops; dónde va cada uno. |
| **Carta** | Cómo presentan tragos, comida y precios; destacados y la página de carta. |
| **Color** | Paleta del local, del feed y de los afiches; roles y contraste. |
| **Textos de página** | Qué palabras van en cada sección y cuáles sobran (mínimo texto, máximo imagen). |
| **Carmen Paz** | La dueña: "este es mi Instagram, así presento mi marca". Jueza final con nota de 20. |

## Fases
**A · Material y marca**
1. **Inventario.** Revisar lo que ya está en el repo (posts, reels, destacadas, carta, reseñas) y completar lo que falte de su Instagram.
2. **Voz de marca.** El agente Voz y el agente Carmen Paz rehacen `brand-voice.md`: qué decir, qué no decir y titulares premium con su fuente.
3. **Tipografías.** Big Shoulders para títulos (familia de su logo), Barlow Condensed para textos y Six Caps solo para el logo. El agente Carmen Paz las valida contra sus afiches.
4. **Paleta.** El agente Color la saca de su local, su feed y sus afiches, con roles y contraste.
5. **Logos y OG.** Se revisan el isotipo, el logotipo, el favicon y la imagen para compartir (la terraza llena).

**B · Contenido**
6. **Guion v3.** Agente Textos de página + Voz. Secciones del servicio: El lugar, Tragos, Comida, Con quién, Eventos, Cuándo y dónde, más la Carta aparte. Una línea suya por sección, como máximo.
7. **Medios.** Agentes Imágenes y Video: selección final, recortes, loops que se reproducen solos, pesos.
8. **Dirección de arte.** Ritmo de la página en pantallas, un momento memorable y movimiento. El agente Carmen Paz aprueba la dirección antes de construir.

**C · Construcción**
9. **Base y publicación.** build y publish con caché versionado; la página nueva convive con la actual hasta aprobarse.
10. **Portada.** Video que se reproduce solo, logo y una línea. Nada más.
11. **El lugar.** Los rincones con fotos y videos (barra, salón, sillones, terrazas, cuadros), un nombre por rincón.
12. **Tragos y comida.** Destacados con foto y precio, y "Ver la carta completa".
13. **Con quién y Eventos.** La vida del bar: fotos de gente y el calendario de sus eventos.
14. **Equipo, reseñas, cuándo y dónde, y pie.** Más la página de la Carta con el estilo nuevo.

**D · Calidad Almud**
15. **Ronda 1.** Los 7 agentes revisan en el celular (390 px), cada uno con nota y lista de cambios; se corrige.
16. **Ronda 2.** Igual, en escritorio y celular; se corrige.
17. **Responsive y accesibilidad.** 390 a 1920 px, inglés, movimiento reducido y sin JavaScript.
18. **QA técnico.** Servir `public/`, cero errores, cero saltos de layout, videos reproduciéndose solos, caché versionado.

**E · Cierre**
19. **Juicio final del agente Carmen Paz.** Nota ≥ 18/20. Si no llega, se vuelve a la fase que corresponda.
20. **Publicación.** Cloudflare en verde, verificación en línea y aviso a Pablo con el link.
