# Almud Bar v2 — plan de 20 fases

Base: método web-regalo-cold-call (ghostwriter estricto, solo material real, public/ por publish.py, Cloudflare Pages, una rama main).
Nuevo: las skills Impeccable, Taste y Emil Kowalski (en Escritorio\almud_bar\skills) guían cada decisión, y cada bloque cierra con una ronda de pulido.

Diagnóstico de la v1 (feedback de Pablo, 2026-10-20):
- Los flecos entre secciones se ven baratos → fuera.
- "Circo" genérico → el carácter está en sus historias: cada post es un cuento con nombres, juegos de palabras y gente.
- Fotos tomadas sin criterio → elegir las épicas y con más likes, con jurado de agentes.

## Bloque A · Fundamentos (1–4)
1. **Skills.** Leer completas Impeccable (SKILL + new-work, craft-floor, critique, audit, polish), Taste (SKILL + tells, imagery, type, layout, motion, copy) y Emil (emil-design-eng, animate, review-animations, animation-performance). Resumen de reglas aplicables en `_plan/skills-notes.md`.
2. **Diagnóstico de la v1.** Correr critique (Impeccable), tells (Taste) y review-animations (Emil) sobre la v1 en línea. Lista de lo que se va, lo que queda y por qué.
3. **Inventario de historias.** Las 180 publicaciones agrupadas en cuentos: aniversarios, Jalogüín, fonda, equipo, nombres de tragos, terraza, Ojo Piojo, Rucalaf, desfile, Teik Agüei. Para cada uno: el texto literal, las fotos y los likes.
4. **Ranking de fotos.** Puntaje por likes (normalizado por época), calidad técnica (nitidez, luz, encuadre) y fuerza narrativa. Top 60 candidatas en hojas de contacto.

## Bloque B · Jurado y dirección (5–8)
5. **Jurado de tres agentes independientes:** diseño gráfico, redes sociales y diseño web. Cada uno elige y justifica sus 25 imágenes y la imagen de portada; se cruzan los votos.
6. **Brief de producto** (PRODUCT.md de Impeccable): modo Persuade/Experience, audiencia (turistas en Castro y locales), qué tiene que sentir quien entra.
7. **Dirección visual nueva** (new-work de Impeccable + direcciones de Taste): 2–3 rutas con moodboard de sus propias fotos y una elegida con argumento. Se mantienen el logo y su voz; se reemplaza el lenguaje gráfico de la v1.
8. **Sistema:** tipografía revisada (typeset), paleta desde las fotos ganadoras (colorize), grilla y ritmo (layout). DESIGN.md con tokens.

## Bloque C · Construcción (9–14)
9. **Guion v2:** estructura de la página como una noche en Almud contada con sus historias. Todo literal y con fuente en `content/copy.md`.
10. **Medios v2:** recortes y tratamiento de las fotos ganadoras, videos elegidos, LQIP, pesos.
11. **Portada y momento memorable** rehechos con la foto o video de portada elegido por el jurado.
12. **Secciones de historias:** cada cuento como capítulo editorial, con foto épica, texto literal y detalle.
13. **Carta, equipo, reseñas y cómo llegar** rediseñados con el nuevo sistema.
14. **Movimiento** según Emil: decidir qué anima y qué no, curvas, duraciones y reducción de movimiento. Fuera todo lo decorativo que no aporte.

## Bloque D · Pulido iterativo (15–18)
15. **Ronda 1:** critique + tells sobre la página completa, en capturas de 390 a 1920 px, y corrección.
16. **Ronda 2:** jurado de los tres agentes revisando el resultado (no el plan), y corrección.
17. **Ronda 3:** polish + audit de Impeccable (detalle, a11y, rendimiento, responsive) y review-animations de Emil.
18. **QA técnico:** CLS < 0,01, raíz = public/, Lighthouse, sin GSAP / movimiento reducido, cambio de idioma y de quiebre, vista sin JS.

## Bloque E · Cierre (19–20)
19. **Auditoría independiente final** (voz y datos / código), corrección de todo lo bloqueante y recomendable.
20. **Publicación:** build + publish, push a main, Cloudflare en verde, verificación en línea (rutas internas, imágenes, miniatura), correo de aviso con antes/después.
