import subprocess, tempfile, glob, sys, numpy as np, shutil
from PIL import Image, ImageFilter
R='/home/claude/almud_bar/assets/raw/'
O='/home/claude/almud_bar/_plan/diag/frames/'
J=[('V031','ig/DFWLrRxyvVB_00.mp4',0.8,1.7,'letrero'),('V031','ig/DFWLrRxyvVB_00.mp4',2.6,3.6,'puerta'),
('V031','ig/DFWLrRxyvVB_00.mp4',4.4,6.2,'banderines'),('V031','ig/DFWLrRxyvVB_00.mp4',6.6,8.3,'mural-ojos'),
('V031','ig/DFWLrRxyvVB_00.mp4',8.4,10.3,'lamparas'),('V009','ig/C5WAi8PLHni_00.mp4',0,7.0,'techo-flecos'),
('V084','hl/hl_tiki_night_41.mp4',8.6,10.6,'marcos-sillon'),('V014','ig/C9BDvFvJk4z_00.mp4',8.8,9.9,'sillones'),
('V013','ig/C8peqOkJ2nJ_00.mp4',11.5,12.4,'salon-cuadros'),('V020','ig/C-YrpVjpCqN_00.mp4',4.2,5.0,'salon-mesas'),
('V020','ig/C-YrpVjpCqN_00.mp4',14.8,15.8,'salon-mesas2'),('V006','ig/C3VODtYsjNX_00.mp4',9.5,11.2,'mural-ojos'),
('V006','ig/C3VODtYsjNX_00.mp4',21,23.5,'patio-mar'),('V002','ig/Cm6yntfIzol_00.mp4',0,0.8,'corazones-letrero'),
('V002','ig/Cm6yntfIzol_00.mp4',1.5,5.5,'corazones'),('V010','ig/C5jk0aAJNYi_00.mp4',0,0.7,'patio-mar'),
('V028','ig/DEYU6RjyjoC_00.mp4',1.8,3.0,'brindis-mar'),('V042','ig/DXzcB3QzWQT_00.mp4',7.2,9.2,'banda-mar'),
('V056','ig/DcuYoBrtSTo_00.mp4',5.2,7.0,'fachada'),('V021','ig/C-dwJHLyPpU_00.mp4',1.4,2.2,'muro-letrero'),
('V021','ig/C-dwJHLyPpU_00.mp4',6.9,7.6,'torta10'),('V014','ig/C9BDvFvJk4z_00.mp4',0,0.6,'letrero'),
('V002','ig/Cm6yntfIzol_00.mp4',19.2,20.4,'techado-cintas'),('V023','ig/DAJLkTHJmFf_00.mp4',3.6,4.6,'barra-lamparas'),
('V013','ig/C8peqOkJ2nJ_00.mp4',1.2,2.4,'equipo-poleras'),('V032','ig/DGLxTmGJ3ZV_00.mp4',7.5,8.8,'flecos-dia'),
('V038','ig/DOO7fgniNI6_00.mp4',0,16.5,'trago-humo')]
for ref,v,t0,t1,lab in J:
    td=tempfile.mkdtemp()
    subprocess.run(['ffmpeg','-loglevel','error','-ss',str(t0),'-to',str(t1),'-i',R+v,'-q:v','1',f'{td}/f_%04d.png'],check=True)
    best=None
    for k,f in enumerate(sorted(glob.glob(td+'/*.png'))):
        g=np.asarray(Image.open(f).convert('L'),dtype=float)
        lap=4*g[1:-1,1:-1]-g[:-2,1:-1]-g[2:,1:-1]-g[1:-1,:-2]-g[1:-1,2:]
        s=lap.var()
        if best is None or s>best[0]: best=(s,f,k)
    im=Image.open(best[1]).convert('RGB')
    # assume ~30fps for timestamp estimate
    fps=float(eval(subprocess.check_output(['ffprobe','-v','error','-select_streams','v','-show_entries','stream=r_frame_rate','-of','csv=p=0',R+v]).decode().strip()))
    t=t0+best[2]/fps
    name=f'{ref}_{lab}_{t:.2f}s.jpg'
    im.save(O+name,quality=92); print(name, im.size, round(best[0],1))
    shutil.rmtree(td)
