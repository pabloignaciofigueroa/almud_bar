# Fase 8 · Contrato de dirección y surface brief (v2)

Decisión del cliente (vinculante), sobre las imágenes de la fase 7:
1. **Portada = viewport de la ruta B** (`ruta-b-viewport.jpg`), con su defecto corregido: el scrim ya no entierra las caras.
2. **Lenguaje visual del sitio = moodboard de la ruta A** (`ruta-a.jpg`): sus afiches.
3. **La carta = moodboard de la ruta C** (`ruta-c.jpg`): la carta como la imprimen.

Esto es un híbrido. B pone la primera pantalla, A pone el mundo y C pone la única página de papel. La v1 queda solo como anti-referencia.

Context loading did not run; leí el contexto del proyecto directamente (`PRODUCT.md`, `brief-v2.md`, `rutas.md`, `skills-notes.md`, las notas de las skills y `seleccion.json`).
**Sustituto declarado:** `seed: none (unavailable)`, porque el binario `impeccable concept-seed` no está autorizado. Va en su lugar el sorteo de Taste ya corrido en la fase 7 (`draw-options.txt`: `page-is-the-object` gana; `place-carries-it` y `split-stage` quedan como competitivos). Este híbrido es la fusión que eligió el cliente: el objeto-afiche (A) como mundo y el lugar (B) como primera pantalla.

---

## Direction contract
```
THESIS: Almud ya imprime su mundo: afiches nocturnos sobre negro y una carta en papel. La web
        abre bajo su techo de cintas lleno de gente y después habla en sus afiches. Rechaza el
        bar "premium" casi negro con serif dorada y video de chorro, y el cotillón arcoíris de la v1.
OWN-WORLD: noche cálida #170e0b (la sombra de sus fotos), tinta papel #f6ecdc, un solo acento
        barra #ff3f6c solo en la acción. Cinco campos planos de Ojo Piojo, uno por pantalla y cada
        uno con su tinta. Six Caps a escala de afiche y Oswald para el resto. Fotos rectas en
        mosaico 4:5. Una sola hoja de papel: la carta, con nombres en azul #2023e4 y precios
        magenta #cd007a. Esquinas rectas, sin sombras, sin líneas.
STORY: ve que hoy está lleno (caras, cintas), sabe en 10 s qué es, cuándo abre y dónde queda.
        Ve la promo real de hoy, cree en los tragos y la cocina por sus nombres y fotos, y abre
        la carta, el mapa o el DM.
FIRST VIEWPORT: barra de nav plana sobre noche (5 enlaces + [Ver la carta] en barra). Debajo,
        P189 a sangre y a 1:1, hasta 1440 px de ancho (más allá, noche a los lados), anclada
        para que el techo ocupe ~45 % y las caras el tercio inferior sin nada encima. Logotipo
        ALMUD BAR + isotipo (38 % del ancho) sobre la pared de zinc entre techo y caras, a la
        izquierda. A la derecha, sobre la pared oscura, la bio [BIO], "Abrimos de Mar a Sáb a
        las 18:00hrs · Serrano 325, Castro" [BIO], Cómo llegar y Escríbanos al DM. Scrim radial
        neutro solo detrás de cada bloque de tipo. En teléfono: foto a sangre, caras al 46–60 %,
        tipo debajo de las caras con scrim desde el 40 % inferior.
FORM: portada-lugar (B) + afiche-página (A) + hoja-carta (C). Fusión elegida por el cliente
        entre el 1.º y el 2.º de la lista ordenada. seed: none (unavailable)
FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the
        verdict, DESIGN.md, and every shipping raster carrying its provenance
```

---

## Surface brief

**Alcance y modo.** Sitio público de una página, en modo **Persuade**. "El lugar" y "Con quién" se comportan como Experience. Bilingüe ES/EN, con el teléfono primero.

**Público.** Turista o local en Castro que mira el teléfono a las 17:30, de noche y a veces con mala señal, y decide adónde ir hoy. Los dueños, que tienen que reconocerse.

**Trabajo y acción.** Decidir ir hoy. La acción funcional es abrir el mapa (Serrano 325), escribir al DM o ver la carta. No hay reservas.

**Prueba y contenido.**
- P189, la terraza llena.
- La promo literal de hoy [CARTA-7].
- Nombres, descripciones y precios literales de la carta.
- Las fotos del jurado (31).
- Sus captions con ID de fuente.
- Nada inventado: ni hora de cierre ni filas.

**Restricciones.**
- Fotos de 1440 px sin ampliar.
- Six Caps + Oswald, nada más.
- Un color de campo por pantalla.
- Sin eyebrows, emoji, degradados (salvo el scrim funcional), sombras, vidrio ni líneas en la carta.
- Sin JS, el contenido queda completo.

**Dirección elegida y momento memorable.** La portada bajo las cintas. Después, capítulos-afiche y la carta en papel.

### El único momento autoral: "la franja se imprime"
Ocurre una sola vez, cuando el bloque **Hoy en Almud** entra en pantalla:
1. el campo del día se abre como una tira de afiche (`clip-path: inset(0 100% 0 0) → inset(0)`, 700 ms, `--ease-in-out`);
2. el titular del día sube con máscara de línea (800 ms, `--ease-out`, +240 ms);
3. la foto se abre de arriba hacia abajo (600 ms, +360 ms).

**Por qué este y no otro:**
- Es el único lugar donde el lenguaje de afiche (las tiras de Ojo Piojo) toca algo que cambia cada día. El movimiento queda atado al contenido vivo, no a la decoración.
- La portada queda quieta a propósito. Así el LCP y la legibilidad no dependen de la animación (Taste: legible en ≤1,2 s), y las caras se ven de inmediato.
- Todo lo demás es feedback (presión .97, hover de color) o reveals `once` cortos.
- En `prefers-reduced-motion` queda un fade de 180 ms.

### La única cosa viva: "Hoy en Almud"
- La promo literal de `content/carta.json › promos`, según el día en `America/Santiago`:
  - Mar: Negroni & Fernet c/Coca Cola, campo coral.
  - Mié: "Miércoles de piscoleinnnn!" [IG-019] + Piscolein & Gin Tonic, turquesa.
  - Jue: "hoy es Jueves de Sangría!" [IG-039] + Sangría de la casa, fucsia.
  - Sáb: Ramón a $ 4.500!, verde.
  - En todos: "$ 4.500", "de 18:00 a 22:00 hrs" y "* Siempre sujeto a stock! *" [CARTA-7].
- **Vie** no tiene promo: va "Venga venga que nadie le detenga!" y "Viernes ya!" [IG-003], en amarillo.
- **Dom y Lun:** "Abrimos de Mar a Sáb a las 18:00hrs" [BIO] y la promo del martes.
- Debajo va siempre la semana completa, que también es el estado sin JS.

**Por qué:** responde lo primero que pregunta la escena de las 17:30 ("¿qué hay hoy?") con contenido real. Vuelve el lema "todos los días son una fiesta" un mecanismo y no un adjetivo, y se apoya en algo que ya existe: no hay que inventar ni mantener nada.

### Decisiones abiertas
1. **Resolución de P189 en pantallas de DPR 2.** A 1:1 en un retina se ve a media resolución. Pedir el original en alta (alternativa 3 del asterisco) apenas el cliente acepte.
2. **El ancla vertical de la portada** (`top: -19,7 %` del ancho) está afinada para 1440 × 900. Hay que verificar en 1280 × 720 y 1536 × 864 que el logotipo siga sobre la pared y no sobre las caras. Si en pantallas bajas no cabe, el tipo de la derecha baja a una franja de noche bajo la foto.
3. **Texto EN** de la cosa viva (glosas [UI] de "Hoy", los días).
4. **Asignación de campos por capítulo.** Cambia la de `rutas.md` (ver `sistema.md` §2.3): Tragos pasa a amarillo y Con quién a fucsia, porque el fucsia sobre fotos rojas y rosadas se empasta.
5. **Video.** Siguen en pie los loops V021, V009 y V031 de `veredicto.md`; el tile no los muestra.
6. **Logotipo en SVG claro** (`brand/almud-horizontal-claro.svg`): falta confirmar el trazo del isotipo a 250 px en teléfono.
