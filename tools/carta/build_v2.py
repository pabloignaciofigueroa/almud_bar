# Builds content/carta-v2.json from a hand transcription of the 7 carta PDFs
# (checked against pdftotext -layout, pdfplumber column crops and 150 dpi renders).
import json, re

R = '/home/claude/almud_bar/'
OLD = json.load(open(R + 'content/carta.json'))

def P(n): return '$ ' + n          # price as printed
def it(nombre, precio=None, desc=None, tags=None, nota=None, precios=None, **extra):
    d = {'nombre': nombre}
    if desc: d['desc'] = desc
    if precio: d['precio'] = P(precio)
    if precios: d['precios'] = {k: P(v) for k, v in precios.items()}
    if tags: d['tags'] = tags
    if nota: d['nota'] = nota
    d.update(extra)
    return d
def two(cols, a, b): return dict(zip(cols, [a, b]))

# ---------------------------------------------------------------- CARTA-2
casa = [
 it('Pinche Güey', '8.800', 'Un guarisnaque complejo pa l@s que disfrutan sabores más potentes: Mezcal, tequila, horchata de maní tostado y merkén, pomelo y limón! Un cóctel cítrico, picantito, tostado, ahumado. Atrévase se se se!'),
 it('Aquí te las traigo Peter', '6.700', 'Este es tan lindo! Le llea: Mistral Nobel Cristalino, licor de flor de saúco, cranberry, limoncito y un toque dulce de jarabe. Pero lejos lo más bacán es la burbuja que viene aquí!'),
 it('Cómo te voy a olvidar', '6.800', 'Este es un cóctel sencillo, pero muuuuuy rico [y bonito]: va con Vodka Pera, un toque cítrico de limoncito, jarabe pal dulzor y terminamos con Vino tinteli, que tiñe de un color hermoso este cóctel que está 10/10'),
 it('Guarever como sea', '6.200', 'Dulcecito y aromático, nos lleva al caribe con el licor de plátano y licor de café, luego aterrizamos al mejor país de Chile con el pisqueli, su toque con el mix sagüer y rematamos con una cremosa espuma de ron de coco. Hit!', tags=['nuevo']),
 it('Not Collins', '6.700', 'Conoce el Tom Collins? Este es así, pero en una variante un poco más dulce y super refrescante: amaretto disaronno, jarabe, limón y soda. Infalible!', tags=['nuevo']),
 it('Te espero en la cuneta', '7.800', 'Esta es una versión más dulzona del siempre bien ponderado Margarita: tequila blanco, curaçao, limón y jugo de piña: pum!'),
 it('Deja tomao', '7.400', 'Este nació como un cóctel sin alcohol; pero la mezcla de pepino, jugo de mango, limón y miel nos pidió probarlo con gin ..... y nos enamoró!'),
 it('Sagüer on Faia', '7.900', 'Este es un sour bien especial: va con Mistral Nobel Fire, limón y jarabe que complementa este cóctel especiado, medio picantito y muy rico!!!'),
 it('Sangría Foreva!', '6.500', 'Esta versión te dejará como perro con dos colas! Vino Carménère, toda la malicia del pisco añejado, jarabe de canela, unos toques frutales infaltables y mucho amor'),
 it('Ramón', '7.100', 'Es una precisa mezcla: gin, licor marrasquino, limón y romero. Para los fanáticos de los cócteles cítricos y el frescor del romero! [el vasito va con crusta de sal de romero]'),
 it('Tranquilein John Wayne', '6.800', 'Esta maravilla lleva una mezcla de Whiskys [blended scotch], jugo de manzana, jarabe de canela y limón: un cóctel muy balanceado y refrescante!'),
 it('Desde que te conocí', '6.900', 'Muy refrecante coctelcito, con base de Ramazzotti más el sabor imperdible de la maracuyá, limoncito y terminamos con un toque de espumante... déjese cautivar por esta maravilla!'),
 it('A veces me pongo Coquette', '7.100', 'Este es de lo más que hay: mezcla perfecta de pisco berries con crema de whisky, frambuesa, naranja y jarabe de canela: una delicia rosada, cremosa y dulzona!'),
 it('Iquique Glorioso', '7.400', 'Maracuyá, mango y piña, enlazados al destilado patagónico Trä·kàl y Pisco. Oh si! Este cóctel trae el trópico mezclado con el sur de nuestro país a tu boca: no lo olvidarás!'),
]

# ---------------------------------------------------------------- CARTA-3
VC = ['NORMAL [90 cc]', 'CORTO XL [150 cc]']
mundo = [
 {'titulo': 'Clásicos', 'nota': '[Algunos recomendados de su Almudcito]', 'items': [
   it('Daiquiri', '5.700', 'Desde Cuba llega esta mezcla infalible: ron blanco, jarabe, limón y pulpa de fruta!'),
   it('Bloody Mary', '6.700', 'Este es saladito! Vodka, jugo de tomate casero, salsa inglesa, limón y tabasco'),
   it('Espresso Martini', '6.200', 'Esta delicia te hará entrar en calor: Vodka, Kahlúa, jarabe y extracción de café en frío [cold brew] casero!'),
   it('Tom Collins', '6.900', 'Este clásico es parecido al siempre bien ponderado sour: gin, jarabe, limón y soda.', nota='Puedes pedirlo con gin frutilla!'),
   it('Cosmopolitan', '6.200', 'Nos encanta este coctelcito, tan sex & the city!: vodka, triple sec, jarabe de arándanos y limón. Delichus!'),
   it('Penicilin', '8.200', 'Como lo indica su nombre, este es la mejor medicina! whisky escocés, jarabe de jengibre, miel y limón'),
 ]},
 {'titulo': 'Vermú', 'nota': 'UN VERMUCITO CON UNA TÓNICA QUEDA PICHO CALUGA!', 'columnas': VC,
  'nota_pie': 'AGREGUE UNA TÓNICA FINOLI FENTIMANS POR $3.700 [TONIC WATER, ROSE LIMONADE O VALENCIAN ORANGE]',
  'items': [
   it('Carpano', desc='Rosso / Bianco', precios=two(VC, '3.500', '5.800')),
   it('Cinzano', desc='Rosso / Bianco', precios=two(VC, '3.500', '5.800')),
   it('Martini', desc='Rosso / Bianco / Dry', precios=two(VC, '3.500', '5.800')),
   it('Martini', desc='Rubino / Ambrato', precios=two(VC, '5.800', '9.600')),
   it('Dolin', desc='Rosso / Bianco / Dry', precios=two(VC, '5.800', '9.600')),
   it('La Madre', desc='Rosso / Bianco', precios=two(VC, '7.000', '11.600')),
   it('Casals', desc='Rosso', precios=two(VC, '9.200', '15.300')),
 ]},
 {'titulo': 'Mule', 'nota': 'DESTILADO + GINGER BEER, JUGO DE LIMÓN, MENTA Y SODA', 'items': [
   it('Mistral Mule', '8.400', 'Base de Mistral Apple/ Honey/ Fire'),
   it('Moscow Mule', '7.600', 'Base de vodka'),
   it('Träkál Mule', '9.900', 'Base de destilado patagónico de peras y manzanas'),
   it('London Mule', '8.000', 'Base de gin'),
   it('Moscat Mule', '7.200', 'Base de pisco moscatel'),
 ]},
 {'titulo': 'Negroni', 'items': [
   it('Clásico', '6.200', 'Gin, Campari y Vermú Rosso'),
   it('Premium', '8.600', 'Gin a elección, Campari y Vermú Rosso'),
   it('Patagónico', '7.200', 'Träkál, Campari y Vermú Rosso'),
   it('Boulevardier', '6.500', 'Bourbon, Campari y Vermú Rosso'),
   it('Blanconi', '6.900', 'Gin, Cointreau y Vermú Bianco'),
 ]},
 {'titulo': 'Spritz', 'items': [
   it('Aperol / Ramazzotti / Campari / Vermú', '6.700'),
   it('Flor de saúco', '6.700'),
   it('St Germain', '9.900', '[El original flor de saúco]'),
   it('Chambord', '9.200', '[Licor de frambuesas rojas y negras, miel & coñac]'),
 ]},
 {'titulo': 'Sagüer', 'items': [
   it('Tradicional / Tradicional sabores', '5.200', '[Chilensis!]'),
   it('Peruano / Peruano maracuyá', '6.500'),
   it('Whisky', '6.500'),
   it('Niu York', '6.500', '[Como el whisky sour, pero con top de vino tinteli]'),
   it('Träkál', '9.900', '[Destilado patagónico de peras y manzanas]'),
   it('Amaretto', '4.500'),
 ]},
 {'titulo': 'Mojitos', 'items': [
   it('Tradicional o sabores', '5.900', '[Frambuesa, mango, piña o maracuyá]'),
   it('Vodka / Espumante', '5.900'),
   it('Jägermojito', '6.900'),
   it('Aperol', '6.500'),
 ]},
 {'titulo': 'Red Bull te da aaalas', 'items': [
   it('Tropical Gin', '7.800', 'Red bull tropical + gin + toque de maracuyá'),
   it('Wild Dragon', '7.800', 'Red Bull Dragon Fruit + Ballantines cherry'),
   it('Jägerbomb', '6.600', 'Red bull + shot de Jägermeister'),
 ]},
]

# ---------------------------------------------------------------- CARTA-4
NX = ['NORMAL [90 cc]', 'CORTO XL [150 cc]']
CX = ['CORTO [90 cc]', 'CORTO XL [150 cc]']
GT = ['CORTO [90 cc]', 'GIN & TONIC']
def rows(cols, data):
    out = []
    for r in data:
        n, a, b = r[0], r[1], r[2]
        d = r[3] if len(r) > 3 else None
        out.append(it(n, desc=d, precios=two(cols, a, b)))
    return out
NI = 'Precio del corto normal o XL\nNO INCLUYE BEBIDA'
espir = [
 {'titulo': 'Piscolein o combinadito', 'nota': NI, 'columnas': NX, 'items': rows(NX, [
   ('Mistral Gran Nobel', '10.900', '18.100'),
   ('Mistral Nobel Cristalino', '8.000', '13.300'),
   ('Mistral Nobel / Manzana / Fire / Miel', '5.800', '9.600'),
   ('Mistral 40º', '4.000', '6.400'),
   ('Mistral 35º', '3.600', '5.700'),
   ('Kappa XO', '15.600', '26.000'),
   ('Waqar 40º', '13.000', '21.600'),
   ('Bou Barroeta - Cofradía', '13.600', '22.600'),
   ('Bou Barroeta - Romanet', '12.600', '21.000'),
   ('Bou Barroeta - Maria’s', '11.400', '19.000'),
   ('Bou Barroeta - A mis nietas', '9.000', '15.000'),
   ('Tololo Black', '12.400', '20.600'),
   ('Tololo Blue', '10.200', '17.000'),
   ('Black Heron', '10.200', '17.000'),
   ('Horcón Quemado 40°', '5.700', '9.000'),
   ('Alto del Carmen 40° Doble Destilado', '5.400', '8.700'),
   ('Gobernador 40º', '5.400', '8.700'),
   ('Horcón Quemado 35°', '5.400', '8.700'),
   ('Alto del Carmen 40° High Berries', '4.800', '7.700'),
   ('Alto del Carmen 40°', '4.800', '7.700'),
   ('Sagrado Corazón 40º Transparente/Reservado', '4.800', '7.700'),
   ('Republicano Añejado o Triple Destilado', '4.800', '7.700'),
   ('Sagrado Corazón 35º', '4.000', '6.400'),
   ('Alto del Carmen 35° Robles del Sur', '3.800', '6.000'),
   ('Gobernador 35°', '3.600', '5.700'),
   ('Alto del Carmen 35°', '3.600', '5.700'),
 ])},
 {'titulo': 'Vodkita', 'nota': NI, 'columnas': CX, 'items': rows(CX, [
   ('Stoli Elit', '14.400', '24.000'),
   ('Grey Goose', '12.000', '20.000', '[Tradicional o Sabores]'),
   ('Prairie', '8.000', '13.300', '[Tradicional o Pepino]'),
   ('Gabri / Zubrowka / Antártica', '7.000', '11.700'),
   ('Carmela', '7.000', '11.700', '[Vodka Chilote!]'),
   ('Absolut', '5.200', '8.400', '[Absolut Blue o Sabores]'),
   ('Mawunko', '5.000', '7.600', '[Tradicional o Sabores]'),
   ('Stolichnaya', '5.000', '7.600', '[Tradicional o Pepino]'),
   ('Wyborowa', '4.400', '7.000'),
 ])},
 {'titulo': 'Ron poromponpon', 'nota': NI, 'columnas': CX, 'items': rows(CX, [
   ('Diplomático Reserva/ Matusalem 15 años', '14.000', '23.300'),
   ('Bacoo 11 años', '12.400', '20.600'),
   ('Pampero Aniversario / Bacoo 7 años', '11.000', '18.300'),
   ('Flor de Caña 18 años', '10.800', '18.000'),
   ('Diplomático Mantuano', '9.400', '15.600'),
   ('Zacapa Ambar 12 años / Bacoo 4 años', '8.000', '13.300'),
   ('Bush Original / Maracuyá & Guayaba', '8.000', '13.300'),
   ('Pampero Selección / / Matusalem 7 años', '7.700', '12.800'),
   ('Havana 7 años', '7.400', '12.300'),
   ('Kraken', '6.200', '10.200'),
   ('Flor de Caña 12 años', '5.900', '9.800'),
   ('Plantation', '5.400', '9.000'),
   ('Flor de Caña Coco o Spresso', '5.000', '8.300'),
   ('Malibu (ron sabor coco)', '5.000', '8.300'),
   ('Flor de Caña 5 años', '4.500', '7.500'),
   ('Havana Añejo Especial', '4.500', '7.500'),
 ])},
 {'titulo': 'Whiscachos', 'nota': 'Empezamos con la selección de lo más pituqueli que tenemos, estos vienen en cortos de 2 oz [60 ml]',
  'nota_pie': 'Los whiscachos no incluyen bebida pal que le guste tomarlo puritano', 'items': [
   it('Johnnie Walker Blue Label', '65.000', 'Blended [Escocia], su mezcla es muy selecta: sólo uno de cada diez mil barriles sirve para crear el Etiqueta Azul.'),
   it('The Dalmore Single Malt 12 años', '32.000', 'Highland Single Malt [Escocia], envejece los primeros 9 años en barricas de bourbon de roble blanco americano, luego la mitad se transfiere a toneles de jerez los últimos 3 años.'),
   it('Glenfiddich Single Malt 18 años', '28.000', 'Whisky escocés, preparado en barricas de jerez y bourbon por 18 años, para después mezclarse en pequeñas barricas numeradas, lo que otorga una complejidad única'),
   it('Macallan Sherry Oak 12 años', '27.000', 'Highland Single Malt [Escocia] Madura exclusivamente en barricas de roble europeo que tuvieron jerez oloroso. Sabor intenso, con aromas de jerez, miel, vainilla y roble especiado'),
   it('Macallan Double Cask 12 años', '26.100', 'Highland Single Malt [Escocia] Madura en barricas de roble americano y europeo que tuvieron jerez oloroso. Sabor equilibrado y ligero: notas de vainilla, especias, cítricos, jengibre y miel.'),
 ]},
 {'titulo': 'Blended', 'padre': 'Whiscachos', 'nota': 'Elija su medida 90 o 150 cc!', 'columnas': CX, 'items': rows(CX, [
   ('Akashi Japanese blended whisky', '22.400', '37.300'),
   ('Johnnie Walker Gold Label', '16.000', '26.600'),
   ('Johnnie Walker Swing 18 años', '15.200', '25.300'),
   ('Johnnie Walker Black Label', '10.800', '18.000'),
   ('Monkey Shoulder', '9.800', '16.300', '[Blended]'),
   ('Ballantines Wild', '7.000', '11.600', '[sabor cereza]'),
   ('Johnnie Walker Red Label', '5.000', '8.300'),
   ('Grants Blended Scotch', '4.700', '7.800'),
 ])},
 {'titulo': 'Irish', 'padre': 'Whiscachos', 'nota': 'Elija su medida 90 o 150 cc!', 'columnas': CX, 'items': rows(CX, [
   ('The Dead Rabbit Irish whiskey', '14.200', '23.600'),
   ('Jameson Irish whiskey', '6.800', '11.300'),
   ('Tullamore Dew Irish whiskey', '6.000', '10.000'),
 ])},
 {'titulo': 'Single Malt', 'padre': 'Whiscachos', 'nota': 'Elija su medida 90 o 150 cc!', 'columnas': CX, 'items': rows(CX, [
   ('Bruichladdich Classic Laddie', '26.000', '43.000', '[Islay Single Malt]'),
   ('Glenfiddich Single Malt 15 años', '27.000', '45.000'),
   ('Glenfiddich Single Malt 12 años', '11.200', '18.600'),
 ])},
 {'titulo': 'Bourbon / Tennessee', 'padre': 'Whiscachos', 'nota': 'Elija su medida 90 o 150 cc!', 'columnas': CX, 'items': rows(CX, [
   ('Jack Daniel’s Single Barrel', '20.200', '33.600'),
   ('Woodfoord Reserve', '13.000', '21.600'),
   ('Jack Daniel’s Gentleman', '11.800', '19.600'),
   ('Ole Smoky Tennessee', '9.400', '15.600'),
   ('Jack Daniel’s 7 / Honey / Fire / Apple', '9.200', '15.300'),
   ('Bulleit Bourbon', '8.000', '13.300'),
   ('Wild Turkey / American Honey', '6.800', '11.300'),
   ('Evan Williams', '6.000', '10.000'),
   ('Jim Beam Bourbon', '5.800', '9.600'),
 ])},
 {'titulo': 'Amamos el GIN!', 'nota': 'Puede pedir un corteli o el gin&tonic que viene con una tónica Fentimans [200 ml]\nVariedades: tónica tradicional, rose limonade o valencian orange',
  'columnas': GT, 'items': rows(GT, [
   ('Matsui The Hakuto', '21.700', '25.400', '[Japón, 47°]'),
   ('Mary Le Bone', '21.700', '25.400', '[Inglaterra, 51,5°]'),
   ('Citadelle Old Tom', '17.400', '21.100', '[Francia, 46°]'),
   ('The Botanist', '16.800', '20.500', '[Escocia, 46°]'),
   ('Mare Capri', '16.800', '20.500', '[España, 42,7°]'),
   ('Martin Miller’s', '16.600', '20.300', '[Inglaterra, 40°]'),
   ('Whitley Neill Rhubarb & Ginger Gin', '16.600', '20.300', '[Inglaterra, 43°]'),
   ('Goodwinds', '15.000', '18.700', '[Chile, 42°]'),
   ('Mare', '15.000', '18.700', '[España, 42,5°]'),
   ('London n°1', '14.000', '17.700', '[Inglaterra, 47°]'),
   ('Mombasa', '13.200', '16.900', '[España, 41,5°]'),
   ('Mombasa Frutilla', '13.200', '16.900', '[España, 37,5°]'),
   ('Citadelle', '12.400', '16.100', '[Francia, 44°]'),
   ('Luxardo', '11.800', '15.500', '[Italia, 43°]'),
   ('Bloom', '11.400', '15.100', '[Inglaterra, 46°]'),
   ('Hendrick’s', '10.900', '14.600', '[Escocia, 41,4°]'),
   ('Opihr', '9.900', '13.900', '[Inglaterra, 42,5°]'),
   ('Tanqueray 10', '9.800', '13.500', '[Escocia. 47,3°]'),
   ('Engine', '9.800', '13.500', '[Italia, 42°]'),
   ('Mom', '9.000', '12.700', '[Inglaterra, 39,5°]'),
   ('Mom Love', '9.000', '12.700', '[Inglaterra, 37,5°]'),
   ('Bulldog', '9.000', '12.700', '[Inglaterra, 40°]'),
   ('Puerto de Indias', '8.400', '12.100', '[España, 37,5°]'),
   ('Proa', '8.400', '12.100', '[Chile, 45°]'),
   ('Hayman’s Old Tom', '7.600', '11.300', '[Inglaterra, 41,4°]'),
   ('Carpintero Negro', '7.400', '11.100', '[Chile, 42,5°]'),
   ('Tanqueray Royale', '7.200', '10.900', '[Escocia, 41,3°]'),
   ('La República Amazónica / Andina', '7.000', '10.700', '[Bolivia, 42°]'),
   ('Tanqueray Bossa Nova', '6.800', '10.500', 'Escocia, 30°]'),
   ('Tanqueray Sevilla', '6.800', '10.500', '[Escocia, 41,3°]'),
   ('Mawunko', '6.600', '10.300', '[Chiloé-Chile, 40°]'),
   ('Gabri', '6.400', '10.100', '[Chile, 40°]'),
   ('Quintal Andes / Franklin', '6.400', '10.100', '[Chile,43°]'),
   ('Tanqueray', '6.400', '10.100', '[Escocia, 43,1°]'),
   ('Beefeater Pink', '6.400', '10.100', '[Inglaterra, 35,7°]'),
   ('Beefeater Blood Orange', '6.000', '9.700', '[Inglaterra, 35,7°]'),
   ('Beefeater', '6.000', '9.700', '[Inglaterra, 40°]'),
   ('Bombay Bramble', '6.000', '9.700', '[Inglaterra, 37,5°]'),
   ('Bombay Sapphire', '6.000', '9.700', '[Inglaterra, 47°]'),
   ('Faraway', '5.500', '9.200', '[Chile - Chiloé, 42°]'),
 ])},
 {'titulo': 'Tequilazos & mezcalazos', 'nota': 'Shot de 75 cc acompañado de limón & sal', 'items': [
   it('Mezcal Legendario Domingo', '12.900'),
   it('Mezcal 400 Conejos', '11.500'),
   it('Mezcal La del Bateo', '8.500'),
   it('Tequila Don Julio', '13.400', '[Blanco]'),
   it('Tequila Herradura Añejo', '10.500'),
   it('Tequila Butterfly', '8.200', '[Blue, Rosa o Silver Cristalino]'),
   it('Tequila Cazadores', '5.500', '[Blanco o Reposado]'),
   it('Tequila Jimador', '5.200', '[Blanco o Reposado]'),
   it('Tequila Olmeca', '4.500', '[Blanco o Reposado]'),
 ]},
]

# ---------------------------------------------------------------- CARTA-6
def vino(bodega, nombre, origen, cepa, precio):
    return it(nombre, precio, cepa, nota=origen, bodega=bodega)
vinos = [
 {'titulo': 'Tintelis', 'items': [
   vino('Miguel Torres', 'Las Mulas', '[Valle Central]', 'Carménère / Vino 100% orgánico & vegano', '15.000'),
   vino('Casa Bauzá', 'Presumido', '[Valle Central]', 'Carménère', '25.900'),
   vino('Koyle', 'Royale', '[Valle de Colchagua]', 'Carménère', '30.900'),
   vino('Casa Bauzá', 'Atrevido', '[Valle del Maipo]', 'Mezcla Tinta', '31.900'),
   vino('Santa Ema', 'Gran Reserva', '[Valle del Maipo]', 'Merlot', '18.000'),
   vino('Lapostolle', 'Grand Selection', '[Valle de Colchagua]', 'Cabernet Sauvignon', '18.000'),
   vino('Salentein', 'Portillo', '[Valle de Uco, Mendoza]', 'Malbec', '18.000'),
   vino('Valle Secreto', 'First Edition', '[Valle de Cachapoal]', 'Syrah', '19.500'),
 ]},
 {'titulo': 'Blanquelis', 'items': [
   vino('Miguel Torres', 'Santa Digna', '[Valle Central]', 'Chardonnay o Sauvignon Blanc', '15.000'),
   vino('Garcés Silva', 'Boya', '[Valle de Leyda / San Antonio]', 'Chardonnay', '16.900'),
 ]},
 {'titulo': 'Espumantes', 'items': [
   it('Miguel Torres Estelado Brut Rosé', '19.000'),
   it('Undurraga Brut', '12.000'),
   it('Undurraga Free Rosé', '12.000', nota='[sin acohol]'),
 ]},
 {'titulo': 'Por copa', 'items': [
   it('Undurraga Brut', '4.500', 'Espumante', nota='[botellita 187 cc]'),
   it('Santa Digna', '4.500', 'Carménère / Cabernet Sauvignon / Sauvignon Blanc', nota='[botellita 187 cc]'),
 ]},
]

# ---------------------------------------------------------------- CARTA-5
mock = [
 {'titulo': 'Mocktails de la casa', 'nota': 'COCTELCITOS SIN ALCOHOL', 'items': [
   it('Otra cosa mariposa', '6.400', 'Si te gusta el café, este te hará llegar al cielo!: extracción de café en frío, jugo de maracuyá, jarabe de canela y ginger ale'),
   it('La moto chantá', '6.400', 'Juguito de mango y maracuyá, pepino, jarabe simple, limón y bitter pepino! [El vasito va con crusta de sal]'),
   it('Embolinando la perdiz', '5.900', 'Un poco más cítrico y sobretodo refrescante: jugo de pomelo y manzana, miel, limón y menta!'),
   it('Soy una limonhada', '6.200', 'Refrescante como una limonada, pero con un toque mágico! Jugo de apio, jugo de manzana, jarabe y limón.'),
   it('Efecto placebo', '6.400', 'Rico rico: jugo de frambuesa, jugo de maracuyá, jarabe, limón, menta y rematamos con tónica'),
   it('Six Seven', '5.900', 'Dulcecito, sencillo y muy delicioso: Jugo de piña, jarabe de almendras y el infaltable toque del limón!'),
 ]},
 {'titulo': 'Mocktails clásicos', 'items': [
   it('Sangría sin alcohol, olé!', '6.600'),
   it('Ramazzotti Spritz sin copetín!', '6.200', '[ZEROZOTTI]'),
   it('Piña colada virginsísima', '6.400'),
   it('Mojito sin alcohol', '4.900', '[Puedes pedirlo con miel, jengibre o maracuyá]'),
   it('Pisco sagüer sin alcohol', '5.900', '[Puedes pedirlo con miel, jengibre o maracuyá]'),
 ]},
]
jugos = [{'titulo': None, 'items': [
   it('Jugos de pulpa', '3.000'),
   it('Limonada', '3.500', '[Puedes pedirla con miel, menta y/o jengibre]'),
   it('Bebidas gaseosas', '2.400'),
   it('Agua sin gas Puyehue', '2.300', '[330 cc]'),
   it('Perrier agua con gas', '2.300', '[330 cc]'),
   it('Acqua Panna / S.Pellegrino', '3.000', '[505 cc]'),
   it('Red Bull', '3.500', '[Regular, Tropical, Fruta del Dragón, light ]'),
   it('Tónicas Fentimans', '3.700', '[200 cc]'),
   it('Espumante', '12.000', '[Undurraga Free Rosé / 750 cc ]'),
]}]
cervezas = [{'titulo': None, 'items': [
   it('Peroni 0°', '3.600'), it('Heineken 0°', '3.600'), it('Mahou 0°', '4.900'), it('Extra michelada', '1.500'),
]}]
calientes = [{'titulo': None, 'items': [
   it('Espresso / Americano', '2.500'), it('Té / Infusiones', '2.200'),
]}]

# ---------------------------------------------------------------- CARTA-1
V = ['veggie']
comilona = [
 {'titulo': 'Picoteos', 'items': [
   it('Aceitunas', '6.500', 'Porción de aceitunas aliñaditas ricas delichus!', tags=V),
   it('Tukulito Sakayama', '15.900', 'Tataki de lomo de atún marinado pa chuparse el bigoteli Acompañado de pancito y salsa de la casa.'),
   it('Una cosa poca', '11.900', 'Que tan poca cosa no es! Este es como le fondiú franchuto pero más mejor porque es shileno!: mix de quesos con tomatito al horno, palta y pesto. Acompañado de pancito de la casa! Real manjarsh!', tags=V),
   it('La carne es débil', '11.900', 'Muy sabrosón & jugosito: carne de res, champiñones y tomate cherry, salteados en oliva y ajo, con un toque de paprika y cilantro. Acompañado de pancito de la casa!'),
   it('Con tuti si no pa qué!', '19.900', '[Versión 2.0] Especial pa compartir: champis salteados en mantequilla y nuez moscada, paltita con aceite de ajo y pimentón asado, queso de cabra, queso de campo, aceitunas, tomatito cherry, frutos secos, fruta de la temporada, nuestra deliciosa salsa ajo cilantro y pancito de la casa!', tags=V),
   it('A ponerle wendy!', '26.700', 'Entre ponerle y no ponerle [mejor ponerle!]: carne, pollo, champis, tomate en gajos y cebolla, todo salteado con aceite de ajo, queso de cabra y de campo, pepinos y ají encurtidos de la casa, jamón serrano crudo y crispy, pebrecito, nuestra deliciosa salsa ajo cilantro y pancito de la casa!'),
   it('Eres tan exótica', '16.500', 'Esta mezcla recuerda la comida al estilo thai: camarones y pollo en un cremosito menjunje de curry verde, leche de coco, cebolla morada, humus y cilantro. Acompañado de pancito de la casa. Pa paladares exóticos y singulares :)'),
   it('Todo que ver!', '16.000', 'Este es un cevichito pa chuparse el bigoteli. Atún rojo, pimentón amarillo, palta, cebolla morá, piña y rematamos con cilantro. El pescadín está aliñado con tremenda injundia basada en leche de coco, curry verde, y limón sutil. Va con pan de la casa!'),
 ]},
 {'titulo': 'Greditas', 'nota': 'Base de papas en cubitos, al horno. Macanúo pa compartir!', 'items': [
   it('Campestre', '13.500', 'Este gustoso menjunje combina puras cosas güenazas: champiñones, parmesano, pesto, crema y hierbas. Rematamos con pimentón rojo asado', tags=V),
   it('Camarón que se duerme', '15.900', 'Delichus mix: camarones, mezclado con queso crema, cebollín, cilantro, champiñones, jengibre desglasado con vino blanco'),
   it('Muéveme el pollo', '14.900', 'Medio dulzón y muy sabrosón: pollito, crema, nuestra rica pomodoro, curry, maní tostado y salsa teriyaki casera [También en versión veggie]'),
 ]},
 {'titulo': 'Sanguches', 'nota_pie': 'Todas las salsitas de nuestros sanguches están elaboradas por nosotros, van con pan de masa mami y mucho amor', 'items': [
   it('Chambreao', '10.900', 'Hamburguesa 100% vacuno, queso de campo, cebolla caramelizada, hojas verdes de temporada, pepinillo dill del Almudcito y salsa barbacoa-bourbon casera. En pan de hamburguesa de masa mami.'),
   it('Hamburguesa Almud', '8.900', 'Hamburguesa de lentejas de la casa muy sabrosa!, palta fileteada, tomatito, mix verde de temporada y salsa ajo cilantro en base a acquafaba. En pan de hamburguesa de masa mami.', tags=['veggie', 'vegan']),
   it('Cabrone', '9.500', 'Quesito de cabra, palta fileteada, pimentón rojo asado, hojas verdes de temporada y salsa ajo cilantro en base a acquafaba. En pan ciabatta de masa mami.', tags=V),
 ]},
 {'titulo': 'Pizzas artesanales', 'nota': 'Con base de pomodoro casera y queso mozzarella',
  'nota_pie': 'Las masas de nuestras pizzas son hechas por nosotros! puedes pedir cualquiera miti mota, menos la Zorrona, la Terrible Pollo y la Blanquita', 'items': [
   it('Trufona', '13.900', 'Menjunje de hongos al vino tinto y aceite de trufa', tags=V),
   it('Caprichosa', '15.900', 'Queso de cabra, nueces, aceitunas, cilantro y aceite de cilantro', tags=V),
   it('Huerta sabrosa', '13.900', 'Tomate cherry, champiñones , hojas verdes de temporada y salsa ajo cilantro', tags=V),
   it('Chanchito azul', '15.900', 'Queso azul, jamón serrano y aceite de ajo'),
   it('Blanquita', '14.500', 'Esta no tiene pomodoro, es una pizza blanca: base de crema, mozzarella, palta fileteada, cebolla caramelizada, ají verde y un toque de merkén!', tags=['veggie', 'picante']),
   it('Tartufita', '15.900', 'Quesito de cabra, tomate, pimentón rojo asado y un toque sabrosón de aceite de trufa. Una delicia!', tags=V),
   it('Cabras a la higuera', '15.900', 'Queso de cabra, higos, tomate cherry glaseado y reducción de aceto balsámico.', tags=V),
   it('Zorrona', '16.900', 'Carne en trozos [200 grs asiento], cebolla morada, ajo, champiñones y hojas verdes de temporada'),
   it('Terrible pollo', '16.900', 'Pollito en cubos salteado en pesto, queso crema y un toque de vino blanco, además lleva tomate, cebolla caramelizada, champiñones y hojas verdes de temporada'),
 ]},
 {'titulo': 'Pa los chichichos', 'nota': '[Para menores hasta 12 años]', 'items': [
   it('Pollito pío', '7.500', 'Dados de pollito salteado, acompañado de palta fileteada'),
   it('Bartolito', '9.900', 'Pizza de 30 cms diámetro. Base de pomodoro, mozzarella, tomate y aceitunas.'),
   it('La vaca Lola', '8.900', 'Hamburguesa casera 100% vacuno con queso derretido y tomate. En pan de hamburguesa de masa mami!'),
 ]},
 {'titulo': 'Somos dulzones', 'items': [
   it('Pizza dulzona', '12.500', 'Ideal para compartir! Es una pizza, pero dulce, está super delichus! Pasta de avellana, crema, frutos rojos glaseados, almendras fileteadas y hojitas de menta.'),
   it('Topiturrón', '6.900', '[RELOADED] Turrón de chocolate con galletas y nueces, gel de naranja y arándanos, acompañado de un sorbete de frutos rojos sobre tierra de galletas y almendras'),
   it('Crumblecito ito ito', '5.900', 'Este es un postre calientito! Crumble de manzana, chips de chocolate, almendras y nueces, acompañado con heladito de pepino de la casa, que además de ser delichussss, da un toque refrescante'),
 ]},
]

# ---------------------------------------------------------------- CARTA-7
promos = [{'titulo': None, 'nota': 'de 18:00 a 22:00 hrs', 'nota_pie': '* Siempre sujeto a stock! *', 'items': [
   it('Negroni & Fernet c/Coca Cola', '4.500', dia='Martes', dia_n=2),
   it('Piscolein & Gin Tonic', '4.500', dia='Miércoles', dia_n=3),
   it('Sangría de la casa', '4.500', dia='Jueves', dia_n=4),
   it('Ramón', '4.500', dia='Sábado', dia_n=6, texto='Ramón a $ 4.500!'),
]}]

secciones = [
 dict(id='cocteleria-de-la-casa', titulo='Coctelería de la casa', fuente='CARTA-2', intro=None, grupos=[{'titulo': None, 'items': casa}]),
 dict(id='cocteles-del-mundo-mundial', titulo='Cócteles del mundo mundial', fuente='CARTA-3', intro=None, grupos=mundo),
 dict(id='espirituosos', titulo='Espirituosos', fuente='CARTA-4', intro=None, grupos=espir),
 dict(id='vinos-espumantes', titulo='Vinos & espumantes', fuente='CARTA-6', intro=None, grupos=vinos),
 dict(id='mocktails-sin-alcohol', titulo='Mocktails sin alcohol', fuente='CARTA-5', intro=None, grupos=mock),
 dict(id='jugos-bebidas', titulo='Jugos & bebidas', fuente='CARTA-5', intro=None, grupos=jugos),
 dict(id='cervezas-sin-alcohol', titulo='Cervezas sin alcohol', fuente='CARTA-5', intro=None, grupos=cervezas),
 dict(id='bebidas-calientes', titulo='Bebidas calientes', fuente='CARTA-5', intro=None, grupos=calientes),
 dict(id='comilona', titulo='Comilona', fuente='CARTA-1', intro=None, grupos=comilona),
 dict(id='nuestras-promos', titulo='Nuestras promos', fuente='CARTA-7', intro='ALMUDCITO PROMOS', grupos=promos),
]

# ------------------------------------------------ corrections applied to the fresh transcription
correcciones = []
def fix(sec_id, nombre, field, old, new, motivo):
    for s in secciones:
        if s['id'] != sec_id: continue
        for g in s['grupos']:
            for i in g['items']:
                if i['nombre'] != nombre: continue
                if field == 'precios':
                    for k, v in i['precios'].items():
                        if v == old: i['precios'][k] = new
                else:
                    assert old in i[field], (nombre, old)
                    i[field] = i[field].replace(old, new)
                correcciones.append({'fuente': s['fuente'], 'item': nombre, 'campo': field, 'antes': old, 'despues': new, 'motivo': motivo})
                return
    raise KeyError(nombre)

fix('cocteleria-de-la-casa', 'Aquí te las traigo Peter', 'desc', 'Le llea', 'Le lleva', 'Errata documentada en copy.md (Correcciones mínimas)')
fix('cocteleria-de-la-casa', 'Desde que te conocí', 'desc', 'refrecante', 'refrescante', 'Errata documentada en copy.md (Correcciones mínimas)')
fix('comilona', 'Tukulito Sakayama', 'desc', 'bigoteli Acompañado', 'bigoteli. Acompañado', 'copy.md: punto donde el PDF tiene un emoji (♡)')
correcciones += [
 {'fuente': 'CARTA-2', 'item': 'Te espero en la cuneta', 'campo': 'nombre', 'antes': 'C U N E T A', 'despues': 'cuneta', 'motivo': 'Rotura OCR: letras espaciadas por tracking tipográfico'},
 {'fuente': 'CARTA-4', 'item': 'Tullamore Dew Irish whiskey', 'campo': 'precios.CORTO XL [150 cc]', 'antes': '$ 1 0.000', 'despues': '$ 10.000', 'motivo': 'Rotura OCR/kerning: espacio dentro del número (en el render se ve "$10.000")'},
 {'fuente': 'CARTA-3', 'item': 'Vodka / Espumante', 'campo': 'nombre', 'antes': 'VODKA  / ESPUMANTE', 'despues': 'Vodka / Espumante', 'motivo': 'Doble espacio colapsado'},
 {'fuente': 'CARTA-1/2/3/4/5', 'item': '(varios)', 'campo': 'desc', 'antes': 'texto con salto de línea / espacio dejado por un emoji (p. ej. "shileno! : mix")', 'despues': 'una línea, espacio simple ("shileno!: mix")', 'motivo': 'Saltos de línea del maquetado unidos; espacio que dejaba el glifo de emoji eliminado'},
]

emoji = [
 {'fuente': 'CARTA-1', 'item': 'Aceitunas', 'glifo_pdf': 'S', 'aspecto': '👌 (mano OK)', 'tras': 'ricas delichus!'},
 {'fuente': 'CARTA-1', 'item': 'Tukulito Sakayama', 'glifo_pdf': 'A', 'aspecto': '♡', 'tras': 'pa chuparse el bigoteli (reemplazado por ".")'},
 {'fuente': 'CARTA-1', 'item': 'Una cosa poca', 'glifo_pdf': '1', 'aspecto': '😜 (carita guiño/lengua)', 'tras': 'porque es shileno!'},
 {'fuente': 'CARTA-1', 'item': 'Campestre', 'glifo_pdf': 'S', 'aspecto': '👌', 'tras': 'pimentón rojo asado'},
 {'fuente': 'CARTA-1', 'item': 'Camarón que se duerme', 'glifo_pdf': '^', 'aspecto': '🙌 (manos arriba)', 'tras': 'vino blanco'},
 {'fuente': 'CARTA-1', 'item': 'Muéveme el pollo', 'glifo_pdf': 'a', 'aspecto': '👏 (aplauso)', 'tras': 'teriyaki casera'},
 {'fuente': 'CARTA-1', 'item': 'Sanguches (nota_pie)', 'glifo_pdf': 'A', 'aspecto': '♡', 'tras': 'y mucho amor'},
 {'fuente': 'CARTA-1', 'item': 'Pizzas artesanales (nota_pie)', 'glifo_pdf': 'D', 'aspecto': '😻 (carita con corazones)', 'tras': 'son hechas por nosotros!'},
 {'fuente': 'CARTA-1', 'item': 'Pizzas artesanales (nota_pie)', 'glifo_pdf': 'l', 'aspecto': '👀 (ojos)', 'tras': 'antes de "puedes pedir"'},
 {'fuente': 'CARTA-1', 'item': 'Crumblecito ito ito', 'glifo_pdf': 'S', 'aspecto': '👌', 'tras': 'da un toque refrescante'},
 {'fuente': 'CARTA-2', 'item': 'Aquí te las traigo Peter', 'glifo_pdf': 'M', 'aspecto': '🔥 (llama)', 'tras': 'la burbuja que viene aquí!'},
 {'fuente': 'CARTA-2', 'item': 'Te espero en la cuneta', 'glifo_pdf': 'MR', 'aspecto': '🔥👊', 'tras': 'jugo de piña: pum!'},
 {'fuente': 'CARTA-2', 'item': 'Sangría Foreva!', 'glifo_pdf': 'A', 'aspecto': '♡', 'tras': 'y mucho amor'},
 {'fuente': 'CARTA-3', 'item': 'Penicilin', 'glifo_pdf': 'M', 'aspecto': '🔥', 'tras': 'miel y limón'},
 {'fuente': 'CARTA-3', 'item': 'St Germain', 'glifo_pdf': 'A', 'aspecto': '♡', 'tras': '[El original flor de saúco ♡]'},
 {'fuente': 'CARTA-3', 'item': 'Jägerbomb', 'glifo_pdf': 'MR', 'aspecto': '🔥👊', 'tras': 'nombre JÄGERBOMB'},
 {'fuente': 'CARTA-4', 'item': 'Whiscachos (nota_pie)', 'glifo_pdf': 'S', 'aspecto': '👌', 'tras': 'tomarlo puritano'},
 {'fuente': 'CARTA-5', 'item': 'Efecto placebo', 'glifo_pdf': 'A', 'aspecto': '♡', 'tras': 'rematamos con tónica'},
 {'fuente': 'CARTA-5', 'item': 'Ramazzotti Spritz sin copetín!', 'glifo_pdf': 'M', 'aspecto': '🔥', 'tras': '[ZEROZOTTI 🔥]'},
]

iconos = {
 'veggie': 'Hoja verde (fuente "Leafs") junto al nombre. No es texto impreso; se usa "veggie" porque es la palabra de la propia carta ("[También en versión veggie]").',
 'vegan': 'Sello caligráfico "Vegan" (fuente "VeganIcons") junto a Hamburguesa Almud.',
 'picante': 'Llamita roja (fuente "Fire") junto a Blanquita (lleva ají verde y merkén).',
 'nuevo': 'Sello rojo "NUEVO" (imagen) junto a Guarever como sea y Not Collins.',
 'omitidos': 'Ornamentos decorativos (fuente "CatShop", espacios), viñetas ornamentales y flecha (fuente "Arrows") de CARTA-7.',
}

# ------------------------------------------------ keep carta.json text where items overlap; report diffs
old_items = {}
for k, src in (('coctel', 'cocteleria-de-la-casa'), ('mocktail', 'mocktails-sin-alcohol'), ('comilona', 'comilona')):
    for o in OLD[k]:
        old_items[(src, o['n'])] = o
diferencias = []
matched = set()
for s in secciones:
    for g in s['grupos']:
        for i in g['items']:
            o = old_items.get((s['id'], i['nombre']))
            if not o: continue
            matched.add((s['id'], i['nombre']))
            if o.get('g') and o['g'] != g['titulo']:
                diferencias.append({'item': i['nombre'], 'campo': 'grupo', 'pdf': g['titulo'], 'carta.json': o['g']})
            for f_new, f_old in (('desc', 'd'), ('precio', 'p')):
                newv = i.get(f_new, '')
                oldv = o.get(f_old, '')
                if f_new == 'precio': oldv = '$ ' + oldv
                if (newv or '') != (oldv or ''):
                    diferencias.append({'item': i['nombre'], 'campo': f_new, 'pdf_v2_transcripcion': newv, 'carta.json': oldv, 'usado': 'carta.json'})
                    if oldv: i[f_new] = oldv
                    else: i.pop(f_new, None)
for key in old_items:
    if key not in matched:
        diferencias.append({'item': key[1], 'campo': 'nombre', 'nota': 'en carta.json pero no encontrado en v2'})
# promos vs carta.json
promo_items = secciones[-1]['grupos'][0]['items']
for p, n in zip(OLD['promos'], promo_items):
    if p['d'] != n['dia'] or (p['t'] != n['nombre'] and p['t'] != n.get('texto')):
        diferencias.append({'item': p['t'], 'campo': 'promo', 'pdf': n['nombre'], 'carta.json': p['t']})

out = {
 '_fuente': 'Carta oficial Almud Bar (uqr.to/ppvi), 7 PDFs en assets/raw/carta/ descargados 2026-10-08 (CARTA-1 Comilona, CARTA-2 Coctelería de la casa, CARTA-3 Cócteles del mundo mundial, CARTA-4 Espirituosos, CARTA-5 Mocktails sin alcohol + Jugos & bebidas + Cervezas sin alcohol + Bebidas calientes, CARTA-6 Vinos & espumantes, CARTA-7 Nuestras promos). Transcripción literal verificada contra pdftotext -layout, recortes por columna con pdfplumber y render a 150 dpi. Convenciones: los títulos de sección son los nombres de cada carta; los títulos de grupo y los nombres de ítem impresos en MAYÚSCULAS display se pasan a minúscula de oración/nombre propio (como en carta.json); notas, intros y descripciones conservan las mayúsculas de la capa de texto del PDF. Los corchetes [..] que siguen al nombre impreso van en "desc" (o "nota" en vinos, donde "desc" es la cepa). Los ítems que ya estaban en carta.json conservan su texto exacto (ver _diferencias_con_carta_json). Precios tal como impresos ("$ 8.800"); multi-medida en "precios" con las etiquetas de columna del grupo ("columnas").',
 '_correcciones': correcciones,
 '_emoji_omitidos': emoji,
 '_iconos_a_tags': iconos,
 '_diferencias_con_carta_json': diferencias,
 '_dudas': [
  'Erratas impresas NO corregidas (no están en copy.md): "Undurraga Free Rosé [sin acohol]" (CARTA-6); "Woodfoord Reserve" (CARTA-4); "Pampero Selección / / Matusalem 7 años" (doble barra, CARTA-4); "Tanqueray Bossa Nova Escocia, 30°]" (falta "[", CARTA-4); "[Escocia. 47,3°]" (punto por coma, Tanqueray 10); "[Chile,43°]" sin espacio; "Penicilin" (CARTA-3). Decidir si se agregan a Correcciones mínimas.',
  'Grafías inconsistentes entre cartas, conservadas: "Trä·kàl" (CARTA-2) / "Träkál" (CARTA-3 y CARTA-4); "Mistral 40º" (º ordinal) vs "Horcón Quemado 40°" (° grado); "Mistral Apple/ Honey/ Fire" y "Diplomático Reserva/ Matusalem" (espacio sólo después de la barra).',
  'CARTA-7: la flecha une "SÁBADO / RAMÓN a $ 4.500!" con "de 18:00 a 22:00 hrs"; no queda claro si el horario aplica sólo al sábado o a todas las promos. Se dejó como nota del grupo (igual que promo_hora en carta.json).',
  'CARTA-1: el bloque "Pa los chichichos" dice "[Para menores hasta 12 años]"; se guardó como nota de grupo.',
  'Whiscachos: la carta tiene un bloque de cortos de 2 oz [60 ml] con precio único y luego subgrupos Blended / Irish / Single Malt / Bourbon / Tennessee con dos medidas; los subgrupos llevan "padre": "Whiscachos".',
  'Tags "veggie", "vegan", "picante", "nuevo" vienen de íconos, no de texto impreso (ver _iconos_a_tags).',
  'Vermú: "Martini" aparece dos veces (Rosso/Bianco/Dry y Rubino/Ambrato) con precios distintos; se mantienen como dos ítems con el mismo nombre.',
  'Bebidas (CARTA-5): "Red Bull [Regular, Tropical, Fruta del Dragón, light ]" y "Espumante [Undurraga Free Rosé / 750 cc ]" conservan el espacio antes de "]" tal como impreso.',
 ],
 'secciones': secciones,
}
json.dump(out, open(R + 'content/carta-v2.json', 'w'), ensure_ascii=False, indent=1)
print(json.dumps(diferencias, ensure_ascii=False, indent=1))
