# Revisión del inglés · Almud Bar v4

Revisión de todo el texto EN que generan `tools/boceto_v4.py` (→ `nueva/index.html`) y `tools/carta_v4.py` (→ `nueva/carta/index.html`), más sus fuentes: `assets/v3/media.json` (`alt.en`), `content/carta-glosas-en-v3.json` y los diccionarios `GL`, `CHIP_EN`, `NOTA_EN`, `TAB`, `TAG` y `DAY_EN` de `carta_v4.py`. No se tocó ningún archivo del sitio.

**Ortografía: inglés de EE. UU.** Hoy el sitio mezcla inglés británico (colour, Centre, caramelised, coriander) con palabras de EE. UU. (clothespins, cilantro no aparece, "pm"). Propongo usar EE. UU. en todo el sitio. El turista angloparlante de Chiloé viene sobre todo de EE. UU. y Canadá, y en los menús de América el uso de EE. UU. es lo esperado. Los cambios son: color, colorful, colored, center, caramelized, cilantro (hojas), shrimp (no prawns), favorite.

**Limón:** el limón chileno de la carta es *lemon*. Hoy las glosas dicen unas veces lime y otras lemon para el mismo «limón». Propongo **lemon** en todas, salvo «limón sutil» (que sería *key lime*, pero no aparece en ninguna glosa).

**Leyenda.** **error**: inglés incorrecto o poco natural, mala traducción, o algo que falta y que el turista necesita. **mejora**: tono, naturalidad o coherencia.

---

## 1. Home — `tools/boceto_v4.py`

| # | Prioridad | Ubicación | Actual | Propuesto | Por qué |
|---|---|---|---|---|---|
| 1 | error | L189 `g()` claim del hero | Signature cocktails, food & lovely music since 2014 | Signature cocktails, food & good music since 2014 | «Lovely music» suena británico y de abuela. «Good music» es lo natural en un bar. |
| 2 | error | L341 meta description `data-en` | Signature cocktails, food &amp; lovely music since 2014. Serrano 325, Castro. | Signature cocktails, food &amp; good music since 2014. Serrano 325, Castro, Chiloé. | Mismo cambio que #1. Además «Chiloé» es lo que busca el turista. |
| 3 | error | L199 `title()` lugar | We're restless and we love colour! | Restless souls who love colorssss! | Ortografía US. Recupera el chiste de «colorssss», que la glosa perdía. |
| 4 | mejora | L113 rincón barra, glosa | We really love our bar! | Gosh, we love our little bar! | «Pucha» y «barrita»: hay que conservar la exclamación y el diminutivo cariñoso. |
| 5 | mejora | L114 rincón terraza techada, glosa | We roofed part of the terrace | Part of the terrace has a roof now | «We roofed» es seco y técnico. La versión propuesta es más natural y suena a novedad. |
| 6 | mejora | L116 rincón terraza, glosa | We love the sunsets from our little terrace | We love a sunset from our little terrace | «Love a…» es más coloquial y cálido. Opcional. |
| 7 | mejora | L117 rincón lámparas, etiqueta | The lamps | Lamps | Las otras etiquetas no llevan artículo (Covered terrace, Lounge, Terrace). |
| 8 | error | L117 rincón lámparas, glosa | We love the sparkle, the lights | We love a little sparkle and twinkly lights | La lista con coma suena a traducción literal. «brillitos» se traduce mejor como *a little sparkle*. |
| 9 | mejora | L118 rincón Ojo Piojo, etiqueta | Ojo Piojo [Mural of eyes] | Ojo Piojo [Heads up! · eye mural] | «Ojo piojo» es un modismo (= ¡atento!). La glosa explica el juego y no solo el objeto. |
| 10 | mejora | L118 rincón Ojo Piojo, glosa | A look is worth a thousand words | A look says more than a thousand words | La original es correcta. La propuesta sigue mejor el refrán inglés y suena menos calcada. Opcional. |
| 11 | error | L214 `title()` tragos | A lot of love, colour and hard work | Lots of love, color and hard work | Ortografía US. «Lots of» es más ligero y conversacional. |
| 12 | mejora | L226 glosa Sagüer (home) | [Spiced sour with a little heat] | [Spiced pisco sour with a little heat] | La carta dice «pisco sour». Las dos glosas deben coincidir, y «pisco» le da identidad al trago. |
| 13 | mejora | L227 glosa Sangría (home) | [Carménère wine, aged pisco, cinnamon] | [Carménère, aged pisco, cinnamon, fruit] | Alinea con la carta. «Carménère wine» es redundante. |
| 14 | error | L232 kicker mocktails `data-en` | Alcohol-free (sustituye a «Mocktails») | Mocktails | «Mocktails» ya es inglés. Al cambiarlo, el modo EN pierde la palabra clave que el turista busca. |
| 15 | mejora | L233 glosa «no dejamos a nadie ajuera» | We leave nobody out | Nobody gets left out! | Más natural y con exclamación, como el resto de las glosas de marca. |
| 16 | error | L245 `title()` comida | A simple kitchen, but more than tasty! | Simple food, but seriously tasty! | Aquí «cocina» es la comida, no el cuarto. «more than tasty» no es idiomático. «seriously tasty» recoge el «sabrosona». |
| 17 | mejora | L248 glosa pizzas | [Artisan pizzas] | [Handmade pizzas] | «Artisan» suena a marketing de supermercado. La carta dice que las masas las hacen ellos. |
| 18 | ok | L252 glosa Tukulito (home) | [Marinated tuna tataki] | [Marinated tuna tataki] | Sin cambio (está bien). Se anota solo para que quede igual que en la carta. |
| 19 | mejora | L147 evento Fondita | Fondita [Fiestas Patrias party] | Fondita [Chile's Independence Day party] | El turista no conoce «Fiestas Patrias». |
| 20 | mejora | L285 `title()` equipo | What a team we've got! | One heck of a team! | «Peazo de equipo» es más pícaro que «What a team». Opcional. |
| 21 | ok | L264 `title()` quién | We're nothing without you! | (sin cambio) | Correcto y con buen tono. |
| 22 | ok | L275 `title()` eventos | Going all out! | (sin cambio) | Buen equivalente de «tirar la casa por la ventana». |
| 23 | mejora | L158 reseña Emilie, traducción | it made us very happy to come across a real bar | we were so happy to stumble on a real bar | Más natural. Mantiene la minúscula inicial del original. |
| 24 | mejora | L160 reseña Dana, traducción | The service is very warm and personal. | The service is so warm and friendly. | En reseñas de hostelería en inglés, «warm and friendly» es la colocación natural de «cálida y cercana». |
| 25 | ok | L155, L157 reseñas Dorothee y Oscar | — | (sin cambio) | Traducciones fieles y naturales. |
| 26 | mejora | L307 `title()` dónde | See you from 6 pm | Doors open at 6 pm — see you there! | «See you from 6 pm» no se dice. La propuesta suena hospitalaria, como el «Le esperamos». |
| 27 | error | L310 dirección, referencia `data-en` | Opposite the Castro Cultural Centre | Across from the Castro Cultural Center | Ortografía US (Center). En EE. UU. se dice «across from». |
| 28 | mejora | L309 `dt` sr-only | Days | Open | El lector de pantalla oye «Open: Tue–Sat», que tiene más sentido. |
| 29 | ok | L313 y L314 botones | Message us on Instagram · Get directions | (sin cambio) | Correctos. |
| 30 | mejora | L323 glosa pie «USTÉ SE LO MERECE!» | You deserve it! | You've earned it, friend! | «Usté» es un trato cariñoso y burlón. «friend» le da ese guiño. Opcional. |
| 31 | mejora | L326 créditos `data-en` | Images | Photos & video | Bajo ese título hay créditos de fotógrafos y productoras de video. «Images» suena genérico. |
| 32 | ok | L168, L171, L172, L173, L191, L238, L258 UI | Skip to content · Main · English/Español · Menu · See the menu · See the full menu | (sin cambio) | Correctos y concisos. |

## 2. Alt y aria de fotos y videos — `assets/v3/media.json` (`alt.en`)

Solo los que se usan en `nueva/`.

| # | Prioridad | Clave | Actual | Propuesto | Por qué |
|---|---|---|---|---|---|
| 33 | error | images.lugar-terraza-techada | …thousands of coloured ribbons, heaters glowing. | The covered terrace packed with people under a ceiling of thousands of colored ribbons, heaters glowing. | US: colored. |
| 34 | error | images.con-quien-risa | …a wall of vertical coloured ribbons. | A woman bursts out laughing at her table, in front of a wall of colored ribbons hanging vertically. | US. «vertical colored ribbons» se lee mal. |
| 35 | error | images.con-quien-brindis | …under the coloured-ribbon ceiling… | A table toasts under the colored-ribbon ceiling, next to a lit patio heater. | US. |
| 36 | error | images.equipo-milagros | …colourful paper fans behind her. | A member of the floor team smiles while serving a table, colorful paper fans behind her. | US. |
| 37 | error | images.carta-camaron | A black clay dish of prawns and mushrooms in a creamy sauce. | A black clay pot of shrimp and mushrooms in a creamy sauce. | US: shrimp. Coincide con la glosa «Clay pot: shrimp…». |
| 38 | mejora | images.carta-saguer | A torch smokes an amber drink on a wooden coaster. | A kitchen torch smokes an amber drink on a wooden coaster. | «A torch» solo puede leerse como antorcha. Aclarar que es un soplete. |
| 39 | mejora | images.eventos-fondita | Almud's Fiestas Patrias "fondita": blue and orange paper lanterns… | Almud's "fondita" for Chile's Independence Day: blue and orange paper lanterns hanging among the ribbons over the busy terrace. | Igual que #19: hay que explicar qué es. |
| 40 | mejora | images.lugar-sillones | …patterned cushions and encaustic tiles. | …patterned cushions and patterned cement tiles. | «Encaustic tiles» es un término técnico poco conocido para la baldosa hidráulica. Opcional. |
| 41 | error | videos.portada-escritorio (aria) | The coloured-ribbon ceiling, the eye mural… | The colored-ribbon ceiling, the eye mural and the glowing clothespin lamps, one after another. | US. |
| 42 | error | videos.lugar-cintas (aria) | …thousands of coloured ribbons and warm lights. | A slow pan across the ceiling of thousands of colored ribbons and warm lights. | US. |
| 43 | error | videos.comida-cazuela (aria) | …with chopped coriander. | A creamy seafood stew bubbling in a black clay pot, topped with chopped cilantro. | US: cilantro para las hojas. |
| 44 | mejora | videos.donde-letrero (aria) | The illuminated ALMUD BAR sign, the camera tilting down to… | The lit-up ALMUD BAR sign; the camera tilts down to the glass-and-wood front door. | La construcción absoluta suena forzada. «front door» es más natural. |
| 45 | ok | resto de alts usados (lugar-barra, lugar-terraza-abierta, lugar-lampara-pinzas, lugar-ojo-piojo, tragos-*, comida-pizza, con-quien-barra/amigos/solo, eventos-10/12-anos, eventos-jaloguin, carta-olvidar/sangria/coquette/moto/tukulito/contuti, equipo-javier/eduardo/liz/pablete, portada-celular, tragos-humo) | — | (sin cambio) | Descriptivos y concretos, sin «image of». |

*(Aunque no se usan en v4, los alts de `comida-ceviche`, `comida-hamburguesa`, `lugar-cuadros`, `eventos-primavera` y `equipo-grupo` también dicen coloured/colourful/caramelised/coriander. Conviene corregirlos en la misma pasada.)*

## 3. Carta — interfaz y estructura (`tools/carta_v4.py`)

| # | Prioridad | Ubicación | Actual | Propuesto | Por qué |
|---|---|---|---|---|---|
| 46 | error | L221 meta description `data-en` | Something for every taste! House cocktails, classics, spirits, wines, alcohol-free and food. | Something for every taste! House cocktails, classics, spirits, wine, alcohol-free drinks and food. | «alcohol-free» queda como adjetivo sin sustantivo. |
| 47 | mejora | L39 TABS `vinos` | Wines | Wine & bubbly | La pestaña incluye espumantes. «bubbly» mantiene el tono juguetón. |
| 48 | mejora | L37 TABS `mundo` | World classics | Classic cocktails | «World classics» es ambiguo (¿música?, ¿comida?). Si se quiere el chiste de «mundo mundial», sería «Classics from around the world». |
| 49 | error | L42 TABS `promos` | Deals | Happy hour | Son promos diarias de 18:00 a 22:00: en inglés eso es happy hour, y es lo que busca el turista. |
| 50 | mejora | L44 GL, glosas de cabecera | [reds] · [whites] · [whiskies] · [rum] · [vodka] · [kids] · [desserts] | [Reds] · [Whites] · [Whiskies] · [Rum] · [Vodka] · [Kids] · [Desserts] | Coherencia: las demás cabeceras (Classics, Sours, Small plates…) van con mayúscula. |
| 51 | mejora | L46 GL `Jugos & bebidas` | Juices & soft drinks | Juices & sodas | En US se dice «soda». «soft drinks» es UK. Aplicar también en CHIP_EN, L49. |
| 52 | mejora | L50 CHIP_EN `Pizzas artesanales` | Pizzas | Handmade pizzas | Coherencia con #17. |
| 53 | mejora | L52 CHIP_EN `Amamos el GIN!` | Gin | We love gin! | Es una frase de la marca con exclamación. La glosa debería guardar el entusiasmo. |
| 54 | mejora | L50 CHIP_EN `Greditas` | Clay pots | Clay-pot bakes | «Clay pots» solo puede leerse como macetas. Así queda claro que es comida al horno. |
| 55 | mejora | L55 NOTA_EN `Elija su medida 90 o 150 cc!` | Choose 90 or 150 cc | Pick your pour: 90 or 150 ml | Más natural y con el tono de la marca. En inglés se usa «ml», no «cc». |
| 56 | mejora | L56 NOTA_EN pie Whiscachos | [No mixer included] | [No mixer — for those who like it neat] | Conserva el chiste del «puritano». |
| 57 | mejora | L57 NOTA_EN promos | 6 to 10 pm · Always subject to stock! | 6–10 pm · While supplies last! | «Subject to stock» es UK y de letra chica. «While supplies last» es la fórmula US. |
| 58 | error | L54 NOTA_EN «Precio del corto normal…» | Single or XL pour · mixer not included | Regular or XL pour · mixer not included | Las columnas dicen «NORMAL/CORTO» y «XL»: «Regular» calza con la carta. |
| 59 | error | faltan glosas (nuevas claves NOTA_EN) | Vermú nota «UN VERMUCITO CON UNA TÓNICA QUEDA PICHO CALUGA!»: sin glosa | [Vermouth & tonic? Chef's kiss!] | El chiste queda fuera para el lector EN. |
| 60 | error | faltan glosas | Vermú pie «AGREGUE UNA TÓNICA… $3.700»: sin glosa | [Add a Fentimans tonic for $3.700] | Es un precio. El turista lo necesita. |
| 61 | error | faltan glosas | Mule nota «DESTILADO + GINGER BEER, JUGO DE LIMÓN, MENTA Y SODA»: sin glosa | [Spirit + ginger beer, lemon, mint & soda] | Explica todo el grupo. |
| 62 | error | faltan glosas | Gin nota «Puede pedir un corteli o el gin&tonic…»: sin glosa | [Neat pour or G&T with a Fentimans tonic (200 ml): classic, rose lemonade or Valencian orange] | Explica las dos columnas de precio. |
| 63 | error | faltan glosas | Tequila nota «Shot de 75 cc acompañado de limón & sal»: sin glosa | [75 ml shot with lemon & salt] | Información práctica. |
| 64 | error | faltan glosas | Whiscachos nota «…cortos de 2 oz [60 ml]»: sin glosa | [Our fanciest pours · 2 oz (60 ml)] | Información práctica, con el guiño de «pituqueli». |
| 65 | error | faltan glosas | Pa los chichichos nota «[Para menores hasta 12 años]»: sin glosa | [Ages 12 and under] | Es una regla del local. |
| 66 | error | faltan glosas | Pizzas pie «…puedes pedir cualquiera miti mota, menos la Zorrona, la Terrible Pollo y la Blanquita»: sin glosa | [Our dough is homemade! Any pizza can be half-and-half, except Zorrona, Terrible pollo and Blanquita] | Es una regla de pedido. |
| 67 | mejora | faltan glosas | Pizzas nota «Con base de pomodoro casera y queso mozzarella» | [Homemade tomato sauce & mozzarella base] | Ayuda a leer las pizzas. |
| 68 | mejora | faltan glosas | Greditas nota «Base de papas en cubitos, al horno. Macanúo pa compartir!» | [On a bed of baked diced potatoes · great for sharing!] | Explica qué es una gredita. |
| 69 | mejora | faltan glosas | Sanguches pie «Todas las salsitas… masa mami y mucho amor» | [All sauces made in-house, on sourdough bread, with lots of love] | Tono de marca y dato de producto. |
| 70 | mejora | faltan glosas | Clásicos nota «[Algunos recomendados de su Almudcito]» | [A few favorites from your Almudcito] | Coherencia: el resto de las notas va glosado. |
| 71 | mejora | faltan glosas | Mocktails nota «COCTELCITOS SIN ALCOHOL» | [Alcohol-free cocktails] | Coherencia. |
| 72 | mejora | faltan glosas | Grupo «Red Bull te da aaalas»: sin glosa | [Red Bull gives you wiiings] | Juego de palabras fácil de conservar. |
| 73 | error | faltan glosas en ítem | Espumantes · Undurraga Free Rosé `nota: [sin alcohol]` | [alcohol-free] | Dato crítico para quien no bebe. |
| 74 | mejora | faltan glosas en ítem | Por copa · `nota: [botellita 187 cc]` | [187 ml mini bottle] | Dato práctico. |
| 75 | mejora | faltan glosas en ítem | Tom Collins `nota: Puedes pedirlo con gin frutilla!` | [Also with strawberry gin] | Dato práctico. |
| 76 | mejora | L153 cabeceras de tabla | NORMAL [90 cc] · CORTO [90 cc] · CORTO XL [150 cc] · GIN & TONIC | Añadir `data-en`: REGULAR [90 ml] · XL [150 ml] · G&T | Hoy las columnas de precio no tienen EN. |
| 77 | ok | L245, L247, L248, L249, L255, L256, L259, L262, L263 UI | Skip to content · Almud Bar · Home · Menu · Message us on Instagram · The menu · something for every taste! · Menu sections · Official menu (PDF) · Home | (sin cambio) | Correctos. Opcional: «Home» → «Back home». |
| 78 | ok | L58 DAY_EN y L59 TAG | Tue/Wed/… · New, Veggie, Vegan, Spicy | (sin cambio) | Correctos. |

## 4. Carta — glosas de ingredientes (`content/carta-glosas-en-v3.json`)

| # | Prioridad | Clave | Actual | Propuesto | Por qué |
|---|---|---|---|---|---|
| 79 | mejora | Pinche Güey | [Mezcal, tequila, toasted peanut horchata, merkén, grapefruit, lime · smoky, a little spicy] | [Mezcal, tequila, toasted-peanut horchata, merkén (smoked chili), grapefruit, lemon · smoky, a little spicy] | Explica qué es el merkén. Usa lemon, como dice la nota de arriba. |
| 80 | mejora | Aquí te las traigo Peter | [Pisco, elderflower liqueur, cranberry, lime · topped with a smoke bubble] | […, cranberry, lemon · topped with a smoke bubble] | Lemon (coherencia). |
| 81 | mejora | Cómo te voy a olvidar | [Pear vodka, lime, syrup, red wine float] | [Pear vodka, lemon, syrup, red wine float] | Lemon (coherencia). |
| 82 | mejora | Not Collins | [Amaretto, syrup, lemon, soda · sweeter Tom Collins] | [Amaretto, syrup, lemon, soda · a sweeter take on the Tom Collins] | Falta el artículo: así suena telegráfico. |
| 83 | mejora | Te espero en la cuneta | [Tequila, curaçao, lime, pineapple · sweeter margarita] | [Blanco tequila, curaçao, lemon, pineapple · a sweeter take on the margarita] | Igual que #82. |
| 84 | mejora | Deja tomao | [Gin, cucumber, mango, lime, honey] | [Gin, cucumber, mango, lemon, honey] | Lemon (coherencia). |
| 85 | mejora | Desde que te conocí | [Ramazzotti, passion fruit, lime, sparkling wine] | [Ramazzotti, passion fruit, lemon, sparkling wine] | Lemon (coherencia). |
| 86 | error | Tranquilein John Wayne | [Blended scotch, …] | [Blended Scotch, apple juice, cinnamon syrup, lemon] | «Scotch» lleva mayúscula (denominación de origen). |
| 87 | mejora | A veces me pongo Coquette | [Berry pisco, whisky cream, raspberry, orange, cinnamon · creamy, pink] | [Berry pisco, whisky cream liqueur, raspberry, orange, cinnamon · pink and creamy] | «whisky cream» solo es ambiguo. «pink and creamy» suena más natural. |
| 88 | mejora | Iquique Glorioso | [Trä·kàl, pisco, passion fruit, mango, pineapple] | [Trä·kàl (Patagonian apple-pear spirit), pisco, passion fruit, mango, pineapple] | El turista no sabe qué es Trä·kàl, y la carta misma lo explica. |
| 89 | mejora | La moto chantá | […, lime · salt rim] | [Mango, passion fruit, cucumber, lemon · salt rim] | Lemon (coherencia). |
| 90 | mejora | Embolinando la perdiz | [Grapefruit, apple, honey, lime, mint] | [Grapefruit, apple, honey, lemon, mint] | Lemon (coherencia). |
| 91 | mejora | Efecto placebo | [Raspberry, passion fruit, lime, mint, tonic] | [Raspberry, passion fruit, lemon, mint, tonic] | Lemon (coherencia). |
| 92 | mejora | Six Seven | [Pineapple, almond syrup, lime] | [Pineapple, almond syrup, lemon] | Lemon (coherencia). |
| 93 | mejora | Mojito sin alcohol | [Virgin mojito · honey, ginger or passion fruit] | [Virgin mojito · try it with honey, ginger or passion fruit] | Hoy parece una lista de ingredientes: son opciones. |
| 94 | mejora | Pisco sagüer sin alcohol | [Alcohol-free pisco sour · honey, ginger or passion fruit] | [Alcohol-free pisco sour · try it with honey, ginger or passion fruit] | Igual que #93. |
| 95 | mejora | Tukulito Sakayama | [Marinated tuna tataki, bread, house sauce] | [Marinated tuna tataki with house bread and sauce] | Más fluido. |
| 96 | mejora | Una cosa poca | [Baked cheese fondue with tomato, avocado and pesto, bread] | [Chilean-style baked cheese fondue with tomato, avocado and pesto, house bread] | Recoge el chiste de «más mejor porque es shileno» y elimina la coma colgante. |
| 97 | mejora | Todo que ver! | [Tuna ceviche with avocado, pineapple, coconut and green curry] | [Red tuna ceviche with avocado, pineapple, coconut and green curry, house bread] | Completa la glosa: la carta dice que va con pan. |
| 98 | mejora | Muéveme el pollo | […, teriyaki · veggie option] | [Clay pot: chicken, cream, tomato, curry, peanuts, teriyaki · also comes veggie] | Más natural. |
| 99 | error | Chambreao | [Beef burger, cheese, caramelised onion, pickles, bourbon BBQ sauce] | [Beef burger, cheese, caramelized onion, dill pickles, bourbon BBQ sauce, sourdough bun] | US: caramelized. «sourdough» es un argumento de venta. |
| 100 | mejora | Hamburguesa Almud | [Lentil burger, avocado, tomato, greens · vegan] | [Lentil burger, avocado, tomato, greens, sourdough bun · vegan] | El pan de masa madre es dato de la carta. |
| 101 | mejora | Cabrone | [Goat cheese, avocado, roasted pepper, greens, ciabatta] | [Goat cheese, avocado, roasted red pepper, greens, sourdough ciabatta] | Más preciso. |
| 102 | error | Caprichosa | [Goat cheese, walnuts, olives, coriander] | [Goat cheese, walnuts, olives, cilantro] | US: cilantro (hojas). |
| 103 | error | Huerta sabrosa | [Cherry tomato, mushrooms, greens, garlic-coriander sauce] | [Cherry tomatoes, mushrooms, greens, garlic-cilantro sauce] | US: cilantro. Plural natural. |
| 104 | error | Blanquita | [White pizza: cream, mozzarella, avocado, caramelised onion, green chili] | [White pizza: cream, mozzarella, avocado, caramelized onion, green chili, merkén · spicy] | US. La versión propuesta además avisa del picante. |
| 105 | mejora | Cabras a la higuera | [Goat cheese, figs, glazed cherry tomato, balsamic] | [Goat cheese, figs, glazed cherry tomatoes, balsamic glaze] | Plural natural. «balsamic glaze» es la forma usual. |
| 106 | mejora | Zorrona | [Beef chunks, red onion, garlic, mushrooms, greens] | [Beef chunks (200 g), red onion, garlic, mushrooms, greens] | Dato que da la carta. Opcional. |
| 107 | mejora | Topiturrón | [Chocolate nougat, orange gel, berry sorbet] | [Chocolate nougat with cookies and nuts, orange-cranberry gel, berry sorbet] | Más fiel al ES, sin alargar mucho. |
| 108 | ok | Las otras 25 glosas (Guarever, Sagüer, Sangría, Ramón, Otra cosa mariposa, Soy una limonhada, Sangría/Ramazzotti/Piña colada sin alcohol, Aceitunas, La carne es débil, Con tuti, A ponerle wendy, Eres tan exótica, Campestre, Camarón que se duerme, Trufona, Chanchito azul, Tartufita, Terrible pollo, Pollito pío, Bartolito, La vaca Lola, Pizza dulzona, Crumblecito) | — | (sin cambio) | Naturales, cortas y fieles. |

---

### Resumen

- **98 cambios propuestos**: 33 marcados **error** y 65 **mejora**. Las filas 18, 21, 22, 25, 29, 32, 45, 77, 78, 108 son «ok» (sin cambio).
- Los «error» se dividen en tres grupos: ortografía UK frente a US (colour, Centre, caramelised, coriander, prawns), traducciones poco naturales (lovely music, A simple kitchen…, Alcohol-free en lugar de Mocktails, Deals) y glosas que faltan con información práctica (sin alcohol, edad de los chichichos, miti mota, precio de la tónica, tamaño de los shots).
- Hecho con lo que hay hoy en `nueva/`. Ningún texto en español, nombre de trago o nombre de plato fue tocado.
