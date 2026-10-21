# Fase 3 · Inventario de historias (cuentos) — Almud Bar v2

> Fuente: los 180 posts de `content/ig_posts.json` (dic-2022 → oct-2026) y las 4 destacadas (`assets/raw/hl/highlights.json`), cruzados con `_plan/diag/catalogo.csv`. Datos completos en `content/historias.json`.
> Cada post IG va en **un solo** cuento (`posts`). Los cruces van en `see_also`. Resultado: 180/180 asignados en 35 cuentos, más 3 destacadas.
> Las citas son literales: se extraen por programa desde la caption. Solo se quitan los glifos emoji (quedan anotados en `emoji_removed`) y el salto de línea se escribe " / ". Hay 5 posts con voz de terceros (IG-007, 028, 029, 033, 056), marcados con `voz`.
> **Fuerza (sobre 20)** = engagement (likes norm. medio, tope x3 → 0–5) + foto (top-3 épica×calidad → 0–5) + narrativa (juicio, 1–5) + "quién es Almud" (juicio, 1–5).

## 1. Ranking de cuentos por fuerza

| # | Cuento (`id`) | Tipo | Posts | ♥ total | Norm. medio | Fuerza | Años |
|---|---|---|---|---|---|---|---|
| 1 | aniversario-11 | aniversario | 4 | 861 | 2,37 | 17,3 | 2025 |
| 2 | equipo | equipo | 17 | 3195 | 1,95 | 16,7 | 2022–26 |
| 3 | aniversario-10 | aniversario | 8 | 1931 | 1,89 | 16,6 | 2024 |
| 4 | los-papis | equipo | 1 | 1488 | 15,42 | 16,4 | 2026 |
| 5 | aniversario-12 (+ destacada) | aniversario | 3 | 651 | 2,25 | 16,2 | 2026 |
| 6 | musica-en-vivo (Isleños) | colaboración | 2 | 706 | 6,08 | 16,0 | 2026 |
| 7 | gente-y-parroquianos | gente/clientes | 2 | 330 | 2,72 | 15,9 | 2025–26 |
| 8 | almud-rucalaf | colaboración | 3 | 748 | 4,30 | 15,7 | 2026 |
| 9 | fondita | fiesta/evento | 8 | 953 | 0,99 | 15,3 | 2023–26 |
| 10 | terraza-y-techo-de-cintas | espacio/obra | 13 | 1871 | 1,44 | 15,1 | 2023–26 |
| 11 | carta-y-nombres | tragos/carta | 12 | 921 | 0,74 | 14,6 | 2022–26 |
| 12 | techado-2026 | espacio/obra | 1 | 238 | 2,47 | 14,3 | 2026 |
| 13 | jaloguin | fiesta/evento | 6 | 929 | 1,38 | 14,1 | 2023–25 |
| 14 | el-almudcito-se-presenta | otro | 2 | 369 | 1,13 | 13,3 | 2024–25 |
| 15 | la-barrita | espacio/obra | 5 | 576 | 1,24 | 13,3 | 2023–26 |
| 16 | fin-de-ano-y-resumenes | otro | 8 | 1231 | 1,22 | 13,2 | 2022–25 |
| 17 | bendita-primavera | fiesta/evento | 3 | 467 | 1,18 | 12,4 | 2024 |
| 18 | aniversario-9 | aniversario | 6 | 892 | 1,50 | 12,4 | 2023 |
| 19 | lluvia-y-frio | ciudad/Castro | 9 | 640 | 0,73 | 12,4 | 2023–26 |
| 20 | ojo-piojo | espacio/obra | 2 | 228 | 1,06 | 12,3 | 2023–24 |
| 21 | mujeres-8m | equipo | 3 | 685 | 1,67 | 12,2 | 2023–25 |
| 22 | amor-14f (+ Orgullo) | fiesta/evento | 6 | 472 | 0,78 | 11,5 | 2024–26 |
| 23 | equipo-fin-de-ano | equipo | 4 | 660 | 1,23 | 11,3 | 2022–25 |
| 24 | castro-vista-y-atardeceres | ciudad/Castro | 2 | 173 | 1,08 | 11,3 | 2023, 2026 |
| 25 | solcito-y-verano | ciudad/Castro | 6 | 657 | 0,90 | 11,2 | 2023, 2025 |
| 26 | comilona | comida | 15 | 997 | 0,65 | 11,0 | 2023–26 |
| 27 | teik-aguei (solo destacada) | otro | 0 | — | — | 10,8 | 2020 |
| 28 | desfile-de-modas | colaboración | 4 | 908 | 1,26 | 10,7 | 2025 |
| 29 | chaolin-verano | fiesta/evento | 2 | 174 | 0,78 | 10,1 | 2024 |
| 30 | invitaciones-diarias | otro | 12 | 653 | 0,55 | 9,9 | 2023–26 |
| 31 | negroni (Week + martes) | tragos/carta | 3 | 100 | 0,41 | 9,4 | 2025–26 |
| 32 | promos-de-la-semana | tragos/carta | 5 | 310 | 0,63 | 9,3 | 2024–26 |
| 33 | mambo-tiki (+ destacada 2020) | fiesta/evento | 1 | 51 | 0,56 | 9,1 | 2020, 2025 |
| 34 | visitas-de-marca | colaboración | 1 | 132 | 1,00 | 8,1 | 2024 |
| 35 | bazar-y-gorritos | otro | 1 | 144 | 1,58 | 7,9 | 2025 |
Cómo leer el ranking:
- **Los aniversarios forman una saga.** Son cuatro cuentos (9, 10, 11 y 12 años), pero en la web van como un solo capítulo que cuenta el paso del tiempo.
- **los-papis, musica-en-vivo y almud-rucalaf** suben por engagement de terceros:
  - IG-007 es un reel de creadores (x15,4);
  - IG-028/029 son posts de Isleños;
  - la noche Rucalaf ocurrió en el patio de Rucalaf.
  Ninguna de sus frases fuertes está escrita en la voz de Almud, o el lugar no es Serrano 325.
- **Fondita, carta y comilona** tienen likes bajos (x0,7–1,0) y aun así cargan las mejores fotos (Fondita, P297) y los mejores juegos de palabras.
- **Mambo Tiki y Negroni Week**, dos de los eventos que se esperaban, son débiles como capítulo: un solo afiche o tres posts. Conviene que entren como líneas dentro de aniversarios y carta.
- **Teik Agüei** solo existe en stories, sin caption. Sus textos (#Teik agüei, #VOLVEREMOS, AlmudcitoenCasa) están transcritos en el catálogo y **hay que verificarlos a ojo** antes de citarlos.

## 2. Capítulos recomendados para la v2 (8)

Para el titular se toma un fragmento literal de ≤32 caracteres. Aritmética de Six Caps (k≈0,40) a 390 px, con 358 px útiles:
- a 96 px caben unos 9 caracteres por línea, así que solo los titulares de ≤18 caracteres caben en 2 líneas a ese tamaño;
- de 19 a 32 caracteres hay que bajar el display a ~56 px en móvil (16 caracteres por línea).

La barra indica el corte de línea sugerido.

### 2.1 El equipo (`equipo` + `mujeres-8m` + `equipo-fin-de-ano`)
- **Titular:**
  - «Peazo de equipo / que tenemos!» (28, IG-048)
  - «Somos una banda / variada» (23, IG-067)
  - «qué pedazo de team / tenemos!» (27, IG-010)
- **Foto decisiva:** `ig/DaWM8rlo1FR_00.jpg` (P333): dos garzonas con corbata y jockey, 3219 px, noche cálida, x3,27. Apoyos:
  - `ig/CqEI2nSJP2__00.jpg` (P036);
  - `ig/DEP9IUpR9G4_00.jpg` (P157, el equipo con el fiordo detrás; luz de día).
- **Texto literal:** «Se deslizan como angelitos, con trago en mano por los salones: la amada @lizzearellanol el ondero @eduu.ardoo y el más rápido del oeste @jano_cruz11» (IG-067). «Nada de esto sería posible sin la comilona delichus que nos trae el clan cocina que es O SEAAA, puro oro» (IG-067).
- **Por qué:** es la prueba sin adjetivos nuestros. Cada persona aparece con su apodo y su @. El cuento cubre 2022–2026 y suma 3195 ♥.

### 2.2 Los años (`aniversario-9 → 12`)
- **Titular:**
  - «Doce / años!» (10, IG-010)
  - «12 años de / tanto tanto» (22, IG-010)
  - «una década de tanto / tanto tanto!» (32, IG-101)
- **Foto decisiva:** `ig/DM_Ih5dyVKH_07.jpg` (P189): techo de banderines sobre la terraza llena, 5/5, x2,99. Hitos:
  - `ig/C9dHAAxJkSi_00.jpg` (P073, el "10" de flores);
  - `ig/Dbg3ekilC4P_11.jpg` (P348, la multitud de los 12 años; luz mixta).
- **Texto literal:** «Doce años! Cuánto coctelcito ha pasado bajo este puente, 12 años de tanto tanto, que valía la pena tirar la casa por la ventana!» (IG-010).
- **Por qué:** es el único cuento que se repite cada año con más fuerza: 9 (antifaces), 10 (concurso y década), 11 (Mambo Tiki y El Gobernador) y 12 (@isosur.prod). Se cuenta como línea de tiempo.

### 2.3 Fondita ita ita (`fondita`)
- **Titular:**
  - «nos sacamos una / fondita ita ita» (31, IG-081)
  - «Amamos el / diecioshoooo!!» (24, IG-006)
  - «Nos endieciochamos» (18, IG-043)
- **Foto decisiva:** `ig/DAMHps8JVVr_04.jpg` (P090): faroles y flecos sobre la gente, 5/5. Par para un split: `ig/DAMHps8JVVr_07.jpg` (P093, la barra curva completa).
- **Texto literal:** «Tendremos 4 días pa tirar el bar por la ventana desde hoy Martes 17 hasta el Viernes 20 le tendremos: terremotos, borgoñita, empanadas de horno, una beia decoración, toda la güena onda y hasta DJ nos sacamos hoy!» (IG-081). «Recuerde que también elegiremos la mejor paya! Sólo debes escribirla y dejarla con tu nombre en nuestras guirnaldas tricolor!» (IG-081).
- **Por qué:** tiene la serie de fotos más pulida y en la familia de luz de la casa. Se repite de 2023 a 2026 y la paya es un gesto propio.

### 2.4 La terraza y el techo de cintas (`terraza-y-techo-de-cintas` + `techado-2026`)
- **Titular:**
  - «nos gusta el / colorssss!» (23, IG-111)
  - «Tardes y nochecitas / de terraza!» (31, IG-160)
  - Epílogo 2026: «Techamos parte / de la terraza» (28, IG-004)
- **Foto decisiva:** `ig/CoIvWmcpFBq_00.jpg` (P021, 1332×1665: mesas bajo cintas verticales). El túnel P046 es más épico, pero solo mide 873 px y va en tamaño medio. Más material:
  - loop V009 (techo de flecos);
  - epílogo: `ig/Dd94G-HlL-W_04.jpg` (P385, el brasero nuevo).
- **Texto literal:** «Somos inquietos y nos gusta el colorssss! Tratando siempre de hacer nuestro Almudcito beio para su deleite, y también pa comer y empinar el codein en un lugar estimulante y boni boni!» (IG-111). «Techamos parte de la terraza, le pusimos todo el colors y calor del mundo mundial, pa que usté pueda disfrutar de su pucho tranquilein john wayne sin mojarse y calentit@, qué mejor?!» (IG-004).
- **Por qué:** es el "colors" de la marca hecho espacio y pasa de 2023 a la obra de octubre de 2026. El juego «tranquilein john wayne» es también un trago de la carta.

### 2.5 Nombres de tragos y comilona (`carta-y-nombres` + `comilona` + `negroni`)
- **Titular:**
  - «mejor los tomamos / todos!» (24, IG-046)
  - «Demasiada complikeichon / elegir» (30, IG-046)
  - «sencilla pero más / que sabrosona!» (32, IG-022)
- **Foto decisiva:** `ig/DYsZ0GNo_88_00.jpg` (P297): splash rojo en coupe, 5/5, 3177 px, en un "marco que crece". Apoyos: V038 (burbuja de humo, IG-044) y V054 (piel de naranja, Negroni).
- **Texto literal:** «Tantos creadores con tantísimo talento e innumerables horas de probar, probar y probar, con inmenso esfuerzo de todo nuestro sacrificado equipo, que debemos empinar una y otra vez, hasta llegar a la fórmula más macanúa - ardua pega!» (IG-021). «Este se llama EN QUÉ TOPAMOH?! y es como un Old Fashioned: bourbon, vino blanco fortificado, angostura, toque dulzón y al final un poco de burbuja, juertón pero dulcecito!» (IG-178).
- **Por qué:** los nombres son el chiste más propio de la casa. En captions aparecen Cómo te voy a olvidar, Aquí te las traigo Peter, Sagüer on Faia, La moto chantá, Con tuti si no pa qué! y Topiturrón. Tiene likes bajos, así que gana por texto y foto, no por engagement.

### 2.6 Jalogüín (`jaloguin`)
- **Titular:**
  - «Lo pasamos / la muerte» (20, IG-072)
  - «amamos / jalogüinssss!» (20, IG-072)
  - «traguitos y / travesuras 1313» (27, IG-124)
- **Foto decisiva:** `ig/DCIEfJUylnY_03.jpg` (P124): bartender lanzando una botella frente al muro rojo, 5/5, la única horizontal fuerte. Con 1068 px va como banda media, no a sangre. Alternativa vertical: `ig/DShtzZ0FD9H_00.jpg` (P229, 1440 px).
- **Texto literal:** «Se comió, se tomó, se bailó, quedamos con dolor de guata de tanto reír» (IG-072). «Jalogüínnnnn! Lo pasamos bomba, picho caluga, macanúo!» (IG-041; emoji quitado tras "bomba").
- **Por qué:** es una fiesta anual con nombre propio, tres años seguidos. Carga la barra y los sillones (P136). Riesgo: muchas caras de clientes.

### 2.7 Las sociales (`gente-y-parroquianos`)
- **Titular:**
  - «no somos ná / sin ustedes!» (24, IG-026)
  - «nuestro barsucho / ucho ucho!» (27, IG-026)
- **Foto decisiva:** `ig/CpVyxXJJrhO_00.jpg` (P031, IG-152): clientas riendo y brindando en la barra, 5/4, noche cálida. Mosaico chico con las fotos de flash de IG-026 (x5,0), con permiso de imagen.
- **Texto literal:** «Nunca publicamos las “sociales” de nuestras jornadas recreativas alineadoras de chakras» … «Ya saben que no somos ná sin ustedes! Faltan muuuchas más, pero no se pueden subir más de 20 cuec!» (IG-026).
- **Por qué:** es la frase que define la casa, y engagement alto.

### 2.8 Quiénes somos (`el-almudcito-se-presenta` + `los-papis` + `ojo-piojo`)
- **Titular:**
  - «Somos su / Almudcito ito ito» (26, IG-092)
  - «los papis / del almud» (19, IG-067)
  - «OJO / PIOJO» (9, IG-118)
- **Foto/video decisivo:** V031 (`ig/DFWLrRxyvVB_00.mp4`, 1–10,4 s, sin subtítulos; incluye el mural de ojos a los 7–8 s). Complemento: afiche P063 (Ojo Piojo).
- **Texto literal:** «Somos su Almudcito ito ito desbordando amor, locura, pasión, frenesí y un derroshe de coctelcitos y comilona ona ona!» (IG-092). «Por último, los papis del almud: el franchuto @rusio_mezclao y la disharashera @cepaz» (IG-067). «OJO PIOJO es un proyecto hecho con mucho amor, paciencia y tiempo» (IG-118).
- **Por qué:** dice quién es Almud con sus propias palabras. Las líneas de IG-007 sobre Sylvain son de terceros y solo entran como cita atribuida.

**Banca** (para v2.1 o para notas dentro de otros capítulos):
- musica-en-vivo: el mejor video con el mar (V042), pero necesita permiso de Isleños y va como voz de terceros;
- almud-rucalaf: la locación es ajena;
- lluvia-y-frio con solcito-y-verano: el clima de Chiloé como hilo de texto entre capítulos ("al mal tiempo, güena cara!", IG-140);
- fin-de-ano-y-resumenes: «se construye y crece a pausa», IG-119;
- bendita-primavera: única foto buena de sillones, P114;
- amor-14f;
- teik-aguei: pandemia, documental.

## 3. Cómo cuentan un cuento (dispositivos recurrentes)

Conteo sobre los 175 posts con voz propia:

| Dispositivo | Frecuencia | Ejemplos literales |
|---|---|---|
| Nombre propio del bar en diminutivo | 119/175 | «su Almudcito», «Almudcito ito ito» (IG-013) |
| Diminutivo en cascada (ito ito / ita ita / eco) | 66/175 | «fondita ita ita» (IG-081), «comilona ona ona» (IG-092), «barsucho ucho ucho» (IG-026), «chanchulín lín lín» (IG-051), «PULENTO ALANCITO ITO ITO» (IG-156) |
| Invitación con hora | 112 «le esperamos» · 79 "18:00 / 6 pm" | «Véngase pal Almudcito ito ito, le esperamos desde las 6 pm :)» (IG-013) |
| Trato de **usté** | 47/175 | «usté se lo merece» (14), «pa que le vamos a contar si usté ya sabe!» (IG-005) |
| Anglicismo fonético -eichon | 27/175 | celebreichon, brindeichon, conmemoreichon, decoreichon, complikeichon, concentreichon |
| Cierre-firma | 83/175 «Besi» · 25 «Ya sabe ya» · 18 «Venga venga…» · 12 «Que no se lo cuenten» · 15 «Salucita» | «Que no se lo cuenten! Besiiiii» (IG-032) |
| Día de la semana como gancho | 52/175 | «Viernes ya!», «Hoy es Miércoles de piscoleinnnn!» |
| Clima de Chiloé como antagonista | 41/175 | «al mal tiempo, güena cara!!!» (IG-140), «pucha que está helao Juan!» (IG-103) |
| Nombrar a la gente con @ y apodo | 14 listas de 3+ @ | «el franchuto @rusio_mezclao y la disharashera @cepaz» (IG-067) |
| Crédito al fotógrafo | 70/175 | «📸: @catarsis.fotografia», «las imágenes de @estudiouno.prod» |
| Gracias en triple | 6/175 | «GRACIAS GRACIAS GRACIAS» (IG-048, IG-100) |

**Estructura típica de un cuento de evento** (Jalogüín, aniversarios, Fondita), en tres tiempos:
1. **Anuncio:** afiche, qué habrá y a qué hora, «Ya sabe ya».
2. **Noche:** reel.
3. **"Registros":** carrusel de 20 fotos que se publica en 2–4 entregas («Seguimos recordando…», «Otros registros…»), con agradecimiento nominal al equipo, al DJ (@dj.santiago.matus en 5 eventos), al fotógrafo y a los amiguis.

El cierre es casi siempre una vuelta al presente: «Hoy miércoles ya le estamos esperando» (IG-049).
**Léxico de la casa por cuento** (detalle en `lexicon` de cada cuento): guarisnaque, güergüero, buche, empinar el codo/codein, comilona, menjunje, ñam ñam/glup glup, parroquian@s, jornada recreativa, delichus, macanúo, picho caluga, choriflai, mortal kombat, tikitikití, japi berdey, guanderful, tumorrou, colors, mundo mundial, llenifer, beio, -eli (tinteli, bigoteli, litreli), onfaya, ponerle wendy, corasound, maldición gitana, lucrecias.

## 4. Espacios pedidos por el cliente: qué cuento puede cargar cada uno

Las cifras son fotos o videos fuertes (épica ≥4 y calidad ≥4) sobre el total del cuento, según `spaces_carried`.

| Espacio | Cuento portador (foto) | Otros cuentos que lo cargan | Estado |
|---|---|---|---|
| **Sofás** | bendita-primavera: P114, 1/1 (la única buena) | jaloguin: P136, 0/1, grupo disfrazado | **Brecha:** hay que pedir fotos |
| **Mesas interiores** | aniversario-10: P073, el "10" de flores | lluvia-y-frio: P076 (IG-094), 2/2; aniversario-12: P339 | Justo. P076 es horizontal |
| **Barra** | aniversario-11: 8/9 | jaloguin 6/9 (P124), equipo 5/7, fondita 3/5 (P093), la-barrita 3/8, aniversario-12 3/3 (P362) | Sobra |
| **Patio techado** | aniversario-11: P189 | aniversario-12 7/13 (mixta), terraza 4/5 (P021, P046), fondita 2/2 (P090), techado-2026 2/2 | Sobra. El techado de 2026 cambia el espacio |
| **Terraza descubierta** | terraza: P039, P035 | musica-en-vivo 2/2 (V042, de día), aniversario-12 P357 (violeta), solcito P159 | Media |
| **Cuadros/arte** | ojo-piojo: 1/2 (P063, V005, V006) | mujeres-8m (mural de corazones P174), fin-de-ano (V002), el-almudcito-se-presenta (V031, 7–8 s), mambo-tiki/teik-aguei (V084, marcos; P429, carta enmarcada) | **Brecha** en foto fija: resolver con frames de video |
| **Personal** | equipo: 10/14 | fondita 2/3, aniversario-11 5/7, mujeres-8m (P174, de día), los-papis (V056, terceros) | Bien |

## 5. Notas de fidelidad y riesgos

- **Emoji con significado.** Hay casos en que quitar el emoji cambia el sentido:
  - «Barrita llena ♥️ contento!» (IG-171) queda en «Barrita llena contento!»; está marcado con `nota` y no se propone como titular;
  - «le esperamos con mucho 🧡 traguitos» (IG-124) se cortó antes del glifo.
- **Ortografía original:** se mantiene tal cual («alegres!! , hemos», IG-102; «@lizzearellano» y «@lizzearellanol» conviven en las captions); también las letras dobles Unicode de 𝕋𝕌𝕂𝕌𝕃𝕀𝕋𝕆𝕊𝔸𝕂𝔸𝕐𝔸𝕄𝔸 (IG-139), que no se citan.
- **Voces de terceros:** IG-007, IG-028, IG-029, IG-033, IG-056 y la cita de @rominaberatto en IG-055. Si se usan, van atribuidas.
- **Caras:** IG-026, Jalogüín y 12 años tienen muchos clientes identificables. Para usos grandes conviene preferir al equipo.
- **Identidad de los dueños:** no está verificada en las fotos (P217, P347 y P248 son "¿dueño?"). No hay que rotular a nadie.
