# Dirección de arte — Almud Bar

## Idea
Un bar circense que se ríe de sí mismo. La web es **su noche**: fondo aubergine profundo (la sombra real de sus fotos) que se llena de las cosas de colores que cuelgan en el bar — flecos de papel picado, cintas de la terraza, pinzas de ropa (su foto de perfil), luces. La seriedad la pone la tipografía (Six Caps, condensada y alta, como el "ALMUD" del logo); el chiste lo ponen sus palabras.

Lo que la hace distinta de una web de bar "premium" genérica:
- No hay un acento único: hay **seis colores de cinta** con funciones (barra=rosa, brasa=naranjo, pisco=ámbar, cinta=verde, cielo=azul, violeta=fiesta).
- La textura es **física**: flecos de papel que se mecen con la velocidad del scroll, grano de película, polaroids colgadas con pinzas.
- Los titulares son **citas literales** de su Instagram, en su ortografía ("usté", "colorssss").

## Ritmo

```
[cargador: Almud·cito·ito·ito]
HERO ─ video 100svh · ALMUD (Six Caps gigante) + BAR fino + isotipo · bio · horario
 ~~~ cinta de léxico: guarisnaque · güergüero · comilona ... (marquee)
HISTORIA ★ momento memorable: el isotipo (un almud, la medida chilota) se abre
          como ventana al video de la marca; la narración aparece frase a frase
MANIFIESTO ─ "Somos su Almudcito ito ito desbordando amor..." palabra a palabra en colores
 ~~~ flecos
RINCONES ─ galería horizontal (sticky): barra · luces · salón · terraza techada · fogón · terraza · vista · cintas · Ojo Piojo
CARTA ─ pestañas · lista de nombres (los chistes) + panel con foto/descr/precio · promos de la semana (hoy resaltado)
COMILONA ─ masas de fotos a distinta velocidad + citas
JORNADAS ─ tablero de afiches y fotos de eventos (año + cita)
EQUIPO ─ polaroids colgadas de un cordel con pinzas
RESEÑAS ─ carrusel internacional (es/en/fr) con arrastre
CÓMO LLEGAR ─ foto de la puerta + mapa diferido + horarios + DM
PIE ─ "Besiiiii 😘" gigante · créditos de fotógrafos
```

## Momento memorable
"El almud se abre": sección de 320vh con hijo sticky. El isotipo (caja de madera vista desde arriba) ocupa el centro; con el scroll, su cara superior (rombo) se transforma — clip-path de polígono — en una ventana a pantalla completa que muestra el video de la marca (IG-061, recortado para quitar los subtítulos quemados). La narración original aparece en Six Caps, frase por frase. Botón de sonido con barras para escuchar la voz real.

## Movimiento
- Curvas: `expo.out` / `cubic-bezier(.16,1,.3,1)`; 0,6–1,1 s. Entradas rápidas, salidas suaves.
- Revelados con máscara (líneas que suben dentro de su caja).
- Parallax con `inset` negativo del medio, nunca secciones más altas que la pantalla salvo las sticky.
- Flecos: `skewX` según velocidad de Lenis (se mecen al bajar rápido).
- Polaroids: leve balanceo con la velocidad.
- Micro: botones magnéticos, subrayados que crecen, etiqueta "Arrastrar" en carruseles, menú a pantalla completa con imagen al pasar.
- `prefers-reduced-motion`: todo visible, sin sticky animado (la galería horizontal pasa a scroll nativo), sin video autoplay.
