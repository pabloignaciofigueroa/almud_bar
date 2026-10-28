// Capturas del dossier · sitio final (raíz, la que está en almudbar.pages.dev)
// computador 1440x900 @1.5 · celular 390x844 @2.5
// Uso: python3 -m http.server 8765 (desde la raíz del repo) y NODE_PATH=$(npm root -g) node dossier/capture.js
const {chromium}=require('playwright');
const OUT=__dirname+'/shots/'; const U='http://localhost:8765/';
// [clave, selector, modo, x]  modos: top · center · offset(fracción del alto) · px · bottom
const S=[
 ['lugar-a','.lugar','top'],['lugar-b','.lleno','center'],['lugar-c','.rincones','center'],
 ['tragos-a','.tragos','top'],['tragos-peter','.peter','center'],['tragos-b','.tragos__band','offset',0.45],['tragos-c','.tragos__named','center'],
 ['comida-a','.comida','top'],['comida-b','.co__more','center'],
 ['quien-a','.quien','top'],['quien-b','.qz','center'],
 ['eventos-a','.eventos','top'],['eventos-b','.fs','center'],
 ['equipo-a','.equipo','top'],['equipo-b','.eqz','center'],
 ['resenas','.resenas','center'],
 ['cierre-a','.donde','top'],['cierre-b','.donde__t','center'],
 ['pie','.pie','bottom'],
];
// salta directo con Lenis (el desplazamiento suave del sitio) para que no se quede a medio camino
async function to(p,y){await p.evaluate(y=>{y=Math.max(0,y);if(window.__lenis)window.__lenis.scrollTo(y,{immediate:true,force:true});else scrollTo(0,y)},y)}
async function go(p,y){
  const cur=await p.evaluate(()=>scrollY);
  const step=cur<y?380:-380;
  for(let s=cur;(step>0?s<y:s>y);s+=step){await p.mouse.wheel(0,step);await p.waitForTimeout(110)}
  await p.waitForTimeout(600);
  await to(p,y); await p.waitForTimeout(2800);
}
async function pos(p,sel,mode,x,vh){
  return p.evaluate(([sel,mode,x,vh])=>{const e=document.querySelector(sel); if(!e) return -1;
    const top=e.getBoundingClientRect().top+scrollY, h=e.offsetHeight;
    if(mode==='top')return top; if(mode==='offset')return top+h*x; if(mode==='px')return top+x;
    if(mode==='bottom')return Math.min(top+h-vh, document.documentElement.scrollHeight-vh); return top+(h-vh)/2;},[sel,mode,x,vh]);
}
async function shoot(p,vh,prefix,list){
  for(const [k,sel,mode,x] of list){
    const y=await pos(p,sel,mode,x,vh); if(y<0){console.log('no',sel);continue}
    await go(p,y);
    const y2=await pos(p,sel,mode,x,vh);   // las fotos que cargan al acercarse cambian el alto: se vuelve a medir
    if(Math.abs(y2-y)>4){await to(p,y2); await p.waitForTimeout(2600);}
    await p.screenshot({path:`${OUT}${prefix}-${k}.jpg`,type:'jpeg',quality:84});
  }
}
async function flip(p,vh,prefix){
  const y=await pos(p,'.eqz','center',0,vh); await go(p,y);
  await p.evaluate(()=>{const f=[...document.querySelectorAll('.flip')]; [1,4].forEach(i=>f[i]&&f[i].click())});
  await p.waitForTimeout(1800); await p.screenshot({path:`${OUT}${prefix}-equipo-flip.jpg`,type:'jpeg',quality:84});
}
// SOLO=clave1,clave2 rehace solo esas capturas de computador
const SOLO=process.env.SOLO?process.env.SOLO.split(','):null;
(async()=>{const b=await chromium.launch();
  if(SOLO){const c=await b.newContext({viewport:{width:1440,height:900},deviceScaleFactor:1.5,locale:'es-CL'});const p=await c.newPage();await p.goto(U);await p.waitForTimeout(9000);
    await shoot(p,900,'d',S.filter(x=>SOLO.includes(x[0])));await b.close();return}
  const c=await b.newContext({viewport:{width:1440,height:900},deviceScaleFactor:1.5,locale:'es-CL'});
  const p=await c.newPage(); await p.goto(U);
  await p.waitForTimeout(900); await p.screenshot({path:OUT+'d-carga-1.jpg',type:'jpeg',quality:84});
  await p.waitForTimeout(1300); await p.screenshot({path:OUT+'d-carga-2.jpg',type:'jpeg',quality:84});
  await p.waitForTimeout(1500); await p.screenshot({path:OUT+'d-apertura.jpg',type:'jpeg',quality:84});
  await p.waitForTimeout(6000); await p.screenshot({path:OUT+'d-hero.jpg',type:'jpeg',quality:84});
  await p.waitForTimeout(4000); await p.screenshot({path:OUT+'d-hero2.jpg',type:'jpeg',quality:84});
  await shoot(p,900,'d',S); await flip(p,900,'d'); await c.close();
  const m=await b.newContext({viewport:{width:390,height:844},deviceScaleFactor:2.5,isMobile:true,hasTouch:true,locale:'es-CL'});
  const q=await m.newPage(); await q.goto(U); await q.waitForTimeout(1500);
  await q.screenshot({path:OUT+'m-carga.jpg',type:'jpeg',quality:84});
  await q.waitForTimeout(9000); await q.screenshot({path:OUT+'m-hero.jpg',type:'jpeg',quality:84});
  await q.waitForTimeout(4000); await q.screenshot({path:OUT+'m-hero2.jpg',type:'jpeg',quality:84});
  await shoot(q,844,'m',S); await flip(q,844,'m');
  const q2=await m.newPage(); await q2.goto(U); await q2.waitForTimeout(9000);
  await q2.click('[data-lang]'); await q2.waitForTimeout(800);
  await go(q2,await pos(q2,'.lugar','top',0,844)); await q2.screenshot({path:OUT+'m-en-lugar.jpg',type:'jpeg',quality:84});
  await q2.evaluate(()=>{try{localStorage.removeItem('almud-idioma')}catch(e){}});
  const q3=await m.newPage(); await q3.goto(U+'carta/'); await q3.waitForTimeout(3000);
  await q3.screenshot({path:OUT+'m-carta.jpg',type:'jpeg',quality:84});
  await q3.evaluate(()=>scrollTo(0,700)); await q3.waitForTimeout(1500); await q3.screenshot({path:OUT+'m-carta2.jpg',type:'jpeg',quality:84});
  await m.close();
  const d=await b.newContext({viewport:{width:1440,height:900},deviceScaleFactor:1.5,locale:'es-CL'});
  const p3=await d.newPage(); await p3.goto(U+'carta/'); await p3.waitForTimeout(3000);
  await p3.screenshot({path:OUT+'d-carta.jpg',type:'jpeg',quality:84});
  await b.close();})();
