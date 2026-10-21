import pandas as pd, numpy as np
from PIL import Image
ROOT = '/home/claude/almud_bar/'
cat = pd.read_csv(ROOT + '_plan/diag/catalogo.csv').set_index('ref')
FR = '_plan/diag/frames/'

# ref, file(None=catalog), bucket, N(0-1), crop, fx, fy, flags, nota, overrides dict
C = [
# ---- stills
('P189',None,'patio techado',.9,'16:9',50,38,'','Techo de banderines sobre la terraza llena (11 años)'),
('P124',None,'barra',1.0,'16:9',45,38,'','Bartender lanza la botella frente al muro rojo'),
('P090',None,'patio techado',.8,'16:9',50,40,'','Faroles y flecos de papel sobre la gente (Fondita)'),
('P093',None,'barra',.7,'4:5',50,55,'','Barra curva completa con banderines'),
('P348',None,'fiestas/eventos',.9,'4:5',50,45,'violeta;credito @isosur.prod','Multitud de los 12 años desde arriba'),
('P283',None,'fiestas/eventos',.6,'4:5',45,35,'violeta;tercero:Rucalaf (locación a verificar)','Vapor sobre la olla, noche Rucalaf'),
('P290',None,'fiestas/eventos',.5,'4:5',50,60,'violeta;tercero:Rucalaf (locación a verificar)','Olla sobre fogata, noche Rucalaf'),
('P046',None,'patio techado',.7,'1:1',50,40,'baja-res','Túnel de cintas sobre mesas llenas'),
('P184',None,'barra',.8,'4:5',45,40,'','Bartender vierte frente al muro de botellas'),
('P200',None,'barra',.8,'4:5',55,45,'','Bartender de camisa roja sirve, delantal con logo'),
('P073',None,'fiestas/eventos',1.0,'4:5',50,45,'','El 10 de flores: hito de los 10 años'),
('P217',None,'dueños',.9,'4:5',55,35,'violeta;identidad sin confirmar;casi-dup:P221','Torta de los 11 años bajo el letrero ALMUD'),
('P254',None,'barra',.9,'4:5',50,40,'','Dos clientas brindan frente al muro rosa (x6,2)'),
('P210',None,'fiestas/eventos',.7,'4:5',45,40,'flash;caras de clientes','Señora con glitter riendo, 11 años'),
('P204',None,'barra',.9,'4:5',35,30,'','Botella en alto bajo la lámpara de flecos'),
('P221',None,'dueños',1.0,'4:5',50,40,'violeta;identidad sin confirmar','Torta con velas bajo el letrero luminoso ALMUD BAR'),
('P109',None,'barra',.9,'4:5',55,35,'dup:P395,P120','Bartender riendo, camisa floreada, muro rosa'),
('P333',None,'equipo/personal',.9,'4:5',50,40,'credito @isosur.prod','Dos garzonas con corbata y jockey'),
('P371',None,'fiestas/eventos',.7,'4:5',50,45,'violeta','Torta y grupo apretado, 12 años'),
('P359',None,'patio techado',.7,'16:9',50,45,'violeta','Terraza repleta desde arriba, 12 años'),
('P357',None,'terraza descubierta',.6,'4:5',50,50,'violeta','Pérgola iluminada en violeta, patio de noche'),
('P364',None,'fiestas/eventos',.6,'4:5',45,40,'violeta','Mujer de rulos con vaso'),
('P362',None,'barra',.8,'4:5',50,40,'dup:P392','Bartender frente al muro rojo con el cartel ALMUD (3072 px)'),
('P297',None,'tragos',.6,'1:1',50,45,'','Splash rojo en copa coupe (estudio)'),
('P036',None,'equipo/personal',1.0,'4:5',50,40,'','Garzona con pizza mira por sobre el hombro'),
('P195',None,'equipo/personal',.9,'4:5',40,40,'','Garzona con jockey ALMUD y bandeja de tragos'),
('P187',None,'equipo/personal',.8,'4:5',50,45,'','Garzona con corbata lleva tragos entre mesas'),
('P182',None,'patio techado',.7,'4:5',50,40,'','Brindis bajo banderines y estufa'),
('P196',None,'patio techado',.6,'4:5',50,40,'','Terraza bajo banderines y estufa'),
('P198',None,'fiestas/eventos',.9,'4:5',50,35,'','Brindis eufórico con gorro, 11 años'),
('P194',None,'barra',.6,'4:5',50,50,'','Clientes acodados bajo la lámpara de mimbre'),
('P197',None,'equipo/personal',.7,'4:5',50,40,'casi-dup:P333','Dos garzonas posando con jockey'),
('P039',None,'terraza descubierta',.8,'4:5',50,45,'','Patio de noche: guirnaldas, árboles y mesas llenas'),
('P157',None,'vista/Castro',.9,'16:9',50,45,'día;también equipo','El equipo con el mar de Castro detrás'),
('P027',None,'equipo/personal',.7,'4:5',50,40,'','Bartender de bigote y tirantes a cámara'),
('P086',None,'tragos',.6,'4:5',50,50,'','Tres copas con espuma y flores secas'),
('P087',None,'barra',.7,'4:5',45,40,'','Bartender de polera rayada prepara un martini'),
('P097',None,'tragos',.6,'4:5',50,55,'','Copa tallada, muro rosa desenfocado'),
('P092',None,'barra',.7,'4:5',50,40,'','Bartender de delantal naranja agita la coctelera'),
('P347',None,'dueños',.9,'4:5',50,35,'violeta;identidad sin confirmar','Lleva la torta de los 12 años entre la gente'),
('P346',None,'barra',.6,'4:5',50,50,'byn','Blanco y negro: fila de shots'),
('P339',None,'mesas interiores',.6,'4:5',50,45,'','Lámpara de mimbre y muro rojo (3072 px, cálida)'),
('P294',None,'mesas interiores',.6,'4:5',60,40,'tercero:Rucalaf (locación a verificar)','Mujer con boina bajo lámparas de mimbre'),
('P231',None,'barra',.8,'4:5',45,40,'','Bartender riendo con coctelera, muro rojo'),
('P242',None,'equipo/personal',.8,'4:5',50,45,'disfraz','Garzona con corona de flores lleva dos pizzas'),
('P229',None,'fiestas/eventos',.6,'4:5',50,45,'disfraz','Jalogüín frente a la barra rosa'),
('P031',None,'barra',.9,'4:5',50,40,'','Clientas riendo y brindando con tragos de colores'),
('P385',None,'fiestas/eventos',.5,'4:5',50,50,'','Brasas del fogón nuevo (oct-2026)'),
('P394',None,'equipo/personal',.7,'4:5',50,40,'violeta','Garzona con pizza bajo luz violeta'),
('P393',None,'comida',.8,'4:5',50,40,'','Garzón tatuado lleva el plato (3072 px)'),
('P111',None,'fiestas/eventos',.8,'4:5',50,40,'','Músico con guitarra bajo abanicos de papel'),
('P100',None,'fiestas/eventos',.8,'4:5',50,55,'','Músicos acústicos bajo banderines'),
('P101',None,'fiestas/eventos',.7,'4:5',55,40,'','DJ con tocado de abanicos'),
('P108',None,'tragos',.7,'4:5',50,40,'','Brindis de dos copas contra la ventana'),
('P114',None,'sillones',.9,'4:5',45,45,'','Mujer riendo en el sillón de cojines estampados'),
('P107',None,'tragos',.5,'4:5',40,50,'dup:P312','Vaso tiki de madera con flor'),
('P021',None,'patio techado',.6,'4:5',50,45,'','Mesas bajo cintas verticales'),
('P025',None,'equipo/personal',.7,'4:5',50,40,'','Sonrisa con trago frente a las cintas'),
('P003',None,'tragos',.6,'4:5',55,50,'','Negroni sobre el posavaso Almud'),
('P035',None,'terraza descubierta',.6,'4:5',50,50,'','Patio de ripio, mesas llenas, pérgola'),
('P077',None,'equipo/personal',.9,'16:9',50,50,'','El equipo completo tras la barra'),
('P013',None,'tragos',.6,'1:1',60,50,'','Soplete sobre el vaso tallado'),
('P008',None,'tragos',.5,'1:1',50,55,'','Copa balón con menta, pinza'),
('P159',None,'terraza descubierta',.7,'4:5',45,35,'día;credito @estudiouno.prod','Copa de sandía en la terraza florida'),
('P041',None,'mesas interiores',.9,'4:5',50,40,'','Carcajada frente al muro de cintas'),
('P051',None,'equipo/personal',.8,'4:5',50,40,'','Bartender con globos y dos sangrías'),
('P083',None,'fiestas/eventos',.8,'4:5',50,35,'','Pizza en alto entre la multitud'),
('P098',None,'equipo/personal',.8,'4:5',45,50,'','Garzona con chaleco multicolor y pizza'),
('P043',None,'equipo/personal',.8,'4:5',50,40,'','Bartender de rulos ofrece un trago a cámara'),
('P202',None,'equipo/personal',.9,'16:9',50,50,'franjas-negras','Equipo completo tras la barra'),
('P076',None,'mesas interiores',.5,'16:9',50,50,'','Mesas interiores, ventanal de reja, muro rojo'),
('P020',None,'vista/Castro',.5,'16:9',50,55,'día','Techos de Castro y el mar al atardecer'),
('P004',None,'fachada/letrero',.5,'16:9',50,50,'','Puerta de madera vidriada desde dentro'),
('P199',None,'fachada/letrero',.7,'4:5',50,40,'','Megáfono en la puerta de madera'),
('P298',None,'comida',.4,'4:5',50,50,'día','Ceviche en greda negra con pan (3024 px)'),
('P299',None,'comida',.4,'4:5',50,50,'','Tabla de jamón, maní y naranja (3072 px)'),
('P070',None,'comida',.4,'4:5',50,50,'','Tacos de atún en tabla'),
('P029',None,'comida',.6,'4:5',50,60,'','Pizza con rúcula en la mano del garzón'),
('P091',None,'comida',.4,'4:5',50,50,'dup:P300','Cazuela negra con ñoquis'),
('P164',None,'comida',.5,'4:5',50,50,'día;credito @estudiouno.prod','Tabla de picoteo con martini al sol'),
('P169',None,'comida',.4,'4:5',50,45,'día;credito @estudiouno.prod','Cazuela y pan en plato enlozado azul'),
('P174',None,'cuadros/murales',.8,'4:5',50,50,'día','Equipo frente al mural de corazones'),
('P175',None,'equipo/personal',.8,'4:5',50,50,'día','Equipo riendo frente al mural de corazones'),
('P012',None,'cuadros/murales',.6,'16:9',50,50,'baja-res','Barra con el muro de cuadros al fondo'),
('P069',None,'barra',.5,'4:5',50,50,'','Muro de botellas, letrero EXPENDIO DE ALCOHOLES'),
('P252',None,'barra',.7,'16:9',50,55,'byn;credito @mariannefuentealba','Siluetas en la barra (blanco y negro)'),
('P153',None,'dueños',.6,'1:1',50,45,'identidad sin confirmar','Muestra la polera calavera ALMUD BAR'),
('P136',None,'sillones',.6,'16:9',50,50,'baja-res;disfraz','Grupo disfrazado en los sillones'),
# ---- high-res video covers (IG upscaled, effective ~1080 px)
('V014-cover',None,'cuadros/murales',.6,'4:5',50,30,'portada-sobremuestreada','Lámpara de pinzas: el isotipo hecho objeto',{'eff':1080}),
('V030-cover',None,'tragos',.6,'4:5',50,55,'portada-sobremuestreada','Soplete y posavaso de pinzas',{'eff':1080}),
('V051-cover',None,'barra',.5,'4:5',50,45,'','Muro de botellas rosa con flores',{}),
# ---- video frames (file, E, Q, likes from parent video)
('V031-f01',FR+'V031_letrero_0.87s.jpg','fachada/letrero',.7,'16:9',55,40,'video-frame;credito @estudiouno.prod','Letrero luminoso ALMUD BAR (V031 0,9 s)',{'v':'V031','E':4,'Q':3}),
('V031-f02',FR+'V031_puerta_3.27s.jpg','fachada/letrero',.6,'16:9',50,50,'video-frame;credito @estudiouno.prod','Puerta de madera y banderines (V031 3,3 s)',{'v':'V031','E':3,'Q':3}),
('V031-f03',FR+'V031_banderines_6.07s.jpg','patio techado',.5,'16:9',50,40,'video-frame;credito @estudiouno.prod','Banderines en contrapicado (V031 6,1 s)',{'v':'V031','E':4,'Q':3}),
('V031-f04',FR+'V031_mural-ojos_6.60s.jpg','cuadros/murales',.7,'16:9',50,45,'video-frame;credito @estudiouno.prod','Mural Ojo Piojo (V031 6,6 s)',{'v':'V031','E':4,'Q':3}),
('V031-f05',FR+'V031_lamparas_8.53s.jpg','barra',.5,'16:9',35,45,'video-frame;credito @estudiouno.prod','Lámparas de varillas encendidas (V031 8,5 s)',{'v':'V031','E':4,'Q':3}),
('V009-f01',FR+'V009_techo-flecos_2.00s.jpg','patio techado',.5,'9:16',50,45,'video-frame','Techo de flecos con luces (V009 2,0 s)',{'v':'V009','E':5,'Q':3}),
('V084-f01',FR+'V084_marcos-sillon_9.07s.jpg','cuadros/murales',.6,'9:16',50,35,'video-frame;story-480p;caras','Muro negro de marcos de colores (V084 9,1 s)',{'v':'V084','E':3,'Q':1,'L':1.0}),
('V014-f01',FR+'V014_sillones_9.30s.jpg','sillones',.5,'4:5',50,65,'video-frame;muy-oscuro','Rincón de sillones Chesterfield y mesas redondas (V014 9,3 s)',{'v':'V014','E':3,'Q':2}),
('V013-f01',FR+'V013_salon-cuadros_12.00s.jpg','mesas interiores',.8,'9:16',50,45,'video-frame;violeta','Garzona con pizzas en el salón del muro de cuadros (V013 12 s)',{'v':'V013','E':4,'Q':2}),
('V020-f01',FR+'V020_salon-mesas2_15.73s.jpg','mesas interiores',.6,'4:5',50,45,'video-frame','Mesas del salón con risa (V020 15,7 s)',{'v':'V020','E':3,'Q':2}),
('V006-f01',FR+'V006_mural-ojos_9.67s.jpg','cuadros/murales',.6,'4:5',50,45,'video-frame;día','Mural de ojos, primer plano (V006 9,7 s)',{'v':'V006','E':3,'Q':3}),
('V010-f01',FR+'V010_patio-mar_0.00s.jpg','vista/Castro',.6,'4:5',50,40,'video-frame;día;dup:V006 21,9 s','Patio de bancas al atardecer con el mar (V010 0 s)',{'v':'V010','E':4,'Q':3}),
('V002-f01',FR+'V002_corazones-letrero_0.00s.jpg','cuadros/murales',.6,'4:5',45,45,'video-frame;día','Mural de corazones y @ALMUD BAR pintado (V002 0 s)',{'v':'V002','E':3,'Q':3}),
('V002-f02',FR+'V002_techado-cintas_20.30s.jpg','patio techado',.6,'4:5',45,40,'video-frame;día','Techado de cintas al atardecer, lleno (V002 20,3 s)',{'v':'V002','E':4,'Q':3}),
('V028-f01',FR+'V028_brindis-mar_1.80s.jpg','vista/Castro',.7,'4:5',50,40,'video-frame;día;credito @estudiouno.prod','Brindis bajo el bambú con el mar detrás (V028 1,8 s)',{'v':'V028','E':3,'Q':4}),
('V042-f01',FR+'V042_banda-mar_7.33s.jpg','vista/Castro',.8,'4:5',50,40,'video-frame;día;tercero:Isleños (pedir permiso)','Isleños tocando en el patio con el mar (V042 7,3 s)',{'v':'V042','E':4,'Q':4}),
('V056-f01',FR+'V056_fachada_6.20s.jpg','fachada/letrero',.6,'9:16',50,25,'video-frame;subtitulos;tercero:creadores (reel V056)','Fachada con letrero de noche (V056 6,2 s)',{'v':'V056','E':3,'Q':2}),
('V021-f01',FR+'V021_muro-letrero_1.61s.jpg','barra',.5,'4:5',40,50,'video-frame','Muro rosa con el cartel ALMUD (V021 1,6 s, 1080p)',{'v':'V021','E':4,'Q':3}),
('V021-f02',FR+'V021_torta10_7.51s.jpg','fiestas/eventos',.6,'4:5',50,50,'video-frame','Torta con velas 10 (V021 7,5 s, 1080p)',{'v':'V021','E':3,'Q':3}),
('V013-f02',FR+'V013_equipo-poleras_1.60s.jpg','equipo/personal',.7,'4:5',50,40,'video-frame;fondo-gris','Equipo con poleras de pinzas (V013 1,6 s)',{'v':'V013','E':3,'Q':3}),
('V032-f01',FR+'V032_flecos-dia_8.37s.jpg','patio techado',.4,'4:5',50,50,'video-frame;credito @estudiouno.prod','Flecos de colores de día (V032 8,4 s)',{'v':'V032','E':3,'Q':3}),
('V038-f01',FR+'V038_trago-humo_5.00s.jpg','tragos',.5,'4:5',50,60,'video-frame','Coupe roja con ahumador (V038 5 s)',{'v':'V038','E':4,'Q':3}),
]

LP = {'mixto':4,'flash':3,'día':2,'otro':2,'noche cálida':0}
RAT = {'4:5':.8,'16:9':16/9,'1:1':1,'3:4':.75,'9:16':9/16}
rows = []
for c in C:
    ref, f, bucket, N, crop, fx, fy, flags, nota = c[:9]
    ov = c[9] if len(c) > 9 else {}
    src = ov.get('v', ref)
    m = cat.loc[src]
    file = f or m['file']
    W, H = Image.open(ROOT + file).size
    E = ov.get('E', m['epica']); Q = ov.get('Q', m['q_tecnica'])
    ln = ov.get('L', m['likes_norm_era'] if pd.notna(m['likes_norm_era']) else 1.0)
    light = m['light']
    if 'byn' in flags: light = 'otro'
    if ref.startswith('V0') and '-f' in ref:
        light = 'día' if 'día' in flags else ('mixto' if 'violeta' in flags else 'noche cálida')
    eff = ov.get('eff', None)
    Wf, Hf = (W, H)
    if eff:  # upscaled cover: effective short side
        s = eff / min(W, H); Wf, Hf = int(W*s), int(H*s)
    r = RAT[crop]
    cw = int(min(Wf, Hf*r))
    short = min(Wf, Hf)
    Es, Qs = (E-1)/4, (Q-1)/4
    Ls = min(np.log1p(ln)/np.log1p(4), 1)
    base = 100*(0.35*Es + 0.25*Qs + 0.25*Ls + 0.15*N)
    pen = {}
    if short < 600: pen['res'] = 12
    elif short < 800: pen['res'] = 8
    elif short < 1000: pen['res'] = 4
    if LP.get(light, 0): pen['luz'] = LP[light]
    if any(k in flags for k in ['subtitulos','franjas-negras','story-480p']): pen['texto'] = 8 if 'subtitulos' in flags or 'story' in flags else 3
    if 'tercero' in flags: pen['tercero'] = 5
    P = sum(pen.values())
    rows.append(dict(ref=ref, file=file.replace('assets/raw/',''), bucket=bucket, E=E, Q=Q, likes_norm=round(float(ln),2),
        E_s=round(Es,3), Q_s=round(Qs,3), L_s=round(float(Ls),3), N_s=N, base=round(base,1), penalties=';'.join(f'{k}-{v}' for k,v in pen.items()),
        P=P, score=round(base-P,1), light=light, res=f'{W}x{H}', crop=crop, fx=fx, fy=fy, max_w=cw,
        uso=('hero' if cw>=1920 else 'media' if cw>=960 else 'mosaico' if cw>=600 else 'miniatura'),
        flags=flags, nota=nota))
df = pd.DataFrame(rows)
def alt(r):
    W,H=map(int,r.res.split('x'))
    if r.ref in ('V014-cover','V030-cover'): W,H=1080,int(1080*H/W)
    a = '16:9' if r.crop in ('4:5','9:16','3:4','1:1') else '4:5'
    return pd.Series({'crop_alt':a,'max_w_alt':int(min(W,H*RAT[a]))})
df = pd.concat([df, df.apply(alt,axis=1)],axis=1)

QUOTA = {'barra':6,'equipo/personal':5,'patio techado':4,'terraza descubierta':3,'mesas interiores':3,'sillones':3,'cuadros/murales':4,
         'tragos':5,'comida':4,'fiestas/eventos':5,'fachada/letrero':2,'vista/Castro':2,'dueños':2}
CAP = {'dueños':2,'barra':10,'fiestas/eventos':8,'patio techado':7,'equipo/personal':8,'tragos':6,'comida':5}
df = df.sort_values('score', ascending=False).reset_index(drop=True)
sel = []
df = df[~df['flags'].str.contains('casi-dup')].reset_index(drop=True)
for b, q in QUOTA.items():
    sel += list(df[df.bucket==b].index[:q])
mix = lambda s: sum(df.loc[i,'light']=='mixto' for i in s)
for i in df.index:
    if len(sel) >= 60: break
    if i in sel: continue
    b = df.loc[i,'bucket']
    if sum(df.loc[j,'bucket']==b for j in sel) >= CAP.get(b, 6): continue
    if df.loc[i,'light']=='mixto' and mix(sel) >= 10: continue
    sel.append(i)
top = df.loc[sel].sort_values('score', ascending=False).reset_index(drop=True)
top.insert(0, 'rank', range(1, len(top)+1))
top['quota'] = ''
for b, q in QUOTA.items():
    idx = top[top.bucket==b].index[:q]
    top.loc[idx, 'quota'] = 'cuota'
rest = df[~df.index.isin(sel)].copy()
top.to_csv('/tmp/claude-0/-home-claude/011b3bf8-fa11-50bd-ba3e-4cc567dfb832/scratchpad/top.csv', index=False)
rest.to_csv('/tmp/claude-0/-home-claude/011b3bf8-fa11-50bd-ba3e-4cc567dfb832/scratchpad/rest.csv', index=False)
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 200)
print(top[['rank','ref','bucket','score','base','penalties','crop','max_w','light','quota']].to_string())
print(top.bucket.value_counts()); print(top.light.value_counts()); print(top.crop.value_counts())
print(rest[['ref','bucket','score']].head(25).to_string())
