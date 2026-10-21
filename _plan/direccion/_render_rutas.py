import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageOps

R = "/home/claude/almud_bar"
S = "/tmp/claude-0/-home-claude/011b3bf8-fa11-50bd-ba3e-4cc567dfb832/scratchpad"
OUT = R + "/_plan/direccion"
T = S + "/ttf/"
def F(name, size): return ImageFont.truetype(T + name, size)
SIX = lambda s: F("six-caps-latin-400-normal.ttf", s)
OS3 = lambda s: F("oswald-latin-300-normal.ttf", s)
OS4 = lambda s: F("oswald-latin-400-normal.ttf", s)
OS6 = lambda s: F("oswald-latin-600-normal.ttf", s)

IG = R + "/assets/raw/ig/"
P = {
 "P189": IG+"DM_Ih5dyVKH_07.jpg", "P093": IG+"DAMHps8JVVr_07.jpg", "P090": IG+"DAMHps8JVVr_04.jpg",
 "P039": IG+"Cqn78DFp5Nm_00.jpg", "P114": IG+"DBMtYELSzNS_14.jpg", "P339": IG+"Dbg3ekilC4P_02.jpg",
 "P297": IG+"DYsZ0GNo_88_00.jpg", "P086": IG+"DAMHps8JVVr_00.jpg", "P184": IG+"DM_Ih5dyVKH_02.jpg",
 "P362": IG+"Dbok2NyFNdb_05.jpg", "P097": IG+"DAMHps8JVVr_11.jpg", "P036": IG+"CqEI2nSJP2__00.jpg",
 "P393": IG+"DeNQ8A2lDgg_02.jpg", "P305": IG+"DY0AUvhlHjI_13.jpg", "P091": IG+"DAMHps8JVVr_05.jpg",
 "P254": IG+"DU35ZDPCBcH_00.jpg", "P031": IG+"CpVyxXJJrhO_00.jpg", "P041": IG+"CrMRBMNpdIF_00.jpg",
 "P194": IG+"DM_Ih5dyVKH_12.jpg", "P198": IG+"DM_Ih5dyVKH_16.jpg", "P199": IG+"DM_Ih5dyVKH_17.jpg",
 "P333": IG+"DaWM8rlo1FR_00.jpg", "P003": IG+"Cmce2h1J3Wl_00.jpg", "P070": IG+"C7HV31OLXTJ_00.jpg",
 "V014": IG+"C9BDvFvJk4z_00.jpg",
 "OJO": IG+"C1dQ670t1Z3_00.jpg", "ANIV9": IG+"CvN-aMGpq5j_00.jpg", "PRIDE": IG+"DaJPccpomwO_00.jpg",
 "NEGW": IG+"Ddmu3OdFLxs_01.jpg", "FOND": IG+"DdMQYLYlMK4_00.jpg", "MAMBO": IG+"DMilf4pprEi_00.jpg",
 "V009": R+"/_plan/diag/frames/V009_techo-flecos_2.00s.jpg", "V002": R+"/_plan/diag/frames/V002_techado-cintas_20.30s.jpg",
 "V031L": R+"/_plan/diag/frames/V031_letrero_0.87s.jpg", "OJOS": R+"/_plan/diag/frames/V031_mural-ojos_6.60s.jpg",
 "C2": S+"/c2hi-1.jpg", "C1": S+"/c1hi-1.jpg", "C7": S+"/c7hi-1.jpg",
 "PROF": R+"/assets/raw/hl/profile_pic.jpg",
}
LOGO_C = R+"/brand/png/almud-horizontal-claro.png"
LOGO_D = R+"/brand/png/almud-horizontal-oscuro.png"

def cover(key, w, h, fx=.5, fy=.5):
    im = Image.open(P[key] if key in P else key).convert("RGB")
    sw, sh = im.size
    s = max(w/sw, h/sh)
    if s > 1.0:  # never upscale: crop a smaller region and flag it in sketch by leaving it (still scale for preview)
        pass
    nw, nh = round(sw*s), round(sh*s)
    im = im.resize((nw, nh), Image.LANCZOS)
    x = int((nw-w)*fx); y = int((nh-h)*fy)
    return im.crop((x, y, x+w, y+h))

def logo(path, h):
    im = Image.open(path).convert("RGBA")
    bb = im.getbbox(); im = im.crop(bb)
    w = round(im.width*h/im.height)
    return im.resize((w, h), Image.LANCZOS)

def text(d, xy, s, font, fill, anchor="la"):
    d.text(xy, s, font=font, fill=fill, anchor=anchor)

def tw(d, s, font):
    b = d.textbbox((0,0), s, font=font); return b[2]-b[0]

def swatches(d, x, y, cols, w=150, h=70, ink="#f6ecdc"):
    for i,(hx,name) in enumerate(cols):
        d.rectangle([x+i*w, y, x+i*w+w-6, y+h], fill=hx, outline="#77706a", width=1)
        text(d, (x+i*w, y+h+8), f"{name}  {hx}", OS4(16), ink)

def pair(desk, phone, bg, path, label_ink):
    W = 1440 + 60 + 390 + 60; H = 900 + 110
    c = Image.new("RGB", (W, H), "#2a2a2a")
    d = ImageDraw.Draw(c)
    text(d, (30, 22), "Desktop 1440×900", OS4(22), "#bbbbbb")
    text(d, (1530, 22), "Teléfono 390×844", OS4(22), "#bbbbbb")
    c.paste(desk, (30, 70)); c.paste(phone, (1530, 70))
    c.save(path, "JPEG", quality=84, optimize=True)
    print(path, os.path.getsize(path)//1024, "KB")

def btn(d, x, y, label, bg, fg, font, padx=22, h=48):
    w = tw(d, label, font) + padx*2
    d.rectangle([x, y, x+w, y+h], fill=bg)
    text(d, (x+padx, y+h/2), label, font, fg, "lm")
    return w

# ------------------------------------------------------------------ RUTA A
DAY = {"bg":"#171515","ink":"#f6ecdc","mute":"#bdb6ad","barra":"#ff3f6c","dia":"#40b9c2"}
def ruta_a():
    W,H = 1440,900
    im = Image.new("RGB",(W,H),DAY["bg"]); d = ImageDraw.Draw(im)
    m = 32
    # nav
    lg = logo(LOGO_C, 58); im.paste(lg,(m,18),lg)
    x = 690
    for s in ["El lugar","Tragos","Comida","Eventos"]:
        text(d,(x,46),s,OS4(18),DAY["ink"],"lm"); x += tw(d,s,OS4(18))+34
    btn(d, W-m-tw(d,"Ver la carta",OS6(17))-44, 22, "Ver la carta", DAY["barra"], "#171515", OS6(17))
    # right: Ojo Piojo device — día color field, P189 en tres franjas
    rx, rw = 760, W-760
    d.rectangle([rx,88,W,H], fill=DAY["dia"])
    strips = [(0.05,0.10),(0.42,0.5),(0.80,0.9)]
    sh = (H-88-4*22)//3
    src = Image.open(P["P189"]).convert("RGB")
    sw = rw-2*28
    sc = sw/src.width; full = src.resize((sw, round(src.height*sc)), Image.LANCZOS)
    for i,(fy,_) in enumerate(strips):
        y0 = int((full.height-sh)*fy)
        im.paste(full.crop((0,y0,sw,y0+sh)), (rx+28, 88+22+i*(sh+22)))
    # left poster
    text(d,(m-6,170),"MIÉRCOLES",SIX(300),DAY["ink"])
    text(d,(m,505),"PISCOLEIN & GIN TONIC",OS6(44),DAY["dia"])
    text(d,(m,565),"$ 4.500  ·  de 18:00 a 22:00 hrs",OS4(26),DAY["ink"])
    text(d,(m,640),"Coctelería de autor, comida & música bonita desde 2014",OS4(24),DAY["ink"])
    text(d,(m,680),"Abrimos de Mar a Sáb a las 18:00hrs  ·  Serrano 325, Castro",OS3(22),DAY["mute"])
    w = btn(d,m,740,"Ver la carta",DAY["barra"],"#171515",OS6(19),h=54)
    text(d,(m+w+28,767),"Cómo llegar",OS4(19),DAY["ink"],"lm")
    d.line([m+w+28,782,m+w+28+tw(d,"Cómo llegar",OS4(19)),782],fill=DAY["ink"],width=2)
    x2=m+w+28+tw(d,"Cómo llegar",OS4(19))+36
    text(d,(x2,767),"Escríbanos al DM",OS4(19),DAY["ink"],"lm")
    d.line([x2,782,x2+tw(d,"Escríbanos al DM",OS4(19)),782],fill=DAY["ink"],width=2)
    text(d,(m,860),"* Siempre sujeto a stock! *",OS3(16),DAY["mute"])
    # phone
    pw,ph=390,844
    p = Image.new("RGB",(pw,ph),DAY["bg"]); q=ImageDraw.Draw(p); pm=16
    lg = logo(LOGO_C,40); p.paste(lg,(pm,14),lg)
    btn(q,pw-pm-tw(q,"Carta",OS6(15))-36,12,"Carta",DAY["barra"],"#171515",OS6(15),padx=18,h=44)
    q.rectangle([0,70,pw,70+400],fill=DAY["dia"])
    sw2 = pw-2*16; sc=sw2/src.width; full2=src.resize((sw2,round(src.height*sc)),Image.LANCZOS)
    sh2=(400-4*14)//3
    for i,(fy,_) in enumerate(strips):
        y0=int((full2.height-sh2)*fy); p.paste(full2.crop((0,y0,sw2,y0+sh2)),(16,70+14+i*(sh2+14)))
    text(q,(pm-3,478),"MIÉRCOLES",SIX(150),DAY["ink"])
    text(q,(pm,640),"PISCOLEIN & GIN TONIC",OS6(24),DAY["dia"])
    text(q,(pm,676),"$ 4.500 · de 18:00 a 22:00 hrs",OS4(17),DAY["ink"])
    text(q,(pm,712),"Coctelería de autor, comida & música",OS4(17),DAY["ink"])
    text(q,(pm,736),"bonita desde 2014",OS4(17),DAY["ink"])
    text(q,(pm,770),"Abrimos de Mar a Sáb a las 18:00hrs",OS3(16),DAY["mute"])
    text(q,(pm,794),"Serrano 325, Castro  ·  Cómo llegar",OS3(16),DAY["mute"])
    pair(im,p,DAY["bg"],OUT+"/ruta-a-viewport.jpg",DAY["ink"])

# ------------------------------------------------------------------ RUTA B
CB = {"bg":"#140e12","ink":"#f1e3d8","mute":"#c9ad9c","barra":"#ff3f6c","brasa":"#e6874c"}
def ruta_b():
    W,H=1440,900
    im = cover("P189",W,H,.5,.22)
    # neutral scrim bottom third
    sc = Image.new("L",(1,H))
    for y in range(H):
        t = min(1,max(0,(y-H*0.42)/(H*0.30))); top = max(0,1-y/130)*0.6
        sc.putpixel((0,y),int(255*max(t*0.86,top)))
    black = Image.new("RGB",(W,H),"#0c0809"); im = Image.composite(black,im,sc.resize((W,H)))
    d=ImageDraw.Draw(im); m=32
    # nav (no bar)
    for i,s in enumerate(["El lugar","Tragos","Comida","Eventos","Carta"]):
        pass
    x=m
    text(d,(m,40),"El lugar     Tragos     Comida     Con quién     Eventos",OS4(18),CB["ink"],"lm")
    btn(d,W-m-tw(d,"Ver la carta",OS6(17))-44,16,"Ver la carta",CB["barra"],"#140e12",OS6(17))
    lg = logo(LOGO_C,210); im.paste(lg,(m-4,H-210-160),lg)
    text(d,(m,H-128),"Coctelería de autor, comida & música bonita desde 2014",OS4(26),CB["ink"])
    text(d,(m,H-84),"Abrimos de Mar a Sáb a las 18:00hrs  ·  Serrano 325, Castro",OS3(22),CB["mute"])
    text(d,(W-m,H-84),"Cómo llegar     Escríbanos al DM",OS4(20),CB["ink"],"ra")
    pw,ph=390,844
    p = cover("P189",pw,ph,.5,.15)
    sc = Image.new("L",(1,ph))
    for y in range(ph):
        t=min(1,max(0,(y-ph*0.45)/(ph*0.25))); top=max(0,1-y/110)*0.6
        sc.putpixel((0,y),int(255*max(t*0.88,top)))
    p = Image.composite(Image.new("RGB",(pw,ph),"#0c0809"),p,sc.resize((pw,ph)))
    q=ImageDraw.Draw(p); pm=16
    text(q,(pm,36),"Menú",OS4(17),CB["ink"],"lm")
    btn(q,pw-pm-tw(q,"Ver la carta",OS6(15))-36,14,"Ver la carta",CB["barra"],"#140e12",OS6(15),padx=18,h=44)
    lg=logo(LOGO_C,104); p.paste(lg,(pm-2,ph-104-210),lg)
    text(q,(pm,ph-178),"Coctelería de autor, comida &",OS4(19),CB["ink"])
    text(q,(pm,ph-152),"música bonita desde 2014",OS4(19),CB["ink"])
    text(q,(pm,ph-108),"Abrimos de Mar a Sáb a las 18:00hrs",OS3(16),CB["mute"])
    text(q,(pm,ph-84),"Serrano 325, Castro",OS3(16),CB["mute"])
    text(q,(pm,ph-46),"Cómo llegar    ·    Escríbanos al DM",OS4(17),CB["ink"])
    pair(im,p,CB["bg"],OUT+"/ruta-b-viewport.jpg",CB["ink"])

# ------------------------------------------------------------------ RUTA C
CC = {"bg":"#fbfaf7","ink":"#1b1a2e","azul":"#2023e4","mag":"#ec008c","mute":"#4a4860","noche":"#150b12"}
def ruta_c():
    W,H=1440,900
    im = Image.new("RGB",(W,H),CC["bg"]); d=ImageDraw.Draw(im); m=32
    # photo plate right, bleeding
    ph_ = cover("P189",640,H,.5,.25); im.paste(ph_,(W-640,0))
    lg=logo(LOGO_D,44); im.paste(lg,(m,28),lg)
    text(d,(330,50),"El lugar    Tragos    Comida    Eventos",OS4(18),CC["ink"],"lm")
    # carta cover sheet
    text(d,(m-4,120),"COCTELERÍA DE AUTOR,",SIX(138),CC["azul"])
    text(d,(m-4,285),"COMIDA & MÚSICA BONITA",SIX(138),CC["azul"])
    text(d,(m,458),"desde 2014  ·  Serrano 325, Castro  ·  Abrimos de Mar a Sáb a las 18:00hrs",OS4(20),CC["mute"])
    # today's promo as carta row
    y=520
    text(d,(m,y),"MIÉRCOLES",OS6(40),CC["azul"])
    text(d,(m,y+56),"PISCOLEIN & GIN TONIC  ·  de 18:00 a 22:00 hrs",OS4(22),CC["ink"])
    text(d,(760,y+4),"$ 4.500",OS6(40),CC["mag"],"ra")
    # carta sample rows
    rows=[("PINCHE GÜEY","$ 8.800"),("TE ESPERO EN LA CUNETA","$ 7.800"),("OTRA COSA MARIPOSA","$ 5.900")]
    yy=640
    for n,pr in rows:
        text(d,(m,yy),n,OS6(26),CC["azul"]); text(d,(760,yy),pr,OS6(26),CC["mag"],"ra"); yy+=44
    btn(d,m,800,"Ver la carta completa",CC["azul"],"#ffffff",OS6(19),h=54)
    text(d,(m+300,827),"Cómo llegar",OS4(19),CC["ink"],"lm")
    text(d,(m+440,827),"Escríbanos al DM",OS4(19),CC["ink"],"lm")
    pw,ph=390,844
    p = Image.new("RGB",(pw,ph),CC["bg"]); q=ImageDraw.Draw(p); pm=16
    p.paste(cover("P189",pw,340,.5,.2),(0,64))
    lg=logo(LOGO_D,38); p.paste(lg,(pm,13),lg)
    text(q,(pw-pm,32),"Carta",OS6(17),CC["azul"],"rm")
    text(q,(pm-2,418),"COCTELERÍA DE AUTOR,",SIX(70),CC["azul"])
    text(q,(pm-2,502),"COMIDA & MÚSICA BONITA",SIX(70),CC["azul"])
    text(q,(pm,594),"desde 2014 · Serrano 325, Castro",OS4(16),CC["mute"])
    text(q,(pm,640),"MIÉRCOLES",OS6(24),CC["azul"]); text(q,(pw-pm,640),"$ 4.500",OS6(24),CC["mag"],"ra")
    text(q,(pm,676),"PISCOLEIN & GIN TONIC · de 18:00 a 22:00 hrs",OS4(16),CC["ink"])
    text(q,(pm,712),"Abrimos de Mar a Sáb a las 18:00hrs",OS3(16),CC["mute"])
    btn(q,pm,770,"Ver la carta completa",CC["azul"],"#ffffff",OS6(16),h=48)
    pair(im,p,CC["bg"],OUT+"/ruta-c-viewport.jpg",CC["ink"])

# ------------------------------------------------------------------ MOODBOARDS
def board(path, bg, ink, title, idea, tiles, sw, typespec):
    W,H=2000,1300
    c=Image.new("RGB",(W,H),bg); d=ImageDraw.Draw(c)
    text(d,(40,30),title,SIX(110),ink)
    text(d,(40,150),idea,OS4(26),ink)
    for (key,x,y,w,h,fx,fy) in tiles:
        if key.startswith("LOGO"):
            lg=logo(LOGO_C if key=="LOGO_C" else LOGO_D,h); c.paste(lg,(x,y),lg); continue
        c.paste(cover(key,w,h,fx,fy),(x,y))
    swatches(d,40,1160,sw,w=210,h=56,ink=ink)
    typespec(c,d)
    c.save(path,"JPEG",quality=82,optimize=True); print(path,os.path.getsize(path)//1024,"KB")

def mood_a():
    bg,ink="#171515","#f6ecdc"
    tiles=[("OJO",40,210,360,450,.5,.3),("ANIV9",410,210,360,450,.5,.5),("PRIDE",780,210,300,450,.4,.5),
           ("P189",1090,210,420,560,.5,.3),("P362",1520,210,440,560,.5,.4),
           ("P254",40,670,300,470,.5,.3),("P297",350,670,300,470,.5,.5),("P184",660,670,300,470,.5,.3),
           ("MAMBO",970,780,300,360,.5,.45),("P036",1280,780,300,360,.5,.4),("P093",1590,780,370,360,.5,.5)]
    def ts(c,d):
        pass
    sw=[("#171515","negro afiche"),("#f6ecdc","papel"),("#ff3f6c","barra · acción"),("#f26343","Mar"),
        ("#40b9c2","Mié"),("#cd0b61","Jue"),("#fac307","Vie"),("#06aa6b","Sáb")]
    board(OUT+"/ruta-a.jpg",bg,ink,"A · EL AFICHE DE HOY",
          "En esta página, cada día de la semana se vuelve un afiche de Almud: negro, Six Caps, un color de franja por día (Ojo Piojo).",tiles,sw,ts)

def mood_b():
    bg,ink="#140e12","#f1e3d8"
    tiles=[("P189",40,210,560,740,.5,.25),("V009",610,210,300,540,.5,.4),("P090",920,210,420,540,.5,.2),
           ("V002",1350,210,300,540,.5,.3),("P039",1660,210,300,540,.5,.5),
           ("P093",610,760,380,380,.5,.5),("P114",1000,760,300,380,.5,.3),("P041",1310,760,320,380,.5,.4),("P031",1640,760,320,380,.5,.5),
           ("P339",40,960,280,180,.5,.3),("OJOS",330,960,270,180,.5,.5)]
    sw=[("#140e12","noche"),("#46201a","salón"),("#f1e3d8","tinta (luz)"),("#ff3f6c","barra · acción"),("#e6874c","brasa · 1 campo")]
    board(OUT+"/ruta-b.jpg",bg,ink,"B · BAJO LAS CINTAS",
          "En esta página, el techo de cintas de la terraza se vuelve el cielo que cubre cada capítulo.",tiles,sw,lambda c,d:None)

def mood_c():
    bg,ink="#fbfaf7","#1b1a2e"
    tiles=[("C2",40,210,300,880,.5,0),("C1",350,210,300,880,.5,0),("C7",660,210,300,560,.5,.0),
           ("P003",970,210,330,420,.5,.5),("P070",1310,210,330,420,.5,.5),("P297",1650,210,310,420,.5,.5),
           ("P189",970,640,330,450,.5,.3),("P036",1310,640,330,450,.5,.4),("P086",1650,640,310,450,.5,.5),
           ("LOGO_D",660,800,0,110,0,0)]
    sw=[("#fbfaf7","hoja"),("#2023e4","azul carta"),("#ec008c","magenta precio"),("#1b1a2e","tinta"),("#150b12","noche (Eventos)")]
    board(OUT+"/ruta-c.jpg",bg,ink,"C · LA CARTA DE LA CASA",
          "En esta página, la carta oficial de Almud se vuelve el índice del bar entero: cada rincón, trago y plato es una línea.",tiles,sw,lambda c,d:None)

ruta_a(); ruta_b(); ruta_c(); mood_a(); mood_b(); mood_c()
