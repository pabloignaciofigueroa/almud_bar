# Textos de página v3 · Almud Bar

Fase 6 del plan v3 (`_plan/PLAN_v3.md`). Agente Textos de página. Aquí se decide qué palabras van en cada pantalla y cuáles sobran. La regla es mínimo texto: hablan las fotos y los videos. Cada texto tiene que ser claro para un turista y verse premium.

**Manda sobre** `content/copy-v2.md`. De la v2 se reusan fuentes y hallazgos, no textos.
**Vinculantes:** `_plan/v3/02-titulares-aprobados.md` (titulares de Carmen Paz, que van tal cual), `_plan/v3/03-04-validacion-carmen.md` (botones, sin RESERVAR) y `content/brand-voice-v3.md` (frases aptas y prohibidas).

## 0. Cómo leer este archivo

- `«…» [FUENTE]`: texto literal de Almud. Las fuentes son:
  - `[IG-NNN]`: caption, en `content/ig_posts.json`.
  - `[BIO]`: `content/bio.txt`.
  - `[CARTA-n]`: `content/carta-v2.json`.
  - `[TAG-001]`: etiquetas de persona en las 6 fotos de IG-001, tomadas de `assets/raw/ig/posts_new.json` (`usertags`).
  - `[DATO]`: `content/research_web.md`.
  - `[RESEÑA:autor]`: `content/reviews.json`.

  Solo se usan recortes contiguos, sin cambiar palabras. Los emoji se quitan.
- `‹…› [UI]`: etiqueta de interfaz nuestra. Es mínima, neutra y sin artículos.
- `“…”` en la columna EN: glosa nuestra para el turista. En modo EN, las etiquetas [UI] se reemplazan por su EN y los literales de Almud se quedan en español con la glosa debajo (`lang="en"`, tamaño de cuerpo, nunca en display). Los nombres de la carta, de los eventos y «Ojo Piojo» no se traducen. Si hace falta, se aclaran entre corchetes.
- La columna **Cuenta** dice si el texto entra en la meta de ≤ 150 palabras visibles: `sí`, `no·reseña` (sección Reseñas, salvo su titular) o `no·carta` (nombres y precios de la carta destacada).
- La pantalla no lleva otros textos que los de estas tablas. Si un texto no está aquí, no va.

---

## Nav (fija; aparece al dejar la portada)

| Elemento | ES visible | Fuente | EN | Cuenta |
|---|---|---|---|---|
| Logo | (SVG `brand/almud-horizontal-oscuro.svg`, sin texto) | — | — | — |
| Carta | ‹Carta› | [UI] | “Menu” | sí |
| Idioma | ‹EN› | [UI] | ‹ES› | sí |

---

## 1. Portada

Logo, claim de la bio y botones, sin otra frase (nota 4 de Carmen). El video (techo de cintas o letrero) habla solo, sin texto encima.

| Elemento | ES visible | Fuente | EN | Cuenta |
|---|---|---|---|---|
| Logo | (SVG con isotipo; alt “Almud Bar”) | — | — | — |
| Claim | «Coctelería de autor, comida & música bonita desde 2014» | [BIO] | “Signature cocktails, food & lovely music since 2014” | sí |
| Botón principal (muro rosa) | ‹Ver la carta› | [UI] | “See the menu” | sí |
| Botón 2 → mapa | ‹Cómo llegar› | [UI] | “Get directions” | sí |

---

## 2. El lugar

| Elemento | ES visible | Fuente | EN | Cuenta |
|---|---|---|---|---|
| Titular | «Somos inquietos y nos gusta el colorssss!» | [IG-111] | “We're restless and we love colour!” | sí |
| Rincón | ‹Barra› | [UI] | “The bar” | sí |
| línea | «Pucha que nos gusta nuestra barrita!» | [IG-087] | “We really love our bar!” | sí |
| Rincón | ‹Salón› | [UI] | “The room” | sí |
| Rincón | ‹Terraza techada› | [UI] | “Covered terrace” | sí |
| línea | «Techamos parte de la terraza» | [IG-004] | “We roofed part of the terrace” | sí |
| Rincón | ‹Terraza› | [UI] | “Terrace” | sí |
| línea | «Amamos los atardeceres desde nuestra terracita» | [IG-163] | “We love the sunsets from our little terrace” | sí |
| Rincón | ‹Lámparas› | [UI] | “The lamps” | sí |
| línea | «Nos gustan los brillitos, las luces» | [IG-147] | “We love the sparkle, the lights” | sí |
| Rincón | «Ojo Piojo» | [IG-118] | “Ojo Piojo [mural of eyes]” | sí |
| línea | «una mirada vale más que mil palabras» | [IG-118] | “a look is worth a thousand words” | sí |

- Para el Salón no hay línea aprobada, así que va solo el nombre.
- **Sobran:** ‹Sillones›. El material es poco y la foto P114 no muestra los sillones (crítica 1 de la v2). Vuelve, solo con su nombre, si fase 7 consigue una foto que los muestre.
- La terracita va recortada, sin «ita ita» (nota 2 de Carmen), y una sola vez en el sitio.

---

## 3. Tragos

| Elemento | ES visible | Fuente | EN | Cuenta |
|---|---|---|---|---|
| Titular | «mucho amor, color y trabajo» | [IG-045] | “a lot of love, colour and work” | sí |
| Bajada | «innumerables horas de probar, probar y probar» | [IG-021] | “countless hours of tasting, tasting and tasting” | sí |
| Destacado | «Aquí te las traigo Peter» · «$ 6.700» | [CARTA-2] | “[pisco, elderflower, cranberry, bubble]” | no·carta |
| Destacado | «Sagüer on Faia» · «$ 7.900» | [CARTA-2] | “[spiced, slightly hot sour]” | no·carta |
| Destacado | «Sangría Foreva!» · «$ 6.500» | [CARTA-2] | “[Carménère, aged pisco, cinnamon]” | no·carta |
| Rótulo sin alcohol | ‹Mocktails› | [UI] | “Alcohol-free” | sí |
| Línea sin alcohol | «no dejamos a nadie ajuera» | [IG-011] | “we leave nobody out” | sí |
| Destacado sin alcohol | «La moto chantá» · «$ 6.400» | [CARTA-5] | “[mango, passion fruit, cucumber]” | no·carta |

- Sin botón propio: ‹Carta› va fija en la nav y cada destacado enlaza a su ítem en `carta/`.
- Destacados = tragos con foto propia de ese ítem, igual que en la v2 §6b (V038, V030, P228, P336). Fase 7 confirma la foto. Si una no queda, se saca el ítem; no se cambia por otro trago sin foto.
- **Sobra en todo el sitio:** «mejor los tomamos todos!» [IG-046] (veto 1 de Carmen).

---

## 4. Comida

| Elemento | ES visible | Fuente | EN | Cuenta |
|---|---|---|---|---|
| Titular | «una cocina sencilla pero más que sabrosona!» | [IG-022] | “a simple kitchen, but more than tasty!” | sí |
| Destacado | «Tukulito Sakayama» · «$ 15.900» | [CARTA-1] | “[marinated tuna tataki]” | no·carta |
| Destacado | «Camarón que se duerme» · «$ 15.900» | [CARTA-1] | “[baked shrimp clay pot]” | no·carta |
| Destacado | «Pizza dulzona» · «$ 12.500» | [CARTA-1] | “[sweet pizza: hazelnut, red berries]” | no·carta |

- **Sobra:** «pa chuparse el bigoteli», que está vetada en todo el sitio. Como está dentro de la descripción del Tukulito en la carta, solo puede aparecer en `carta/`.

---

## 5. Con quién

| Elemento | ES visible | Fuente | EN | Cuenta |
|---|---|---|---|---|
| Titular | «no somos ná sin ustedes!» | [IG-026] | “we're nothing without you!” | sí |

- No lleva más texto. Las fotos de noches cualquiera dicen el "para qué".
- **Sobran:** los rótulos de ocasión de la v2 (‹Solo›, ‹En pareja›…) y sus líneas: «pa usté solit@…» lleva @, y «Pa agarrar perso…» es de carrete.

---

## 6. Eventos (calendario)

| Elemento | ES visible | Fuente | EN | Cuenta |
|---|---|---|---|---|
| Titular | «tirar la casa por la ventana!» | [IG-010] | “going all out!” | sí |
| Mes | ‹Feb› | [UI] | “Feb” | sí |
| Evento | «14F» | [IG-116] | “14F [Valentine's Day]” | sí |
| Mes | ‹Jul› | [UI] | “Jul” | sí |
| Evento | «Aniversario» | [IG-090] | “Anniversary” | sí |
| Mes | ‹Sep› | [UI] | “Sep” | sí |
| Evento | «Fondita» | [IG-080] | “Fondita [national holidays]” | sí |
| Evento | «Negroni Week» | [IG-005] | “Negroni Week” | sí |
| Mes | ‹Oct› | [UI] | “Oct” | sí |
| Evento | «Jalogüín» | [IG-071] | “Jalogüín [Halloween]” | sí |
| Marca | ‹Próximo› | [UI] | “Next” | sí |

- **Regla de ‹Próximo›.** Va en dorado (`--dorado`, cambio P2) en el primer evento del calendario cuyo mes sea igual o posterior al mes en curso, con la hora de `America/Santiago`. Si no queda ninguno, pasa al primero del año. Hoy, 21-10-2026, marca **Jalogüín (Oct)**. Sin JS no se marca nada.
- El calendario solo muestra el mes y el nombre. No lleva días, años futuros ni frases de promesa: no se anuncia ninguna edición.
- «Fondita» es un recorte contiguo de «nuestra fondita ita ita!!» [IG-080], sin la cascada. «Aniversario» sale de «No superamos nuestro aniversario!» [IG-090].
- **Sobran:**
  - «chaolin bombín al verano» [IG-030]: son 4 palabras y la edición 2026 se hizo en un local ajeno.
  - «Tiki Night» [BIO]: fue una sola noche, dentro del aniversario de 2025.
  - Bendita Primavera: fue una sola vez, en 2024.
  - «Nos vemos en las próximas cositas…» [IG-010]: es una promesa.

---

## 7. Equipo

| Elemento | ES visible | Fuente | EN | Cuenta |
|---|---|---|---|---|
| Titular | «Peazo de equipo que tenemos!» | [IG-048] | “What a team we've got!” | sí |
| Foto 1 | «@milagroosjm» | [TAG-001] | = | sí |
| Foto 2 | «@javier.agmc» | [TAG-001] | = | sí |
| Foto 3 | «@eduu.ardoo» | [TAG-001] | = | sí |
| Foto 4 | «@lizzearellano» | [TAG-001] | = | sí |
| Foto 5 | «@pablete_bartender_» | [TAG-001] | = | sí |
| Foto 6 | «@elymar_bocarejo» | [TAG-001] | = | sí |

- **Quiénes siguen.** IG-001 (07-10-2026) es el último posteo de equipo. Su caption no trae @, pero cada una de sus 6 fotos etiqueta a una persona: `DeNQ8A2lDgg_00`…`_05`, en el orden de la tabla. Esas 6 personas son el equipo. Cada @ va bajo su propia foto y enlaza a su perfil.
- **@lizzearellano** se escribe como en la etiqueta, que es la cuenta real. Con esto se resuelve la duda de la v2 entre «lizzearellano» y «lizzearellanol».
- **Sobran:**
  - Los otros @ de IG-010 (@jaav11, @daweed.cagliano, @haqum.v99) y los de IG-048 que no salen en IG-001.
  - Los dueños (@cepaz, @rusio_mezclao): no están en IG-001 y no tienen foto confirmada (inventario). Se agregan solo si Carmen lo pide.
  - El cuerpo de la v2: «Est@s guapetones…» habla del físico de las personas.

---

## 8. Reseñas

| Elemento | ES visible | Fuente | EN | Cuenta |
|---|---|---|---|---|
| Titular | «Que no se lo cuenten» | [IG-024] | “Don't just take their word for it” (obligatoria) | sí |
| R1 `lang="fr"` | «Super soirée à Castro ! Le service est sympa, super ambiance, avec musique très sympa!» | [RESEÑA:Dorothee M] | “Great night out in Castro! Friendly service, great atmosphere, really nice music!” | no·reseña |
| firma | ‹Dorothee · Épinal, Francia · Tripadvisor› | [UI] | “Dorothee · Épinal, France · Tripadvisor” | no·reseña |
| R2 `lang="en"` | «Really cute place. Good menu including lots of vegetarian options» | [RESEÑA:Rachael Fox] | (original) | no·reseña |
| firma | ‹Rachael · Takaka, Nueva Zelanda · Tripadvisor› | [UI] | “Rachael · Takaka, New Zealand · Tripadvisor” | no·reseña |
| R3 `lang="es"` | «De los mejores bares que he visitado. Tienen una terraza maravillosa.» | [RESEÑA:Oscar] | “One of the best bars I've been to. They have a wonderful terrace.” | no·reseña |
| firma | ‹Oscar · Santiago, Chile · Tripadvisor› | [UI] | “Oscar · Santiago, Chile · Tripadvisor” | no·reseña |
| R4 `lang="fr"` | «cela nous a fait bien plaisir de tomber sur un vrai bar» | [RESEÑA:Emilie A] | “it made us very happy to come across a real bar” | no·reseña |
| firma | ‹Emilie · París, Francia · Tripadvisor› | [UI] | “Emilie · Paris, France · Tripadvisor” | no·reseña |
| R5 `lang="en"` | «Cool waiters, great food and comfy seats» | [RESEÑA:Benjamín] | (original) | no·reseña |
| firma | ‹Benjamín · Puerto Varas, Chile · Tripadvisor› | [UI] | “Benjamín · Puerto Varas, Chile · Tripadvisor” | no·reseña |
| R6 `lang="es"` | «La atención es muy cálida y cercana.» | [RESEÑA:Dana] | “The service is very warm and personal.” | no·reseña |
| firma | ‹Dana · Castro, Chile · Tripadvisor› | [UI] | “Dana · Castro, Chile · Tripadvisor” | no·reseña |

- **Mezcla:** dos en francés, dos en inglés y dos en español. Son cuatro orígenes: Francia, Nueva Zelanda, Santiago y Castro.
- **Cómo se citan:** las citas son recortes contiguos con la ortografía original («Decor», «a la carte», «Castro !»). Se firma con el nombre de pila, sin apellido ni inicial. Ninguna habla de filas ni de espera.
- **Glosa.** En modo EN, las reseñas en francés y en español llevan la glosa EN debajo, en tamaño chico. En modo ES se muestran solo en su idioma original; las de francés pueden llevar una glosa [ES] opcional en tamaño chico.
- **Alternativas sin origen:** se quedaron fuera porque `reviews.json` no trae su país, aunque son las favoritas de Carmen:
  - «The bar tenders are artists, sit on the bar and watch.» [RESEÑA:Ai T] (Google)
  - «the food isn't an afterthought – it's fantastic.» [RESEÑA:Holger K] (Google)

  Si se acepta firmar solo con ‹Google› [UI], cualquiera de las dos puede reemplazar a R5.

---

## 9. Cuándo y dónde

| Elemento | ES visible | Fuente | EN | Cuenta |
|---|---|---|---|---|
| Titular | «Le esperamos desde las 18:00 hrs» | [IG-155] | “We're expecting you from 6 pm” | sí |
| Días | «Mar a Sáb» | [BIO] | “Tue to Sat” | sí |
| Dirección | «Serrano 325, Castro» | [BIO] | “Serrano 325, Castro” | sí |
| Referencia | «Al frente del Centro Cultural de Castro» | [DATO] | “Opposite the Castro Cultural Centre” | sí |
| Botón → `https://ig.me/m/almud_bar` | ‹Escríbenos por DM› | [UI] | “Message us on Instagram” | sí |
| Botón → mapa de Google (Serrano 325) | ‹Cómo llegar› | [UI] | “Get directions” | sí |

- **Horario.** Es el de la bio y nada más. «Mar a Sáb» es un recorte contiguo de «Abrimos de Mar a Sáb a las 18:00hrs» [BIO], y el titular ya dice la hora. No lleva hora de cierre, teléfono, lunes ni reservas.
- **Mapa.** Va estático hasta que se toca. El título del iframe es ‹Mapa: Serrano 325, Castro› [UI] (solo para el lector de pantalla, no es visible).
- **Sobran:**
  - «Abrimos de Mar a Sáb a las 18:00hrs» completo: repetiría la hora del titular.
  - ‹Horario› y ‹Dirección› como rótulos.
  - «Nuestro bazar @bazar_almud» [BIO].
  - Los rótulos ‹Instagram› y ‹@almud_bar›: el botón DM ya lleva a Instagram.

---

## 10. Pie

| Elemento | ES visible | Fuente | EN | Cuenta |
|---|---|---|---|---|
| Firma | «USTÉ SE LO MERECE!» | [IG-087] | “You deserve it!” | sí |
| Rótulo créditos | ‹Imágenes› | [UI] | “Images” | sí |
| crédito | «@catarsis.fotografia» | [IG-163] | = | sí |
| crédito | «@estudiouno.prod» | [IG-064] | = | sí |
| crédito | «@tamillanquileo» | [IG-126] | = | sí |
| crédito | «@isosur.prod» | [IG-009] | = | sí |
| crédito | «@rober.patagonico» | [IG-103] | = | sí |
| Rótulo créditos | ‹Afiches› | [UI] | “Posters” | sí |
| crédito | «@dosistudio» | [IG-081] | = | sí |

- **Cómo acredita la marca.** Almud firma sus fotos con «📸: @…» y sus videos con «🎥: @…» o «Video: @…». Como los emoji no van en el texto visible, se agrupan bajo ‹Imágenes›, palabra que usa la propia marca: «las imágenes de @estudiouno.prod» [IG-050]. Los afiches se acreditan aparte: «El afiche, como siempre, de manos de la querida @dosistudio» [IG-081].
- **Qué créditos quedan.** Solo los autores cuyas fotos o videos use la fase 7. Si un autor no queda en el sitio, se borra su @. Cada @ enlaza a su perfil.
- **Sobran:**
  - «Que no se lo cuenten! Besiiiii» (firma de la v2): Besi está prohibido y «Que no se lo cuenten» ya es el titular de Reseñas.
  - La nota ‹Hecho con fotos, textos y carta…›.
  - La línea ©.
  - La repetición de horario y dirección.

---

## C. Página Carta (`carta/`)

| Elemento | ES visible | Fuente | EN |
|---|---|---|---|
| Título | ‹La carta› | [UI] | “The menu” |
| Bajada | «tenemos pa todos los gustos!» | [IG-011] | “something for every taste!” |
| Sección 1 | «Coctelería de la casa» | [CARTA-2] | “House cocktails” |
| Sección 2 | «Cócteles del mundo mundial» | [CARTA-3] | “Cocktails from all over the world” |
| Sección 3 | «Espirituosos» | [CARTA-4] | “Spirits” |
| Sección 4 | «Vinos & espumantes» | [CARTA-6] | “Wines & sparkling” |
| Sección 5 | «Mocktails sin alcohol» | [CARTA-5] | “Alcohol-free cocktails” |
| Sección 6 | «Jugos & bebidas» | [CARTA-5] | “Juices & soft drinks” |
| Sección 7 | «Cervezas sin alcohol» | [CARTA-5] | “Alcohol-free beers” |
| Sección 8 | «Bebidas calientes» | [CARTA-5] | “Hot drinks” |
| Sección 9 | «Comilona» | [CARTA-1] | “Comilona [food]” |
| Sección 10 | «Nuestras promos» | [CARTA-7] | “Our deals” |
| Nota promos | «de 18:00 a 22:00 hrs» · «* Siempre sujeto a stock! *» | [CARTA-7] | “6 to 10 pm · Always subject to stock!” |
| Enlace | ‹Carta oficial (PDF)› → `https://uqr.to/ppvi` | [UI] | “Official menu (PDF)” |
| Enlace | ‹Inicio› | [UI] | “Home” |

**Grupos** (rótulos literales dentro de cada sección; el orden es el del PDF):
- «Cócteles del mundo mundial» [CARTA-3]: «Clásicos» [CARTA-3] · «Vermú» [CARTA-3] · «Mule» [CARTA-3] · «Negroni» [CARTA-3] · «Spritz» [CARTA-3] · «Sagüer» [CARTA-3] · «Mojitos» [CARTA-3] · «Red Bull te da aaalas» [CARTA-3]
- «Espirituosos» [CARTA-4]: «Piscolein o combinadito» [CARTA-4] · «Vodkita» [CARTA-4] · «Ron poromponpon» [CARTA-4] · «Whiscachos» [CARTA-4] · «Amamos el GIN!» [CARTA-4] · «Tequilazos & mezcalazos» [CARTA-4]
- «Vinos & espumantes» [CARTA-6]: «Tintelis» [CARTA-6] · «Blanquelis» [CARTA-6] · «Espumantes» [CARTA-6] · «Por copa» [CARTA-6]
- «Mocktails sin alcohol» [CARTA-5]: «Mocktails de la casa» [CARTA-5] · «Mocktails clásicos» [CARTA-5]
- «Comilona» [CARTA-1]: «Picoteos» [CARTA-1] · «Greditas» [CARTA-1] · «Sanguches» [CARTA-1] · «Pizzas artesanales» [CARTA-1] · «Pa los chichichos» [CARTA-1] · «Somos dulzones» [CARTA-1]

**Notas de la carta**
- **Títulos de sección.** CARTA-3, CARTA-4 y CARTA-6 no imprimen el título en la página; sale del nombre del archivo del PDF (lo dice `carta-v2.json › _fuente`). Al construir la página, el título de sección se lee de `carta-v2.json › secciones[].titulo`; no se reescribe a mano.
- **Glosas EN de los nombres.** Los nombres de ítems no se traducen. En modo EN, cada sección lleva su glosa bajo el título, y los grupos con juego de palabras se aclaran entre corchetes:
  - “Tintelis [reds]”
  - “Blanquelis [whites]”
  - “Whiscachos [whiskies]”
  - “Ron poromponpon [rum]”
  - “Vodkita [vodka]”
  - “Pa los chichichos [kids]”
  - “Somos dulzones [desserts]”
- **Texto de los ítems.** Nombre, descripción y precio salen tal cual de `content/carta-v2.json`. Esta página no tiene meta de palabras.
- **Caja.** Las mayúsculas en pantalla se ponen con CSS.
- **«Almudcito».** La nota «[Algunos recomendados de su Almudcito]» [CARTA-3] y la intro «ALMUDCITO PROMOS» [CARTA-7] son texto impreso en la carta y se respetan. Es el único lugar donde aparece la palabra.

---

## Conteo de palabras visibles (ES)

Regla: se cuentan como palabra todos los tokens separados por espacios que tengan una letra, un número o «&». Entran el titular de Reseñas, los botones, los rótulos, los @, la nav y el pie. Quedan fuera las citas y firmas de las reseñas, los nombres y precios de la carta destacada, y los textos que no se ven (alt y aria). Lo calcula el script de la sección siguiente.

<!-- CONTEO -->
| Sección | Palabras |
|---|---|
| Nav | 2 |
| 1 Portada | 14 |
| 2 El lugar | 45 |
| 3 Tragos | 17 |
| 4 Comida | 7 |
| 5 Con quién | 5 |
| 6 Eventos | 18 |
| 7 Equipo | 11 |
| 8 Reseñas (solo titular) | 4 |
| 9 Cuándo y dónde | 23 |
| 10 Pie | 12 |
| **Total landing (ES)** | **158** |

---

## Verificación

Script: `/tmp/claude-0/-home-claude/011b3bf8-fa11-50bd-ba3e-4cc567dfb832/scratchpad/verify_copy_v3.py`. Es una adaptación de `tools/verify_voice_v3.py` y queda fuera del repo. Hace cuatro cosas:
- **Literales.** Usa la misma normalización (sin emoji, minúsculas, espacios colapsados y sin espacio antes de un signo). Busca cada `«…» [FUENTE]` como subcadena de su fuente:
  - IG, BIO, CARTA y VID, como en el script original;
  - TAG-001: los `usertags` de IG-001 en `posts_new.json`;
  - DATO: `research_web.md`;
  - RESEÑA: la cita en `reviews.json` del autor indicado.
- **Terceros.** Rechaza las captions de terceros (IG-007, IG-028, IG-029 e IG-056).
- **Prohibidos.** Aplica la lista de prohibidos de `brand-voice-v3.md` §4 a todo texto ES visible de la landing, salvo los nombres de la carta. También revisa RESERVAR, «mejor los tomamos todos», «bigoteli», «Almudcito» y «Besi».
- **Conteo.** Cuenta las palabras (tabla de arriba) y sale con código 1 si hay fallas.

<!-- RESULTADO -->
